# DICTO · dictospheres.com — exact solids for the figures of the Dehn Canon paper.
# Numbers in Q(sqrt5) as a + b sqrt5 with exact fractions (class Q5). A solid is built from exact corners (V-rep) or from exact
# half-spaces (H-rep, corners found exactly from every triple of planes). Faces, edges, edge lengths squared and the cosine
# squared and sign of every dihedral angle are exact; each edge angle is named from a fixed table of exact values, and an
# unknown value stops the script. Floats are made only at the end, for drawing.
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np


class Q5:
    __slots__ = ('a', 'b')

    def __init__(s, a=0, b=0):
        s.a = Fr(a); s.b = Fr(b)

    @staticmethod
    def c(x): return x if isinstance(x, Q5) else Q5(x)
    def __add__(s, o): o = Q5.c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q5(-s.a, -s.b)
    def __sub__(s, o): return s + (-Q5.c(o))
    def __rsub__(s, o): return Q5.c(o) - s
    def __mul__(s, o): o = Q5.c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = Q5.c(o); n = o.a * o.a - 5 * o.b * o.b
        assert n != 0, 'division by zero'
        return s * Q5(o.a / n, -o.b / n)
    def __eq__(s, o): o = Q5.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        d = a * a - 5 * b * b                       # a and b of opposite signs: the larger square wins
        return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s): return f'({s.a}+{s.b}√5)'


R5 = Q5(0, 1); PHI = Q5(Fr(1, 2), Fr(1, 2)); G = Q5(Fr(-1, 2), Fr(1, 2))     # φ and g = 1/φ
dot = lambda u, v: sum((x * y for x, y in zip(u, v)), Q5())
sub = lambda u, v: tuple(x - y for x, y in zip(u, v))
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
q = lambda *xs: tuple(Q5.c(x) for x in xs)


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


# exact named angles: (sign of cos, cos^2) -> name, and whether the angle is a rational multiple of π
ANG = {}
def _a(name, sg, c2, rat): ANG[(sg, Q5.c(c2))] = (name, rat)
_a('π/2', 0, 0, True)
for nm, c2 in [('π/3', Fr(1, 4)), ('π/4', Fr(1, 2)), ('π/5·2', (3 - R5) / 8), ('π/5', (3 + R5) / 8)]:
    _a(nm, 1, c2, True); _a('π − ' + nm, -1, c2, True)
for nm, c2 in [('arccos(1/3)', Fr(1, 9)), ('arccos(1/√3)', Fr(1, 3)), ('α', Fr(1, 5)), ('γ', Fr(5, 9)),
               ('β', Fr(1, 3) - 2 * R5 / 15), ('ε', Fr(1, 3) + 2 * R5 / 15)]:
    _a(nm, 1, c2, False); _a('π − ' + nm, -1, c2, False)


class Solid:
    """Exact convex solid: corners V (tuples of Q5), faces as (outward normal, offset, ordered corner indices)."""

    def __init__(s, V, planes):
        s.V = V; s.F = []
        for n, d in planes:
            on = [i for i, v in enumerate(V) if dot(n, v) == d]
            assert all((dot(n, v) - d).sign() <= 0 for v in V), 'corner outside a face plane'
            if len(on) >= 3: s.F.append((n, d, on))
        # drop repeated planes (same corner set)
        seen = {}; F = []
        for f in s.F:
            k = tuple(sorted(f[2]))
            if k not in seen: seen[k] = 1; F.append(f)
        s.F = F
        Vf = s.vf()
        for k, (n, d, on) in enumerate(s.F):             # order each face's corners round its centre
            c = Vf[on].mean(0); nf = np.array([float(x) for x in n]); nf /= np.linalg.norm(nf)
            u = Vf[on[0]] - c; u /= np.linalg.norm(u); w = np.cross(nf, u)
            on = sorted(on, key=lambda i: np.arctan2((Vf[i] - c) @ w, (Vf[i] - c) @ u)); s.F[k] = (n, d, on)
        E = {}
        for k, f in enumerate(s.F):
            for a, b in zip(f[2], f[2][1:] + f[2][:1]): E.setdefault(tuple(sorted((a, b))), []).append(k)
        assert all(len(x) == 2 for x in E.values()), 'not a closed polytope'
        s.E = []                                           # (a, b, length^2, angle name, rational?)
        for (a, b), (i, j) in sorted(E.items()):
            n1, n2 = s.F[i][0], s.F[j][0]; p = dot(n1, n2)
            c2 = p * p / (dot(n1, n1) * dot(n2, n2)); sg = -p.sign()
            assert (sg, c2) in ANG, f'unknown dihedral angle: sign {sg}, cos² {c2}'
            nm, rat = ANG[(sg, c2)]; e = sub(s.V[a], s.V[b]); s.E.append((a, b, dot(e, e), nm, rat))
        # Euler's formula as a sanity check
        assert len(V) - len(s.E) + len(s.F) == 2

    def vf(s): return np.array([[float(x) for x in v] for v in s.V])

    def classes(s):
        out = {}
        for a, b, l2, nm, rat in s.E: out[(nm, l2)] = out.get((nm, l2), 0) + 1
        return out


def from_vertices(V):
    """Convex hull of exact corners: face planes found from the float hull, then checked exactly."""
    from scipy.spatial import ConvexHull
    V = [q(*v) for v in V]; Vf = np.array([[float(x) for x in v] for v in V])
    H = ConvexHull(Vf); groups = {}
    for simp, eq in zip(H.simplices, H.equations): groups.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
    planes = []
    for ids in groups.values():
        ids = sorted(ids); a, b, c = (V[i] for i in ids[:3])
        n = cross(sub(b, a), sub(c, a)); d = dot(n, a)
        others = [v for v in V if not dot(n, v) == d]
        if any((dot(n, v) - d).sign() > 0 for v in others): n = tuple(-x for x in n); d = -d
        assert all((dot(n, v) - d).sign() < 0 for v in others)
        assert all(dot(n, V[i]) == d for i in ids), 'face not planar'
        planes.append((n, d))
    keep = sorted(set(H.vertices)); assert len(keep) == len(V), 'a given corner is not a corner of the hull'
    return Solid(V, planes)


def from_halfspaces(N, B):
    """{x : n_i · x <= b_i}: corners exactly from every triple of planes."""
    N = [q(*n) for n in N]; B = [Q5.c(b) for b in B]; V = []
    for i, j, k in combinations(range(len(N)), 3):
        m = [N[i], N[j], N[k]]; D = det3(m)
        if D == 0: continue
        rhs = [B[i], B[j], B[k]]; x = []
        for col in range(3):
            mm = [list(r) for r in m]
            for r in range(3): mm[r][col] = rhs[r]
            x.append(det3(mm) / D)
        x = tuple(x)
        if all((dot(n, x) - b).sign() <= 0 for n, b in zip(N, B)) and x not in V: V.append(x)
    return Solid(V, list(zip(N, B)))


def perms3(v):                                             # cyclic permutations
    return [(v[0], v[1], v[2]), (v[1], v[2], v[0]), (v[2], v[0], v[1])]


def signs(v):
    out = set()
    for sx in (1, -1):
        for sy in (1, -1):
            for sz in (1, -1): out.add((v[0] * sx, v[1] * sy, v[2] * sz))
    return list(out)


def uniq(L):
    out = []
    for v in L:
        if v not in out: out.append(v)
    return out
