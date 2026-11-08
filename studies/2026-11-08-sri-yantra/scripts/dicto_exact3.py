"""DICTO Yantra exact form, last stage (11-08 night): dicto_exact2.py reached the PARI resultant in t (degree 2240 in u) and then
failed comparing values (float overflow). Here: RH, RD from dicto-exact-RH-RD.pkl; the same norm and factor selection; PARI resultant;
PARI factors it over Q; for each factor its real roots at 120 digits; the factor with a root nearest GF1's u (known to 30 digits) is
the answer, accepted only if that root agrees to 25 digits and no other factor comes within 1e-10."""
import pickle, json, time, sys
import sympy as sp
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.0f} s]', *a, flush=True)
sys.argv = [sys.argv[0]]
t, u = sp.symbols('t u', positive=True); w = sp.Symbol('w')
def norm_q(P):
    """Norm over Q(sqrt5): replace sqrt5 by w, multiply by the conjugate, reduce w^2 = 5."""
    Pw = sp.expand(P.subs(sp.sqrt(5), w)); N = sp.expand(Pw * Pw.subs(w, -w))
    return sp.Poly(sp.rem(sp.Poly(N, w), sp.Poly(w**2 - 5, w)).as_expr(), t, u)
def keep(P, t0, u0, tag):
    fl = sp.factor_list(P.as_expr()); say(tag, 'factor degrees (t, u):', [(sp.degree(f, t), sp.degree(f, u)) for f, m in fl[1]])
    best = min(((abs(sp.N(f.subs({t: t0, u: u0}), 30)), f) for f, m in fl[1] if f.free_symbols & {t, u}), key=lambda x: x[0])
    say(tag, 'kept factor of degree', sp.degree(best[1], t), sp.degree(best[1], u), 'residual', sp.N(best[0], 3)); return best[1], best[0]
RH, RD = (sp.sympify(eval(x, sp.__dict__)) for x in pickle.load(open('dicto-exact-RH-RD.pkl', 'rb')))
GF = json.load(open('golden_family.json'))['GF1']; u0 = sp.Float(GF['u'], 30)
t0 = sp.Float(GF['b']['1']['a'], 40) / sp.Float(GF['w']['1']['a'], 40)
a, ra = keep(norm_q(sp.Poly(RH, t, u)), t0, u0, 'RH'); b, rb = keep(norm_q(sp.Poly(RD, t, u)), t0, u0, 'RD')
import cypari2; pari = cypari2.Pari(); pari.allocatemem(16 * 10**9); pari.set_real_precision(120)
pa = lambda X: sp.sstr(X).replace('**', '^')
R = pari(f'polresultant({pa(a)}, {pa(b)}, t)'); say('resultant degree in u', pari.poldegree(R, 'u'))
F = pari.factor(R); say('factors (degree x multiplicity):', [(int(pari.poldegree(F[0][i], 'u')), int(F[1][i])) for i in range(len(F[0]))])
U0 = pari('0.679318588706774657388650310391')
res = []
for i in range(len(F[0])):
    f = F[0][i]
    if pari.poldegree(f, 'u') < 1: continue
    roots = pari.polrootsreal(f) if pari.poldegree(f, 'u') > 1 else [pari.polcoef(f, 0, 'u') * -1 / pari.polcoef(f, 1, 'u')]
    d = min(abs(r - U0) for r in roots) if len(roots) else pari(1)
    lg = -120.0 if d == 0 else float(pari.log(d) / pari.log(10))   # 0: agrees at the working precision
    res.append((lg, int(pari.poldegree(f, 'u')), f))
res.sort(key=lambda x: x[0])
for lg, dg, f in res[:4]: say(f'factor degree {dg}: nearest real root differs from GF1 u by 10^{lg:.1f}')
best = res[0]; second = res[1][0] if len(res) > 1 else 0
open('dicto-yantra-exact-u.txt', 'w').write(str(best[2])); say('written dicto-yantra-exact-u.txt (degree', best[1], ')')
print('FINAL ok' if best[0] < -25 and second > -10 else 'FINAL FAIL: no factor isolates GF1 u to 25 digits')
