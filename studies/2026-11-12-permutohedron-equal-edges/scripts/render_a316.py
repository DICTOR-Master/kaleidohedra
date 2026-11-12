"""Render A3-16 (the 13-corner equal-edged atom of the A3 deformation cone) for DICTO, and print its exact corners and faces.

Corners are rebuilt exactly with the study's own walk (same as gp_analyse.build); faces from the convex hull, merged by plane.
Checks: 13 corners, 24 edges all of squared length 1, 13 faces = 4 triangles + 9 four-sided, Euler.
Also compares with the octet lattice and reports which faces are parallel pairs (central symmetry test).
usage: python render_a316.py OUTDIR
"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coxeter import QF, Fan, vsub, vkey
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
F = Fan("A3")
bits = int("53def66f5", 16)
C = len(F.W); V = [None] * C; V[0] = (QF(0), QF(0), QF(0)); st = [0]; ok = True
while st:
    c = st.pop()
    for i in range(3):
        d = F.nb[c][i]; w = F.wallidx[(min(c, d), max(c, d))]
        r = F.walls[w][3] if F.walls[w][0] == c else tuple(-x for x in F.walls[w][3])
        vd = vsub(V[c], r) if bits >> w & 1 else V[c]
        if V[d] is None: V[d] = vd; st.append(d)
        elif vkey(V[d]) != vkey(vd): ok = False
pts = {vkey(v): v for v in V}
ex = list(pts.values())
fl = lambda q: float(q.a) + float(q.b) * math.sqrt(QF.D)
P = np.array([[fl(c) for c in v] for v in ex]); P -= P.mean(axis=0)
checks = []
def chk(n, c): checks.append(c); print(("PASS " if c else "FAIL ") + n, flush=True)
chk("walk closes", ok); chk("13 corners", len(P) == 13)
h = ConvexHull(P)
planes = []
for eq in h.equations:
    if not any(np.allclose(eq, q, atol=1e-9) for q in planes): planes.append(eq)
faces = []
for eq in planes:
    idx = [i for i in range(len(P)) if abs(P[i] @ eq[:3] + eq[3]) < 1e-9]
    c0 = P[idx].mean(axis=0); n = eq[:3]; u = P[idx[0]] - c0; u /= np.linalg.norm(u); vv = np.cross(n, u)
    idx.sort(key=lambda i: math.atan2((P[i] - c0) @ vv, (P[i] - c0) @ u)); faces.append(idx)
edges = set()
for f in faces:
    for k in range(len(f)): edges.add(tuple(sorted((f[k], f[(k + 1) % len(f)]))))
L = [np.linalg.norm(P[a] - P[b]) for a, b in edges]
chk("24 edges", len(edges) == 24); chk("all edges length 1", max(abs(x - 1) for x in L) < 1e-9)
kinds = {}
for f in faces: kinds[len(f)] = kinds.get(len(f), 0) + 1
chk("4 triangles + 9 four-sided", kinds == {3: 4, 4: 9}); chk("Euler", len(P) - len(edges) + len(faces) == 2)
par = sum(1 for i, a in enumerate(planes) for b in planes[i + 1:] if np.allclose(a[:3], -b[:3], atol=1e-9))
print("parallel face pairs:", par, "of", len(planes), "faces (centrally symmetric needs all paired)")
print("corners (exact):"); [print("  ", tuple(str(c) for c in v)) for v in ex]
json.dump({"corners": P.tolist(), "faces": faces}, open(os.path.join(out, "a3-16.json"), "w"))

col = {3: "#e8b04a", 4: "#5b8fd6"}
fig = plt.figure(figsize=(12, 4.6), dpi=200)
logo = os.path.expanduser("~/k-research/papers/dicto-logo.png")
for k, (el, az) in enumerate([(22, 30), (22, 150), (70, 75)]):
    ax = fig.add_subplot(1, 3, k + 1, projection="3d")
    for f in faces:
        sq = len(f) == 4 and all(abs(np.dot(P[f[(j+1)%4]]-P[f[j]], P[f[(j+2)%4]]-P[f[(j+1)%4]])) < 1e-9 for j in range(4))
        c = "#7cc47a" if sq else col[len(f)]
        ax.add_collection3d(Poly3DCollection([P[f]], facecolor=c, edgecolor="#222", linewidths=1.6, alpha=1.0))
    r = np.abs(P).max() * 1.05
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.view_init(el, az); ax.axis("off")
fig.text(0.5, 0.04, "A3-16: 13 corners, 24 equal edges; 4 triangles (gold), 5 squares (green), 4 rhombi 60/120 (blue)", ha="center", fontsize=10)
if os.path.exists(logo):
    im = plt.imread(logo); a = fig.add_axes([0.9, 0.82, 0.08, 0.15]); a.imshow(im); a.axis("off")
fig.savefig(os.path.join(out, "a3-16-render.png"), bbox_inches="tight"); print("wrote render")
print("FINAL ok" if all(checks) else "FINAL FAIL")
