#!/usr/bin/env python3
"""Harmonic fingerprint (#94 method, methods.Q3d / W6, calibrated) of the golden Dehn-zero truncated tetrahedra and the references:
uniform 1/4 cut (the β-tin tiler), Archimedean 1/3, plain tetrahedron, octahedron (cuts 1/2 at all four corners)."""
import sys, json, itertools, numpy as np
sys.path.insert(0, 'scripts/_lib'); import methods as M
from scipy.spatial import ConvexHull
phi = (1 + 5**.5)/2
V = np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)], float)
def solid(c):
    pts = []
    for i in range(4):
        for j in range(4):
            if i != j: pts.append(V[i] + c[i]*(V[j] - V[i]))
    P = np.unique(np.round(pts, 12), axis=0); h = ConvexHull(P); return P[h.vertices]
G = json.load(open('data/golden-cuts.json'))
shapes = {'uniform 1/4 (tiler)': [.25]*4, 'Archimedean 1/3': [1/3]*4, 'octahedron': [.5]*4, 'tetrahedron': [1e-9]*4}
for g in G: shapes['golden ' + ','.join(g['cuts'])] = [phi**-j if j else 1e-9 for j in g['cuts_phi_powers']]
out = {}
for name, c in shapes.items():
    P = solid(c); cen = P.mean(0)
    q = {l: float(M.Q3d(P, l, centre=cen)) for l in (3, 4, 6, 8)}
    out[name] = {'corners': len(P), 'Q': q, 'W6': float(M.W6(P, centre=cen))}
    print(f"{name:32s} corners {len(P):2d}  " + '  '.join(f"Q{l}={v:.4f}" for l, v in q.items()) + f"  W6={out[name]['W6']:.4f}")
json.dump(out, open('data/golden-harmonic.json', 'w'), indent=1)
