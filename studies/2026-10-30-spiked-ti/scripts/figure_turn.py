# TI Star: the solids of one turn (golden cycle, s = phi). Panels: the core Ip ∩ Dh (icosahedron truncated at 1/phi^3); the
# dodecahedron Dh of the 20 hexagon tips with TI + 20 hexagonal spikes inside and the 12 pentagonal spikes coming through its faces;
# the icosahedron Ip of the 12 pentagon tips with the 20 hexagonal spikes coming through; and K, both at once.
import json, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull, HalfspaceIntersection
GOLD, VIOLET, TEAL, BG, PALE, RED, BLUE = '#d4af37', '#8e5bd6', '#2bb3a3', '#0d0d12', '#e8e2cc', '#cd3e28', '#3f6fd8'
phi = (1 + 5 ** .5) / 2; s = phi
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
pen = np.array([s * f.mean(0) for f in FT if len(f) == 5]); hexa = np.array([s * f.mean(0) for f in FT if len(f) == 6])
def spikes(n):
    out = []
    for f in FT:
        if len(f) != n: continue
        t = s * f.mean(0); out += [np.array([f[i], f[(i + 1) % len(f)], t]) for i in range(len(f))]
    return out
def pl(Q):
    h = ConvexHull(Q); u = {}
    for eq in h.equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
core = HalfspaceIntersection(np.vstack([pl(pen), pl(hexa)]), np.zeros(3)).intersections; core = core[ConvexHull(core).vertices]
EQ = pl(P); nper = [sum(1 for p in P if abs(eq[:3] @ p + eq[3]) < 1e-8) for eq in EQ]
cut = lambda H: (lambda W: W[ConvexHull(W).vertices])(HalfspaceIntersection(H, np.zeros(3)).intersections)
D_TI = cut(EQ[[n == 5 for n in nper]]); I_TI = cut(EQ[[n == 6 for n in nper]])
fig = plt.figure(figsize=(17, 4.4), facecolor=BG); R = 1.55 * s
def panel(k, layers, title):
    ax = fig.add_subplot(1, 5, k, projection='3d')
    for polys, col, al in layers: ax.add_collection3d(Poly3DCollection(polys, facecolor=col, edgecolor='#f5f0dc', linewidths=0.25, alpha=al))
    for a in 'xyz': getattr(ax, f'set_{a}lim')(-R, R)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(16, 28); ax.set_title(title, color=PALE, fontsize=9)
panel(1, [(faces(P), GOLD, 0.95), (faces(D_TI), BLUE, 0.16), (faces(I_TI), RED, 0.16)], 'inner pair: TI\'s own\ndodecahedron and icosahedron')
panel(2, [(faces(P), GOLD, 0.95), (faces(core), '#f5f0dc', 0.16)], 'core: icosahedron\ntruncated at 1/φ³')
panel(3, [(faces(P), GOLD, 0.95), (spikes(6), TEAL, 0.95), (spikes(5), VIOLET, 0.95), (faces(hexa), BLUE, 0.2)], 'dodecahedron of the 20 hexagon tips:\nthe 12 pentagonal spikes come through')
panel(4, [(faces(P), GOLD, 0.95), (spikes(6), TEAL, 0.95), (spikes(5), VIOLET, 0.95), (faces(pen), RED, 0.2)], 'icosahedron of the 12 pentagon tips:\nthe 20 hexagonal spikes come through')
panel(5, [(spikes(6), TEAL, 0.9), (spikes(5), VIOLET, 0.9), (faces(np.vstack([pen, hexa])), '#f5f0dc', 0.16)], 'pentakis hull K: the spiked dodecahedron\nand the spiked icosahedron at once')
fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')
fig.savefig('figures/turn-solids.png', dpi=170, facecolor=BG, bbox_inches='tight'); print('ok')
