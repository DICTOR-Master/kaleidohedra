"""Probe 2 of the census H4 numbering: bar conventions with (bar, l, r) enumeration order."""
import sys, os, json
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
o = np.array(sorted(range(120), key=lambda i: tuple(s5(c) for c in W.exact[i])))
inv = np.empty(120, int); inv[o] = np.arange(120)
mul, conj = W.qmul, W.qconj; X = np.arange(120)
convs = {
 'l x rbar | l xbar rbar': lambda l, r, b: mul[mul[l, conj[X] if b else X], conj[r]],
 'l x rbar | l xbar r':    lambda l, r, b: mul[mul[l, conj[X]], r] if b else mul[mul[l, X], conj[r]],
 'l x rbar | bar(l x rbar)': lambda l, r, b: conj[mul[mul[l, X], conj[r]]] if b else mul[mul[l, X], conj[r]],
 'l x r | l xbar r':       lambda l, r, b: mul[mul[l, conj[X] if b else X], r],
 'l x r | bar(l x r)':     lambda l, r, b: conj[mul[mul[l, X], r]] if b else mul[mul[l, X], r],
 'lbar x r | lbar xbar r': lambda l, r, b: mul[mul[conj[l], conj[X] if b else X], r],
}
orbs = [s for s in d['sets'] if s['kind'] == 'orbit']
for nm, f in convs.items():
    for order_name, en in (('bar,l,r', [(b, l, r) for b in (0, 1) for l in range(120) for r in range(120)]),
                           ('bar,r,l', [(b, l, r) for b in (0, 1) for r in range(120) for l in range(120)])):
        seen = set(); lst = []
        for b, l, r in en:
            p = inv[f(o[l], o[r], b)[o]]; k = p.tobytes()
            if k not in seen: seen.add(k); lst.append(p)
        good = tot = 0
        for s in orbs:
            for gi in s['groups']:
                gens = d['groups'][gi]['gens']
                lab = components(120, [lst[g] for g in gens]); rep = s['rep']; tot += 1
                if len(set(lab[rep])) == 1 and (lab == lab[rep[0]]).sum() == len(rep): good += 1
        print(f'{nm:28s} {order_name}: {good}/{tot}', flush=True)
