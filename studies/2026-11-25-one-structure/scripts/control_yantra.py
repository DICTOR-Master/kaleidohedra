"""Positive control for B1: the rational Sri Yantra R1 of study 2026-11-08-sri-yantra (every corner rational; README there,
section 3) drawn as 27 segments, run through the same exact shadow code (shadow_core.py) and pencil test; its incidence is
written in the format of data/shadows.json for yantra_sat.py, which must answer SAT. Writes data/control-yantra.json."""
import os, sys, json
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "../../2026-11-25-plate-harmony/scripts")))
from nf import NF
from shadow_core import Shadow
F = NF([-5, 0, 1], "2.2360679774997896964091736687312762354406183596115")
b = [Fr(248, 3611), Fr(48, 233), Fr(4, 13), Fr(23, 61), Fr(86, 197), Fr(8, 15), Fr(576, 937), Fr(172, 229), Fr(8, 9)]
w = [Fr(836, 3611), Fr(3401, 11883), Fr(6, 13), Fr(1805, 12444), Fr(703, 6698), Fr(38, 255), Fr(456, 937), Fr(16245, 50609), Fr(323, 1485)]
a = {8: b[0], 6: b[1], 9: b[2], 1: b[5], 5: b[6], 4: b[7], 2: b[8], 3: Fr(1), 7: Fr(0)}
P = []; segs = []
def pt(x, y):
    P.append((F.c(x), F.c(-y))); return len(P) - 1
for i in range(1, 10):
    l = pt(-w[i - 1], b[i - 1]); r = pt(w[i - 1], b[i - 1]); ap = pt(Fr(0), a[i])
    segs += [(l, r), (l, ap), (r, ap)]
c = pt(Fr(0), Fr(1, 2))
S = Shadow(P, segs, c); S.run(); s = S.summary()
print({k: v for k, v in s.items() if k != "incidence"}, flush=True)
assert s["marmas"] >= 18 and s["yantra_test"]["pass"] >= 1
s.update({"polyhedron": "control: rational Sri Yantra R1", "kind": "control", "direction": "plane"})
json.dump({"shadows": [s]}, open(os.path.join(STUDY, "data/control-yantra.json"), "w"), default=str)
print("FINAL ok control_yantra", flush=True)
