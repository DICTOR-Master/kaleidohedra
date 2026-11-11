"""Chapter 4 figure: (a) the chamfered cube Z (generators e1, e2, e3 and the four half body diagonals) in grey glass with its six
cube pyramids (gold) in the dents under the squares; (b) a block of the filling: chamfered cubes and the unit cubes between them.
Checks the hexagon side lengths (1, sqrt3/2, sqrt3/2, 1, sqrt3/2, sqrt3/2, the long sides opposite) and volume 15 on the way."""
import itertools, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
h = .5; G = np.array([[1,0,0],[0,1,0],[0,0,1],[h,h,h],[h,h,-h],[h,-h,h],[-h,h,h]])
P = np.array([sum(s * g / 2 for s, g in zip(sg, G)) for sg in itertools.product((1, -1), repeat=7)])
H = ConvexHull(P); V = P[H.vertices]; assert abs(H.volume - 15) < 1e-9
faces = {}
for s, eq in zip(H.simplices, H.equations): faces.setdefault(tuple(np.round(eq, 6)), set()).update(s)
polys = []; sides_ok = True
for eq, idx in faces.items():
    Q = P[list(idx)]; c = Q.mean(0); n = np.array(eq[:3]); u = Q[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    Q = Q[np.argsort(np.arctan2((Q - c) @ w, (Q - c) @ u))]; polys.append(Q)
    if len(Q) == 6:
        e = np.round(np.linalg.norm(np.roll(Q, -1, 0) - Q, axis=1), 6); sides_ok &= sorted(e) == sorted([1, 1, .866025, .866025, .866025, .866025]) and all(abs(e[i] - e[i + 3]) < 1e-6 for i in range(3))
print('faces', {k: sum(1 for p in polys if len(p) == k) for k in (4, 6)}, 'hexagon sides 1, sqrt3/2 with opposite sides equal:', sides_ok, 'volume', round(H.volume, 9))
fig = plt.figure(figsize=(11, 5.2), dpi=170); fig.patch.set_facecolor('#f3f0e8')
ax = fig.add_subplot(121, projection='3d'); ax.set_facecolor('#f3f0e8')
ax.add_collection3d(Poly3DCollection(polys, facecolor=(0.62, 0.66, 0.74, 0.28), edgecolor=(0.2, 0.22, 0.28, 0.9), linewidths=0.8))
pyr = []
for ax_i in range(3):
    for s in (1, -1):
        sq = [p for p in polys if len(p) == 4 and abs(abs(p.mean(0)[ax_i]) - np.abs(P[:, ax_i]).max()) < 1e-6 and np.sign(p.mean(0)[ax_i]) == s]
        if not sq: continue
        base = sq[0]; apex = base.mean(0) - s * 0.5 * np.eye(3)[ax_i]
        for i in range(4): pyr.append([base[i], base[(i + 1) % 4], apex])
ax.add_collection3d(Poly3DCollection(pyr, facecolor=(0.83, 0.65, 0.16, 0.95), edgecolor=(0.35, 0.25, 0.03, 1), linewidths=0.6))
r = 1.9; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.view_init(22, -35); ax.set_axis_off()
ax.set_title('(a) the chamfered cube, volume 15, and its six cube pyramids', fontsize=9)
ax2 = fig.add_subplot(122, projection='3d'); ax2.set_facecolor('#f3f0e8')
Lp = [np.array(v) for v in itertools.product(range(-2, 3, 2), repeat=3) if sum(v) % 4 == 0 and max(abs(x) for x in v) <= 2]
for t in Lp:
    if abs(t[2]) > 0: continue
    ax2.add_collection3d(Poly3DCollection([p + t for p in polys], facecolor=(0.62, 0.66, 0.74, 0.22), edgecolor=(0.2, 0.22, 0.28, 0.55), linewidths=0.4))
    c = t + np.array([2, 0, 0]); cube = list(itertools.product((-.5, .5), repeat=3))
    cf = [[c + np.array(cube[i]) for i in f] for f in ([0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5])]
    ax2.add_collection3d(Poly3DCollection(cf, facecolor=(0.83, 0.65, 0.16, 0.9), edgecolor=(0.35, 0.25, 0.03, 1), linewidths=0.5))
r = 3.4; ax2.set_xlim(-r + 1, r + 1); ax2.set_ylim(-r, r); ax2.set_zlim(-r, r); ax2.set_box_aspect((1, 1, 1)); ax2.view_init(28, -50); ax2.set_axis_off()
ax2.set_title('(b) one layer of the filling: chamfered cubes and unit cubes', fontsize=9)
plt.tight_layout(); plt.savefig('fig-chamfered.png', facecolor=fig.get_facecolor())
print('FINAL ok' if sides_ok and abs(H.volume - 15) < 1e-9 else 'FINAL FAIL')
