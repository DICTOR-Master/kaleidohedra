"""Diagnose census 'twisted' sets that are not in the independent family: is some image of the
set under the symmetry group a union of twisted classes of one of our (G, alpha) partitions,
and of how many classes?  usage: python diag_tw.py CENSUS_DIR WORLD"""
import sys, os, json, pickle
from fractions import Fraction as Fr
import numpy as np
import multiprocessing as mp
from core import *
from worlds import world

CEN, name = sys.argv[1], sys.argv[2]
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
W = world(name)
fname = {'600': 'U600', 'snub': 'SNUB'}[name]
sets = json.load(open(os.path.join(CEN, f'census-{fname}.json')))['sets']
def s5(x):
    a, b = Fr(x[0]), Fr(x[1]); return (a + b / 2, b / 2)
o = np.array(sorted(range(W.n), key=lambda i: tuple(s5(c) for c in W.exact[i])))
P = W.PU
def canon_exact(idx):
    m = np.zeros((P.shape[0], W.n), bool)
    m[np.repeat(np.arange(P.shape[0]), len(idx)), P[:, idx].ravel()] = True
    pk = np.packbits(m, axis=1); oo = np.lexsort(pk.T[::-1]); return pk[oo[0]].tobytes()
import glob
mine = set()
for fn in glob.glob(os.path.join(DATA, f'canon-{name}-*.pkl')):
    mine |= set(pickle.load(open(fn, 'rb')).values())
missing = [s for s in sets if canon_exact(o[np.array(s['rep'])]) not in mine]
tw = pickle.load(open(os.path.join(DATA, f'partitions-{name}.pkl'), 'rb'))['tw']
print('missing census sets:', len(missing), ' twisted partitions:', len(tw), flush=True)

def test(si):
    s = missing[si]; idx = o[np.array(s['rep'])]
    M = np.zeros((P.shape[0], W.n), np.float32)
    M[np.repeat(np.arange(P.shape[0]), len(idx)), P[:, idx].ravel()] = 1
    best = None
    for t, (tag, nL, cl) in enumerate(tw):
        k = len(cl)
        H = np.zeros((W.n, k), np.float32)
        for c, members in enumerate(cl): H[members, c] = 1
        cnt = M @ H; sz = H.sum(0)
        good = np.all((cnt == 0) | (cnt == sz), axis=1)
        if good.any():
            r = int((cnt[np.argmax(good)] > 0).sum())
            if best is None or r < best[0]:
                best = (r, k, nL)
    return s['size'], s['zeros'], best

with mp.get_context('fork').Pool(24) as pool:
    res = pool.map(test, range(len(missing)))
from collections import Counter
summary = Counter()
for size, z, b in res:
    print(f'  size {size:3d} zeros {z}: ' + (f'union of {b[0]} classes of a partition with {b[1]} classes (|G| = {b[2]})' if b else 'NOT a union of classes of any of our twisted partitions'))
    summary[('union' if b else 'none', b[0] if b else None, b[1] > 9 if b else None)] += 1
print('summary (kind, #classes, partition has >9 classes):', dict(summary))
ok = all(b for _, _, b in res)
print('FINAL ok' if ok else 'FINAL FAIL some census sets are not unions of our twisted classes')
