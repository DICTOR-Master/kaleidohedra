# Views inside the cell of the cut-OG lattice packing (DICTO 5 Nov 2026): planes through the gap room (cage) and its windows,
# the solid (copper) and the wave field, critical points marked (atom gold, bond white, window cyan, room black ring).
import numpy as np, itertools, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
D = np.load("lattice-wave.npz"); S, F, B, P = D["S"], D["F"], D["B"], D["pts"]; N = S.shape[0]; Bi = np.linalg.inv(B)
cF = ndimage.spline_filter(F, order=3, mode="grid-wrap")
cS = S
def sample(c, X): return ndimage.map_coordinates(c, ((X @ Bi.T)*N - 0.5).T % N, order=3 if c is cF else 1, mode="grid-wrap", prefilter=False)
real = lambda q: (q/N) @ B.T
cage = real(P[P[:, 3] == 0][0, :3]); wins = [real(p[:3]) for p in P if p[3] == 1]
img = np.array(list(itertools.product(range(-1, 2), repeat=3)), float) @ B.T
def near(x, ref): return min((x + s for s in img), key=lambda y: np.linalg.norm(y - ref))
wg = sorted([near(w, cage) for w in wins], key=lambda w: np.linalg.norm(w - cage))[:4]
planes = [("through the gap room and two of its windows", np.cross(wg[0] - cage, wg[1] - cage)), ("through the gap room, turned 90°", wg[0] - cage), ("through the gap room, third direction", np.cross(np.cross(wg[0] - cage, wg[1] - cage), wg[0] - cage))]
ext = 1.1; n = 220; t = np.linspace(-ext, ext, n)
fig, axs = plt.subplots(2, 3, figsize=(13, 8.8), facecolor="white")
for j, (title, nv) in enumerate(planes):
    nv = nv/np.linalg.norm(nv); e1 = np.cross(nv, [0.3, 0.5, 0.8]); e1 /= np.linalg.norm(e1); e2 = np.cross(nv, e1)
    X = cage + t[:, None, None]*e1 + t[None, :, None]*e2; Xf = X.reshape(-1, 3)
    s = sample(cS, Xf).reshape(n, n); fv = sample(cF, Xf).reshape(n, n)
    axs[0, j].imshow(s.T > 0.5, origin="lower", cmap="copper", extent=(-ext, ext, -ext, ext)); axs[0, j].set_title("solid (copper) and gap (black)\n" + title, fontsize=9)
    axs[1, j].imshow(fv.T, origin="lower", cmap="magma", extent=(-ext, ext, -ext, ext)); axs[1, j].contour(t, t, s.T, levels=[0.5], colors="#4dd0e1", linewidths=0.7)
    axs[1, j].set_title("spherical waves at the packing's own wavelength", fontsize=9)
    for p in P:
        x = near(real(p[:3]), cage); dd = (x - cage) @ nv
        if abs(dd) < 0.08:
            a, bb = (x - cage) @ e1, (x - cage) @ e2; st = {3: ("o", "#d4a020", "atom"), 2: ("s", "white", "bond"), 1: ("D", "#4dd0e1", "window"), 0: ("o", "none", "room")}[int(p[3])]
            for ax in axs[:, j]: ax.scatter([a], [bb], marker=st[0], s=70, c=st[1], edgecolors="black", linewidths=1.5, zorder=5)
for ax in axs.ravel(): ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Inside the densest lattice packing of the cut OG: one gap room per copy (black ring), opening through eight windows (cyan)", fontsize=11)
fig.text(0.5, 0.01, "DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=8, color="#555")
plt.savefig("lattice-views.png", dpi=120, bbox_inches="tight"); print("FINAL ok")
