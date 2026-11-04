#!/usr/bin/env python3
"""Interlocking (Dyskin kinematic test, slides + twists; interlock_rot.py of 2026-11-04-hopf-interlock, calibrated) of the β-tin tiling by S(2) = T(4) minus corners.
Slab = tiles whose centroids lie within half a period of a plane through the origin, for normals (0,0,1), (1,1,1), (1,1,0); inner tiles (lateral distance < 3) tested,
the rest fixed. Same calibration line as the original (Dyskin tetrahedra) is run first by the imported module."""
import os, sys, json, itertools, numpy as np
here = os.getcwd(); IL = os.path.expanduser('~/kres-tmp/2026-11-04-hopf-interlock')
g = {'__file__': os.path.join(IL, 'interlock_rot.py')}; exec(open(os.path.join(IL, 'interlock_rot.py')).read().split("# calibration: Dyskin tetrahedra")[0], g)
d = json.load(open('data/tiling-N20.json'))
B = np.array([(1,1,0),(1,0,1),(0,1,1)], float).T; L = B @ np.array([[10,1,4],[0,2,1],[0,0,1]], float)
V0 = np.array([(0,0,0),(4,4,0),(4,0,4),(0,4,4)], float); S = np.array([V0[i] + (V0[j] - V0[i])/4 for i in range(4) for j in range(4) if i != j])
M = [np.array(m) for m in d['orient_matrices']]
copies = []
for (oi, r) in d['placements']:
    R = M[d['orientations_used'].index(oi)]
    for t in itertools.product(range(-8, 9), repeat=3):
        X = S @ R.T + np.array(r) + L @ np.array(t, float); c = X.mean(0)
        if np.linalg.norm(c) < 22: copies.append(X)
cen = np.array([x.mean(0) for x in copies]); R_ = {}
for nrm in ((0, 0, 1), (1, 1, 1), (1, 1, 0)):
    n = np.array(nrm, float); n /= np.linalg.norm(n)
    h = cen @ n; sel = [i for i in range(len(copies)) if abs(h[i]) < 3.0]
    bodies = [[copies[i]] for i in sel]; kinds = ['S2']*len(sel); cs = cen[sel]
    lat = np.linalg.norm(cs - np.outer(cs @ n, n), axis=1); ids = [i for i in range(len(sel)) if lat[i] < 3.5]
    R_[str(nrm)] = g['run'](f'β-tin slab ⊥ {nrm}', bodies, ids, kinds)
json.dump(R_, open('data/interlock-btin.json', 'w'), indent=1, default=str)
