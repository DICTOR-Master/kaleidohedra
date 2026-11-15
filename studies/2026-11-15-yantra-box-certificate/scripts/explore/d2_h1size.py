"""Sizes of the kernel's unreduced numerator for variants of the (1,4,6) equation."""
from sage.all__sagemath_singular import QQ, PolynomialRing
R3 = PolynomialRing(QQ, 'u,t,S'); u, t, S = R3.gens(); Fr = R3.fraction_field()
import json, os
J = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'lean-deriv.json')))
def dec(p): return sum(QQ(c) * u**e[0] * t**e[1] * S**e[2] for e, c in p)
TAB = [(dec(r['N']), dec(r['D'])) for r in J['table']]
ix = {n: i for i, n in enumerate(J['names'])}
def F(n): return TAB[ix[n]]
def sub(a, b): return (a[0] * b[1] - b[0] * a[1], a[1] * b[1])
def mul(a, b): return (a[0] * b[0], a[1] * b[1])
def red(a):
    g = a[0].gcd(a[1]); return (a[0] // g, a[1] // g)
Q, b4, b2, k1, k6, w6 = F('Q'), F('b4'), F('b2'), F('k1'), F('k6'), F('w6')
e = sub(mul(k1, sub(Q, b4)), mul(k6, sub(b4, b2))); print('E146 as now:', len(e[0].monomials()))
e2 = sub(mul(mul(k1, sub(Q, b4)), sub(Q, b2)), mul(w6, sub(b4, b2))); print('s1 form:', len(e2[0].monomials()))
e1r, e2r, e3r = red(sub(Q, b4)), red(sub(Q, b2)), red(sub(b4, b2))
print('helpers reduced sizes', [len(x[0].monomials()) for x in (e1r, e2r, e3r)], [len(x[1].monomials()) for x in (e1r, e2r, e3r)])
f = sub(mul(mul(k1, e1r), e2r), mul(w6, e3r)); print('with reduced helpers, s1 form:', len(f[0].monomials()))
g = sub(mul(k1, e1r), mul(k6, e3r)); print('with reduced helpers, k6 form:', len(g[0].monomials()))
H1 = None
for line in open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'inputs', 'system-K.txt')):
    if line.startswith('H1 = '): H1 = R3(line.split(' = ', 1)[1].strip().replace('^', '**'))
print('H1 terms', len(H1.monomials()))
for nm, x in (('now', e), ('s1', e2), ('helpers s1', f), ('helpers k6', g)):
    q = x[0] // H1; print(nm, 'cofactor terms', len(q.monomials()), 'exact', q * H1 == x[0])
# helper quantities h1 = k1 (Q - b4), h2 = k6 (b4 - b2), reduced
h1 = red(mul(k1, sub(Q, b4))); h2 = red(mul(k6, sub(b4, b2)))
print('h1', len(h1[0].monomials()), len(h1[1].monomials()), 'h2', len(h2[0].monomials()), len(h2[1].monomials()))
g = h1[1].gcd(h2[1]); print('common denominator factor terms', len(g.monomials()))
f = sub(h1, h2); print('frac(h1 - h2) numerator', len(f[0].monomials()), 'cof', len((f[0] // H1).monomials()))
# with a common-denominator helper: write h2 over D1 when D2 | D1 ?
print('D1 % D2 == 0:', h1[1] % h2[1] == 0, ' D2 % D1 == 0:', h2[1] % h1[1] == 0)
# unreduced intermediate sizes of the kernel's frac for E146 as now
a = mul(k1, sub(Q, b4)); b = mul(k6, sub(b4, b2))
print('unreduced a:', len(a[0].monomials()), len(a[1].monomials()), ' b:', len(b[0].monomials()), len(b[1].monomials()))
