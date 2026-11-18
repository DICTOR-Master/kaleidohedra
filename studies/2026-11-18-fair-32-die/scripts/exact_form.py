# Exact form of the fair 32-face die's R^2 in Q(sqrt2, sqrt(2+sqrt2), sqrt5) = Q(cos(2pi/16), sqrt5), by PSLQ, then checked symbolically.
from mpmath import mp, mpf, sqrt, pslq, polyroots, nstr
import sympy as s
mp.dps = 200
coef = [1, -280, 10220, -121800, 483350, -609000, 255500, -35000, 625]
roots = polyroots(coef, maxsteps=2000, extraprec=800)
R2 = [r.real for r in roots if abs(r.imag) < mpf(10)**-100 and abs(r.real - mpf('1.1823250951')) < 1e-6][0]
a, b, c = sqrt(2), sqrt(2 + sqrt(2)), sqrt(5)
basis = [mpf(1), a, b, a*b]
B = basis + [v*c for v in basis]
rel = pslq([R2] + B, maxcoeff=10**8, maxsteps=10**6)
print('relation:', rel)
x = s.symbols('x'); A2, Bs, C5 = s.sqrt(2), s.sqrt(2 + s.sqrt(2)), s.sqrt(5)
sb = [1, A2, Bs, A2*Bs]; SB = sb + [v*C5 for v in sb]
expr = -sum(s.Rational(k, rel[0]) * v for k, v in zip(rel[1:], SB))
print('R^2 =', expr, '=', s.N(expr, 30))
P = x**8 - 280*x**7 + 10220*x**6 - 121800*x**5 + 483350*x**4 - 609000*x**3 + 255500*x**2 - 35000*x + 625
chk = s.simplify(s.expand(P.subs(x, expr))) == 0 and abs(s.N(expr, 50) - s.Float(str(R2), 50)) < 1e-40
print('exact check P(expr) == 0 and matches the root:', chk)
print('FINAL ok' if chk else 'FINAL FAIL')
