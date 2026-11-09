"""Exact slope u* of the rhombus threshold (DICTO 10 Nov 2026). Family u = v with (b) (natural coordinate t) and (c) (G(S) = 0);
the tiny extra pieces are born where t4's right leg, t5's base and t6's right leg meet: C(u, t, S) = 0 (det3, model.py).
Eliminate S (Res_S of G with H1 and with C), then t (PARI), factor, keep the factor through u* = 0.745996537184295...
usage (dicto-big-brother): ~/geom/bin/python -u threshold_exact.py"""
import sys, time, io, contextlib
sys.path.insert(0, '.')
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
import sympy as sp
from model import solve, det3
Hm = [f for f, m in sp.factor_list(N.H)[1] if sp.degree(f, N.t) == 10][0]
from sage.all__sagemath_singular import QQ, PolynomialRing, pari
Rg = PolynomialRing(QQ, 'u,t,S'); U, Tt, SS = Rg.gens(); Fr = Rg.fraction_field()
R4 = PolynomialRing(QQ, 'u,v,t,S')
def to_sage(e): return Rg(R4(sp.sstr(sp.expand(e)).replace('**', '^'))(U, U, Tt, SS))
G = to_sage(N.G); H1 = to_sage(Hm)
Qn_, Qd_ = sp.fraction(sp.factor(N.Q)); Qf = Fr(to_sage(Qn_)) / Fr(to_sage(Qd_))
u = Fr(U); one = Fr(1)
P = u**2 / (1 + u**2); R = one / (1 + u**2); w = u / (1 + u**2)
tri = solve(P, Qf, R, Fr(SS), w, w, None, b1=Fr(Tt)**2 / (1 + Fr(Tt)**2))
b, ww, a = tri['b'], tri['w'], tri['a']
Cx = det3(((ww[4], b[4]), (0, a[4])), ((-ww[5], b[5]), (ww[5], b[5])), ((ww[6], b[6]), (0, a[6])))
C = Rg(Fr(Cx).numerator()); say('G, H1, C built; degrees in S', G.degree(SS), H1.degree(SS), C.degree(SS), '; C terms', len(C.monomials()))
import mpmath as mp
mp.mp.dps = 60
un = mp.mpf('0.74599653718429518158585978727747621288024776478302')
def ev(F, pt):
    tot = mp.mpf(0); size = mp.mpf(0)
    for e, c in F.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator()) * mp.mpf(1)
        for x, k in zip(pt, e): term *= x**k
        tot += term; size += abs(term)
    return abs(tot) / (size or 1)
def through(F, pt, name):
    best = None
    for fac, m in F.factor():
        if fac.degree() == 0: continue
        vv = ev(fac, pt); say(f'  {name} factor degrees {[fac.degree(g) for g in Rg.gens()]}^{m}: value {mp.nstr(vv, 3)}')
        if best is None or vv < best[0]: best = (vv, fac)
    return best[1]
import json
th = json.load(open('rhombus-threshold.json')); Sn = mp.mpf(th['S']); Qn = mp.mpf(th['Q'])
from rhombus import yantra
b1n = yantra(un, un, Qn, Sn)['b'][1]; tn = mp.sqrt(b1n / (1 - b1n))
say('t at u*:', mp.nstr(tn, 20), '; b1 =', mp.nstr(tn**2 / (1 + tn**2), 15), '; C there', mp.nstr(ev(C, (un, tn, Sn)), 3))
R1 = G.resultant(H1, SS); say('R1 = Res_S(G, H1) degrees (u, t)', R1.degree(U), R1.degree(Tt))
R2 = G.resultant(C, SS); say('R2 = Res_S(G, C) degrees (u, t)', R2.degree(U), R2.degree(Tt))
A1 = through(R1, (un, tn, Sn), 'R1'); A2 = through(R2, (un, tn, Sn), 'R2')
Rt = pari(str(A1).replace('^', '^')).polresultant(pari(str(A2)), 't'); say('Res_t done, degree in u', pari.poldegree(Rt, 'u'))
fl = pari.factor(Rt); best = None
for i in range(len(fl[0])):
    f = fl[0][i]; d = int(pari.poldegree(f, 'u'))
    if d == 0: continue
    vv = abs(pari.subst(f, 'u', pari(mp.nstr(un, 55)))) ; say(f'  Res_t factor degree {d}^{fl[1][i]}')
    roots = [abs(complex(r) - float(un)) for r in pari.polroots(f)] if d < 400 else [1]
    dist = min(roots); best = (dist, f, d) if best is None or dist < best[0] else best
dist, f, d = best
open('threshold-minpoly-u.txt', 'w').write(str(f) + '\n')
say(f'u* is a root of a factor of degree {d}; nearest root at distance {dist:.2e}; even: {all(int(pari.polcoef(f, k, "u")) == 0 for k in range(1, d, 2))}')
print('FINAL ok' if dist < 1e-12 else 'FINAL FAIL: no factor through u*')
