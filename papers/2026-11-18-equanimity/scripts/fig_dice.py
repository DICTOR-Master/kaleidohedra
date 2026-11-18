# Figure 1: the eight fair dice of the axis lines, from the exact vertex dumps (study 2026-11-18-fair-32-die, verts-*.json).
# Solid faces, crisp edges, no haze; two neutral tones for the two face families (labels only).
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ORDER = [('tc', 10, 'tetrahedron ∩ cube'), ('co', 14, 'cube ∩ octahedron'), ('tr', 16, 'tetrahedron ∩ rhombic dodecahedron'),
         ('cr', 18, 'cube ∩ rhombic dodecahedron'), ('or', 20, 'octahedron ∩ rhombic dodecahedron'), ('di', 32, 'dodecahedron ∩ icosahedron'),
         ('dt', 42, 'dodecahedron ∩ rhombic triacontahedron'), ('it', 50, 'icosahedron ∩ rhombic triacontahedron')]
NA = {'tc': 4, 'co': 6, 'tr': 4, 'cr': 6, 'or': 8, 'di': 12, 'dt': 12, 'it': 20}
CA, CB = '#5b6f8a', '#d9c7a3'   # slate, sand (labels only)
L = np.array([0.45, -0.35, 0.82]); L /= np.linalg.norm(L)
fig = plt.figure(figsize=(12, 6.4), dpi=200)
for k, (m, N, name) in enumerate(ORDER):
    D = json.load(open('verts-%s.json' % m))
    ax = fig.add_subplot(2, 4, k + 1, projection='3d', computed_zorder=False)
    polys, cols = [], []
    for f, vs in D['faces'].items():
        P = np.array([[float(c) for c in v] for v in vs]); c = P.mean(0); n = c / np.linalg.norm(c)
        u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        P = P[np.argsort(np.arctan2((P - c) @ w, (P - c) @ u))]
        base = np.array(matplotlib.colors.to_rgb(CA if int(f) < NA[m] else CB))
        shade = 0.55 + 0.45 * max(0.0, float(n @ L))
        polys.append(P); cols.append(np.clip(base * shade, 0, 1))
    pc = Poly3DCollection(polys, facecolors=cols, edgecolors='#1a1a1a', linewidths=0.6)
    ax.add_collection3d(pc)
    r = max(np.abs(np.concatenate(polys)).max(), 1)
    for s in (ax.set_xlim, ax.set_ylim, ax.set_zlim): s(-r, r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-58); ax.set_axis_off()
    ax.set_title('%d faces\n%s' % (N, name), fontsize=9)
plt.subplots_adjust(left=0, right=1, top=0.93, bottom=0, wspace=0, hspace=0.12)
plt.savefig('fig-fair-dice.png', facecolor='white')
print('FINAL ok')
