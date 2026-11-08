"""Theorem Q, symbolic part: with rational leg slopes u (t7), v (t3) and depths Q (= b6), S (= b9),
the single non-rational step of Huet's chain is the quadratic for b1 (Chiodo's Apollonius step).
We compute its discriminant Delta(u, v, Q, S) and split it into square part x odd part.
Output: ../data/discriminant-data.txt with the odd (square-free) part, used by rational_search2.py.
Check: at three random rational points the factorised form equals the direct discriminant."""
import sympy as sp, random
u, v, Q, S, t = sp.symbols('u v Q S t')
P = v**2/(1+v**2); w3 = v/(1+v**2); R = 1/(1+u**2); w7 = u/(1+u**2)
xW = w7*P/R; xX = xW*(S-R)/(S-P); k9 = xX/(R-P); k3 = w3/(1-P)
b8 = (k3+k9*P)/(k3+k9); xF = k9*(Q-P); w6 = xW*(S-Q)/(S-P); xZ = k3*(1-R); k7 = w7/R
mA = xZ/(Q-P); c4 = xF/(b8-Q)
D2 = mA*(P-t)+k7*(R-t); N2 = mA*Q*(P-t); D4 = c4*(R-t)+xZ; N4 = c4*b8*(R-t)+xZ*t
F = mA*(P-t)*(Q*D4-N4)*k7*Q - w6*(N4*D2-N2*D4)
num = sp.factor(sp.together(F).as_numer_denom()[0])
const, fl = sp.factor_list(num)
core = [f for f, m in fl if sp.degree(f, t) == 2]
assert len(core) == 1
A, B, C = sp.Poly(core[0], t).all_coeffs()
disc = sp.expand(B**2 - 4*A*C)
dc, dfl = sp.factor_list(disc)
odd = [f for f, m in dfl if m % 2 == 1]
print('closing quadratic in b1: degrees (t,u,v,Q,S) =', [sp.degree(core[0], x) for x in (t, u, v, Q, S)])
print('discriminant = constant', dc, 'x', ' x '.join(f'[deg(u,v,Q,S)={tuple(sp.degree(f, x) for x in (u, v, Q, S))}]^{m}' for f, m in dfl))
oddpart = sp.expand(dc * sp.Mul(*odd))
print('odd part degrees (u,v,Q,S):', [sp.degree(oddpart, x) for x in (u, v, Q, S)])
ok = True
for _ in range(3):
    pt = {u: sp.Rational(random.randint(70, 90), 100), v: sp.Rational(random.randint(60, 80), 100),
          Q: sp.Rational(random.randint(50, 57), 100), S: sp.Rational(random.randint(80, 90), 100)}
    lhs = disc.subs(pt); rhs = (dc*sp.Mul(*[f**m for f, m in dfl])).subs(pt)
    ok = ok and sp.simplify(lhs - rhs) == 0
with open('../data/discriminant-data.txt', 'w') as fh:
    fh.write('# odd part of the Apollonius discriminant Delta(u,v,Q,S) (Delta = odd part x square)\n')
    fh.write(str(oddpart) + '\n')
    fh.write('# closing quadratic in t = b1 (numerator, Huet conditions, slopes u, v)\n')
    fh.write(str(core[0]) + '\n')
print('FINAL ok' if ok else 'FINAL FAIL discriminant factorisation check')
