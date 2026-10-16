# DICTO OCD Stella (the stella cut of the companion solid; named by DICTO 2026-10-16): render data for render_stella.html. Faces tagged by
# plane kind: golden hexagon, golden quadrilateral, companion triangle (OCD hexagon planes), joint triangle (cell hexagon walls). The OCD inside
# and the 8 joint neighbours (the shortest lattice vectors). Float from data/stella-cut-exact.json (exact there).
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
D = json.load(open('data/stella-cut-exact.json')); S = D['S']; V = np.array(S['v']); C = np.array(D['cell']['v']); Bs = np.array(D['basis'])
O = np.array(json.load(open('data/network.json'))['ocd'])
Hc = ConvexHull(C); walls = np.unique(np.round(Hc.equations, 6), axis=0)
def kind(f):
    P = V[f]
    if len(f) == 6: return 'ghex'
    if len(f) == 4: return 'gquad'
    on_wall = any(np.all(np.abs(P @ w[:3] + w[3]) < 1e-6) for w in walls)
    return 'joint' if on_wall else 'ctri'
def order(f):   # corners of a planar convex face in cyclic order
    P = V[f]; c = P.mean(0); nn = np.cross(P[1] - P[0], P[2] - P[0]); nn /= np.linalg.norm(nn); u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(nn, u)
    return [f[i] for i in np.argsort(np.arctan2((P - c) @ w, (P - c) @ u))]
S['f'] = [order(f) for f in S['f']]
kinds = [kind(f) for f in S['f']]
H = ConvexHull(V); inside = np.all(O @ H.equations[:, :3].T + H.equations[:, 3] <= 1e-6)
vecs = sorted({tuple(np.round(Bs.T @ np.array(m, float), 9)) for m in itertools.product(range(-2, 3), repeat=3) if any(m)}, key=lambda v: np.linalg.norm(v))
L = np.linalg.norm(vecs[0]); nb = [list(v) for v in vecs if abs(np.linalg.norm(v) - L) < 1e-6]
ho = ConvexHull(O); groups = {}
for s, e in zip(ho.simplices, ho.equations): groups.setdefault(tuple(np.round(e, 6)), set()).update(s)
of = []
for k, idx in groups.items():
    idx = list(idx); nn = np.array(k[:3]); c = O[idx].mean(0); u = O[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(nn, u)
    of.append([int(i) for i in sorted(idx, key=lambda i: np.arctan2((O[i] - c) @ w, (O[i] - c) @ u))])
json.dump({'S': {'v': V.tolist(), 'f': S['f'], 'k': kinds}, 'ocd': {'v': O.tolist(), 'f': of}, 'nb': nb}, open('data/stella-render.json', 'w'))
from collections import Counter; print(Counter(kinds), 'nb lengths', sorted({round(float(np.linalg.norm(v)),4) for v in nb}), 'S radius', round(float(np.linalg.norm(V,axis=1).max()),4), 'OCD inside S:', bool(inside), 'joint neighbours:', len(nb), 'ocd faces', len(of))
