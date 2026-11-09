"""Exact polar-line (Hopscotch) toolkit for sweeps S(mu) = {a_k . x <= b0_k + b1_k mu}.

Field: Q(sqrt d) with exact Fractions (class F). Vertices are found in floating point and then
re-derived and certified exactly (exact solve, exact feasibility, exact tight sets, Euler check).
Walls are found by walking the line: on an open interval every corner is affine in mu,
x(mu) = p + mu q, and the next wall is the smallest root > s of a_k.x(mu) = b_k(mu) over all
corners and all planes not already tight, which is exactly the 4x4 concurrency determinant.
dicto-big-brother, ~/geom/bin/python. Study 2026-11-09-dual-sweeps.
"""
from fractions import Fraction as Q
import itertools, math
import numpy as np

D = 5  # set by caller via set_field


def set_field(d):
    global D
    D = d


class F:
    __slots__ = ('a', 'b')

    def __init__(self, a=0, b=0):
        if isinstance(a, F):
            self.a, self.b = a.a, a.b
            return
        self.a = Q(a)
        self.b = Q(b)

    @staticmethod
    def c(x):
        return x if isinstance(x, F) else F(x)

    def __add__(s, o):
        o = F.c(o); return F(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __sub__(s, o):
        o = F.c(o); return F(s.a - o.a, s.b - o.b)

    def __rsub__(s, o):
        return F.c(o) - s

    def __neg__(s):
        return F(-s.a, -s.b)

    def __mul__(s, o):
        o = F.c(o); return F(s.a * o.a + D * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - D * s.b * s.b
        if n == 0:
            raise ZeroDivisionError
        return F(s.a / n, -s.b / n)

    def __truediv__(s, o):
        return s * F.c(o).inv()

    def __rtruediv__(s, o):
        return F.c(o) * s.inv()

    def sign(s):
        a, b = s.a, s.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        # opposite signs: compare a^2 with D b^2
        if a > 0:
            return 1 if a * a > D * b * b else -1
        return 1 if D * b * b > a * a else -1

    def __eq__(s, o):
        o = F.c(o); return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0

    def __float__(s):
        return float(s.a) + float(s.b) * math.sqrt(D)

    def __repr__(s):
        if s.b == 0:
            return str(s.a)
        if s.a == 0:
            return f'{s.b}*r{D}'
        return f'({s.a} + {s.b}*r{D})'

    def sym(s):
        import sympy as sp
        return sp.Rational(s.a.numerator, s.a.denominator) + sp.Rational(s.b.numerator, s.b.denominator) * sp.sqrt(D)


ZERO, ONE = F(0), F(1)


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def solve3(A, b):
    d = det3(A)
    if d == ZERO:
        return None
    out = []
    for j in range(3):
        M = [[(b[i] if k == j else A[i][k]) for k in range(3)] for i in range(3)]
        out.append(det3(M) / d)
    return out


def det4(M):
    tot = ZERO
    for j in range(4):
        minor = [[M[i][k] for k in range(4) if k != j] for i in range(1, 4)]
        t = M[0][j] * det3(minor)
        tot = tot + t if j % 2 == 0 else tot - t
    return tot


class Sweep:
    """planes: list of (a (3 F), b0 F, b1 F, family str)."""

    def __init__(self, planes):
        self.P = planes
        self.A = np.array([[float(x) for x in p[0]] for p in planes])
        self.B0 = np.array([float(p[1]) for p in planes])
        self.B1 = np.array([float(p[2]) for p in planes])
        n = len(planes)
        self.triples = np.array(list(itertools.combinations(range(n), 3)))

    def rhs(self, k, mu):
        return self.P[k][1] + self.P[k][2] * mu

    def vertices(self, mu):
        """exact corners at exact mu: list of (x (3 F), frozenset tight)."""
        muf = float(mu)
        b = self.B0 + self.B1 * muf
        T = self.triples
        M = self.A[T]  # (t,3,3)
        dets = np.linalg.det(M)
        ok = np.abs(dets) > 1e-9
        T, M = T[ok], M[ok]
        X = np.linalg.solve(M, b[T][..., None])[..., 0]
        feas = np.all(X @ self.A.T <= b[None, :] + 1e-7, axis=1)
        T, X = T[feas], X[feas]
        seen = {}
        for t, x in zip(T, X):
            key = tuple(np.round(x, 6))
            if key in seen:
                continue
            seen[key] = t
        out = {}
        for key, t in seen.items():
            Am = [list(self.P[k][0]) for k in t]
            bm = [self.rhs(k, mu) for k in t]
            x = solve3(Am, bm)
            tight = []
            good = True
            for k, p in enumerate(self.P):
                r = dot(p[0], x) - self.rhs(k, mu)
                s = r.sign()
                if s > 0:
                    good = False; break
                if s == 0:
                    tight.append(k)
            if not good:
                raise RuntimeError('float vertex not exactly feasible')
            out[tuple(x)] = frozenset(tight)
        return [(list(k), v) for k, v in out.items()]

    def structure(self, mu):
        V = self.vertices(mu)
        cnt = {}
        for _, T in V:
            for k in T:
                cnt[k] = cnt.get(k, 0) + 1
        facets = {k for k, c in cnt.items() if c >= 3}
        edges = []
        bonds = set()
        for i, j in itertools.combinations(range(len(V)), 2):
            common = V[i][1] & V[j][1] & facets
            if len(common) >= 2:
                edges.append((i, j))
                bonds.add(frozenset(common) if len(common) == 2 else frozenset(common))
        faces = {k: cnt[k] for k in facets}
        euler = len(V) - len(edges) + len(facets)
        return dict(V=V, facets=facets, faces=faces, edges=edges, bonds=bonds, euler=euler)

    def census(self, st):
        fam = {}
        for k, n in st['faces'].items():
            key = (self.P[k][3], n)
            fam[key] = fam.get(key, 0) + 1
        return dict(sorted(fam.items()))

    def affine_vertices(self, s):
        """at a generic s: each corner as p + mu q (exact)."""
        out = []
        for x, T in self.vertices(s):
            T = sorted(T)
            for t in itertools.combinations(T, 3):
                Am = [list(self.P[k][0]) for k in t]
                if det3(Am) != ZERO:
                    p = solve3(Am, [self.P[k][1] for k in t])
                    q = solve3(Am, [self.P[k][2] for k in t])
                    out.append((p, q, frozenset(T), t))
                    break
        return out

    def roots(self, s):
        """all roots mu of a_k.(p+mu q) = b0_k + b1_k mu for corners at s and planes not tight there.
        Also asserts that corners with >3 tight planes are tight identically (s generic)."""
        res = []
        for p, q, T, t in self.affine_vertices(s):
            for k, pl in enumerate(self.P):
                num = pl[1] - dot(pl[0], p)
                den = dot(pl[0], q) - pl[2]
                if k in T:
                    if not (num == ZERO and den == ZERO):
                        raise RuntimeError(f'sample {s} is a wall (corner {t} + plane {k})')
                    continue
                if den == ZERO:
                    continue
                res.append((num / den, t, k))
        return res

    def next_wall(self, s):
        r = [x for x in self.roots(s) if x[0] > s]
        if not r:
            return None, []
        w = min(r, key=lambda x: float(x[0]))
        w = min((x[0] for x in r if abs(float(x[0]) - float(w[0])) < 1e-9), key=lambda z: z)  # exact min
        return w, [x for x in r if x[0] == w]

    def prev_wall(self, s):
        r = [x for x in self.roots(s) if x[0] < s]
        if not r:
            return None
        return max((x[0] for x in r), key=lambda z: float(z))

    def wall_det(self, quad):
        """4x4 concurrency determinant of 4 planes as a function of mu; returns (D(0), D(1), D(2), root)."""
        def Dm(mu):
            return det4([list(self.P[k][0]) + [-(self.rhs(k, mu))] for k in quad])
        d0, d1, d2 = Dm(ZERO), Dm(ONE), Dm(F(2))
        lin = (d2 - d1 * 2 + d0) == ZERO
        root = None if d1 == d0 else (-d0) / (d1 - d0)
        return d0, d1 - d0, lin, root

    def walk(self, s0, top=None, eps=Q(1, 64), maxwalls=50):
        """walk upward from generic s0 (S = mu P* there) wall by wall. Returns list of walls with data."""
        walls = []
        s = F(s0)
        while len(walls) < maxwalls:
            w, hits = self.next_wall(s)
            if w is None or (top is not None and w > top):
                break
            # a generic point just above w
            e = F(eps)
            while True:
                s2 = w + e
                try:
                    pw = self.prev_wall(s2)
                    nw, _ = self.next_wall(s2)
                except RuntimeError:
                    e = e * Q(1, 2); continue
                if pw == w:
                    break
                e = e * Q(1, 2)
            walls.append(dict(mu=w, hits=hits, below=s, above=s2))
            s = s2
        return walls

    # ---- antipol and t_min (sphere row) ----
    def antipol_planes(self, st, mu):
        """S^v: same normals, inverted distances, facets of S only: a.y <= |a|^2 / b(mu)."""
        out = []
        for k in sorted(st['facets']):
            a = self.P[k][0]
            out.append((a, dot(a, a) / self.rhs(k, mu), ZERO, self.P[k][3]))
        return out

    def tmin(self, mu, st=None):
        st = st or self.structure(mu)
        Sv = Sweep(self.antipol_planes(st, mu))
        Vv = Sv.vertices(ZERO)
        best = None
        for x, _ in st['V']:
            for y, _ in Vv:
                v = dot(x, y)
                if best is None or v > best:
                    best = v
        return best, Sv, Vv


def classify(sw, s_below, s_above):
    """compare face structure on the two sides of a wall: faces and bonds (face pairs sharing an edge)."""
    a, b = sw.structure(s_below), sw.structure(s_above)
    fa, fb = a['facets'], b['facets']
    born, died = fb - fa, fa - fb
    keep = fa & fb
    ba = {x for x in a['bonds'] if x <= keep}
    bb = {x for x in b['bonds'] if x <= keep}
    lost, gained = ba - bb, bb - ba
    kinds = []
    if born: kinds.append('emergence of faces')
    if died: kinds.append('dissolution of faces')
    if lost and gained: kinds.append('jump (bonds between surviving faces dissolve and emerge at once)')
    elif lost: kinds.append('dissolution of bonds')
    elif gained: kinds.append('emergence of bonds')
    fam = lambda S: sorted({sw.P[k][3] for k in S})
    fb_ = lambda S: sorted({tuple(sorted(sw.P[k][3] for k in x)) for x in S})
    return dict(kinds=kinds, born=(len(born), fam(born)), died=(len(died), fam(died)),
                bonds_lost=(len(lost), fb_(lost)), bonds_gained=(len(gained), fb_(gained)),
                census_below=sw.census(a), census_above=sw.census(b), V=(len(a['V']), len(b['V'])),
                euler=(a['euler'], b['euler']))


def foot_sweep(sw, facets):
    """S^v as a sweep in nu = 1/mu for a fixed facet set of S (each family has b0 = 0 or b1 = 0)."""
    pl = []
    for k in sorted(facets):
        a, b0, b1, fam = sw.P[k]
        n2 = dot(a, a)
        if b1 == ZERO:
            pl.append((a, n2 / b0, ZERO, fam))
        else:
            assert b0 == ZERO
            pl.append((a, ZERO, n2 / b1, fam))
    return Sweep(pl)
