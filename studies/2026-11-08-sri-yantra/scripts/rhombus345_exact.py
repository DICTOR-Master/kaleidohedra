"""The 3-4-5 rhombus yantra, exactly.  Conditions: Huet's (all 18 marmas, 6 corner touches, apex-on-base,
t3 and t7 inscribed) + DICTO's rhombus with diagonals 3 : 4 (u = v = 3/4, so t3 and t7 are congruent with
P = 9/25, R = 16/25, half-widths 12/25: rational) + base corners of t1 and t9 on the circle.
Elimination with resultants (Singular/PARI via passagemath), then an exact number-field tower
K1 = Q(S), K2 = K1(Q) in which b1 and every coordinate is computed and EVERY condition is checked to be
exactly 0 (number-field arithmetic, no floats).  Kulaichev's fourth condition (incircle concentric) is
then measured, not imposed."""
import sys, time
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing, NumberField
import mpmath as mp
from model import solve, all_conditions, MARMAS, CORNERS
T0 = time.time()
def log(*a): print(f'[{time.time()-T0:6.1f}s]', *a, flush=True)

k = QQ(3) / 4
P = k**2 / (1 + k**2); R = 1 / (1 + k**2); w3 = k / (1 + k**2); w7 = k / (1 + k**2)
assert (P, R, w3) == (QQ(9) / 25, QQ(16) / 25, QQ(12) / 25)
Rg = PolynomialRing(QQ, 'Q,S,t'); Qv, Sv, tv = Rg.gens(); F = Rg.fraction_field()
Q, S, t = F(Qv), F(Sv), F(tv)
v = u = F(k)
xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); k3 = w3 / (1 - P)
b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); xZ = k3 * (1 - R); k7 = w7 / R
mA = xZ / (Q - P); c4 = xF / (b8 - Q)
D2 = mA * (P - t) + k7 * (R - t); N2 = mA * Q * (P - t); D4 = c4 * (R - t) + xZ; N4 = c4 * b8 * (R - t) + xZ * t
core = Rg((mA * (P - t) * (Q * D4 - N4) * k7 * Q - w6 * (N4 * D2 - N2 * D4)).numerator())
m1 = xZ * (P - t) / ((R - t) * (Q - P))
Eb = Rg((m1**2 * (Q - t)**2 + t**2 - t).numerator())
w9 = k9 * (S - P)
Ec = Rg((w9**2 + S**2 - S).numerator())

mp.mp.dps = 60
NUM = {'Q': mp.mpf('0.55083606692440806115769475188496404087330329657893'),
       'S': mp.mpf('0.920514060908054173523222345217381391191335145784'),
       't': mp.mpf('0.10272206295244749828362969596133185960971103978954')}

def ev(p):
    names = [str(g) for g in p.parent().gens()]
    tot = mp.mpf(0)
    for mon, c in p.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator())
        for j, e in enumerate(mon):
            if e: term *= NUM[names[j]] ** e
        tot += term
    return tot

def keep(p, label):
    best = None
    for f, m in p.factor():
        if f.degree() == 0: continue
        sz = max(abs(mp.mpf(int(c.numerator())) / int(c.denominator())) for c in f.coefficients())
        rel = abs(ev(f)) / sz
        if best is None or rel < best[0]: best = (rel, f)
    log(f'{label}: kept factor, degrees (Q,S,t) =', [best[1].degree(g) for g in Rg.gens()], ' rel. residual at the numeric point', mp.nstr(best[0], 3))
    return best[1]

pS = keep(Ec, 'Ec (t9 corners on circle)')
pB = keep(Eb, 'Eb (t1 corners on circle)')
pC = keep(core, 'core (Huet closing quadratic)')
rQS = keep(pC.resultant(pB, tv), 'Res_t(core, Eb)')
mQ = keep(rQS.resultant(pS, Sv), 'Res_S -> minimal polynomial of Q')
mT = keep(pC.resultant(pS, Sv).resultant(pB, Qv), 'Res_S, Res_Q -> minimal polynomial of b1')

U = PolynomialRing(QQ, 'x'); x = U.gen()
def uni(p, g):
    d = p.dict(); out = U(0)
    for mon, c in d.items(): out += c * x ** mon[Rg.gens().index(g)]
    return out / out.leading_coefficient()
fS, fQ, fT = uni(pS, Sv), uni(mQ, Qv), uni(mT, tv)
for name, f in (('S = b9', fS), ('Q = b6', fQ), ('b1', fT)):
    den = ZZ(1)
    for c in f.list(): den = den.lcm(QQ(c).denominator())
    fi = (f * den).change_ring(ZZ); fi = fi // fi.content()
    print(f'MINPOLY {name}: degree {fi.degree()}, irreducible {fi.is_irreducible()}:  {fi}')

# exact tower: K1 = Q(S), K2 = K1(Q); then b1 from gcd of the two conditions in t
K1 = NumberField(fS, 'sS'); sS = K1.gen()
Ux = PolynomialRing(K1, 'y'); y = Ux.gen()
gQ = Ux(0)
for mon, c in rQS.dict().items(): gQ += c * sS ** mon[1] * y ** mon[0]
facs = [f for f, m in gQ.factor() if f.degree() > 0]
log('Res_t(core,Eb) over K1 factors into degrees', [f.degree() for f in facs])
results = []
for fQK in facs:
    K2 = K1.extension(fQK, 'qQ') if fQK.degree() > 1 else K1
    qQ = K2.gen() if fQK.degree() > 1 else -fQK[0] / fQK[1]
    sS2 = K2(sS)
    Ut = PolynomialRing(K2, 'z'); z = Ut.gen()
    def sub(p):
        r = Ut(0)
        for mon, c in p.dict().items(): r += c * qQ ** mon[0] * sS2 ** mon[1] * z ** mon[2]
        return r
    g = sub(pC).gcd(sub(pB))
    if g.degree() != 1: continue
    b1 = -g[0] / g[1]
    tri = solve(K2(P), qQ, K2(R), sS2, K2(w3), K2(w7), None, b1=b1)
    conds = all_conditions(tri)
    zero = all(c == 0 for _, c in conds)
    results.append((K2, tri, zero, conds))
    log(f'factor of degree {fQK.degree()}: b1 linear, {len(conds)} conditions all exactly zero: {zero}; absolute degree {K2.absolute_degree()}')
ok = any(z for _, _, z, _ in results)
print('field of definition: degree', [K2.absolute_degree() for K2, _, z, _ in results if z])
print('FINAL ok' if ok else 'FINAL FAIL no exact 3-4-5 rhombus yantra')
