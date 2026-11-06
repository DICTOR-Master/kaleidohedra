"""#47 open question 1 (DICTO 11-06 "go ahead with #47"): does C + T + O (edge 1) fill space with no connector?
Construction: the octet (tetrahedral-octahedral honeycomb) cut along its triangle planes: every octahedron and tetrahedron lies between
two neighbouring planes (vertices = fcc points, planes = close-packed layers, spacing sqrt(2/3)), so a layer is a flat slab. Cubes of
edge 1 make flat slabs too. Stack: cubes for z in [-2, 0], octet layers for z in [0, 3h], cubes again above. Check: random points in a
box, each inside exactly one tile; every tile a regular solid of edge 1 (edge lengths checked); each kind used."""
import numpy as np, itertools, time
from scipy.spatial import ConvexHull
t0 = time.time(); h = np.sqrt(2 / 3)
a1 = np.array([1., 0, 0]); a2 = np.array([.5, np.sqrt(3) / 2, 0])
shift = [np.zeros(3), (a1 + a2) / 3, 2 * (a1 + a2) / 3]   # A, B, C close-packed positions
R = 6
def layer_pts(k):   # ABC stacking (fcc): layer k at height k h, offset shift[k % 3]
    return [i * a1 + j * a2 + shift[k % 3] + np.array([0, 0, k * h]) for i in range(-R, R + 1) for j in range(-R, R + 1)]
tiles = []
NL = 3
for k in range(NL):
    lo, hi = layer_pts(k), layer_pts(k + 1)
    P = np.array(lo + hi)
    # all tets/octs of the octet between planes k and k+1: unit-edge simplices/octahedra from points at distance 1
    from scipy.spatial import cKDTree
    T = cKDTree(P); nb = T.query_pairs(1 + 1e-6)
    adj = {i: set() for i in range(len(P))}
    for i, j in nb:
        if abs(np.linalg.norm(P[i] - P[j]) - 1) < 1e-6: adj[i].add(j); adj[j].add(i)
    nlo = len(lo); found = set()
    for i in range(len(P)):
        for j, k2, l in itertools.combinations(sorted(adj[i]), 3):
            if j < i or k2 < i or l < i: continue
            if k2 in adj[j] and l in adj[j] and l in adj[k2]:
                q = (i, j, k2, l)
                if any(x < nlo for x in q) and any(x >= nlo for x in q): found.add(('T', q))
    # octahedra: 3 lo + 3 hi, all pairwise at 1 except 3 opposite pairs at sqrt2
    for i in range(nlo):
        for j, k2 in itertools.combinations(sorted(x for x in adj[i] if x < nlo), 2):
            if k2 not in adj[j]: continue
            tri = (i, j, k2); c = P[list(tri)].mean(0)
            # the hi triangle above the centre, turned 60 deg: hi points at distance 1 from two of the tri
            up = [x for x in range(nlo, len(P)) if sum(x in adj[y] for y in tri) == 2]
            up = [x for x in up if np.linalg.norm(P[x, :2] - c[:2]) < 0.6]
            if len(up) == 3: found.add(('O', tuple(sorted(tri + tuple(up)))))
    for kind, q in found: tiles.append((kind, P[list(q)]))
# cubes below z=0 and above z=NL*h
for i, j, k in itertools.product(range(-R, R), range(-R, R), range(-2, 0)):
    tiles.append(('C', np.array([[i + a, j + b, k + c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], float)))
top = NL * h
for i, j, k in itertools.product(range(-R, R), range(-R, R), range(0, 2)):
    tiles.append(('C', np.array([[i + a, j + b, top + k + c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], float)))
# edge check
def edges_ok(kind, V):
    D = np.linalg.norm(V[:, None] - V[None], axis=2); d = np.sort(D[np.triu_indices(len(V), 1)])
    want = {'T': [1] * 6, 'O': [1] * 12 + [np.sqrt(2)] * 3, 'C': [1] * 12 + [np.sqrt(2)] * 12 + [np.sqrt(3)] * 4}[kind]
    return np.allclose(d, sorted(want), atol=1e-6)
assert all(edges_ok(k, V) for k, V in tiles)
hulls = [ConvexHull(V) for _, V in tiles]
rng = np.random.default_rng(1); N = 200000
pts = np.c_[rng.uniform(-3, 3, (N, 2)), rng.uniform(-1.9, top + 1.9, N)]
cnt = np.zeros(N, int)
for hh in hulls: cnt += (hh.equations[:, :3] @ pts.T + hh.equations[:, 3:4] <= 1e-12).all(0)
from collections import Counter
print('tiles', Counter(k for k, _ in tiles), 'volumes T/O/C', [round(np.mean([hh.volume for (k, _), hh in zip(tiles, hulls) if k == K]), 6) for K in 'TOC'])
print(f'points {N}: exactly once {np.mean(cnt == 1):.6f}, min {cnt.min()}, max {cnt.max()}')
ok = cnt.min() == 1 and cnt.max() == 1
print(f"FINAL {'OK' if ok else 'FAIL'} {time.time() - t0:.0f}s")
