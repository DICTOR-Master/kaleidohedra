"""Probe candidate point orderings of the 120-cell against the census zero lists (first 300 sets)."""
import sys, os, json
from fractions import Fraction as Fr
import numpy as np
from core import *
from worlds import world

CEN = sys.argv[1]
sets = json.load(open(os.path.join(CEN, 'census-U120.json')))['sets'][:300]
W = world('120')
def s5(x):
    a, b = Fr(x[0]), Fr(x[1]); return (a + b / 2, b / 2)
pts = {}
pts['sum'] = W.exact
pts['phi^-2 sum'] = [tuple(qmul(c, (2, -1)) for c in p) for p in W.exact]
pts['phi^-2 sum / 2'] = [tuple((Fr(a, 2), Fr(b, 2)) for a, b in p) for p in pts['phi^-2 sum']]
pts['phi^-1 sum'] = [tuple(qmul(c, (-1, 1)) for c in p) for p in W.exact]
pts['phi^-3 sum'] = [tuple(qmul(qmul(c, (2, -1)), (-1, 1)) for c in p) for p in W.exact]
keys = {
    'sqrt5 basis': lambda p: tuple(s5(c) for c in p),
    'phi basis': lambda p: tuple((Fr(c[0]), Fr(c[1])) for c in p),
    'float': lambda p: tuple(qfloat(c) for c in p),
}
res = []
for pn, P in pts.items():
    for kn, kf in keys.items():
        for rev in (False, True):
            o = np.array(sorted(range(600), key=lambda i: kf(P[i]), reverse=rev))
            good = sum(1 for s in sets if W.T.zeros(o[s['rep']]) == s['zeros'])
            res.append((good, pn, kn, rev))
            print(f'{good:4d}/300  points {pn:16s} key {kn:12s} reverse {rev}', flush=True)
# also: cells in lexicographic order of their sorted corner indices (corners in census 600-cell order)
D_order = sorted(range(120), key=lambda i: tuple(s5(c) for c in world('600').exact[i]))
rank = np.empty(120, int); rank[D_order] = np.arange(120)
for nm, kf in (('cells by sorted corner ranks', lambda c: tuple(sorted(rank[list(c)]))),):
    o = np.array(sorted(range(600), key=lambda i: kf(W.cells[i])))
    good = sum(1 for s in sets if W.T.zeros(o[s['rep']]) == s['zeros'])
    print(f'{good:4d}/300  {nm}', flush=True)
