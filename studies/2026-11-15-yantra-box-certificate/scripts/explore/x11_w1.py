"""Exploration: chart W1 (s, z, xi) -> u = s, tau = s^4 (1 + s^2 z), rho = 1 + s xi.  Lowest s-orders of F~ and window tests."""
import sys
from sage.all__sagemath_singular import QQ, PolynomialRing
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens(); Fr = Rn.fraction_field()
src = {}
for line in open(sys.argv[1]):
    if line.startswith('['): continue
    k, e = line.split(' = ', 1); src[k.strip().rstrip('~')] = Rn(e.strip().replace('^', '**'))
one = Fr(1); t = u * tau
P = u**2 / (1 + u**2); R = one / (1 + u**2); w3 = u / (1 + u**2)
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2); k3 = w3 / (1 - P); xZ = k3 * (1 - R)
c138 = w1 * (R - b1) - xZ * (P - b1); n = w1 * P * (R - b1) - xZ * b1 * (P - b1)
X = {'G': Fr(src['G']), 'H': Fr(src['H1']), 'D': Fr(src['D']), 'c138': c138, 'n - c/2': n - c138 / 2, 'Rc - n': R * c138 - n}
Rs = PolynomialRing(QQ, 's,z,x'); s, z, x = Rs.gens(); Fs = Rs.fraction_field()
sub = (s, s**4 * (1 + s**2 * z), 1 + s * x)
for nm, f in X.items():
    g = Fs(f.numerator()(*sub)) / Fs(f.denominator()(*sub))
    N = Rs(g.numerator()); Dd = Rs(g.denominator())
    mD = min(e[0] for e in Dd.dict()); lD = sum(c * z**e[1] * x**e[2] for e, c in Dd.dict().items() if e[0] == mD)
    mN = min(e[0] for e in N.dict())
    out = []
    for k in range(mN, mN + int(sys.argv[2])):
        lk = sum(c * z**e[1] * x**e[2] for e, c in N.dict().items() if e[0] == k)
        out.append(f's^{k - mD}: {str(lk.factor()) if lk != 0 else 0}'[:220])
    print(f'{nm} (denominator lead {lD}):'); [print('    ', o) for o in out]
