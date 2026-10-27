"""DICTO 2026-10-27: 'the squares can be octahedrons'. Test, exactly: a cell (regular tetrahedron) cut through four of its
edges gives a four-sided face; it is a square exactly when the cut is parallel to two opposite edges of the cell and halfway
between them (the equator of the cell's midpoint octahedron). For every gap slice of the atlas, count the four-sided faces
and those that are such mid-cuts, exactly in Q(√5).
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python squares_midcuts.py
"""
import json

from polytopes import polytope
from q5 import Q5, dot

P = polytope("600-cell")
V, cells = P["V"], P["st"]["K4"]
A = json.load(open("../data/atlas600.json"))
tot_quad = tot_sq = 0
for lab, D in P["dirs"].items():
    d = D["d"]; h = [dot(v, d) for v in V]
    hs = sorted(set(h), key=float)
    for a, b in zip(hs, hs[1:]):
        if float(a + b) < 0:
            continue
        hv = (a + b) / Q5(2)
        quad = sq = 0
        for c in cells:
            below = [h[i] for i in c if (h[i] - hv).sign() < 0]
            above = [h[i] for i in c if (h[i] - hv).sign() > 0]
            if len(below) == 2 and len(above) == 2:
                quad += 1
                if below[0] == below[1] and above[0] == above[1] and below[0] + above[0] == hv + hv:
                    sq += 1
        rec = next(o for o in A if o["direction"] == lab and not o["at_vertex_layer"] and abs(o["h"] - float(hv)) < 1e-9)
        tot_quad += quad; tot_sq += sq
        print(f"{lab:>12} gap at {float(hv):8.5f}: four-sided {quad:3d} (atlas {rec['face_sizes'].get('4', 0):3d}), mid-cut squares {sq}")
print("total four-sided", tot_quad, "mid-cut squares", tot_sq)
