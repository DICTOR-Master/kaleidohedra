"""Arrangement of the sides of symmetric triangles (one axis), exact where the field is exact.

A triangle is (b, w, a): base depth b, base half-width w, apex (0, a); depth d is measured down from
the top point O of the circle of diameter 1.  Points are (x, d).  Field elements may be Fractions or
QF (exact a + b sqrt(D), studies/2026-11-12-yantra-regions-45) or Fractions of stored decimals; with
eps > 0, points closer than eps are merged and |cross| <= eps_cross counts as collinear (used only for
the yantras stored as decimals).

Counts returned by analyse():
  faces        bounded regions of the arrangement of all 3n sides
  tri, quad    split of the bounded regions by TRUE corners (a vertex where a line only ends on a side,
               or passes straight through, is not a corner)
  rings        {depth c: number of regions inside exactly c triangles}
  odd, odd_tri, odd_quad   regions inside an odd number of triangles (#103 Proposition 3) and their split
  star         star-point count (Chapati and Chapati 2026, Zenodo 10.5281/zenodo.23188650): for every odd
               c below the deepest level, the convex corners of the outline of {depth >= c}; plus the
               number of regions at the deepest level (the trikona counted as one)
  star_by      the star-point terms, outermost first
Checks inside analyse (raise on failure): Euler V - E + F = 2 (connected); the depth is the same from
every side of a region; every edge lies on exactly one side and changes the depth by exactly one; the sum
over regions of depth x area equals the sum of the triangles' areas (exactly, or to eps_cross).
"""
from fractions import Fraction as Fr
from functools import cmp_to_key


def sgn(z):
    if hasattr(z, 'sign'):
        return z.sign()
    return (z > 0) - (z < 0)


def cross(o, p, q):
    return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])


class Arr:
    def __init__(self, tris, eps=None, eps_cross=None):
        self.T = tris                         # list of (b, w, a)
        self.eps, self.epsc = eps, eps_cross
        self.P = []                           # vertices

    # ---------------------------------------------------------------- numbers
    def zero(self, z):
        if self.eps is None:
            return sgn(z) == 0
        return abs(z) <= self.epsc

    def s(self, z):
        return 0 if self.zero(z) else sgn(z)

    def pid(self, p):
        if self.eps is None:
            for k, q in enumerate(self.P):
                if q[0] == p[0] and q[1] == p[1]:
                    return k
        else:
            e = self.eps
            for k, q in enumerate(self.P):
                if abs(q[0] - p[0]) <= e and abs(q[1] - p[1]) <= e:
                    return k
        self.P.append(p)
        return len(self.P) - 1

    # ---------------------------------------------------------------- geometry
    def verts(self, i):
        b, w, a = self.T[i]
        return ((-w, b), (w, b), (0 * w, a))     # left corner, right corner, apex

    def segments(self):
        out = []
        for i in range(len(self.T)):
            L, R, A = self.verts(i)
            out += [(L, R, i), (R, A, i), (A, L, i)]
        return out

    def inside_strict(self, i, m):
        L, R, A = self.verts(i)
        s1, s2, s3 = self.s(cross(L, R, m)), self.s(cross(R, A, m)), self.s(cross(A, L, m))
        return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)

    def interior_left(self, i, p, q):
        """is triangle i's interior on the left of the directed line p->q (which lies on its side)?"""
        L, R, A = self.verts(i)
        c = ((L[0] + R[0] + A[0]) / 3, (L[1] + R[1] + A[1]) / 3)
        return sgn(cross(p, q, c)) > 0

    def build(self):
        segs = self.segments()
        cuts = [[] for _ in segs]
        tol = None if self.eps is None else Fr(1, 10 ** 20)
        for si, s in enumerate(segs):
            cuts[si].append((Fr(0), self.pid(s[0])))
            cuts[si].append((Fr(1), self.pid(s[1])))
        for si in range(len(segs)):
            P1, P2, _ = segs[si]
            for ti in range(si + 1, len(segs)):
                P3, P4, _ = segs[ti]
                d = (P2[0] - P1[0]) * (P4[1] - P3[1]) - (P2[1] - P1[1]) * (P4[0] - P3[0])
                if self.zero(d):
                    # parallel; collinear overlap is not expected in these figures: check
                    if self.zero(cross(P1, P2, P3)) and self.zero(cross(P1, P2, P4)):
                        raise ValueError('collinear overlapping sides')
                    continue
                p = ((P3[0] - P1[0]) * (P4[1] - P3[1]) - (P3[1] - P1[1]) * (P4[0] - P3[0])) / d
                q = ((P3[0] - P1[0]) * (P2[1] - P1[1]) - (P3[1] - P1[1]) * (P2[0] - P1[0])) / d
                if tol is None:
                    ok = 0 <= p <= 1 and 0 <= q <= 1
                else:
                    ok = -tol <= p <= 1 + tol and -tol <= q <= 1 + tol
                if ok:
                    X = (P1[0] + p * (P2[0] - P1[0]), P1[1] + p * (P2[1] - P1[1]))
                    k = self.pid(X)
                    cuts[si].append((p, k)); cuts[ti].append((q, k))
        # edges with the triangle sides that carry them
        E = {}
        for si, s in enumerate(segs):
            cs = sorted(cuts[si], key=lambda t: t[0])
            ids = []
            for _, k in cs:
                if not ids or ids[-1] != k:
                    ids.append(k)
            for k in range(len(ids) - 1):
                u, v = ids[k], ids[k + 1]
                if u == v:
                    continue
                E.setdefault((u, v), set()).add(s[2]); E.setdefault((v, u), set()).add(s[2])
        self.E = E
        nb = {}
        for (u, v) in E:
            nb.setdefault(u, []).append(v)
        P = self.P

        def cmp_at(o):
            def half(v):
                dx, dy = P[v][0] - P[o][0], P[v][1] - P[o][1]
                sy, sx = sgn(dy), sgn(dx)
                return 0 if (sy > 0 or (sy == 0 and sx > 0)) else 1
            def c(v1, v2):
                h1, h2 = half(v1), half(v2)
                if h1 != h2:
                    return h1 - h2
                return -sgn(cross(P[o], P[v1], P[v2]))
            return c
        for u in nb:
            nb[u].sort(key=cmp_to_key(cmp_at(u)))
        self.nb = nb
        used, faces, fof = set(), [], {}
        for e in E:
            if e in used:
                continue
            f = []; cur = e
            while cur not in used:
                used.add(cur); fof[cur] = len(faces); f.append(cur)
                p, q = cur
                L = nb[q]; k = L.index(p)
                cur = (q, L[(k - 1) % len(L)])
            faces.append(f)
        self.faces, self.fof = faces, fof
        # f is traversed with the face on the LEFT of each half-edge? check orientation by area sign
        return self

    def farea2(self, f):
        P = self.P
        return sum(P[u][0] * P[v][1] - P[v][0] * P[u][1] for (u, v) in f)

    def depth_left(self, e):
        p, q = self.P[e[0]], self.P[e[1]]
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        on = self.E[e]
        dep = 0
        for i in range(len(self.T)):
            if i in on:
                dep += 1 if self.interior_left(i, p, q) else 0
            else:
                dep += 1 if self.inside_strict(i, m) else 0
        return dep

    def analyse(self):
        self.build()
        P = self.P
        A = [self.farea2(f) for f in self.faces]
        neg = [k for k, a in enumerate(A) if sgn(a) < 0]
        # orientation convention: walk with nb[(k-1)] -> bounded faces have one sign; detect it
        if len(neg) == 1:
            outer, sign_bd = neg[0], 1
        else:
            pos = [k for k, a in enumerate(A) if sgn(a) > 0]
            assert len(pos) == 1, ('outer face not unique', len(neg), len(pos))
            outer, sign_bd = pos[0], -1
        nV, nE, nF = len(P), len(self.E) // 2, len(self.faces)
        assert nV - nE + nF == 2, ('Euler', nV, nE, nF)
        # depth of every face from one half-edge, checked on all of its half-edges
        depth = {}
        for k, f in enumerate(self.faces):
            if k == outer:
                continue
            ds = set()
            for e in f:
                # the face lies to the left of e when sign_bd = 1 (counter-clockwise bounded faces)
                ee = e if sign_bd == 1 else (e[1], e[0])
                ds.add(self.depth_left(ee))
            assert len(ds) == 1, ('depth not constant on a face', ds)
            depth[k] = ds.pop()
        for e, on in self.E.items():           # each edge changes the depth by the number of sides on it
            a, b = self.fof[e], self.fof[(e[1], e[0])]
            da, db = depth.get(a, 0), depth.get(b, 0)
            assert abs(da - db) == len(on) and len(on) == 1, ('edge depth jump', da, db, on)
        # true corners
        def corners(f):
            n = len(f); k = 0
            for j in range(n):
                u, v = f[j - 1][0], f[j][0]
                w_ = f[j][1]
                if not self.zero(cross(P[u], P[v], P[w_])):
                    k += 1
            return k
        bounded = [k for k in range(nF) if k != outer]
        cs = {k: corners(self.faces[k]) for k in bounded}
        tot_area = sum(A[k] for k in bounded) * sign_bd
        wsum = sum(A[k] * depth[k] for k in bounded) * sign_bd
        tsum = sum(2 * w * abs(a - b) for (b, w, a) in self.T)
        assert self.zero(wsum - tsum), 'depth-weighted area differs from the sum of triangle areas'
        rings = {}
        for k in bounded:
            rings[depth[k]] = rings.get(depth[k], 0) + 1
        odd = [k for k in bounded if depth[k] % 2 == 1]
        # star points: convex corners of the outline of {depth >= c}
        maxd = max(depth.values())
        star_by = []
        for c in range(1, maxd, 2):
            star_by.append(self.convex_outline_corners(depth, c, sign_bd, outer))
        star_by.append(rings.get(maxd, 0))
        res = dict(V=nV, E=nE, faces=len(bounded),
                   tri=sum(1 for k in bounded if cs[k] == 3), quad=sum(1 for k in bounded if cs[k] == 4),
                   other=sum(1 for k in bounded if cs[k] not in (3, 4)),
                   rings={c: rings[c] for c in sorted(rings)}, odd=len(odd),
                   odd_tri=sum(1 for k in odd if cs[k] == 3), odd_quad=sum(1 for k in odd if cs[k] == 4),
                   odd_other=sum(1 for k in odd if cs[k] not in (3, 4)),
                   maxdepth=maxd, star=sum(star_by), star_by=star_by, area2=tot_area)
        return res

    def convex_outline_corners(self, depth, c, sign_bd, outer):
        """At each vertex, runs of consecutive faces with depth >= c (in the rotation order); a run that
        is not the whole neighbourhood is a corner of the outline; it is convex when its angle is < 180
        degrees, i.e. when the turn from its first ray to its last ray is a strict left turn (ccw)."""
        P = self.P
        cnt = 0
        for v, L in self.nb.items():
            n = len(L)
            # the face between ray L[j] and ray L[j+1] (ccw): it is the face on the left of (v -> L[j+1])
            # when bounded faces are ccw ... determine via fof of half-edge (v, L[j+1]) or its twin.
            inreg = []
            for j in range(n):
                a_, b_ = L[j], L[(j + 1) % n]
                # face containing the sector from ray a_ to ray b_ (ccw): it is left of (v->b_)?  The face
                # walk next(cur=(p,q)) = (q, nb[q][k-1]) traces faces with the face on the right of
                # half-edges when nb is ccw.  Use the face of half-edge (a_ -> v) whose next is (v, L[idx-1]).
                f = self.fof[(b_, v)]          # half-edge into v from b_, next goes to L[(idx(b_)-1)] = a_
                d = 0 if f == outer else depth[f]
                inreg.append(d >= c)
            if all(inreg) or not any(inreg):
                continue
            # runs
            for j in range(n):
                if inreg[j] and not inreg[j - 1]:
                    k = j
                    while inreg[(k + 1) % n]:
                        k += 1
                    r1, r2 = L[j], L[(k + 1) % n]
                    if sgn(cross(P[v], P[r1], P[r2])) > 0:
                        cnt += 1
        return cnt


# exact numbers a + b sqrt(D), copied unchanged (less __float__) from studies/2026-11-12-yantra-regions-45/scripts/yantra_regions45.py
class QF:
    """a + b sqrt(D), a, b Fractions; D a positive non-square Fraction (class attribute). Exact sign by a^2 vs b^2 D."""
    __slots__ = ('a', 'b')
    D = None

    def __init__(self, a, b=0):
        self.a = Fr(a); self.b = Fr(b)

    @staticmethod
    def of(x):
        return x if isinstance(x, QF) else QF(x, 0)

    def __add__(s, o): o = QF.of(o); return QF(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = QF.of(o); return QF(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return QF.of(o) - s
    def __neg__(s): return QF(-s.a, -s.b)
    def __mul__(s, o):
        if isinstance(o, QF): return QF(s.a * o.a + s.b * o.b * QF.D, s.a * o.b + s.b * o.a)
        o = Fr(o); return QF(s.a * o, s.b * o)
    __rmul__ = __mul__
    def __truediv__(s, o):
        if not isinstance(o, QF): o = Fr(o); return QF(s.a / o, s.b / o)
        n = o.a * o.a - o.b * o.b * QF.D
        return QF((s.a * o.a - s.b * o.b * QF.D) / n, (s.b * o.a - s.a * o.b) / n)
    def __rtruediv__(s, o): return QF.of(o) / s
    def __pow__(s, k):
        r = QF(1); x = s
        while k:
            if k & 1: r = r * x
            x = x * x; k >>= 1
        return r
    def sign(s):
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sb == 0 or sa == sb: return sa if sa else sb
        if sa == 0: return sb
        d = s.a * s.a - s.b * s.b * QF.D
        return sa if d > 0 else sb
    def __eq__(s, o):
        if isinstance(o, (int, Fr)): return s.b == 0 and s.a == o
        if isinstance(o, QF): return s.a == o.a and s.b == o.b
        return NotImplemented
    def __hash__(s): return hash(s.a) if s.b == 0 else hash((s.a, s.b))
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def __abs__(s): return -s if s.sign() < 0 else s
    def __bool__(s): return not (s.a == 0 and s.b == 0)
    def __str__(s): return f'{s.a} + {s.b}*sqrt({QF.D})'
    __repr__ = __str__


