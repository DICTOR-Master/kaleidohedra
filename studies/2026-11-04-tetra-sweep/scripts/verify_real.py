#!/usr/bin/env python3
"""Uniform construction for real cuts (α, β, γ, 0), Σ = 1, at corners V0..V2 of T = conv{0, b1, b2, b3} (b1 = (1,1,0), b2 = (1,0,1), b3 = (0,1,1)):
tiles P and σ_z(P) + w, lattice L = B·diag(1−α, 1−β, 1−γ). Integer data: w ∈ {0, b1/n}. Here w = s·b1 scanned over s ∈ [0, 1) (the b1 direction mod L... plus
the two found values), and each candidate checked with real polytopes: no overlaps among copies near the origin, coverage of random points exactly once.
Calibration: integer cuts (2,1,0,0)/3 and (1,1,1,0)/3 (known tilers) must pass at their found w; a wrong w must fail."""
import sys, json, itertools, math, numpy as np
sys.path.insert(0, 'scripts/_lib'); import methods as Mt
from scipy.spatial import ConvexHull, Delaunay
phi = (1 + 5**.5)/2
B = np.array([(1,1,0),(1,0,1),(0,1,1)], float).T; V = np.array([(0,0,0),(1,1,0),(1,0,1),(0,1,1)], float)
def piece(c):
    pts = [V[i] + c[i]*(V[j] - V[i]) for i in range(4) for j in range(4) if i != j]
    P = np.unique(np.round(pts, 12), axis=0); return P[ConvexHull(P).vertices]
SZ = np.diag([1., 1., -1.])
def check(c, w):
    P = piece(c); Q = P @ SZ.T + w; L = B @ np.diag([1 - c[0], 1 - c[1], 1 - c[2]])
    vol_ok = abs(2*ConvexHull(P).volume - abs(np.linalg.det(L))) < 1e-9
    cop = []
    for t in itertools.product(range(-6, 7), repeat=3):
        s = L @ np.array(t, float)
        for X in (P, Q):
            Y = X + s
            if np.linalg.norm(Y.mean(0)) < 3.2: cop.append(Y)
    cen = [y.mean(0) for y in cop]; ov = 0; pairs = 0
    for i, j in itertools.combinations(range(len(cop)), 2):
        if np.linalg.norm(cen[i] - cen[j]) > 2.5: continue
        pairs += 1
        if Mt.overlap(cop[i], cop[j]): ov += 1
    rng = np.random.default_rng(0); X = rng.uniform(-0.6, 0.6, (4000, 3)); cnt = np.zeros(len(X), int)
    for y in cop: cnt += Delaunay(y).find_simplex(X) >= 0
    return vol_ok, ov, pairs, {int(k): int(v) for k, v in zip(*np.unique(cnt, return_counts=True))}
cases = {'cal (2,1,0,0)/3 w=0': ([2/3, 1/3, 0, 0], [0, 0, 0]), 'cal (1,1,1,0)/3 w=b1/3': ([1/3]*3 + [0], [1/3, 1/3, 0]),
         'cal WRONG (1,1,1,0)/3 w=0': ([1/3]*3 + [0], [0, 0, 0]),
         'golden (φ^-1, φ^-2, 0, 0) w=0': ([1/phi, 1/phi**2, 0, 0], [0, 0, 0])}
for nm, (c, w) in cases.items():
    r = check(c, np.array(w, float)); print(nm, '| vol', r[0], '| overlaps', r[1], 'of', r[2], '| coverage', r[3], flush=True)
# 3-cut golden: scan w = s·b1
for c in ([1/phi**2, 1/phi**2, 1/phi**3, 0], [1/phi, 1/phi**3, 1/phi**4, 0]):
    best = []
    for s in np.linspace(0, 1, 41):
        r = check(c, s*np.array([1, 1, 0.])); best.append((r[1], s, r[3]))
    best.sort(); print('golden', [round(x, 4) for x in c], 'best s:', [(round(s, 3), o, cov) for o, s, cov in best[:3]], flush=True)
