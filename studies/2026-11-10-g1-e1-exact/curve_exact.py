"""Exact threshold curve T(u, v) = 0 (DICTO 10 Nov 2026). Two-slope family with (b) (natural coordinate t) and (c) (G = 0); the
threshold meeting C = det(t4 right leg, t5 base, t6 right leg). Eliminate S (Singular), keep the factors through the point
u = v = u*, then eliminate t (Singular resultant), factor, keep the factor through u = v = u*. Writes curve-T.txt.
usage: python -u curve_exact.py"""
import sys, time, io, contextlib
sys.path.insert(0, '.')
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
import sympy as sp
from model import solve, det3
Hm = [f for f, m in sp.factor_list(N.H)[1] if sp.degree(f, N.t) == 10][0]
from sage.all__sagemath_singular import QQ, PolynomialRing
Rg = PolynomialRing(QQ, 'u,v,t,S'); U, V, Tt, SS = Rg.gens(); Fr = Rg.fraction_field()
def to_sage(e): return Rg(sp.sstr(sp.expand(e)).replace('**', '^'))
G = to_sage(N.G); H1 = to_sage(Hm)
Qn_, Qd_ = sp.fraction(sp.factor(N.Q)); Qf = Fr(to_sage(Qn_)) / Fr(to_sage(Qd_))
u, v = Fr(U), Fr(V); one = Fr(1)
P = v**2 / (1 + v**2); R = one / (1 + u**2)
tri = solve(P, Qf, R, Fr(SS), v / (1 + v**2), u / (1 + u**2), None, b1=Fr(Tt)**2 / (1 + Fr(Tt)**2))
b, ww, a = tri['b'], tri['w'], tri['a']
C = Rg(Fr(det3(((ww[4], b[4]), (0, a[4])), ((-ww[5], b[5]), (ww[5], b[5])), ((ww[6], b[6]), (0, a[6])))).numerator())
say('built: degrees in S', G.degree(SS), H1.degree(SS), C.degree(SS), '; C terms', len(C.monomials()))
import mpmath as mp, json
mp.mp.dps = 60
th = json.load(open('rhombus-threshold.json')); un = mp.mpf(th['u_star']); Sn = mp.mpf(th['S']); Qn = mp.mpf(th['Q'])
from rhombus import yantra
b1n = yantra(un, un, Qn, Sn)['b'][1]; tn = mp.sqrt(b1n / (1 - b1n)); pt = (un, un, tn, Sn)
def ev(F):
    tot = mp.mpf(0); size = mp.mpf(0)
    for e, c in F.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator())
        for x, k in zip(pt, e): term *= x**k
        tot += term; size += abs(term)
    return abs(tot) / (size or 1)
def through(F, name):
    best = None
    for fac, m in F.factor():
        if fac.degree() == 0: continue
        val = ev(fac); say(f'  {name} factor degrees (u,v,t) {fac.degree(U)},{fac.degree(V)},{fac.degree(Tt)}: {mp.nstr(val, 3)}')
        if best is None or val < best[0]: best = (val, fac)
    return best[1]
R1 = G.resultant(H1, SS); say('R1 degrees (u,v,t)', R1.degree(U), R1.degree(V), R1.degree(Tt), 'terms', len(R1.monomials()))
A1 = through(R1, 'R1')
R2 = G.resultant(C, SS); say('R2 degrees (u,v,t)', R2.degree(U), R2.degree(V), R2.degree(Tt), 'terms', len(R2.monomials()))
A2 = through(R2, 'R2')
open('curve-A1A2.txt', 'w').write(f'A1 = {A1}\nA2 = {A2}\n'); say('saved A1, A2; eliminating t')
Rt = A1.resultant(A2, Tt); say('Res_t degrees (u, v)', Rt.degree(U), Rt.degree(V), 'terms', len(Rt.monomials()))
Tc = through(Rt, 'Res_t')
open('curve-T.txt', 'w').write(str(Tc) + '\n')
say('T(u, v): degrees', Tc.degree(U), Tc.degree(V), 'total', Tc.total_degree(), 'terms', len(Tc.monomials()), 'symmetric in u, v:', Tc == Tc.subs({U: V, V: U}))
print('FINAL ok' if ev(Tc) < mp.mpf(10)**-40 else 'FINAL FAIL')
