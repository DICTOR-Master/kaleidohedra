"""Shared exact tools for s9_why_not_cubes.py, s10_honeycomb_cubes.py and s11_star_polytopes.py (paper #89).
K = Q(sqrt2, sqrt5): a + b sqrt2 + c sqrt5 + d sqrt10 with Fractions; equality and sign are decided exactly.
Reflection groups from root systems, Wythoff points, edges, hyperplane sections and an exact face check
(floats only propose hull facets; every facet plane and side is then verified exactly in K).
"""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull, cKDTree

R2, R5 = math.sqrt(2), math.sqrt(5)


def _s2sign(p, q):            # sign of p + q sqrt2, p, q Fractions
    if p >= 0 and q >= 0: return 0 if (p == 0 and q == 0) else 1
    if p <= 0 and q <= 0: return -1
    d = p * p - 2 * q * q
    return (1 if p > 0 else -1) if d > 0 else (-1 if p > 0 else 1) if d < 0 else 0


class K:
    __slots__ = ('v',)
    def __init__(s, a=0, b=0, c=0, d=0):
        s.v = (Fr(a), Fr(b), Fr(c), Fr(d))
    @staticmethod
    def c(x): return x if isinstance(x, K) else K(x)
    def __add__(s, o): o = K.c(o); return K(*(x + y for x, y in zip(s.v, o.v)))
    __radd__ = __add__
    def __sub__(s, o): o = K.c(o); return K(*(x - y for x, y in zip(s.v, o.v)))
    def __rsub__(s, o): return K.c(o) - s
    def __neg__(s): return K(*(-x for x in s.v))
    def __mul__(s, o):
        o = K.c(o); a, b, c, d = s.v; e, f, g, h = o.v
        return K(a*e + 2*b*f + 5*c*g + 10*d*h, a*f + b*e + 5*(c*h + d*g), a*g + c*e + 2*(b*h + d*f), a*h + d*e + b*g + c*f)
    __rmul__ = __mul__
    def conj2(s): a, b, c, d = s.v; return K(a, -b, c, -d)
    def conj5(s): a, b, c, d = s.v; return K(a, b, -c, -d)
    def inv(s):
        m = s * s.conj2()                 # in Q(sqrt5)
        n = m * m.conj5()                 # rational
        assert n.v[1] == n.v[2] == n.v[3] == 0 and n.v[0] != 0
        return s.conj2() * m.conj5() * K(1 / n.v[0])
    def __truediv__(s, o): return s * K.c(o).inv()
    def __rtruediv__(s, o): return K.c(o) * s.inv()
    def sign(s):
        a, b, c, d = s.v
        sp, sq = _s2sign(a, b), _s2sign(c, d)          # P + sqrt5 Q
        if sq == 0: return sp
        if sp == 0 or sp == sq: return sq if sp == 0 else sp
        P2 = K(a, b) * K(a, b); Q2 = K(c, d) * K(c, d) * 5
        t = _s2sign(*(P2 - Q2).v[:2])
        return sp if t > 0 else sq if t < 0 else 0
    def iszero(s): return all(x == 0 for x in s.v)
    def __eq__(s, o): return (s - K.c(o)).iszero()
    def __hash__(s): return hash(s.v)
    def __lt__(s, o): return (s - K.c(o)).sign() < 0
    def __gt__(s, o): return (s - K.c(o)).sign() > 0
    def __le__(s, o): return (s - K.c(o)).sign() <= 0
    def __ge__(s, o): return (s - K.c(o)).sign() >= 0
    def __float__(s): a, b, c, d = s.v; return float(a) + float(b) * R2 + float(c) * R5 + float(d) * R2 * R5
    def __repr__(s): return kstr(s)


def kstr(x):
    names = ('', '√2', '√5', '√10'); out = []
    for q, n in zip(x.v, names):
        if q == 0: continue
        out.append(f'{q}{n}' if n == '' else (f'{q}{n}' if q not in (1, -1) else ('-' if q == -1 else '') + n))
    return ' + '.join(out).replace('+ -', '- ') if out else '0'


S2, S5 = K(0, 1), K(0, 0, 1)
PHI = K(Fr(1, 2), 0, Fr(1, 2))
ZERO, ONE = K(0), K(1)
def dot(u, w):
    s = ZERO
    for a, b in zip(u, w): s = s + a * b
    return s
def vsub(u, w): return tuple(a - b for a, b in zip(u, w))
def vadd(u, w): return tuple(a + b for a, b in zip(u, w))
def vscale(k, u): return tuple(k * a for a in u)
def fl(u): return np.array([float(a) for a in u])
def key(u): return tuple(a.v for a in u)


def reflect(p, a, aa):
    return vsub(p, vscale(dot(p, a) * 2 / aa, a))


def orbit(p, roots, limit=10 ** 6):
    rr = [(a, dot(a, a)) for a in roots]
    seen = {key(p): p}; todo = [p]
    while todo:
        q = todo.pop()
        for a, aa in rr:
            r = reflect(q, a, aa); k = key(r)
            if k not in seen:
                seen[k] = r; todo.append(r)
                if len(seen) > limit: raise RuntimeError('orbit too large')
    return list(seen.values())


def simple_roots(roots, generic):
    # alpha is simple iff its reflection makes exactly one positive root negative (alpha itself)
    pos = [r for r in roots if dot(r, generic).sign() > 0]
    simple = []
    for a in pos:
        aa = dot(a, a)
        if sum(1 for b in pos if dot(reflect(b, a, aa), generic).sign() < 0) == 1: simple.append(a)
    return simple


def chain(simple):
    """order simple roots along the Coxeter diagram (a path for A4, B4, F4, H4); return roots and bond labels m"""
    n = len(simple); m = {}
    for i, j in itertools.combinations(range(n), 2):
        c = float(dot(simple[i], simple[j])) / math.sqrt(float(dot(simple[i], simple[i])) * float(dot(simple[j], simple[j])))
        ang = math.degrees(math.acos(max(-1, min(1, c))))
        mm = round(180 / (180 - ang)) if ang > 91 else 2
        if mm > 2: m[(i, j)] = m[(j, i)] = mm
    deg = {i: sum(1 for j in range(n) if (i, j) in m) for i in range(n)}
    ends = [i for i in range(n) if deg[i] == 1]
    # put the end with the higher bond first (4 or 5 end) when the path is not symmetric
    def walk(s):
        path = [s]
        while len(path) < n:
            nx = [j for j in range(n) if (path[-1], j) in m and j not in path]; path.append(nx[0])
        return path
    paths = [walk(e) for e in ends]
    paths.sort(key=lambda p: -m[(p[0], p[1])])
    p = paths[0]
    return [simple[i] for i in p], [m[(p[k], p[k + 1])] for k in range(n - 1)]


def wythoff_point(simple, rings):
    """p with p.a_k = |a_k|/2 for ringed nodes (unit edges), 0 otherwise; exact Gaussian elimination in K"""
    n = len(simple)
    norms = []
    for a in simple:
        aa = dot(a, a)
        nr = {K(1): K(1), K(2): S2, K(4): K(2), K(Fr(1, 2)): S2 / 2}.get(aa)
        assert nr is not None, aa
        norms.append(nr)
    M = [list(simple[k]) + [norms[k] / 2 if (k + 1) in rings else ZERO] for k in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if not M[r][c].iszero()); M[c], M[piv] = M[piv], M[c]
        iv = M[c][c].inv(); M[c] = [x * iv for x in M[c]]
        for r in range(n):
            if r != c and not M[r][c].iszero():
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return tuple(M[k][n] for k in range(n))


def edges_at(V, d2target, tol=1e-7):
    F = np.array([fl(v) for v in V]); t = cKDTree(F); r = math.sqrt(float(d2target))
    out = []
    for i, j in t.query_pairs(r + 1e-6):
        dd = vsub(V[i], V[j])
        if abs(float(dot(dd, dd)) - float(d2target)) < tol and dot(dd, dd) == d2target: out.append((i, j))
    return out


def min_d2(V):
    F = np.array([fl(v) for v in V]); t = cKDTree(F); d, i = t.query(F, k=2)
    k = int(np.argmin(d[:, 1])); dd = vsub(V[k], V[int(i[k, 1])]); return dot(dd, dd)


def section(V, E, d, h, H=None):
    if H is None: H = [dot(v, d) for v in V]
    pts = {}
    for v, x in zip(V, H):
        if x == h: pts[key(v)] = v
    for a, b in E:
        sa, sb = (H[a] - h).sign(), (H[b] - h).sign()
        if sa * sb < 0:
            t = (h - H[a]) / (H[b] - H[a]); p = vadd(V[a], vscale(t, vsub(V[b], V[a]))); pts[key(p)] = p
    return list(pts.values())


def det3(a, b, c):
    return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])


def normal4(u, v, w):
    """vector orthogonal to u, v, w in R^4 (generalised cross product), exact"""
    M = [u, v, w]; out = []
    for k in range(4):
        cols = [c for c in range(4) if c != k]
        sub3 = [[M[r][c] for c in cols] for r in range(3)]
        out.append(det3(*sub3) * (1 if k % 2 == 0 else -1))
    return tuple(out)


def faces_exact(P, d):
    """faces of the 3D convex polytope P (points in a hyperplane perpendicular to d, in R^4).
    Returns list of face corner-index lists; raises if exact verification fails."""
    F = np.array([fl(p) for p in P]); dn = fl(d) / np.linalg.norm(fl(d))
    B = np.linalg.svd(dn[None])[2][1:]; Q = (F - F.mean(0)) @ B.T
    hl = ConvexHull(Q)
    groups = {}
    for eq, s in zip(np.round(hl.equations, 7), hl.simplices): groups.setdefault(tuple(eq), set()).update(s)
    faces = []
    for g in groups.values():
        g = sorted(g); a, b, c = g[0], g[1], g[2]
        # pick a non-collinear triple
        for c in g[2:]:
            nrm = normal4(d, vsub(P[b], P[a]), vsub(P[c], P[a]))
            if any(not x.iszero() for x in nrm): break
        on = []; side = set()
        for i, p in enumerate(P):
            s = dot(nrm, vsub(p, P[a])).sign()
            if s == 0: on.append(i)
            else: side.add(s)
        assert len(side) <= 1 and sorted(on) == g, 'exact facet check failed'
        faces.append(g)
    return faces


def signature(faces):
    from collections import Counter
    return dict(sorted(Counter(len(f) for f in faces).items()))


def golden_x():
    """x_G(4), x_L(4) for the square: phi/(sqrt2 + 2 phi), 1/(phi sqrt2 + 2), exact in K"""
    return PHI / (S2 + 2 * PHI), ONE / (PHI * S2 + 2)


def cut_cube(x, half=ONE):
    """cube [-half, half]^3 cut at every corner at fraction x of the edge (24 corners)"""
    pts = []
    for s in itertools.product((1, -1), repeat=3):
        c = tuple(K(si) * half for si in s)
        for k in range(3):
            p = list(c); p[k] = p[k] - K(s[k]) * 2 * half * x; pts.append(tuple(p))
    return pts


def similar(S, T):
    """corner-to-corner bijection S -> T scaling all squared distances by one factor, exact; returns (ok, factor)"""
    n = len(S)
    if n != len(T): return False, None
    DS = [[float(dot(vsub(S[i], S[j]), vsub(S[i], S[j]))) for j in range(n)] for i in range(n)]
    DT = [[float(dot(vsub(T[i], T[j]), vsub(T[i], T[j]))) for j in range(n)] for i in range(n)]
    k = max(max(r) for r in DT) / max(max(r) for r in DS)
    f = [None] * n; used = [False] * n
    def go(i):
        if i == n: return True
        for c in range(n):
            if used[c]: continue
            if all(abs(DT[c][f[j]] - k * DS[i][j]) < 1e-9 * max(1, k) for j in range(i)):
                f[i] = c; used[c] = True
                if go(i + 1): return True
                used[c] = False
        return False
    if not go(0): return False, None
    def d2(A, i, j): return dot(vsub(A[i], A[j]), vsub(A[i], A[j]))
    lam = d2(T, f[0], f[1]) / d2(S, 0, 1)
    ok = all(d2(T, f[i], f[j]) == lam * d2(S, i, j) for i, j in itertools.combinations(range(n), 2))
    return ok, lam


# ---------------------------------------------------------------- root systems
def roots_B4():
    R = []
    for i in range(4):
        for s in (1, -1):
            v = [ZERO] * 4; v[i] = K(s); R.append(tuple(v))
    for i, j in itertools.combinations(range(4), 2):
        for s, t in itertools.product((1, -1), repeat=2):
            v = [ZERO] * 4; v[i] = K(s); v[j] = K(t); R.append(tuple(v))
    return R


def roots_F4():
    R = roots_B4()
    R += [tuple(K(Fr(s, 2)) for s in ss) for ss in itertools.product((1, -1), repeat=4)]
    return R


def v600():
    """the 120 vertices of the 600-cell, circumradius 1 (also the 120 roots of H4)"""
    P = []
    for i in range(4):
        for s in (1, -1):
            v = [ZERO] * 4; v[i] = K(s); P.append(tuple(v))
    P += [tuple(K(Fr(s, 2)) for s in ss) for ss in itertools.product((1, -1), repeat=4)]
    base = (PHI / 2, K(Fr(1, 2)), (PHI - 1) / 2, ZERO)
    evenp = [p for p in itertools.permutations(range(4)) if sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) % 2 == 0]
    seen = {key(p) for p in P}
    for pe in evenp:
        for ss in itertools.product((1, -1), repeat=4):
            v = tuple(base[pe[i]] * K(ss[i]) for i in range(4)); k = key(v)
            if k not in seen: seen.add(k); P.append(v)
    assert len(P) == 120
    return P


def roots_A4():
    """A4 in the hyperplane sum = 0 of R^5, written in an orthonormal-free way: we keep 5 coordinates"""
    R = []
    for i, j in itertools.permutations(range(5), 2):
        v = [ZERO] * 5; v[i] = ONE; v[j] = -ONE; R.append(tuple(v))
    return R
