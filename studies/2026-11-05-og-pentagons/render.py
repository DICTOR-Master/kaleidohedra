# OG and the OG with its 12 five-fold tips cut (= rectified truncated icosahedron). DICTO question 5 Nov 2026.
import json, numpy as np, math, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from fractions import Fraction as F
s5 = math.sqrt(5); D = json.load(open("step1-ocd-exact.json"))
q = lambda x: (lambda a, b: float(F(a)) + float(F(b))*s5)(*x.split("|")) if isinstance(x, str) else float(x)
V = np.array([[q(x) for x in p] for p in D["V"]]); V -= V.mean(0); r = np.linalg.norm(V, axis=1)
def faces(P):
    h = ConvexHull(P); pl = {}
    for eq, s in zip(h.equations, h.simplices): pl.setdefault(tuple(np.round(eq, 6)), (eq, set()))[1].update(s)
    out = []
    for eq, f in pl.values():
        f = list(f); c = P[f].mean(0); n = eq[:3]; e1 = P[f[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        f.sort(key=lambda i: math.atan2((P[i] - c) @ e2, (P[i] - c) @ e1)); out.append(P[f])
    return out
col = {3: "#d4a020", 4: "#7a5fb0", 5: "#c0392b", 6: "#4fa3a5"}
fig = plt.figure(figsize=(12, 6.4), facecolor="white")
for k, (P, t) in enumerate([(V, "DICTO Ogdoecontahedron (OG)\n20 hexagons + 60 kites"),
                            (V[r < 0.69], "OG with its 12 five-fold tips cut\n= rectified truncated icosahedron\n20 hexagons, 12 pentagons, 60 triangles")]):
    ax = fig.add_subplot(1, 2, k + 1, projection="3d"); F_ = faces(P)
    ax.add_collection3d(Poly3DCollection(F_, facecolors=[col[len(f)] for f in F_], edgecolors="#222", linewidths=.6, alpha=.95), autolim=False)
    m = .6; ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_zlim(-m, m); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(18, 32); ax.set_title(t, fontsize=11)
fig.text(.5, .03, "The 90 remaining corners all lie on the OG sphere (r = 2/3): the edge midpoints of a regular truncated icosahedron.\nDICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=9, color="#444")
plt.savefig("og-pentagons.png", dpi=130, bbox_inches="tight")
