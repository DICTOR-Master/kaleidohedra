"""LEAD 4, the last step, EXACT: the degree-6 invariant harmonic of the icosahedral group takes its maximum on the unit sphere at the
five-fold axes and its minimum at the three-fold axes. (lead4_cert.py checked this on 400 000 points; here it is proved.)

Proof route (all exact, Q(sqrt5) arithmetic, no floats in any decision):
 1. H(u, w) = mean_g ((gu).w)^6 - |u|^6 |w|^6 / 7 (the degree-6 harmonic part, as in lead4_cert.py); Phi(u) = H(u, x0), x0 = (0, 1, phi).
    Exact identity  H(x0, x0) * H(u, w) = Phi(u) * Phi(w)  (rank one, as a polynomial identity).
 2. Exact identity  Phi = alpha * f6 + beta * |u|^6  with f6 = (y^2 - phi^2 z^2)(z^2 - phi^2 x^2)(x^2 - phi^2 y^2) (product of the six
    planes through the origin normal to the five-fold axes), alpha > 0.
 3. f6 depends only on X = x^2, Y = y^2, Z = z^2, so on the sphere its range is the range of the CUBIC F(X, Y, Z) on the triangle
    X + Y + Z = 1, X, Y, Z >= 0. A continuous function on a closed triangle takes its extremes at a vertex, at a critical point of
    an edge, or at an interior critical point. All of these are found exactly: edges by factoring F' over Q(sqrt5), the interior by
    the resultant of the two partial derivatives (factored into linear factors over Q(sqrt5)) and a gcd for the other coordinate.
    Every candidate value is compared exactly with F at the five-fold and three-fold axes.
 4. Hence Phi on the sphere ranges exactly over [Phi(three-fold), Phi(five-fold)], so h = Phi(u)Phi(w)/H(x0,x0) >= Phi_min Phi_max /
    H(x0, x0) = h at the extremal pair = -16/945, and mean p >= 0 for all unit u, w: the icosahedral constant 15 - 6 sqrt5 follows
    from moments plus the degree-6 harmonic with no numerical step.
POSITIVE CONTROL: the same pipeline on the octahedral degree-4 invariant x^4 + y^4 + z^4 (F = X^2 + Y^2 + Z^2) returns the known range
[1/3, 1] (three-fold min, four-fold max). Count control: the critical points found lift to exactly 12 + 20 + 30 = 62 axis points.
NEGATIVE CONTROLS: (a) the claim 'the maximum is at a two-fold axis' is refuted by the candidate list; (b) dropping the edges loses the
true maximum (interior only gives the two-fold value); (c) f6 built with 8/5 in place of phi cannot represent Phi (no alpha, beta)."""
import itertools, sys, time, sympy as sp
T0 = time.time()
checks = {}
def check(k, ok): checks[k] = bool(ok); print(('ok   ' if ok else 'FAIL ') + k, flush=True)
PILOT = len(sys.argv) > 1 and sys.argv[1] == 'pilot'
s5 = sp.sqrt(5); phi = (1 + s5) / 2
x, y, z = sp.symbols('x y z', real=True); X, Y, Zs = sp.symbols('X Y Z', real=True)

def ab(e):
    """e in Q(sqrt5) -> (a, b) rationals with e = a + b sqrt5 (asserted exact)."""
    e = sp.expand(sp.radsimp(sp.sympify(e)))
    b = e.coeff(s5); a = sp.expand(e - b * s5)
    assert a.is_Rational and b.is_Rational, ('not in Q(sqrt5)', e)
    return a, b
def sgn(e):
    """exact sign of a + b sqrt5."""
    a, b = ab(e)
    if b == 0: return int(sp.sign(a))
    if a == 0: return int(sp.sign(b))
    if a > 0 and b > 0: return 1
    if a < 0 and b < 0: return -1
    d = a * a - 5 * b * b          # |a| vs |b| sqrt5
    return int(sp.sign(a)) if d > 0 else -int(sp.sign(a)) if d < 0 else 0
def le(p, q): return sgn(q - p) >= 0
def eq(p, q): return sgn(q - p) == 0

def linear_roots(poly, var):
    """all roots of a univariate polynomial over Q(sqrt5), required to split into linear factors; returns list (or None if it does not split)."""
    P = sp.Poly(poly, var, extension=s5)
    if P.is_zero: return None
    if P.degree() <= 0: return []
    _, facs = sp.factor_list(P.as_expr(), var, extension=s5)
    roots = []
    for f, _m in facs:
        fp = sp.Poly(f, var, extension=s5)
        if fp.degree() == 0: continue
        if fp.degree() != 1: return None
        c1, c0 = fp.all_coeffs(); roots.append(sp.expand(sp.radsimp(-c0 / c1)))
    return roots

def range_on_triangle(F, name, use_edges=True):
    """exact candidate list for the extremes of the polynomial F(X, Y, Z) on the triangle X + Y + Z = 1, X, Y, Z >= 0.
    returns list of (point, value, kind)."""
    cands = []
    for P in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        cands.append((P, sp.expand(F.subs({X: P[0], Y: P[1], Zs: P[2]})), 'vertex'))
    t = sp.Symbol('t')
    if use_edges:
        for zero in range(3):                     # edge with coordinate `zero` = 0, parametrised by t in (0, 1)
            pts = [None] * 3; others = [i for i in range(3) if i != zero]
            pts[zero] = 0; pts[others[0]] = t; pts[others[1]] = 1 - t
            g = sp.expand(F.subs({X: pts[0], Y: pts[1], Zs: pts[2]}))
            rts = linear_roots(sp.diff(g, t), t)
            check(f'{name}: edge {"XYZ"[zero]} = 0: F\' splits over Q(sqrt5) (exact roots {rts})', rts is not None)
            for r in rts or []:
                if sgn(r) > 0 and sgn(1 - r) > 0:
                    P = tuple(sp.expand(sp.sympify(c).subs(t, r)) for c in pts)
                    cands.append((P, sp.expand(sp.radsimp(g.subs(t, r))), 'edge'))
    G = sp.expand(F.subs(Zs, 1 - X - Y)); GX = sp.diff(G, X); GY = sp.diff(G, Y)
    R = sp.Poly(sp.expand(sp.radsimp(sp.resultant(GX, GY, Y))), X, extension=s5)
    check(f'{name}: interior: resultant of the two partials in Y is a nonzero polynomial in X (degree {R.degree()}): finitely many critical X',
          not R.is_zero)
    xr = linear_roots(R.as_expr(), X)
    check(f'{name}: interior: the resultant splits over Q(sqrt5) into linear factors (X roots {xr})', xr is not None)
    # (every common root (X0, Y0) of GX, GY makes R(X0) = 0 regardless, so the X list is complete; the Y step below is a gcd per X0)
    for x0 in xr or []:
        a = sp.Poly(sp.expand(GX.subs(X, x0)), Y, extension=s5); b = sp.Poly(sp.expand(GY.subs(X, x0)), Y, extension=s5)
        if a.is_zero and b.is_zero:
            check(f'{name}: interior: at X = {x0} both partials vanish identically in Y (a critical LINE): not allowed', False); continue
        gg = a if b.is_zero else b if a.is_zero else sp.gcd(a, b)
        yr = linear_roots(gg.as_expr(), Y)
        check(f'{name}: interior: at X = {x0} the common Y roots split over Q(sqrt5) ({yr})', yr is not None)
        for y0 in yr or []:
            z0 = sp.expand(1 - x0 - y0)
            assert sp.expand(sp.radsimp(GX.subs({X: x0, Y: y0}))) == 0 and sp.expand(sp.radsimp(GY.subs({X: x0, Y: y0}))) == 0
            P = (x0, y0, z0)
            if all(sgn(c) > 0 for c in P):
                cands.append((P, sp.expand(sp.radsimp(F.subs({X: x0, Y: y0, Zs: z0}))), 'interior'))
    return cands

# ------------------------------------------------------------------------------------------------------------------------------
print('--- POSITIVE CONTROL: octahedral degree-4 invariant x^4 + y^4 + z^4 -> F = X^2 + Y^2 + Z^2', flush=True)
Foct = X**2 + Y**2 + Zs**2
c_oct = range_on_triangle(Foct, 'O control')
vals = [v for _, v, _ in c_oct]
mn = min(vals, key=lambda v: float(v)); mx = max(vals, key=lambda v: float(v))
check('O control: every candidate lies in [1/3, 1] (exact) and both ends are attained: min 1/3 at the centre (three-fold), max 1 at a vertex (four-fold)',
      all(le(sp.Rational(1, 3), v) and le(v, 1) for v in vals) and any(eq(v, sp.Rational(1, 3)) for v in vals) and any(eq(v, 1) for v in vals))
print(f'O control: candidates {[(P, v, k) for P, v, k in c_oct]}  ({time.time() - T0:.1f} s)', flush=True)

# ------------------------------------------------------------------------------------------------------------------------------
print('--- I: the degree-6 invariant harmonic', flush=True)
u = sp.Matrix([x, y, z])
def gen_group(gens, n):
    G = [sp.eye(3)]; fr = [sp.eye(3)]; key = lambda M: tuple(round(float(e), 9) for e in M); seen = {key(sp.eye(3))}
    while fr:
        nx = []
        for M in fr:
            for g in gens:
                N = (g * M).applyfunc(lambda e: sp.radsimp(sp.expand(e)))
                if key(N) not in seen: seen.add(key(N)); G.append(N); nx.append(N)
        fr = nx
    assert len(G) == n, len(G); return G
g3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]]); g2 = sp.diag(1, -1, -1)
cv = 1 / (2 * phi); vax = sp.Matrix([0, 1, phi])
cross = sp.Matrix([[0, -vax[2], vax[1]], [vax[2], 0, -vax[0]], [-vax[1], vax[0], 0]])
h5 = (cv * sp.eye(3) + cross / 2 + (1 - cv) / (1 + phi**2) * vax * vax.T).applyfunc(lambda e: sp.radsimp(sp.simplify(e)))
I = gen_group([g3, g2, h5], 60)
check('I: 60 exact rotations, all orthogonal with det 1 (exact)',
      all((M * M.T).applyfunc(lambda e: sp.radsimp(sp.expand(e))) == sp.eye(3) and sp.radsimp(sp.expand(M.det())) == 1 for M in I))
x0 = sp.Matrix([0, 1, phi]); n0 = sp.expand((x0.T * x0)[0])                    # |x0|^2 = 1 + phi^2
uu = x**2 + y**2 + z**2
# Phi(u) = H(u, x0) = mean_g ((g u).x0)^6 - |u|^6 |x0|^6 / 7
Phi = sp.Poly(sum(sp.expand(((M * u).T * x0)[0])**6 for M in I) / 60 - uu**3 * n0**3 / 7, x, y, z, extension=s5)
print(f'Phi built ({time.time() - T0:.1f} s)', flush=True)
# cross-check: the orbit of x0 is the 12 icosahedron vertices (each 5 times), so Phi = mean over the 12 vertices
verts = []
for M in I:
    v = (M.T * x0).applyfunc(lambda e: sp.radsimp(sp.expand(e)))
    if v not in verts: verts.append(v)
Phi12 = sp.Poly(sum(sp.expand((u.T * v)[0])**6 for v in verts) / 12 - uu**3 * n0**3 / 7, x, y, z, extension=s5)
check(f'I: orbit of the five-fold axis has {len(verts)} points and Phi equals the 12-vertex mean exactly', len(verts) == 12 and (Phi - Phi12).is_zero)
check('I: Phi is harmonic (Laplacian = 0, exact)', sp.Poly(sum(sp.diff(Phi.as_expr(), v, 2) for v in (x, y, z)), x, y, z, extension=s5).is_zero)
if not PILOT:
    # rank one as a polynomial identity: H(x0, x0) H(u, w) = Phi(u) Phi(w)
    w1, w2, w3 = sp.symbols('w1 w2 w3', real=True); w = sp.Matrix([w1, w2, w3]); ww = w1**2 + w2**2 + w3**2
    VARS = (x, y, z, w1, w2, w3)
    lin = [sp.Poly(((M * u).T * w)[0], *VARS, extension=s5) for M in I]
    H = sum((L**6 for L in lin), sp.Poly(0, *VARS, extension=s5)) * sp.Rational(1, 60) - sp.Poly(uu**3 * ww**3 / 7, *VARS, extension=s5)
    hxx = sp.radsimp(sp.expand(H.as_expr().subs({x: 0, y: 1, z: phi, w1: 0, w2: 1, w3: phi})))
    PhiW = sp.Poly(Phi.as_expr().subs({x: w1, y: w2, z: w3}, simultaneous=True), *VARS, extension=s5)
    check(f'I: H(x0, x0) H(u, w) = Phi(u) Phi(w) identically (rank one, exact; H(x0, x0) = {hxx})',
          (H * hxx - sp.Poly(Phi.as_expr(), *VARS, extension=s5) * PhiW).is_zero)
    print(f'H identity done ({time.time() - T0:.1f} s)', flush=True)
else:
    hxx = sp.radsimp(sp.expand(Phi.as_expr().subs({x: 0, y: 1, z: phi})))
check('I: H(x0, x0) = Phi(x0) > 0 (exact sign)', sgn(hxx) > 0)

def f6_with(q):
    return sp.expand((y**2 - q**2 * z**2) * (z**2 - q**2 * x**2) * (x**2 - q**2 * y**2))
def represent(fpoly):
    al, be = sp.symbols('alpha beta')
    diff = sp.Poly(sp.expand(Phi.as_expr() - al * fpoly - be * uu**3), x, y, z)
    sol = sp.solve([sp.radsimp(c) for c in diff.coeffs()], [al, be], dict=True)
    return sol
sol = represent(f6_with(phi))
check(f'I: Phi = alpha f6 + beta |u|^6 exactly, f6 = (y^2 - phi^2 z^2)(z^2 - phi^2 x^2)(x^2 - phi^2 y^2): solution {sol}', len(sol) == 1)
alpha = sp.radsimp(sol[0][sp.Symbol('alpha')]); beta = sp.radsimp(sol[0][sp.Symbol('beta')])
check(f'I: alpha = {alpha} > 0 (exact sign)', sgn(alpha) > 0)
check('NEGATIVE CONTROL (c): f6 built with 8/5 in place of phi cannot represent Phi (no alpha, beta)', len(represent(f6_with(sp.Rational(8, 5)))) == 0)

Fico = (Y - phi**2 * Zs) * (Zs - phi**2 * X) * (X - phi**2 * Y)
check('I: f6(x, y, z) = F(x^2, y^2, z^2) (exact)', sp.expand(Fico.subs({X: x**2, Y: y**2, Zs: z**2}) - f6_with(phi)) == 0)
cands = range_on_triangle(sp.expand(Fico), 'I')
print(f'candidates found ({time.time() - T0:.1f} s):', flush=True)
for P, v, k in cands: print(f'   {k:8s} X, Y, Z = {P}   F = {v} ~ {float(v):.12f}', flush=True)
ax5 = sp.Matrix([0, 1, phi]); ax3 = sp.Matrix([1, 1, 1]); ax2 = sp.Matrix([1 / phi, phi, 1])     # edge midpoint (0,1,phi) + (1,phi,0), scaled
def F_at(axis):
    n = sp.expand((axis.T * axis)[0])
    return sp.expand(sp.radsimp(Fico.subs({X: axis[0]**2 / n, Y: axis[1]**2 / n, Zs: axis[2]**2 / n})))
F5, F3, F2 = F_at(ax5), F_at(ax3), F_at(ax2)
def fixers(axis):
    return sum(1 for M in I if (M * axis - axis).applyfunc(lambda e: sp.radsimp(sp.expand(e))) == sp.zeros(3, 1))
check(f'I: the three test axes are a five-, three- and two-fold axis of this I (stabiliser orders {fixers(ax5)}, {fixers(ax3)}, {fixers(ax2)})',
      (fixers(ax5), fixers(ax3), fixers(ax2)) == (5, 3, 2))
print(f'F at five-fold {F5} ~ {float(F5):.12f}; three-fold {F3} ~ {float(F3):.12f}; two-fold {F2} ~ {float(F2):.12f}', flush=True)
vals = [v for _, v, _ in cands]
check('I: every candidate value lies in [F(three-fold), F(five-fold)] (exact comparisons in Q(sqrt5))', all(le(F3, v) and le(v, F5) for v in vals))
check('I: both ends are attained among the candidates (F5 on edges, F3 at the centre and on edges)', any(eq(v, F5) for v in vals) and any(eq(v, F3) for v in vals))
# count control: lift candidate points to the sphere (2^(number of nonzero coordinates) sign choices)
lift = sum(2 ** sum(1 for c in P if sgn(c) != 0) for P, _, _ in cands)
n5 = sum(2 ** sum(1 for c in P if sgn(c) != 0) for P, v, _ in cands if eq(v, F5))
n3 = sum(2 ** sum(1 for c in P if sgn(c) != 0) for P, v, _ in cands if eq(v, F3))
check(f'COUNT CONTROL: candidates lift to {lift} sphere points = 62 axis points (12 five-fold with F5: {n5}, 20 three-fold with F3: {n3}, 30 two-fold)',
      lift == 62 and n5 == 12 and n3 == 20)
check('NEGATIVE CONTROL (a): the claim "max at a two-fold axis" is refuted exactly (F5 > F2)', sgn(F5 - F2) > 0 and not all(le(v, F2) for v in vals))
c_int = range_on_triangle(sp.expand(Fico), 'I (no edges)', use_edges=False)
check('NEGATIVE CONTROL (b): without the edges the five-fold maximum is missed (interior/vertex max < F5): the edge step is essential',
      all(sgn(F5 - v) > 0 for _, v, _ in c_int))
# conclusion
Phi5 = sp.radsimp(alpha * F5 + beta); Phi3 = sp.radsimp(alpha * F3 + beta)
Phi5_direct = sp.radsimp(Phi.as_expr().subs({x: 0, y: 1 / sp.sqrt(n0), z: phi / sp.sqrt(n0)}))
check(f'I: Phi on the unit sphere ranges exactly over [{sp.simplify(Phi3)}, {sp.simplify(Phi5)}] = [-80/189 - 32 sqrt5/189, 16/21 + 32 sqrt5/105]',
      eq(Phi3, -sp.Rational(80, 189) - 32 * s5 / 189) and eq(Phi5, sp.Rational(16, 21) + 32 * s5 / 105) and eq(Phi5_direct, Phi5))
hmin = sp.radsimp(Phi3 * Phi5 / hxx)
check(f'I: min of h(u, w) = Phi(u) Phi(w) / H(x0, x0) over unit u, w is Phi_min Phi_max / H(x0, x0) = {sp.simplify(hmin)}, = -16/945 (the extremal pair)',
      sgn(Phi3) < 0 < sgn(Phi5) and eq(hmin, -sp.Rational(16, 945)))
check('I: hence mean p = A + p6 h >= A + p6 (-16/945) = 0 for ALL unit u, w (p6 > 0, lead4_cert.py): the range step is now exact',
      all(checks.values()))
# last link of the argument, made exact: if max_g (gu).w < c for some pair, mean p >= 0 with p <= 0 on [-1, c) forces every t_g to be a
# zero of p below c, i.e. in {-c, c', -c'}; the orbit's moments of degree 0..5 (a 5-design) then admit no weights: contradiction.
c = sp.sqrt((5 + 2 * s5) / 15); cp = sp.sqrt((5 - 2 * s5) / 15)
wts = sp.symbols('q1 q2 q3'); pts3 = [-c, cp, -cp]
mom = {0: 1, 1: 0, 2: sp.Rational(1, 3), 3: 0, 4: sp.Rational(1, 5), 5: 0}
eqs = [sp.expand(sum(q * v**k for q, v in zip(wts, pts3)) - m) for k, m in mom.items()]
solw = sp.solve(eqs, wts, dict=True)
check(f'I: no weights on {{-c, c\', -c\'}} match the orbit moments of degree 0..5 (exact solve: {solw}), so max_g (gu).w >= c for every unit pair', solw == [])
w4 = sp.symbols('r1 r2 r3 r4'); pts4 = [c, -c, cp, -cp]
sol4 = sp.solve([sp.expand(sum(q * v**k for q, v in zip(w4, pts4)) - m) for k, m in mom.items()], w4, dict=True)
check(f'POSITIVE CONTROL for that solve: with c allowed ({{c, -c, c\', -c\'}}, the extremal orbit) weights exist: {sol4}',
      len(sol4) == 1 and all(sgn(sp.radsimp(v)) >= 0 for v in sol4[0].values()))
print(f'time {time.time() - T0:.1f} s', flush=True)
bad = [k for k, v in checks.items() if not v]
print('FINAL ok' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
