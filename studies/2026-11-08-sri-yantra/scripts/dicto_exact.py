"""Exact form of the DICTO Yantra (perfect Cleo-Antonius yantra, GF1) by elimination in natural coordinates (always terminates).
Unknowns: u (upper great slope), t (t1's corner on the circle), S (bottom depth); v = p/u with p = 2/phi^3.
  G(S; u, v) = 0      t9's corners on the circle (natural.py)
  H(t, S; u, v) = 0   the construction's closing relation (degree 10 in t)
  D(t, S; u, v) = 0   bindu centred: the incircle centre of the triangle (t1's legs, t5's base) at depth 1/2, squared free of roots
Eliminate S (resultant with G), then t: one polynomial in u over Q(sqrt5); factor; the factor vanishing at GF1's u is the answer.
Progress lines with times; final line FINAL ok / FINAL FAIL."""
import sympy as sp, json, time, natural as N
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.0f} s]', *a, flush=True)
u, v, t, S = N.u, N.v, N.t, N.S
s5 = sp.sqrt(5); phi = (1 + s5) / 2; p = sp.nsimplify(2 / phi**3)
P = v**2 / (1 + v**2); R = 1 / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
xW = w7 * P / R; k3 = w3 / (1 - P); xZ = k3 * (1 - R); Q = N.Q
xX = xW * (S - R) / (S - P); k9 = xX / (R - P)
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2); m1 = w1 / (Q - b1)
b5 = (m1 * Q + k9 * P) / (m1 + k9)                       # (1,5,9)
# bindu: apex (0, Q) of t1 down to base at depth b5: height h = Q - b5 (apex below base), half-width hw = m1 h
h = Q - b5; hw = m1 * h
# incircle centre depth = b5 + r, r = hw h / (hw + sqrt(hw^2 + h^2)); centred: b5 + r = 1/2
# => sqrt(hw^2 + h^2) = hw h/(1/2 - b5) - hw  -> square: hw^2 + h^2 = (hw h/(1/2 - b5) - hw)^2
c = sp.Rational(1, 2) - b5
D = sp.numer(sp.together((hw**2 + h**2) * c**2 - (hw * h - hw * c)**2))
say('D built')
Hm = [f for f, m in sp.factor_list(sp.factor(sp.numer(sp.together(N.H))))[1] if sp.degree(f, t) == 10][0]
sub = {v: p / u}
G1 = sp.numer(sp.together(N.G.subs(sub))); H1 = sp.numer(sp.together(Hm.subs(sub))); D1 = sp.numer(sp.together(D.subs(sub)))
say('substituted; degrees in S:', sp.degree(G1, S), sp.degree(H1, S), sp.degree(D1, S))
RH = sp.resultant(G1, H1, S); say('res(G,H) in S done; degree in t', sp.degree(RH, t), 'in u', sp.degree(RH, u))
RD = sp.resultant(G1, D1, S); say('res(G,D) in S done; degree in t', sp.degree(RD, t), 'in u', sp.degree(RD, u))
RU = sp.resultant(RH, RD, t); say('res in t done; degree in u', sp.degree(RU, u))
GF = json.load(open('golden_family.json'))['GF1']; uv = sp.Float(GF['u'], 40)
fl = sp.factor_list(sp.expand(RU), u, extension=[s5]); say('factored:', [sp.degree(f, u) for f, m in fl[1]])
best = min(((abs(sp.N(f.subs(u, uv), 30)), f) for f, m in fl[1] if sp.degree(f, u) > 0), key=lambda x: x[0])
say('GF1 u lies on a factor of degree', sp.degree(best[1], u), 'residual', sp.N(best[0], 3))
open('dicto-yantra-exact-u.txt', 'w').write(str(best[1]))
print('FINAL ok' if best[0] < 1e-20 else 'FINAL FAIL: no factor vanishes at the DICTO Yantra')
