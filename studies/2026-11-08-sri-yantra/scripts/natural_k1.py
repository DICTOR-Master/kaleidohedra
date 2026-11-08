"""The DICTO Yantra (Cleo-Octangula, both small triangles on the circle: K1) exactly in natural coordinates: u = 2/phi^2, v = 1/sqrt2.
S: the root of G(S) (quadratic over Q(sqrt2, sqrt5)) matching K1. t: the degree-10 relation H(t, S) with that S; factor it over
Q(sqrt2, sqrt5) after clearing S where possible, and find which factor holds K1's t; report its degree."""
import sympy as sp, json, natural as N
s5, s2 = sp.sqrt(5), sp.sqrt(2)
phi = (1 + s5) / 2
U, V = sp.nsimplify(2 / phi**2), 1 / s2
Gk = sp.expand(N.G.subs({N.u: U, N.v: V}))
K = json.load(open('kites.json'))['K1']; Sk = sp.Float(K['b']['9']['a'], 40); b1k = sp.Float(K['b']['1']['a'], 40); tk = sp.sqrt(b1k / (1 - b1k))
Sroots = sp.solve(Gk, N.S)
Sex = min(Sroots, key=lambda r: abs(sp.N(r - Sk, 40)))
print('S exact:', sp.radsimp(Sex))
print('S value:', sp.N(Sex, 25), ' K1 S:', sp.N(Sk, 25))
Hmain = [f for f, m in sp.factor_list(sp.factor(sp.numer(sp.together(N.H))))[1] if sp.degree(f, N.t) == 10][0]
# eliminate S: resultant of the degree-10 relation and G in S gives a polynomial in t over Q(sqrt2, sqrt5)
Res = sp.resultant(sp.expand(Hmain.subs({N.u: U, N.v: V})), Gk, N.S)
Res = sp.Poly(sp.expand(Res), N.t)
print('after eliminating S: degree in t =', Res.degree())
fl = sp.factor_list(Res.as_expr(), N.t, extension=[s2, s5])
best = None
for f, m in fl[1]:
    val = abs(sp.N(f.subs(N.t, tk), 30))
    print('  factor of degree', sp.degree(f, N.t), ' value at K1:', sp.N(val, 3))
    if best is None or val < best[0]: best = (val, sp.degree(f, N.t))
print('K1 t lies on a factor of degree', best[1], 'over Q(sqrt2, sqrt5)')
print('FINAL ok' if best[0] < 1e-20 else 'FINAL FAIL: no factor vanishes at K1')
