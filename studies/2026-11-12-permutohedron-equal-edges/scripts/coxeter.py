"""Exact Coxeter fans of A3, B3, H3 and the deformation cones of their Coxeter permutohedra.

Field Q(sqrt d) with exact fractions (d = 2 for A3, B3; d = 5 for H3). Everything here is exact.
Theory used (credited, not ours): generalized permutohedra (Postnikov 2009) and Coxeter generalized permutohedra
(Ardila, Castillo, Eur, Postnikov 2020): a polytope is in the closed deformation cone of the W-permutohedron iff its normal
fan coarsens the Coxeter fan; it is then fixed (up to translation) by its edge lengths l_e >= 0 on the walls e of the fan,
subject to the closing condition around every 2-face.
"""
from fractions import Fraction as Fr
import itertools


class QF:
    __slots__ = ('a', 'b')
    D = 5

    def __init__(s, a=0, b=0):
        s.a = a if isinstance(a, Fr) else Fr(a)
        s.b = b if isinstance(b, Fr) else Fr(b)

    def __add__(s, o):
        o = o if isinstance(o, QF) else QF(o)
        return QF(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __neg__(s):
        return QF(-s.a, -s.b)

    def __sub__(s, o):
        return s + (-(o if isinstance(o, QF) else QF(o)))

    def __rsub__(s, o):
        return (-s) + o

    def __mul__(s, o):
        o = o if isinstance(o, QF) else QF(o)
        return QF(s.a * o.a + QF.D * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - QF.D * s.b * s.b
        assert n != 0
        return QF(s.a / n, -s.b / n)

    def __truediv__(s, o):
        o = o if isinstance(o, QF) else QF(o)
        return s * o.inv()

    def __eq__(s, o):
        o = o if isinstance(o, QF) else QF(o)
        return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def iszero(s):
        return s.a == 0 and s.b == 0

    def sign(s):
        """exact sign of a + b sqrt(D)"""
        a, b = s.a, s.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        # opposite signs: compare a^2 with D b^2
        if a * a > QF.D * b * b:
            return 1 if a > 0 else -1
        return 1 if b > 0 else -1

    def __lt__(s, o):
        return (s - o).sign() < 0

    def __gt__(s, o):
        return (s - o).sign() > 0

    def __float__(s):
        return float(s.a) + float(s.b) * QF.D ** 0.5

    def key(s):
        return (s.a, s.b)

    def __repr__(s):
        if s.b == 0:
            return str(s.a)
        return f'({s.a}{"+" if s.b >= 0 else ""}{s.b}*sqrt{QF.D})'


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def vsub(u, v):
    return tuple(a - b for a, b in zip(u, v))


def vadd(u, v):
    return tuple(a + b for a, b in zip(u, v))


def vscale(c, u):
    return tuple(c * a for a in u)


def vkey(u):
    return tuple(x.key() for x in u)


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def matmul(A, B):
    return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), QF(0)) for j in range(3)) for i in range(3))


def matvec(A, v):
    return tuple(sum((A[i][k] * v[k] for k in range(3)), QF(0)) for i in range(3))


def mkey(A):
    return tuple(vkey(r) for r in A)


def det3(A):
    return dot(A[0], cross(A[1], A[2]))


def inv3(A):
    """inverse of a 3x3 matrix whose ROWS are A[0..2]"""
    d = det3(A)
    c0, c1, c2 = cross(A[1], A[2]), cross(A[2], A[0]), cross(A[0], A[1])
    # inverse has columns c0/d, c1/d, c2/d
    di = d.inv()
    return tuple(tuple(c[i] * di for c in (c0, c1, c2)) for i in range(3))


def rank(rows):
    """exact rank of a list of vectors (lists of QF) by Gaussian elimination"""
    M = [list(r) for r in rows]
    if not M:
        return 0
    n = len(M[0])
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if not M[i][c].iszero()), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        iv = M[r][c].inv()
        M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and not M[i][c].iszero():
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def simple_roots(name):
    if name in ('A3', 'B3'):
        QF.D = 2
        s = QF(0, Fr(1, 2))   # 1/sqrt2
        if name == 'A3':
            return [(QF(0), s, -s), (s, -s, QF(0)), (QF(0), s, s)], None
        return [(s, -s, QF(0)), (QF(0), s, -s), (QF(0), QF(0), QF(1))], None
    QF.D = 5
    phi = QF(Fr(1, 2), Fr(1, 2))
    iphi = QF(Fr(-1, 2), Fr(1, 2))
    h = Fr(1, 2)
    return [(QF(1), QF(0), QF(0)), (-phi * h, QF(h), -iphi * h), (QF(0), QF(-1), QF(0))], None


EXPECT = {'A3': (24, {(0, 1): 3, (1, 2): 3, (0, 2): 2}), 'B3': (48, {(0, 1): 3, (1, 2): 4, (0, 2): 2}),
          'H3': (120, {(0, 1): 5, (1, 2): 3, (0, 2): 2})}


class Fan:
    def __init__(self, name):
        self.name = name
        al, _ = simple_roots(name)
        self.al = al
        self.checks = []
        # Coxeter matrix check: <a_i, a_j> = -cos(pi/m)
        cosm = {2: QF(0), 3: QF(Fr(-1, 2)), 4: None, 5: None}
        for (i, j), m in EXPECT[name][1].items():
            g = dot(al[i], al[j])
            if m == 2:
                ok = g.iszero()
            elif m == 3:
                ok = g == QF(Fr(-1, 2))
            elif m == 4:
                ok = g * g == QF(Fr(1, 2)) and g.sign() < 0
            else:
                ok = g == -QF(Fr(1, 4), Fr(1, 4))   # -phi/2
            self.checks.append((f'{name} Coxeter m({i+1},{j+1})={m}', ok))
        for i in range(3):
            self.checks.append((f'{name} |a{i+1}|=1', dot(al[i], al[i]) == QF(1)))
        I = tuple(tuple(QF(1 if i == j else 0) for j in range(3)) for i in range(3))
        S = []
        for a in al:
            S.append(tuple(tuple((QF(1) if i == j else QF(0)) - 2 * a[i] * a[j] for j in range(3)) for i in range(3)))
        self.S = S
        # group by BFS; element index = chamber index
        els = [I]
        idx = {mkey(I): 0}
        k = 0
        while k < len(els):
            g = els[k]
            for s in S:
                h = matmul(g, s)
                kk = mkey(h)
                if kk not in idx:
                    idx[kk] = len(els)
                    els.append(h)
            k += 1
        self.W = els
        self.Widx = idx
        self.checks.append((f'{name} |W| = {EXPECT[name][0]}', len(els) == EXPECT[name][0]))
        # fundamental weights: <w_i, a_j> = delta_ij ; w_i = column i of inv(A) with A rows a_j
        Ai = inv3(tuple(al))
        om = [tuple(Ai[r][i] for r in range(3)) for i in range(3)]
        for i in range(3):
            for j in range(3):
                assert dot(om[i], al[j]) == QF(1 if i == j else 0)
        self.om = om
        rays, rayidx, raytype = [], {}, []
        for g in els:
            for i in range(3):
                v = matvec(g, om[i])
                kk = vkey(v)
                if kk not in rayidx:
                    rayidx[kk] = len(rays)
                    rays.append(v)
                    raytype.append(i)
        self.rays, self.rayidx, self.raytype = rays, rayidx, raytype
        self.chray = [tuple(rayidx[vkey(matvec(g, om[i]))] for i in range(3)) for g in els]
        # neighbours: chamber g -- chamber g s_i across the wall dropping ray type i; root g a_i is positive on chamber g
        self.nb = [[idx[mkey(matmul(g, S[i]))] for i in range(3)] for g in els]
        walls, wallidx = [], {}
        for c, g in enumerate(els):
            for i in range(3):
                d = self.nb[c][i]
                kk = (min(c, d), max(c, d))
                if kk not in wallidx:
                    wallidx[kk] = len(walls)
                    walls.append((c, d, i, matvec(g, al[i])))   # root positive on chamber c
        self.walls, self.wallidx = walls, wallidx
        # positive roots (up to sign) and wall -> root index
        roots, rootidx = [], {}
        self.wallroot = []
        for (c, d, i, r) in walls:
            kk = vkey(r)
            nk = vkey(tuple(-x for x in r))
            if kk in rootidx:
                self.wallroot.append(rootidx[kk])
            elif nk in rootidx:
                self.wallroot.append(rootidx[nk])
            else:
                rootidx[kk] = len(roots)
                roots.append(r)
                self.wallroot.append(rootidx[kk])
        self.roots = roots
        # faces: cycles of walls around each ray
        faces = []
        for r, v in enumerate(rays):
            t = raytype[r]
            c0 = next(c for c in range(len(els)) if self.chray[c][t] == r)
            others = [i for i in range(3) if i != t]
            cyc = []
            cur, step = c0, 0
            while True:
                i = others[step % 2]
                d = self.nb[cur][i]
                w = wallidx[(min(cur, d), max(cur, d))]
                rv = walls[w][3] if walls[w][0] == cur else tuple(-x for x in walls[w][3])
                # v_next - v_cur = - l * rv
                cyc.append((w, tuple(-x for x in rv)))
                cur = d
                step += 1
                if cur == c0 and step % 2 == 0:
                    break
            faces.append(cyc)
        self.faces = faces
        R, E, C = len(rays), len(walls), len(els)
        self.checks.append((f'{name} every wall on exactly 2 faces',
                            all(sum(w == ww for f in faces for (ww, _) in f) == 2 for w in range(E))))
        self.checks.append((f'{name} Euler V-E+F = {C}-{E}+{R} = 2', C - E + R == 2))

    # ---- linear algebra of the cone ----
    def vertex(self, c, h):
        g = self.W[c]
        M = tuple(matvec(g, self.om[i]) for i in range(3))
        Mi = inv3(M)
        hv = [h[self.chray[c][i]] for i in range(3)]
        return tuple(sum((Mi[r][k] * hv[k] for k in range(3)), QF(0)) for r in range(3))

    def lengths(self, h):
        """wall-crossing edge lengths l_e(h); the closed deformation cone is {h : all l_e >= 0}"""
        V = [self.vertex(c, h) for c in range(len(self.W))]
        return [dot(vsub(V[c], V[d]), r) for (c, d, i, r) in self.walls]

    def L_matrix(self):
        R = len(self.rays)
        cols = []
        for j in range(R):
            h = [QF(1) if k == j else QF(0) for k in range(R)]
            cols.append(self.lengths(h))
        return [[cols[j][e] for j in range(R)] for e in range(len(self.walls))]

    def K_rows(self):
        E = len(self.walls)
        rows = []
        for cyc in self.faces:
            for x in range(3):
                row = [QF(0)] * E
                for (w, u) in cyc:
                    row[w] = row[w] + u[x]
                rows.append(row)
        return rows

    def allowed(self, f):
        cyc = self.faces[f]
        out = []
        for m in range(1 << len(cyc)):
            s = [QF(0)] * 3
            for k, (w, u) in enumerate(cyc):
                if m >> k & 1:
                    s = [a + b for a, b in zip(s, u)]
            if all(x.iszero() for x in s):
                out.append(m)
        return out

    def sym_group(self):
        """symmetries of the fan used for congruence: W, and W x {+-1} when -1 is not in W (A3)"""
        mats = list(self.W)
        negI = tuple(tuple(QF(-1 if i == j else 0) for j in range(3)) for i in range(3))
        if mkey(negI) not in self.Widx:
            mats += [matmul(negI, g) for g in self.W]
        return mats

    def wall_perm(self, X):
        rmap = [self.rayidx[vkey(matvec(X, v))] for v in self.rays]
        chkey = {frozenset(rs): c for c, rs in enumerate(self.chray)}
        cmap = [chkey[frozenset(rmap[r] for r in rs)] for rs in self.chray]
        perm = []
        for (c, d, i, r) in self.walls:
            a, b = cmap[c], cmap[d]
            perm.append(self.wallidx[(min(a, b), max(a, b))])
        return perm

    def support(self, verts):
        return [max(dot(v, r) for v in verts) for r in self.rays]
