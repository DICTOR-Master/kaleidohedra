"""DICTO Yantra exact form, second route (11-08 night: dicto_exact.py was killed, exit 137, at the last resultant in t; sympy ran out
of memory on degrees (20, 64) in t and (38, 112) in u). Same steps up to RH, RD (imported unchanged), saved to disk; then each is
made rational (norm over Q(sqrt5): P(w) P(-w) with w^2 = 5), factored, and only the factor vanishing at GF1's (t, u) is kept; the
last resultant in t is done in PARI (cypari2, large stack), then factored, and the factor vanishing at GF1's u is the answer.
MODE=pilot runs stage B on a small known case (u = sqrt2-like toy) to prove the pipeline in < 5 min."""
import os, sys, time, json, pickle
import sympy as sp
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.0f} s]', *a, flush=True)
t, u, w = sp.symbols('t u w')
def norm_q(P):
    """Norm over Q(sqrt5): replace sqrt5 by w, multiply by the conjugate, reduce w^2 = 5."""
    Pw = sp.expand(P.subs(sp.sqrt(5), w)); N = sp.expand(Pw * Pw.subs(w, -w))
    return sp.Poly(sp.rem(sp.Poly(N, w), sp.Poly(w**2 - 5, w)).as_expr(), t, u)
def keep(P, t0, u0, tag):
    fl = sp.factor_list(P.as_expr()); say(tag, 'factor degrees (t, u):', [(sp.degree(f, t), sp.degree(f, u)) for f, m in fl[1]])
    best = min(((abs(sp.N(f.subs({t: t0, u: u0}), 30)), f) for f, m in fl[1] if f.free_symbols & {t, u}), key=lambda x: x[0])
    say(tag, 'kept factor of degree', sp.degree(best[1], t), sp.degree(best[1], u), 'residual', sp.N(best[0], 3)); return best[1], best[0]
def pari_res(A, B, u0):
    import cypari2; pari = cypari2.Pari(); pari.allocatemem(16 * 10**9)
    R = pari(f'polresultant({sp.sstr(A).replace("**", "^")}, {sp.sstr(B).replace("**", "^")}, t)'); say('PARI resultant in t done; degree in u', pari.poldegree(R, 'u'))
    F = pari.factor(R); best = None
    for i in range(len(F[0])):
        f = F[0][i]; val = abs(complex(pari.subst(f, 'u', pari(str(u0)))))
        if pari.poldegree(f, 'u') > 0 and (best is None or val < best[0]): best = (val, f)
    say('u factor of degree', pari.poldegree(best[1], 'u'), 'value at GF1 u', best[0]); return best
if os.environ.get('MODE') == 'pilot':
    # toy: x = t = u + 1 with u = sqrt(2)+sqrt(5)/5 style relation, two curves through (t0, u0)
    u0 = sp.sqrt(2) + sp.sqrt(5); t0 = u0 + 1
    A = sp.expand((t - u - 1) * (t + 3)); B = sp.expand(u**2 - 2*sp.sqrt(5)*u + 3 + 0*t + (t - u - 1)*0)  # B: u^2 - 2 sqrt5 u + 3 = 0 has root sqrt5+sqrt2
    An = norm_q(A); Bn = norm_q(B + (t - u - 1) * t)
    a, ra = keep(An, sp.N(t0, 50), sp.N(u0, 50), 'A'); b, rb = keep(Bn, sp.N(t0, 50), sp.N(u0, 50), 'B')
    val, f = pari_res(a, b, sp.N(u0, 50))
    ok = val < 1e-20 and str(f).replace(' ', '') in ('u^4-14*u^2+9',)
    print('pilot polynomial:', f); print('FINAL ok' if ok else 'FINAL FAIL: pilot did not recover u^4 - 14u^2 + 9'); sys.exit()
sys.argv = [sys.argv[0]]
src = open('dicto_exact.py').read().split("RU = sp.resultant(RH, RD, t)")[0]
exec(src)   # the same steps as dicto_exact.py up to RH, RD
pickle.dump((sp.srepr(RH), sp.srepr(RD)), open('dicto-exact-RH-RD.pkl', 'wb')); say('RH, RD saved')
GF = json.load(open('golden_family.json'))['GF1']; u0 = sp.Float(GF['u'], 50)
b1, w1 = sp.Float(GF['b']['1']['a'], 50), sp.Float(GF['w']['1']['a'], 50); t0 = b1 / w1
a, ra = keep(norm_q(sp.Poly(RH, t, u)), t0, u0, 'RH'); b, rb = keep(norm_q(sp.Poly(RD, t, u)), t0, u0, 'RD')
val, f = pari_res(a, b, u0)
open('dicto-yantra-exact-u.txt', 'w').write(str(f)); say('written dicto-yantra-exact-u.txt')
print('FINAL ok' if val < 1e-20 and ra < 1e-20 and rb < 1e-20 else 'FINAL FAIL: no factor vanishes at the DICTO Yantra')
