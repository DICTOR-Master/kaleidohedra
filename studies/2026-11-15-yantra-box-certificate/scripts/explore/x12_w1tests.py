"""Exploration: in chart W1, leading s-order of every admissibility test N/D; sign over the window z in (0,1) at s = 0."""
import sys, re
from sage.all__sagemath_singular import QQ, PolynomialRing
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens()
tests = {}
for line in open(sys.argv[1]):
    m = re.match(r'\[(.*)\] (N|D) = (.*)', line)
    if m: tests.setdefault(m.group(1), {})[m.group(2)] = Rn(m.group(3).replace('^', '**'))
Rs = PolynomialRing(QQ, 's,z,x'); s, z, x = Rs.gens()
sub = (s, s**4 * (1 + s**2 * z), 1 + s * x)
def lead(f):
    g = Rs(f(*sub)); m = min(e[0] for e in g.dict()); return m, sum(c * z**e[1] * x**e[2] for e, c in g.dict().items() if e[0] == m)
for k, nd in tests.items():
    mN, lN = lead(nd['N']); mD, lD = lead(nd['D'])
    # sign of lN/lD on grid z in (0,1), x in [0, 3] (x is pinned near 1 by G)
    sg = set()
    for zi in range(1, 20):
        for xi in range(0, 31):
            a = lN(0, QQ(zi) / 20, QQ(xi) / 10); b = lD(0, QQ(zi) / 20, QQ(xi) / 10)
            sg.add(0 if a * b == 0 else (1 if a * b > 0 else -1))
    print(f'{k}: N ~ s^{mN} ({str(lN.factor())[:70]}), D ~ s^{mD} ({str(lD.factor())[:50]}); signs on window: {sorted(sg)}')
