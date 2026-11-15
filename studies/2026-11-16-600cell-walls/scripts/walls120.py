#!/usr/bin/env python3
"""Lead 3 of the walls test: do B's 40 non-wall plates (the phi*sqrt2 triangles) lie in the 120-cell's own Vacuus plates?
The 120-cell Q = the dual of the 600-cell P (its 600 vertices = the centroids of P's 600 tetrahedra). Its plates = central
hyperplanes spanned by its 720 pentagons. Same mirrors as P (both H4). Floating point, tolerance 1e-7."""
import runpy, numpy as np, sys, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(sys.argv[1] if len(sys.argv) > 1 else 'walls.py')
P, F, faces2, plane_normal, mirrors, Pplates, test = (g[k] for k in ('P', 'F', 'faces2', 'plane_normal', 'mirrors', 'Pplates', 'test'))
from scipy.spatial import ConvexHull
h = ConvexHull(P); C = {}
for s_ in h.simplices:
    v = P[s_].mean(0); C.setdefault(tuple(np.round(v, 5) + 0.0), v)
C = np.array(list(C.values()))
print('120-cell vertices:', len(C))
fQ, ridQ = faces2(C, 4); print('120-cell: cells', len(fQ), '2-faces', len(ridQ))
Qplates = np.unique(np.round([plane_normal(C, c) for c in ridQ], 9), axis=0); print("120-cell's own Vacuus plates:", len(Qplates))
qinM = sum(np.min(np.linalg.norm(mirrors - n, axis=1)) < 1e-7 for n in Qplates); print('of which H4 mirrors:', qinM)
fac, rid = faces2(F); res = {}
for c in rid:
    n = plane_normal(F, c); w6 = np.min(np.linalg.norm(Pplates - n, axis=1)) < 1e-7; w120 = np.min(np.linalg.norm(Qplates - n, axis=1)) < 1e-7
    k = (len(c), bool(w6), bool(w120)); res[k] = res.get(k, 0) + 1
print('B by (corners, 600-cell wall, 120-cell wall):', res)
hidden = sum(v for k, v in res.items() if k[1] or k[2])
checks = [len(C) == 600, len(fQ) == 120, len(ridQ) == 720]
print(f'B plates in the walls of the pair: {hidden} of {len(rid)}'); print('checks', checks)
print('FINAL ok' if all(checks) else 'FINAL FAIL checks')
