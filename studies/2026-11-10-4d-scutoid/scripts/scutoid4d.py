"""A 4D scutoid (DICTO 10 Nov: "a 4th dimensional scutoid?!"). The power cell of one hole, stacked over the slider λ, is the convex 4D
polytope {(x, λ): n_k·x <= b_k0 + b_k1·λ, λa <= λ <= λb} (linear in x and λ). Its 3D slices are the power cells; across a wall they change
neighbours (the flip). Here: word AC, s = 1/5, an octahedral hole, λ from -19/120 to -1/40 (across the wall -5s/8 = -1/8, where the
octahedral contact across a layer flips to a tetrahedral one). Output: 4D vertex/facet counts, the facets (which neighbour each belongs
to, and whether it spans the whole λ range or starts/ends inside), the 3D slice at three λ, and data for a render."""
import sys, os, json, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
def inner(A):
    """Chebyshev centre of {x: A[:, :-1] x + A[:, -1] <= 0} (max ball); None if empty"""
    M = A[:, :-1]; b = -A[:, -1]; nr = np.linalg.norm(M, axis=1)
    r = linprog(np.r_[np.zeros(M.shape[1]), -1], A_ub=np.c_[M, nr], b_ub=b, bounds=[(None, None)] * M.shape[1] + [(0, None)], method='highs')
    return (r.x[:-1], r.x[-1]) if r.status == 0 and r.x[-1] > 1e-7 else (None, 0)
sys.path.insert(0, os.path.expanduser('~/work/b1-walls/swap')); sys.path.insert(0, os.path.expanduser('~/work/st57/scripts')); sys.path.insert(0, os.path.expanduser('~/work/splash'))
from validate import Net, Cell, net_for, ROLE_OF
WORDS = ['ABC', 'AC', 'ACBC', 'ACABC', 'ACBCAC', 'ACBABC']; s, la, lb, wall = Fr(1, 5), Fr(-19, 120), Fr(-1, 40), Fr(-1, 8)
def cell4d(word, i):
    spec = net_for(word, s); net = Net(word, spec['G'], spec['T'], spec['motif'], spec['w']); n = len(word)
    c = Cell(net, i, (wall,), Fr(12)); H = c.H
    if c.empty: return None
    L = np.linalg.cholesky(np.array(spec['G'], float)).T; Li = np.linalg.inv(L)
    rows, labels = [], []
    for k, h in enumerate(H):
        nl = np.array([float(x) for x in h['n']]); b0, b1 = float(h['b'][0]), float(h['b'][1])
        rows.append(np.r_[Li.T @ nl, -b1, -b0]); labels.append((ROLE_OF[h['j'] % 3], round((float(h['c'][2]) - float(net.motif[i][1][2])) * n)))
    rows.append(np.r_[0, 0, 0, 1, -float(lb)]); labels.append(('λ top', 0)); rows.append(np.r_[0, 0, 0, -1, float(la)]); labels.append(('λ bottom', 0))
    A = np.array(rows); c0, rad = inner(A)
    if c0 is None: return None
    hs = HalfspaceIntersection(A, c0); V = np.unique(np.round(hs.intersections, 9), axis=0); hull = ConvexHull(V); used = {}
    An = A[:, :4] / np.linalg.norm(A[:, :4], axis=1)[:, None]
    for simp, eq in zip(hull.simplices, hull.equations):
        k = int(np.argmin(np.linalg.norm(An - eq[:4], axis=1))); used.setdefault(k, set()).update(simp)
    return A, c0, V, used, labels
found = []
for word in WORDS:
    for i in range(3 * len(word)):
        R = cell4d(word, i)
        if R is None: continue
        A, c0, V, used, labels = R; lam = V[:, 3]
        part = [(labels[k], round(lam[sorted(v)].min(), 4), round(lam[sorted(v)].max(), 4)) for k, v in used.items()
                if labels[k][0][0] != 'λ' and not (lam[sorted(v)].min() < float(la) + 1e-9 and lam[sorted(v)].max() > float(lb) - 1e-9)]
        if part: found.append((word, i, ROLE_OF[i % 3], len(V), len(used), part))
print(f'holes whose 4D cell has facets that begin or end inside the λ range: {len(found)}')
for f in found[:12]: print('  ', f[:5], f[5])
word, i = found[0][0], found[0][1]
A, c0, V, used, labels = cell4d(word, i)
lam = V[:, 3]
for k in sorted(used, key=lambda k: labels[k]):
    vs = sorted(used[k]); lo, hi = lam[vs].min(), lam[vs].max()
    span = 'whole range' if lo < float(la) + 1e-9 and hi > float(lb) - 1e-9 else f'λ {lo:+.4f} … {hi:+.4f}'
    print(f'  facet: neighbour {labels[k][0]:>8} layer {labels[k][1]:+d}: {len(vs)} corners, {span}')
def slice3(lv):
    A3 = A.copy(); A3[:, 4] = A[:, 4] + A[:, 3] * lv; A3 = A3[:-2][:, [0, 1, 2, 4]]
    p3, _ = inner(A3)
    if p3 is None: return np.zeros((0, 3)), 0
    h3 = HalfspaceIntersection(A3, p3); W = np.unique(np.round(h3.intersections, 9), axis=0); hh = ConvexHull(W)
    nf = len({tuple(np.round(e, 6)) for e in hh.equations}); return W, nf
out = {}
for lv, name in ((float(la) + 1e-4, 'just above -(4-s)/24'), (float(wall) - 0.01, 'just below the wall -5s/8'), (float(wall), 'at the wall -5s/8'), (float(wall) + 0.01, 'just above the wall'), (float(lb) - 1e-4, 'just below -s/8')):
    W, nf = slice3(lv); out[name] = W.tolist()
    nb = []
    A3 = A.copy(); A3[:, 4] = A[:, 4] + A[:, 3] * lv
    for k in range(len(A) - 2):
        if len(W) and np.sum(np.abs(W @ A3[k, :3] + A3[k, 4]) < 1e-7) >= 3: nb.append(labels[k])
    print('     neighbours sharing a face:', sorted(set(nb)), flush=True); print(f'  3D slice {name} (λ = {lv:+.4f}): {len(W)} corners, {nf} faces')
json.dump({'V4': V.tolist(), 'slices': out}, open('scutoid4d.json', 'w'))
print('FINAL ok' if found else 'FINAL FAIL: no hole changes neighbours across the wall')
