"""Stage 4: an independent elimination, in Singular (via sage) and PARI, in natural coordinates, for both cases.
usage: python -u stage4_elim.py D|K
Unknowns u, t, S (t: t1's corner is the circle point (t/(1+t^2), t^2/(1+t^2)), so (b) holds by construction; Q = Q(t) by the
marma (1,3,8), natural.py). Equations, all from natural.py / dicto_exact.py unchanged:
   G(S) = 0 (condition (c)),  H1(t, S) = 0 (closing equation, the degree-10 factor),  D(t, S) = 0 (bindu centred, squared)
with v = u (case K, Kulaichev's (a)) or v = p/u, p = 2/phi^3 = 2w - 4, w = sqrt5 (case D).
R1 = Res_S(G, H1), R2 = Res_S(G, D) (Singular); case D: norms over Q(sqrt5), N(R) = R(w) R(-w) mod w^2 - 5. Each is factored
(Singular) and every factor is saved. Then R = Res_t(a, b) of the factors a, b through the numerical point (PARI), factored
(PARI). Pass: the stored minimal polynomial f (Theorem 9 / 10) is one of the factors of R, up to a constant.
The proof that f(u0) = 0 uses these factor lists in stage 5 (every other factor is shown nonzero at the certified solution).
Writes stage4-<case>.txt (factor lists) and prints FINAL ok / FINAL FAIL."""
import sys, time, json, io, contextlib
sys.path.insert(0, '.')
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
case = sys.argv[1]
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
import sympy as sp
u, v, t, S = N.u, N.v, N.t, N.S
Hm = [f for f, m in sp.factor_list(N.H)[1] if sp.degree(f, t) == 10][0]
say('G, H1 taken from natural.py (sympy)')
from sage.all__sagemath_singular import QQ, PolynomialRing
Rg = PolynomialRing(QQ, 'w,u,t,S'); W, U, Tt, SS = Rg.gens(); Fr = Rg.fraction_field()
R5 = PolynomialRing(QQ, 'w,u,v,t,S'); V5 = R5.gens()[2]
def to_sage(e):
    F5 = R5(sp.sstr(sp.expand(e)).replace('**', '^'))          # Singular's own parser
    dv = F5.degree(V5)
    out = Rg(0)
    for k in range(dv + 1):                                     # F5 = sum_k c_k v^k
        ck = F5.coefficient({V5: k})
        ck = Rg(str(ck)) if ck != 0 else Rg(0)
        if case == 'K': out += ck * U**k
        else: out += ck * (2 * W - 4)**k * U**(dv - k)          # v = (2w - 4)/u, times u^dv
    if case == 'K': return out
    return out
red = lambda F: F.reduce([W**2 - 5]) if case == 'D' else F
G1, H1 = (red(to_sage(e)) for e in (N.G, Hm))
# bindu condition, the same formulas as dicto_exact.py, built in Singular's fraction field (sympy is too slow here)
Fv = (U if case == 'K' else (2 * W - 4) / Fr(U)); one = Fr(1)
Pf = Fv**2 / (1 + Fv**2); Rf = one / (1 + U**2); w3f = Fv / (1 + Fv**2); w7f = U / (1 + U**2)
xWf = w7f * Pf / Rf; k3f = w3f / (1 - Pf)
Qn_, Qd_ = sp.fraction(sp.factor(N.Q)); Qf = Fr(to_sage(Qn_)) / Fr(to_sage(Qd_))
xXf = xWf * (SS - Rf) / (SS - Pf); k9f = xXf / (Rf - Pf)
b1f = Tt**2 / (1 + Tt**2); w1f = Tt / (1 + Tt**2); m1f = w1f / (Qf - b1f)
b5f = (m1f * Qf + k9f * Pf) / (m1f + k9f); hf = Qf - b5f; hwf = m1f * hf; cf = one / 2 - b5f
Dexpr = (hwf**2 + hf**2) * cf**2 - (hwf * hf - hwf * cf)**2
D1 = red(Dexpr.numerator()); Dden = Dexpr.denominator()
open(f'stage4-{case}-Dden.txt', 'w').write(''.join(f'{fa}\n' for fa, m in Dden.factor()))
say('D built in Singular')
say('in Singular: degrees in S', G1.degree(SS), H1.degree(SS), D1.degree(SS), '; terms', len(G1.monomials()), len(H1.monomials()), len(D1.monomials()))
open(f'stage4-{case}-system.txt', 'w').write(f'G = {G1}\nH1 = {H1}\nD = {D1}\n')
R1 = red(G1.resultant(H1, SS)); say('R1 = Res_S(G, H1): degrees (t, u, w)', R1.degree(Tt), R1.degree(U), R1.degree(W))
R2 = red(G1.resultant(D1, SS)); say('R2 = Res_S(G, D):  degrees (t, u, w)', R2.degree(Tt), R2.degree(U), R2.degree(W))
def norm(F):
    if case == 'K': return F
    Fm = F.subs({W: -W}); return (F * Fm).reduce([W**2 - 5])
N1, N2 = norm(R1), norm(R2)
assert N1.degree(W) <= 0 and N2.degree(W) <= 0
say('norms over Q(sqrt5) (case D) done: degrees (t, u)', (N1.degree(Tt), N1.degree(U)), (N2.degree(Tt), N2.degree(U)))
import mpmath as mp
mp.mp.dps = 80
st1 = json.load(open(f'stage1-{case}.json')); un = mp.mpf(st1['u_1000_digits'][:90])
tn = {'D': mp.mpf('0.04397772610421809944376588907842364688956'), 'K': mp.mpf('0.103270075308203946272572702702691751496327239362942147553129')}[case]
tn = mp.sqrt(tn / (1 - tn))                                 # b1 = t^2/(1+t^2), t > 0
def ev(F, uu, tt):
    tot = mp.mpf(0); size = mp.mpf(0)
    for (ew, eu, et, es), cf in F.dict().items():
        term = mp.mpf(int(cf.numerator())) / int(cf.denominator()) * uu**eu * tt**et
        tot += term; size += abs(term)
    return abs(tot) / size
out = io.StringIO()
kept = []
for name, F in (('N1', N1), ('N2', N2)):
    t1 = time.time(); fl = F.factor(); say(f'{name} factored in {time.time() - t1:.1f} s')
    rows = []
    for fac, m in fl:
        val = ev(fac, un, tn) if fac.degree() > 0 else mp.mpf(1)
        rows.append((val, fac, m))
        out.write(f'{name} factor (t-degree {fac.degree(Tt)}, u-degree {fac.degree(U)}, multiplicity {m}): {fac}\n')
        say(f'   factor degrees (t, u) = ({fac.degree(Tt)}, {fac.degree(U)})^{m}, relative value at the numerical point {mp.nstr(val, 3)}')
    best = min(rows, key=lambda r: r[0]); kept.append(best[1])
    say(f'   kept: degrees ({best[1].degree(Tt)}, {best[1].degree(U)})')
open(f'stage4-{case}.txt', 'w').write(out.getvalue())
import cypari2
pari = cypari2.Pari(); pari.allocatemem(16 * 10**9)
A = pari(str(kept[0]).replace('t', 'z')); B = pari(str(kept[1]).replace('t', 'z'))
open(f'stage4-{case}-kept.txt', 'w').write(f'a = {kept[0]}\nb = {kept[1]}\n')
t1 = time.time(); Rt = pari.polresultant(A, B, 'z'); say(f'PARI Res_t(a, b): degree {pari.poldegree(Rt, "u")} in u ({time.time() - t1:.1f} s)')
t1 = time.time(); Fz = pari.factor(Rt); say(f'PARI factored in {time.time() - t1:.1f} s:', [(int(pari.poldegree(Fz[0][i], 'u')), int(Fz[1][i])) for i in range(len(Fz[0]))])
f = pari(open({'D': 'dicto-yantra-exact-u.txt', 'K': 'kulaichev-minpoly-u.txt'}[case]).read().strip().replace('x', 'u'))
found = any(pari.poldegree(Fz[0][i], 'u') == pari.poldegree(f, 'u') and pari.pollead(f, 'u') * Fz[0][i] == pari.pollead(Fz[0][i], 'u') * f for i in range(len(Fz[0])))
with open(f'stage4-{case}-Rfactors.txt', 'w') as fh:
    for i in range(len(Fz[0])): fh.write(f'{Fz[1][i]} {Fz[0][i]}\n')
say('the stored f is a factor of Res_t(a, b):', found)
print('FINAL ok' if found else 'FINAL FAIL: the stored polynomial is not a factor of the new eliminant')
