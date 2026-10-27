"""The Red Queen 120-cell picture (DICTO 2026-10-28): its 120 dodecahedra in 9 layers round one, in perspective from just beyond the
opposite cell (as the Cleo shells of #63), and the gold core cut from its centre into Aristotle's 12 pentagonal pyramids.
Floats for drawing only; every count and shape is proved exactly in red_queen.py and five_pyramids.py. usage: render_red_queen.py <600cell-source.json> <out.png>"""
import json, sys, os
from collections import defaultdict
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.expanduser("~/kres-tmp/4d/scripts")); from render import BG, GOLD, mark
S = json.load(open(sys.argv[1])); V = np.array(S["vertices"], float); cells = S["cells"]
R = np.array([V[c].mean(0) for c in cells])                       # Red Queen corners = White Queen cell centres
cov = defaultdict(list); [cov[i].append(ci) for ci, c in enumerate(cells) for i in c]
RC = [cov[i] for i in range(120)]                                  # Red Queen cells: the 20 corners round each White Queen vertex
d = V[0] / np.linalg.norm(V[0]); hR = R @ d; he = hR.min() * 21 / 20
B = np.linalg.svd(np.eye(4) - np.outer(d, d))[0][:, :3]           # a basis of the space across the axis
P = np.array([(p - (p @ d) * d) @ B / ((p @ d) - he) for p in R])
hc = V @ d; layers = sorted(set(np.round(hc, 9)), reverse=True)
L = [[i for i in range(120) if abs(hc[i] - h) < 1e-7] for h in layers]
edges = [(a, b) for a in range(600) for b in range(a + 1, 600) if abs(np.linalg.norm(R[a] - R[b]) - np.linalg.norm(R[RC[0][0]] - R[[x for x in RC[0] if x != RC[0][0]]]).min(1).min()) < 1e-6] if False else None
e2 = min(np.sum((R[a] - R[b]) ** 2) for a in RC[0] for b in RC[0] if a != b)
def cell_edges(c): return [(a, b) for k, a in enumerate(c) for b in c[k + 1:] if abs(np.sum((R[a] - R[b]) ** 2) - e2) < 1e-7]
def solid(ax, c, col, alpha, lw):
    pts = P[c]; h = ConvexHull(pts)
    ax.add_collection3d(Poly3DCollection([pts[s] for s in h.simplices], facecolor=col, edgecolor="none", alpha=alpha))
    ax.add_collection3d(Line3DCollection([P[[a, b]] for a, b in cell_edges(c)], colors="#f3ead2", linewidths=lw))
COL = plt.cm.viridis(np.linspace(0.15, 0.95, len(L)))
plt.rcParams["figure.facecolor"] = BG
fig = plt.figure(figsize=(16, 7.4))
names = ["core"] + [f"layer {k}" for k in range(1, len(L))]
for k in range(len(L) + 1):
    ax = fig.add_subplot(2, 5, k + 1, projection="3d"); ax.set_facecolor(BG); ax.set_axis_off()
    if k == len(L):                                                # the core cut into Aristotle's 12 pentagonal pyramids
        c = RC[L[0][0]]; pts = P[c]; h = ConvexHull(pts)
        for s in h.simplices: ax.add_collection3d(Poly3DCollection([np.vstack([pts[s], [0, 0, 0]])[[0, 1, 2]], np.vstack([pts[s[[0, 1]]], [[0, 0, 0]]]),
                                                                     np.vstack([pts[s[[1, 2]]], [[0, 0, 0]]]), np.vstack([pts[s[[2, 0]]], [[0, 0, 0]]])], facecolor=GOLD, edgecolor="none", alpha=0.18))
        ax.add_collection3d(Line3DCollection([P[[a, b]] for a, b in cell_edges(c)], colors=GOLD, linewidths=1.2))
        ax.add_collection3d(Line3DCollection([[np.zeros(3), P[a]] for a in c], colors="#f3ead2", linewidths=0.5))
        lim = np.abs(pts).max(); title = "the core: 12 pentagonal pyramids\n(Aristotle's dodecahedron pyramid)"
    else:
        for j in range(k): [solid(ax, RC[i], COL[j], 0.05, 0.08) for i in L[j]]
        for i in L[k]: solid(ax, RC[i], GOLD if k == 0 else COL[k], 0.85 if k == 0 else 0.5, 0.35)
        lim = np.abs(np.vstack([P[RC[i]] for j in range(k + 1) for i in L[j]])).max()
        title = f"{names[k]}\n{len(L[k])} dodecahedr{'on' if len(L[k]) == 1 else 'a'} · one kind"
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim): f(-lim, lim)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(20, 30)
    ax.set_title(title, color=GOLD if k in (0, len(L)) else "white", fontsize=8.5)
fig.suptitle("The Red Queen 120-cell: 120 dodecahedra in 9 layers round one (1, 12, 20, 12, 30, 12, 20, 12, 1)", color="white", fontsize=12)
mark(fig); fig.savefig(sys.argv[2], dpi=130, facecolor=BG)
print("written", sys.argv[2])
