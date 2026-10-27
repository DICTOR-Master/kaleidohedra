# Swap Rule proof, step 3: the BORDER at s = 1 (DICTO 2026-10-27). The far half of a tetrahedral piece (the half below the mid-plane
# for tetX, which sits at 3/4 of the gap; by the mirror, the half above for tetY) is the same for a c and an h lower layer iff s >= 1.
# (a) s >= 1 (q >= 2/3): with K0 = the cell against the sites of its OWN gap only, cut at zeta <= 1/2, every site of the gap below, of
#     either type, satisfies pow_i <= pow_j on all of K0 (one exact Farkas certificate each, over all q >= 2/3 and lam in the range).
#     Hence the far half = K0 for c and for h alike.
# (b) 1/2 <= s < 1: let j run over the gap-below sites present for c but not for h. g_j(q) = max over lam and p in the h far half of
#     pow_i - pow_j is concave in q (one lifted polyhedron); exact values g_j(1/3) > 0 and g_j(2/3) = 0 give g_j > 0 on [1/3, 2/3): at
#     every such spacing some lam has a point of the h far half outside the c far half. (c) containment the other way round
#     (c far half inside the h far half, all h sites certified) makes the c far half a proper subset: strictly smaller volume, so the two
#     far halves are not congruent.
import sys
from fractions import Fraction as Fr
from swapgeom import *
from locality import half_rows
def own_rows(t, q0, qmax=None):
    i, S = sites('tetX', t)
    own = [j for j in S['K'] if j[1] > 0]                 # gap 0 sites only (heights 1/4, 1/2, 3/4)
    below = [j for j in S['K'] if j[1] < 0]               # gap -1 sites of type t
    return i, own, below, [row(i, j) for j in own] + domain_rows(t, q0, True, qmax)
ok = bad = 0
print('(a) s >= 1: gap-below sites never cut the far half of tetX (cell against its own gap)')
for t in 'ch':
    i, own, below, R = own_rows(t, Fr(2, 3))
    for j in below:
        a, b = row(i, j); res = lp_max(a, R)
        good = res['status'].startswith('optimal') and res['value'] <= b and check_cert(a, R, res['y'], b)
        ok += good; bad += not good
        if not good: print('  FAIL', t, j, res.get('status'), res.get('value'), b)
    print(f'  type {t}: {len(below)} gap-below sites; running {ok} PASS {bad} FAIL', flush=True)
print(f'(a) TOTAL {ok} PASS, {bad} FAIL')
# (b)
CLOW = ([-Fr(3, 16), -1, 0, 0, 0], Fr(1, 4))           # lam >= -1/4 - 3q/16: the comparison needs the c pieces to exist
def g(tf, j, q):
    i, S, R = half_rows('tetX', tf, q, qmax=q); R = R + [CLOW]; a, b = row(i, j); res = lp_max(a, R)
    if res['status'] == 'infeasible': return None
    assert res['status'].startswith('optimal'), res
    return res['value'] - b
_, Sc = sites('tetX', 'c'); _, Sh = sites('tetX', 'h')
ckeys = {(j[0], j[1]) for j in Sc['K'] if j[1] < 0}; hkeys = {(j[0], j[1]) for j in Sh['K'] if j[1] < 0}
only_c = [j for j in Sc['K'] if j[1] < 0 and (j[0], j[1]) not in hkeys]
only_h = [j for j in Sh['K'] if j[1] < 0 and (j[0], j[1]) not in ckeys]
print(f'(b) {len(only_c)} gap-below sites present for c only, {len(only_h)} for h only')
witness = []
for j in only_c:
    g1, g2 = g('h', j, Fr(1, 3)), g('h', j, Fr(2, 3))
    if g1 is not None and g1 > 0: witness.append((j, g1, g2))
for j, g1, g2 in witness: print(f'  c-site {j}: g(1/3) = {g1}, g(2/3) = {g2}')
bw = [w for w in witness if w[2] is not None and w[2] >= 0]
print(f'(b) witnesses with g(1/3) > 0 and g(2/3) >= 0: {len(bw)}  -> {"PASS" if bw else "FAIL"}')
for qq in (Fr(2, 3) - Fr(1, 10**6), Fr(1, 2)):
    print(f'  check: max g at q = {qq}:', max(g('h', j, qq) or -1 for j, _, _ in witness))
# (c) every h-only site satisfied on the c far half, q in [1/3, 2/3] (exact certificates)
okc = badc = 0
i, S, R = half_rows('tetX', 'c', Fr(1, 3), qmax=Fr(2, 3))
for j in only_h:
    a, b = row(i, j); res = lp_max(a, R)
    good = res['status'].startswith('optimal') and res['value'] <= b and check_cert(a, R, res['y'], b)
    okc += good; badc += not good
    if not good: print('  (c) not contained:', j, res.get('value'), b)
print(f'(c) c far half inside every h-only halfspace: {okc} PASS, {badc} FAIL')
# (d) the h far half has interior: a rational point (lam, p) strictly inside every inequality at q = 1/3 and at q = 2/3 (then, the
#     inequalities being affine in (q, lam, p) jointly, at every q in between). With (b) this gives an open set of the h far half outside
#     the c far half, so with (c) the c far half is a proper subset with strictly smaller volume: not congruent.
import numpy as np
from scipy.optimize import linprog
okd = 0
for qq in (Fr(1, 3), Fr(2, 3)):
    i, S, R = half_rows('tetX', 'h', qq, qmax=qq); R = [r for r in R + [CLOW] if any(x != 0 for x in r[0][1:])]   # q fixed: drop q-only rows
    A = np.array([[float(x) for x in a[1:]] for a, _ in R]); bb = np.array([float(b - a[0] * qq) for a, b in R]); nr = np.linalg.norm(A, axis=1) + 1e-12
    res = linprog(np.r_[0, 0, 0, 0, -1.0], A_ub=np.c_[A, nr], b_ub=bb, bounds=[(None, None)] * 4 + [(0, 1)], method='highs')
    x = [Fr(v).limit_denominator(10**6) for v in res.x[:4]]
    strict = all(a[0] * qq + sum(a[1 + r] * x[r] for r in range(4)) < b for a, b in R)
    okd += strict; print(f'(d) q = {qq}: interior point lam, x, y, u = {[str(v) for v in x]}: {"PASS" if strict else "FAIL"}')
print(f'(d) {okd} PASS, {2 - okd} FAIL')
