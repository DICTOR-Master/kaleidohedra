"""The yantra in natural coordinates (DICTO 11-08: 'there must be a simpler formula'). Great slopes u (t7), v (t3); t9's corners on the
circle give S from u, v by one quadratic G(S) = 0; t1's corner is the circle point (x, d) = (t/(1+t^2), t^2/(1+t^2)), and then Q is
LINEAR in t (from t1's leg through t3's base corner line, the (1,3,8) marma). The construction's closing (Apollonius) equation becomes
one relation H(t, S) = 0. Compute G and H symbolically, their degrees, and check them on the Cleo-Antonius perfect yantra (GF1)."""
import sympy as sp, json
u, v, t, S = sp.symbols('u v t S', positive=True)
P = v**2 / (1 + v**2); R = 1 / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
xW = w7 * P / R
# (c): t9 corner on the circle: w9 = xW (S - R)/(R - P); w9^2 = S (1 - S)
G = sp.factor(sp.numer(sp.together((xW * (S - R) / (R - P))**2 - S * (1 - S))))
# t1 corner on the circle via t
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
k3 = w3 / (1 - P); xZ = k3 * (1 - R)
Qs = sp.symbols('Q')
# (1,3,8) with m1 = w1/(Q - b1) and the model's m1 = xZ (P - b1)/((R - b1)(Q - P)): linear in Q
Qsol = sp.solve(sp.Eq(w1 / (Qs - b1), xZ * (P - b1) / ((R - b1) * (Qs - P))), Qs)
assert len(Qsol) == 1; Q = sp.simplify(Qsol[0])
# the remaining pieces of the model, then the Apollonius equation F(b1) = 0
xX = xW * (S - R) / (S - P); k9 = xX / (R - P); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P)
k7 = w7 / R; mA = xZ / (Q - P); c4 = xF / (b8 - Q)
D2 = mA * (P - b1) + k7 * (R - b1); N2 = mA * Q * (P - b1); D4 = c4 * (R - b1) + xZ; N4 = c4 * b8 * (R - b1) + xZ * b1
F = mA * (P - b1) * (Q * D4 - N4) * k7 * Q - w6 * (N4 * D2 - N2 * D4)
H = sp.factor(sp.numer(sp.together(F)))
fac = sp.factor_list(H)
print('G(S) =', G)
print('Q(t) =', sp.factor(Q))
print('H factors (degree in t, degree in S):')
for f_, m in fac[1]:
    print('   ', sp.degree(f_, t), sp.degree(f_, S), ' multiplicity', m, '' if sp.degree(f_, t) + sp.degree(f_, S) > 2 else f_)
# check on GF1 (Cleo-Antonius perfect yantra)
GF = json.load(open('golden_family.json'))['GF1']
num = {u: sp.Float(GF['u'], 40), v: sp.Float(GF['v'], 40)}
b1v = sp.Float(GF['b']['1']['a'], 40); tv = sp.sqrt(b1v / (1 - b1v))
Sv = sp.Float(GF['b']['9']['a'], 40)
vals = {**num, t: tv, S: Sv}
print('check on GF1: G =', sp.N(G.subs(vals), 8), ' H factors:', [sp.N(f_.subs(vals), 8) for f_, m in fac[1]])
print('       Q(t) =', sp.N(Q.subs(vals), 15), ' GF1 Q =', GF['b']['6']['a'][:17])
gq = abs(float(sp.N(G.subs(vals), 30))); hq = min(abs(float(sp.N(f_.subs(vals), 30))) for f_, m in fac[1]); qq = abs(float(sp.N(Q.subs(vals) - sp.Float(GF['b']['6']['a'], 40), 30)))
print('residuals G, H, Q:', gq, hq, qq)
ok = gq < 1e-25 and hq < 1e-25 and qq < 1e-25
print('FINAL ok' if ok else 'FINAL FAIL: natural-coordinate relations do not vanish on GF1')
