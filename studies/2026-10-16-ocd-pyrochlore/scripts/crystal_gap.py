# The gap of the pyrochlore two-solid crystal (stella cuts on network 1, the OCD's hexagon icosahedra on network 2): voxels over one periodic
# fcc cell; connected pieces, their volumes and convexity. Float. -> data/crystal-gap.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
N = json.load(open('data/network.json')); T = np.array(N['T']); Lb = np.array(N['Lb']).T
R = json.load(open('data/crystal-render.json')); S = np.array(R['stella']['v']); I = np.array(R['ico']['v'])
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
PS, PI = planes(S), planes(I)
n = 112; g = (np.arange(n) + 0.5) / n
Fr = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); X = Fr @ Lb.T
inside = np.zeros(len(X), bool)
for m in itertools.product((-1, 0, 1, 2), repeat=3):
    a = Lb @ np.array(m, float)
    for c, P in ((a, PS), (a + T[0], PS), (a + 2 * T[0], PI), (a + 3 * T[0], PI)):
        Y = X - c; inside |= np.all(Y @ P[:, :3].T + P[:, 3] <= 1e-9, axis=1)
gap = (~inside).reshape(n, n, n); lab, k = ndimage.label(gap)
par = list(range(k + 1))
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for ax in range(3):
    for x, y in zip(np.take(lab, 0, axis=ax).ravel(), np.take(lab, n - 1, axis=ax).ravel()):
        if x and y: par[find(x)] = find(y)
roots = {}
L = lab.reshape(-1)
for i in range(1, k + 1): roots.setdefault(find(i), []).append(i)
vox = abs(np.linalg.det(Lb)) / n ** 3
out = ['DICTO · dictospheres.com', 'Gap of the pyrochlore two-solid crystal (float, voxels)', f'  filled {inside.mean():.4f}; gap {1 - inside.mean():.4f}']
big = []
for r, ids in roots.items():
    sel = np.isin(L, ids); cnt = sel.sum()
    if cnt < 300: continue
    f = Fr[sel]; f0 = f[0]; f = f - np.round(f - f0); pts = f @ Lb.T
    h = ConvexHull(pts); big.append((cnt * vox, h.volume, pts.mean(0)))
big.sort(key=lambda b: -b[0])
out.append(f'  gap pieces per cell (> 300 voxels): {len(big)}; total {sum(b[0] for b in big):.4f} of cell {abs(np.linalg.det(Lb)):.4f}')
for v, hv, c in big[:12]: out.append(f'    volume {v:.5f}, hull {hv:.5f}, convex share {v / hv:.3f}')
print('\n'.join(out)); open('data/crystal-gap.txt', 'w').write('\n'.join(out) + '\n')
