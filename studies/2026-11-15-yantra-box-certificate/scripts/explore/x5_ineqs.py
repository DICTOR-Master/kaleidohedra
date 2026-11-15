"""Exploration: bad boundary points of F~ = 0 in (u, tau, rho) and the admissibility quantities (stripped N/D) at them."""
import sys
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing, RR, RealField, AA, QQbar
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens(); Fr = Rn.fraction_field()
src = {}
for line in open(sys.argv[1]):
    k, e = line.split(' = ', 1); src[k] = Rn(e.strip().replace('^', '**'))
G, H, D = src['G'], src['H1'], src['D']
# --- bad points on tau = 1 ---
Ru = PolynomialRing(QQ, 'U,P'); U, Pp = Ru.gens()
g1 = Ru(G.subs({tau: 1})(U, 1, Pp)); h1 = Ru(H.subs({tau: 1})(U, 1, Pp)); d1 = Ru(D.subs({tau: 1})(U, 1, Pp))
hd = h1.gcd(d1)
print('tau=1: gcd(H,D) factors:', [(f.degree(U), f.degree(Pp), m) for f, m in hd.factor()])
res = g1.resultant(hd, Pp)
print('Res_rho(G, gcd) factors:', [(str(f) if f.degree() < 6 else f'deg {f.degree()}', m) for f, m in res.factor()])
Ruu = PolynomialRing(QQ, 'x')
pts = []
for f, m in res.factor():
    fx = Ruu(f.univariate_polynomial()) if f.degree() > 0 else None
    if fx is None: continue
    for r in fx.roots(AA, multiplicities=False):
        if 0 <= r <= 1:
            # rho values
            gr = PolynomialRing(AA, 'y')(g1(r, PolynomialRing(AA, 'y').gen()))
            for rh in gr.roots(AA, multiplicities=False):
                if hd(r, rh) == 0: pts.append((r, 1, rh))
print('bad points on tau = 1 (u in [0,1]):', [(float(a), b, float(c)) for a, b, c in pts])
# --- admissibility quantities ---
one = Fr(1); t = u * tau; Rv = one / (1 + u**2); S = (1 + rho * (1 - u) * u**2) / (1 + u**2)
v = u; P = v**2 / (1 + v**2); R = Rv; w3 = v / (1 + v**2); w7 = u / (1 + u**2)
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
k3 = w3 / (1 - P); xZ = k3 * (1 - R)
c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: Fr(0)}
w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
Q_ = {}
for i in range(1, 9): Q_[f'b{i+1}-b{i}'] = b[i+1] - b[i]
for i in range(1, 10): Q_[f'w{i}'] = w[i]
for i in range(1, 10): Q_[f'apex{i}'] = (a[i] - b[i]) if i <= 5 else (b[i] - a[i])
for i in (2, 4, 5, 6, 8, 9): Q_[f'disc{i}'] = -(w[i]**2 + b[i]**2 - b[i])
Q_['1/2-b5'] = one / 2 - b5; Q_['Q-1/2'] = Q - one / 2
POS = [u, 1 - u, tau, 1 - tau, 1 + u, rho]
def strip(f):
    f = Rn(f); kept = Rn(f.lc() if f.degree() == 0 else 1); c = 1
    out = Rn(1); sign = 1
    fl = f.factor(); sign = fl.unit()
    for g, m in fl:
        if any(g == p for p in POS) or all(cc > 0 for cc in g.coefficients()): continue
        if any(g == -p for p in POS) or all(cc < 0 for cc in g.coefficients()): sign *= (-1)**m; continue
        if m % 2 == 0: continue        # even power: nonzero at admissible points, sign irrelevant
        out *= g
    return sign * out
qs = {}
for k, q in Q_.items():
    N = strip(q.numerator()); Dd = strip(q.denominator()); qs[k] = (N, Dd)
    print(f'{k}: N deg {N.degree()} ({len(N.monomials())} terms), D deg {Dd.degree()} ({len(Dd.monomials())} terms)')
bad = [(QQ(0), QQ(0), QQ(1)), (QQ(1), QQ(1), QQ(2))] + pts
for p in bad:
    print('point', [float(x) for x in p])
    for k, (N, Dd) in qs.items():
        n = N(*p); d = Dd(*p)
        tag = 'VIOLATED' if (n != 0 and d != 0 and (n > 0) != (d > 0)) else ('0/0' if n == 0 and d == 0 else ('N=0' if n == 0 else ('D=0' if d == 0 else 'ok')))
        if tag != 'ok': print(f'    {k}: {tag}  N={float(n):.4g} D={float(d):.4g}')
import pickle
pickle.dump({k: (str(N), str(Dd)) for k, (N, Dd) in qs.items()}, open(sys.argv[2], 'wb'))
