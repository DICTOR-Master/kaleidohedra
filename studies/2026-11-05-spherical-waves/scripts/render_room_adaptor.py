# Render the room adaptor of the densest cut-OG lattice packing, alone (three views) and with the cut OGs around it. DICTO 5 Nov 2026.
import json, itertools, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LightSource
from scipy.spatial import ConvexHull
D = np.load("adaptor-mesh.npz"); V, T, c, B = D["v"], D["t"], D["c"], D["B"]
O = np.array(json.load(open("/home/dicto/study-runs/og-pent/cut/data/network.json"))["ocd"]); O = O - O.mean(0)
tris = V[T] - c; ls = LightSource(azdeg=315, altdeg=40)
def shade(tr, col):
    n = np.cross(tr[:, 1] - tr[:, 0], tr[:, 2] - tr[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    k = np.clip(0.35 + 0.65*np.abs(n @ np.array([0.4, -0.5, 0.75])/np.linalg.norm([0.4, -0.5, 0.75])), 0, 1)
    return [tuple(np.array(col)*kk) + (1,) for kk in k]
def ogfaces():
    h = ConvexHull(O); return [O[s] for s in h.simplices]
fig = plt.figure(figsize=(14, 7.2), facecolor="white"); r = np.abs(tris).max()*0.62
for i, (el, az) in enumerate(((20, 30), (60, 120), (-10, 250))):
    ax = fig.add_subplot(2, 3, i + 1, projection="3d")
    ax.add_collection3d(Poly3DCollection(tris, facecolors=shade(tris, (0.98, 0.70, 0.30)), edgecolors="none"), autolim=False)
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(el, az)
ax = fig.add_subplot(2, 3, (4, 6), projection="3d")
ax.add_collection3d(Poly3DCollection(tris, facecolors=shade(tris, (0.98, 0.70, 0.30)), edgecolors="none"), autolim=False)
F = ogfaces(); near = sorted([B @ np.array(m, float) - c for m in itertools.product(range(-2, 3), repeat=3)], key=np.linalg.norm)[:4]
for s in near:
    tr = np.array([f + s for f in F]); ax.add_collection3d(Poly3DCollection(tr, facecolors=[(0.30, 0.64, 0.65, 0.22)]*len(tr), edgecolors=(0.2, 0.4, 0.4, 0.15), linewidths=0.2), autolim=False)
r2 = r*1.75; ax.set_xlim(-r2, r2); ax.set_ylim(-r2, r2); ax.set_zlim(-r2, r2); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(20, 30)
fig.text(0.5, 0.965, "The room adaptor of the densest cut-OG lattice packing: one piece per copy, cut OG + adaptor fill space", ha="center", fontsize=12)
fig.text(0.5, 0.505, "the adaptor from three sides (volume 0.326555, 22.4% of space)", ha="center", fontsize=9, color="#333")
fig.text(0.5, 0.03, "with the four nearest cut OGs (translucent teal) that bite into it  ·  DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=9, color="#333")
plt.savefig("room-adaptor.png", dpi=125, bbox_inches="tight"); print("FINAL ok")
