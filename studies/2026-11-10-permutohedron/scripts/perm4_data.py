"""Data for the 3D build of the 4D permutohedron (DICTO 10 Nov: "can we build a permutahedron" -> "4D one, as 3D build").
Corners: the 120 orderings of (1, 2, 3, 4, 5), in an orthonormal frame of the hyperplane x1 + ... + x5 = 15. Cells: one per proper non-empty
subset S of {1..5} (the corners whose coordinates on S are the |S| smallest values): |S| = 1 or 4 -> truncated octahedron (24 corners, 10
cells), |S| = 2 or 3 -> hexagonal prism (12 corners, 20 cells). Each cell's faces (squares, hexagons) as corner loops; the edges; a generic
sweep direction with every event (births, deaths, swaps: pairs letting go and meeting). Checks: 120 corners, 240 edges, 30 cells, every corner
in 4 cells (simple), sweep counts = h-vector (26, 66, 26)."""
import itertools, json, numpy as np
from scipy.spatial import ConvexHull
P = np.array(list(itertools.permutations(range(1, 6))), float); n = len(P)
c = P.mean(0); U, S_, Vt = np.linalg.svd(P - c); B = Vt[:4]; X = (P - c) @ B.T          # 4D coordinates
edges = [(i, j) for i, j in itertools.combinations(range(n), 2) if np.abs(P[i] - P[j]).sum() == 2 and sorted(np.abs(P[i] - P[j])) == [0, 0, 0, 1, 1]]
cells = []
for k in range(1, 5):
    for S in itertools.combinations(range(5), k):
        vs = [v for v in range(n) if set(P[v, list(S)].astype(int)) == set(range(1, k + 1))]
        cells.append({'S': list(S), 'kind': 'TO' if k in (1, 4) else 'HP', 'V': vs})
for cl in cells:                                                                      # faces: hull in the cell's own 3D frame
    Y = X[cl['V']]; cc = Y.mean(0); u, s_, vt = np.linalg.svd(Y - cc); Z = (Y - cc) @ vt[:3].T; h = ConvexHull(Z); F = {}
    for simp, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    faces = []
    for eq, vs in F.items():
        vs = list(vs); nrm = np.array(eq[:3]); cen = Z[vs].mean(0); e1 = Z[vs[0]] - cen; e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
        vs.sort(key=lambda q: np.arctan2((Z[q] - cen) @ e2, (Z[q] - cen) @ e1)); faces.append([cl['V'][q] for q in vs])
    cl['F'] = faces
per = [sum(v in cl['V'] for cl in cells) for v in range(n)]
assert (len(edges), len(cells), set(per)) == (240, 30, {4}), (len(edges), len(cells), set(per))
pairs = [(a, b, sorted(set(cells[a]['V']) & set(cells[b]['V']))) for a, b in itertools.combinations(range(30), 2)]
pairs = [(a, b, f) for a, b, f in pairs if len(f) >= 3]
d = np.array([0.26, 0.53, -0.72, 0.36]); d /= np.linalg.norm(d); H = X @ d; hs = np.sort(H); assert np.min(np.diff(hs)) > 1e-6
def state(z):
    alive = {i for i, cl in enumerate(cells) if H[cl['V']].min() < z < H[cl['V']].max()}
    return alive, {(a, b) for a, b, f in pairs if H[f].min() < z < H[f].max()}
ev = []; prev = state((hs[0] + hs[1]) / 2); cnt = {'born': 0, 'died': 0, 'swap': 0}
for k in range(1, n - 1):
    cur = state((hs[k] + hs[k + 1]) / 2)
    lost = [list(e) for e in prev[1] - cur[1] if e[0] in cur[0] and e[1] in cur[0]]; gained = [list(e) for e in cur[1] - prev[1] if e[0] in prev[0] and e[1] in prev[0]]
    born = sorted(cur[0] - prev[0]); died = sorted(prev[0] - cur[0])
    cnt['born'] += len(born); cnt['died'] += len(died); cnt['swap'] += 1 if (lost and gained) else 0
    ev.append({'h': float(hs[k]), 'lost': lost, 'gained': gained, 'born': born, 'died': died}); prev = cur
print('sweep counts', cnt, ' expected h = (26, 66, 26)')
assert cnt == {'born': 26, 'died': 26, 'swap': 66}
out = {'X': np.round(X, 6).tolist(), 'edges': edges, 'cells': [{'kind': cl['kind'], 'S': cl['S'], 'V': cl['V'], 'F': cl['F']} for cl in cells],
       'sweep': {'d': d.tolist(), 'hmin': float(hs[0]), 'hmax': float(hs[-1]), 'events': ev}, 'pairs': [[a, b, f] for a, b, f in pairs]}
json.dump(out, open('perm4.json', 'w'), separators=(',', ':')); print('cells', sum(cl['kind'] == 'TO' for cl in cells), 'TO,', sum(cl['kind'] == 'HP' for cl in cells), 'prisms; FINAL ok')
