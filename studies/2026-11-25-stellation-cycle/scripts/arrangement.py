"""Exact boundary edges of a filled polyhedron that is a union of cells of a plane arrangement (Q(sqrt5), pure Python).

The polyhedron is given by a membership oracle member(sg), where sg(i) is the exact sign of n_i.x - d_i at a sample point (never 0 there).
Every edge of the polyhedron lies on a line where two candidate planes meet. Each such line is cut at every other candidate plane; at the
midpoint m of each piece, the planes through the line split a small disc round it into sectors; the sector sample point is
m + (tiny) w, with w the sum of the two rays bounding the sector, so the signs are sign(n.w) for the planes through the line and
sign(n.m - d) for the rest (exact, no epsilon needed). The piece is an edge of the polyhedron iff the in/out pattern round the line is not
constant and not one flat half-plane split (exactly two changes on two opposite rays). The planes of the changing rays carry faces."""
from q5 import Q, dot, cross, vsub, vadd, vsc, det3, iszero, vkey, pkey


class Arrangement:
    def __init__(self, planes):
        """planes: list of (n, d) meaning the half-space n.x <= d is 'inside' (sign -1)."""
        self.P = []           # canonical planes (n, d) with first nonzero coordinate of n = +1
        self.index = {}
        self.src = []         # for each input plane: (canonical index, orientation +1/-1)
        for n, d in planes:
            piv = next(x for x in n if x.sign() != 0)
            nn = tuple(y / piv for y in n); dd = d / piv
            o = 1 if piv.sign() > 0 else -1          # sign(n.x - d) = o * sign(nn.x - dd)
            k = (vkey(nn), dd.key())
            if k not in self.index:
                self.index[k] = len(self.P); self.P.append((nn, dd))
            self.src.append((self.index[k], o))

    def edges(self, member, keep=None):
        """keep(m): optional exact prefilter on piece midpoints (False = skip the piece, it cannot be an edge)."""
        P = self.P; NP = len(P)
        lines = {}
        for i in range(NP):
            for j in range(i + 1, NP):
                u = cross(P[i][0], P[j][0])
                if iszero(u): continue
                p = solve_line(P[i], P[j], u)
                lk = (pkey(u), vkey(p))
                if lk not in lines:
                    lines[lk] = (p, u)
        out = []          # (line key, p, u, t0, t1, face plane indices)
        for lk, (p, u) in lines.items():
            thru = [k for k in range(NP) if dot(P[k][0], u).sign() == 0 and (dot(P[k][0], p) - P[k][1]).sign() == 0]
            ts = {}
            for k in range(NP):
                nu = dot(P[k][0], u)
                if nu.sign() == 0: continue
                t = (P[k][1] - dot(P[k][0], p)) / nu
                ts[t.key()] = t
            T = sorted(ts.values(), key=lambda q: q.f())
            for a in range(len(T) - 1):           # exact order check of neighbours (float sort)
                assert T[a] < T[a + 1]
            rays = sector_rays(u, thru, P)
            for a in range(len(T) - 1):
                t0, t1 = T[a], T[a + 1]
                m = vadd(p, vsc((t0 + t1) / 2, u))
                if keep is not None and not keep(m): continue
                base = {}
                def sg_at(w):
                    def sg(i):
                        if i in thr_set:
                            return dot(P[i][0], w).sign()
                        if i not in base:
                            base[i] = (dot(P[i][0], m) - P[i][1]).sign()
                        return base[i]
                    return sg
                thr_set = set(thru)
                ins = []
                for r in range(len(rays)):
                    w = vadd(rays[r][0], rays[(r + 1) % len(rays)][0])
                    sgf = sg_at(w)
                    ins.append(bool(member(lambda src_i, sgf=sgf: self.src[src_i][1] * sgf(self.src[src_i][0]))))
                L = len(rays)
                ch = [r for r in range(L) if ins[r - 1] != ins[r]]     # ray r lies between sector r-1 and sector r
                if not ch: continue
                if len(ch) == 2 and rays[ch[0]][1] == rays[ch[1]][1]:
                    continue                                             # one flat face across the line
                out.append((lk, p, u, t0, t1, sorted({rays[r][1] for r in ch})))
        return out


def solve_line(Pi, Pj, u):
    """the point of the line {n_i.x = d_i, n_j.x = d_j} closest to... (any fixed point: the one with u.x = 0)"""
    from q5 import solve3
    x = solve3(Pi[0], Pi[1], Pj[0], Pj[1], u, Q(0))
    assert x is not None
    return x


def sector_rays(u, thru, P):
    """the 2r rays (trace directions of the planes through the line) in the disc at right angles to u, sorted by angle; (ray, plane)"""
    import functools
    R = []
    for k in thru:
        t = cross(u, P[k][0]); R.append((t, k)); R.append((vsc(Q(-1), t), k))
    e1 = R[0][0]; e2 = cross(u, e1)
    def half(r):
        x, y = dot(r, e1), dot(r, e2)
        return 0 if (y.sign() > 0 or (y.sign() == 0 and x.sign() > 0)) else 1
    def cmp(A, B):
        ha, hb = half(A[0]), half(B[0])
        if ha != hb: return ha - hb
        xa, ya, xb, yb = dot(A[0], e1), dot(A[0], e2), dot(B[0], e1), dot(B[0], e2)
        c = (xa * yb - xb * ya).sign()
        assert c != 0
        return -c
    return sorted(R, key=functools.cmp_to_key(cmp))
