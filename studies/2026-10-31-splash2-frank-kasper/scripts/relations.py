# Exact linear relations among a small set of per-atom counts over every TCP structure (sympy nullspace, rationals).
import sys, json
from fractions import Fraction as Fr
import sympy as sp
D = json.load(open(sys.argv[1]))
FK = [r for r in D['structures'] if r['ok']]
names = ['x12', 'x14', 'x15', 'x16', 't0', 't1', 't2', 's12', 's14', 's15', 's16', 'one']
def row(r):
    C = r['census']; N = C['N']
    g = lambda k: sp.Rational(C.get(k, 0), N)
    return [g('N12'), g('N14'), g('N15'), g('N16'), g('tet_j0'), g('tet_j1'), g('tet_j2'), g('shell6_Z12'), g('shell6_Z14'), g('shell6_Z15'), g('shell6_Z16'), 1]
for label, rows in (('all TCP', FK), ('physical', [r for r in FK if r['kind'] == 'cif']), ('square-triangle', [r for r in FK if r['kind'] == 'st']), ('FK59', [r for r in FK if r['kind'] == 'fk59'])):
    M = sp.Matrix([row(r) for r in rows])
    ns = M.nullspace()
    print('==', label, len(rows), 'rank', M.rank(), 'relations', len(ns))
    for v in ns:
        v = v / max(abs(x) for x in v) if False else v
        den = sp.ilcm(*[sp.fraction(x)[1] for x in v]); v = v * den
        print('   0 =', ' + '.join(f'({v[i]})*{names[i]}' for i in range(len(names)) if v[i] != 0))
