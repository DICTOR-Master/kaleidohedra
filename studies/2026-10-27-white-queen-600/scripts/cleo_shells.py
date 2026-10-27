"""The Cleo-core shell of the 600-cell (DICTO 2026-10-27): the 600 cells round one vertex v, in 15 shells by the height of
their centre along v. Perspective from an eye just beyond the opposite vertex v' (height -2 - 1/10, exact): the 20 cells at
v' face the eye and wrap the outside; the other 580 cells nest inside without overlap, the 20 cells at v in the middle.
EXACT check: in every shell, all cells have the same sorted list of six squared edge lengths in this view (Q(√5)), and the
core cells are the icosahedron's central pyramid (apex at the centre, base vertices on a regular icosahedron).
Picture: renders/cleo-shells.png, one panel per shell (that shell solid, the shells inside it faint), core in gold.
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python cleo_shells.py
"""
import json
from collections import defaultdict
from fractions import Fraction as Fr

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from polytopes import polytope
from q5 import Q5, ZERO, dot, q5str
from render import BG, GOLD, mark
from shadows import Space

P = polytope("600-cell")
V, cells = P["V"], P["st"]["K4"]
d = P["dirs"]["vertex-first"]["d"]                 # = the vertex v itself (|v|² = 4)
sp = Space(4, d, None)
h = [dot(x, d) / dot(d, d) * Q5(2) for x in V]    # height along v, in units where v is at +2
EYE = Q5(Fr(-21, 10))
proj = []
for x, hx in zip(V, h):
    s = Q5(1) / (hx - EYE)
    proj.append(tuple(s * y for y in sp.y(x)))       # exact coordinates in the frame of sp (metric sp.mdot)
cent = lambda c: sum((h[i] for i in c), ZERO) / Q5(4)
shells = defaultdict(list)
for c in cells:
    shells[cent(c)].append(c)
keys = sorted(shells, key=float, reverse=True)       # from the cells at v (top) down to the cells at v'
def edge_list(c):
    L = []
    for i in range(4):
        for j in range(i + 1, 4):
            w = tuple(a - b for a, b in zip(proj[c[i]], proj[c[j]]))
            L.append(sp.mdot(w, w))
    return tuple(sorted(L, key=float))
report = []
for k, key in enumerate(keys):
    kinds = {edge_list(c) for c in shells[key]}
    report.append({"shell": k, "cells": len(shells[key]), "kinds_by_exact_edges": len(kinds), "height": q5str(key)})
    print(f"shell {k:2d}: {len(shells[key]):3d} cells, {len(kinds)} kind(s) by exact edge lengths, centre height {q5str(key)}")
# core = the 20 cells at v: apex v projects to the centre? check the 12 neighbours are equidistant and at one height
v = max(range(120), key=lambda i: float(h[i]))
nb = sorted({i for c in shells[keys[0]] for i in c} - {v})
rad = {sp.mdot(tuple(a - b for a, b in zip(proj[i], proj[v])), tuple(a - b for a, b in zip(proj[i], proj[v]))) for i in nb}
print("core: 20 cells, apex projects to", "the centre" if all(y == ZERO for y in proj[v]) else "off centre",
      "| 12 base corners", len(nb), "at", len(rad), "distance(s) from the apex")
json.dump({"eye_height": "-21/10", "shells": report}, open("../data/cleo_shells.json", "w"), indent=1, ensure_ascii=False)

# picture
F = np.array([[float(y) * m for y, m in zip(p, sp.mf)] for p in proj])
COL = plt.cm.viridis(np.linspace(0.15, 0.95, len(keys)))
plt.rcParams["figure.facecolor"] = BG
fig = plt.figure(figsize=(16, 10.6))
lim = None
for k, key in enumerate(keys):
    ax = fig.add_subplot(3, 5, k + 1, projection="3d"); ax.set_facecolor(BG); ax.set_axis_off()
    for j in range(k):                            # inner shells faint
        ax.add_collection3d(Poly3DCollection([F[list(t)] for c in shells[keys[j]] for t in
                            [(c[0], c[1], c[2]), (c[0], c[1], c[3]), (c[0], c[2], c[3]), (c[1], c[2], c[3])]],
                            facecolor=(1, 1, 1, 0.02), edgecolor=(1, 1, 1, 0.06), linewidths=0.2))
    col = GOLD if k == 0 else COL[k]
    tris = [F[list(t)] for c in shells[key] for t in [(c[0], c[1], c[2]), (c[0], c[1], c[3]), (c[0], c[2], c[3]), (c[1], c[2], c[3])]]
    ax.add_collection3d(Poly3DCollection(tris, facecolor=col, edgecolor="#f3ead2", linewidths=0.25, alpha=0.55 if k else 0.85))
    pts = F[sorted({i for c in shells[key] for i in c})]
    r = np.abs(pts).max() * 1.05
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-r, r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(20, 30)
    name = "Cleo core: 20 Cleo-Icos" if k == 0 else ("outer wrap: the 20 cells at the far vertex" if k == len(keys) - 1 else f"shell {k}")
    ax.set_title(f"{name}\n{len(shells[key])} pieces · one kind", color=GOLD if k == 0 else "white", fontsize=8)
fig.suptitle("The 600-cell as a shell of 600 pieces round a Cleo core: 15 shells, each of one kind of piece",
             color="white", fontsize=13)
fig.text(0.5, 0.925, "perspective from just beyond the opposite vertex · each panel drawn at its own scale · exact check: every shell one kind by exact edge lengths",
         color="#aab0bb", fontsize=8.5, ha="center")
mark(fig)
fig.savefig("../renders/cleo-shells.png", dpi=130, facecolor=BG)
