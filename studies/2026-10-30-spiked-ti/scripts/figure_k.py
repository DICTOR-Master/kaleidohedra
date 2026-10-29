# K alone (golden cycle): the hull of the 32 tips of the TI Star. Left: K, its 60 triangles coloured by the corner they rise to
# (each triangle has one pentagon tip, violet corner, and two hexagon tips); middle: K as the dodecahedron of the hexagon tips (blue)
# with 12 low pentagonal pyramids; right: K as the icosahedron of the pentagon tips (red) with 20 low triangular pyramids.
import json, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
GOLD, VIOLET, TEAL, BG, PALE, RED, BLUE = '#d4af37', '#8e5bd6', '#2bb3a3', '#0d0d12', '#e8e2cc', '#cd3e28', '#3f6fd8'
phi = (1 + 5 ** .5) / 2; s = phi
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
h = ConvexHull(P); F = []; seen = set()
for eq in h.equations:
    k = tuple(np.round(eq, 7))
    if k not in seen: seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
pen = np.array([s * P[f].mean(0) for f in F if len(f) == 5]); hexa = np.array([s * P[f].mean(0) for f in F if len(f) == 6])
K = np.vstack([pen, hexa]); hk = ConvexHull(K)
tris = [K[sm] for sm in hk.simplices]
def faces(Q):
    hq = ConvexHull(Q); out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out:
            ids = [i for i, p in enumerate(Q) if abs(eq[:3] @ p + eq[3]) < 1e-8]; R = Q[ids]; c = R.mean(0); n = eq[:3]
            a = R[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a); out[k] = R[np.argsort(np.arctan2((R - c) @ b, (R - c) @ a))]
    return list(out.values())
fig = plt.figure(figsize=(13, 4.6), facecolor=BG); Rm = 1.25 * np.linalg.norm(K, axis=1).max()
def panel(k, layers, title):
    ax = fig.add_subplot(1, 3, k, projection='3d')
    for polys, col, al in layers: ax.add_collection3d(Poly3DCollection(polys, facecolor=col, edgecolor='#f5f0dc', linewidths=0.5, alpha=al))
    for a in 'xyz': getattr(ax, f'set_{a}lim')(-Rm, Rm)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(18, 28); ax.set_title(title, color=PALE, fontsize=10)
# shade each triangle by its normal for depth, gold
panel(1, [(tris, GOLD, 0.95)], 'K: 32 corners, 60 triangles\n(12 five-fold corners, 20 six-fold)')
# dodecahedron + 12 caps
caps = [t for t in tris]
panel(2, [(faces(hexa), BLUE, 0.85), (tris, VIOLET, 0.25)], 'a dodecahedron (the 20 hexagon tips)\nwith 12 low pentagonal pyramids')
panel(3, [(faces(pen), RED, 0.85), (tris, TEAL, 0.25)], 'an icosahedron (the 12 pentagon tips)\nwith 20 low triangular pyramids')
fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')
fig.savefig('figures/k-alone.png', dpi=170, facecolor=BG, bbox_inches='tight'); print('ok')
