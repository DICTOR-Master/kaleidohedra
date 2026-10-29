# TI Pyramids figure: left, TI cut from its centre into 12 pentagonal (gold) and 20 hexagonal (violet) pyramids,
# drawn apart; right, the hexagonal bipyramid: TI's hexagonal pyramid (violet) on the truncated tetrahedron's (teal).
# Run on dicto-big-brother: ~/geom/bin/python scripts/figure.py
import itertools, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
GOLD, VIOLET, TEAL, BG = '#d4af37', '#8e5bd6', '#2bb3a3', '#0d0d12'
phi = (1 + 5 ** .5) / 2
P = set()
for b in [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)]:
    for q in [(b[0], b[1], b[2]), (b[1], b[2], b[0]), (b[2], b[0], b[1])]:
        for s in itertools.product([1, -1], repeat=3): P.add(tuple(np.round(np.array(q) * s, 9)))
P = np.array(sorted(P)) / 2
h = ConvexHull(P); F = {}
for sm, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
def ordered(ids, V):
    Q = V[list(ids)]; c = Q.mean(0); n = c / np.linalg.norm(c); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
    return Q[np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]
fig = plt.figure(figsize=(10, 5), facecolor=BG)
ax = fig.add_subplot(1, 2, 1, projection='3d')
for ids in F.values():
    B = ordered(ids, P); c = B.mean(0); d = 0.9 * c / np.linalg.norm(c)
    polys = [B + d] + [np.array([np.zeros(3), B[i], B[(i + 1) % len(B)]]) + d for i in range(len(B))]
    ax.add_collection3d(Poly3DCollection(polys, facecolor=GOLD if len(B) == 5 else VIOLET, edgecolor='#f5f0dc', linewidths=0.3, alpha=0.9))
r = 3.1
for s in 'xyz': getattr(ax, f'set_{s}lim')(-r, r)
ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(18, 30)
ax.set_title('TI from its centre:\n12 pentagonal (gold) + 20 hexagonal (violet) pyramids', color='#e8e2cc', fontsize=9)
# hexagonal bipyramid
ax = fig.add_subplot(1, 2, 2, projection='3d')
H = np.array([[np.cos(k * np.pi / 3), np.sin(k * np.pi / 3), 0] for k in range(6)])
hF, hT = (18 * 5 ** .5 + 42) ** .5 / 4, 6 ** .5 / 4
for apex, col in [(np.array([0, 0, hF]), VIOLET), (np.array([0, 0, -hT]), TEAL)]:
    ax.add_collection3d(Poly3DCollection([np.array([apex, H[i], H[(i + 1) % 6]]) for i in range(6)], facecolor=col, edgecolor='#f5f0dc', linewidths=0.8, alpha=0.85))
for s in 'xy': getattr(ax, f'set_{s}lim')(-1.5, 1.5)
ax.set_zlim(-1.1, 1.9 + 0.4); ax.set_box_aspect((3, 3, 3.4)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(12, 25)
ax.set_title('hexagonal bipyramid: TI\'s hexagonal pyramid\non the truncated tetrahedron\'s (teal)', color='#e8e2cc', fontsize=9)
fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')
fig.savefig('figures/ti-pyramids.png', dpi=200, facecolor=BG, bbox_inches='tight'); print('ok')
