# Step 8 (DICTO: "pyrochlore sharing of space in conflict zones"). Exploratory, float.
# Keep all 6 limbs per copy; where two limbs cross (at a square-face centre) they share the conflict zone, as pyrochlore
# tetrahedra share corners. The zone = intersection of the crossing pair. Shape? Is it the octahedral bridge of step 6 (the solid
# bounded by the 8 facing hexagon planes)? Volumes: all limbs with shared zones against the gap.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
S = json.load(open('data/limb-sets.json')); classes = [np.array(c['P']) for c in S['classes']]
N = json.load(open('data/network.json')); T = np.array(N['T']); O = np.array(N['ocd'])
cells = []
for m in itertools.product(range(-2, 3), repeat=4):
    p = sum(k * t for k, t in zip(m, T))
    if np.linalg.norm(p) < 2.6 and not any(np.allclose(p, c) for c in cells): cells.append(p)
def inter(P, Q):
    H = np.vstack([ConvexHull(P).equations, ConvexHull(Q).equations]); nrm = np.linalg.norm(H[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if r.status != 0 or r.x[3] < 1e-7: return None
    X = np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0); return X
def shape(X):
    h = ConvexHull(X); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    return len(X), sorted(int(sum(abs(X @ e[:3] + e[3]) < 1e-7)) for e in pl), h.volume
zones = []
for a, b in itertools.combinations(range(len(classes)), 2):
    for q in cells:
        X = inter(classes[a], classes[b] + q)
        if X is not None and not any(np.allclose(np.sort(X, axis=0), np.sort(Z, axis=0), atol=1e-8) for _, _, Z in zones): zones.append((a, b, X))
vl = ConvexHull(classes[0]).volume
out = [f'limb volume {vl:.6f}; conflict zones found among the 6 limb classes (with translates): {len(zones)}']
for a, b, X in zones[:4]:
    nc, fs, v = shape(X); out.append(f'   limbs {a} x {b}: zone with {nc} corners, faces of {fs} corners, volume {v:.6f} ({100 * v / vl:.1f}% of a limb)')
# compare with the octahedral bridge of step 6: rebuild it here
EO = ConvexHull(O).equations
hexes = []
for e in EO:
    idx = np.abs(O @ e[:3] + e[3]) < 1e-7
    if idx.sum() == 6 and not any(np.allclose(e, h[0]) for h in hexes): hexes.append((e, O[idx]))
free = [h for h in hexes if not any(abs(h[0][:3] @ (t / np.linalg.norm(t)) - 1) < 1e-9 for t in np.vstack([T, -T]))]
a0, b0, Z0 = zones[0]; s0 = Z0.mean(0)
near = [(e, c) for c in cells for e, P in free if np.linalg.norm(P.mean(0) + c - s0) < 0.75 and e[:3] @ (s0 - P.mean(0) - c) > 0]
H = np.array([np.r_[-e[:3], e[:3] @ c - e[3]] for e, c in near]); nrm = np.linalg.norm(H[:, :3], axis=1)
r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, 5)])
Bx = np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0)
same = len(Bx) == len(Z0) and all(np.min(np.linalg.norm(Z0 - x, axis=1)) < 1e-7 for x in Bx)
inside = all(np.all(ConvexHull(Bx).equations[:, :3] @ z + ConvexHull(Bx).equations[:, 3] <= 1e-7) for z in Z0)
out.append(f'the octahedral bridge at that site: {shape(Bx)[0]} corners, volume {ConvexHull(Bx).volume:.6f}; zone identical to the bridge: {same}; zone inside the bridge: {inside}')
per_copy = 6 * vl - 3 * shape(Z0)[2]
out.append(f'all 6 limbs per copy with each conflict zone counted once: {per_copy:.6f} of the gap 0.335695 per copy ({100 * per_copy / 0.335695:.1f}%)')
print('\n'.join(out)); open('data/conflict.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'zone': Z0.tolist(), 'bridge': Bx.tolist()}, open('data/conflict.json', 'w'))
