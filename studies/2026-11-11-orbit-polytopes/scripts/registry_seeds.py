"""Exact seeds of the Icosaxes and Unborn Axes from the app's registry, whose corners are stored to about 1e-8: the seed ratios are
recognised exactly in Q(sqrt5) at tolerance 1e-6, and the corners are rebuilt from the exact seed; the worst mismatch is reported.
(The main run, exact_seeds.py, demands 1e-9 and so could not confirm these two.)"""
import json, sys
import numpy as np, sympy as sp
from scipy.spatial import cKDTree
sys.argv = ['x']
import exact_seeds as E
def recog(v):
    c = sp.nsimplify(v, E.SQ, tolerance=1e-6, rational=False)
    return sp.radsimp(c) if abs(float(c) - v) < 1e-6 else None
S = {s['id']: s for s in json.load(open('solids.json'))}
ok = True
for k in ['DICTO_ICOSAXES', 'DICTO_UNBORN_AXES']:
    V = np.unique(np.round(np.array(S[k]['corners'], float), 9), axis=0); V = V - V.mean(0)
    mats = E.sym_group(V); x, simple, Rs = E.chamber_and_roots(V, mats); order, bonds = E.chain_order(simple)
    lab = np.array([simple[i] @ x for i in order]); sc = lab[np.abs(lab) > 1e-9].min(); rel = lab / sc
    ex = [sp.Integer(0) if abs(v) < 1e-9 else recog(float(v)) for v in rel]
    xs = np.linalg.solve(np.array([simple[i] for i in order]), np.array([float(e) for e in ex]) * sc)
    Ms = [np.eye(3) - 2 * np.outer(r, r) for r in Rs]; t = cKDTree(V); orb = [xs]; seen = {tuple(np.round(xs, 6))}; fr = [xs]
    while fr:
        nf = []
        for y in fr:
            for M in Ms:
                z = M @ y; key = tuple(np.round(z, 6))
                if key not in seen: seen.add(key); orb.append(z); nf.append(z)
        fr = nf
    orb = np.array(orb); worst = float(t.query(orb)[0].max()); good = len(orb) == len(V) and worst < 1e-6; ok &= good
    seed = ', '.join(map(str, ex))
    print(f"{S[k]['name']}: chain {bonds}, seed ({seed}), rebuilt {len(orb)} of {len(V)} corners, worst mismatch {worst:.1e}: {'PROOF at the registry precision' if good else 'NOT confirmed'}")
print('FINAL ok' if ok else 'FINAL FAIL')
