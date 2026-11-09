# bird1_certificate.py -- DICTO Hopscotch, icosahedral line, bird 1 (study 2026-11-09-icosahedral-line).
# A moment certificate for #43 Theorem 2's constant: for unit u, w, max over the 60 rotations g of I of (g u).w >= c,
# c^2 = (5 + 2 sqrt5)/15 (so 1/c^2 = 15 - 6 sqrt5), using the degree-6 icosahedral harmonic H.
# Exact in Q(sqrt5): sympy Polys over QQ<sqrt5>.
# Steps: (0) known cases: the 60 rotations; octahedral cubic certificate mean (1 - 3m^2)/(9m); 1/c^2 = 15 - 6 sqrt5.
#        (1) orbit moments E[t^k], k = 0..7, symbolic u, w: odd ones vanish, E[t^2], E[t^4] uniform, E[t^6] = |u|^6|w|^6/7 + kappa H(u)H(w).
#        (2) the range of H on the sphere: critical points lie on mirror planes (Jacobian of |x|^2, Q6, Q10 = const * product of the
#            15 mirror forms); on a mirror circle the critical points are exactly the 5-, 3-, 2-fold axes.
#        (3) the degree-7 certificate p(t) = (t - c)(t + c)^2 (t^2 - a^2)^2, a^2 = (5 - 2 sqrt5)/15: E[p] = c (A + kappa z), z = H(u)H(w),
#            A + kappa z >= 0 on the whole range of z, = 0 exactly at z = H(5-fold)H(3-fold).
#        (4) no polynomial of degree <= 6 reaches c (the extremal orbit's values -c, -a, a are interior zeros of even order).
import itertools, time
import sympy as sp
t0 = time.time()
s5 = sp.sqrt(5); phi = (1 + s5) / 2
K = sp.QQ.algebraic_field(s5)
def red(M): return M.applyfunc(lambda x: sp.nsimplify(sp.radsimp(sp.expand(x))))
A3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]]); B2 = sp.diag(1, -1, -1)
# the 60 rotations of the icosahedron with corners (0, +-1, +-phi) and cyclic permutations (the frame of the axes below):
# every rotation is fixed by where it sends one corner V0 and one neighbour V1
V12 = [sp.Matrix(p) for s1 in (1, -1) for s2 in (1, -1) for p in ((0, s1, s2 * phi), (s1, s2 * phi, 0), (s2 * phi, 0, s1))]
def sq(v): return sp.nsimplify(sp.radsimp(sp.expand(v.dot(v))))
V0 = V12[0]; nb = [v for v in V12 if sq(v - V0) == 4]; V1 = nb[0]
Bm = sp.Matrix.hstack(V0, V1, V0.cross(V1)).inv()
mats = []
for v in V12:
    for v2 in V12:
        if sq(v2 - v) == 4:
            M = red(sp.Matrix.hstack(v, v2, v.cross(v2)) * Bm)
            if all(any(red(M * a - b) == sp.zeros(3, 1) for b in V12) for a in V12): mats.append(M)
C5 = mats[1]
checks = {}
checks['|I| = 60 rotations, orthogonal, det 1'] = len(mats) == 60 and all(red(M.T * M) == sp.eye(3) and sp.simplify(M.det() - 1) == 0 for M in mats)

# (0) known cases
m = sp.symbols('m', positive=True)
Tt = sp.Symbol('T'); pc = sp.expand((Tt - m) * (Tt + 1 / (3 * m))**2)
mom3 = {0: 1, 1: 0, 2: sp.Rational(1, 3), 3: 0}
mean_oct = sp.simplify(sum(pc.coeff(Tt, k) * mom3[k] for k in range(4)))
checks['octahedral cubic certificate mean = (1 - 3m^2)/(9m)'] = sp.simplify(mean_oct - (1 - 3 * m**2) / (9 * m)) == 0
c2 = (5 + 2 * s5) / 15; a2 = (5 - 2 * s5) / 15
checks['1/c^2 = 15 - 6 sqrt5'] = sp.simplify(1 / c2 - (15 - 6 * s5)) == 0

# (1) orbit moments, symbolic
u = sp.symbols('u1:4'); w = sp.symbols('w1:4'); X = u + w
tg = [sp.Poly(sum(w[i] * M[i, j] * u[j] for i in range(3) for j in range(3)), *X, domain=K) for M in mats]
U2 = sp.Poly(sum(x**2 for x in u), *X, domain=K); W2 = sp.Poly(sum(x**2 for x in w), *X, domain=K)
mom = {}
for k in range(8):
    tk = time.time()
    S = sp.Poly(0, *X, domain=K)
    for t in tg: S += t**k
    mom[k] = S * sp.Rational(1, 60)
    print(f'E[t^{k}] computed ({len(mom[k].terms())} terms, {time.time() - tk:.0f} s)', flush=True)
checks['odd moments E[t], E[t^3], E[t^5], E[t^7] vanish identically'] = all(mom[k].is_zero for k in (1, 3, 5, 7))
checks['E[t^2] = |u|^2|w|^2/3'] = (mom[2] - U2 * W2 * sp.Rational(1, 3)).is_zero
checks['E[t^4] = |u|^4|w|^4/5'] = (mom[4] - U2**2 * W2**2 * sp.Rational(1, 5)).is_zero
# the degree-6 invariant harmonic: H(x) = sum over the 6 unit 5-fold axes of (a.x)^6 - (6/7)|x|^6
ax5 = [sp.Matrix([0, 1, phi]), sp.Matrix([0, 1, -phi]), sp.Matrix([1, phi, 0]), sp.Matrix([1, -phi, 0]), sp.Matrix([phi, 0, 1]), sp.Matrix([-phi, 0, 1])]
x = sp.symbols('x1:4')
def Qn(n, var):
    return sp.Poly(sum((sum(a[i] * var[i] for i in range(3)))**n / (a.dot(a))**sp.Rational(n, 2) for a in ax5), *var, domain=K)
R2x = sp.Poly(sum(v**2 for v in x), *x, domain=K)
Hx = Qn(6, x) - R2x**3 * sp.Rational(6, 7)
lap = sum(Hx.diff(v).diff(v) for v in x)
checks['H = Q6 - (6/7)|x|^6 is harmonic'] = lap.is_zero
checks['H is invariant under the 60 rotations'] = all((sp.Poly(Hx.as_expr().subs({x[i]: sum(M[i, j] * x[j] for j in range(3)) for i in range(3)}, simultaneous=True), *x, domain=K) - Hx).is_zero for M in mats)
Hu = sp.Poly(Hx.as_expr().subs(dict(zip(x, u)), simultaneous=True), *X, domain=K)
Hw = sp.Poly(Hx.as_expr().subs(dict(zip(x, w)), simultaneous=True), *X, domain=K)
D6 = mom[6] - U2**3 * W2**3 * sp.Rational(1, 7)
HH = Hu * Hw
# kappa from one coefficient, then the identity
mono = HH.monoms()[0]
kappa = sp.nsimplify(sp.radsimp(sp.expand(D6.coeff_monomial(mono) / HH.coeff_monomial(mono))))
checks['E[t^6] = |u|^6|w|^6/7 + kappa H(u)H(w) identically (orbits are 5-designs, not 6-designs)'] = (D6 - HH * kappa).is_zero
print('kappa =', kappa, '=', float(kappa), flush=True)

# (2) range of H on the sphere
Q10 = Qn(10, x)
J = sp.Matrix([[R2x.diff(v).as_expr() for v in x], [Hx.diff(v).as_expr() for v in x], [Q10.diff(v).as_expr() for v in x]]).det()
Jp = sp.Poly(sp.expand(J), *x, domain=K)
# 15 two-fold axes = mirror normals: the 30 edge midpoints of the icosahedron (0,1,phi)-type corners, up to sign
V12 = [sp.Matrix(p) for s1 in (1, -1) for s2 in (1, -1) for p in ((0, s1, s2 * phi), (s1, s2 * phi, 0), (s2 * phi, 0, s1))]
mids = []
for i, j in itertools.combinations(range(12), 2):
    d = V12[i] - V12[j]
    if sp.simplify(d.dot(d) - 4) == 0:
        mvec = red((V12[i] + V12[j]) / 2)
        if not any(red(mvec + q) == sp.zeros(3, 1) for q in mids): mids.append(mvec)
checks['15 mirror normals (two-fold axes)'] = len(mids) == 15
prod = sp.Poly(1, *x, domain=K)
for q in mids: prod *= sp.Poly(sum(q[i] * x[i] for i in range(3)), *x, domain=K)
qt, rm = sp.div(Jp, prod)
checks['Jacobian(|x|^2, H, Q10) = nonzero constant * product of the 15 mirror forms'] = rm.is_zero and qt.is_ground and not qt.is_zero
# mirror circle x1 = 0 (normal (1,0,0) is a two-fold axis): critical points of H on it
y, z = sp.symbols('y z')
Hm = sp.Poly(Hx.as_expr().subs({x[0]: 0, x[1]: y, x[2]: z}), y, z, domain=K)
g = sp.Poly(z * Hm.diff(y) - y * Hm.diff(z), y, z, domain=K)
axes_in_plane = {'5': [(1, phi), (1, -phi)], '3': [(phi, 1 / phi), (phi, -1 / phi)], '2': [(1, 0), (0, 1)]}
lin = sp.Poly(1, y, z, domain=K)
for lst in axes_in_plane.values():
    for (p, q) in lst: lin *= sp.Poly(q * y - p * z, y, z, domain=K)
qt2, rm2 = sp.div(g, lin)
checks['on the mirror circle the critical points of H are exactly the 5-, 3-, 2-fold axes'] = rm2.is_zero and qt2.is_ground and not qt2.is_zero
def Hval(v):
    v = sp.Matrix(v); n = v.dot(v)
    return sp.nsimplify(sp.radsimp(sp.expand(Hx.as_expr().subs(dict(zip(x, v)), simultaneous=True) / n**3)))
H5 = Hval(ax5[0]); H3 = Hval([1 / phi, 0, phi]); H2 = Hval([0, 0, 1])
print('H on the sphere at the axes: H5 =', H5, float(H5), ' H3 =', H3, float(H3), ' H2 =', H2, float(H2), flush=True)
checks['H5 = max, H3 = min of H on the sphere (H5 > H2 > H3, H5 > 0 > H3)'] = bool(H5 > H2) and bool(H2 > H3) and bool(H5 > 0) and bool(H3 < 0)
zmin = sp.nsimplify(sp.radsimp(sp.expand(H5 * H3))); zmax = sp.nsimplify(sp.radsimp(sp.expand(max(H5**2, H3**2, key=float))))
print('z = H(u)H(w) ranges over [H5 H3, max(H5^2, H3^2)] = [', zmin, ',', zmax, '] =', [float(zmin), float(zmax)], flush=True)

# (3) the certificate
s = sp.Symbol('s')
q = sp.expand((s - c2) * (s - a2)**2)            # p(t) = (t + c)(t^2 - c^2)(t^2 - a^2)^2 = (t + c) q(t^2); odd part has mean 0
Es = {0: 1, 1: sp.Rational(1, 3), 2: sp.Rational(1, 5)}
Aconst = sp.nsimplify(sp.radsimp(sp.expand(sum(q.coeff(s, k) * Es[k] for k in range(3)) + q.coeff(s, 3) * sp.Rational(1, 7))))
print('E[p] = c (A + kappa z), A =', Aconst, '=', float(Aconst), ' kappa =', kappa, flush=True)
checks['E[p] = 0 at z = H5 H3 (u on a 5-fold, w on a 3-fold axis)'] = sp.simplify(Aconst + kappa * zmin) == 0
checks['kappa > 0, so A + kappa z >= 0 on the whole range, equality only at z = H5 H3'] = bool(kappa > 0)
# direct check of the extremal orbit: u = 5-fold, w = 3-fold, the 60 values are +-c, +-a (15 each)
u0 = ax5[0] / sp.sqrt(ax5[0].dot(ax5[0])); w0 = sp.Matrix([1 / phi, 0, phi]); w0 = w0 / sp.sqrt(w0.dot(w0))
vals = [sp.nsimplify(sp.radsimp(sp.expand(((M * u0).dot(w0))**2))) for M in mats]
from collections import Counter
cnt = Counter(vals); print('extremal orbit: squared values', dict(cnt))
checks['extremal orbit values: t^2 in {c^2, a^2}, 30 each, max t = c'] = set(cnt) == {sp.nsimplify(c2), sp.nsimplify(a2)} and sorted(cnt.values()) == [30, 30]
# contradiction step: values in {-c, -a, a} cannot have mean 0 and mean square 1/3 (exact: x = share of -c)
xs = sp.nsimplify(sp.radsimp((sp.Rational(1, 3) - a2) / (c2 - a2)))
checks['share of -c forced to 1/2, then mean <= -c/2 + a/2 < 0 (contradiction)'] = xs == sp.Rational(1, 2) and bool(c2 > a2)
# (4) degree <= 6: LP bound (float) for the record, with z at both ends of its range
import numpy as np
from scipy.optimize import linprog
def lp_bound(deg, zvals, mm, ngrid=1500):
    # feasibility of p (deg) with p <= 0 on [-1, mm] and E_z[p] >= 1 at each z in zvals (normalised); returns True if a certificate exists
    from numpy.polynomial import legendre
    tgrid = np.linspace(-1, mm, ngrid)
    kap = float(kappa)
    def Ek(k, zz):
        if k % 2: return 0.0
        return {0: 1, 2: 1 / 3, 4: 1 / 5, 6: 1 / 7 + kap * zz, 8: None}[k]
    A_ub = [[tt**k for k in range(deg + 1)] for tt in tgrid]; b_ub = [0] * ngrid
    for zz in zvals: A_ub.append([-Ek(k, zz) for k in range(deg + 1)]); b_ub.append(-1)
    r = linprog(np.zeros(deg + 1), A_ub=A_ub, b_ub=b_ub, bounds=[(-1e4, 1e4)] * (deg + 1), method='highs')
    return r.status == 0
best = {}
for deg in (5, 6, 7):
    lo, hi = 0.5, 0.86
    for _ in range(40):
        mid = (lo + hi) / 2
        if lp_bound(deg, [float(zmin), float(zmax)], mid): lo = mid
        else: hi = mid
    best[deg] = lo
    print(f'degree {deg}: best moment bound m >= {lo:.6f} (constant 1/m^2 = {1 / lo**2:.6f}); c = {float(sp.sqrt(c2)):.6f}', flush=True)
checks['LP: degree 5 gives sqrt(3/5), degree 6 stays below c, degree 7 reaches c'] = abs(best[5] - (3 / 5)**.5) < 1e-3 and best[6] < float(sp.sqrt(c2)) - 5e-3 and abs(best[7] - float(sp.sqrt(c2))) < 1e-3
for k, v in checks.items(): print(('  ok   ' if v else '  FAIL ') + k)
print(f'time {time.time() - t0:.0f} s')
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
