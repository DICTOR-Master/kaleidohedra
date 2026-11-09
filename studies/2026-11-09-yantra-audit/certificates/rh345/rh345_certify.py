"""Certified count for Rh345, DICTO's 3-4-5 rhombus yantra (DICTO 10 Nov 2026: 'certify the 3-4-5 rhombus count').
Same standard as Propositions 3 and 11 (Kulaichev's yantra). u = v = 3/4 exactly, so P = 9/25, R = 16/25, w3 = w7 = 12/25.
Step 1 (this script): the system  core = 0 (Huet's closing equation), Eb = 0 (t1's corners on the circle), Ec = 0 (t9's corners
on the circle)  in (Q, S, t), t = b1, is the one of rhombus345_exact.py (which checks every condition exactly in the number field).
Interval Newton (Krawczyk) at 560 digits proves it has exactly one solution in a small box around the numerical yantra, and
encloses it. Step 2: every base depth, half-width and apex is rebuilt from that box by model.solve in interval arithmetic and
written as stage5-K.json (Rh345 has u = v, so the symbolic model of case K applies unchanged). Step 3: certified_counts.py K.
usage (in ~/yantra-audit/rh345 with model.py): python -u rh345_certify.py"""
import sys, json, time
sys.path.insert(0, '.')
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
from sage.all__sagemath_singular import QQ, PolynomialRing
import mpmath as mp
from mpmath import iv
from model import solve
mp.mp.dps = 560; iv.dps = 560
Rg = PolynomialRing(QQ, 'Q,S,t'); Qv, Sv, tv = Rg.gens(); F = Rg.fraction_field()
Q, S, t = F(Qv), F(Sv), F(tv)
k = QQ(3) / 4
P = k**2 / (1 + k**2); R = 1 / (1 + k**2); w3 = k / (1 + k**2); w7 = k / (1 + k**2)
xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); k3 = w3 / (1 - P)
b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); xZ = k3 * (1 - R); k7 = w7 / R
mA = xZ / (Q - P); c4 = xF / (b8 - Q)
D2 = mA * (P - t) + k7 * (R - t); N2 = mA * Q * (P - t); D4 = c4 * (R - t) + xZ; N4 = c4 * b8 * (R - t) + xZ * t
core = Rg((mA * (P - t) * (Q * D4 - N4) * k7 * Q - w6 * (N4 * D2 - N2 * D4)).numerator())
m1 = xZ * (P - t) / ((R - t) * (Q - P))
Eb = Rg((m1**2 * (Q - t)**2 + t**2 - t).numerator())
Ec = Rg(((k9 * (S - P))**2 + S**2 - S).numerator())
Fs = [core, Eb, Ec]; J = [[f.derivative(g) for g in Rg.gens()] for f in Fs]
say('system built; degrees', [f.total_degree() for f in Fs])
def ev(p, X):
    tot = 0
    for mon, c in p.dict().items():
        term = iv.mpf(int(c.numerator())) / int(c.denominator()) if isinstance(X[0], iv.mpf.__class__) or True else 0
        for x, e in zip(X, mon):
            if e: term = term * x**e
        tot = tot + term
    return tot
m0 = [mp.mpf('0.55083606692440806115769475188496404087330329657893'), mp.mpf('0.920514060908054173523222345217381391191335145784'),
      mp.mpf('0.10272206295244749828362969596133185960971103978954')]
# Newton refinement in plain multiprecision to ~550 digits
def evf(p, X):
    tot = mp.mpf(0)
    for mon, c in p.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator())
        for x, e in zip(X, mon):
            if e: term *= x**e
        tot += term
    return tot
for it in range(12):
    Fv = mp.matrix([evf(f, m0) for f in Fs]); Jv = mp.matrix([[evf(d, m0) for d in row] for row in J])
    step = mp.lu_solve(Jv, Fv); m0 = [m0[i] - step[i] for i in range(3)]
    if mp.norm(step) < mp.mpf(10)**-545: break
say('Newton done, last step', mp.nstr(mp.norm(step), 3))
# Krawczyk test on the box m0 +- r
r = mp.mpf(10)**-480
X = [iv.mpf([m0[i] - r, m0[i] + r]) for i in range(3)]
Jm = mp.matrix([[evf(d, m0) for d in row] for row in J]); Y = mp.inverse(Jm)
Fm = [ev(f, [iv.mpf(m) for m in m0]) for f in Fs]
JX = [[ev(d, X) for d in row] for row in J]
K = []
for i in range(3):
    s = iv.mpf(m0[i])
    for j in range(3): s -= iv.mpf(Y[i, j]) * Fm[j]
    for j in range(3):
        c = (1 if i == j else 0) - sum((iv.mpf(Y[i, l]) * JX[l][j] for l in range(3)), iv.mpf(0))
        s += c * (X[j] - iv.mpf(m0[j]))
    K.append(s)
inside = all(K[i].a > X[i].a and K[i].b < X[i].b for i in range(3))
wid = max(K[i].delta for i in range(3))
say('Krawczyk: K inside X:', inside, '; enclosure width', mp.nstr(mp.mpf(wid), 3))
if not inside: raise SystemExit('FINAL FAIL: Krawczyk test not passed')
Qi, Si, ti = K
fr = lambda q: iv.mpf(int(q.numerator())) / int(q.denominator())
tri = solve(fr(P), Qi, fr(R), Si, fr(w3), fr(w7), None, b1=ti)
for d in ('b', 'w', 'a'):
    for i in tri[d]:
        if not isinstance(tri[d][i], type(Qi)): tri[d][i] = iv.mpf(int(tri[d][i])) if tri[d][i] in (0, 1) else fr(QQ(tri[d][i]))
PAD = mp.mpf(10)**-555   # round OUTWARD: printed ends must still enclose the true value (first run rounded to nearest and failed)
fmt = lambda z: [mp.nstr(mp.make_mpf(z._mpi_[0]) - PAD, 558, strip_zeros=False), mp.nstr(mp.make_mpf(z._mpi_[1]) + PAD, 558, strip_zeros=False)]
out = {'case': 'Rh345', 'digits': 560, 'u': '3/4', 'v': '3/4',
       'b': {str(i): fmt(z) for i, z in tri['b'].items()}, 'w': {str(i): fmt(z) for i, z in tri['w'].items()},
       'a': {str(i): fmt(z) for i, z in tri['a'].items()}, 'box': [fmt(z) for z in K]}
json.dump(out, open('stage5-K.json', 'w'))
say('stage5-K.json written (Rh345 enclosures); Q', mp.nstr(mp.mpf(Qi.mid), 20), 'S', mp.nstr(mp.mpf(Si.mid), 20), 'b1', mp.nstr(mp.mpf(ti.mid), 20))
print('FINAL ok' if inside and wid < mp.mpf(10)**-550 else 'FINAL FAIL: Krawczyk box not certified')
