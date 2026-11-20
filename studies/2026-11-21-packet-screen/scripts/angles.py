# Packet screen 2026-11-21, step 2: the distinct dihedral angles of all pieces.
# For each angle theta (cos theta = sign * sqrt(c2), c2 exact in the piece's field):
#   exact minimal polynomial of cos theta; exact test whether theta/pi is rational (Chebyshev test, reused from
#   studies/2026-11-21-gap-study/scripts/pyramid_dehn.py: theta = 2 pi k/n in lowest terms has cos of degree phi(n)/2,
#   and then minpoly(cos) divides T_n(x) - 1).
# Output data/angles.json: one row per distinct angle (identified across fields by minimal polynomial + value).
import sys, os, json
from fractions import Fraction as Fr
import mpmath as mp
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__))
from nf import fields, minpoly_of_root, X

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = fields(); mp.mp.dps = 120

def el(K, s): return K.el([Fr(t) for t in s])

def rational_pi(mpoly):
    d = mpoly.degree()
    cands = [n for n in range(1, 8 * d * d + 9) if (n <= 2 and d == 1) or (n >= 3 and sp.totient(n) == 2 * d)]
    for n in cands:
        if sp.Poly(sp.chebyshevt(n, X) - 1, X).rem(mpoly).is_zero: return n
    return None

def main():
    pieces = json.load(open(os.path.join(HERE, 'data', 'pieces.json')))
    rows = []; local = {}
    mpcache = {}
    for p in pieces:
        K = F[p['field']]
        for e in p['edges']:
            key = (p['field'], e[2], tuple(e[3]))
            if key in local: continue
            c2 = el(K, e[3]); cosv = e[2] * mp.sqrt(K.num(c2))
            if (p['field'], tuple(e[3])) not in mpcache: mpcache[(p['field'], tuple(e[3]))] = K.minpoly(c2)
            g = mpcache[(p['field'], tuple(e[3]))]
            h = sp.Poly(g.as_expr().subs(X, X ** 2), X)
            m = minpoly_of_root(h, cosv)
            # identify across fields
            hit = None
            for r in rows:
                if r['minpoly'] == str(m.as_expr()) and abs(r['_cos'] - cosv) < mp.mpf(10) ** -90: hit = r; break
            if hit is None:
                n = rational_pi(m)
                th = mp.acos(cosv)
                hit = {'id': len(rows), 'minpoly': str(m.as_expr()), 'degree': m.degree(), '_cos': cosv,
                       'cos': mp.nstr(cosv, 40), 'deg': mp.nstr(th * 180 / mp.pi, 30), 'theta': mp.nstr(th, 110),
                       'rational_pi_n': n, 'rational': n is not None,
                       'over_pi': (str(sp.Rational(2 * int(mp.nint(th * n / (2 * mp.pi))), n)) if n else None),   # T_n(cos) = 1 => n theta = 2 pi k exactly
                       'occurs': []}
                rows.append(hit)
            local[key] = hit['id']; hit['occurs'].append([p['field'], e[2], e[3]])
        print(p['id'], 'angles so far', len(rows), flush=True)
    for r in rows: del r['_cos']
    json.dump(rows, open(os.path.join(HERE, 'data', 'angles.json'), 'w'), indent=0)
    nr = sum(1 for r in rows if r['rational'])
    print(f'distinct dihedral angles: {len(rows)}; rational multiples of pi: {nr}; irrational: {len(rows) - nr}')
    from collections import Counter
    print('irrational by field:', Counter(o[0] for r in rows if not r['rational'] for o in r['occurs'][:1]))
    ok1 = all(r['rational'] == (r['over_pi'] is not None) for r in rows)
    ok2 = all(k in local for p in pieces for k in [(p['field'], e[2], tuple(e[3])) for e in p['edges']])
    print(('ok   ' if ok1 else 'FAIL ') + 'every rational angle has its exact multiple of pi'); print(('ok   ' if ok2 else 'FAIL ') + 'every edge of every piece has an angle')
    print('FINAL ok' if (ok1 and ok2) else 'FINAL FAIL')

if __name__ == '__main__':
    main()
