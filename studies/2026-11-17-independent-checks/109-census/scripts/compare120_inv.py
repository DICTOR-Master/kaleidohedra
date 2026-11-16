"""120-cell comparison without the census point ordering (the JSON stores no coordinates and its
120-cell ordering is not a coordinate sort): match census sets to independent classes by the
group-invariant triple (size, exact zero list, stabiliser order in H4).
usage: python compare120_inv.py CENSUS_DIR"""
import sys, os, json
from collections import Counter
import numpy as np
import multiprocessing as mp
from core import *
from worlds import world

CEN = sys.argv[1]
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
W = world('120'); P = W.PU
mine = json.load(open(os.path.join(DATA, 'indep-120.json')))
cen = json.load(open(os.path.join(CEN, 'census-U120.json')))['sets']

def stab(i):
    idx = np.array(mine[i]['idx']); m = np.zeros(W.n, bool); m[idx] = True
    return int(m[P[:, idx]].all(1).sum())

if __name__ == '__main__':
    with mp.get_context('fork').Pool(24) as pool:
        st = pool.map(stab, range(len(mine)), chunksize=200)
    myinv = Counter((r['size'], tuple(r['zeros']), s) for r, s in zip(mine, st))
    fam = Counter((r['size'], tuple(r['zeros']), s) for r, s in zip(mine, st) if set(r['tags']) & {'orbit', 'union2'})
    ceninv = Counter((s['size'], tuple(s['zeros']), s['stab_order']) for s in cen)
    found = sum(v for k, v in ceninv.items() if k in myinv)
    print(f'census 120-cell sets: {len(cen)}; distinct invariant triples (size, zeros, stabiliser): {len(ceninv)}')
    print(f'census sets whose triple occurs among the independent classes: {found}/{len(cen)}')
    over = sum(1 for k, v in ceninv.items() if k in myinv and v > myinv[k])
    print(f'triples where the census has more sets than the independent family has classes: {over}')
    for k, v in ceninv.items():
        if k not in myinv: print('   NOT FOUND triple', k, 'x', v)
        elif v > myinv[k]: print('   census count', v, '> independent', myinv[k], 'for', k)
    print(f'independent classes: {len(mine)}, distinct triples: {len(myinv)}')
    orbinv = Counter((r['size'], tuple(r['zeros']), s) for r, s in zip(mine, st) if 'orbit' in r['tags'])
    print(f'independent single-orbit classes: {sum(orbinv.values())}; their triples present in the census: '
          f'{sum(v for k, v in orbinv.items() if k in ceninv)}; census sets of kind orbit: {sum(1 for s in cen if s["kind"] == "orbit")}')
    print('FINAL ok' if found == len(cen) and over == 0 else 'FINAL FAIL see above')
