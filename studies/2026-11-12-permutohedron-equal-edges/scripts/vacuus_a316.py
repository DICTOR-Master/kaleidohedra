"""DICTO Vacuus of the DICTO 13-Corner Octet Atom (A3-16), as defined in #87: O = corner centroid; one fin (triangle O, a, b)
from the centre to every edge ab, one strut from the centre to every corner. Exists iff O is strictly inside every face plane.
Reports: existence, fins (24), struts (13), which fins are coplanar (they merge into flat plates), and renders the Vacuus
inside a see-through shell.  usage: python vacuus_a316.py FIGDIR   (reads FIGDIR/a3-16.json written by render_a316.py)
"""
import sys, os, json, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

out = sys.argv[1]; d = json.load(open(os.path.join(out, "a3-16.json")))
P = np.array(d["corners"]); faces = d["faces"]
O = P.mean(axis=0)
checks = []
def chk(n, c): checks.append(bool(c)); print(("PASS " if c else "FAIL ") + n, flush=True)
# existence: O strictly inside every face plane
inside = []
for f in faces:
    n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); n /= np.linalg.norm(n)
    c = P[f].mean(axis=0)
    if n @ (c - P.mean(axis=0)) < 0: n = -n
    inside.append(n @ (O - P[f[0]]) < -1e-9)
chk("Vacuus exists (centroid strictly inside all 13 face planes)", all(inside))
edges = sorted({tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in faces for k in range(len(f))})
chk("24 fins", len(edges) == 24); chk("13 struts", len(P) == 13)
# coplanar fins -> plates
def plane(a, b):
    n = np.cross(P[a] - O, P[b] - O); return n / np.linalg.norm(n)
groups = []
for e in edges:
    n = plane(*e)
    for g in groups:
        if abs(abs(n @ g["n"]) - 1) < 1e-9: g["e"].append(e); break
    else: groups.append({"n": n, "e": [e]})
sizes = sorted((len(g["e"]) for g in groups), reverse=True)
print("fin planes:", len(groups), "fins per plane:", sizes, flush=True)
print("plates of 2 or more coplanar fins:", sum(1 for s in sizes if s > 1), flush=True)
json.dump({"centroid": O.tolist(), "fin_planes": len(groups), "fins_per_plane": sizes}, open(os.path.join(out, "a3-16-vacuus.json"), "w"))

pal = ["#d9534f", "#5b8fd6", "#7cc47a", "#e8b04a", "#9b6fd0", "#3fb8b0", "#e07b39", "#c4c4c4"]
fig = plt.figure(figsize=(12, 4.8), dpi=200)
for k, (el, az) in enumerate([(22, 30), (22, 150), (70, 75)]):
    ax = fig.add_subplot(1, 3, k + 1, projection="3d")
    for gi, g in enumerate(sorted(groups, key=lambda g: -len(g["e"]))):
        c = pal[gi] if len(g["e"]) > 1 else "#bdbdbd"
        ax.add_collection3d(Poly3DCollection([[O, P[a], P[b]] for a, b in g["e"]], facecolor=c, edgecolor="#333", linewidths=0.8, alpha=0.85))
    ax.add_collection3d(Line3DCollection([[O, p] for p in P], colors="#222", linewidths=1.6))
    ax.add_collection3d(Poly3DCollection([P[f] for f in faces], facecolor=(0.6, 0.75, 0.95, 0.07), edgecolor="#555", linewidths=1.2))
    r = np.abs(P - O).max() * 1.05
    ax.set_xlim(O[0] - r, O[0] + r); ax.set_ylim(O[1] - r, O[1] + r); ax.set_zlim(O[2] - r, O[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(el, az); ax.axis("off")
fig.text(0.5, 0.04, "DICTO Vacuus of the DICTO 13-Corner Octet Atom: 24 fins (coplanar fins share a colour, single fins grey), 13 struts, see-through shell", ha="center", fontsize=9.5)
logo = os.path.expanduser("~/k-research/papers/dicto-logo.png")
if os.path.exists(logo):
    a = fig.add_axes([0.9, 0.82, 0.08, 0.15]); a.imshow(plt.imread(logo)); a.axis("off")
fig.savefig(os.path.join(out, "a3-16-vacuus.png"), bbox_inches="tight"); print("wrote render", flush=True)
print("FINAL ok" if all(checks) else "FINAL FAIL")
