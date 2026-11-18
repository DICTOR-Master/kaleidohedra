# Is the fair 32-face die's R^2 in the field of the 16-gon (cos(pi/16), degree 4) together with sqrt5?
import sympy as s
x = s.symbols('x')
p = x**8 - 280*x**7 + 10220*x**6 - 121800*x**5 + 483350*x**4 - 609000*x**3 + 255500*x**2 - 35000*x + 625
print('irreducible over Q:', s.factor_list(p))
for ext, name in ((s.sqrt(5), 'Q(sqrt5)'), (s.sqrt(2), 'Q(sqrt2)'), ([s.sqrt(2), s.sqrt(5)], 'Q(sqrt2,sqrt5)'),
                  (s.sqrt(2+s.sqrt(2)), 'Q(cos pi/8)'), ([s.sqrt(2+s.sqrt(2)), s.sqrt(5)], 'Q(cos pi/8, sqrt5)')):
    try:
        print(name, s.factor_list(p, extension=ext)[1].__len__(), 'factors:', [s.degree(f, x) for f, _ in s.factor_list(p, extension=ext)[1]])
    except Exception as e:
        print(name, 'error', e)
roots = sorted([r for r in s.Poly(p, x).nroots(n=30) if r.is_real])
print('real roots:', [s.N(r, 12) for r in roots])
import mpmath as m
m.mp.dps = 40
print('candidates tan^2(k pi/16)*?:', [m.nstr(m.tan(k*m.pi/16)**2, 10) for k in range(1, 8)])
print('candidates 5*tan^2(k pi/32):', [m.nstr(5*m.tan(k*m.pi/32)**2, 10) for k in range(1, 16)])
irr = len(s.factor_list(p)[1]) == 1
split = [s.degree(f, x) for f, _ in s.factor_list(p, extension=[s.sqrt(2+s.sqrt(2)), s.sqrt(5)])[1]] == [1]*8
print('FINAL ok' if irr and split else 'FINAL FAIL')
