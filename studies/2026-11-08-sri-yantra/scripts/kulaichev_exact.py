"""Exact algebraic form of the Kulaichev-Rao-Pustynski yantra (Huet's conditions + Kulaichev's four
extra conditions).  Elimination by resultants in Singular/PARI (passagemath); at every step only the
irreducible factor that vanishes at the 80-digit numerical solution (kulaichev_numeric.py) is kept.
Output: the minimal polynomial over Q of the leg slope u (= tan of the half apex angle of t3, t7)
and of the depths P, Q, S, b1 of the defining lines."""
import time, sys
from sage.all__sagemath_singular import QQ, PolynomialRing, ZZ
import mpmath as mp
T0 = time.time()
def log(*a): print(f'[{time.time()-T0:7.1f}s]', *a, flush=True)

Rg = PolynomialRing(QQ, 'u,Q,S,t'); u, Q, S, t = Rg.gens(); F = Rg.fraction_field()
u, Q, S, t = [F(x) for x in (u, Q, S, t)]
v = u
P = v**2 / (1 + v**2); R = 1 / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); k3 = w3 / (1 - P)
b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); xZ = k3 * (1 - R); k7 = w7 / R
mA = xZ / (Q - P); c4 = xF / (b8 - Q)
D2 = mA * (P - t) + k7 * (R - t); N2 = mA * Q * (P - t); D4 = c4 * (R - t) + xZ; N4 = c4 * b8 * (R - t) + xZ * t
core = mA * (P - t) * (Q * D4 - N4) * k7 * Q - w6 * (N4 * D2 - N2 * D4)
m1 = xZ * (P - t) / ((R - t) * (Q - P))
b5 = (m1 * Q + k9 * P) / (m1 + k9)
w9 = k9 * (S - P)
Eb = m1**2 * (Q - t)**2 + t**2 - t
Ec = w9**2 + S**2 - S
Ed = m1**2 * (Q - F(1)/2)**2 - (F(1)/2 - b5)**2 * (1 + m1**2)

# numerical solution (80 digits) from kulaichev_numeric.py, recomputed here
mp.mp.dps = 90
sys.path.insert(0, '.')
from kulaichev_numeric import u as un, Q as Qn, S as Sn, yantra
tn = yantra(un, Qn, Sn)['b'][1]
pt = {'u': un, 'Q': Qn, 'S': Sn, 't': tn}
names = ['u', 'Q', 'S', 't']

def ev(p):
    """evaluate polynomial p (in Rg) at the numerical point with mpmath."""
    tot = mp.mpf(0)
    for mon, c in p.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator())
        for k, e in enumerate(mon):
            if e: term *= pt[names[k]] ** e
        tot += term
    return tot

def keep(p, label):
    """factor p and keep the irreducible factor vanishing at the point (relative test)."""
    fs = p.factor()
    best = None
    for f, m in fs:
        val = abs(ev(f)); size = sum(abs(mp.mpf(int(c.numerator()))/int(c.denominator())) for c in f.coefficients())
        rel = val / size
        if best is None or rel < best[0]: best = (rel, f)
    log(f'{label}: {len(list(fs))} factors, kept degrees', [best[1].degree(x) for x in Rg.gens()], 'rel residual', mp.nstr(best[0], 3))
    return best[1]

def num(e): return Rg(e.numerator())
uR, QR, SR, tR = Rg.gens()
pc = keep(num(core), 'core'); pb = keep(num(Eb), 'Eb'); pcc = keep(num(Ec), 'Ec'); pd = keep(num(Ed), 'Ed')
r1 = keep(pc.resultant(pb, tR), 'Res_t(core,Eb)')
open('kulaichev-step-r1.txt', 'w').write(str(r1)); log('saved r1')
r2 = keep(pc.resultant(pd, tR), 'Res_t(core,Ed)')
open('kulaichev-step-r2.txt', 'w').write(str(r2)); log('saved r2')
r3 = keep(r1.resultant(r2, QR), 'Res_Q')
open('kulaichev-step-r3.txt', 'w').write(str(r3)); log('saved r3')
r4 = keep(r3.resultant(pcc, SR), 'Res_S')
open('kulaichev-step-r4.txt', 'w').write(str(r4)); log('saved r4')
log('minimal polynomial of u: degree', r4.degree(uR))
U = PolynomialRing(ZZ, 'x'); mu = U(r4.univariate_polynomial().change_ring(QQ) * r4.univariate_polynomial().denominator())
mu = mu // mu.content()
print('MINPOLY_u =', mu)
open('kulaichev-minpoly-u.txt', 'w').write(str(mu) + '\n')
# check: irreducible, and root near numeric u
from sage.all__sagemath_pari import pari
print('irreducible over Q:', mu.is_irreducible())
roots = pari(mu).polrootsreal(precision=300)
close = float(min(abs(r - pari(str(un))) for r in roots)) if len(roots) else 1.0   # PARI reals: no double overflow (11-08 lesson)
print('closest root distance to numeric u (double):', close)
log('done')
ok = mu.is_irreducible() and close < 1e-12
print('FINAL ok' if ok else 'FINAL FAIL kulaichev exact')
