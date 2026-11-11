#!/usr/bin/env python3
"""Harmonic fingerprint (#94 method, methods.Q3d / W6) of the HexOct tiles along the λ walk (Concordance 6.1, HexOct row, harmonic columns).
Point set = the tile's corners (union of its 4 pieces, deduplicated), centre = the tile's ball. Scan λ, report sign changes of Q-like signed quantities
(use the m = 0 coefficient q_l0 about the stacking axis, real for these 3-fold symmetric sets, so zeros are sign changes) and Q4, Q6 minima."""
import os, sys, math, json, numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, 'scripts/_lib') if os.path.isdir('scripts/_lib') else None
sys.path.insert(0, os.path.expanduser('~/study-runs/2026-11-04-tetra-sweep/scripts/_lib')); sys.path.insert(0, os.path.expanduser('~/study-runs/2026-11-04-dehn-screen/scripts/_lib')); import methods as M
from scipy.special import sph_harm_y
HEX = os.path.expanduser('~/work/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as T
os.chdir(here); H = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*H])
def pts(word, L, lam):
    os.chdir(HEX); pieces, tz = T.tile(word, L, lam); os.chdir(here)
    X = np.unique(np.round(np.vstack([np.array([cart(p) for p in P]) for k, up, s_, P, J in pieces]), 9), axis=0)
    return X, cart((0, 0, L)) if True else None
def q0(P, l, c):
    u = P - c; u = u/np.linalg.norm(u, axis=1)[:, None]; th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0])
    return float(sph_harm_y(l, 0, th, ph).mean().real)
lams = [Fr(-7, 16) + Fr(i, 400)*(Fr(3, 8) + Fr(7, 16)) for i in range(1, 400)]
out = {}
for word, L, nm in (('ABC', 1, 'c-tile'), ('AB', 0, 'h-tile')):
    rows = []
    for lam in lams:
        try: X, _ = pts(word, L, lam)
        except Exception: continue
        c = X.mean(0); X = X[np.linalg.norm(X - c, axis=1) > 1e-9]
        rows.append((float(lam), q0(X, 4, c), q0(X, 6, c), M.Q3d(X, 4, centre=c), M.Q3d(X, 6, centre=c)))
    sc = {}
    for idx, nmq in ((1, 'q40'), (2, 'q60')):
        sc[nmq] = [round((a[0] + b[0])/2, 4) for a, b in zip(rows, rows[1:]) if a[idx]*b[idx] < 0]
    m4 = min(rows, key=lambda r: r[3]); m6 = min(rows, key=lambda r: r[4])
    out[nm] = {'n': len(rows), 'sign_changes': sc, 'Q4_min': (m4[0], m4[3]), 'Q6_min': (m6[0], m6[4])}
    print(nm, json.dumps(out[nm]), flush=True)
json.dump(out, open('data/hexoct-harmonic.json', 'w'), indent=1)
