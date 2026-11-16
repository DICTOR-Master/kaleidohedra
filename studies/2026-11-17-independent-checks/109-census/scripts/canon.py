"""Independent census, stage B: classes of candidate sets up to the symmetry group; exact zeros.
usage: python canon.py WORLD [start stop]   (chunks of the mask list; results merged by merge.py)"""
import sys, os, time, pickle
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
keys = list(masks.keys())
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
stop = int(sys.argv[3]) if len(sys.argv) > 3 else len(keys)
keys = keys[start:stop]
P = W.PU

def canon_of(idx):
    m = np.zeros((P.shape[0], W.n), bool)
    m[np.repeat(np.arange(P.shape[0]), len(idx)), P[:, idx].ravel()] = True
    pk = np.packbits(m, axis=1)
    o = np.lexsort(pk.T[::-1])
    return pk[o[0]].tobytes()

_r = np.random.default_rng(2026)
W1 = _r.integers(0, 2**63, size=W.n, dtype=np.int64)
W2 = _r.integers(0, 2**63, size=W.n, dtype=np.int64)
def canon_hash(idx):
    # set invariant under the group: (min over images of two independent 64-bit set hashes)
    im = P[:, idx]
    with np.errstate(over='ignore'):
        a = W1[im].sum(1); b = W2[im].sum(1)
    return np.int64(a.min()).tobytes() + np.int64(b.min()).tobytes() + np.int32(len(idx)).tobytes()
HASH = name in ('120', 'E8') or os.environ.get('HASH') == '1'

def work(chunk):
    out = []
    for k in chunk:
        idx = np.where(np.unpackbits(np.frombuffer(k, np.uint8))[:W.n])[0]
        out.append((k, canon_hash(idx) if HASH else canon_of(idx)))
    return out

if __name__ == '__main__':
    log('world', name, 'masks in chunk', len(keys), f'[{start}:{stop}]')
    chunks = [keys[i::480] for i in range(480)]
    res = {}
    with mp.get_context('fork').Pool(24) as pool:
        for i, part in enumerate(pool.imap_unordered(work, chunks)):
            for k, c in part:
                res[k] = c
            if i % 60 == 0: log('chunks done', i + 1, '/', len(chunks))
    pickle.dump(res, open(os.path.join(DATA, ('hashcheck-' if os.environ.get('HASH') == '1' else '') + f'canon-{name}-{start}-{stop}.pkl'), 'wb'))
    log('canonical forms', len(res), 'distinct classes in chunk', len(set(res.values())))
    log('FINAL ok')
