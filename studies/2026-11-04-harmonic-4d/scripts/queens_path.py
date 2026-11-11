#!/usr/bin/env python3
"""Harmonic fingerprint (4D, methods.Q4d) of the Red Queen (120-cell) and of the path between the Queens: S(mu) = P ∩ mu P*,
P = 600-cell (circumradius 1), P* = {y : y·v <= 1 for the 120 corners v} (a 120-cell), mu from r_P^2 (S = mu P*) to 1 (S = P).
H4 symmetry silences degrees 1..11 everywhere; the readings are Q12 and Q20. compute-host."""
import os, sys, json, itertools, math
sys.path.insert(0, os.path.expanduser('~/work/_lib')); import methods as M
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = M.PHI
tess = np.array(list(itertools.product((1, -1), repeat=4)), float)
V = np.unique(np.round(np.vstack([tess/2, M.perms((1, 0, 0, 0)), M.even_perms((phi/2, .5, 1/(2*phi), 0))]), 12), axis=0)
h = ConvexHull(V); F = np.unique(np.round(h.equations, 9), axis=0)          # facets n·x + d <= 0
rP = float(np.min(-F[:, 4])); C120 = F[:, :4] / (-F[:, 4:5])                 # 120-cell corners = polar of the facets
C120 = np.unique(np.round(C120, 9), axis=0)
print('600-cell facets', len(F), 'inradius', round(rP, 6), '| 120-cell corners', len(C120))
print('120-cell degrees 2..12:', [round(M.Q4d(C120, l), 4) for l in range(2, 13)], ' Q20 %.4f' % M.Q4d(C120, 20))
print('600-cell Q12 %.4f Q20 %.4f' % (M.Q4d(V, 12), M.Q4d(V, 20)))
H = np.vstack([F, np.hstack([V, -np.ones((len(V), 1))])])
def S(mu):
    Hm = H.copy(); Hm[len(F):, 4] = -mu
    return np.unique(np.round(HalfspaceIntersection(Hm, np.zeros(4)).intersections, 5), axis=0)
mus = np.linspace(rP**2 + 1e-4, 1 - 1e-4, 161); rows = []
for mu in mus:
    P = S(mu); rows.append((float(mu), len(P), M.Q4d(P, 12), M.Q4d(P, 20)))
R = np.array(rows)
for k, l in ((2, 12), (3, 20)):
    q = R[:, k]; z = [(round(R[i, 0], 5), int(R[i, 1]), round(q[i], 4)) for i in range(1, len(q)-1) if q[i] <= q[i-1] and q[i] <= q[i+1] and q[i] < 0.02]
    print(f'path: Q{l} near-zeros (mu, corners, Q):', z)
print('corner counts along the path:', sorted(set(int(r[1]) for r in rows)))
json.dump({'rP': rP, 'rows': rows}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'queens-path.json'), 'w'))
