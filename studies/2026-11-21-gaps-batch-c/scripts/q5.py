# Exact arithmetic in Q(sqrt5) with Python fractions, and exact convex polytopes (float combinatorics, exact planes and vertices,
# every inequality re-checked exactly). Gaps batch C, 21 Nov 2026.
from fractions import Fraction as F
import itertools
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

class Q:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = F(a); s.b = F(b)
    def __add__(s, o): o = q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b)
    def __sub__(s, o): return s + (-q(o))
    def __rsub__(s, o): return q(o) - s
    def __mul__(s, o): o = q(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        if n == 0: raise ZeroDivisionError
        return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * q(o).inv()
    def __rtruediv__(s, o): return q(o) * s.inv()
    def __eq__(s, o): o = q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):                                  # exact sign of a + b sqrt5
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sb == 0: return sa
        if sa == 0 or sa == sb: return sb
        return sa if s.a * s.a > 5 * s.b * s.b else sb
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def f(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}√5'
        return f'{s.a} {"+" if s.b > 0 else "-"} {abs(s.b)}√5'
def q(x): return x if isinstance(x, Q) else Q(x)
PHI = Q(F(1, 2), F(1, 2)); S5 = Q(0, 1)

def dot(u, v): return sum((u[i] * v[i] for i in range(3)), Q(0))
def sub(u, v): return [u[i] - v[i] for i in range(3)]
def scl(c, u): return [q(c) * x for x in u]
def cross(u, v): return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
def fl(V): return np.array([[x.f() for x in v] for v in V])
def key(v): return tuple((x.a, x.b) for x in v)
def uniq(V):
    seen = {}; [seen.setdefault(key(v), v) for v in V]; return list(seen.values())

def cyc(base_signs):                              # cyclic permutations of all sign choices of a triple
    out = []
    for t in base_signs:
        for s in itertools.product((1, -1), repeat=3):
            p = [q(t[i]) * s[i] for i in range(3)]
            for k in range(3): out.append(p[k:] + p[:k])
    return uniq(out)

def facets(V):
    """Exact facet planes (n, d), n.x <= d, of conv(V), V exact; origin assumed interior. Checked exactly."""
    Vf = fl(V); h = ConvexHull(Vf); groups = {}
    for eq, simp in zip(h.equations, h.simplices):
        k = tuple(np.round(eq / np.abs(eq[3]) if abs(eq[3]) > 1e-12 else eq, 9)); groups.setdefault(k, set()).update(simp)
    out = []
    for idx in groups.values():
        idx = sorted(idx)
        for i0, i1, i2 in itertools.combinations(idx, 3):
            n = cross(sub(V[i1], V[i0]), sub(V[i2], V[i0]))
            if any(x != 0 for x in n): break
        d = dot(n, V[i0])
        if d.sign() < 0: n = [-x for x in n]; d = -d
        on = [i for i in range(len(V)) if dot(n, V[i]) == d]
        assert all(dot(n, v) <= d for v in V), 'facet check failed'
        assert set(on) >= set(idx) and len(on) >= 3
        out.append((n, d))
    return out

def vertices_of(Hs):
    """Exact vertices of {x : n.x <= d for (n, d) in Hs} (origin interior). Each vertex solved exactly from 3 tight planes, all checked."""
    A = np.array([[*[x.f() for x in n], -d.f()] for n, d in Hs])
    hi = HalfspaceIntersection(A, np.zeros(3)); out = []
    for p in hi.intersections:
        act = [i for i, (n, d) in enumerate(Hs) if abs(sum(n[j].f() * p[j] for j in range(3)) - d.f()) < 1e-7 * (1 + abs(d.f()))]
        for i, j, k in itertools.combinations(act, 3):
            M = [Hs[i][0], Hs[j][0], Hs[k][0]]; det = dot(M[0], cross(M[1], M[2]))
            if det != 0: break
        rhs = [Hs[i][1], Hs[j][1], Hs[k][1]]
        x = [dot([rhs[0], rhs[1], rhs[2]], [cross(M[1], M[2])[c], cross(M[2], M[0])[c], cross(M[0], M[1])[c]]) / det for c in range(3)]
        out.append(x)
    out = uniq(out)
    for x in out:
        assert all(dot(n, x) <= d for n, d in Hs)
        assert sum(1 for n, d in Hs if dot(n, x) == d) >= 3
    return out

def contain(A, B, FB=None):
    """least s with A ⊂ s·B (B star-shaped about 0): max over corners a of A and facets of B of (n.a)/d; and the corners of A that touch."""
    FB = FB or facets(B); best = None
    for a in A:
        for n, d in FB:
            r = dot(n, a) / d
            if best is None or r > best: best = r
    touch = sum(1 for a in A if any(dot(n, a) / d == best for n, d in FB))
    return best, touch

def edges(V):
    d2 = [dot(sub(a, b), sub(a, b)) for a, b in itertools.combinations(V, 2)]
    m = min(d2, key=lambda z: z.f()); m = [z for z in d2 if z == m][0]
    return [(a, b) for a, b in itertools.combinations(V, 2) if dot(sub(a, b), sub(a, b)) == m]

def trunc(V, x):                                 # cut every corner at edge fraction x (0 < x < 1/2)
    x = q(x); out = []
    for a, b in edges(V):
        out += [[a[i] + x * (b[i] - a[i]) for i in range(3)], [b[i] + x * (a[i] - b[i]) for i in range(3)]]
    return uniq(out)

def rect(V): return uniq([[(a[i] + b[i]) / 2 for i in range(3)] for a, b in edges(V)])
