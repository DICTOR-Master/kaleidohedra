# Cut OG (one sphere) beside its all-equal-edge version. DICTO 5 Nov 2026.
import json, numpy as np, math, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from fractions import Fraction as F
s5 = math.sqrt(5); D = json.load(open("step1-ocd-exact.json"))
q = lambda x: (lambda a, b: float(F(a)) + float(F(b))*s5)(*x.split("|")) if isinstance(x, str) else float(x)
V = np.array([[q(x) for x in p] for p in D["V"]]); V -= V.mean(0); C = V[np.linalg.norm(V, axis=1) < .69]
L = np.load("trunc-tri-left.npy"); E = np.load("trunc-tri-right.npy"); E -= E.mean(0)
def faces(P):
    h = ConvexHull(P); pl = {}
    for eq, s in zip(h.equations, h.simplices): pl.setdefault(tuple(np.round(eq, 5)), (eq, set()))[1].update(s)
    out = []
    for eq, f in pl.values():
        f = list(f); c = P[f].mean(0); e1 = P[f[0]] - c; e2 = np.cross(eq[:3], e1)
        f.sort(key=lambda i: math.atan2((P[i] - c) @ e2, (P[i] - c) @ e1)); out.append(P[f])
    return out
col = {3: "#d4a020", 5: "#c0392b", 6: "#4fa3a5"}
fig = plt.figure(figsize=(12, 6.4), facecolor="white")
for k, (P, t) in enumerate([(L, "LEFT: hexagons as truncated triangles\n(all angles 120°, sides alternate 0.16 / 0.30)"),
                            (E, "RIGHT: its mirror image\nthe long and short sides swap places")]):
    ax = fig.add_subplot(1, 2, k + 1, projection="3d"); F_ = faces(P)
    ax.add_collection3d(Poly3DCollection(F_, facecolors=[col.get(len(f), "#888") for f in F_], edgecolors="#222", linewidths=.6, alpha=1), autolim=False)
    m = .55; ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_zlim(-m, m); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(18, 32); ax.set_title(t, fontsize=11)
    print(t.split("\n")[0], {n: sum(len(f) == n for f in F_) for n in (3, 5, 6)})
fig.text(.5, .03, "Hexagons as truncated triangles: possible only by giving up mirror symmetry, so the solid comes as a left and a right.\nDICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=9, color="#444")
plt.savefig("og-truncated-triangles.png", dpi=130, bbox_inches="tight")
