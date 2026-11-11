"""EXACT proof (rational arithmetic) that DICTO's closed Hemi RD build, the chamfered cube, fills space with cube pyramids.
Z = the zonohedron with generators e1, e2, e3 (unit) and the four half body diagonals (+-1/2, +-1/2, +-1/2) (one of each pair);
this is DICTO's 14 Hemi RDs + 6 cube pyramids (hull of the build, matched numerically to 1e-9 in analyse_build.py).
Claim: Z + L and the unit cube Q + (2,0,0) + L, L = {(a,b,c) in Z^3 even, a+b+c = 0 mod 4} (det 16), tile space.
Proof: (1) vol Z = 15 exactly (zonotope volume = sum of |det| over generator triples); vol Q = 1; det L = 16; so the pieces have
density 1. (2) Any two pieces have disjoint interiors: for every pair within reach, an exact separating axis (a facet normal of either
piece or a cross product of an edge direction of each) gives projections that meet in at most a point. A packing of space by convex
bodies with density 1 is a tiling. FINAL ok only if every pair separates and the volumes match."""
import itertools
from fractions import Fraction as F
h = F(1, 2)
G = [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)), (h, h, h), (h, h, -h), (h, -h, h), (-h, h, h)]
def det3(a, b, c): return a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
volZ = sum(abs(det3(*t)) for t in itertools.combinations(G, 3))
# vertices of Z: sums of +-g/2 that are extreme = all sign choices, then keep the extreme ones (support check by facets below)
pts = {tuple(sum(s * g[i] / 2 for s, g in zip(sg, G)) for i in range(3)) for sg in itertools.product((1, -1), repeat=7)}
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return sum(x*y for x, y in zip(a, b))
normals = {n for a, b in itertools.combinations(G, 2) for n in [cross(a, b)] if any(n)}
def support(P, n): return max(dot(p, n) for p in P)
# extreme vertices: a point is a vertex if it is the unique maximiser of some generic direction; simpler: keep points on >= 3 facet planes
fac = [(n, support(pts, n)) for n in normals] + [(tuple(-x for x in n), support(pts, tuple(-x for x in n))) for n in normals]
VZ = [p for p in pts if sum(1 for n, c in fac if dot(p, n) == c) >= 3]
print('Z:', len(VZ), 'vertices,', len(fac), 'facet planes, volume', volZ)
Q = [tuple(F(x) for x in v) for v in itertools.product((h, -h), repeat=3)]
EZ = [g for g in G]; EQ = [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))]   # edge directions (zonotope edges = generators)
NZ = [n for n, c in fac]; NQ = [(F(1),F(0),F(0)), (F(0),F(1),F(0)), (F(0),F(0),F(1))]
def axes(e1, e2, n1, n2): return set(n1) | set(n2) | {cross(a, b) for a in e1 for b in e2 if any(cross(a, b))}
AXZZ = axes(EZ, EZ, NZ, NZ); AXZQ = axes(EZ, EQ, NZ, NQ); AXQQ = axes(EQ, EQ, NQ, NQ)
def separated(P, Qp, AX):
    for n in AX:
        a0, a1 = min(dot(p, n) for p in P), max(dot(p, n) for p in P)
        b0, b1 = min(dot(p, n) for p in Qp), max(dot(p, n) for p in Qp)
        if a1 <= b0 or b1 <= a0: return True
    return False
L = [(a, b, c) for a in range(-6, 7, 2) for b in range(-6, 7, 2) for c in range(-6, 7, 2) if (a + b + c) % 4 == 0]
sh = lambda P, t: [tuple(x + y for x, y in zip(p, t)) for p in P]
cq = (F(2), F(0), F(0)); bad = 0; pairs = 0
reach = 6   # diameter bound: Z within |x|_inf <= 3/2 + ... ; pairs farther than 6 apart are separated trivially
for t in L:
    if t == (0, 0, 0) or max(abs(x) for x in t) > reach: continue
    pairs += 1; bad += not separated(VZ, sh(VZ, t), AXZZ)
for t in L:
    for P, AX in [(VZ, AXZQ)]:
        s = tuple(x + y for x, y in zip(t, cq))
        if max(abs(x) for x in s) > reach: continue
        pairs += 1; bad += not separated(P, sh(Q, s), AX)
for t in L:
    s0 = cq; s1 = tuple(x + y for x, y in zip(t, cq))
    if t == (0, 0, 0) or max(abs(x) for x in t) > reach: continue
    pairs += 1; bad += not separated(sh(Q, s0), sh(Q, s1), AXQQ)
detL = abs(det3((2, 2, 0), (2, 0, 2), (0, 2, 2)))
print(f'pairs checked {pairs}, not separated {bad}; vol Z = {volZ}, vol Q = 1, det L = {detL}')
ok = bad == 0 and volZ + 1 == detL and volZ == 15
print('FINAL ok: chamfered cubes + cubes (6 cube pyramids each) tile space (exact)' if ok else 'FINAL FAIL')
