import os, sys, math, itertools, numpy as np
from fractions import Fraction as Fr
src = open('scripts/hpiece_congruent.py').read().split("for l in lams:")[0]; lams = []; exec(src)
os.chdir(HEX); pc, _ = T.tile('ABC', 1, Fr(3, 8)); os.chdir(here)
S = [np.unique(np.round(np.array([cart(p) for p in P]), 10), axis=0) for k, up, s_, P, J in pc]
print('c-tile pieces:', len(S), [len(s) for s in S]); r = congruent(S[0], S[1]); print('Echo #0 ≅ #1:', r is not None, 'det', None if r is None else round(np.linalg.det(r[0])))
Q = S[0] - S[0].mean(0)
def same(A, B): return all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-8 for a in A)
mir = []
for n in itertools.product((-1, 0, 1), repeat=3):
    n = np.array(n, float)
    if not n.any(): continue
    n /= np.linalg.norm(n); R = np.eye(3) - 2*np.outer(n, n)
    if same(Q @ R.T, Q): mir.append(np.round(n, 3).tolist())
# general test: any improper isometry fixing the corner set (via congruent of Q with its mirror)
achiral = congruent(Q, Q @ np.diag([1, 1, -1.]).T) is not None
print('Echo mirror planes (axis-aligned/diagonal search):', mir, '| Echo achiral (congruent to its mirror image):', achiral)
