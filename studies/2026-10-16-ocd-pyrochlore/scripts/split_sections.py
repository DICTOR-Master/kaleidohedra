# The three-way split of space in the bcc packing (DICTO, 2026-10-16): Ogdoecontahedra (gold), the non-golden shell inside each
# golden envelope cut at its joints (pink: adapters / resin), the golden region between envelopes (cyan: Bodhi pieces). Exact
# plane sections: (a) through a copy's centre, normal to a cube axis; (b) through a square-face centre (an X junction); (c) the
# joint plane of two joined copies (normal to a three-fold axis), showing the six-pointed star of the two envelope cut faces.
import json, itertools, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T']); R = json.load(open('data/network-render.json'))
cube = np.array(R['cube']); Ec = np.array(json.load(open('data/bodhi-envelope-cut.json'))['envelope_cut'])
B = np.array([T[0] + T[1], T[0] + T[2], T[0]]).T
sites = [B @ np.array(m, float) for m in itertools.product(range(-4, 5), repeat=3)]
def section(P, n, c):
    h = ConvexHull(P); pts = []
    for s in h.simplices:
        for a, b in itertools.combinations(s, 2):
            da, db = P[a] @ n - c, P[b] @ n - c
            if da * db < 0: t = da / (da - db); pts.append(P[a] + t * (P[b] - P[a]))
            elif abs(da) < 1e-12: pts.append(P[a])
    return np.unique(np.round(np.array(pts), 10), axis=0) if pts else np.zeros((0, 3))
a_half = 0.5 * np.linalg.norm(T[0] + T[1])
views = [('through a copy, across a cube axis', cube[0], 0.0, cube[1]),
         ('through an X junction (square-face centre)', cube[0], a_half, cube[1]),
         ('in a joint plane (three-fold axis): the six-pointed star', T[0] / np.linalg.norm(T[0]), np.linalg.norm(T[0]) / 2, None)]
fig, axs = plt.subplots(1, 3, figsize=(16, 5.9), facecolor='#f4f1ea')
for A, (title, n, c, up) in zip(axs, views):
    if up is None: up = np.cross(n, cube[0]); up /= np.linalg.norm(up)
    up = up - (up @ n) * n; up /= np.linalg.norm(up); right = np.cross(up, n); centre = n * c
    A.set_facecolor('#4dd0e1'); A.set_aspect('equal'); A.set_xticks([]); A.set_yticks([])
    for sp in A.spines.values(): sp.set_visible(False)
    W = 1.25 if 'joint' not in title else 0.6
    for layer, P0, fc, ec in [('env', Ec, '#f48fb1', '#ad1457'), ('ocd', O, '#ffc857', '#7a5a00')]:
        for s in sites:
          if abs((s @ n) - c) > 1.2: continue
          for cc in ((c - 1e-6, c + 1e-6) if 'joint' in title else (c,)):   # a hair to each side of a plane that holds faces
            S = section(P0 + s, n, cc)
            if len(S) < 3: continue
            uv = np.c_[(S - centre) @ right, (S - centre) @ up]
            if np.min(np.abs(uv).max(axis=1)) > W + 0.8: continue
            hh = ConvexHull(uv); A.add_patch(Polygon(uv[hh.vertices], closed=True, fc=fc, ec=ec, lw=1.0, alpha=0.95 if layer == 'ocd' else (0.55 if 'joint' in title else 0.9)))
    A.set_xlim(-W, W); A.set_ylim(-W, W); A.set_title(title, fontsize=12, color='#2b2620', fontweight='bold')
fig.text(0.01, 0.025, 'Exact sections of the bcc packing of DICTO Ogdoecontahedra. Gold: the solids (77.4% of space). Pink: the non-golden shell inside each golden envelope (a rhombic triacontahedron cut at the joints), '
         'for Cleo-Ico adapters or resin (11.8%). Cyan: the golden region between envelopes, walled by golden-rhombus planes, for Bodhi pieces and golden rhombohedra (10.7%).', fontsize=9, color='#5b5346', wrap=True)
fig.text(0.99, 0.965, 'DICTO · dictospheres.com', ha='right', fontsize=10, fontweight='bold', color='#5b5346')
fig.tight_layout(rect=(0, 0.07, 1, 0.95)); fig.savefig('renders/three-way-split.png', dpi=140, facecolor='#f4f1ea'); print('ok')
