"""Row 1 (hyperboloid / projective row), parts (a) and (b), exact (sympy).
Quadric: the yantra's circle x^2 + y^2 = 1, homogeneous X = (x, y, w), J = diag(1, 1, -1) (Klein's absolute).
(a) Every projective map keeping the circle and fixing O = (0,1), T = (0,-1) is T_beta, up to the mirror x -> -x; with the
    half-turn y -> -y (O <-> T) this is the whole stabiliser of the axis. Derivation: M^T J M = J, M O = a O, M T = b T.
(b) T_beta acts on the circle's own coordinate z = x/(1-y) (slope of the line from O) as z -> lambda z, lambda = a = e^theta
    = sqrt((1+beta)/(1-beta)); the upper slope u is z of P, the lower slope v is 1/z of Q, so u v = z_P / z_Q = the cross-ratio
    (P, Q; T, O) on the circle, a projective invariant of the circle's automorphisms that fix O and T."""
import sympy as sp
x, y, a, beta, u, v, z1, z2, z3, z4 = sp.symbols('x y a beta u v z1 z2 z3 z4', real=True)
J = sp.diag(1, 1, -1)
O, T, E1 = sp.Matrix([0, 1, 1]), sp.Matrix([0, -1, 1]), sp.Matrix([1, 0, 0])
checks = {}

# (a) the J-orthogonal complement of O and T is the line of E1 (the pole of the axis x = 0)
X = sp.Matrix(sp.symbols('p q r'))
comp = sp.solve([(X.T * J * O)[0], (X.T * J * T)[0]], list(X)[1:], dict=True)
checks['complement of O,T is E1 (pole of the axis)'] = comp == [{X[1]: 0, X[2]: 0}]
checks['O,T null, <O,T>_J = -2'] = (O.T * J * O)[0] == 0 and (T.T * J * T)[0] == 0 and (O.T * J * T)[0] == -2
# so M E1 = c E1 with c^2 = 1, and <MO, MT> = ab <O,T> forces ab = 1 (a > 0 up to the overall sign of M)
A = sp.Symbol('A', positive=True)
for c in (1, -1):
    B = sp.Matrix.hstack(E1, O, T)
    M = sp.simplify(B * sp.diag(c, A, 1 / A) * B.inv())
    checks[f'c={c}: M^T J M = J'] = sp.simplify(M.T * J * M - J) == sp.zeros(3)
    img = M * sp.Matrix([x, y, 1])
    xp, yp = sp.simplify(img[0] / img[2]), sp.simplify(img[1] / img[2])
    b_of_a = (A**2 - 1) / (A**2 + 1)
    Tx = c * x * sp.sqrt(1 - b_of_a**2) / (1 + b_of_a * y); Ty = (y + b_of_a) / (1 + b_of_a * y)
    checks[f'c={c}: M is T_beta (times x->{c}x), beta=(a^2-1)/(a^2+1)'] = sp.simplify(xp - Tx) == 0 and sp.simplify(yp - Ty) == 0
    print(f"c = {c}:  x' = {xp},  y' = {yp}")
checks['lambda = a = sqrt((1+beta)/(1-beta))'] = sp.simplify(sp.sqrt((1 + (A**2 - 1) / (A**2 + 1)) / (1 - (A**2 - 1) / (A**2 + 1))) - A) == 0
# eigenvalue of T_beta at O is lambda, at T is 1/lambda (T_beta as a matrix: boost in the (y, w) plane)
lam = sp.sqrt((1 + beta) / (1 - beta))
Mb = sp.Matrix([[sp.sqrt(1 - beta**2), 0, 0], [0, 1, beta], [0, beta, 1]])
checks['T_beta matrix keeps J up to scale'] = sp.simplify(Mb.T * J * Mb - (1 - beta**2) * J) == sp.zeros(3)
evO = sp.simplify((Mb * O)[1] / O[1] / sp.sqrt(1 - beta**2)); evT = sp.simplify((Mb * T)[2] / T[2] / sp.sqrt(1 - beta**2))
checks['multiplier at O is lambda, at T 1/lambda'] = sp.simplify(evO**2 - lam**2) == 0 and sp.simplify(evT**2 - 1 / lam**2) == 0 and \
    all(abs(sp.N((evO - lam).subs(beta, bb))) < 1e-30 and abs(sp.N((evT - 1 / lam).subs(beta, bb))) < 1e-30 for bb in (sp.Rational(-1, 3), sp.Rational(1, 2)))
# keeps the circle
Tb = lambda X_, Y_: (X_ * sp.sqrt(1 - beta**2) / (1 + beta * Y_), (Y_ + beta) / (1 + beta * Y_))
xp, yp = Tb(x, y)
checks['circle kept'] = sp.simplify((xp**2 + yp**2 - 1).subs(x**2, 1 - y**2).subs(x, sp.sqrt(1 - y**2))) == 0

# (b) slopes. upper slope (line through O): x/(1-y); lower slope (line through T): x/(1+y)
s_up = sp.simplify(xp / (1 - yp)); s_lo = sp.simplify(xp / (1 + yp))
checks['upper slope u -> lambda u (lines through O)'] = sp.simplify((s_up / (x / (1 - y)))**2 - lam**2) == 0 and \
    sp.simplify((s_up / (x / (1 - y))).subs({beta: sp.Rational(1, 3), x: sp.Rational(1, 5), y: sp.Rational(1, 7)}) - lam.subs(beta, sp.Rational(1, 3))) == 0
checks['lower slope v -> v/lambda (lines through T)'] = sp.simplify((s_lo / (x / (1 + y)))**2 - 1 / lam**2) == 0 and \
    sp.simplify((s_lo / (x / (1 + y))).subs({beta: sp.Rational(1, 3), x: sp.Rational(1, 5), y: sp.Rational(1, 7)}) - 1 / lam.subs(beta, sp.Rational(1, 3))) == 0
# direction check against the computed V1 (K1 seen at beta = -0.0405464286): u 2/phi^2 -> 0.7335605, lambda = 0.9602432
phi = (1 + sp.sqrt(5)) / 2
b1 = sp.Float('-0.0405464286', 20)
lam1 = sp.sqrt((1 + b1) / (1 - b1))
checks['direction (V1 numbers): u_new = lambda*u_old'] = abs(lam1 * 2 / phi**2 - sp.Float('0.7335605468', 20)) < 1e-8 and \
    abs(sp.Float('0.70710678118654752', 20) / lam1 - sp.Float('0.7363829964', 20)) < 1e-8
print('V1: lambda*2/phi^2 =', sp.N(lam1 * 2 / phi**2, 12), ' (1/sqrt2)/lambda =', sp.N(1 / sp.sqrt(2) / lam1, 12))
# the circle coordinate z = x/(1-y) = (1+y)/x; line through T with slope v meets the circle at Q with z_Q = 1/v
t = sp.Symbol('t', real=True)
P = ((2 * t) / (1 + t**2), (t**2 - 1) / (t**2 + 1))      # rational parametrisation with z(P) = t
checks['z(P) = t on the parametrisation'] = sp.simplify(P[0] / (1 - P[1]) - t) == 0
checks['slope from T to P is 1/z(P)'] = sp.simplify(P[0] / (1 + P[1]) - 1 / t) == 0
zp = sp.simplify(Tb(*P)[0] / (1 - Tb(*P)[1]))
checks['T_beta acts on the circle as z -> lambda z'] = sp.simplify((zp / t)**2 - lam**2) == 0
cr = lambda p, q, r, s: (p - r) * (q - s) / ((p - s) * (q - r))
# cross-ratio (P, Q; T, O) with z(T) = 0, z(O) = infinity: limit gives z_P / z_Q
crPQ = sp.limit(cr(z1, z2, 0, z4), z4, sp.oo)
checks['cross-ratio (P,Q;T,O) = z_P/z_Q'] = sp.simplify(crPQ - z1 / z2) == 0
checks['u v = (P,Q;T,O) with z_P = u, z_Q = 1/v'] = sp.simplify(crPQ.subs({z1: u, z2: 1 / v}) - u * v) == 0
checks['cross-ratio invariant under z -> lambda z'] = sp.simplify(cr(z1, z2, z3, z4) - cr(a * z1, a * z2, a * z3, a * z4)) == 0
checks['legs meet on the circle iff u v = 1'] = sp.simplify(P[0]**2 / ((1 - P[1]) * (1 + P[1])) - 1) == 0
# polarity: T_beta commutes with the circle's polarity X -> J X (point <-> line), because M^T J M ~ J
Xs = sp.Matrix([x, y, 1])
checks['T_beta commutes with polarity'] = sp.simplify(Mb.inv().T * (J * Xs) - (J * Mb * Xs) / (1 - beta**2)) == sp.zeros(3, 1)
# the turn: conjugation by the half-turn R: y -> -y gives T_{-beta}
R = sp.diag(1, -1, 1)
Mm = Mb.subs(beta, -beta)
checks['R T_beta R = T_-beta (turn beta -> -beta, lambda -> 1/lambda)'] = sp.simplify(R * Mb * R - Mm) == sp.zeros(3)

for k, ok in checks.items(): print(('ok   ' if ok else 'FAIL ') + k)
bad = [k for k, ok in checks.items() if not ok]
print('FINAL ok' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
