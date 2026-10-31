# Laws in the Ammann-Beenker splash: which counts are linear forms in the tile counts (Pluecker coordinates), and where.
# ~/geom/bin/python ablaw.py out/ab.json > out/ablaw.log
import sys, json
from fractions import Fraction as Fr
import sympy as sp

D = json.load(open(sys.argv[1])); P = [r for r in D['planes'] if r['ok']]
PAIRS = ['01', '02', '03', '12', '13', '23']
AB = ['00100101', '00101101', '01011011', '01101111', '01111111', '11111111']   # F(3) E(4) D(5) C(6) B(7) A(8)
NAME = dict(zip(AB, 'FEDCBA'))
lim = {c: (Fr(v['a']), Fr(v['b'])) for c, v in D['limit']['freq'].items()}

def avg(r): return {c: Fr(x) for c, x in r['avg'].items()}
def runs_equal(r):
    return all(x['stars'] == r['runs'][0]['stars'] for x in r['runs'])
def area_equal(r):
    a = avg(r); return all(all(Fr(x['stars'].get(c, 0)) == a.get(c, 0) for c in set(a) | set(x['stars'])) for x in r['runs'])

def fit(rows, keys, target):
    """exact solve count = sum a_k pl_k over rows; returns coefficients or None (inconsistent)"""
    M = sp.Matrix([[r['pl'][k] for k in keys] for r in rows]); b = sp.Matrix([target(r) for r in rows])
    try:
        sol, params = M.gauss_jordan_solve(b)
    except ValueError:
        return None
    if params.shape[0]: sol = sol.subs({p: 0 for p in params})
    return [sp.Rational(x) for x in sol]

print('planes', len(P), '; t-family', sum(r['name'].startswith('t=') for r in P), '; random', sum(r['name'].startswith('r') for r in P))
print('tile counts = Pluecker coordinates in every run:', all(x['tiles'] == r['pl'] for r in P for x in r['runs']))
abonly = [r for r in P if set(avg(r)) <= set(AB)]
print('planes whose offset-averaged stars are AB stars only:', len(abonly), '(t-family', sum(r['name'].startswith('t=') for r in abonly), ')')
print('  of these, counts independent of the offset:', sum(runs_equal(r) for r in abonly), '; counts = cell areas:', sum(area_equal(r) for r in abonly))
other = [r for r in P if r not in abonly]
print('planes with other stars:', len(other), '; offset-independent', sum(runs_equal(r) for r in other), '; = areas', sum(area_equal(r) for r in other))

print('\n== AB-only planes: each star count (offset average) as a linear form in the six tile counts')
law = {}
for c in AB:
    co = fit(abonly, PAIRS, lambda r: avg(r).get(c, 0))
    law[c] = co
    print(NAME[c], c, 'coefficients (01,02,03,12,13,23):', co)
# by symmetry: rhombs R = 01+03+12+23, squares Q = 02+13
print('\n== in rhombs R and squares Q:')
for c in AB:
    co = fit([dict(r, pl={'R': sum(r['pl'][k] for k in ('01', '03', '12', '23')), 'Q': r['pl']['02'] + r['pl']['13']}) for r in abonly], ['R', 'Q'], lambda r: avg(r).get(c, 0))
    print(NAME[c], co)
    if co:
        # limit: R/N = 2 - sqrt2, Q/N = sqrt2 - 1
        a = co[0] * 2 - co[1]; b = -co[0] + co[1]
        print('   limit on the line:', a, '+', b, 'sqrt2; exact AB value', lim[c])
# actual counts per offset, AB-only planes
print('\n== actual counts (each offset) on AB-only planes, as linear forms in R, Q:')
for c in AB:
    rows = [(r, x) for r in abonly for x in r['runs']]
    M = sp.Matrix([[sum(r['pl'][k] for k in ('01', '03', '12', '23')), r['pl']['02'] + r['pl']['13']] for r, x in rows])
    b = sp.Matrix([x['stars'].get(c, 0) for r, x in rows])
    try:
        sol, params = M.gauss_jordan_solve(b); print(NAME[c], list(sol))
    except ValueError:
        print(NAME[c], 'not linear')
# t-family table
print('\n== t-family (square approximants), offset average')
for r in sorted([r for r in P if r['name'].startswith('t=')], key=lambda r: Fr(r['name'][2:])):
    a = avg(r); extra = {k: str(v) for k, v in a.items() if k not in AB}
    print(r['name'], 'N', r['N'], 'R', sum(r['pl'][k] for k in ('01', '03', '12', '23')), 'Q', r['pl']['02'] + r['pl']['13'],
          'stars', [str(a.get(c, 0)) for c in AB], 'other', extra, 'offset-indep', runs_equal(r), '=area', area_equal(r))

print('\n== split: t-family vs random AB-only planes')
RQ = lambda r: dict(r, pl={'R': sum(r['pl'][k] for k in ('01', '03', '12', '23')), 'Q': r['pl']['02'] + r['pl']['13']})
T = [r for r in abonly if r['name'].startswith('t=')]; Rn = [r for r in abonly if not r['name'].startswith('t=')]
for c in AB:
    print(NAME[c], 't-family in R, Q:', fit([RQ(r) for r in T], ['R', 'Q'], lambda r: avg(r).get(c, 0)), '; random AB-only in six:', fit(Rn, PAIRS, lambda r: avg(r).get(c, 0)))
for r in Rn:
    print(r['name'], r['pl'], {NAME[c]: str(v) for c, v in avg(r).items()}, 'offset-indep', runs_equal(r), '=area', area_equal(r), [{NAME[c]: v for c, v in x['stars'].items()} for x in r['runs']])
