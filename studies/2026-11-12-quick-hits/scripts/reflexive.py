# reflexive.py: independent exact check (our own code) of Hofscheier and Nill, "Reflexive polytopes can have doubly exponentially many
# vertices" (aiXiv 2611.00775), Theorems 2.1 and 2.2: P8 is an 8-dimensional reflexive polytope with 44 vertices and 1371 facets
# (> 6^4 = 1296); P9 is a 9-dimensional reflexive polytope with 48 vertices and 3378 facets (> 6^4.5 ~ 3174.5). Built from the paper's
# Q3 (21 points) and Q2 (15 points): Q o Q = free sum = conv(Q x 0  u  0 x Q).
# Reflexive: the origin is interior and every facet is {a.x = 1} with a an INTEGER vector. Facets found from qhull's triangulation, then
# each facet plane recomputed EXACTLY (fractions) through d of its points; supporting checked exactly against all points; duplicates
# merged. Control: the free sum of hexagons H o H o H o H (Nill's extremal case, reflexive, 6^4 = 1296 facets) must give exactly 1296.
import itertools, math
from fractions import Fraction as F
import numpy as np
from scipy.spatial import ConvexHull
Q3 = [(6,-6,0),(4,0,-2),(3,1,-2),(3,0,0),(3,0,-3),(2,1,-1),(2,-2,2),(1,1,-1),(1,0,1),(1,-1,2),(0,0,-3),(0,-1,2),(0,-3,3),(0,-6,0),(0,-6,-6),(-1,0,0),(-1,0,-1),(-1,-2,2),(-2,-1,-1),(-2,-2,-2),(-3,-3,0)]
Q2 = [(-42,168),(-21,63),(-14,35),(-10,22),(-7,14),(-2,1),(-1,-1),(0,-2),(1,-2),(2,-1),(2,0),(0,14),(-6,54),(-14,98),(-42,210)]
H = [(1,0),(1,1),(0,1),(-1,0),(-1,-1),(0,-1)]
def free_sum(*Qs):
    dims = [len(Q[0]) for Q in Qs]; out = []
    for k, Q in enumerate(Qs):
        for q in Q: out.append(tuple(0 for d in dims[:k] for _ in range(d)) + tuple(q) + tuple(0 for d in dims[k+1:] for _ in range(d)))
    return out
P8 = [p + (-1, -1) for p in free_sum(Q3, Q3)] + [(0,) * 6 + t for t in ((-1, 2), (1, -1))]
P9 = [p + (-1, -1, -1) for p in free_sum(Q2, Q2, Q2)] + [(0,) * 6 + t for t in ((-1, -1, 6), (-1, 2, -1), (1, -1, -1))]
HHHH = free_sum(H, H, H, H)
def solve(M, b):
    n = len(M); A = [[F(x) for x in row] + [F(bb)] for row, bb in zip(M, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]
def analyse(name, pts):
    X = np.array(pts, float); d = X.shape[1]; h = ConvexHull(X)
    verts = sorted(set(h.vertices.tolist())); planes = set(); bad_int = 0; bad_sup = 0
    for simp in h.simplices:
        a = solve([pts[i] for i in simp], [1] * d)
        if a is None: continue
        key = tuple(a)
        if key in planes: continue
        if any(sum(ai * xi for ai, xi in zip(a, p)) > 1 for p in pts): bad_sup += 1; continue
        planes.add(key)
        if any(ai.denominator != 1 for ai in a): bad_int += 1
    print(f'{name}: dimension {d}, points {len(pts)}, vertices {len(verts)}, facets {len(planes)}, facets with a non-integer normal {bad_int}, non-supporting planes {bad_sup}', flush=True)
    return len(verts), len(planes), bad_int
c = analyse('control H o H o H o H', HHHH)
r8 = analyse('P8', P8)
r9 = analyse('P9', P9)
ok = c == (24, 1296, 0) and r8 == (44, 1371, 0) and r9 == (48, 3378, 0)
print(f'claims: P8 44 vertices, 1371 facets > {6**4}; P9 48 vertices, 3378 facets > {6**4.5:.1f}; both reflexive')
print('FINAL ok: both theorems confirmed exactly' if ok else 'FINAL FAIL')
