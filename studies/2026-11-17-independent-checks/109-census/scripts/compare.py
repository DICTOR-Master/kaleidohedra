"""Compare the independent census with the published census JSONs (run only after the
independent results were logged). usage: python compare.py CENSUS_DIR WORLD
(c) every stored census set: zeros recomputed with the independent tone routine;
(a) every census set located (up to the symmetry group) in the independent family;
(b) counts."""
import sys, os, json, pickle, glob
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
from core import *
from worlds import world

CEN, name = sys.argv[1], sys.argv[2]
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
fname = {'600': 'U600', '120': 'U120', '24': 'U24', 'snub': 'SNUB', 'E8': 'E8'}[name]
d = json.load(open(os.path.join(CEN, f'census-{fname}.json')))
sets = d['sets']
W = world(name)
ok = True

def s5(x):  # Q(phi) pair (a, b) = a + b phi  ->  (rational, sqrt5 coefficient)
    a, b = Fr(x[0]), Fr(x[1])
    return (a + b / 2, b / 2)

# candidate orderings: census index c -> our index order[c]
cands = {}
if name in ('600',):
    cands['sorted, sqrt5 basis'] = sorted(range(120), key=lambda i: tuple(s5(c) for c in W.exact[i]))
elif name == 'snub':
    cands['sorted, sqrt5 basis'] = sorted(range(96), key=lambda i: tuple(s5(c) for c in W.exact[i]))
elif name == '24':
    cands['sorted, sqrt5 basis'] = sorted(range(24), key=lambda i: tuple(s5(c) for c in W.exact[i]))
elif name == '120':
    sc = (2, -1)  # phi^-2 = 2 - phi
    cands['sorted phi^-2 * sum, sqrt5 basis'] = sorted(range(600), key=lambda i: tuple(s5(qmul(c, sc)) for c in W.exact[i]))
    cands['sorted sum, sqrt5 basis'] = sorted(range(600), key=lambda i: tuple(s5(c) for c in W.exact[i]))
elif name == 'E8':
    from universes import build_2I
    D = build_2I()[0]
    u = sorted(range(120), key=lambda i: tuple(s5(c) for c in D[i]))
    cands['units sorted, then phi^-1 units'] = u + [i + 120 for i in u]
    pinv = (-1, 1)
    allp = [(D[i], 0, i) for i in range(120)] + [(tuple(qmul(c, pinv) for c in D[i]), 1, i + 120) for i in range(120)]
    cands['all 240 sorted, sqrt5 basis'] = [p[2] for p in sorted(allp, key=lambda p: tuple(s5(c) for c in p[0]))]

best = None
for cn, order in cands.items():
    o = np.array(order)
    good = sum(1 for s in sets if W.T.zeros(o[s['rep']]) == s['zeros'])
    print(f'ordering "{cn}": zero lists agree on {good}/{len(sets)} census sets', flush=True)
    if best is None or good > best[1]:
        best = (cn, good, o)
cn, good, o = best
print(f'(c) using ordering "{cn}": {good}/{len(sets)} census zero lists reproduced exactly')
mism = [(i, s['size'], s['zeros'], W.T.zeros(o[s['rep']])) for i, s in enumerate(sets) if W.T.zeros(o[s['rep']]) != s['zeros']]
for m in mism[:20]:
    print('   MISMATCH set', m)
if mism: ok = False

# (a)/(b): locate census sets in the independent family, up to the symmetry group
P = W.PU
def canon_exact(idx):
    m = np.zeros((P.shape[0], W.n), bool)
    m[np.repeat(np.arange(P.shape[0]), len(idx)), P[:, idx].ravel()] = True
    pk = np.packbits(m, axis=1); oo = np.lexsort(pk.T[::-1]); return pk[oo[0]].tobytes()
_r = np.random.default_rng(2026)
W1 = _r.integers(0, 2**63, size=W.n, dtype=np.int64)
W2 = _r.integers(0, 2**63, size=W.n, dtype=np.int64)
def canon_hash(idx):
    im = P[:, idx]
    with np.errstate(over='ignore'):
        a = W1[im].sum(1); b = W2[im].sum(1)
    return np.int64(a.min()).tobytes() + np.int64(b.min()).tobytes() + np.int32(len(idx)).tobytes()
canon = canon_hash if name in ('120', 'E8') else canon_exact

mine = {}
for fn in glob.glob(os.path.join(DATA, f'canon-{name}-*.pkl')):
    mine.update(pickle.load(open(fn, 'rb')))
masks = pickle.load(open(os.path.join(DATA, f'masks-{name}.pkl'), 'rb'))
mytags = {}
for k, c in mine.items():
    mytags.setdefault(c, set()).add(masks[k])
indep = json.load(open(os.path.join(DATA, f'indep-{name}.json')))

cc = [canon(o[np.array(s['rep'])]) for s in sets]
print(f'(b) census sets: {len(sets)} stored; distinct up to the symmetry group: {len(set(cc))}')
dup = Counter(cc); nd = sum(v - 1 for v in dup.values() if v > 1)
if nd: print(f'    {nd} census sets are images of other census sets under the group')
found = [c in mytags for c in cc]
byk = Counter((s['kind'], f) for s, f in zip(sets, found))
print(f'(a) census sets found in the independent family: {sum(found)}/{len(sets)}  by kind: {dict(byk)}')
for s, f in zip(sets, found):
    if not f:
        print(f'    NOT FOUND: kind {s["kind"]} size {s["size"]} zeros {s["zeros"]} groups {s["groups"][:4]}')
cset = set(cc)
myall = set(mytags)
fam2 = {c for c, t in mytags.items() if t & {'orbit', 'union2'}}
print(f'    independent classes: {len(myall)} (orbit or union of two orbits: {len(fam2)}); '
      f'of these in the census: {len(myall & cset)} ({len(fam2 & cset)})')
# zeros of independent sets with an 'OPEN' style degree: list independent classes NOT in census that carry
# a degree-8 zero (600/120) or degree-4 zero (E8 120-root) -- for information
orb = {c for c, t in mytags.items() if 'orbit' in t}
print(f'    independent single-orbit classes: {len(orb)}; of these in the census: {len(orb & cset)}')
miss = Counter()
for r in indep:
    pass
print('FINAL ok' if ok else 'FINAL FAIL zero-list mismatch')
