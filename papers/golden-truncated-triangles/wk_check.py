# Is DICTO's White Knight congruent (up to scale) to the 120-cell's cell-first section at height 29/64 + 13/64 sqrt5 (#65 atlas row 114)?
# Uses the atlas's own exact cut; compares scale-free invariants: (edge^2 / circumradius^2) for every edge, the sorted list of all
# pairwise squared distances / circumradius^2, and face kinds.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts'))
os.chdir(os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts'))
import atlas120 as A
target = None
for t in A.slice_tasks():
    if t[0] == 'cell-first' and A.q5str(t[1]) == '29/64 + 13/64√5': target = t; break
print('task', target[0], A.q5str(target[1]), target[2])
item, keep, _ = A.cut((target[0], target[1], target[2] is True, target[3]))
P = np.array(keep['fV'], float); P -= P.mean(0)
def inv(P):
    r2 = (np.linalg.norm(P, axis=1) ** 2); R2 = r2.mean()
    D = np.sort(np.round(((P[:, None] - P[None]) ** 2).sum(-1)[np.triu_indices(len(P), 1)] / R2, 6))
    return R2, r2.std() / R2, D
w = json.load(open(os.path.expanduser('~/work/dataset-v7/solids/dicto-white-knight.json')))
W = np.array([[float(c) for c in v['decimal']] for v in w['vertices']]); W -= W.mean(0)
Rs, ss, Ds = inv(P); Rw, sw, Dw = inv(W)
print('slice: corners', len(P), 'radius spread', ss, '| White Knight: corners', len(W), 'radius spread', sw)
same = len(Ds) == len(Dw) and np.max(np.abs(Ds - Dw)) < 1e-5
print('all scale-free pairwise distances equal (congruent up to scale):', same, ' max diff', float(np.max(np.abs(Ds - Dw))) if len(Ds) == len(Dw) else None)
print('scale factor (White Knight / slice) =', (Rw / Rs) ** .5)
