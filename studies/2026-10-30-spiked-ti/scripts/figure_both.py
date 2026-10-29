# TI Star: both cycles, one turn each, drawn to scale within each row. Top: the Double TI Star (s = 2, mirrored pyramids);
# bottom: the Golden TI Star (s = phi). Each row: TI (gold), the TI Star (pentagonal spikes violet, hexagonal teal), the
# pentakis hull of the 32 tips (translucent), and s.TI, whose face centres are the tips (translucent gold), where the next turn begins.
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
FT = faces(P)
fig = plt.figure(figsize=(14, 7.6), facecolor=BG)
for row, (s, name) in enumerate([(2.0, 'Double TI Star (× 2)'), (phi, 'Golden TI Star (× φ)')]):
    tips = [s * f.mean(0) for f in FT]; R = 1.6 * s
    def draw(k, polys, cols, alpha=0.92, title='', faint=0):
        ax = fig.add_subplot(2, 4, 4 * row + k, projection='3d')
        for i, (Q, c) in enumerate(zip(polys, cols)):
            ax.add_collection3d(Poly3DCollection([Q], facecolor=c, edgecolor='#f5f0dc', linewidths=0.25, alpha=(0.18 if i >= len(polys) - faint else alpha)))
        for a in 'xyz': getattr(ax, f'set_{a}lim')(-R, R)
        ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(16, 28); ax.set_title(title, color=PALE, fontsize=9)
    sp, sc = [], []
    for f, t in zip(FT, tips):
        for i in range(len(f)): sp.append(np.array([f[i], f[(i + 1) % len(f)], t])); sc.append(VIOLET if len(f) == 5 else TEAL)
    HF = faces(np.array(tips)); OF = faces(P * s)
    vol = '2' if s == 2 else 'φ'; turn = '8' if s == 2 else 'φ³'
    draw(1, FT, [GOLD] * len(FT), title=f'{name}\ntruncated icosahedron TI')
    draw(2, sp, sc, title=f'TI Star: volume {vol} × TI')
    draw(3, sp + HF, sc + ['#f5f0dc'] * len(HF), title='pentakis hull of the 32 tips', faint=len(HF))
    draw(4, sp + OF, sc + [GOLD] * len(OF), title=f'TI scaled × {"2" if s == 2 else "φ"} (volume {turn} × TI):\nthe next turn begins', faint=len(OF))
fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')
fig.savefig('figures/both-cycles.png', dpi=170, facecolor=BG, bbox_inches='tight'); print('ok')
