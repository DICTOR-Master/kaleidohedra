# Bodhi gap: split each pocket (inner, outer) by nearest symmetry axis (12 five-fold, 20 three-fold, 30 two-fold rays) and report
# each part's volume and convexity (part / its hull), to see whether natural pieces exist.
import os, numpy as np
from scipy import ndimage
from scipy.spatial import ConvexHull
p = os.path.expanduser('~/netv/bodhi_gap.py'); src = open(p).read()
exec(src[:src.index('R = np.linalg.norm(outer')].replace('__file__', repr(p)))
R = np.linalg.norm(outer, axis=1).max(); n = 220; g = np.linspace(-R, R, n); h = g[1] - g[0]
X = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
m = np.all(X @ FO[:, :3].T + FO[:, 3] < 0, axis=1)
for E in SE: m &= ~np.all(X @ E[:, :3].T + E[:, 3] <= 0, axis=1)
lab, k = ndimage.label(m.reshape(n, n, n)); L = lab.reshape(-1)
sizes = np.bincount(L)[1:]; big = np.argsort(sizes)[::-1][:2] + 1
U = {'5': U5, '3': ref['D'] / np.linalg.norm(ref['D'], axis=1)[:, None], '2': ref['ID'] / np.linalg.norm(ref['ID'], axis=1)[:, None]}
A = np.vstack(list(U.values())); cls = np.array(['5'] * 12 + ['3'] * 20 + ['2'] * 30)
for b in big:
    Q = X[L == b]; name = 'inner' if np.linalg.norm(Q, axis=1).mean() < 2.5 else 'outer'
    near = np.argmax((Q / np.linalg.norm(Q, axis=1)[:, None]) @ A.T, axis=1)
    print(f'{name} pocket volume {len(Q) * h ** 3:.3f}')
    for c in '532':
        ids = np.where(cls == c)[0]; parts = [Q[near == i] for i in ids]
        vs = [len(q) * h ** 3 for q in parts]; conv = [len(q) * h ** 3 / ConvexHull(q).volume if len(q) > 10 else 0 for q in parts]
        comps = [ndimage.label(np.isin(np.arange(len(Q)), np.where(near == i)[0]))[1] for i in ids[:1]]
        print(f'   {c}-fold: {len(ids)} parts, each ~{np.mean(vs):.3f} (spread {np.ptp(vs):.3f}), fill of own hull {np.mean(conv):.2f}')
