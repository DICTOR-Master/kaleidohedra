# Facts for every stage (the same counting as steps.py): the whole-ring stages (stages.json) and the partial-ring stages
# (partials.json). Written to stages-facts.json. Runs on dicto-node (thousands of unions); progress to stdout.
import os, sys, json
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA
import steps
HERE = os.path.dirname(os.path.abspath(__file__))
CTX = {}


def setup(view):
    pieces = DATA[view]
    allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    P = [(np.array(V, float) - c0, F) for _, V, F in pieces]
    names = [f'{r}@{np.linalg.norm(Q.mean(0)):.2f}' for (Q, _), (r, _, _) in zip(P, pieces)]
    groups = {}
    for (Q, F), g in zip(P, names): groups.setdefault(g, []).append((Q, F))
    steps.set_axes(groups)
    return P, groups, names


def fact(args):
    view, idx = args
    if view not in CTX: CTX[view] = setup(view)
    P = CTX[view][0]
    d = steps.describe_union([P[i] for i in idx])
    return {'convex': d['convex'], 'faces': d['faces'], 'faceShapes': d['faceShapes'], 'planes': d['planes']}


if __name__ == '__main__':
    sel = json.load(open(os.path.join(HERE, '..', 'selection.json')))  # select.py: the catalogue's stages
    whole = {v: sel[v]['whole'] for v in sel}
    partial = {v: sel[v]['partial'] for v in sel}
    out = {}
    with Pool(4) as pool:
        for view in sel:
            P, groups, names = setup(view)
            jobs = [{'groups': S, 'pieces': sorted(i for i, g in enumerate(names) if g in S), 'how': 'whole rings'} for S in whole[view]]
            jobs += [{'groups': sorted({names[i] for i in p['pieces']}), 'pieces': p['pieces'], 'how': p['how'], 'partial': True} for p in partial[view]]
            facts = []
            for k, f in enumerate(pool.imap(fact, [(view, j['pieces']) for j in jobs], chunksize=8)):
                facts.append(f)
                if k % 50 == 0: print(view, k, '/', len(jobs), flush=True)
            out[view] = [{**j, **f} for j, f in zip(jobs, facts)]
            print(view, len(jobs), 'stages,', sum(f['convex'] for f in facts), 'convex', flush=True)
    json.dump(out, open(os.path.join(HERE, '..', 'stages-facts.json'), 'w'))
    print('done', flush=True)
