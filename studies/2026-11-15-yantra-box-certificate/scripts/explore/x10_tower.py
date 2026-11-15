"""Exploration: chart C1 at its bad point (s, th) = (0, 1): sub-chart th = 1 + s^2 z.  Lowest s-power of G, H, D, c138, Q - 1/2 parts."""
import sys
from sage.all__sagemath_singular import QQ, PolynomialRing
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens(); Fr = Rn.fraction_field()
src = {}
for line in open(sys.argv[1]):
    k, e = line.split(' = ', 1); src[k.strip().rstrip('~')] = Rn(e.strip().replace('^', '**'))
one = Fr(1); t = u * tau
P = u**2 / (1 + u**2); R = one / (1 + u**2); w3 = u / (1 + u**2)
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2); k3 = w3 / (1 - P); xZ = k3 * (1 - R)
c138 = w1 * (R - b1) - xZ * (P - b1); n = w1 * P * (R - b1) - xZ * b1 * (P - b1)
X = {'G': Fr(src['G']), 'H': Fr(src['H1']), 'D': Fr(src['D']), 'c138': c138, 'n - c/2': n - c138 / 2, 'Rc - n': R * c138 - n}
Rs = PolynomialRing(QQ, 's,z,r'); s, z, r = Rs.gens(); Fs = Rs.fraction_field()
for k in sys.argv[2:]:
    Z0 = QQ(k)
    print('--- sub-chart th = 1 + s^2 (z), shift', Z0)
    for nm, f in X.items():
        g = Fs(f.numerator()(s, s**4 * (1 + s**2 * z), r)) / Fs(f.denominator()(s, s**4 * (1 + s**2 * z), r))
        N = Rs(g.numerator()); Dd = Rs(g.denominator())
        def low(P_):
            m = min(e[0] for e in P_.dict()); lead = sum(c * z**e[1] * r**e[2] for e, c in P_.dict().items() if e[0] == m)
            return m, lead
        mN, lN = low(N); mD, lD = low(Dd)
        print(f'{nm}: s^{mN - mD} * ({str(lN.factor())[:200]}) / ({str(lD.factor())[:80]})')
