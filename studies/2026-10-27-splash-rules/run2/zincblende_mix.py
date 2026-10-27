# Splash Rules run 2, zinc blende / wurtzite (DICTO 2026-10-28, 'continue on zinc blende'): run 1's c/h test with two kinds of atom:
# balls S weight lam, the second atom Zn in the tetrahedral sites C weight lam + MU (MU fixed, from the environment), empty holes O + Y
# weight 0 (3C = zinc blende, 2H = wurtzite; MU = 0 is the pyrochlore / diamond run); copied from pyro_mix.py, only the kinds changed; ~/kres-tmp/pyro/pyro_walk.py net, #57's census engine unchanged, exact rational arithmetic).
# Words: every primitive close-packed stacking up to 6 layers, up to symmetry (as scripts/splash.py). For each lam-window:
#   LOCALITY: role + the 3 layer steps round the piece's gap (4 layers) fixes the exact volume (clash count);
#   HALVES:   each volume = a V(pure c) + b V(pure h), constant rational a, b (coefficient matching in lam);
#   SWAP:     V(c under h) + V(h under c) = V(c under c) + V(h under h), per role (types of the gap's lower and upper layer);
#   END:      V(h)/V(c) and V(Janus)/V(c) constant in the window.
# Usage: pyro_mix.py walk <word>   -> raw/pyw_<word>.json      pyro_mix.py mix   -> out/pyro_mix.json + report
import sys, os, json, itertools, io, contextlib
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
MU = Fr(os.environ.get('MU', '1/20')); TAG = 'zb' + str(MU).replace('/', 'o').replace('-', 'm')
def words(maxlen):                                    # copied from scripts/splash.py
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
def steps(word): n = len(word); return [STEP[(word[k], word[(k + 1) % n])] for k in range(n)]
ROLE = ['S', 'C', 'O', 'Y']                             # motif order per gap in pyro_walk.net_for
if sys.argv[1] == 'walk':
    E57 = os.path.expanduser('~/kres-tmp/st57/scripts'); sys.path.insert(0, E57); os.chdir(E57)
    sys.path.insert(0, os.path.expanduser('~/kres-tmp/pyro')); from pyro_walk import net_for
    _nf = net_for
    def net_for(w):                                    # same motif and order (S, C, O, Y); C becomes the second atom 'zn'
        d = _nf(w); kinds = ['atom', 'zn', 'hole', 'hole']
        d['motif'] = [(kinds[i % 4], p) for i, (_, p) in enumerate(d['motif'])]; d['w'] = dict(d['w'], zn=(MU, 1))
        d['name'] = f'zinc blende / wurtzite stacking {w}, MU {MU}'; return d
    import networks, census
    w = sys.argv[2]; key = TAG + '_' + w; networks.NETS[key] = net_for(w); census.NETS[key] = networks.NETS[key]
    C = census.Census(key)
    with contextlib.redirect_stdout(io.StringIO()): d = C.walk()
    fails = [c for c in C.checks if c[0] != 'PASS']; d['_w'] = w; d['_fails'] = len(fails)
    os.makedirs(os.path.join(HERE, 'raw'), exist_ok=True)
    json.dump(d, open(os.path.join(HERE, 'raw', f'{TAG}_{w}.json'), 'w'), indent=1, default=str)
    print(w, len(d['intervals']), 'intervals, census checks failed:', len(fails), flush=True); sys.exit()
import sympy as sp
L = sp.Symbol('lam')
W = words(6); data = {w: json.load(open(os.path.join(HERE, 'raw', f'{TAG}_{w}.json'))) for w in W}
print('words', W, '| census checks failed:', {w: d['_fails'] for w, d in data.items()})
cuts = sorted({Fr(iv[x]) for d in data.values() for iv in d['intervals'] for x in ('lo', 'hi') if iv[x] not in (None, 'None')})
wins = list(zip(cuts, cuts[1:]))
def vol_at(d, i, lo, hi):
    for iv in d['intervals']:
        if Fr(iv['lo']) <= lo and hi <= Fr(iv['hi']):
            x = iv['sites'][i]
            return 0 if x.get('vanished') or 'volume' not in x else sp.expand(len(d['_w']) * sp.sympify(x['volume']).subs('lam', L))
    return None                                         # this word's walk does not reach the window
def ty(a, b): return 'c' if a == b else 'h'
res = {'words': W, 'windows': []}; clashes = 0
for lo, hi in wins:
    table = {}                                          # (role, ctx) -> volume, ctx = mirror-merged 3 steps round the gap
    for w, d in data.items():
        st = steps(w); n = len(w)
        for i in range(4 * n):
            v = vol_at(d, i, lo, hi)
            if v is None: continue
            g = i // 4; ctx = (st[(g - 1) % n], st[g], st[(g + 1) % n]); ctx = min(ctx, tuple(-x for x in ctx))
            k = (ROLE[i % 4], ctx)
            if k in table and sp.expand(table[k] - v) != 0: clashes += 1; print('  CLASH', lo, hi, k, w)
            table.setdefault(k, v)
    win = {'lo': str(lo), 'hi': str(hi), 'roles': {}}
    for role in ROLE:
        T = {}                                          # (lower layer type, upper layer type) -> volume
        for (r, ctx), v in table.items():
            if r != role: continue
            key = ty(ctx[0], ctx[1]) + ty(ctx[1], ctx[2])
            if key in T and sp.expand(T[key] - v) != 0: clashes += 1; print('  CLASH (layer types)', lo, hi, role, key)
            T.setdefault(key, v)
        if not all(k in T for k in ('cc', 'hh')): win['roles'][role] = 'pure piece missing'; continue
        out = {'volumes': {k: str(sp.factor(v)) for k, v in sorted(T.items())}}
        a, b = sp.symbols('a b'); fits = {}
        for k in ('ch', 'hc'):
            if k not in T: continue
            sol = sp.solve(sp.Poly(sp.expand(a * T['cc'] + b * T['hh'] - T[k]), L).all_coeffs(), [a, b], dict=True)
            fits[k] = 'none' if not sol else {s.name: str(val) for s, val in sol[0].items()}
        out['fit'] = fits
        if 'ch' in T and 'hc' in T: out['swap'] = sp.expand(T['ch'] + T['hc'] - T['cc'] - T['hh']) == 0
        if T['cc'] != 0:
            out['end'] = {k: (str(r) if not (r := sp.cancel(T[k] / T['cc'])).free_symbols else 'varies') for k in T if k != 'cc'}
        win['roles'][role] = out
    res['windows'].append(win)
    print(f'({lo}, {hi})')
    for role, o in win['roles'].items():
        print(f'   {role}:', o if isinstance(o, str) else f"fit {o['fit']} | swap {o.get('swap')} | ratio to pure c {o.get('end')}")
res['clashes'] = clashes; print('locality clashes (4 layers round the gap):', clashes)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); json.dump(res, open(os.path.join(HERE, 'out', f'{TAG}_mix.json'), 'w'), indent=1)
