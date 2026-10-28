# Hexagonality Law for the Laves phases on every close-packed stacking up to EIGHT layers (15 words), every lam-window, every role,
# including the foot atom M0, which above lam = 17/96 reads three layer types (#64) and for which the law is not proved (#66).
# Run on dicto-big-brother: cd ~/kres-tmp/splash2 && ~/geom/bin/python hexlaw_laves8.py
import os, json
from fractions import Fraction as Fr
import sympy as sp
import hexlaw as H
roles = ['M0', 'M1', 'K1', 'K2', 'K3', 'T']
W = H.words(8)
data = {w: json.load(open(os.path.join(H.RAW, f'lvw_{w}.json'))) for w in W}
cuts = sorted({Fr(iv[x]) for d in data.values() for iv in d['intervals'] for x in ('lo', 'hi') if iv[x] not in (None, 'None')})
tot = ok = 0; fails = []; out = []
for lo, hi in zip(cuts, cuts[1:]):
    win = {'lo': str(lo), 'hi': str(hi), 'roles': {}}
    for r in roles:
        T = {}
        for w, d in data.items():
            n = len(w); t = sp.Integer(0); good = True
            for g in range(n):
                v = H.vol_at(d, g * 6 + roles.index(r), lo, hi)
                if v is None: good = False; break
                t += v
            if good: T[w] = t
        if 'ABC' not in T or 'AC' not in T: continue
        a = T['ABC'] / 3; b = T['AC'] / 2
        res = {}
        for w in T:
            if w in ('ABC', 'AC'): continue
            lt = H.layer_types(w); nc, nh = lt.count('c'), lt.count('h')
            g = sp.expand(T[w] - nc * a - nh * b) == 0
            res[w] = g; tot += 1; ok += g
            if not g: fails.append((str(lo), str(hi), r, w))
        win['roles'][r] = res
    out.append(win)
print('Laves, words up to 8 layers:', ok, 'of', tot, 'linear in the hexagonality; fails:', fails[:20])
m0 = [(w['lo'], w['hi'], all(w['roles'].get('M0', {}).values()), len(w['roles'].get('M0', {}))) for w in out]
print('M0 by window (lo, hi, all linear, words tested):', m0)
json.dump({'tests': tot, 'pass': ok, 'fails': fails, 'windows': out}, open(os.path.join(H.HERE, 'out', 'hexlaw_laves8.json'), 'w'), indent=1)
