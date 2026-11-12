"""LEAD 7 (12 Nov 2026): Kulaichev's (b) and (c) written as determinants in (u, v), and their behaviour on one viewpoint orbit
(u, v) -> (lambda u, v/lambda), exact (sympy, rational functions; no floats except the data checks at the end).
Frame (row 1): the yantra's circle in the unit disc, homogeneous X = (x, y, w), J = diag(1, 1, -1); depth frame point (x, d) of the
model is X = (2x, 1 - 2d, 1). O = (0, 1, 1), T = (0, -1, 1). Great corners: C7 = t7's corners (+-w7, R), C3 = t3's corner (w3, P),
with P = v^2/(1+v^2), R = 1/(1+u^2), w3 = v/(1+v^2), w7 = u/(1+u^2) (the model's rational parametrisation of the circle).
(1) CONIC DETERMINANT. V(X) = (x^2, xy, y^2, xw, yw, w^2). For any point X:
      Delta(X) := det[V(O); V(T); V(C7+); V(C7-); V(C3+); V(X)] = kappa(u, v) * X^T J X,
    kappa explicit and nonzero for 0 < u, v (it vanishes only when two of the five circle points meet).
(2) (c) = the t9 corner X9 = (w9, S), w9 = xW (S - R)/(R - P), xW = w7 P/R (marma (2,7,9) and t9's apex at P):
      Delta_c = Delta(X9) = 4 kappa * (w9^2 + S^2 - S)  and  numerator(w9^2 + S^2 - S) = G(u, v, S)  (natural.py's G),
    (b) = the t1 corner X1 = (w1, b1), w1 = m1 (Q - b1), m1 = xZ (P - b1)/((R - b1)(Q - P)), xZ = w3 (1 - R)/(1 - P) (marma (1,3,8)):
      Delta_b = Delta(X1) = 4 kappa * (w1^2 + b1^2 - b1) = 4 kappa * B(u, v, Q, b1)/den, B explicit.
    So (b) and (c) are walls of one determinant family: one 6 x 6 conic determinant each, with the same five circle points.
(3) ONE ORBIT. M_lambda = [[2 lambda, 0, 0], [0, lambda^2 + 1, lambda^2 - 1], [0, lambda^2 - 1, lambda^2 + 1]] (the Klein translation
    T_beta, beta = (lambda^2 - 1)/(lambda^2 + 1), scaled to polynomial entries), det M = 8 lambda^3, M^T J M = 4 lambda^2 J.
    Exact: M O ~ O, M T ~ T, M C7(u) ~ C7(lambda u), M C3(v) ~ C3(v/lambda); depths go d -> d' = d/(d + lambda^2 (1 - d)) (check);
    the construction is EQUIVARIANT: M X9(u, v, S) ~ X9(lambda u, v/lambda, S'), M X1(u, v, Q, b1) ~ X1(lambda u, v/lambda, Q', b1');
    Delta(M X_1..M X_6) = (det M)^4 Delta(X_1..X_6) (det Sym^2 M = (det M)^4), hence
      circle form of the image corner = mu(d) x circle form of the corner, mu(d) = lambda^2/(d + lambda^2 (1 - d))^2 > 0
      (d = S for (c), d = b1 for (b)); so G(lambda u, v/lambda, S') = mu(S) G(u, v, S) and B likewise:
    (b) and (c) are constant on every orbit u v = p: they are not walls of the beta-line; they choose WHICH orbits carry a yantra
    with t1, t9 on the circle. On one orbit the only walls are (d) (linear in beta, row 1) and the turn u = v.
Controls: POSITIVE, the data K1, V1, GF1 (40 digits) give Delta_b, Delta_c ~ 0 (relative < 1e-30); the rational yantra R1 gives
exact rational Delta_b, Delta_c (nonzero: R1 has no (b), (c)), and the exact R1 value is reproduced from its own lines.
NEGATIVE, the point (1, 1, 1) off the circle gives Delta = kappa != 0; the vertical stretch diag(1, 2, 1) (keeps the axis, not the circle)
breaks equivariance (its image of C7 leaves the circle) and the covariance of G fails; the old direction (u/lambda, v lambda) fails."""
import sympy as sp, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
u, v, lam, S, Q, b1, x, y, w = sp.symbols('u v lambda S Q b1 x y w', positive=True)
checks = {}
def Pt(xd, d): return sp.Matrix([2 * xd, 1 - 2 * d, 1])
def Vrow(X): return [X[0]**2, X[0] * X[1], X[1]**2, X[0] * X[2], X[1] * X[2], X[2]**2]
J = sp.diag(1, 1, -1)
def geo(u_, v_):
    P = v_**2 / (1 + v_**2); R = 1 / (1 + u_**2); w3 = v_ / (1 + v_**2); w7 = u_ / (1 + u_**2)
    return P, R, w3, w7
P, R, w3, w7 = geo(u, v)
O, Tp = sp.Matrix([0, 1, 1]), sp.Matrix([0, -1, 1])
C7p, C7m, C3p = Pt(w7, R), Pt(-w7, R), Pt(w3, P)
# polynomial representatives of the same projective points (a point scaled by s scales its V row by s^2)
C7p_, C7m_, C3p_ = sp.Matrix([2 * u, u**2 - 1, u**2 + 1]), sp.Matrix([-2 * u, u**2 - 1, u**2 + 1]), sp.Matrix([2 * v, 1 - v**2, 1 + v**2])
checks['(1) polynomial representatives: C7 = (2u, u^2 - 1, u^2 + 1)/(1 + u^2), C3 = (2v, 1 - v^2, 1 + v^2)/(1 + v^2)'] = \
    all(sp.cancel(a - b / (1 + u**2)) == 0 for a, b in zip(C7p, C7p_)) and all(sp.cancel(a - b / (1 + v**2)) == 0 for a, b in zip(C3p, C3p_))
FIVE = [Vrow(p) for p in (O, Tp, C7p_, C7m_, C3p_)]
cof = []                                              # Delta(X) = sum_j cof_j V_j(X): cofactors along the last row (5 x 5 minors)
for j in range(6):
    minor = sp.Matrix([[r[k] for k in range(6) if k != j] for r in FIVE])
    cof.append(sp.factor(sp.expand((-1)**(5 + j) * minor.det(method='berkowitz'))))
scale5 = ((1 + u**2)**2)**2 * ((1 + v**2)**2)         # Delta with the rational points = Delta_poly / scale5
X = sp.Matrix([x, y, w])
D_gen = sp.expand(sum(c * vj for c, vj in zip(cof, Vrow(X)))) / scale5
kappa = sp.factor(-D_gen.subs({x: 0, y: 0, w: 1}))   # the centre has X^T J X = -1
checks['(1) Delta(X) = kappa(u, v) X^T J X identically in X (cofactors = kappa (1, 0, 1, 0, 0, -1))'] = \
    sp.expand(sp.cancel(D_gen - kappa * (X.T * J * X)[0])) == 0
def Delta(X_): return D_gen.subs({x: X_[0], y: X_[1], w: X_[2]}, simultaneous=True)
print('kappa(u, v) =', kappa)
num_k = sp.factor(sp.numer(sp.together(kappa)))
def positive_factor(f, extra=()):
    f = sp.factor(f)
    if f.is_number: return f != 0
    if f in (u, v, lam) or f in extra: return True
    if f.is_Pow: return positive_factor(f.base, extra)
    return all(c > 0 for c in sp.Poly(f, *sorted(f.free_symbols, key=str)).coeffs())
fl_k = sp.factor_list(num_k)[1] + sp.factor_list(sp.denom(sp.together(kappa)))[1]
print('   factors of kappa (numerator and denominator):', fl_k)
checks['(1) kappa != 0 for u, v > 0, u v != 1 (factors: u, v, u v - 1 and positive polynomials); admissible yantras have u v < 1'] = \
    all(positive_factor(f, extra=(u * v - 1, 1 - u * v)) for f, m in fl_k)
# (2) the two corners
xW = w7 * P / R
w9 = xW * (S - R) / (R - P)
X9 = Pt(w9, S)
Dc = sp.cancel(Delta(X9))   # (1) is an identity in x, y, w
circ9 = w9**2 + S**2 - S
checks['(2) Delta_c = 4 kappa (w9^2 + S^2 - S)'] = sp.cancel(Dc - 4 * kappa * circ9) == 0
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-08-sri-yantra', 'scripts'))
cwd = os.getcwd(); os.chdir(os.path.join(HERE, '..', 'data'))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
os.chdir(cwd)
Gnat = N.G.subs({N.u: u, N.v: v, N.S: S})
num9 = sp.numer(sp.together(circ9))
ratio_c = sp.cancel(num9 / Gnat)
checks['(2) numerator(w9^2 + S^2 - S) = (constant or u, v monomial) x G of natural.py'] = not (ratio_c.free_symbols & {S})
print('   numerator(circle_9) / G =', sp.factor(ratio_c))
k3 = w3 / (1 - P); xZ = k3 * (1 - R)
m1 = xZ * (P - b1) / ((R - b1) * (Q - P))
w1 = m1 * (Q - b1)
X1 = Pt(w1, b1)
Db = sp.cancel(Delta(X1))
circ1 = w1**2 + b1**2 - b1
checks['(2) Delta_b = 4 kappa (w1^2 + b1^2 - b1)'] = sp.cancel(Db - 4 * kappa * circ1) == 0
Bnum, Bden = sp.fraction(sp.factor(sp.together(circ1)))
print('   (b): w1^2 + b1^2 - b1 = B/den with B =', sp.factor(Bnum), '   den =', Bden)
print('   (c): w9^2 + S^2 - S = G/den with G =', sp.factor(Gnat))
# (3) one orbit
M = sp.Matrix([[2 * lam, 0, 0], [0, lam**2 + 1, lam**2 - 1], [0, lam**2 - 1, lam**2 + 1]])
checks['(3) det M = 8 lambda^3 and M^T J M = 4 lambda^2 J'] = sp.expand(M.det() - 8 * lam**3) == 0 and sp.expand(M.T * J * M - 4 * lam**2 * J) == sp.zeros(3)
be = (lam**2 - 1) / (lam**2 + 1)
sq = 2 * lam / (lam**2 + 1)
checks['(3) sqrt(1 - beta^2) = 2 lambda/(lambda^2 + 1)'] = sp.cancel(sq**2 - (1 - be**2)) == 0
Tb = lambda X_: sp.Matrix([(X_[0] / X_[2]) * sq / (1 + be * X_[1] / X_[2]), (X_[1] / X_[2] + be) / (1 + be * X_[1] / X_[2]), 1])
pr = lambda A, B_: all(sp.cancel(A[i] * B_[j] - A[j] * B_[i]) == 0 for i in range(3) for j in range(3))
checks['(3) M is T_beta with beta = (lambda^2 - 1)/(lambda^2 + 1) (on a generic point)'] = pr(M * X, Tb(X))
dmap = lambda d: sp.cancel(d / (d + lam**2 * (1 - d)))
def img_depth(xd, d):
    Y = M * Pt(xd, d); return sp.cancel((1 - Y[1] / Y[2]) / 2), sp.cancel(Y[0] / Y[2] / 2)
checks['(3) depth map d -> d/(d + lambda^2 (1 - d)) (levels stay level)'] = sp.cancel(img_depth(x, S)[0] - dmap(S)) == 0
Pl, Rl, w3l, w7l = geo(lam * u, v / lam)
checks['(3) M O ~ O, M T ~ T'] = pr(M * O, O) and pr(M * Tp, Tp)
checks['(3) M C7(u) ~ C7(lambda u), M C3(v) ~ C3(v/lambda) (slopes u -> lambda u, v -> v/lambda)'] = \
    pr(M * C7p, Pt(w7l, Rl)) and pr(M * C7m, Pt(-w7l, Rl)) and pr(M * C3p, Pt(w3l, Pl))
checks['(3) NEGATIVE: the old direction (u/lambda, v lambda) is not the image'] = not pr(M * C7p, Pt(geo(u / lam, v * lam)[3], geo(u / lam, v * lam)[1]))
Sl, Ql, b1l = dmap(S), dmap(Q), dmap(b1)
xWl = w7l * Pl / Rl; w9l = xWl * (Sl - Rl) / (Rl - Pl)
checks['(3) equivariance of (c): M X9(u, v, S) ~ X9(lambda u, v/lambda, S\')'] = pr(M * X9, Pt(w9l, Sl))
k3l = w3l / (1 - Pl); xZl = k3l * (1 - Rl); m1l = xZl * (Pl - b1l) / ((Rl - b1l) * (Ql - Pl)); w1l = m1l * (Ql - b1l)
checks['(3) equivariance of (b): M X1(u, v, Q, b1) ~ X1(lambda u, v/lambda, Q\', b1\')'] = pr(M * X1, Pt(w1l, b1l))
# covariance of the determinant and of G, B
Vx = sp.Matrix(Vrow(X)); VMx = sp.Matrix(Vrow(M * X))
mons = [x**2, x * y, y**2, x * w, y * w, w**2]
S2 = sp.Matrix([[sp.Poly(sp.expand(VMx[i]), x, y, w).coeff_monomial(mons[j]) for j in range(6)] for i in range(6)])
checks['(3) V(M X) = Sym2(M) V(X) and det Sym2(M) = (det M)^4, so Delta(M X_1, ..., M X_6) = (det M)^4 Delta(X_1, ..., X_6)'] = \
    sp.expand(S2 * Vx - VMx) == sp.zeros(6, 1) and sp.expand(S2.det(method='berkowitz') - (8 * lam**3)**4) == 0
# circle form of a level point (x, d): x^2 + d^2 - d = X^T J X / 4; M^T J M = 4 lambda^2 J and (M X)_w = 2 (d + lambda^2 (1 - d)), so
# on the image point it is multiplied by mu(d) = lambda^2/(d + lambda^2 (1 - d))^2, which is > 0 for 0 <= d <= 1
mu = lambda d: lam**2 / (d + lam**2 * (1 - d))**2
checks['(3) third coordinate of M (2x, 1 - 2d, 1) is 2 (d + lambda^2 (1 - d))'] = sp.expand((M * Pt(x, S))[2] - 2 * (S + lam**2 * (1 - S))) == 0
circ9l = w9l**2 + Sl**2 - Sl
checks['(3) (c) on the orbit: w9\'^2 + S\'^2 - S\' = mu(S) (w9^2 + S^2 - S), mu(S) = lambda^2/(S + lambda^2 (1 - S))^2 > 0'] = \
    sp.cancel(circ9l - mu(S) * circ9) == 0
Gl = Gnat.subs({u: lam * u, v: v / lam, S: Sl}, simultaneous=True)
mu_c = sp.factor(sp.cancel(Gl / Gnat))
print('   G(lambda u, v/lambda, S\') / G(u, v, S) =', mu_c)
checks['(3) hence G(lambda u, v/lambda, S\') = mu_c G(u, v, S) with mu_c = lambda^2/(S + lambda^2 (1 - S))^2 (exact)'] = sp.cancel(mu_c - mu(S)) == 0
# the general lemma (generic level point (x, d)): the image point (x', d') of M has x'^2 + d'^2 - d' = mu(d) (x^2 + d^2 - d)
Y_ = M * Pt(x, S); xi, di = Y_[0] / Y_[2] / 2, (1 - Y_[1] / Y_[2]) / 2
checks['(3) lemma: for every level point the image circle form is mu(d) times the circle form'] = sp.cancel(xi**2 + di**2 - di - mu(S) * (x**2 + S**2 - S)) == 0
# (b) then follows from the equivariance of X1 checked above (the image of t1's corner IS the image yantra's t1 corner):
checks['(3) (b) on the orbit: w1\'^2 + b1\'^2 - b1\' = mu(b1) (w1^2 + b1^2 - b1) (lemma + equivariance of X1)'] = \
    checks['(3) lemma: for every level point the image circle form is mu(d) times the circle form'] and \
    checks['(3) equivariance of (b): M X1(u, v, Q, b1) ~ X1(lambda u, v/lambda, Q\', b1\')']
# NEGATIVE controls
checks['NEGATIVE: the point (1, 1, 1) off the circle gives Delta = kappa != 0'] = sp.cancel(Delta(sp.Matrix([1, 1, 1])) - kappa) == 0 and kappa != 0
Ms = sp.diag(1, 2, 1)
checks['NEGATIVE: the vertical stretch diag(1, 2, 1) takes C7 off the circle'] = sp.cancel(((Ms * C7p).T * J * (Ms * C7p))[0]) != 0
dmap_s = lambda d: sp.cancel((1 - 2 * (1 - 2 * d)) / 2)
Gs = Gnat.subs({S: dmap_s(S)})
checks['NEGATIVE: under the stretch (depth image of S, slopes kept) G is not a multiple of G'] = (sp.cancel(Gs / Gnat).free_symbols & {S}) != set()
# POSITIVE data controls
mpd = 50
import mpmath as mp
mp.mp.dps = mpd
D = os.path.join(HERE, '..', 'data')
def data_D(Yd):            # the 6 x 6 determinants from the yantra's own stored corners (no formula in u, v used)
    g = lambda d: {int(k): mp.mpf(z['a']) for k, z in d.items()}
    b_, w_, a_ = g(Yd['b']), g(Yd['w']), g(Yd['apex'])
    uu, vv = w_[7] / (b_[7] - a_[7]), w_[3] / (a_[3] - b_[3])
    pt = lambda xd, d: (2 * xd, 1 - 2 * d, mp.mpf(1))
    V_ = lambda q: [q[0]**2, q[0] * q[1], q[1]**2, q[0] * q[2], q[1] * q[2], q[2]**2]
    five = [(0, 1, 1), (0, -1, 1), pt(w_[7], b_[7]), pt(-w_[7], b_[7]), pt(w_[3], b_[3])]
    det6 = lambda q: mp.det(mp.matrix([V_(p) for p in five] + [V_(q)]))
    scale = abs(det6((0, 0, 1)))                                  # = |kappa|
    return abs(det6(pt(w_[9], b_[9]))) / scale, abs(det6(pt(w_[1], b_[1]))) / scale, uu * vv
K = json.load(open(os.path.join(D, 'kites.json')))['K1']; V = json.load(open(os.path.join(D, 'viewpoint.json')))['V1']
GF = json.load(open(os.path.join(D, 'golden_family.json')))['GF1']
res = {nm: data_D(Yd) for nm, Yd in (('K1', K), ('V1', V), ('GF1', GF))}
for nm, (dc, db, p) in res.items(): print(f'   {nm}: |Delta_c|/|kappa| = {mp.nstr(dc, 3)}, |Delta_b|/|kappa| = {mp.nstr(db, 3)}, u v = {mp.nstr(p, 15)}')
checks['POSITIVE: K1, V1 (same orbit), GF1 have Delta_b = Delta_c = 0 to 1e-30'] = all(dc < 1e-30 and db < 1e-30 for dc, db, p in res.values())
checks['POSITIVE: K1 and V1 lie on one orbit (u v equal to 1e-35)'] = abs(res['K1'][2] - res['V1'][2]) < mp.mpf(10)**-35
# R1, the rational yantra (exact)
R1 = dict(b=[sp.Rational(s) for s in '248/3611 48/233 4/13 23/61 86/197 8/15 576/937 172/229 8/9'.split()],
          w=[sp.Rational(s) for s in '836/3611 3401/11883 6/13 1805/12444 703/6698 38/255 456/937 16245/50609 323/1485'.split()])
uR, vR = sp.Rational(19, 24), sp.Rational(2, 3)
QR, SR, b1R = R1['b'][5], R1['b'][8], R1['b'][0]
sub = {u: uR, v: vR}
checks['R1 exact: P, R, w3, w7 from (u, v) = (19/24, 2/3) match its stored b3, b7, w3, w7'] = \
    [x_.subs(sub) for x_ in (P, R, w3, w7)] == [R1['b'][2], R1['b'][6], R1['w'][2], R1['w'][6]]
w9R = w9.subs({**sub, S: SR}); w1R = w1.subs({**sub, Q: QR, b1: b1R})
checks['R1 exact: the model corners X9, X1 reproduce its stored w9, w1 (the formulas are the yantra\'s own lines)'] = w9R == R1['w'][8] and w1R == R1['w'][0]
DcR = Dc.subs({**sub, S: SR}); DbR = Db.subs({**sub, Q: QR, b1: b1R})
print('   R1 (exact): Delta_c =', sp.nsimplify(DcR), ' Delta_b =', sp.nsimplify(DbR))
checks['R1 exact: Delta_c, Delta_b rational and nonzero (R1 has neither (b) nor (c)); equal to 4 kappa (circle form)'] = \
    DcR.is_rational and DbR.is_rational and DcR != 0 and DbR != 0 and DcR == 4 * kappa.subs(sub) * (R1['w'][8]**2 + SR**2 - SR)
for k_, c_ in checks.items(): print(('  ok   ' if c_ else '  FAIL ') + k_)
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k_ for k_, c_ in checks.items() if not c_))
