# Exact checks: (1) Icosaxes = 120-cell vertex-first section at height (phi/2) x tip (atlas120 exact cut); (2) Cube Pearl = 24-cell section
# perpendicular to a corner, at 1/6 of the way to the tip (exact coordinates in Q(sqrt2): the 24-cell corner direction (1,1,0,0)).
import sys, os, json, itertools, numpy as np, sympy as sp
sys.path.insert(0, os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts')); os.chdir(os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts'))
import atlas120 as A
from fractions import Fraction as Fr
def inv(P):
    P = P - P.mean(0); R2 = (P ** 2).sum(1).mean(); return np.sort(((P[:, None] - P[None]) ** 2).sum(-1)[np.triu_indices(len(P), 1)] / R2)
def ds(name):
    w = json.load(open(os.path.expanduser(f'~/work/dataset-v7/solids/{name}.json'))); return np.array([[float(c) for c in v['decimal']] for v in w['vertices']])
lab = 'vertex-first'; d = A.DIRS[lab][0]; hs = sorted(set(A.dot(p, d) for p in A.R), key=float); tip = hs[-1]
h = A.Q5(Fr(1, 4), Fr(1, 4)) * tip            # phi/2 = 1/4 + sqrt5/4
item, keep, _ = A.cut((lab, h, any(x == h for x in hs), tip))
a, b = inv(np.array(keep['fV'], float)), inv(ds('dicto-icosaxes'))
print('Icosaxes vs 120-cell vertex-first at', A.q5str(h), ': corners', len(keep['fV']), 'faces', item.get('face_sizes'), 'mismatch', float(np.max(np.abs(a - b))) if len(a) == len(b) else 'counts differ')
# 24-cell exact
V = [sp.Matrix(s) for p in set(itertools.permutations([1, 1, 0, 0])) for s in set(itertools.product(*[(x, -x) if x else (0,) for x in p]))]
E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if (V[i] - V[j]).dot(V[i] - V[j]) == 2]
dv = sp.Matrix([1, 1, 0, 0]); top = max(v.dot(dv) for v in V); hh = top / 6
pts = []
for i, j in E:
    a_, b_ = V[i].dot(dv) - hh, V[j].dot(dv) - hh
    if a_ * b_ < 0: t = a_ / (a_ - b_); pts.append(V[i] + t * (V[j] - V[i]))
for v in V:
    if v.dot(dv) == hh: pts.append(v)
B = sp.Matrix([[1, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])   # basis of the hyperplane (orthogonal to dv, not normalised: rescale first row)
Q = np.array([[float(x) for x in (B * p)] for p in pts]); Q[:, 0] /= 2 ** .5
from scipy.spatial import ConvexHull
Q = np.unique(np.round(Q, 12), axis=0); Q = Q[ConvexHull(Q).vertices]
a, b = inv(Q), inv(ds('dicto-cube-pearl'))
print('Cube Pearl vs 24-cell corner-first at h = top/6 =', hh, ': corners', len(Q), 'mismatch', float(np.max(np.abs(a - b))) if len(a) == len(b) else 'counts differ')
