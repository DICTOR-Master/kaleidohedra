"""Step 4b: semantic control of the derivation (b1_polys.py, b1_charts.py), independent of Sage: at the centre of every leaf (exact
rationals) the yantra is rebuilt from the geometry (the construction of studies/2026-11-15-yantra-uniqueness, s3_backsolve.py) and
  T leaf: the named admissibility quantity itself (not its N/D) must be < 0 there, as the certificate claims;
  F leaf: the original system (G, H1, D of system-K.txt at u, t = u tau, S) must be nonzero there, and the sign ratio
          F_orig / F_chart must be the same at every sampled centre of the chart (the dropped factors have a fixed sign).
Usage: b4b_semantic.py polys.json bnb.json system.txt [max leaves per test, default all].  FINAL ok iff no contradiction."""
import json, sys, random
from fractions import Fraction as Fq
psrc, bsrc, ssrc = sys.argv[1], sys.argv[2], sys.argv[3]
MAXL = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
data = json.load(open(psrc)); cert = json.load(open(bsrc))
box = [[Fq(a), Fq(b)] for a, b in data['box']]
mp = data.get('map', ['u', 'tau', 'rho'])
def chart_map(x):
    p, q, r = x; env = {'p': p, 'q': q, 'r': r, 'u': p, 'tau': q, 'rho': r}
    return [eval(e.replace('^', '**'), {}, env) for e in mp]
sysp = {}
for line in open(ssrc):
    if ' = ' in line: k, e = line.split(' = ', 1); sysp[k.strip()] = e.strip().replace('^', '**')
def F_orig(u, t, S): return {k: eval(e, {}, {'u': u, 't': t, 'S': S}) for k, e in sysp.items()}
def evp(p, x): return sum(int(c) * x[0]**e[0] * x[1]**e[1] * x[2]**e[2] for e, c in p)
def quantities(u, t, S):
    one = Fq(1); v = u
    P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
    k3 = w3 / (1 - P); xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
    b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: Fq(0)}
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
    T = {}
    for i in range(1, 9): T[f'b{i} < b{i + 1}'] = b[i + 1] - b[i]
    for i in range(1, 10): T[f'w{i} > 0'] = w[i]
    for i in range(1, 10): T[f'apex t{i}'] = (a[i] - b[i]) if i <= 5 else (b[i] - a[i])
    for i in (2, 4, 5, 6, 8, 9): T[f'corner t{i} in disc'] = -(w[i]**2 + b[i]**2 - b[i])
    T['b9 < 1'] = 1 - S; T['b3 < b6'] = Q - P; T['b5 < 1/2'] = one / 2 - b5; T['Q > 1/2'] = Q - one / 2
    return T
leaves = cert['leaves']; random.seed(7)
bykind = {}
for lf in leaves: bykind.setdefault((lf[6], lf[7]), []).append(lf)
bad = []; checked = 0; skipped = 0; ratio_sign = {}
for (kind, name), L in bykind.items():
    if kind == 'H': continue
    for lf in (L if len(L) <= MAXL else random.sample(L, MAXL)):
        c = [box[j][0] + (box[j][1] - box[j][0]) * Fq(2 * lf[2 * j + 1] + 1, 2**(lf[2 * j] + 1)) for j in range(3)]
        try:
            u, tau, rho = chart_map(c)
            if not (0 < u < 1 and 0 < tau): skipped += 1; continue
            R = 1 / (1 + u**2); S = R + rho * (1 - u) * (1 - R); t = u * tau
            if kind == 'T':
                q = quantities(u, t, S)[name]
                if not q < 0: bad.append((lf, 'quantity', float(q)))
            else:
                fo = F_orig(u, t, S)[name]; fc = evp(data['F'][name], c)
                if fo == 0 or fc == 0: bad.append((lf, 'zero', 0)); continue
                s = (fo > 0) == (fc > 0)
                ratio_sign.setdefault(name, set()).add(s)
            checked += 1
        except ZeroDivisionError:
            skipped += 1
for k, s in ratio_sign.items():
    if len(s) != 1: bad.append((None, f'sign ratio of {k} not constant', 0))
print(f'{psrc}: centres checked {checked}, skipped (outside the open domain or a divisor 0 at the centre) {skipped}; contradictions {len(bad)}')
if bad: print('first contradictions:', bad[:10])
print('FINAL ok' if not bad and checked > 0 else 'FINAL FAIL')
