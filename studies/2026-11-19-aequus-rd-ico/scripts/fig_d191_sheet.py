# D191 Aequus 32 (rhombic dodecahedron ∩ icosahedron): (a) the solid, (b) its Vacuus, (c) the Vacuus down a 3-fold axis
# (one hexagon on a cube diagonal and the ring of faces sharing a corner with it). Style of Equanimity Figures 1-2:
# solid faces, crisp edges; colours are labels only (three neutral tones for the three face families);
# Vacuus: slate = sloping plates, pale sand = plates on the mirrors of Th (the coordinate planes).
import json, sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
D = json.load(open(sys.argv[1]))
FACES = {int(k): np.array([[float(c) for c in v] for v in vs]) for k, vs in D['faces'].items()}
assert len(FACES) == 32
def order(P):
    c = P.mean(0); n = c / np.linalg.norm(c); u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    return P[np.argsort(np.arctan2((P - c) @ w, (P - c) @ u))], n
fam = lambda k: 0 if k < 12 else (1 if k < 20 else 2)
sides = {k: len(P) for k, P in FACES.items()}
assert {sides[k] for k in range(12)} == {5} and {sides[k] for k in range(12, 32)} == {6}, sides
TONES = ['#d9c7a3', '#5b6f8a', '#9aa79a']   # sand: RD pentagons; slate: 8 diagonal hexagons; sage: 12 other hexagons
CS, CM = '#5b6f8a', '#d9c7a3'
L = np.array([0.45, -0.35, 0.82]); L /= np.linalg.norm(L)
edges = {}
for k, P in FACES.items():
    P, n = order(P)
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        key = tuple(sorted([tuple(np.round(a, 9)), tuple(np.round(b, 9))]))
        nrm = np.cross(a, b); nrm /= np.linalg.norm(nrm)
        on_mirror = any(abs(abs(nrm[j]) - 1) < 1e-9 for j in range(3))
        edges.setdefault(key, [a, b, not on_mirror])
nslope = sum(1 for e in edges.values() if e[2]); assert (len(edges), nslope) == (90, 84), (len(edges), nslope)
fig = plt.figure(figsize=(15, 5.6), dpi=200)
# (a) solid
ax = fig.add_subplot(1, 3, 1, projection='3d', computed_zorder=False)
polys, cols = [], []
for k, P in FACES.items():
    P, n = order(P); base = np.array(matplotlib.colors.to_rgb(TONES[fam(k)]))
    polys.append(P); cols.append(np.clip(base * (0.55 + 0.45 * max(0.0, float(n @ L))), 0, 1))
ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors='#1a1a1a', linewidths=0.6))
r = np.abs(np.concatenate(polys)).max()
for s in (ax.set_xlim, ax.set_ylim, ax.set_zlim): s(-r, r)
ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-58); ax.set_axis_off()
ax.set_title('(a) D191 Aequus 32 (rhombic dodecahedron ∩ icosahedron)\nsand: 12 pentagons at 1; slate: 8 hexagons at 1.002759…;\nsage: 12 hexagons at 1.010663…', fontsize=9)
# (b) Vacuus
ax = fig.add_subplot(1, 3, 2, projection='3d', computed_zorder=False)
O = np.zeros(3)
ax.add_collection3d(Poly3DCollection([[O, a, b] for a, b, s in edges.values() if not s], facecolors=CM, edgecolors='none', alpha=0.35))
ax.add_collection3d(Poly3DCollection([[O, a, b] for a, b, s in edges.values() if s], facecolors=CS, edgecolors=CS, linewidths=0.2, alpha=0.55))
ax.add_collection3d(Line3DCollection([[a, b] for a, b, s in edges.values()], colors='#1a1a1a', linewidths=0.7))
for s in (ax.set_xlim, ax.set_ylim, ax.set_zlim): s(-r, r)
ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-58); ax.set_axis_off()
ax.set_title('(b) its Vacuus: 90 plates from the centre to the edges\nslate: 84 sloping; sand: 6 on the mirrors of Th', fontsize=9)
# (c) down the 3-fold axis of one diagonal hexagon
F0, z = order(FACES[12]); y = F0[0] - (F0[0] @ z) * z; y /= np.linalg.norm(y); x = np.cross(y, z); R = np.array([x, y, z])
ring = [P for P in FACES.values() if any(np.min(np.linalg.norm(F0 - p, axis=1)) < 1e-9 for p in P)]
Vr = np.concatenate(ring); inring = lambda p: np.min(np.linalg.norm(Vr - p, axis=1)) < 1e-9
E = [(R @ a, R @ b, s) for a, b, s in edges.values() if inring(a) and inring(b)]
c3, s3 = np.cos(2 * np.pi / 3), np.sin(2 * np.pi / 3); rot = lambda p: np.array([c3 * p[0] - s3 * p[1], s3 * p[0] + c3 * p[1], p[2]])
miss = sum(1 for a, b, s in E if not any((np.allclose(rot(a), p, atol=1e-7) and np.allclose(rot(b), q, atol=1e-7)) or
                                           (np.allclose(rot(a), q, atol=1e-7) and np.allclose(rot(b), p, atol=1e-7)) for p, q, t in E))
assert miss == 0, miss
ax = fig.add_subplot(1, 3, 3)
for a, b, s in sorted(E, key=lambda e: (e[0][2] + e[1][2]) / 3):
    ax.add_patch(plt.Polygon([[0, 0], a[:2], b[:2]], closed=True, facecolor=CS if s else CM, alpha=0.55 if s else 0.35,
                             edgecolor=CS if s else 'none', linewidth=0.2))
for a, b, s in E: ax.plot([a[0], b[0]], [a[1], b[1]], color='#1a1a1a', lw=0.8)
rr = max(max(np.abs(a[:2]).max(), np.abs(b[:2]).max()) for a, b, s in E) * 1.05
ax.set_xlim(-rr, rr); ax.set_ylim(-rr, rr); ax.set_aspect('equal'); ax.set_axis_off()
ax.set_title('(c) the Vacuus down a 3-fold axis: one slate hexagon and its ring\nsides alternate; it turns without a mirror', fontsize=9)
plt.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.01, wspace=0.05)
plt.savefig(sys.argv[2], facecolor='white')
print('edges', len(edges), 'sloping', nslope, '| 3-fold check: edges not mapped', miss); print('FINAL ok')
