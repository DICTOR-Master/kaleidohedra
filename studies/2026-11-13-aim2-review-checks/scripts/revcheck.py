"""Aim 2 paper, referee revision (13 Nov 2026): exact checks of the statements added or reworded after the hostile review.
R1  the turn and the bridge on the cube line: S(2) = cuboctahedron, its polar the rhombic dodecahedron (vol 2, Omega 12); S(2)^v = S(3/2)
    is the UNIFORM truncated octahedron (all edges equal); the bridge polytope S(mu)polar is the hull of the facet feet of S(mu)^v, so
    Omega(S(mu); 0) = 3! h^-6 vol(feet hull of S(c/mu)), c = 3, h = 1, checked against Table 1 at mu = 6/5, 3/2, 5/2, 14/5 (exact; the relation needs h^2 <= mu <= R^2, where both facet types are present).
R2  the moment identity vol((P - y)polar) = int over Ppolar of (1 - x.y)^-(d+1) dx: P = cube [-1,1]^3, Ppolar = octahedron; Taylor
    coefficients of both sides agree exactly through order 6 (LHS closed form 8 prod 1/(1 - y_i^2) / 3!).
R3  the 600-cell line: Table 1 continuity at the two middle walls; outer chambers Omega = 75(sqrt5 - 1)/mu^4 (mu < r^2) and 1440(47 sqrt5 - 105)
    (mu > 1) = 4! vol(600-cell of circumradius 1)/mu^4 and 4! vol(polar 120-cell); turn images of the walls (5+sqrt5)/8 and 1/2+sqrt5/6
    are (5+2sqrt5)/10 and (9+3sqrt5)/16, not walls.
R4  the chamber monomial: in each chamber of the cube, icosahedral and 600-cell lines every corner of S(mu) is a transversal meet:
    active facet normals of rank d - j and active corner-plane normals of rank j, and j is the power of 1/mu in Table 1 (numerical: corners read from the facets of the polar hull at one mu per chamber, tolerance 1e-7).
R5  the alternate-sector lemma: m lines through 0, sectors alternately in and out; sum of the in-sector cone forms = 0 for m = 3, 5, 7, 9
    (exact, random rational directions); for m = 2 the point residue is 2; a cone and its antipode have the same form.
NEG controls: R1 with S(5/3) in place of S(3/2) is not uniform; R2 with exponent -d in place of -(d+1) fails at order 2; R5 with one
    in-sector swapped for an out-sector is nonzero; R4 at a wall gives a mixed count.
Usage: python -u revcheck.py [pilot]"""
import sys, itertools, random, time
import sympy as sp
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull

PILOT = 'pilot' in sys.argv[1:]
OK = True
T0 = time.time()
def check(name, cond):
    global OK
    OK &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
s5 = sp.sqrt(5); phi = (1 + s5) / 2
TASKS = 5

# ---------- R1 ----------
def cube_line_vertices(m):
    """vertices of S(m) = [-1,1]^3 cap {|x|+|y|+|z| <= m}, exact (rational m)."""
    planes = [(sp.Matrix(n), sp.Integer(1)) for n in ([1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1])]
    planes += [(sp.Matrix(s), m) for s in itertools.product([1, -1], repeat=3)]
    V = set()
    for a, b, c in itertools.combinations(planes, 3):
        M = sp.Matrix.hstack(a[0], b[0], c[0]).T
        if M.det() == 0: continue
        x = M.LUsolve(sp.Matrix([a[1], b[1], c[1]]))
        if all((p[0].T * x)[0] <= p[1] for p in planes): V.add(tuple(x))
    return [sp.Matrix(v) for v in V], planes
def edges_lengths(V, planes):
    L = set()
    for u, v in itertools.combinations(V, 2):
        act = [p for p in planes if (p[0].T * u)[0] == p[1] and (p[0].T * v)[0] == p[1]]
        if len(act) >= 2 and sp.Matrix.hstack(*[p[0] for p in act]).rank() == 2: L.add(sp.nsimplify((u - v).dot(u - v)))
    return L
V2, P2 = cube_line_vertices(sp.Integer(2))
check('R1 S(2) has 12 corners, all at the edge midpoints of the cube (cuboctahedron)', len(V2) == 12 and all(sorted(abs(c) for c in v) == [0, 1, 1] for v in V2))
V32, P32 = cube_line_vertices(sp.Rational(3, 2)); L32 = edges_lengths(V32, P32)
check(f'R1 S(3/2) = S(2)^v has 24 corners and one edge length (squared {L32}): the uniform truncated octahedron', len(V32) == 24 and len(L32) == 1)
V53, P53 = cube_line_vertices(sp.Rational(5, 3)); L53 = edges_lengths(V53, P53)
check(f'NEG R1 S(5/3) has two edge lengths {L53} (not uniform)', len(L53) == 2)
def feet_hull_vol(m):
    """hull of the facet feet n_i * dist_i of the active facets of S(m); returns exact volume via a sympy triangulation from 0."""
    V, planes = cube_line_vertices(m)
    act = [p for p in planes if sum(1 for v in V if (p[0].T * v)[0] == p[1]) >= 3]
    feet = [p[0] * p[1] / p[0].dot(p[0]) for p in act]
    F = np.array([[float(x) for x in f] for f in feet]); H = ConvexHull(F)
    vol = 0
    for s in H.simplices:
        vol += abs(sp.Matrix.hstack(*[feet[i] for i in s]).det()) / 6
    return sp.nsimplify(vol)
def omega_table_cube(m):
    m = sp.Rational(m); return 48 / m**3 if m < 1 else 48 / m**2 if m < 2 else 24 / m if m < 3 else sp.Integer(8)
def polar_vol(m):
    """vol of S(m) polar = conv(n_i / dist_i) over active facets (exact)."""
    V, planes = cube_line_vertices(m)
    act = [p for p in planes if sum(1 for v in V if (p[0].T * v)[0] == p[1]) >= 3]
    pts = [p[0] / p[1] for p in act]
    H = ConvexHull(np.array([[float(x) for x in q] for q in pts]))
    return sum(abs(sp.Matrix.hstack(*[pts[i] for i in s]).det()) / 6 for s in H.simplices)
check('R1 polar of S(2) (the rhombic dodecahedron) has volume 2, so Omega(S(2); 0) = 12 = Table 1 value 24/2', polar_vol(sp.Integer(2)) == 2 and omega_table_cube(2) == 12)
check('R1 the feet hull of S(3/2) is the same rhombic dodecahedron (volume 2)', feet_hull_vol(sp.Rational(3, 2)) == 2)
for m in ([sp.Rational(3, 2)] if PILOT else [sp.Rational(6, 5), sp.Rational(3, 2), sp.Rational(5, 2), sp.Rational(14, 5)]):   # the Turn Theorem's range h^2 < mu < R^2
    lhs = 6 * polar_vol(m); rhs = 6 * feet_hull_vol(3 / m)
    check(f'R1 mu = {m}: Omega(S(mu); 0) = 3! vol(polar) = {sp.nsimplify(lhs)} = 3! vol(feet hull of S(3/mu)) = {rhs} = Table 1 {omega_table_cube(m)}',
          sp.simplify(lhs - rhs) == 0 and sp.simplify(lhs - omega_table_cube(m)) == 0)
if not PILOT:
    m = sp.Rational(1, 2); lhs = 6 * polar_vol(m); rhs = 6 * feet_hull_vol(3 / m)
    check(f'NEG R1 outside the range (mu = 1/2, only corner planes active): the feet-hull relation fails ({lhs} against {rhs}), so it is stated for h^2 <= mu <= R^2 only', lhs != rhs)
print(f'PROGRESS {1}/{TASKS} R1 ({time.time()-T0:.0f} s)', flush=True)

# ---------- R2 ----------
y1, y2, y3, t = sp.symbols('y1 y2 y3 t')
Y = [y1, y2, y3]
def oct_moment(mon):
    """exact integral over the octahedron |x|_1 <= 1 of x^a y^b z^c: 8 orthants of the simplex, Dirichlet formula."""
    a, b, c = mon
    if a % 2 or b % 2 or c % 2: return sp.Integer(0)
    return 8 * sp.factorial(a) * sp.factorial(b) * sp.factorial(c) / sp.factorial(a + b + c + 3)
def rhs_series(order, expo):
    tot = 0
    for n in range(order + 1):
        coef = sp.binomial(n + expo - 1, n)            # (1 - s)^-expo = sum binom(n+expo-1, n) s^n
        poly = sp.Poly(sp.expand((y1 * sp.Symbol('a') + y2 * sp.Symbol('b') + y3 * sp.Symbol('c')) ** n), sp.Symbol('a'), sp.Symbol('b'), sp.Symbol('c'))
        for mon, cf in poly.terms(): tot += coef * cf * oct_moment(mon)
    return sp.expand(tot)
lhs = sp.expand(sp.series(sp.Mul(*[1 / (1 - (yy * t) ** 2) for yy in Y]), t, 0, 7).removeO().subs(t, 1)) * sp.Rational(8, 6)
lhs_trunc = sum(term for term in sp.Add.make_args(lhs) if sp.Poly(term, *Y).total_degree() <= 6)
check('R2 vol((cube - y)polar) = int over the octahedron of (1 - x.y)^-4 dx, Taylor coefficients equal through order 6 (exact)', sp.expand(lhs_trunc - rhs_series(6, 4)) == 0)
check('NEG R2 exponent -3 instead of -4 fails', sp.expand(lhs_trunc - rhs_series(6, 3)) != 0)
print(f'PROGRESS {2}/{TASKS} R2 ({time.time()-T0:.0f} s)', flush=True)

# ---------- R3 ----------
r2 = (7 + 3 * s5) / 16
w1, w2 = (5 + s5) / 8, sp.Rational(1, 2) + s5 / 6
f3 = lambda m: 600 * (5 * s5 - 11) / m**3; f2 = lambda m: 1800 * (13 * s5 - 29) / m**2; f1 = lambda m: 1440 * (47 * s5 - 105) / m
Z = lambda e: sp.simplify(sp.radsimp(sp.expand(e))) == 0
check('R3 Table 1 (600-cell) continuous at 1/2 + sqrt5/6 and (5 + sqrt5)/8 (exact)', Z(f3(w2) - f2(w2)) and Z(f2(w1) - f1(w1)))
v600 = sp.Rational(25, 4) * (2 + s5) * ((s5 - 1) / 2) ** 4       # edge 1/phi for circumradius 1
check('R3 mu < r^2: Omega = 4! vol(600-cell, circumradius 1)/mu^4 = 75(sqrt5 - 1)/mu^4, and it meets 600(5 sqrt5 - 11)/mu^3 at r^2 (exact)',
      Z(24 * v600 - 75 * (s5 - 1)) and Z(f3(r2) - 75 * (s5 - 1) / r2**4))
check('R3 mu > 1: Omega = 1440(47 sqrt5 - 105) = -151200 + 67680 sqrt5, the study value 4! vol(120-cell polar)', Z(f1(1) - (-151200 + 67680 * s5)))
im1, im2 = sp.radsimp(r2 / w1), sp.radsimp(r2 / w2)
walls = [sp.Integer(1), w1, w2, r2]
check(f'R3 turn images r^2/((5+sqrt5)/8) = {sp.simplify(im1)} = (5+2sqrt5)/10 and r^2/(1/2+sqrt5/6) = {sp.simplify(im2)} = (9+3sqrt5)/16, neither a wall',
      Z(im1 - (5 + 2 * s5) / 10) and Z(im2 - (9 + 3 * s5) / 16) and all(not Z(im - w) for im in (im1, im2) for w in walls))
print(f'PROGRESS {3}/{TASKS} R3 ({time.time()-T0:.0f} s)', flush=True)

# ---------- R4 ----------
def counts(N_fac, h, Vdir, R, mu, tol=1e-7):
    """corners of S(mu) = {n.x <= h} cap {vhat.x <= mu/R}, read from the facets of the polar conv(n/h, vhat R/mu) (qhull; coplanar
    simplices merged at 1e-7, robust where corners are not simple); per corner, the ranks of the active facet and corner normals."""
    nf = np.array(N_fac, float); nf /= np.linalg.norm(nf, axis=1)[:, None]
    nv = np.array(Vdir, float); nv /= np.linalg.norm(nv, axis=1)[:, None]
    Q = np.vstack([nf / h, nv * R / mu]); H = ConvexHull(Q)
    d = Q.shape[1]; out = set(); seen = set()
    rk = lambda M: int(np.linalg.matrix_rank(M, tol=1e-7)) if len(M) else 0
    for eq in H.equations:
        key = tuple(np.round(eq, 6))
        if key in seen: continue
        seen.add(key)
        on = np.abs(Q @ eq[:d] + eq[d]) < tol
        out.add((rk(Q[:len(nf)][on[:len(nf)]]), rk(Q[len(nf):][on[len(nf):]])))
    return out, len(seen)
# cube
D = 3
cubeN = [v for v in itertools.product([1, 0, -1], repeat=3) if sum(map(abs, v)) == 1]; cubeV = list(itertools.product([1, -1], repeat=3))
res = []
for mu, k in ((0.5, 3), (1.5, 2), (2.5, 1), (3.5, 0)):
    c, n = counts(cubeN, 1.0, cubeV, 3 ** 0.5, mu); res.append((mu, k, c, n))
check(f'R4 cube line: ranks per corner (facet normals, corner normals) by chamber {[(m, sorted(c)) for m, k, c, n in res]} = power of 1/mu',
      all(c == {(D - k, k)} for m, k, c, n in res))
c, n = counts(cubeN, 1.0, cubeV, 3 ** 0.5, 2.0)
check(f'NEG R4 at the wall mu = 2 the meet is not transversal (ranks add to more than 3) ({sorted(c)})', any(f + j > 3 for f, j in c))
# icosahedron (0, +-1, +-phi)
pf = float(phi)
icoV = [p for a in ((0, 1, pf), (1, pf, 0), (pf, 0, 1)) for p in {(a[0]*s0, a[1]*s1, a[2]*s2) for s0 in (1, -1) for s1 in (1, -1) for s2 in (1, -1)}]
icoV = [list(v) for v in {tuple(np.round(v, 12)) for v in icoV}]
H = ConvexHull(np.array(icoV)); icoN = np.unique(np.round(H.equations[:, :3], 9), axis=0); hI = float(-H.equations[0, 3])
RI = float(np.linalg.norm(icoV[0])); wI = [float(x) for x in ((7 + 3 * s5) / 6, phi ** 2, (5 + s5) / 2)]
res = []
for mu, k in ((wI[0] * 0.9, 3), ((wI[0] + wI[1]) / 2, 2), ((wI[1] + wI[2]) / 2, 1), (wI[2] * 1.1, 0)):
    c, n = counts(icoN, hI, icoV, RI, mu); res.append((round(mu, 4), k, c, n))
check(f'R4 icosahedral line: ranks by chamber {[(m, sorted(c)) for m, k, c, n in res]} = power of 1/mu',
      all(c == {(D - k, k)} for m, k, c, n in res))
# 600-cell, circumradius 1
D4 = 4
if not PILOT:
    V600 = set()
    for s in itertools.product([1, -1], repeat=4): V600.add(tuple(0.5 * x for x in s))
    for i in range(4):
        for s in (1, -1):
            v = [0.0] * 4; v[i] = s; V600.add(tuple(v))
    base = (pf / 2, 0.5, 1 / (2 * pf), 0.0)
    even = [p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
    for p in even:
        for s in itertools.product([1, -1], repeat=3):
            v = [0.0] * 4; vals = [base[0] * s[0], base[1] * s[1], base[2] * s[2], 0.0]
            for i in range(4): v[p[i]] = vals[i]
            V600.add(tuple(np.round(v, 12)))
    V600 = [list(v) for v in V600]
    H = ConvexHull(np.array(V600)); N600 = np.unique(np.round(H.equations[:, :4], 9), axis=0); h6 = float(-H.equations[0, 4])
    check(f'R4 600-cell built: {len(V600)} corners, {len(N600)} facets, inradius {h6:.7f} = r', len(V600) == 120 and len(N600) == 600 and abs(h6 - float(sp.sqrt(r2))) < 1e-9)
    w6 = [float(x) for x in (r2, w2, w1, 1)]
    # flag method (qhull merges the 120-cell's 20-corner facets unreliably): corners of S(mu) on the flag v, edge, triangle, tetrahedron;
    # c_k = centre of the k-face; in chamber j the corner is the point of the segment [c_{j-1}, c_j] (or of the ray through c_3 for j = 4)
    # where vhat.x = mu/R; all 720 constraints are evaluated there; the other corners are its images under the symmetry group
    Vn = np.array(V600); cosE = pf / 2
    v = Vn[[i for i in range(120) if abs(Vn[i] @ np.array([1., 0, 0, 0]) - 1) < 1e-9][0]]
    adj = lambda S: [q for q in Vn if all(abs(q @ a - cosE) < 1e-9 for a in S)]
    w = adj([v])[0]; u = adj([v, w])[0]; t4 = adj([v, w, u])[0]
    c = [v, (v + w) / 2, (v + w + u) / 3, (v + w + u + t4) / 4]
    nfn = np.array(N600, float); nfn /= np.linalg.norm(nfn, axis=1)[:, None]
    A = np.vstack([nfn, Vn]); b = lambda mu: np.concatenate([np.full(600, h6), np.full(120, mu)])
    rk = lambda M: int(np.linalg.matrix_rank(M, tol=1e-7)) if len(M) else 0
    res = []
    for mu, k in ((w6[0] * 0.98, 4), ((w6[0] + w6[1]) / 2, 3), ((w6[1] + w6[2]) / 2, 2), ((w6[2] + w6[3]) / 2, 1), (1.02, 0)):
        if k == 0: x = v
        elif k == 4: x = c[3] * mu / (v @ c[3])
        else:
            a0, a1 = c[k - 1], c[k]; tt = (mu - v @ a0) / (v @ (a1 - a0)); x = a0 + tt * (a1 - a0)
            assert -1e-12 <= tt <= 1 + 1e-12
        sl = A @ x - b(mu); feas = bool(sl.max() < 1e-9); act = np.abs(sl) < 1e-9
        res.append((round(mu, 4), k, (rk(A[:600][act[:600]]), rk(A[600:][act[600:]])), feas))
    check(f'R4 600-cell line (flag corner in each chamber; feasible, ranks of active facet and corner normals): {res} = (4 - j, j), j the power of 1/mu',
          all(f and cc == (4 - k, k) for m, k, cc, f in res))
print(f'PROGRESS {4}/{TASKS} R4 ({time.time()-T0:.0f} s)', flush=True)

# ---------- R5 ----------
x, y = sp.symbols('x y')
def cone_form(a, b):
    """canonical form of the cone {s a + t b : s, t >= 0} (a to b counterclockwise): det(a,b)/(det(x,b) det(a,x))."""
    X = sp.Matrix([x, y]); A = sp.Matrix(a); B = sp.Matrix(b)
    d = lambda u, v: u[0] * v[1] - u[1] * v[0]
    return sp.together(d(A, B) / (d(X, B) * d(A, X)))
random.seed(7)
def rays(m):
    # rational directions with distinct slopes, sorted by angle in (0, pi)
    sl = sorted({sp.Rational(random.randint(-60, 60), random.randint(1, 40)) for _ in range(4 * m)}, key=lambda q: -float(q))[:m]
    D = [sp.Matrix([1, q]) for q in sl]                      # angles in (-pi/2, pi/2), sorted by decreasing slope... re-sort by angle
    D = sorted(D, key=lambda v: float(sp.atan2(v[1], v[0])))
    return D + [-v for v in D]                               # 2m rays in counterclockwise order
for m in ((3, 5) if PILOT else (3, 5, 7, 9)):
    R = rays(m); secs = [cone_form(R[i], R[(i + 1) % (2 * m)]) for i in range(2 * m)]
    s_in = sp.simplify(sum(secs[0::2])); s_all = sp.simplify(sum(secs))
    check(f'R5 m = {m} lines, alternate sectors: sum of the in-sector forms = {s_in}; all 2m sectors sum to {s_all} (exact)', s_in == 0 and s_all == 0)
    if m == 3:
        bad = sp.simplify(secs[0] + secs[2] + secs[3])
        check('NEG R5 m = 3 with one in-sector swapped for its neighbour: nonzero', bad != 0)
        check('R5 a cone and its antipode have the same form (m = 3, sectors 0 and 3)', sp.simplify(secs[0] - secs[3]) == 0)
R = rays(2); secs = [cone_form(R[i], R[(i + 1) % 4]) for i in range(4)]
X = sp.Matrix([x, y]); d = lambda u, v: u[0] * v[1] - u[1] * v[0]
L1, L2 = d(R[0], X), d(R[1], X)              # the two lines through 0
f = sp.simplify((secs[0] + secs[2]) * L1 * L2)
check(f'R5 m = 2: the two opposite in-sectors have equal forms and their sum times the two line forms is the constant {f}, twice one cone (point residue 2 in absolute value)',
      sp.simplify(secs[0] - secs[2]) == 0 and f.is_number and sp.simplify(f - 2 * sp.simplify(secs[0] * L1 * L2)) == 0)
print(f'PROGRESS {5}/{TASKS} R5 ({time.time()-T0:.0f} s)', flush=True)
print(f'total {time.time()-T0:.0f} s', flush=True)
print('FINAL ok' if OK else 'FINAL FAIL', flush=True)
