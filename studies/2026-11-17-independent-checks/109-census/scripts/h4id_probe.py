"""Probe the census numbering of H4 elements (from its stored generator ids) by testing
natural enumerations of the maps x -> l x rbar, l xbar rbar against the stored 600-cell orbits."""
import sys, os, json, itertools
from fractions import Fraction as Fr
import numpy as np
from core import *
from engine import *
from worlds import world
CEN = sys.argv[1]
d = json.load(open(os.path.join(CEN, 'census-U600.json')))
W = world('600')
def s5(x):
    a, b = Fr(x[0]), Fr(x[1]); return (a + b / 2, b / 2)
order = sorted(range(120), key=lambda i: tuple(s5(c) for c in W.exact[i]))   # census idx -> ours
o = np.array(order); inv = np.empty(120, int); inv[o] = np.arange(120)
mul, conj = W.qmul, W.qconj
X = np.arange(120)
def perm(l, r, b):  # ours: x -> l x rbar  (indices ours), returned in census indexing
    xs = conj[X] if b else X
    p = mul[mul[l, xs], conj[r]]
    # census indexing: c -> inv[p[o[c]]]
    return inv[p[o]]
orbs = [s for s in d['sets'] if s['kind'] == 'orbit']
def test(enum):
    seen = {}; lst = []
    for (l, r, b) in enum:
        p = perm(l, r, b); k = p.tobytes()
        if k not in seen:
            seen[k] = len(lst); lst.append(p)
    good = 0; tot = 0
    for s in orbs[:60]:
        for gi in s['groups'][:2]:
            gens = d['groups'][gi]['gens']
            lab = components(120, [lst[g] for g in gens])
            rep = s['rep']; tot += 1
            if len(set(lab[rep])) == 1 and (lab == lab[rep[0]]).sum() == len(rep): good += 1
    return good, tot
C = [o[c] for c in range(120)]   # quaternions in census order (our indices)
variants = {
 'bar,l,r': [(C[l], C[r], b) for b in (0, 1) for l in range(120) for r in range(120)],
 'bar,r,l': [(C[l], C[r], b) for b in (0, 1) for r in range(120) for l in range(120)],
 'l,r,bar': [(C[l], C[r], b) for l in range(120) for r in range(120) for b in (0, 1)],
 'r,l,bar': [(C[l], C[r], b) for r in range(120) for l in range(120) for b in (0, 1)],
}
for nm, en in variants.items():
    for conv in ('l x rbar', 'l x r'):
        en2 = en if conv == 'l x rbar' else [(l, int(conj[r]), b) for l, r, b in en]
        print(nm, conv, test(en2), flush=True)
# sorted permutation lists
allp = {}
for (l, r, b) in variants['bar,l,r']:
    p = perm(l, r, b); allp[p.tobytes()] = p
P = sorted(allp.values(), key=lambda p: tuple(p))
def test_list(lst):
    good = tot = 0
    for s in orbs[:60]:
        for gi in s['groups'][:2]:
            gens = d['groups'][gi]['gens']
            lab = components(120, [lst[g] for g in gens]); rep = s['rep']; tot += 1
            if len(set(lab[rep])) == 1 and (lab == lab[rep[0]]).sum() == len(rep): good += 1
    return good, tot
print('sorted perms (image lists)', test_list(P), flush=True)
Pi = sorted(allp.values(), key=lambda p: tuple(perm_inverse(p[None])[0]))
print('sorted perms (inverse lists)', test_list(Pi), flush=True)
