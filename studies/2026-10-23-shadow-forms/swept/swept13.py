# Does the 84% lattice's gap percolate? Label the gap in a 2x2x2 supercell (periodic): 8 pieces = closed pockets, fewer = linked channels.
import numpy as np, itertools, json
from scipy import ndimage
exec(open('swept1.py').read().split('# period:')[0])
B = np.array(json.load(open('swept-general-more.json'))['general']['basis']); B2 = 2*B
n = 150; g = (np.arange(n) + .5)/n; F = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); X = F @ B2
cov = np.zeros(len(X), bool)
for c in itertools.product(range(-2, 5), repeat=3):
    cov |= inside(X - np.array(c) @ B, ES)
gap = (~cov).reshape(n, n, n); lab, k = ndimage.label(gap)
par = list(range(k + 1))
def f(i):
    while par[i] != i: par[i] = par[par[i]]; i = par[i]
    return i
for ax in range(3):
    a = np.take(lab, 0, axis=ax); b = np.take(lab, n - 1, axis=ax)
    for x, y in zip(a.ravel(), b.ravel()):
        if x and y: par[f(x)] = f(y)
roots = np.array([f(i) for i in range(k + 1)]); lab = roots[lab]
sizes = sorted(((lab == r).sum() for r in np.unique(lab) if r), reverse=True)
real = [s for s in sizes if s >= 4e-4 * n**3]
print(f'2x2x2 supercell: {len(real)} real gap pieces (sizes {real[:10]}), gap fraction {gap.mean():.4f}')
print('=> ' + ('closed pockets, one per cell' if len(real) == 8 else 'the gaps link up across cells: channels' if len(real) < 8 else 'more than one pocket per cell'))
