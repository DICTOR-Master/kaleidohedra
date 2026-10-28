# Hexagonality Law for CdCl2 / CdI2 (two kinds of layer, alternating): the total volume of a role over the gaps of
# one parity p is tested against  T_p = f_p(c) n_c[p] + f_p(h) n_h[p] + g_p(c) n_c[p'] + g_p(h) n_h[p']
# where n_t[q] counts layers of type t and parity q (layer g lies below gap g). Four unknowns, solved exactly from
# all words together; the system has more words than unknowns, so consistency is the test.
# Run on dicto-big-brother: cd ~/kres-tmp/splash2 && ~/geom/bin/python hexlaw_cdi2.py
import os, json
from fractions import Fraction as Fr
import sympy as sp
from hexlaw import words, layer_types, vol_at, RAW, HERE, L
roles = ['S', 'C', 'O', 'Y']
W = [w if len(w) % 2 == 0 else w + w for w in words(6)]
data = {w: json.load(open(os.path.join(RAW, f'cdw_{w}.json'))) for w in W}
cuts = sorted({Fr(iv[x]) for d in data.values() for iv in d['intervals'] for x in ('lo', 'hi') if iv[x] not in (None, 'None')})
out = []; tot = ok_all = 0
for lo, hi in zip(cuts, cuts[1:]):
    win = {'lo': str(lo), 'hi': str(hi), 'roles': {}}
    for r in roles:
        for p in (0, 1):
            rows = []
            for w, d in data.items():
                n = len(w); t = 0; good = True
                for g in range(p, n, 2):
                    v = vol_at(d, g * 4 + roles.index(r), lo, hi)
                    if v is None: good = False; break
                    t += v
                if not good: continue
                lt = layer_types(w)
                c = lambda ty, q: sum(1 for k in range(n) if k % 2 == q and lt[k] == ty)
                rows.append((w, [c('c', p), c('h', p), c('c', 1 - p), c('h', 1 - p)], sp.expand(t)))
            if len(rows) < 5: win['roles'][r + 'fe'[p]] = f'only {len(rows)} words'; continue
            x = sp.symbols('x0:4')
            eqs = [sp.expand(sum(ci * xi for ci, xi in zip(cs, x)) - t) for _, cs, t in rows]
            sol = sp.solve(eqs, x, dict=True)
            good = bool(sol); tot += 1; ok_all += good
            win['roles'][r + 'fe'[p]] = {'words': len(rows), 'consistent': good,
                                         'solution': {str(k): str(sp.factor(v)) for k, v in sol[0].items()} if sol else None}
    out.append(win)
    print(f'({lo}, {hi})', {k: (v['consistent'] if isinstance(v, dict) else v) for k, v in win['roles'].items()}, flush=True)
print('CdI2 parity-split law: consistent', ok_all, 'of', tot)
json.dump(out, open(os.path.join(HERE, 'out', 'hexlaw_cdi2.json'), 'w'), indent=1)
