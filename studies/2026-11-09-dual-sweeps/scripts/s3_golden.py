"""Birds 3 and 4: golden cuts on the polar lines.
A. Cube-octahedron line (known case): the four golden cuts of #88 (Icosaxes, Unborn Axes, Greater and Lesser Golden Cut Cubes)
   as roots of 4x4 determinants once the golden ray of the moving solid's edge (a fixed plane through the centre) is added.
B. #89's golden rhombic cuts (RD, RT): are they on CO ∩ mu RD / ID ∩ mu RT? (exact, from #89 Theorem 3's closed forms)
C. Golden stations of the octagon hop on both lines (side ratios phi^{±1}), and the equal-corner-side point.
Exact: sympy for A, B; sweeplib exact fields + sympy for C."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
logf = open(os.path.join(os.path.dirname(__file__), '..', 'data', 's3_golden.log'), 'w')
def log(s): print(s); logf.write(s + '\n'); logf.flush()
checks = []
phi = (1 + sp.sqrt(5)) / 2
m = sp.symbols('mu', positive=True)
Mx = lambda rows: sp.Matrix(rows)
# ---------- A. cube-octahedron line: P_mu = cube [-1,1]^3 ∩ mu·oct {|x|+|y|+|z| <= mu}
log('A. cube-octahedron line, golden cuts as walls of the arrangement + golden rays')
# octahedron side (1 < mu < 2): oct edge from (mu,0,0) to (0,mu,0) lies on x+y+z = mu, x+y-z = mu; cube plane x = 1 cuts it.
# the corner of the oct cut at fraction x of the edge; golden: (1-2x)/x = phi (lesser, x = 1/(phi+2)) or 1/phi (greater, x = 1/phi^2)
res = {}
for name, x in [('Unborn Axes (Lesser Golden Cut Octahedron)', 1 / (phi + 2)), ('Icosaxes (Greater Golden Cut Octahedron)', 1 / phi ** 2)]:
    # golden ray: the point (1-x, x, 0)·mu; plane through the centre containing it and the z axis: x·X - (1-x)·Y = 0
    rows = [[1, 0, 0, -1], [1, 1, 1, -m], [1, 1, -1, -m], [x, -(1 - x), 0, 0]]
    d = sp.expand(Mx(rows).det())
    root = sp.solve(d, m)
    lin = sp.degree(sp.Poly(d, m)) == 1
    mu0 = sp.nsimplify(sp.simplify(root[0]), [sp.sqrt(5)])
    # check the hexagon: corner side sqrt2(mu-1), remnant sqrt2(2-mu)
    ratio = sp.simplify((2 - mu0) / (mu0 - 1))
    log(f'  {name}: det = {sp.simplify(d)} (linear {lin}), mu = {sp.radsimp(mu0)} (~{float(mu0):.10f}); hexagon remnant/corner = {sp.radsimp(ratio)}')
    res[name] = mu0
    checks.append((f'{name}: det linear, golden hexagon', lin and sp.simplify(ratio - (phi if 'Unborn' in name else 1 / phi)) == 0))
checks.append(('Icosaxes at mu = phi, Unborn Axes at mu = 3 - phi', sp.simplify(res['Icosaxes (Greater Golden Cut Octahedron)'] - phi) == 0 and sp.simplify(res['Unborn Axes (Lesser Golden Cut Octahedron)'] - (3 - phi)) == 0))
# cube side (2 < mu < 3): the cube edge from (1,1,1) to (1,1,-1) lies on x = 1, y = 1; the oct plane x+y+z = mu cuts it at z = mu-2.
# octagon on x = 1: corner side sqrt2 (3 - mu), original side 2(mu - 2). golden: 2(mu-2) = phi^{±1} sqrt2 (3-mu)
for name, g in [('Lesser Golden Cut Cube', phi), ('Greater Golden Cut Cube', 1 / phi)]:
    mu0 = sp.solve(sp.Eq(2 * (m - 2), g * sp.sqrt(2) * (3 - m)), m)[0]
    # as a wall: here the MOVING family is the octahedron, the cut edge belongs to the FIXED cube; the golden point
    # (1, 1, 1 - 2x) is fixed and the moving plane x+y+z = mu passes through it: the 4 planes x = 1, y = 1, oct, and z = 1 - 2x
    xg = sp.solve(sp.Eq((1 - 2 * sp.Symbol('x')) / (sp.sqrt(2) * sp.Symbol('x')), g), sp.Symbol('x'))[0]
    rows = [[1, 0, 0, -1], [0, 1, 0, -1], [1, 1, 1, -m], [0, 0, 1, -(1 - 2 * xg)]]
    d = sp.expand(Mx(rows).det()); lin = sp.degree(sp.Poly(d, m)) == 1
    r2 = sp.solve(d, m)[0]
    log(f'  {name}: mu = {sp.radsimp(sp.simplify(mu0))} (~{float(mu0):.10f}); wall det (x=1, y=1, oct, golden plane z = 1-2x_g) linear {lin}, root agrees: {sp.simplify(r2 - mu0) == 0}')
    checks.append((f'{name}: det linear, root = golden cut', lin and sp.simplify(r2 - mu0) == 0))
log('  none of these four is a wall of S(mu) itself: the face-structure walls are 1, 2, 3 only (s0); the golden cuts sit inside the hops (1,2) and (2,3)')
# ---------- B. golden rhombic cuts of #89 (Theorem 3 closed forms)
log('B. #89 golden rhombic cuts versus the second dual sweeps')
def golden_rhombic(cosA):
    sa = sp.sqrt((1 - cosA) / 2); ca = sp.sqrt((1 + cosA) / 2)
    K = (1 / sa + 1 / ca) / 2
    out = {}
    bG = 1 / (1 + phi * K); aG = phi * bG
    bL = 1 / (1 + K / phi); aL = bL / phi
    for nm, a in [('Greater', aG), ('Lesser', aL)]:
        out[nm] = (sp.simplify(a / (2 * sa)), sp.simplify(a / (2 * ca)))
    return out
# RD = {|x_i|+|x_j| <= 1}: sharp corners e_i, blunt (1/2,1/2,1/2); cos(alpha) = 1/3; edge sqrt3/2.
# a cut at fraction y of the edge: sharp plane x = 1 - y/2 (cube family), blunt plane x+y+z = 3/2 - y/2 (oct family).
gRD = golden_rhombic(sp.Rational(1, 3))
tab2 = {'Greater': (0.413095, 0.292102), 'Lesser': (0.279685, 0.197767)}
for nm, (ys, yb) in gRD.items():
    c = 1 - ys / 2; t = sp.Rational(3, 2) - yb / 2
    k = sp.radsimp(sp.simplify(t / c)); nu = sp.radsimp(sp.simplify(1 / c))
    log(f'  {nm} Golden Cut Rhombic Dodecahedron: y_sharp {float(ys):.6f}, y_blunt {float(yb):.6f} (#89 Table 2: {tab2[nm]}); '
        f'minimal polynomial of k: {sp.minimal_polynomial(k, sp.Symbol("z"))}; '
        f'= P_k ∩ nu·RD with P_k = cube ∩ k·oct, k = t/c = {k} (~{float(k):.10f}), nu = {nu} (~{float(nu):.10f}); on CO ∩ mu RD needs k = 2: {sp.simplify(k - 2) == 0}')
    checks.append((f'{nm} GCRD matches #89 Table 2', abs(float(ys) - tab2[nm][0]) < 2e-6 and abs(float(yb) - tab2[nm][1]) < 2e-6))
    checks.append((f'{nm} GCRD is NOT on the CO-RD line (k != 2)', sp.simplify(k - 2) != 0))
# the CO-RD line meets the alternating family (equal corner sides) once: octagon corner sides 2(mu-1) (squares), sqrt2(3mu-4) (triangles)
mA = sp.solve(sp.Eq(2 * (m - 1), sp.sqrt(2) * (3 * m - 4)), m)[0]
log(f'  CO-RD line: equal corner sides only at mu = {sp.radsimp(mu0 := mA)} (~{float(mA):.10f}), outside the octagon hop (4/3, 3/2); '
    f'there 2(mu-1) - sqrt2(3mu-4) > 0 throughout (values {float(2*(sp.Rational(4,3)-1)):.4f} -> {float(2*(sp.Rational(3,2)-1) - sp.sqrt(2)*(sp.Rational(9,2)-4)):.4f})')
checks.append(('CO-RD: equal corner sides at (10+sqrt2)/7, outside (4/3,3/2)', sp.simplify(mA - (10 + sp.sqrt(2)) / 7) == 0 and float(mA) > 1.5))
# RT: use sweeplib's exact ID/RT (orientation of s2). sharp corners (5-fold) at u/H_u, blunt (3-fold) at c/H_c.
import sweeplib as L
from sweeplib import F, Q, ZERO, ONE, dot
L.set_field(5)
_phi_sym = phi
exec(open(os.path.join(os.path.dirname(__file__), 's2_geometry.py')).read())
phi = _phi_sym
S5 = lambda e: e.sym()
u, Hu = pl[0][0], pl[0][1]
V = [S5(z) / S5(Hu) for z in u]
# a neighbouring 3-fold corner: the triangle-centre direction c with c.u largest
best = max(range(12, 32), key=lambda k: float(dot(pl[k][0], u) / pl[k][1]))
cc, Hc = pl[best][0], pl[best][1]
W = [S5(z) / S5(Hc) for z in cc]
Vv, Wv = sp.Matrix(V), sp.Matrix(W)
edge = sp.sqrt(sp.simplify((Vv - Wv).dot(Vv - Wv)))
uh = sp.Matrix([S5(z) for z in u]); uh = uh / sp.sqrt(uh.dot(uh))
ch = sp.Matrix([S5(z) for z in cc]); ch = ch / sp.sqrt(ch.dot(ch))
cosA = sp.nsimplify(sp.Rational(1, 1) - 0)  # placeholder, replaced below
# acute angle at the 5-fold corner: between two edges from V to two 3-fold neighbours
nb = sorted(range(12, 32), key=lambda k: -float(dot(pl[k][0], u) / pl[k][1]))[:2]
W1 = sp.Matrix([S5(z) / S5(pl[nb[0]][1]) for z in pl[nb[0]][0]]); W2 = sp.Matrix([S5(z) / S5(pl[nb[1]][1]) for z in pl[nb[1]][0]])
e1, e2 = W1 - Vv, W2 - Vv
cosA = sp.radsimp(sp.simplify(e1.dot(e2) / sp.sqrt(e1.dot(e1) * e2.dot(e2))))
log(f'  RT: acute angle cos = {cosA} (~{float(cosA):.10f}); tan(alpha/2) = {float(sp.sqrt((1-cosA)/(1+cosA))):.10f} (1/phi = {float(1/phi):.10f})')
gRT = golden_rhombic(cosA)
tab2 = {'Greater': (0.440942, 0.272517), 'Lesser': (0.301265, 0.186192)}
h5 = S5(Hu) / sp.sqrt(uh.dot(uh) * 0 + sum(S5(z) ** 2 for z in u)); h3 = S5(Hc) / sp.sqrt(sum(S5(z) ** 2 for z in cc))
for nm, (ys, yb) in gRT.items():
    d5 = uh.dot(Vv + ys * (Wv - Vv)); d3 = ch.dot(Wv + yb * (Vv - Wv))
    k = sp.simplify((d5 / d3) / (h5 / h3))
    log(f'  {nm} Golden Cut Rhombic Triacontahedron: y_sharp {float(ys):.6f}, y_blunt {float(yb):.6f} (#89 Table 2: {tab2[nm]}); '
        f'(pentagon plane / triangle plane) divided by the ID ratio h5/h3 = {float(k):.10f}; on ID ∩ mu RT needs 1')
    checks.append((f'{nm} GCRT matches #89 Table 2', abs(float(ys) - tab2[nm][0]) < 2e-6 and abs(float(yb) - tab2[nm][1]) < 2e-6))
    checks.append((f'{nm} GCRT is NOT on the ID-RT line', abs(float(k) - 1) > 1e-6))
for n, ok in checks: log(('ok   ' if ok else 'FAIL ') + n)
allok = all(ok for _, ok in checks)
log('FINAL ok' if allok else 'FINAL FAIL: ' + '; '.join(n for n, ok in checks if not ok))
