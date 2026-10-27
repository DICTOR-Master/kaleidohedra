# Splash Rules, run 1 (DICTO 2026-10-27): look for simple rules (halves, thirds, ...) in tables of computed piece volumes.
# Family: the #57 weight walk on the holes of close-packed stackings, with the layer spacing scaled, d^2 = s * 2/3 (s = 1 is #57).
# For each stacking word and each lambda-window: every hole piece (oct over the third position, tet over the lower layer X, tet under
# the upper layer Y) gets a label = its role + the layer steps (+1/-1 mod 3) within r gaps of its own gap, up to the mirror (all signs).
# (1) LOCALITY: the smallest r for which the label fixes the exact volume polynomial in every window, over all words.
# (2) MIX: each label's volume as a*V(pure c) + b*V(pure h) with constant rational a, b (pure c = ABC, pure h = AB), exact.
# Usage: python splash.py <s> [maxlen]   ->  ../data/s_<s>.json
import sys, os, json, itertools
sys.path.insert(0, os.path.expanduser('~/kres-tmp/st57/scripts')); os.chdir(os.path.expanduser('~/kres-tmp/st57/scripts'))
from fractions import Fraction as Fr
import sympy as sp
import census, networks
POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
L = sp.Symbol('lam')
def net_for(word, s):
    n = len(word); motif = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        z = lambda f: Fr(k, n) + f / n
        motif += [('oct', (*POS[Z], z(Fr(1, 2)))), ('tet', (*POS[X], z(Fr(3, 4)))), ('tet', (*POS[Y], z(Fr(1, 4))))]
    G = [[1, Fr(1, 2), 0], [Fr(1, 2), 1, 0], [0, 0, s * Fr(2, 3) * n * n]]
    return dict(name=f"stacking {word}, d^2 = {s}*2/3", G=G, T=[(1, 0, 0), (0, 1, 0), (0, 0, 1)], motif=motif,
                w={"tet": (0, 1), "oct": (0, 0)}, A="tet", B="oct", D2=12, units="ball spacing 1; lam = w_tet - w_oct", expect=[])
STEP = {('A', 'B'): 1, ('B', 'C'): 1, ('C', 'A'): 1, ('B', 'A'): -1, ('C', 'B'): -1, ('A', 'C'): -1}
def steps(word): n = len(word); return [STEP[(word[k], word[(k + 1) % n])] for k in range(n)]
def words(maxlen):
    seen, out = set(), []
    for n in range(2, maxlen + 1):
        for st in itertools.product((1, -1), repeat=n):
            if sum(st) % 3: continue
            if any(st[i:] + st[:i] < st for i in range(n)): continue            # one rotation
            if any(n % p == 0 and st == st[:p] * (n // p) and sum(st[:p]) % 3 == 0 for p in range(1, n)): continue   # primitive words only
            key = min(tuple(st[i:] + st[:i]) for i in range(n)); mk = min(tuple(-x for x in st[i:] + st[:i]) for i in range(n))
            if min(key, mk) in seen: continue
            seen.add(min(key, mk)); w = 'A'
            for x in st[:-1]: w += 'ABC'[('ABC'.index(w[-1]) + x) % 3]
            out.append(w)
    return out
ROLE = ['oct', 'tetX', 'tetY']
def label(st, g, role, r):
    n = len(st); ctx = tuple(st[(g + j) % n] for j in range(-r, r + 1))
    return (role, min(ctx, tuple(-x for x in ctx)))
def walk(word, s):
    key = f'sp_{word}_{s}'; spec = net_for(word, s); networks.NETS[key] = spec; census.NETS[key] = spec
    C = census.Census(key); d = C.walk()
    fails = [c for c in C.checks if c[0] != 'PASS']
    return d, fails
if __name__ == '__main__':
    s = Fr(sys.argv[1]); maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    W = words(maxlen); print('words', W, flush=True)
    data, allfails = {}, {}
    for w in W:
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()): d, f = walk(w, s)
        d['_w'] = w; data[w] = d; allfails[w] = len(f); print(w, len(d['intervals']), 'intervals', 'fails', len(f), flush=True)
    cuts = sorted({Fr(iv[x]) for d in data.values() for iv in d['intervals'] for x in ('lo', 'hi') if iv[x] not in (None, 'None')})
    wins = list(zip(cuts, cuts[1:]))
    def vol_at(d, i, lo, hi):
        mid = (lo + hi) / 2
        for iv in d['intervals']:
            if Fr(iv['lo']) <= lo and hi <= Fr(iv['hi']):
                x = iv['sites'][i]; return None if x.get('vanished') or 'volume' not in x else sp.expand(len(d['_w']) * sp.sympify(x['volume']).subs('lam', L))   # census volume is per unit cell height: x n layers
        return 'gap'
    res = {'s': str(s), 'words': W, 'checks_failed': allfails, 'windows': [[str(a), str(b)] for a, b in wins], 'locality': {}, 'mix': {}}
    for r in (1, 2, 3):
        table, clash = {}, []
        for (lo, hi) in wins:
            for w, d in data.items():
                st = steps(w)
                for i in range(len(w) * 3):
                    v = vol_at(d, i, lo, hi)
                    if v == 'gap': continue
                    lb = (str(lo), label(st, i // 3, ROLE[i % 3], r)); v = 0 if v is None else v
                    if lb in table and sp.simplify(table[lb] - v) != 0: clash.append((lb, w))
                    table.setdefault(lb, v)
        res['locality'][r] = len(clash); print('r', r, 'clashes', len(clash), clash[:3], flush=True)
        if not clash: break
    rmin = r
    pure = {}
    for (lo, lb), v in table.items():
        role, ctx = lb
        if all(x == ctx[0] for x in ctx): pure[(lo, role, 'c')] = v
        if all(ctx[j] != ctx[j + 1] for j in range(len(ctx) - 1)): pure[(lo, role, 'h')] = v
    a, b = sp.symbols('a b')
    for (lo, lb), v in sorted(table.items(), key=lambda t: (t[0][0], str(t[0][1]))):
        role, ctx = lb; pc, ph = pure.get((lo, role, 'c')), pure.get((lo, role, 'h'))
        if pc is None or ph is None: fit = 'no pure ref'
        else:
            eqs = sp.Poly(sp.expand(a * pc + b * ph - v), L).all_coeffs()
            sol = sp.solve(eqs, [a, b], dict=True)
            fit = 'none' if not sol else {k.name: str(sp.nsimplify(val)) for k, val in sol[0].items()}
        res['mix'].setdefault(lo, []).append({'role': role, 'ctx': ''.join('+' if x > 0 else '-' for x in ctx), 'volume': str(sp.factor(v)), 'fit': fit})
    res['rmin'] = rmin
    os.makedirs(os.path.expanduser('~/kres-tmp/splash/data'), exist_ok=True)
    json.dump(res, open(os.path.expanduser(f'~/kres-tmp/splash/data/s_{str(s).replace("/", "_")}.json'), 'w'), indent=1, default=str)
    print('done rmin', rmin, flush=True)
