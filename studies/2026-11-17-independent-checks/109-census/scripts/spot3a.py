"""Spot-check of the Table 3a 'unexplained' sets from the independent enumeration.
For each polytope: find the classes of the independent census carrying the listed zero,
report sizes, full zero lists, stabiliser orders, and which [Cm x Cn] / [Cm x Cn].2 /
[C5 x 2T] unions-of-two-orbits produce them."""
import sys, os, json, itertools
import numpy as np
from core import *
from engine import *
from worlds import world

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
ok = True
def stab(W, idx):
    m = np.zeros(W.n, bool); m[idx] = True
    return int(m[W.PU[:, idx]].all(1).sum())

def canon(W, idx):
    m = np.zeros((W.PU.shape[0], W.n), bool)
    m[np.repeat(np.arange(W.PU.shape[0]), len(idx)), W.PU[:, idx].ravel()] = True
    pk = np.packbits(m, axis=1); o = np.lexsort(pk.T[::-1]); return pk[o[0]].tobytes()

def family_unions(W, Lname, L, R, swap=False):
    e = int(np.where(np.all(np.isclose(W.qU, [1, 0, 0, 0]), axis=1))[0][0])
    gens = {int(W.lab2id[l, r, 0]) for l in L for r in R}
    if swap: gens.add(int(W.lab2id[e, e, 1]))
    lab = components(W.n, [W.PU[g] for g in gens])
    orbs = [np.where(lab == o)[0] for o in range(lab.max() + 1)]
    out = {}
    if len(orbs) > 40: return out
    for a, b in itertools.combinations(range(len(orbs)), 2):
        idx = np.concatenate([orbs[a], orbs[b]])
        out.setdefault(canon(W, idx), (Lname, len(orbs[a]), len(orbs[b])))
    return out

def cyclic_subgroups(W):
    mul = W.qmul; n = len(W.qU)
    e = int(np.where(np.all(np.isclose(W.qU, [1, 0, 0, 0]), axis=1))[0][0])
    subs = {}
    for g in range(n):
        S = {e}; x = g
        while x != e:
            S.add(x); x = int(mul[x, g])
        subs.setdefault(len(S), sorted(S))   # one representative per order (all conjugate in 2I)
    return subs

for name, deg in (('600', 8), ('120', 8), ('E8', 4)):
    W = world(name)
    rows = json.load(open(os.path.join(DATA, f'indep-{name}.json')))
    print(f'== {name}: classes with zero {deg}', flush=True)
    hits = [r for r in rows if deg in r['zeros']]
    forced_full = []
    for r in hits:
        if name == 'E8' and r['size'] != 120: continue
        if name == '600' and r['size'] >= 120: continue
        if name == '120' and r['size'] >= 600: continue
        st = stab(W, r['idx'])
        extra = ''
        if name == 'E8':
            a = sum(1 for i in r['idx'] if i < 120); extra = f' shells {a}+{r["size"]-a}'
        print(f'  size {r["size"]} stab {st}{extra} zeros {r["zeros"]} tags {r["tags"]}', flush=True)
        r['stab'] = st
    if name in ('600', '120'):
        C = cyclic_subgroups(W)
        fams = {}
        for m, n in itertools.combinations_with_replacement(sorted(C), 2):
            for (a, b) in ((m, n), (n, m)):
                fams.update(family_unions(W, f'[C{a} x C{b}]', C[a], C[b]))
            if m == n:
                fams.update(family_unions(W, f'[C{m} x C{m}].2', C[m], C[m], swap=True))
        if name == '120':
            # [C5 x 2T]: 2T = the Hurwitz units inside 2I
            T = [i for i in range(120) if np.all(np.isclose(np.abs(W.qU[i]), 0) | np.isclose(np.abs(W.qU[i]), 1) | np.isclose(np.abs(W.qU[i]), 0.5))]
            for a, b, nm in ((C[5], T, '[C5 x 2T]'), (T, C[5], '[2T x C5]'), (C[10], T, '[C10 x 2T]'), (T, C[10], '[2T x C10]')):
                fams.update(family_unions(W, nm, a, b))
        for r in hits:
            if (name == '600' and r['size'] < 120) or (name == '120' and r['size'] < 600):
                c = canon(W, r['idx'])
                print(f'    size {r["size"]}: union of two orbits of {fams.get(c, "NONE of the [Cm x Cn] families")}', flush=True)
print('FINAL ok' if ok else 'FINAL FAIL')
