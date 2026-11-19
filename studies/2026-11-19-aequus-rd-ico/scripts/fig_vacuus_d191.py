# The Vacuus of the fair RD ∩ icosahedron die (D191), drawn as one panel of Equanimity's Figure 2 (scripts/fig_vacuus.py there):
# each plate as the triangle from the centre to its edge; see-through shell (edges only). Slate: plates on no mirror of the die's
# group Th; pale sand: plates on a mirror of Th (the 3 coordinate planes). Colours are labels only.
# Usage: python fig_vacuus_d191.py <verts-rdi.json> <out.png>
import json, sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
D = json.load(open(sys.argv[1]))
MIRRORS = [np.eye(3)[i] for i in range(3)]
CS, CM = '#5b6f8a', '#d9c7a3'
edges = {}
for f, vs in D['faces'].items():
    P = np.array([[float(c) for c in v] for v in vs])
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        key = tuple(sorted([tuple(np.round(a, 9)), tuple(np.round(b, 9))]))
        nrm = np.cross(a, b); nrm /= np.linalg.norm(nrm)
        edges.setdefault(key, [a, b, not any(abs(abs(nrm @ q) - 1) < 1e-9 for q in MIRRORS)])
O = np.zeros(3)
mir = [[O, a, b] for a, b, s in edges.values() if not s]; slo = [[O, a, b] for a, b, s in edges.values() if s]
fig = plt.figure(figsize=(4.2, 4.4), dpi=220)
ax = fig.add_subplot(1, 1, 1, projection='3d', computed_zorder=False)
ax.add_collection3d(Poly3DCollection(mir, facecolors=CM, edgecolors='none', alpha=0.22))
ax.add_collection3d(Poly3DCollection(slo, facecolors=CS, edgecolors=CS, linewidths=0.2, alpha=0.55))
ax.add_collection3d(Line3DCollection([[a, b] for a, b, s in edges.values()], colors='#1a1a1a', linewidths=0.7))
r = max(np.abs(np.array([a for a, b, s in edges.values()])).max(), 1)
for s in (ax.set_xlim, ax.set_ylim, ax.set_zlim): s(-r, r)
ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.view_init(elev=22, azim=-58)
ax.set_title('32 faces: no regular faces\nrhombic dodecahedron ∩ icosahedron', fontsize=9)
plt.subplots_adjust(left=0, right=1, top=0.92, bottom=0)
fig.savefig(sys.argv[2], facecolor='white', bbox_inches='tight', pad_inches=0.05)
ns = len(slo)
print('plates %d, sloping %d, on mirrors %d' % (len(edges), ns, len(mir)))
print('FINAL ok' if len(edges) == 90 and ns == 84 and len(mir) == 6 else 'FINAL FAIL')
