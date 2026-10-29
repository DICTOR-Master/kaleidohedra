# Spiked football golden cycle: the four stations side by side, drawn to scale: football (gold), spiked football (gold core,
# violet pentagonal and teal hexagonal spikes), the pentakis hull of the tips (translucent), and the football phi times larger.
import json, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
GOLD, VIOLET, TEAL, BG, PALE = '#d4af37', '#8e5bd6', '#2bb3a3', '#0d0d12', '#e8e2cc'
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def faces(Q):
    h = ConvexHull(Q); out = {}
    for eq in h.equations:
        k = tuple(np.round(eq, 7))
        if k not in out:
            ids = [i for i, p in enumerate(Q) if abs(eq[:3] @ p + eq[3]) < 1e-8]; R = Q[ids]; c = R.mean(0); n = eq[:3]
            a = R[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a); out[k] = R[np.argsort(np.arctan2((R - c) @ b, (R - c) @ a))]
    return list(out.values())
FT = faces(P); tips = [phi * f.mean(0) for f in FT]
def draw(ax, polys, cols, alpha=0.92, title=''):
    for Q, c in zip(polys, cols): ax.add_collection3d(Poly3DCollection([Q], facecolor=c, edgecolor='#f5f0dc', linewidths=0.25, alpha=alpha))
    r = 1.95 * phi
    for s in 'xyz': getattr(ax, f'set_{s}lim')(-r / 1.6, r / 1.6)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(16, 28); ax.set_title(title, color=PALE, fontsize=9)
fig = plt.figure(figsize=(14, 4.2), facecolor=BG)
ax = fig.add_subplot(1, 4, 1, projection='3d'); draw(ax, FT, [GOLD] * len(FT), title='football (TI)')
sp, sc = [], []
for f, t in zip(FT, tips):
    for i in range(len(f)): sp.append(np.array([f[i], f[(i + 1) % len(f)], t])); sc.append(VIOLET if len(f) == 5 else TEAL)
ax = fig.add_subplot(1, 4, 2, projection='3d'); draw(ax, sp, sc, title='spiked football = φ · TI')
ax = fig.add_subplot(1, 4, 3, projection='3d'); HF = faces(np.array(tips)); draw(ax, sp + HF, sc + ['#f5f0dc'] * len(HF), title='pentakis hull of the 32 tips')
for c in ax.collections[len(sp):]: c.set_alpha(0.18)
ax = fig.add_subplot(1, 4, 4, projection='3d'); F2 = faces(P * phi); draw(ax, F2, [GOLD] * len(F2), alpha=0.35, title='football × φ: the turn closes')
fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')
fig.savefig('figures/spiked-golden-cycle.png', dpi=170, facecolor=BG, bbox_inches='tight'); print('ok')
