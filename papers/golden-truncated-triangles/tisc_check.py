# Exact: is the TI Star core the 120-cell's cell-first section at height 3(sqrt5 - 2) x tip? (atlas120 exact cut; scale-free comparison)
import sys, os, json, numpy as np
sys.path.insert(0, os.path.expanduser('~/kres-tmp/studies/2026-10-27-white-queen-polar/scripts'))
os.chdir(os.path.expanduser('~/kres-tmp/studies/2026-10-27-white-queen-polar/scripts'))
import atlas120 as A
from fractions import Fraction as Fr
lab = 'cell-first'; d = A.DIRS[lab][0]; hs = sorted(set(A.dot(p, d) for p in A.R), key=float); tip = hs[-1]
k = A.Q5(Fr(-6), Fr(3)) if hasattr(A, 'Q5') else None   # 3*sqrt5 - 6
h = k * tip
print('height', A.q5str(h), float(h), 'tip', A.q5str(tip))
item, keep, _ = A.cut((lab, h, any(x == h for x in hs), tip))
P = np.array(keep['fV'], float); P -= P.mean(0)
def inv(P):
    R2 = (P ** 2).sum(1).mean(); return np.sort(((P[:, None] - P[None]) ** 2).sum(-1)[np.triu_indices(len(P), 1)] / R2)
w = json.load(open(os.path.expanduser('~/kres-tmp/dataset-v7/solids/dicto-ti-star-core.json')))
W = np.array([[float(c) for c in v['decimal']] for v in w['vertices']]); W -= W.mean(0)
a, b = inv(P), inv(W)
print('corners', len(P), len(W), 'faces', item.get('face_sizes'), 'max scale-free mismatch', float(np.max(np.abs(a - b))) if len(a) == len(b) else 'different counts')
print('edge lengths^2 exact', item.get('edge_len2_exact'), item.get('edge_len_count'))
