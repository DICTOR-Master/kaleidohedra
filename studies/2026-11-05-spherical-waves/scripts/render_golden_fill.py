# Render the golden phi-step fill of the room and the leftover (DICTO 5 Nov 2026), plus the "skin" test: how much leftover lies within
# 1, 2, 3 voxels of the cut-OG surface.
import numpy as np, itertools, json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy import ndimage
G = np.load("golden-fill.npz"); W = np.load("lattice-wave.npz"); S = W["S"] > 0.5; free, root, ids, c, B = G["free"], G["root"], G["ids"], G["c"], G["B"]; N = S.shape[0]
dist = ndimage.distance_transform_edt(~np.tile(S, (3, 3, 3)))[N:2*N, N:2*N, N:2*N]
for k in (1, 2, 3): print(f"leftover within {k} voxel(s) of the cut-OG surface: {(free & (dist <= k + 0.01)).sum()/free.sum():.3f}  (all gap: {((~S) & (dist <= k + 0.01)).sum()/(~S).sum():.3f})")
img = np.array(list(itertools.product(range(-1, 2), repeat=3)), float) @ B.T
def near(x): return min((x + s for s in img), key=lambda y: np.linalg.norm(y - c))
D = np.load("adaptor-mesh.npz"); AV, AT = D["v"], D["t"]
fig = plt.figure(figsize=(15, 7.5), facecolor="white")
cols = ["#b8860b", "#d4a020", "#e8c25a", "#f0d98c", "#f7ecc7"]
ax = fig.add_subplot(1, 2, 1, projection="3d"); polys, fc = [], []
for k, o, E in zip(G["PL_k"], G["PL_o"], G["PL_E"]):
    o = near(o)
    if np.linalg.norm(o - c) > 0.62: continue
    P = lambda b: o + b[0]*E[0] + b[1]*E[1] + b[2]*E[2]
    for i in range(3):
        j, l = [x for x in range(3) if x != i]
        for s in (0, 1):
            q = [np.eye(3)[i]*s, np.eye(3)[i]*s + np.eye(3)[j], np.eye(3)[i]*s + np.eye(3)[j] + np.eye(3)[l], np.eye(3)[i]*s + np.eye(3)[l]]
            polys.append([P(b) - c for b in q]); fc.append(cols[k])
ax.add_collection3d(Poly3DCollection(polys, facecolors=fc, edgecolors="#5a4100", linewidths=0.1), autolim=False)
ax.add_collection3d(Poly3DCollection(AV[AT] - c, facecolors=(0.3, 0.64, 0.65, 0.05), edgecolors="none"), autolim=False)
r = 0.55; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(22, 35)
ax.set_title("golden rhombohedra grown in φ-steps (dark gold = first, pale = last)\ninside the room adaptor (faint teal): 84% filled", fontsize=10)
ax = fig.add_subplot(1, 2, 2, projection="3d")
v = np.argwhere(free); X = np.array([near(x) for x in ((v + 0.5)/N) @ B.T]) - c; inroom = np.linalg.norm(X, axis=1) < 0.62
big = (root[tuple(v.T)] == ids[0])
ax.scatter(*X[inroom & big].T, s=1.2, c="#3a7bd5", alpha=0.35, label="the one connected leftover (93%)")
ax.scatter(*X[inroom & ~big].T, s=4, c="#e04040", alpha=0.9, label="small bits (grid dust)")
ax.add_collection3d(Poly3DCollection(AV[AT] - c, facecolors=(0.3, 0.64, 0.65, 0.04), edgecolors="none"), autolim=False)
ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(22, 35)
ax.legend(loc="lower center", frameon=False, fontsize=9, markerscale=6); ax.set_title("what the rhombi leave: 16% of the room\n(the slivers carry the Dehn invariant: rhombi alone can never close them)", fontsize=10)
fig.text(0.5, 0.02, "Densest lattice packing of the cut OG · room found by spherical waves, tone by harmonics, filled by growing golden rhombi · DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=8.5, color="#444")
plt.savefig("golden-fill.png", dpi=125, bbox_inches="tight"); print("FINAL ok")
