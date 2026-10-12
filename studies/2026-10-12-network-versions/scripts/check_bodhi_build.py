import json, sys, itertools, numpy as np
from scipy.optimize import least_squares
src = open('read_build.py').read().split("ov = [")[0].replace('sys.argv[1]', repr(sys.argv[1]))
exec(src)
from collections import Counter; print('pieces:', Counter(k for k, _ in P))
idx = [i for i, (k, W) in enumerate(P) if k == 'RT']
ref0 = P[idx[0]][1] - P[idx[0]][1].mean(0)
print('all RTs same orientation:', all(all(np.min(np.linalg.norm(ref0 - v, axis=1)) < 1e-6 for v in P[i][1] - P[i][1].mean(0)) for i in idx))
C = np.array([P[i][1].mean(0) for i in idx])
m = least_squares(lambda x: np.linalg.norm(C - x[:3], axis=1) - x[3], np.r_[C.mean(0), 1.6]).x
r = np.linalg.norm(C - m[:3], axis=1); print('distances from the middle:', np.round(r, 6), '(Bodhi: phi = 1.618034)')
d = np.linalg.norm(C[:, None] - C[None], axis=2); touch = (np.abs(d - 1.701302) < 1e-4)
print('face-to-face contacts:', int(touch.sum() // 2), '(Bodhi: 30); per piece', touch.sum(1))
ov = [(i, j, round(overlap(P[i][1], P[j][1]), 4)) for i, j in itertools.combinations(range(len(P)), 2)]
print('overlapping pairs:', [o for o in ov if o[2] > 0])
