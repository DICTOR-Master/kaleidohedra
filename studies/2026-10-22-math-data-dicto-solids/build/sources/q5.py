"""Exact arithmetic in Q(sqrt5) and exact 3D convex hulls (float screening, exact verification).

Q5(a, b) = a + b*sqrt(5), a and b Fractions.  Every sign, equality and coplanarity used in a claim is decided
exactly here; floats only propose candidate facets (scipy ConvexHull), which are then verified exactly.
"""
from fractions import Fraction as Fr
import math

import numpy as np
from scipy.spatial import ConvexHull

S5 = math.sqrt(5.0)


class Q5:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = a if isinstance(a, Fr) else Fr(a)
        self.b = b if isinstance(b, Fr) else Fr(b)

    @staticmethod
    def c(x):
        return x if isinstance(x, Q5) else Q5(x)

    def __add__(s, o):
        o = Q5.c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __sub__(s, o):
        o = Q5.c(o); return Q5(s.a - o.a, s.b - o.b)

    def __rsub__(s, o):
        return Q5.c(o) - s

    def __neg__(s):
        return Q5(-s.a, -s.b)

    def __mul__(s, o):
        o = Q5.c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        if n == 0:
            raise ZeroDivisionError
        return Q5(s.a / n, -s.b / n)

    def __truediv__(s, o):
        return s * Q5.c(o).inv()

    def __rtruediv__(s, o):
        return Q5.c(o) * s.inv()

    def sign(s):
        a, b = s.a, s.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        sa, sb = (a > 0) - (a < 0), (b > 0) - (b < 0)
        if sa == sb:
            return sa
        return sa if a * a > 5 * b * b else sb

    def __eq__(s, o):
        o = Q5.c(o); return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __lt__(s, o):
        return (s - o).sign() < 0

    def __le__(s, o):
        return (s - o).sign() <= 0

    def __gt__(s, o):
        return (s - o).sign() > 0

    def __ge__(s, o):
        return (s - o).sign() >= 0

    def __float__(s):
        return float(s.a) + float(s.b) * S5

    def iszero(s):
        return s.a == 0 and s.b == 0

    def __repr__(s):
        return q5str(s)


def q5str(x):
    a, b = x.a, x.b
    if b == 0:
        return str(a)
    bs = ("" if abs(b) == 1 else str(abs(b))) + "√5"
    if a == 0:
        return ("-" if b < 0 else "") + bs
    return f"{a} {'+' if b > 0 else '-'} {bs}"


def q5sympy(x):
    import sympy as sp
    return sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator) * sp.sqrt(5)


ZERO, ONE = Q5(0), Q5(1)
PHI = Q5(Fr(1, 2), Fr(1, 2))
IPHI = Q5(Fr(-1, 2), Fr(1, 2))


def dot(u, v):
    s = ZERO
    for x, y in zip(u, v):
        s = s + x * y
    return s


def sub(u, v):
    return tuple(x - y for x, y in zip(u, v))


def add(u, v):
    return tuple(x + y for x, y in zip(u, v))


def scal(k, u):
    return tuple(k * x for x in u)


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def fl(u):
    return np.array([float(x) for x in u])


# ---------------------------------------------------------------- exact 3D hull of points given in exact coords
def orient2(o, a, b):
    return ((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])).sign()


def hull2d_exact(pts2):
    """Monotone chain, exact; returns indices of strict extreme points in ccw order."""
    idx = sorted(range(len(pts2)), key=lambda i: (float(pts2[i][0]), float(pts2[i][1])))
    # exact re-sort (floats only seed the order; fix ties exactly)
    import functools

    def cmp(i, j):
        for k in (0, 1):
            s = (pts2[i][k] - pts2[j][k]).sign()
            if s:
                return s
        return 0
    idx = sorted(idx, key=functools.cmp_to_key(cmp))
    if len(idx) < 3:
        return idx
    lower, upper = [], []
    for i in idx:
        while len(lower) >= 2 and orient2(pts2[lower[-2]], pts2[lower[-1]], pts2[i]) <= 0:
            lower.pop()
        lower.append(i)
    for i in reversed(idx):
        while len(upper) >= 2 and orient2(pts2[upper[-2]], pts2[upper[-1]], pts2[i]) <= 0:
            upper.pop()
        upper.append(i)
    return lower[:-1] + upper[:-1]


def dedupe(points, fpoints):
    """Exact dedupe; returns list of unique exact points and their float coords."""
    keys = {}
    out, outf = [], []
    for p, f in zip(points, fpoints):
        k = tuple(np.round(f, 7))
        cand = keys.setdefault(k, [])
        hit = False
        for j in cand:
            if all((x - y).iszero() for x, y in zip(out[j], p)):
                hit = True
                break
        if not hit:
            cand.append(len(out))
            out.append(p)
            outf.append(f)
    return out, np.array(outf)


def affine_rank(fpts, tol=1e-9):
    if len(fpts) <= 1:
        return 0
    m = fpts[1:] - fpts[0]
    s = np.linalg.svd(m, compute_uv=False)
    return int((s > tol * max(1.0, s[0])).sum())


def exact_hull3(points, metric_f):
    """points: exact 3-tuples (Q5) in an orthogonal-but-unnormalised frame; metric_f: float axis weights (lengths of
    the frame vectors) so that float metric coords = coords * metric_f.  Returns dict with vertices (exact),
    faces (ccw vertex index lists, outward), all verified exactly."""
    fpts = np.array([[float(x) for x in p] for p in points]) * metric_f
    pts, fpts = dedupe(points, fpts)
    r = affine_rank(fpts)
    if r < 3:
        return {"dim": r, "points": pts, "fpoints": fpts}
    H = ConvexHull(fpts)
    faces = []
    seen_planes = []
    n_all = len(pts)
    for simp in H.simplices:
        i, j, k = [int(t) for t in simp]
        n = cross(sub(pts[j], pts[i]), sub(pts[k], pts[i]))
        off = dot(n, pts[i])
        # orient outward exactly: all points on side <= 0
        sides = [(dot(n, p) - off).sign() for p in pts]
        if any(s > 0 for s in sides) and any(s < 0 for s in sides):
            raise RuntimeError("float facet not a supporting plane (exact check failed)")
        if any(s > 0 for s in sides):
            n = scal(Q5(-1), n); off = -off
            sides = [-s for s in sides]
        on = frozenset(t for t in range(n_all) if sides[t] == 0)
        if on in seen_planes:
            continue
        seen_planes.append(on)
        # 2D exact hull of the face: drop coordinate with largest |normal|
        ax = int(np.argmax([abs(float(c)) for c in n]))
        keep = [a for a in range(3) if a != ax]
        onl = sorted(on)
        p2 = [(pts[t][keep[0]], pts[t][keep[1]]) for t in onl]
        h = hull2d_exact(p2)
        poly = [onl[t] for t in h]
        # make ccw seen from outside: check orientation of poly against n
        a0, a1, a2 = pts[poly[0]], pts[poly[1]], pts[poly[2]]
        if dot(cross(sub(a1, a0), sub(a2, a0)), n).sign() < 0:
            poly = poly[::-1]
        faces.append(poly)
    verts = sorted({v for f in faces for v in f})
    remap = {v: i for i, v in enumerate(verts)}
    faces = [[remap[v] for v in f] for f in faces]
    V = [pts[v] for v in verts]
    E = set()
    for f in faces:
        for a, b in zip(f, f[1:] + f[:1]):
            E.add((min(a, b), max(a, b)))
    # topology checks
    from collections import Counter
    c = Counter()
    for f in faces:
        for a, b in zip(f, f[1:] + f[:1]):
            c[(min(a, b), max(a, b))] += 1
    assert all(v == 2 for v in c.values()), "edge not in exactly two faces"
    assert len(V) - len(E) + len(faces) == 2, "Euler characteristic != 2"
    return {"dim": 3, "V": V, "fV": fpts[verts], "faces": faces, "E": sorted(E)}
