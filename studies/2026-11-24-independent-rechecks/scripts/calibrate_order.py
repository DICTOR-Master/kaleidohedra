# Fix the in-family order of the 122 directions: the convention under which sampled catalogue dice are fair.
import random, sys, json
import numpy as np
from dirs import CONVS, directions, catalogue
from die_num import unit, build, solid_angles
cat = catalogue(); print('catalogue dice:', len(cat))
random.seed(7); sample = random.sample(cat, 80)
res = {}
for conv in CONVS:
    D, _ = directions(conv); Df = np.array([unit([float(x) for x in v]) for v in D]); worst = 0
    for src, sid, idx, dep, N, _, _ in sample:
        V, fc = build(Df[idx], np.array(dep)); om = solid_angles(V, fc)
        worst = max(worst, max(abs(o - 4 * np.pi / N) for o in om))
    res[''.join(conv)] = worst; print(conv, 'max |Omega - 4pi/N| =', '%.2e' % worst, flush=True)
good = [k for k, v in res.items() if v < 1e-8]
print('conventions making all 80 sampled dice fair:', good)
json.dump(res, open('../data/calibrate_order.json', 'w'), indent=1)
