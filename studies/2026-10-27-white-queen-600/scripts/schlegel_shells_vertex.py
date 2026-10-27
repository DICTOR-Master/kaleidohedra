"""The 600-piece shell (Schlegel view from just outside one cell; DICTO 2026-10-27 'how many shells, how many changes of
solid, changeovers'). Cells are grouped into shells by the height of their centre along the cell-first axis (the axis
through the outer cell and the central cell). Within a shell, cells are sorted into shapes by an invariant that does not
depend on the eye distance: the sorted list of (height, distance from the axis) of their four vertices (equal for cells
related by a symmetry round the axis, mirrors included). Also: adjacency shells (steps from the central cell), as a check.
Decimal check (rounded to 1e-9); exact version to follow.
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python schlegel_shells.py ../data/600cell-source.json
"""
import json
import sys
from collections import defaultdict, deque

import numpy as np

D = json.load(open(sys.argv[1])); V = np.array(D["vertices"]); C = [tuple(c) for c in D["cells"]]
num = lambda q: float(eval(q[0])) + float(eval(q[1])) * 5 ** .5
u = np.array([num(x) for x in D["directions"]["vertex-first"]["d_exact"]]); u /= np.linalg.norm(u)
h = V @ u; r = np.linalg.norm(V - np.outer(h, u), axis=1)
ch = {c: round(float(h[list(c)].mean()), 9) for c in C}
shells = defaultdict(list)
for c in C:
    shells[ch[c]].append(c)
inv = lambda c: tuple(sorted((round(float(h[i]), 9), round(float(r[i]), 9)) for i in c))
print("height shells (from the central cell to the outer cell):")
rows = []
for k, hv in enumerate(sorted(shells)):
    cs = shells[hv]; kinds = defaultdict(int)
    for c in cs:
        kinds[inv(c)] += 1
    rows.append({"shell": k, "height": hv, "cells": len(cs), "shapes": len(kinds), "per_shape": sorted(kinds.values())})
    print(f"  shell {k:2d}  height {hv:+.6f}  cells {len(cs):3d}  shapes {len(kinds)}  {sorted(kinds.values())}")
allkinds = {inv(c) for c in C}
print("cells", len(C), "shells", len(shells), "distinct shapes", len(allkinds))
# adjacency shells from the lowest cell
tri = defaultdict(list)
for c in C:
    for x in c:
        tri[tuple(sorted(set(c) - {x}))].append(c)
nb = defaultdict(list)
for t, cs in tri.items():
    nb[cs[0]].append(cs[1]); nb[cs[1]].append(cs[0])
start = min(C, key=lambda c: ch[c]); dist = {start: 0}; q = deque([start])
while q:
    c = q.popleft()
    for n in nb[c]:
        if n not in dist:
            dist[n] = dist[c] + 1; q.append(n)
bfs = defaultdict(int)
for c, k in dist.items():
    bfs[k] += 1
print("adjacency shells (steps from the central cell):", [bfs[k] for k in sorted(bfs)])
json.dump({"height_shells": rows, "distinct_shapes": len(allkinds), "adjacency_shells": [bfs[k] for k in sorted(bfs)]},
          open("../data/schlegel_shells_vertex.json", "w"), indent=1)
