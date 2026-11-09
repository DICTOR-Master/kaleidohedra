# q5.py -- exact arithmetic in Q(sqrt5) and exact polytopes from half-spaces (study 2026-11-09-icosahedral-line).
# Numbers a + b sqrt5 with Fraction a, b; signs exact. A polytope {N_i . x <= d_i} gets its corners from a float half-space
# intersection (combinatorics only), each corner then solved exactly from three independent active planes and checked exactly
# against every plane (on it, or strictly inside).
from fractions import Fraction as Fr
import itertools
import numpy as np
from scipy.spatial import HalfspaceIntersection
S5 = 5 ** .5

class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0):
        s.a = a if isinstance(a, Fr) else Fr(a); s.b = b if isinstance(b, Fr) else Fr(b)
    @staticmethod
    def c(x): return x if isinstance(x, Q5) else Q5(x)
    def __add__(s, o): o = Q5.c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = Q5.c(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q5.c(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = Q5.c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return Q5(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * Q5.c(o).inv()
    def __rtruediv__(s, o): return Q5.c(o) * s.inv()
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) * (1 if a * a > 5 * b * b else -1)
    def __lt__(s, o): return (s - o).sign() < 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def __eq__(s, o): o = Q5.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * S5
    def conj(s): return Q5(s.a, -s.b)
    def __repr__(s):
        if s.b == 0: return f'{s.a}'
        return f'({s.a}) + ({s.b})√5'

PHI = Q5(Fr(1, 2), Fr(1, 2)); IPHI = PHI - 1; ZERO = Q5(0); ONE = Q5(1)
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def scl(k, u): return tuple(k * a for a in u)
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def fl(v): return np.array([x.f() for x in v])
def solve3(N, d):
    # x with N[i].x = d[i], i = 0..2 (Cramer, exact)
    D = dot(N[0], cross(N[1], N[2]))
    if D == ZERO: return None
    c12, c20, c01 = cross(N[1], N[2]), cross(N[2], N[0]), cross(N[0], N[1])
    return tuple((d[0] * c12[i] + d[1] * c20[i] + d[2] * c01[i]) / D for i in range(3))

def corners(planes, tol=1e-7):
    # planes: list of (N, d), N exact 3-vector, d exact, O strictly inside. Returns list of (corner, frozenset of active planes).
    A = np.array([np.r_[fl(N), -d.f()] for N, d in planes])
    hs = HalfspaceIntersection(A, np.zeros(3))
    pts = []
    for p in hs.intersections:
        if not any(np.abs(p - q).max() < 1e-7 for q in pts): pts.append(p)
    out = []
    for p in pts:
        act = [i for i, (N, d) in enumerate(planes) if abs(fl(N) @ p - d.f()) < tol * max(1, abs(d.f()))]
        x = None
        for tri in itertools.combinations(act, 3):
            x = solve3([planes[i][0] for i in tri], [planes[i][1] for i in tri])
            if x is not None: break
        assert x is not None, 'no independent triple'
        sg = [(dot(N, x) - d).sign() for N, d in planes]
        assert all(s <= 0 for s in sg), 'corner outside a plane (exact)'
        exact_act = frozenset(i for i, s in enumerate(sg) if s == 0)
        assert exact_act == frozenset(act), 'float and exact active sets differ'
        out.append((x, exact_act))
    return out

# icosahedral frame: icosahedron corners (0, +-1, +-phi) and cyclic permutations; 3-fold axes (+-1, +-1, +-1) and cyclic
# permutations of (0, +-phi, +-1/phi) (dodecahedron corners, |.|^2 = 3; each is the centre direction of a face of the icosahedron)
def cyc(p): return [p, (p[2], p[0], p[1]), (p[1], p[2], p[0])]
def signs(p):
    out = set()
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(Q5(s[i]) * p[i] for i in range(3)); out.add(q)
    return list(out)
AX5 = sorted({q for p in cyc((ZERO, ONE, PHI)) for q in signs(p)}, key=lambda v: tuple(x.f() for x in v))
AX3 = sorted({q for p in cyc((ZERO, PHI, IPHI)) + [(ONE, ONE, ONE)] for q in signs(p)}, key=lambda v: tuple(x.f() for x in v))
assert len(AX5) == 12 and len(AX3) == 20
# frame check: every three-fold axis b is nearest to exactly three icosahedron corners (a face), all at b.a = phi^2
assert all(sorted(dot(a, b).f() for a in AX5)[-3:] == [(PHI * PHI).f()] * 3 and sorted(dot(a, b).f() for a in AX5)[-4] < (PHI * PHI).f() - 0.1 for b in AX3)
