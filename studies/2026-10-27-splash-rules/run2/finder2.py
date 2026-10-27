# Splash Rules run 2 (DICTO 2026-10-27): exact relations among piece volumes in ANY census weight walk (no c/h pair needed).
# For each network JSON (census.py format) and each window: the distinct piece volumes V_1..V_k (polynomials in lam) and the constant 1.
# (1) RATIOS: V_i / V_j constant (report the exact ratio). (2) RELATIONS: integer null-space vectors of [V_1..V_k, 1] with small
# entries (|c| <= 6), excluding the plain total (counts x volumes = cell volume). (3) STOPS: each stop as a fraction, flag small denominators.
# Two-parameter walks (perovskite: lam, mu; 'chambers' instead of 'intervals') are handled the same way, monomials in lam and mu.
# Usage: finder2.py <net.json> ... -> prints a report; JSON summary to run2/out/<name>.json
import json, sys, os, itertools
import sympy as sp
L, M = sp.symbols('lam mu'); OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'); os.makedirs(OUT, exist_ok=True)
def vec(p, mons): P = sp.Poly(sp.expand(p), L, M); return [P.coeff_monomial(m) for m in mons]
def nets(path):
    d = json.load(open(path))
    if 'intervals' in d or 'chambers' in d: yield d
    else:
        for k, v in d.items():
            if isinstance(v, dict) and ('intervals' in v or 'chambers' in v): yield v
for d in (n for p in sys.argv[1:] for n in nets(p)):
    name = d.get('key', d.get('name', '?')); res = {'name': name, 'windows': []}
    print(f'=== {name}: {d.get("name", "")}', flush=True)
    for iv in d.get('intervals') or [dict(c, lo='chamber', hi=c['verts']) for c in d['chambers']]:
        if 'sites' not in iv: continue
        vols, counts = {}, {}
        for s in iv['sites']:
            if s.get('vanished') or 'volume' not in s: continue
            v = sp.expand(sp.sympify(s['volume']).subs({'lam': L, 'mu': M})); k = sp.srepr(v)
            vols.setdefault(k, (s['kind'], v)); counts[k] = counts.get(k, 0) + 1
        keys = list(vols); V = [vols[k][1] for k in keys]; kinds = [vols[k][0] for k in keys]
        if not V: continue
        mons = sorted({m for v in V for m in sp.Poly(v, L, M).monoms()}); mons = [L ** a * M ** b for a, b in mons]
        if 1 not in mons: mons = [sp.Integer(1)] + mons
        found = []
        for i, j in itertools.combinations(range(len(V)), 2):
            r = sp.cancel(V[i] / V[j])
            if r.free_symbols == set(): found.append(f'ratio {kinds[i]}#{i} / {kinds[j]}#{j} = {r}')
        Mx = sp.Matrix([vec(v, mons) for v in V] + [[1 if m == 1 else 0 for m in mons]]).T
        total = [counts[k] for k in keys] + [None]
        for nv in Mx.nullspace():
            nv = nv * sp.ilcm(*[sp.fraction(x)[1] for x in nv]); g = sp.igcd(*[int(x) for x in nv if x != 0]) or 1; nv = [int(x) // g for x in nv]
            tot = [counts[k] for k in keys]
            if all(nv[i] * tot[0] == tot[i] * nv[0] for i in range(len(tot))): continue        # the plain total: counts x volumes = cell
            if max(abs(x) for x in nv[:-1]) <= 6 and not all(x == 0 for x in nv[:-1]):
                terms = ' + '.join(f'{c}·{kinds[i]}#{i}' for i, c in enumerate(nv[:-1]) if c)
                found.append(f'relation {terms} = {-nv[-1]}·1' if nv[-1] else f'relation {terms} = 0')
        w = {'lo': iv['lo'], 'hi': iv['hi'], 'pieces': len(V), 'found': found}
        res['windows'].append(w)
        print(f"  ({iv['lo']}, {iv['hi']}) {len(V)} distinct pieces: " + ('; '.join(found) if found else '-'), flush=True)
    st = [str(s['lam']) for s in d.get('stops', [])]; res['stops'] = st
    print('  stops:', ', '.join(st), flush=True)
    json.dump(res, open(os.path.join(OUT, f'{name}.json'), 'w'), indent=1)
