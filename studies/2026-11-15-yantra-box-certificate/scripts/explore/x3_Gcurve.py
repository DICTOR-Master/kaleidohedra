from sage.all__sagemath_singular import QQ, PolynomialRing
R = PolynomialRing(QQ, 'u,S'); u, S = R.gens()
G = u**10*S**2 + 3*u**8*S**2 - 3*u**8*S + u**6*S**2 - 2*u**6*S + u**6 - 2*u**4*S**2 + 2*u**4*S + S**2 - S
a = G.coefficient({S: 2}); b = G.coefficient({S: 1}); c = G.coefficient({S: 0})
print('a =', a.factor()); print('b =', b.factor()); print('c =', c.factor())
disc = b**2 - 4*a*c
print('disc =', disc.factor())
