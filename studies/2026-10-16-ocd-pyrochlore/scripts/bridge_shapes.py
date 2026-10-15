# Step 6 (DICTO: "would anything tetrahedral or octahedral with hexagon faces bridge the gaps?"). Exploratory, float.
# Gap centres in the bcc packing: octahedral sites (square-face centres of the Voronoi cell) and tetrahedral sites (cell corners
# where four cells meet). Around a site take the free hexagons of nearby OCDs that face it; the solid bounded by their planes
# (the side away from each OCD) is the candidate bridge. Checks: closed? each hexagon inside its face (full contact)?
# collision with any OCD? shape (faces, which are hexagons), volume.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
N = json.load(open('data/network.json')); R = json.load(open('data/network-render.json')); G = json.load(open('data/gaps.json'))
O = np.array(N['ocd']); T = np.array(N['T']); cube = np.array(R['cube']); V = np.array(G['V'])
EO = ConvexHull(O).equations
hexes = []
for e in EO:
    idx = np.abs(O @ e[:3] + e[3]) < 1e-7
    if idx.sum() == 6 and not any(np.allclose(e, h[0]) for h in hexes): hexes.append((e, O[idx]))
contact = [h for h in hexes if any(abs(h[0][:3] @ (t / np.linalg.norm(t)) - 1) < 1e-9 for t in np.vstack([T, -T]))]
free = [h for h in hexes if not any(h[0] is c[0] for c in contact)]
assert len(hexes) == 20 and len(free) == 12
cells = []
for m in itertools.product(range(-3, 4), repeat=4):
    p = sum(k * t for k, t in zip(m, T))
    if np.linalg.norm(p) < 3.2 and not any(np.allclose(p, c) for c in cells): cells.append(p)
def overlaps_ocd(H, c):
    A = np.vstack([H, EO - np.c_[np.zeros((len(EO), 3)), EO[:, :3] @ c]]); nrm = np.linalg.norm(A[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], nrm], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)]); return r.status == 0 and r.x[3] > 1e-7
sites = {'octahedral (square-face centre)': cube[2] * np.abs(V @ cube[2]).max(), 'tetrahedral (cell corner)': V[np.argmax(V @ (cube[0] + 0.3 * cube[1] + 0.1 * cube[2]))]}
out = []
for name, s in sites.items():
    # free hexagons near the site that face it: centre within reach and outward normal pointing towards the site
    near = []
    for c in cells:
        for e, P in free:
            hc = P.mean(0) + c; n = e[:3]
            if np.linalg.norm(hc - s) < 0.75 and n @ (s - hc) > 0: near.append((e, P + c, c))
    # the region beyond each hexagon plane:  n.(x - c) >= h   ->   -n.x + (n.c + h) <= 0, with h = -e[3]
    H = np.array([np.r_[-e[:3], e[:3] @ c - e[3]] for e, P, c in near])
    nrm = np.linalg.norm(H[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, 5)])
    line = f'{name}: {len(near)} facing hexagons'
    if r.status != 0 or r.x[3] < 1e-7: out.append(line + ': their planes enclose nothing'); continue
    try:
        X = HalfspaceIntersection(H, r.x[:3]).intersections
    except Exception as ex:
        out.append(line + f': region not closed ({type(ex).__name__})'); continue
    if not np.all(np.isfinite(X)) or np.abs(X).max() > 1e3: out.append(line + ': their planes do not close it (the region is open, it runs off to infinity)'); continue
    X = np.unique(np.round(X, 9), axis=0); hP = ConvexHull(X)
    full = all(all(np.all(hP.equations[:, :3] @ v + hP.equations[:, 3] <= 1e-9) for v in P) for e, P, c in near)
    coll = [tuple(np.round(c, 3)) for c in cells if overlaps_ocd(np.c_[hP.equations[:, :3], hP.equations[:, 3]], c)]
    pl = []
    for e in hP.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    kinds = sorted(sum(abs(X @ e[:3] + e[3]) < 1e-7) for e in pl)
    out.append(line + f': closed solid, {len(X)} corners, {len(pl)} faces with {kinds} corners each, volume {hP.volume:.6f}; '
               f'every hexagon fully inside its face: {full}; collides with {len(coll)} OCDs')
print('\n'.join(out)); open('data/bridge-shapes.txt', 'w').write('\n'.join(out) + '\n')

# Detail for the octahedral site: does each face of the bridge lie inside the hexagon in its plane (the bridge sits fully on
# the hexagons), or does it reach past the hexagon edge? Face shapes: rhombi? Volume against the gap.
s = sites['octahedral (square-face centre)']; near = []
for c in cells:
    for e, P in free:
        hc = P.mean(0) + c
        if np.linalg.norm(hc - s) < 0.75 and e[:3] @ (s - hc) > 0: near.append((e, P + c, c))
H = np.array([np.r_[-e[:3], e[:3] @ c - e[3]] for e, P, c in near]); nrm = np.linalg.norm(H[:, :3], axis=1)
r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, 5)])
X = np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0); hP = ConvexHull(X)
det = []
for e, P, c in near:
    n = e[:3]; on = X[np.abs((X - c) @ n + e[3]) < 1e-7]          # the bridge's corners in this hexagon's plane
    hx = ConvexHull(P @ np.linalg.svd(P - P.mean(0))[2][:2].T); E2 = hx.equations; B2 = np.linalg.svd(P - P.mean(0))[2][:2]
    inside = all(np.all(E2[:, :2] @ (q @ B2.T) + E2[:, 2] <= 1e-9) for q in on)
    L = [np.linalg.norm(on[i] - on[j]) for i, j in itertools.combinations(range(len(on)), 2)]
    det.append((len(on), inside))
from collections import Counter
fs = Counter(det)
extra = [f'octahedral bridge detail: faces (corners, inside its hexagon): {dict(fs)}; volume per bridge {hP.volume:.6f}; '
         f'3 bridges per OCD fill {3 * hP.volume:.6f} of the gap 0.335695 per OCD ({300 * hP.volume / 0.335695:.1f}%)']
print('\n'.join(extra)); open('data/bridge-shapes.txt', 'a').write('\n'.join(extra) + '\n')
