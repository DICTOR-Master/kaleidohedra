# The star chain, golden version: S0 = TI, S1 = Star Halo, S2 = the 1/phi^3 core, S3 = Halo II (placeholder), each the hull of the
# spike tips of the one before; S4 has the shape of TI again. Each drawn alone, scaled to the same radius, shaded; corners of S1 and S3
# coloured by kind (five-fold violet, six-fold teal).
import json, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
GOLD, VIOLET, TEAL, BG, PALE = '#d4af37', '#8e5bd6', '#2bb3a3', '#0d0d12', '#e8e2cc'
phi = (1 + 5 ** .5) / 2; t = phi
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return V, list(out.values())
chain = [P]
for _ in range(4):
    V, FL = facelist(chain[-1]); chain.append(np.array([t * (-eq[3]) * eq[:3] for eq, _ in FL]))
L = np.array([-0.4, 0.5, 0.8]); L /= np.linalg.norm(L)
names = ['TI', 'Star Halo', 'core (icosahedron\ntruncated at 1/φ³)', 'Catalan pentakis\ndodecahedron', 'TI again']
fig = plt.figure(figsize=(16, 4), facecolor=BG)
for k, Q in enumerate(chain):
    V, FL = facelist(Q); V = V / np.linalg.norm(V, axis=1).max()
    ax = fig.add_subplot(1, 5, k + 1, projection='3d'); base = np.array(mc.to_rgb(GOLD if k % 2 == 0 else VIOLET))
    polys, cols = [], []
    for eq, ids in FL:
        R = V[ids]; c = R.mean(0); a = R[0] - c; a /= np.linalg.norm(a); b = np.cross(eq[:3], a); R = R[np.argsort(np.arctan2((R - c) @ b, (R - c) @ a))]
        polys.append(R); cols.append(tuple(np.clip(base * (0.35 + 0.75 * max(0, eq[:3] @ L)), 0, 1)))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolor='#2a2010', linewidths=0.6))
    if k % 2 == 1:
        r = np.linalg.norm(V, axis=1); five = r > (r.max() + r.min()) / 2 if r.max() / r.min() > 1.001 else np.zeros(len(r), bool)
        deg = np.array([sum(1 for _, ids in FL if i in ids) for i in range(len(V))])
        ax.scatter(*V[deg == 5].T, color=VIOLET, s=22); ax.scatter(*V[deg == 6].T, color=TEAL, s=14)
    for a in 'xyz': getattr(ax, f'set_{a}lim')(-0.85, 0.85)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(18, 28)
    ax.set_title(f'S{k}: {names[k]}', color=PALE, fontsize=10)
fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')
fig.savefig('figures/star-chain.png', dpi=170, facecolor=BG, bbox_inches='tight'); print('ok')
