# The catalogue's selection (DICTO 2026-10-13, "are you breaking them down too much?"): the main route, every convex stage, and
# the partial rings that sit on a complete shell (a convex stage). All other stages stay as counts in stages.json / partials.json.
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
st = {R['view']: R for R in json.load(open(os.path.join(HERE, 'stages.json')))}
steps = json.load(open(os.path.join(HERE, 'steps.json')))
part = json.load(open(os.path.join(HERE, 'partials.json')))
out = {}
for view in DATA:
    pieces = DATA[view]; allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    ring = [f'{r}@{np.linalg.norm(np.array(V, float).mean(0) - c0):.2f}' for r, V, _ in pieces]
    order = [s['added'].split(' ')[0] for s in steps[view]]
    route = [order[:k + 1] for k in range(len(order))]
    shells = [r for r, s in zip(route, steps[view]) if s['convex']] + st[view]['convex']
    whole = list({tuple(sorted(x)): list(x) for x in route + st[view]['convex']}.values())
    shell_sets = {tuple(sorted(x)) for x in shells}
    kept = []
    for p in part[view]:
        idx = set(p['pieces'])
        w = tuple(sorted(g for g in set(ring[i] for i in idx) if all(i in idx for i, x in enumerate(ring) if x == g)))
        if w in shell_sets: kept.append(p)
    out[view] = {'whole': whole, 'partial': kept}
    print(view, len(whole), 'whole,', len(kept), 'partial')
json.dump(out, open(os.path.join(HERE, 'selection.json'), 'w'))
