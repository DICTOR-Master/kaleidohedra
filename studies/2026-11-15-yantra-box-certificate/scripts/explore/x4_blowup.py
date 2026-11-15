"""Exploration: F in the coordinates (u, tau, rho): t = u*tau, S = R + rho*(1-u)*(1-R).  Strip factors positive on the open box; look at faces."""
import sys
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
R3 = PolynomialRing(QQ, 'u,t,S'); u0, t0, S0 = R3.gens()
src = {}
for line in open(sys.argv[1]):
    k, e = line.split(' = ', 1); src[k] = R3(e.strip().replace('^', '**'))
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens(); Fr = Rn.fraction_field()
Rv = 1 / (1 + u**2); Sv = Fr(1 + rho * (1 - u) * u**2) / (1 + u**2)
POS = [u, 1 - u, tau, 1 - tau, 1 + u, 1 + u**2]
def strip(f):
    f = Rn(f); kept = Rn(1); dropped = []
    for g, m in f.factor():
        if g.degree() == 0: continue
        if any(g == p or g == -p for p in POS) or all(c > 0 for c in g.coefficients()): dropped.append((g, m)); 
        else: kept *= g**m
    return kept, dropped
out = {}
for k in ('G', 'H1', 'D'):
    f = src[k]; dS = f.degree(S0)
    g = Fr(f(u, u * tau, Sv)) * (1 + u**2)**dS
    assert g.denominator().degree() == 0
    kept, dropped = strip(g.numerator())
    out[k] = kept
    print(k, 'degrees (u,tau,rho):', kept.degree(u), kept.degree(tau), kept.degree(rho), ' terms', len(kept.monomials()), ' dropped', [(str(a), m) for a, m in dropped], ' kept factors', [(p.degree(u), p.degree(tau), p.degree(rho), m) for p, m in kept.factor()])
    print('   max coefficient digits', max(len(str(abs(c))) for c in kept.coefficients()))
G, H, D = out['G'], out['H1'], out['D']
for name, sub in (('u=0', {u: 0}), ('u=1', {u: 1}), ('tau=0', {tau: 0}), ('tau=1', {tau: 1}), ('rho=0', {rho: 0})):
    g, h, d = [Rn(x.subs(sub)) for x in (G, H, D)]
    print(name, ': G ->', g.factor() if g.degree() < 12 and g != 0 else ('0' if g == 0 else f'deg {g.degree()}'), '; H zero', h == 0, '; D zero', d == 0)
    print('    gcd(G,H) =', str(g.gcd(h))[:150], '; gcd(G,D) =', str(g.gcd(d))[:150], '; gcd(H,D) =', str(h.gcd(d))[:200])
open(sys.argv[2], 'w').write(f'G = {G}\nH1 = {H}\nD = {D}\n')
