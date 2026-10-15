# Step 25 (DICTO: "run the exact proof of the golden ring heights"). All in Q(sqrt5).
# The five-fold axis is a = v/|v| for an exact OCD corner v, so a height is h(X) = X.v/|v|. Ratios of heights are exact.
# (A) Lemma: every joint (bond) vector b_i has b_i.v = (m_i + n_i phi) U for one exact U, so every site (an integer combination
#     of bonds) has height (m + n phi) u with u = U/|v|: golden heights for ALL copies, not only the silent ones.
# (B) The silent core rings of the radius-10 run (matched to the exact sites): exact (m, n) per ring, and exact ratios of
#     squared distances from the axis.
import sys, json, numpy as np
from fractions import Fraction as Fr
sys.argv = ['chorus_exact_big.py', '10.0']
src = open('scripts/chorus_exact_big.py').read().split('alive = np.ones')[0]
exec(src)                                                      # exact OCD, bonds, voices, sites (no silencing)
iv = int(np.argmax(np.linalg.norm(Of, axis=1))); v = OCD[iv]; vv = dot(v, v)
assert np.allclose(f(v) / np.linalg.norm(f(v)), a5)
phi = Q(Fr(1, 2), Fr(1, 2))
def ppow(p):
    r = Q(1)
    for _ in range(p): r = r * phi
    return r
def zphi(q):                                                   # q = m + n phi exactly? return (m, n) or None
    n = 2 * q.b; m = q.a - q.b
    return (int(m), int(n)) if n.denominator == 1 and m.denominator == 1 else None
c = [dot(b, v) for b in bond]
out = [f'five-fold axis through the exact corner v = ({", ".join(map(str, v))}), |v|^2 = {vv}']
# candidate unit: the smallest positive height of a bond, divided down until all ratios are golden integers
U = min((x for x in c if x.f() > 1e-12), key=lambda q: q.f())
for div in (1, 2, 3, 4, 5, 6, 8, 10, 12):
    Ud = U / Q(div)
    if all(zphi(x / Ud) for x in c): break
else: raise SystemExit('no golden unit found')
mn = [zphi(x / Ud) for x in c]
# reduce: if all (m, n) share a common golden-integer factor, the unit could be larger; record gcd of the integers
from math import gcd
g = 0
for m_, n_ in mn: g = gcd(g, gcd(abs(m_), abs(n_)))
Ud = Ud * Q(g); mn = [zphi(x / Ud) for x in c]
u2 = Ud * Ud / vv
out.append(f'(A) unit U = {Ud}; u = U/|v| with u^2 = {u2} = {u2.f():.8f} (u = {u2.f() ** .5:.6f})')
out.append(f'    all 20 bond heights are golden integers times u (exact): {mn}')
# (B) exact sites of the radius-10 run, matched to the silent ones
D = json.load(open('data/chorus-exact-r10.json')); Sf = np.array(D['silenced']); Pf = np.array([x for x, _ in sites])
exactS = []
for s in Sf:
    j = int(np.argmin(np.linalg.norm(Pf - s, axis=1))); assert np.linalg.norm(Pf[j] - s) < 1e-6; exactS.append(sites[j][1])
rows = []
for X in exactS:
    h = dot(X, v); r2 = dot(X, X) - h * h / vv                   # squared distance from the axis, exact
    rows.append((zphi(h / Ud), r2))
assert all(r[0] is not None for r in rows)
out.append(f'(B) all {len(rows)} silent copies (core and seams) have exact golden heights; check: every height / u is m + n phi: True')
core = [(mn_, r2) for mn_, r2 in rows if r2.f() < 1.05 ** 2]
rings = {}
for mn_, r2 in core: rings.setdefault((mn_, r2), 0); rings[(mn_, r2)] += 1
out.append(f'    core rings (within 1.05 of the axis): {len(rings)} rings, sizes {sorted(set(rings.values()))}')
ref = min((r2 for (_, r2) in rings), key=lambda q: q.f())
for (mn_, r2), k in sorted(rings.items(), key=lambda t: t[0][1].f()):
    ratio = r2 / ref
    pw = next((p for p in range(0, 13) if ratio == ppow(p)), None)
    out.append(f'    height = ({mn_[0]} + {mn_[1]} phi) u = {((Q(mn_[0]) + Q(mn_[1]) * phi).f() * u2.f() ** .5):+.5f}   distance^2 = {r2} ({r2.f() ** .5:.4f});'
               f' distance^2 / innermost = {ratio}' + (f' = phi^{pw} exactly (distance ratio phi^{pw / 2:g})' if pw is not None else ''))
print('\n'.join(out)); open('data/chorus-heights-exact.txt', 'w').write('\n'.join(out) + '\n')
