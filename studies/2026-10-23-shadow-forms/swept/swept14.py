# Picture of the 84% lattice's gap channels: gap voxels of a 2x2x2 block of cells, coloured by depth, beside one swept piece for scale.
import numpy as np, itertools, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
exec(open('swept1.py').read().split('# period:')[0])
B = np.array(json.load(open('swept-general-more.json'))['general']['basis']); B2 = 2*B
n = 90; g = (np.arange(n) + .5)/n; F = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); X = F @ B2
cov = np.zeros(len(X), bool)
for c in itertools.product(range(-2, 5), repeat=3): cov |= inside(X - np.array(c) @ B, ES)
G = X[~cov]; G = G[np.random.default_rng(1).random(len(G)) < .35]
fig = plt.figure(figsize=(16, 8), dpi=110)
for k, (el, az) in enumerate([(20, 30), (60, 120)]):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d')
    ax.scatter(G[:, 0], G[:, 1], G[:, 2], s=1.2, c=G @ np.array([.3, .5, .8]), cmap='plasma', alpha=.55, linewidths=0)
    S = np.vstack([D, D + sweep]); h = ConvexHull(S); off = (B2.sum(0)) / 2 - S.mean(0)
    ax.add_collection3d(Poly3DCollection([S[s] + off + np.array([0, 0, 0]) * 0 + (B2.sum(0) * .9) for s in h.simplices], facecolor=(.85, .7, .3, .25), edgecolor=(.5, .4, .2, .15)))
    ax.view_init(el, az); ax.set_box_aspect((1, 1, 1)); ax.set_axis_off()
    ax.set_title(['the gap channels of 2×2×2 cells (84.2% filled)', 'another view'][k], fontsize=13)
fig.text(.5, .03, 'Swept dodecahedra, best general lattice: 15.8% of space is one connected network of channels (no closed pockets). Gold: one swept piece for scale.   DICTO', ha='center', fontsize=11, color='0.3')
plt.savefig('swept-gap-channels-84.png', bbox_inches='tight'); print('saved')
