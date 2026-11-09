"""G1 exactly (DICTO 10 Nov 2026: 'computing their exact forms'). G1 = the Cleo-Octangula (u = 2/phi^2 = 3 - sqrt5 above,
v = 1/sqrt2 below) with (b) t1's corners on the circle and (d) the bindu centred. Natural coordinates (natural.py, Theorem 6):
t1's corner = (t/(1+t^2), t^2/(1+t^2)), so (b) holds by construction; unknowns t, S. Equations: H1(t, S) = 0 (closing equation,
the degree-10 factor) and D(t, S) = 0 (bindu centred, squared; formulas of the audit's stage4_elim.py). Eliminate S, take the
norm from Q(sqrt2, sqrt5) to Q, factor, keep the factor through G1's stored t. Writes g1-minpoly-t.txt; FINAL ok/FAIL.
usage (dicto-big-brother, in a folder holding natural.py and model.py): ~/geom/bin/python -u g1_exact.py"""
import sys, time, io, contextlib
sys.path.insert(0, '.')
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
import sympy as sp
t, S = N.t, N.S
Hm = [f for f, m in sp.factor_list(N.H)[1] if sp.degree(f, t) == 10][0]
from sage.all__sagemath_singular import QQ, PolynomialRing
Rg = PolynomialRing(QQ, 'w,r,t,S'); W, Rr, Tt, SS = Rg.gens(); Fr = Rg.fraction_field()
R5 = PolynomialRing(QQ, 'u,v,t,S'); U5, V5 = R5.gens()[:2]
UV = {'u': 3 - W, 'v': Rr / 2}
red = lambda F: F.reduce([W**2 - 5, Rr**2 - 2])
def to_sage(e):
    F5 = R5(sp.sstr(sp.expand(e)).replace('**', '^'))
    return red(F5(3 - W, Rr / 2, Tt, SS))
H1 = to_sage(Hm); say('H1 built: degrees t, S', H1.degree(Tt), H1.degree(SS))
Fu, Fv = Fr(3 - W), Fr(Rr) / 2; one = Fr(1)
Pf = Fv**2 / (1 + Fv**2); Rf = one / (1 + Fu**2); w3f = Fv / (1 + Fv**2); w7f = Fu / (1 + Fu**2)
xWf = w7f * Pf / Rf; k3f = w3f / (1 - Pf)
Qn_, Qd_ = sp.fraction(sp.factor(N.Q)); Qf = Fr(to_sage(Qn_)) / Fr(to_sage(Qd_))
xXf = xWf * (SS - Rf) / (SS - Pf); k9f = xXf / (Rf - Pf)
b1f = Tt**2 / (1 + Tt**2); w1f = Tt / (1 + Tt**2); m1f = w1f / (Qf - b1f)
b5f = (m1f * Qf + k9f * Pf) / (m1f + k9f); hf = Qf - b5f; hwf = m1f * hf; cf = one / 2 - b5f
Dexpr = (hwf**2 + hf**2) * cf**2 - (hwf * hf - hwf * cf)**2
D1 = red(Rg(Dexpr.numerator())); say('D built: degrees t, S', D1.degree(Tt), D1.degree(SS))
import mpmath as mp
mp.mp.dps = 60
b1n = mp.mpf('0.07143114981382940633887064757549777559436'); tn = mp.sqrt(b1n / (1 - b1n))
wn, rn = mp.sqrt(5), mp.sqrt(2)
def ev(F, tt, ss=None):
    tot = mp.mpf(0); size = mp.mpf(0)
    for e, c in F.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator()) * wn**e[0] * rn**e[1] * tt**e[2] * (ss**e[3] if ss is not None else 1)
        tot += term; size += abs(term)
    return abs(tot) / (size or 1)
R = red(H1.resultant(D1, SS)); say('Res_S(H1, D): degrees t, w, r', R.degree(Tt), R.degree(W), R.degree(Rr))
Nr = red(R * R.subs({Rr: -Rr})); Nw = red(Nr * Nr.subs({W: -W})); assert Nw.degree(W) <= 0 and Nw.degree(Rr) <= 0
say('norm to Q: degree in t', Nw.degree(Tt))
best = None
for fac, m in Nw.factor():
    if fac.degree(Tt) == 0: continue
    val = ev(fac, tn); say(f'  factor degree {fac.degree(Tt)}^{m}: relative value at G1 {mp.nstr(val, 3)}')
    if best is None or val < best[0]: best = (val, fac)
val, f = best
open('g1-minpoly-t.txt', 'w').write(str(f) + '\n')
say('G1: t is a root of an irreducible polynomial of degree', f.degree(Tt), '; residual', mp.nstr(val, 3))
print('FINAL ok' if val < mp.mpf(10)**-40 else 'FINAL FAIL: no factor vanishes at G1')
