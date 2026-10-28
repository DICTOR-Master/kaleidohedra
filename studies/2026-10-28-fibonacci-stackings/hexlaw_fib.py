# Hexagonality Law on the Fibonacci approximants (Laves phases, every role incl. the foot atom M0): total of each role over one
# period = n_c T(ABC)/3 + n_h T(AC)/2, exactly, in every lam-window. Words given on the command line (those with finished walks).
import os, sys, json
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, os.path.expanduser('~/kres-tmp/splash2'))
import hexlaw as H
roles = ['M0', 'M1', 'K1', 'K2', 'K3', 'T']
W = sys.argv[1:]
data = {w: json.load(open(os.path.join(H.RAW, f'lvw_{w}.json'))) for w in W + ['ABC', 'AC']}
cuts = sorted({Fr(iv[x]) for d in data.values() for iv in d['intervals'] for x in ('lo', 'hi') if iv[x] not in (None, 'None')})
tot = ok = 0; fails = []
for lo, hi in zip(cuts, cuts[1:]):
    for r in roles:
        T = {}
        for w, d in data.items():
            t = sp.Integer(0); good = True
            for g in range(len(w)):
                v = H.vol_at(d, g * 6 + roles.index(r), lo, hi)
                if v is None: good = False; break
                t += v
            if good: T[w] = t
        if 'ABC' not in T or 'AC' not in T: continue
        for w in W:
            if w not in T: continue
            lt = H.layer_types(w); g = sp.expand(T[w] - lt.count('c') * T['ABC'] / 3 - lt.count('h') * T['AC'] / 2) == 0
            tot += 1; ok += g
            if not g: fails.append((str(lo), str(hi), r, w))
print('Fibonacci approximants', W, ':', ok, 'of', tot, 'exact; fails', fails)
