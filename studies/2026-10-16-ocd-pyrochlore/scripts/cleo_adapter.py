# Step 11 (DICTO: "where are the AXE and CLEOs when we need them?"). Exploratory, float.
# Face check (in the icosahedral frame): AXE has faces perpendicular to 3- and 5-fold axes only; CLEO one 3-fold and three
# 5-fold; FUJI four 3-fold and three 5-fold. None has a golden-rhombus plane (perpendicular to a 2-fold axis). The Cleo-Ico
# (pyramid on an icosahedron face, apex at the centre) has a 3-fold base and three 2-fold sides: a hexagon-to-golden-rhombi adapter.
# Here: a Cleo-Ico on each of the 12 free hexagons, base = the hexagon's alternate corners, apex outward; fit and collisions.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T'])
EO = ConvexHull(O).equations
hexes = []
for e in EO:
    idx = np.abs(O @ e[:3] + e[3]) < 1e-7
    if idx.sum() == 6 and not any(np.allclose(e, h[0]) for h in hexes): hexes.append((e, O[idx]))
free = [h for h in hexes if not any(abs(h[0][:3] @ (t / np.linalg.norm(t)) - 1) < 1e-9 for t in np.vstack([T, -T]))]
r = np.linalg.norm(O, axis=1); A5 = O[np.abs(r - r.max()) < 1e-9]; A5 /= np.linalg.norm(A5, axis=1)[:, None]
pieces = []
for e, H in free:
    n = e[:3] / np.linalg.norm(e[:3]); c = H.mean(0)
    ang = np.arctan2((H - c) @ np.cross(n, H[0] - c), (H - c) @ (H[0] - c)); H = H[np.argsort(ang)]
    best = None
    for start in (0, 1):                                   # the two inscribed triangles (alternate corners)
        tri = H[start::2]; L = np.linalg.norm(tri[0] - tri[1])
        apex = c + n * L * ((3 + 5 ** .5) / (4 * 3 ** .5))     # icosahedron inradius for edge L: phi^2 / (2 sqrt3) * L
        P = np.vstack([tri, apex])
        # sides: the planes through the apex and each base edge must be perpendicular to two-fold axes (golden-rhombus planes)
        ok = True
        for i in range(3):
            q = np.cross(tri[(i + 1) % 3] - tri[i], apex - tri[i]); q /= np.linalg.norm(q)
            two = [ (A5[a] + A5[b]) / np.linalg.norm(A5[a] + A5[b]) for a, b in itertools.combinations(range(12), 2) if abs(A5[a] @ A5[b] - 1 / 5 ** .5) < 1e-9]
            if max(abs(np.array(two) @ q)) < 1 - 1e-7: ok = False
        if ok: best = P
    pieces.append(best)
fitted = sum(p is not None for p in pieces)
print(f'Cleo-Ico on the 12 free hexagons: {fitted} fit with golden-rhombus sides (the other inscribed triangle does not)', flush=True)
cells = []
for m in itertools.product(range(-2, 3), repeat=4):
    p = sum(k * t for k, t in zip(m, T))
    if 1e-9 < np.linalg.norm(p) < 2.6 and not any(np.allclose(p, c) for c in cells): cells.append(p)
def overlap(E1, E2):
    H = np.vstack([E1, E2]); nrm = np.linalg.norm(H[:, :3], axis=1)
    rr = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)]); return rr.status == 0 and rr.x[3] > 1e-8
shift = lambda E, c: E - np.c_[np.zeros((len(E), 3)), E[:, :3] @ c]
EP = [ConvexHull(P).equations for P in pieces if P is not None]
hits_ocd = sum(overlap(E, shift(EO, c)) for E in EP for c in cells)
hits_cleo = sum(overlap(E, shift(F, c)) for E in EP for F in EP for c in cells)
own = sum(overlap(EP[a], EP[b]) for a, b in itertools.combinations(range(len(EP)), 2))
v = ConvexHull(pieces[0]).volume
out = [f'Cleo-Ico adapters: {fitted} per copy, each volume {v:.6f} (base edge {np.linalg.norm(pieces[0][0] - pieces[0][1]):.6f}); '
       f'collisions: with neighbouring OCDs {hits_ocd}, with neighbours\' adapters {hits_cleo}, among one copy\'s own adapters {own}',
       f'they fill {fitted * v:.6f} of the gap 0.335695 per copy ({100 * fitted * v / 0.335695:.1f}%); each hexagon keeps 3 small corner triangles outside the base']
print('\n'.join(out)); open('data/cleo-adapter.txt', 'w').write('\n'.join(out) + '\n')
json.dump([P.tolist() for P in pieces if P is not None], open('data/cleo-adapter.json', 'w'))
