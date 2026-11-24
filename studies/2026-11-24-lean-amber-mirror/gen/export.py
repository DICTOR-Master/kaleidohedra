"""Export the data of the three-edge certificate of Theorem 3 (iv), paper #118, from the amber-ammann study.
Runs odd_edges.py of that study unchanged (runpy) and writes cert.json: for each of the three odd edges, the cells round it in
cycle order and the walls joining them; the tree path (the BFS frames of odd_edges.py) from the start cell to the first cell of
each cycle; every wall's two cells (patch order) and four 6D corners; the three planes as odd_edges.py prints them.
Usage: python export.py PATH/TO/amber-ammann/scripts"""
import runpy, sys, os, io, json, contextlib
S = sys.argv[1]; sys.path.insert(0, S)
with contextlib.redirect_stdout(io.StringIO()):
    G = runpy.run_path(os.path.join(S, "odd_edges.py"))
interior, walls, parent, start, odd, planes = G['interior'], G['walls'], G['parent'], G['start'], G['odd'], G['planes']
cert = [((-2,0,-1,-1,0,-1),(-1,0,-1,-1,0,-1)), ((-2,0,-1,-1,0,-1),(-2,0,0,-1,0,-1)), ((-1,0,-1,-1,0,-1),(-1,0,0,-1,0,-1))]
def wall_between(a, b): return next(k for k, (t1, t2, W, p) in enumerate(walls) if {t1, t2} == {a, b})
out = {"start": start, "edges": [], "walls": {}}
for e in cert:
    seq, wk = interior[e]; c = seq[0]; path = [c]
    while c != start: c = parent[c]; path.append(c)
    path = path[::-1]; pw = [wall_between(path[i], path[i+1]) for i in range(len(path)-1)]
    out["edges"].append({"edge": e, "cells": seq, "walls": wk, "path": path, "path_walls": pw,
                         "plane": [str(q) for q in planes[odd.index(e)]]})
    for k in wk + pw:
        t1, t2, W, pts = walls[k]; out["walls"][k] = {"a": t1, "b": t2, "corners": pts}
json.dump(out, open("cert.json", "w"), indent=1)
print(json.dumps(out["edges"], indent=None)); print("walls", sorted(out["walls"]))
