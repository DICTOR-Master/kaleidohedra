"""LEAD 5 (exact): t_min on the icosahedral two-family line, and whether the turn's fixed point maximises it.
S_lam = {a.x <= 1 for the 12 unit five-fold normals a (dodecahedron faces); b.x <= lam for the 20 unit three-fold normals b
(icosahedron faces)}. Inverting distances (same planes) gives S_lam^v = S_{1/lam}: the turn is lam -> 1/lam, fixed point lam = 1.
By (B), t_min(S_lam) = max_{x in S_lam, y in S_{1/lam}} x.y, symmetric under the turn by construction.
All 60 corners of S_lam form ONE orbit of the rotation group I in each chamber, so t_min = max_g x0(lam).(g y0(1/lam)).
Steps: exact group I (Q(sqrt5)); walls (4-plane concurrency determinants); corner x0(lam) per chamber; the maximising g at sample
points (float), its exact expression; exact check at rational lam against all 3600 corner pairs (exact max); the middle piece in
the turn-invariant s = lam + 1/lam; max at the fixed point."""
import itertools, sympy as sp
from fractions import Fraction
checks = {}
def check(k, ok): checks[k] = bool(ok); print(('ok   ' if ok else 'FAIL ') + k, flush=True)
s5 = sp.sqrt(5); phi = (1 + s5) / 2
lam = sp.Symbol('lam', positive=True)
def vecs_A():
    out = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            for p in ([0, s1, s2 * phi], [s1, s2 * phi, 0], [s2 * phi, 0, s1]): out.append(sp.Matrix(p))
    return out
def vecs_B():
    out = [sp.Matrix(v) for v in itertools.product([1, -1], repeat=3)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            for p in ([0, s1 * phi, s2 / phi], [s1 * phi, s2 / phi, 0], [s2 / phi, 0, s1 * phi]): out.append(sp.Matrix(p))
    return out
nA2 = sp.simplify(1 + phi**2); nB2 = sp.Integer(3)
A = vecs_A(); B = vecs_B()
check('12 five-fold vectors |A|^2 = phi + 2, 20 three-fold vectors |B|^2 = 3',
      len(A) == 12 and len(B) == 20 and all(sp.simplify((v.T * v)[0] - nA2) == 0 for v in A) and all(sp.simplify((v.T * v)[0] - 3) == 0 for v in B))
nA, nB = sp.sqrt(nA2), sp.sqrt(nB2)
# plane (V, d): V.x <= d ; unit-normal distances 1 (A) and lam (B)
planesA = [(v, nA) for v in A]
def planesB(L): return [(v, nB * L) for v in B]
rho2 = 15 - 6 * s5; rho = sp.sqrt(rho2)
# ---- walls: a corner of the dodecahedron (3 A planes) reaches a B plane -> lam = rho (and 1/rho); the 2A+1B / 1A+2B switch:
# two A planes and two B planes concurrent
def conc(pl):
    return sp.Matrix([[*v, -d] for v, d in pl]).det()
# find concurrent quadruples generically: pick a1, a2 adjacent (angle between five-fold axes = arccos(1/sqrt5)), b1, b2 sharing their edge
adjA = [(i, j) for i, j in itertools.combinations(range(12), 2) if sp.simplify((A[i].T * A[j])[0] - nA2 / s5) == 0]
check('dodecahedron: 30 edges (adjacent five-fold pairs)', len(adjA) == 30)
i, j = adjA[0]
near_b = sorted(range(20), key=lambda k: -float((B[k].T * (A[i] + A[j]))[0]))[:2]
wdet = sp.factor(sp.simplify(conc([planesA[i], planesA[j]] + [(B[k], nB * lam) for k in near_b])))
lw = [r for r in sp.solve(wdet, lam) if r.is_positive]
print('wall det (2 A + 2 B planes on one edge):', wdet, ' roots', lw, flush=True)
lw = [r for r in lw if 1 < float(r) < 1.25]
print('wall det degree in lam:', sp.degree(sp.numer(sp.together(wdet)), lam), flush=True)
check('the type wall (icosidodecahedron): one root lam_w in the line, 1 < lam_w < rho (its turn image 1/lam_w is the same event on S^v)', len(lw) == 1)
lw = sp.radsimp(lw[0]); print('lam_w =', lw, '=', sp.N(lw, 15), ' 1/lam_w =', sp.radsimp(1 / lw), flush=True)
# ---- exact group I (as in row2_sphere.py)
D = lambda s: sp.diag(*s)
g3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]]); g2 = D((1, -1, -1))
cv = 1 / (2 * phi); vax = sp.Matrix([0, 1, phi])
cross = sp.Matrix([[0, -vax[2], vax[1]], [vax[2], 0, -vax[0]], [-vax[1], vax[0], 0]])
h5 = (cv * sp.eye(3) + cross / 2 + (1 - cv) / (1 + phi**2) * vax * vax.T).applyfunc(lambda e: sp.radsimp(sp.simplify(e)))
I = [sp.eye(3)]; fr = [sp.eye(3)]; key = lambda M: tuple(round(float(e), 9) for e in M); seen = {key(sp.eye(3))}
while fr:
    nx = []
    for M in fr:
        for g in (g3, g2, h5):
            N = (g * M).applyfunc(lambda e: sp.radsimp(sp.expand(e)))
            if key(N) not in seen: seen.add(key(N)); I.append(N); nx.append(N)
    fr = nx
check('I: 60 exact rotations', len(I) == 60 and all(sp.simplify(M.T * M - sp.eye(3)) == sp.zeros(3) for M in I[:60:7]))
# ---- corners: chamber 1 (lam < lam_w): 2A + 1B ; chamber 2 (lam > lam_w): 1A + 2B
def corner(pl):
    M = sp.Matrix([list(v) for v, _ in pl]); r = sp.Matrix([d for _, d in pl])
    return (M.LUsolve(r)).applyfunc(lambda e: sp.radsimp(sp.simplify(e)))
x_2A1B = corner([planesA[i], planesA[j], (B[near_b[0]], nB * lam)])
a_far = [k for k in range(12) if k not in (i, j)]
# 1A + 2B corner: the five-fold plane i with two adjacent three-fold planes around it
nbB = sorted(range(20), key=lambda k: -float((B[k].T * A[i])[0]))[:5]
pair = [(p, q) for p, q in itertools.combinations(nbB, 2) if abs(float((B[p].T * B[q])[0]) - float(sp.sqrt(5) * 1)) < 1e-9]
p, q = pair[0]
x_1A2B = corner([planesA[i], (B[p], nB * lam), (B[q], nB * lam)])
def valid(x, L):
    return all(float((v.T * x)[0].subs(lam, L)) <= float(d.subs(lam, L) if hasattr(d, 'subs') else d) + 1e-9 for v, d in planesA + planesB(lam))
check('corner types: 1A+2B (icosahedron end, lam -> 1/rho) for lam < lam_w, 2A+1B (dodecahedron end) for lam > lam_w (float at 7 points)',
      all(valid(x_1A2B, L) for L in (0.8, 0.9, 1.0, 1.09)) and all(valid(x_2A1B, L) for L in (1.11, 1.2, 1.25)) and not valid(x_1A2B, 1.15) and not valid(x_2A1B, 1.0))
def x0(L):      # exact corner of S_L
    return (x_1A2B if L < lw else x_2A1B).subs(lam, L)
def tmin_exact(L):          # exact max over all 60 x 60 corner pairs (orbits of x0)
    X = x0(L); Y = x0(1 / L)
    vals = [((g * X).T * Y)[0] for g in I]
    best = max(vals, key=lambda e: float(e))
    return sp.radsimp(sp.simplify(best)), vals
# ---- the three pieces
t_end = rho * lam
samples = [sp.Rational(k, 100) for k in (80, 82, 85, 88, 90)]
ok_end = True
for L in samples:
    if L >= 1 / lw: continue
    tv, _ = tmin_exact(L); ok_end &= sp.simplify(tv - rho * L) == 0 and sp.simplify(tv - tmin_exact(1 / L)[0]) == 0
check(f'end piece t_min = rho*lam (rho^2 = 15 - 6sqrt5) for 1/rho < lam <= 1/lam_w, exact at the samples below 1/lam_w, and t(1/lam) = t(lam)', ok_end)
# middle: identify the maximising g symbolically at lam = 1, then the expression in lam
X1 = x_1A2B; Y1 = x_1A2B.subs(lam, 1 / lam)
cands = [sp.radsimp(sp.simplify(((g * X1).T * Y1)[0])) for g in I]
mids = [sp.Rational(k, 100) for k in (91, 93, 95, 97, 99, 100, 101, 104, 107, 109)]
mids = [L for L in mids if 1 / lw < L < lw]
winners = set()
for L in mids:
    v = [float(c.subs(lam, L)) for c in cands]; winners.add(max(range(60), key=lambda k: v[k]))
wexpr = sp.simplify(cands[sorted(winners)[0]])
print('middle piece candidates winning at the samples:', sorted(winners), ' expression:', wexpr, flush=True)
same = all(sp.simplify(cands[k] - wexpr) == 0 for k in winners)
check('middle piece: one expression wins at every middle sample', same)
ok_mid = True
for L in mids:
    tv, _ = tmin_exact(L); ok_mid &= sp.simplify(tv - wexpr.subs(lam, L)) == 0
check(f'middle piece equals the exact t_min (max of 3600 pairs) at {len(mids)} rational lam in (1/lam_w, lam_w)', ok_mid)
s = sp.Symbol('s', positive=True)
sub = sp.simplify(sp.expand(wexpr))
# express in s = lam + 1/lam if possible
f_s = sp.simplify(sp.together(sub).subs(lam, (s + sp.sqrt(s**2 - 4)) / 2))
f_s2 = sp.simplify(sp.together(sub).subs(lam, (s - sp.sqrt(s**2 - 4)) / 2))
turn_inv = sp.simplify(f_s - f_s2) == 0
print('middle piece in s:', sp.simplify(f_s), '| turn-invariant:', turn_inv, flush=True)
check('middle piece is turn-invariant (a function of s = lam + 1/lam)', turn_inv)
lin = sp.simplify(sp.diff(f_s, s, 2)) == 0
print('middle piece linear in s:', lin, flush=True)
d1 = sp.simplify(sp.diff(sub, lam).subs(lam, 1))
check('fixed point lam = 1 is a critical point of the middle piece', d1 == 0)
t1 = sp.radsimp(sp.simplify(sub.subs(lam, 1))); R2_1 = (x_1A2B.subs(lam, 1).T * x_1A2B.subs(lam, 1))[0]
print('t_min at the fixed point:', t1, '=', sp.N(t1, 15), '; R^2 of S_1:', sp.radsimp(sp.simplify(R2_1)), flush=True)
check('at the fixed point t_min = R^2 of the self-antipol S_1', sp.simplify(t1 - R2_1) == 0)
# max at the fixed point: middle piece <= t1 on (lam_w, 1/lam_w) (exact: t1 - f >= 0 as a function of s >= 2), ends below
gap = sp.simplify(t1 - f_s)
print('t(1) - middle(s) =', sp.factor(gap), flush=True)
s_w = sp.radsimp(lw + 1 / lw)
grid = [2 + (s_w - 2) * sp.Rational(k, 40) for k in range(1, 41)]
check('t(1) - middle >= 0 on 2 < s <= s_w (exact at 40 points) and = 0 only at s = 2', all(float(gap.subs(s, g)) > 0 for g in grid) and sp.simplify(gap.subs(s, 2)) == 0)
check('ends meet the middle at the walls: rho/lam_w = middle(1/lam_w) < t(1)', float(rho / lw) < float(t1) and sp.simplify(rho / lw - wexpr.subs(lam, 1 / lw)) == 0)
a5, b5 = 10 - s5, sp.sqrt(6 * s5 + 30) / 2
check('b = sqrt(30 + 6sqrt5)/2 = 3*lam_w', sp.simplify(b5 - 3 * lw) == 0)
line = sorted(set([sp.Rational(k, 50) for k in range(40, 63)]))
line = [L for L in line if float(1 / rho) < float(L) < float(rho)]
okmin = all(sp.simplify(tmin_exact(L)[0] - sp.Min(rho * L, rho / L, a5 - b5 * (L + 1 / L))) == 0 for L in line)
check(f'closed form t_min = min(rho*lam, rho/lam, 10 - sqrt5 - 3 lam_w s) at {len(line)} rational lam across (1/rho, rho), exact', okmin)
check('max at the fixed point holds for EVERY lam: t(1) - middle = 3 lam_w (s - 2) >= 0 (s >= 2 by AM-GM), ends below the middle',
      sp.simplify(gap - 3 * lw * (s - 2)) == 0)
print('RESULT: t_min = rho*lam (1/rho < lam <= 1/lam_w), middle piece above (1/lam_w <= lam <= lam_w), rho/lam beyond; linear in s:', lin)
bad = [k for k, v in checks.items() if not v]
print('FINAL ok' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
