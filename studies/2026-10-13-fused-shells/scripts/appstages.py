# The app's Top shell stages (DICTO 2026-10-13: "about 11 interesting shapes on chain step 2, 5 on lotus seed, 4 on dodecahedral
# chain", seen with the slider): pieces grouped exactly as world-chains.js does (centre distance, levels merged within 6% of the
# radius), each stage = every level up to it, fused and described (steps.describe_union). Output: appstages.json.
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA
import steps
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
VIEWS = sys.argv[1].split(',') if len(sys.argv) > 1 else ['karma.step2', 'karma.lotus', 'karma.dodeca']
OUT = sys.argv[2] if len(sys.argv) > 2 else 'appstages.json'
out = {}
for view in VIEWS:
    pieces = DATA[view]
    allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    P = [(np.array(V, float) - c0, F) for _, V, F in pieces]
    radius = np.linalg.norm(allP - c0, axis=1).max()
    dist = [float(np.linalg.norm(np.array(V, float).mean(0) - c0)) for _, V, _ in pieces]
    levels = []
    for d in sorted(dist):
        if not levels or d - levels[-1] >= radius * 0.06: levels.append(d)
    shell = [min(range(len(levels)), key=lambda i: abs(levels[i] - d)) for d in dist]
    groups = {}
    for (Q, F), (r, _, _) in zip(P, pieces): groups.setdefault(f'{r}@{np.linalg.norm(Q.mean(0)):.2f}', []).append((Q, F))
    steps.set_axes(groups)
    res = []
    for k in range(len(levels)):
        idx = [i for i in range(len(P)) if shell[i] <= k]
        d = steps.describe_union([P[i] for i in idx])
        roles = {}
        for i in range(len(P)):
            if shell[i] == k: roles[pieces[i][0]] = roles.get(pieces[i][0], 0) + 1
        res.append({'level': k, 'adds': roles, 'pieces': [i for i in range(len(P)) if shell[i] == k], **{x: d[x] for x in ('convex', 'faces', 'faceShapes', 'planes', 'planeFamilies')}})
        print(view, k + 1, '/', len(levels), roles, '->', 'convex' if d['convex'] else 'non-convex', d['faces'], d['faceShapes'], d['planes'], 'planes', flush=True)
    out[view] = res
json.dump(out, open(os.path.join(HERE, OUT), 'w'))
print('done')
