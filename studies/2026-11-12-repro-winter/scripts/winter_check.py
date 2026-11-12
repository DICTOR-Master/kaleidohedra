# winter_check.py: independent numerical test (our own code) of Winter, "A relation between Mahler volume and flag number for convex
# polytopes" (aiXiv 2610.00447, arXiv 2610.09990). Theorem 1: vol(P) vol((P - P)^o) <= F(P) / (d!)^2, F = number of flags.
# Corollary 2 (centrally symmetric): vol(P) vol(P^o) <= 2^d F(P) / (d!)^2. Conjecture 3: equality exactly for Hanner polytopes (and,
# in (1), their faces). Here d = 2, 3, 4: regular polygons, the Platonic solids, prisms, bipyramids, random polytopes (generic points in
# a ball and on a sphere), the cube / cross-polytope (Hanner: equality), simplices, the 4-cube, 16-cell, 24-cell, random 4-polytopes.
# Flags from the face lattice built from the hull (coplanar facets merged). Volumes by convex hulls; (P-P)^o by halfspace intersection.
# Controls: the cube and the cross-polytope must give EQUALITY in (1) (Hanner) to 1e-9; every case must satisfy (1).
import itertools, math, sys
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
rng = np.random.default_rng(12)
def facets(P):
    h = ConvexHull(P); E = h.equations; n = len(E); par = list(range(n))
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for i in range(n):
        for j in h.neighbors[i]:
            if np.abs(E[i] - E[j]).max() < 1e-9: par[f(i)] = f(j)
    G = {}
    for i in range(n): G.setdefault(f(i), set()).update(h.simplices[i].tolist())
    eq = {}
    for i in range(n): eq[f(i)] = E[i]
    return [(frozenset(v), eq[k]) for k, v in G.items()], h
def flags(P, idx=None):
    """number of flags of the polytope conv(P) (full-dimensional in its own span), recursively over facets"""
    P = np.asarray(P, float); d = np.linalg.matrix_rank(P[1:] - P[0]) if len(P) > 1 else 0
    if d == 0: return 1
    if d == 1: return 2
    c = P.mean(0); B = np.linalg.svd(P - c)[2][:d]; Q = (P - c) @ B.T      # coordinates in the affine span
    F, h = facets(Q)
    verts = set(h.vertices.tolist())
    return sum(flags(Q[sorted(v & verts)]) for v, _ in F)
def polar_vol(P):
    """vol of the polar of conv(P) (P must contain the origin in its interior)"""
    F, h = facets(P)
    H = np.array([eq for _, eq in F]); H = H / (-H[:, -1:])                  # a.x <= 1  ->  rows (a, -1)
    pts = H[:, :-1]                                                         # polar of {a.x <= 1} = conv of the a's
    return ConvexHull(pts).volume
def winter(P):
    P = np.asarray(P, float); d = P.shape[1]; h = ConvexHull(P); V = P[h.vertices]
    D = np.array([p - q for p in V for q in V])                             # P - P = conv of pairwise differences
    lhs = h.volume * polar_vol(D); rhs = flags(V) / math.factorial(d) ** 2
    W = np.round(V - V.mean(0), 9) + 0.0; cs = {tuple(r) for r in W} == {tuple(r) for r in (-W + 0.0)}   # whole points (12 Nov fix: columns were sorted apart)
    mahler = h.volume * polar_vol(V - V.mean(0)) if cs else None
    return lhs, rhs, mahler
phi = (1 + 5 ** .5) / 2
cases = {}
for n in (3, 4, 5, 6, 8, 12): cases[f'{n}-gon'] = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
cube = list(itertools.product((-1, 1), repeat=3)); octa = [tuple(s * (i == j) for j in range(3)) for i in range(3) for s in (1, -1)]
tet = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
ico = [p for a in ((0, 1, phi),) for c in (a, (a[1], a[2], a[0]), (a[2], a[0], a[1])) for p in [tuple(s * x for s, x in zip(sg, c)) for sg in itertools.product((1, -1), repeat=3)]]
dod = list(itertools.product((-1, 1), repeat=3)) + [p for a in ((0, 1 / phi, phi),) for c in (a, (a[1], a[2], a[0]), (a[2], a[0], a[1])) for p in [tuple(s * x for s, x in zip(sg, c)) for sg in itertools.product((1, -1), repeat=3)]]
cases.update({'cube (Hanner)': cube, 'octahedron (Hanner)': octa, 'tetrahedron': tet, 'icosahedron': ico, 'dodecahedron': dod})
for n in (3, 5, 6, 8):
    ring = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
    cases[f'{n}-prism'] = [(x, y, z) for x, y in ring for z in (-1, 1)]; cases[f'{n}-bipyramid'] = [(x, y, 0) for x, y in ring] + [(0, 0, 1), (0, 0, -1)]
perm = list(set(itertools.permutations((-2, -1, 1, 2))))                       # 4D permutohedron (truncated octahedron in 3D: project)
c4 = list(itertools.product((-1, 1), repeat=4)); x16 = [tuple(s * (i == j) for j in range(4)) for i in range(4) for s in (1, -1)]
c24 = list(set(tuple(v) for p in itertools.permutations((1, 1, 0, 0)) for v in [tuple(s * x for s, x in zip(sg, p)) for sg in itertools.product((1, -1), repeat=4)]))
simplex4 = [tuple(1 if j == i else 0 for j in range(4)) for i in range(4)] + [(-.25, -.25, -.25, -.25)]
cases.update({'4-cube (Hanner)': c4, '16-cell (Hanner)': x16, '24-cell': c24, '4-simplex': simplex4})
for k in range(40): cases[f'random 3D {k}'] = rng.normal(size=(int(rng.integers(8, 30)), 3))
for k in range(20): X = rng.normal(size=(int(rng.integers(10, 40)), 3)); cases[f'random 3D sphere {k}'] = X / np.linalg.norm(X, axis=1)[:, None]
for k in range(15): cases[f'random 4D {k}'] = rng.normal(size=(int(rng.integers(10, 25)), 4))
for k in range(10): X = rng.normal(size=(int(rng.integers(6, 16)), 3)); cases[f'random 3D symmetric {k}'] = np.vstack([X, -X])
worst = 0; ok = True; rows = []
for name, P in cases.items():
    lhs, rhs, m = winter(P); r = lhs / rhs; worst = max(worst, r); ok &= lhs <= rhs * (1 + 1e-9)
    d = np.asarray(P).shape[1]; c2 = None if m is None else m / (2 ** d * flags(np.asarray(P, float)[ConvexHull(np.asarray(P, float)).vertices]) / math.factorial(d) ** 2)
    if c2 is not None: ok &= c2 <= 1 + 1e-9
    rows.append((name, r, c2))
    if not name.startswith('random') or r > 0.95: print(f'{name:24s} (1): lhs/rhs = {r:.9f}' + ('' if c2 is None else f'   (2): {c2:.9f}'), flush=True)
eq = {n: r for n, r, _ in rows if 'Hanner' in n}
print(f'cases {len(rows)}; all satisfy (1){" and (2) where centrally symmetric" if ok else ""}: {ok}; largest ratio {worst:.9f}; Hanner ratios {eq}')
ctrl = all(abs(r - 1) < 1e-9 for r in eq.values())
print('FINAL ok' if ok and ctrl else 'FINAL FAIL')
