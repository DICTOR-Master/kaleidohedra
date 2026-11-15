"""Exploration: level-3 chart (s, ze, et) -> u = s, tau = s^4 (1 + s^4 ze), rho = 1 + s (1 + s et): leading orders of F~ and of the tests."""
import sys, re
from sage.all__sagemath_singular import QQ, PolynomialRing
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens()
F = {}; tests = {}
for line in open(sys.argv[1]):
    m = re.match(r'\[(.*)\] (N|D) = (.*)', line)
    if m: tests.setdefault(m.group(1), {})[m.group(2)] = Rn(m.group(3).replace('^', '**'))
    elif ' = ' in line: k, e = line.split(' = ', 1); F[k.strip()] = Rn(e.strip().replace('^', '**'))
Rs = PolynomialRing(QQ, 's,z,x'); s, z, x = Rs.gens()
A = int(sys.argv[2]); B = int(sys.argv[3])          # tau = s^4 (1 + s^A z), rho = 1 + s + s^B x
sub = (s, s**4 * (1 + s**A * z), 1 + s + s**B * x)
def lead(f, k=1):
    g = Rs(f(*sub)); m = min(e[0] for e in g.dict())
    return m, [sum(c * z**e[1] * x**e[2] for e, c in g.dict().items() if e[0] == m + j) for j in range(k)]
for k, f in F.items():
    m, L = lead(f, 2); print(f'{k}: s^{m}: {str(L[0].factor())[:150]} | next: {str(L[1])[:100]}')
for k, nd in tests.items():
    mN, lN = lead(nd['N']); mD, lD = lead(nd['D'])
    if lN[0].degree() > 0 or lD[0].degree() > 0:
        print(f'  [{k}] N ~ s^{mN} ({str(lN[0].factor())[:80]}), D ~ s^{mD} ({str(lD[0].factor())[:60]})')
