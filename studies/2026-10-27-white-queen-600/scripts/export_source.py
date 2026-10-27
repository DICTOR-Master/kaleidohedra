"""The White Queen world, step 1: the 600-cell source model, exact, with its checks.

The 120 vertices come from the definition (q5/polytopes.py: the 8 permutations of (±2,0,0,0), the 16 points (±1,±1,±1,±1),
the 96 even permutations of (±φ,±1,±1/φ,0)); edges, triangles and tetrahedral cells are FOUND (minimal-distance pairs and
their cliques), never typed in. Every check below is exact arithmetic in Q(√5); the script stops at the first failure.
Output data/600cell-source.json: each coordinate as [a, b] meaning a + b√5 (a, b rational strings), floats for drawing,
edges, triangles, cells, the four direction elements, and the check log.
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python export_source.py
"""
import json
from collections import Counter

from polytopes import polytope
from q5 import Q5, dot, sub

P = polytope("600-cell")
V, st = P["V"], P["st"]
E, T, C = st["E"], st["T"], st["K4"]
log = []


def check(name, ok):
    log.append({"check": name, "pass": bool(ok)})
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        raise SystemExit(1)


check("120 vertices", len(V) == 120 and len(set(V)) == 120)
check("every vertex at squared distance 4 from the centre (circumradius 2)", all(dot(v, v) == Q5(4) for v in V))
check("720 edges", len(E) == 720)
check("every edge has squared length 6 - 2√5 (edge √5 - 1)", st["edge2"] == Q5(6, -2) and
      all(dot(sub(V[i], V[j]), sub(V[i], V[j])) == Q5(6, -2) for i, j in E))
deg = Counter(x for e in E for x in e)
check("every vertex has 12 neighbours", set(deg.values()) == {12})
check("1200 triangles", len(T) == 1200)
check("600 tetrahedral cells", len(C) == 600)
check("Euler characteristic V - E + F - C = 0", len(V) - len(E) + len(T) - len(C) == 0)
tri_in = Counter(t for c in C for t in [tuple(sorted(set(c) - {x})) for x in c])
check("every triangle lies in exactly 2 cells", len(tri_in) == 1200 and set(tri_in.values()) == {2})
edge_in = Counter(tuple(sorted((c[i], c[j]))) for c in C for i in range(4) for j in range(i + 1, 4))
check("every edge lies in exactly 5 cells", set(edge_in.values()) == {5} and len(edge_in) == 720)
vert_in = Counter(x for c in C for x in c)
check("every vertex lies in exactly 20 cells", set(vert_in.values()) == {20})
adj = st["adj"]
ok = True
for v in range(120):
    nb = adj[v]
    sub_deg = [len(adj[u] & nb) for u in nb]
    ok &= len(nb) == 12 and set(sub_deg) == {5}
check("the 12 neighbours of every vertex form an icosahedron (each touches 5 of the others)", ok)
check("every cell is a regular tetrahedron (its 6 edges are edges)", all(
    tuple(sorted((c[i], c[j]))) in set(map(tuple, E)) for c in C for i in range(4) for j in range(i + 1, 4)))

fx = lambda q: [str(q.a), str(q.b)]
out = {
    "name": "600-cell",
    "definition": "vertices: permutations of (±2,0,0,0); (±1,±1,±1,±1); even permutations of (±φ,±1,±1/φ,0), φ=(1+√5)/2",
    "coordinate_format": "each coordinate [a, b] = a + b√5, a and b rational",
    "circumradius": 2, "edge": "√5 - 1",
    "vertices_exact": [[fx(x) for x in v] for v in V],
    "vertices": [[round(float(x), 15) for x in v] for v in V],
    "edges": [list(e) for e in E],
    "triangles": [list(t) for t in T],
    "cells": [list(c) for c in C],
    "directions": {k: {"element": list(d["element"]), "d_exact": [fx(x) for x in d["d"]]} for k, d in P["dirs"].items()},
    "checks": log,
}
json.dump(out, open("../data/600cell-source.json", "w"), separators=(",", ":"), ensure_ascii=False)
print("written ../data/600cell-source.json")
