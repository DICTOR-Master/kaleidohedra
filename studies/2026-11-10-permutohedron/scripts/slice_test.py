"""Slice test (DICTO 10 Nov: "the space filling non repeating shape we have been trying to build can that be seen too"; "yes queue the slice
test"). The 4D permutohedron honeycomb = the Voronoi cells of the lattice A4* (Z^5 projected onto x1 + ... + x5 = 0). Its slice by a 3D
hyperplane {u·x = c} is the power diagram of the sites' projections with weights -(u·p - c)^2. For directions u turning from a rational one
(a repeating slice) to a golden one (non-repeating), count the cells in a ball and the DISTINCT cell shapes (up to congruence: sorted squared
corner distances, 6 digits). A non-repeating slice with few shapes would be DICTO's aim seen this way. Usage: python slice_test.py [steps]"""
import sys, itertools, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull, cKDTree
from scipy.optimize import linprog
phi = (1 + 5 ** .5) / 2
Q = np.linalg.svd(np.eye(5) - 1 / 5)[0][:, :4]                     # orthonormal basis of the sum-zero hyperplane (columns)
Z = np.array(list(itertools.product(range(-5, 6), repeat=4)), float); Z = np.c_[Z, np.zeros(len(Z))]   # z5 = 0 fixes the shift by (1,...,1)
L = (Z - Z.mean(1, keepdims=True)) @ Q                              # A4* points in 4D coordinates
L = np.unique(np.round(L, 9), axis=0); T = cKDTree(L)
def unit(v): v = np.asarray(v, float); v = v - v.mean(); w = v @ Q; return w / np.linalg.norm(w)
U0, U1 = unit([1, -1, 0, 0, 0]), unit([1, phi, phi ** 2, phi ** 3, phi ** 4])
def slice_shapes(u, c=0.1234567, R=2.4):
    u = u / np.linalg.norm(u); E = np.linalg.svd(np.eye(4) - np.outer(u, u))[0][:, :3]    # basis of the slice
    h = L @ u - c; P3 = L @ E; keep = np.where(np.abs(h) < 2.0)[0]                       # only sites near the slice can own a piece
    P3k, hk = P3[keep], h[keep]; w = -hk ** 2; tree = cKDTree(P3k); sigs = set(); cnt = 0
    for i in np.where(np.linalg.norm(P3k, axis=1) < R)[0]:
        nb = [j for j in tree.query_ball_point(P3k[i], 3.2) if j != i]
        A = np.array([2 * (P3k[j] - P3k[i]) for j in nb]); b = np.array([(P3k[j] @ P3k[j] + hk[j] ** 2) - (P3k[i] @ P3k[i] + hk[i] ** 2) for j in nb])
        nr = np.linalg.norm(A, axis=1); r = linprog(np.r_[0, 0, 0, -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
        if r.status != 0 or r.x[-1] < 1e-7: continue                                          # this site has no piece in the slice
        hs = HalfspaceIntersection(np.c_[A, -b], r.x[:3]); V = np.unique(np.round(hs.intersections, 8), axis=0)
        D2 = np.sort(np.round(((V[:, None] - V[None]) ** 2).sum(-1)[np.triu_indices(len(V), 1)], 5)); sigs.add((len(V), tuple(D2))); cnt += 1
    return cnt, len(sigs)
steps = int(sys.argv[1]) if len(sys.argv) > 1 else 10
import os
RADII = tuple(float(x) for x in os.environ.get('RADII', '2.4,3.4').split(','))
print(f'START slice test: {steps + 1} directions from rational [1,-1,0,0,0] to golden [1, φ, φ², φ³, φ⁴]; balls {RADII}', flush=True)
res = []
TS = [float(x) for x in os.environ['TS'].split(',')] if os.environ.get('TS') else [k / steps for k in range(steps + 1)]
for k, t in enumerate(TS):
    u = (1 - t) * U0 + t * U1; row = []
    for R in RADII:
        cells, shapes = slice_shapes(u, R=R); row.append((cells, shapes))
    res.append(row)
    print(f'PROGRESS {(k + 1) / len(TS):.2f} t = {t:.2f}: ' + '  '.join(f'R {R}: {c} cells / {sh} shapes' for R, (c, sh) in zip(RADII, row)), flush=True)
print('FINAL ok' if all(c > 0 for row in res for c, _ in row) else 'FINAL FAIL: an empty slice')
