"""Independent census, stage C: merge canonical chunks, exact zeros per class, summary.
usage: python merge.py WORLD"""
import sys, os, glob, json, pickle, time
from collections import Counter, defaultdict
import numpy as np
import multiprocessing as mp
from core import *
from worlds import world

name = sys.argv[1]
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
t0 = time.time()
def log(*a): print(f'[{time.time()-t0:7.1f}s]', *a, flush=True)
W = world(name)
masks = pickle.load(open(os.path.join(DATA, f'masks-{name}.pkl'), 'rb'))
canon = {}
for fn in sorted(glob.glob(os.path.join(DATA, f'canon-{name}-*.pkl'))):
    canon.update(pickle.load(open(fn, 'rb')))
assert set(canon) == set(masks), (len(canon), len(masks))
cls = defaultdict(set); REP = {}
for k, c in canon.items():
    cls[c].add(masks[k])
    if c not in REP or k < REP[c]: REP[c] = k
log('masks', len(masks), 'classes up to the symmetry group', len(cls))

def zeros_of(c):
    rep = min(cls[c + b'']) if False else c
    k0 = REP[c]
    idx = np.where(np.unpackbits(np.frombuffer(k0, np.uint8))[:W.n])[0]
    return c, idx.tolist(), W.T.zeros(idx)

if __name__ == '__main__':
    with mp.get_context('fork').Pool(24) as pool:
        res = pool.map(zeros_of, list(cls), chunksize=50)
    out = []
    for c, idx, z in res:
        out.append({'size': len(idx), 'idx': idx, 'zeros': z, 'tags': sorted(cls[c])})
    out.sort(key=lambda r: (r['size'], r['idx']))
    json.dump(out, open(os.path.join(DATA, f'indep-{name}.json'), 'w'))
    tagc = Counter(tuple(r['tags']) for r in out)
    log('classes by provenance tags:', dict(tagc))
    fam = [r for r in out if set(r['tags']) & {'orbit', 'union2'}]
    log('classes that are an orbit or a union of two orbits:', len(fam))
    log('classes with at least one zero (k<=20):', sum(1 for r in out if r['zeros']))
    sig = Counter(tuple(r['zeros']) for r in out)
    log('distinct zero signatures:', len(sig))
    log('classes with zero at 8:', sum(1 for r in out if 8 in r['zeros']))
    for r in out:
        if 8 in r['zeros'] and r['size'] < 120:
            print('   deg-8 set: size', r['size'], 'zeros', r['zeros'], 'tags', r['tags'])
    log('FINAL ok')
