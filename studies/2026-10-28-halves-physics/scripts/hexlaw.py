# Hexagonality Law check (DICTO 10-28, halves physics): for every family of the Splash Rules run 2 (#60, #64), every
# lam-window and every role, is the total volume of that role over one period of a stacking exactly
#     T(word) = n_c * alpha(lam) + n_h * beta(lam)
# (n_c, n_h = numbers of cubic and hexagonal layers in the period), i.e. linear in the hexagonality n_h / n?
# alpha from the pure cubic stacking ABC, beta from the pure hexagonal AC; every other word is a test.
# Reads the raw weight walks of run 2 (exact rational volumes, polynomials in lam). Run on dicto-big-brother:
#   cd ~/kres-tmp/splash2 && ~/geom/bin/python hexlaw.py
import os, json, itertools
from fractions import Fraction as Fr
import sympy as sp
L = sp.Symbol('lam')
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw')
def words(maxlen):                                    # as splash.py / the run 2 scripts
    seen, out = set(), []
    for n in range(2, maxlen + 1):
        for st in itertools.product((1, -1), repeat=n):
            if sum(st) % 3: continue
            if any(st[i:] + st[:i] < st for i in range(n)): continue
            if any(n % p == 0 and st == st[:p] * (n // p) and sum(st[:p]) % 3 == 0 for p in range(1, n)): continue
            key = min(tuple(st[i:] + st[:i]) for i in range(n)); mk = min(tuple(-x for x in st[i:] + st[:i]) for i in range(n))
            if min(key, mk) in seen: continue
            seen.add(min(key, mk)); w = 'A'
            for x in st[:-1]: w += 'ABC'[('ABC'.index(w[-1]) + x) % 3]
            out.append(w)
    return out
STEP = {('A', 'B'): 1, ('B', 'C'): 1, ('C', 'A'): 1, ('B', 'A'): -1, ('C', 'B'): -1, ('A', 'C'): -1}
def steps(w): n = len(w); return [STEP[(w[k], w[(k + 1) % n])] for k in range(n)]
def layer_types(w): st = steps(w); n = len(w); return ['c' if st[k - 1] == st[k] else 'h' for k in range(n)]
W6 = words(6)
FAM = [  # name, raw prefix, roles per gap, words, parity-split roles
    ('pyrochlore (#60)', 'pyw', ['S', 'C', 'O', 'Y'], W6, False),
    ('rock salt / NiAs (#64)', 'rsw', ['S', 'C', 'O', 'Y'], W6, False),
    ('CdCl2 / CdI2 (#64)', 'cdw', ['S', 'C', 'O', 'Y'], [w if len(w) % 2 == 0 else w + w for w in W6], True),
    ('zinc blende MU=1/20 (#64)', 'zb1o20', ['S', 'C', 'O', 'Y'], W6, False),
    ('zinc blende MU=1/10 (#64)', 'zb1o10', ['S', 'C', 'O', 'Y'], W6, False),
    ('zinc blende MU=-1/20 (#64)', 'zbm1o20', ['S', 'C', 'O', 'Y'], W6, False),
    ('zinc blende MU=-1/10 (#64)', 'zbm1o10', ['S', 'C', 'O', 'Y'], W6, False),
    ('Laves (#64)', 'lvw', ['M0', 'M1', 'K1', 'K2', 'K3', 'T'], W6, False),
]
def vol_at(d, i, lo, hi):
    for iv in d['intervals']:
        if iv['lo'] in (None, 'None') or iv['hi'] in (None, 'None'): continue
        if Fr(iv['lo']) <= lo and hi <= Fr(iv['hi']):
            x = iv['sites'][i]
            return sp.Integer(0) if x.get('vanished') or 'volume' not in x else sp.expand(len(d['_w']) * sp.sympify(x['volume']).subs('lam', L))
    return None
report = {}; grand = {'tests': 0, 'pass': 0, 'fail': 0}
for name, pre, roles, W, par in FAM:
    data = {w: json.load(open(os.path.join(RAW, f'{pre}_{w}.json'))) for w in W}
    cuts = sorted({Fr(iv[x]) for d in data.values() for iv in d['intervals'] for x in ('lo', 'hi') if iv[x] not in (None, 'None')})
    fam = {'windows': []}; ft = fp = ff = 0
    pc, ph = ('ABCABC', 'AC') if par else ('ABC', 'AC')
    for lo, hi in zip(cuts, cuts[1:]):
        win = {'lo': str(lo), 'hi': str(hi), 'roles': {}}
        rk = roles if not par else [r + p for r in roles for p in 'fe']
        for role in rk:
            T = {}
            for w, d in data.items():
                n = len(w); k = len(roles); tot = sp.Integer(0); ok = True
                for g in range(n):
                    if par and 'fe'[g % 2] != role[-1]: continue
                    v = vol_at(d, g * k + roles.index(role[:-1] if par else role), lo, hi)
                    if v is None: ok = False; break
                    tot += v
                if ok: T[w] = tot
            if pc not in T or ph not in T: win['roles'][role] = 'pure stacking missing'; continue
            lt = {w: layer_types(w) for w in T}
            if par:   # count layer types by parity of the layer (layer g sits below gap g)
                cnt = {w: (sum(1 for g, t in enumerate(lt[w]) if t == 'c' and 'fe'[g % 2] == role[-1]),
                           sum(1 for g, t in enumerate(lt[w]) if t == 'h' and 'fe'[g % 2] == role[-1])) for w in T}
            else:
                cnt = {w: (lt[w].count('c'), lt[w].count('h')) for w in T}
            a = sp.expand(T[pc] / cnt[pc][0]); b = sp.expand(T[ph] / cnt[ph][1])
            res = {}
            for w in T:
                if w in (pc, ph): continue
                nc, nh = cnt[w]; ok = sp.expand(T[w] - nc * a - nh * b) == 0
                res[w] = ok; ft += 1; fp += ok; ff += (not ok)
            win['roles'][role] = {'alpha': str(sp.factor(a)), 'beta': str(sp.factor(b)), 'tests': res}
        fam['windows'].append(win)
    fam['summary'] = {'tests': ft, 'pass': fp, 'fail': ff}; report[name] = fam
    grand['tests'] += ft; grand['pass'] += fp; grand['fail'] += ff
    print(f'{name}: {fp}/{ft} words linear in hexagonality', flush=True)
    for win in fam['windows']:
        bad = {r: [w for w, ok in o['tests'].items() if not ok] for r, o in win['roles'].items() if isinstance(o, dict) and not all(o['tests'].values())}
        if bad: print(f'   window ({win["lo"]}, {win["hi"]}) fails: {bad}')
report['grand'] = grand; print('TOTAL', grand)
json.dump(report, open(os.path.join(HERE, 'out', 'hexlaw.json'), 'w'), indent=1)
