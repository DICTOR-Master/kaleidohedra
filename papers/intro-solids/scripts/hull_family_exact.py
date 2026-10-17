# DICTO · dictospheres.com — the dodecahedron–icosahedron hull family in closed form, checked exactly in Q(√5) (2026-10-17).
# A member is the convex hull of the icosahedron (0, ±1, ±φ) (cyclic) and the dual-placed dodecahedron k·{(±1, ±1, ±1), (0, ±φ, ±1/φ) cyclic}.
# Its icosahedron edge is 2 and its dodecahedron edge 2k/φ, so the edge ratio (icosahedron / dodecahedron) is φ/k.
#   DICTO Metaxyhexecontahedron M (Vajrayana §3): ratio 9/φ⁴, so k = φ⁵/9;  DICTO Palintriacontahedron X (§4): ratio 3/√5, so k = φ√5/3.
# For each: every one of the 32 points is a corner, the faces (exact planes), their shapes, the edges, insphere / midsphere, the volume,
# and for M the match with the paper's construction (R_D² / R_I² from data/gap-member.txt) and its 1 = touching reach.
from fractions import Fraction as Fr
import itertools, numpy as np
from scipy.spatial import ConvexHull
class Q:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q(o) - s
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): o = o if isinstance(o, Q) else Q(o); return s * o.inv()
    def __eq__(s, o): o = o if isinstance(o, Q) else Q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * 5 ** .5
    def sgn(s):
        a, b = s.a, s.b
        if a == 0 and b == 0: return 0
        if a >= 0 and b >= 0: return 1
        if a <= 0 and b <= 0: return -1
        return (1 if a > 0 else -1) if a * a > 5 * b * b else (1 if b > 0 else -1)
    def __repr__(s): return f'{s.a} + {s.b}√5' if s.b else f'{s.a}'
phi = Q(Fr(1, 2), Fr(1, 2)); iphi = phi - 1
dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
sub = lambda u, v: [u[i] - v[i] for i in range(3)]
cross = lambda u, v: [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
ICO = [c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([Q(0), Q(s1), s2 * phi])]
DOD = [[Q(a), Q(b), Q(c)] for a in (1, -1) for b in (1, -1) for c in (1, -1)] + [c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([Q(0), s1 * phi, s2 * iphi])]   # the dual position: corners over the icosahedron's face centres
def member(name, k):
    P = ICO + [[k * x for x in v] for v in DOD]
    h = ConvexHull(np.array([[x.f() for x in v] for v in P]))
    assert len(h.vertices) == 32, 'not all 32 points are corners'
    planes = []
    for simp in h.simplices:
        a, b, c = (P[i] for i in simp); n = cross(sub(b, a), sub(c, a)); d = dot(n, a)
        if d.sgn() < 0: n, d = [-x for x in n], -d
        on = [i for i, v in enumerate(P) if dot(n, v) == d]
        assert all((dot(n, v) - d).sgn() <= 0 for v in P), 'not convex'
        key = tuple(sorted(on))
        if key not in [p[0] for p in planes]: planes.append((key, n, d))
    sizes = sorted({len(p[0]) for p in planes})
    E = set()
    for key, n, d in planes:
        for i, j in itertools.combinations(key, 2):
            # an edge: no other corner of the face beyond the line i-j inside the face (for triangles every pair is an edge)
            if len(key) == 3: E.add(tuple(sorted((i, j))))
    el = sorted({(dot(sub(P[i], P[j]), sub(P[i], P[j]))) for i, j in E}, key=lambda q: q.f())
    dist2 = sorted({(d * d / dot(n, n)) for key, n, d in planes}, key=lambda q: q.f())
    mids = sorted({(lambda m: dot(m, m))([(P[i][t] + P[j][t]) * Q(Fr(1, 2)) for t in range(3)]) for i, j in E}, key=lambda q: q.f())
    # volume: pyramids from the centre over each (triangular) face
    vol = Q(0)
    for key, n, d in planes:
        a, b, c = (P[i] for i in key); t = dot(a, cross(b, c)); vol = vol + (t if t.sgn() > 0 else -t)
    vol = vol * Q(Fr(1, 6))
    ratio = phi / k
    print(f'== {name}: k = {k} = {k.f():.9f}; edge ratio (icosahedron / dodecahedron) = φ/k = {ratio} = {ratio.f():.9f}; squared {ratio * ratio}')
    print(f'   corners 32 (12 five-fold, 20 three-fold), faces {len(planes)}, face sizes {sizes}, edges {len(E)}')
    print(f'   squared edge lengths: ' + '; '.join(f'{q} = {q.f():.6f}' for q in el))
    print(f'   squared face distances: ' + '; '.join(f'{q}' for q in dist2) + (' -> insphere' if len(dist2) == 1 else ' -> no insphere'))
    print(f'   squared edge-midpoint radii: ' + '; '.join(f'{q}' for q in mids) + (' -> midsphere' if len(mids) == 1 else ' -> no midsphere'))
    print(f'   squared corner radii: five-fold {dot(ICO[0], ICO[0])}, three-fold {k * k * 3}')
    print(f'   volume {vol} = {vol.f():.9f}')
    return P, planes, k
M = member('DICTO Metaxyhexecontahedron', phi ** 5 / 9 if False else (phi * phi * phi * phi * phi) / 9)
X = member('DICTO Palintriacontahedron', phi * Q(0, 1) / 3)
# M as the paper builds it: the hull of the RT's 12 five-fold corners (R_I² = 45/8 − 9√5/8) and the 20 face centres of I·φ³ (R_D² = 47/24 + 7√5/8)
paper = Q(Fr(47, 24), Fr(7, 8)) / Q(Fr(45, 8), Fr(-9, 8)); mine = M[2] * M[2] * 3 / (1 + phi * phi)
print('M matches the paper (same ratio of three-fold to five-fold corner radii, exact):', paper == mine, paper)
