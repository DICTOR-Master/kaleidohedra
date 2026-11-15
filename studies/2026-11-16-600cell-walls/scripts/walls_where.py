#!/usr/bin/env python3
"""Where do B's 40 visible plates point? Compare each plate's normal direction with the directions of the 600-cell's
corners (= its mirrors), edge midpoints, triangle centres, cell centres (= 120-cell corners)."""
import runpy, sys, io, contextlib, itertools, numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(sys.argv[1] if len(sys.argv) > 1 else 'walls.py')
P, F, faces2, plane_normal, canon, mirrors = (g[k] for k in ('P', 'F', 'faces2', 'plane_normal', 'canon', 'mirrors'))
from scipy.spatial import ConvexHull
d = np.linalg.norm(P[:, None] - P[None], axis=2); e = d[d > 1e-9].min()
edges = [(i, j) for i in range(120) for j in range(i + 1, 120) if abs(d[i, j] - e) < 1e-7]
tris = [t for t in itertools.combinations(range(120), 3) if all(abs(d[a, b] - e) < 1e-7 for a, b in itertools.combinations(t, 2))]
cells = ConvexHull(P).simplices
fam = {'corners (mirrors)': P, 'edge midpoints': np.array([P[list(x)].mean(0) for x in edges]),
       'triangle centres': np.array([P[list(x)].mean(0) for x in tris]), 'cell centres (120-cell corners)': np.array([P[s].mean(0) for s in cells])}
dirs = {k: np.unique(np.round([canon(v) for v in V], 9), axis=0) for k, V in fam.items()}
print({k: len(v) for k, v in dirs.items()}, 'edges', len(edges), 'triangles', len(tris))
fac, rid = faces2(F); out = {}
for c in rid:
    n = plane_normal(F, c); hit = [k for k, D in dirs.items() if np.min(np.linalg.norm(D - n, axis=1)) < 1e-7]
    k = (len(c), tuple(hit)); out[k] = out.get(k, 0) + 1
for k, v in sorted(out.items(), key=str): print(v, 'plates on', k[0], '-gons; normal along:', k[1] or 'none of these')
checks = [len(edges) == 720, len(tris) == 1200, len(cells) == 600]
print('checks', checks); print('FINAL ok' if all(checks) else 'FINAL FAIL checks')
