# Splash Rules run 2: the relay census's Delian (fcc + all tetrahedral holes) and hcp-holes walks against run 1's pure c and pure h
# pieces at s = 1 (data/s_1.json). For every run-1 window inside a relay interval and every role (oct, tet over X, tet under Y): the
# exact ratio run-1 volume / relay volume. A constant in every window means the same volume functions up to the volume unit.
# Usage (on dicto-big-brother, in ~/kres-tmp/splash2): python relay_vs_run1.py > relay_vs_run1.log
import json, sympy as sp
from fractions import Fraction as Fr
s1 = json.load(open('../splash/data/s_1.json'))
for name, ctx in (('delian', '---'), ('hcpholes', '-+-')):
    d = json.load(open(f'raw/{name}.json'))
    for iv in d['intervals']:
        lo, hi = Fr(iv['lo']), Fr(iv['hi']); vols = {}
        for s in iv['sites']:
            if 'volume' in s: vols.setdefault(s['kind'], set()).add(sp.expand(sp.sympify(s['volume'])))
        for w in s1['mix']:
            if lo <= Fr(w) < hi:
                ref = {x['role']: sp.expand(sp.sympify(x['volume'])) for x in s1['mix'][w] if x['ctx'] == ctx}
                for role, k in (('oct', 'oct'), ('tetX', 'tet'), ('tetY', 'tet')):
                    if role in ref: print(name, f'window from {w}', role, 'run1/relay =', [str(sp.cancel(ref[role] / v)) for v in vols.get(k, [])])
