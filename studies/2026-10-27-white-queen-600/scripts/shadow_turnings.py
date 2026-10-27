"""The White Queen 600-cell: every view along the six turnings (DICTO 2026-10-27: 'the missing views ... is the proof').

Turning from main view A to main view B (great circle in the plane of the two unit directions), the shadow's front layer
(cells facing the viewer) changes only when a cell turns side-on (its centre direction n becomes perpendicular to the
view u). Between two such events the same cells are in front, so the front tiling keeps one pattern (the shadow analogue
of #63's one-pattern-per-gap lemma). This script lists, for each of the six turnings, the event angles (cells swapping
from front to back or back to front) and, in every gap, the shadow hull's vertex and face counts and the number of
front cells. Floating point (decimal check); exact version to follow.
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python shadow_turnings.py ../data/600cell-source.json
"""
import itertools
import json
import sys

import numpy as np
from scipy.spatial import ConvexHull

D = json.load(open(sys.argv[1]))
V = np.array(D["vertices"]); C = np.array(D["cells"])
num = lambda q: float(eval(q[0])) + float(eval(q[1])) * 5 ** .5
U = {k: (lambda u: u / np.linalg.norm(u))(np.array([num(x) for x in d["d_exact"]])) for k, d in D["directions"].items()}
N = V[C].mean(1)                                   # cell centres = outward normals (up to length)
NAMES = list(U)


def faces_of(P):
    H = ConvexHull(P)
    planes = {tuple(np.round(eq, 7)) for eq in H.equations}
    return len(H.vertices), len(planes)


def view(u):
    Q, _ = np.linalg.qr(np.column_stack([u, np.eye(4)]))
    return V @ Q[:, 1:4]


out = {}
for a, b in itertools.combinations(NAMES, 2):
    u0 = U[a]; w = U[b] - (U[b] @ u0) * u0; w /= np.linalg.norm(w)
    end = np.arctan2(U[b] @ w, U[b] @ u0)                                  # angle from A to B
    # cell side-on when (n.u0) cos t + (n.w) sin t = 0
    t = np.mod(np.arctan2(-(N @ u0), N @ w), np.pi)
    ev = np.unique(np.round(t[(t > 1e-9) & (t < end - 1e-9)], 9))
    marks = np.concatenate([[0.0], ev, [end]])
    gaps = []
    for i, (x, y) in enumerate(zip(marks, marks[1:])):
        tm = (x + y) / 2; u = np.cos(tm) * u0 + np.sin(tm) * w
        nv, nf = faces_of(view(u))
        gaps.append({"from_deg": round(np.degrees(x), 4), "to_deg": round(np.degrees(y), 4),
                     "front_cells": int((N @ u > 1e-12).sum()), "hull_vertices": nv, "hull_faces": nf})
    out[f"{a} -> {b}"] = {"angle_deg": round(np.degrees(end), 4), "events": len(ev),
                          "event_deg": [round(np.degrees(x), 4) for x in ev], "gaps": gaps}
    print(f"{a:>12} -> {b:<12} turn {np.degrees(end):7.3f}°  swap events {len(ev):3d}  gaps {len(gaps):3d}  "
          f"front cells {sorted({g['front_cells'] for g in gaps})}", flush=True)
json.dump(out, open("../data/shadow_turnings.json", "w"), indent=1)
