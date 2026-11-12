"""Aim 2, chunk 5b (12 Nov 2026): the DICTO Yantra cones as positive geometries. Method and checks: ../README.md.
Exact (sympy rational-function identities, symbolic a, h = b - a, w > 0) except part D (dual-volume integrals: mpmath, numerical only).
Usage: python -u yantra_cones.py [pilot]"""
import sys, json, time, os
from fractions import Fraction as Fr
from multiprocessing import get_context
import sympy as sp

PILOT = sys.argv[1:] == ['pilot']
HERE = os.path.dirname(os.path.abspath(__file__))
x, y, z, m, rho, t = sp.symbols('x y z m rho t', real=True)
a = sp.Symbol('a', real=True)
h, w = sp.symbols('h w', positive=True)
C = (1 - m**2) / (1 + m**2); S = 2*m / (1 + m**2); DTH = 2 / (1 + m**2)   # rational circle, dtheta/dm


def zero(e):
    e = sp.cancel(sp.together(e))
    return e == 0 or sp.simplify(e) == 0


def pm1(e):
    """is e (a ratio of residue forms) exactly +1 or -1? returns (ok, value shown)"""
    r = sp.cancel(sp.together(e))
    if r not in (1, -1):
        r = sp.simplify(r)
    return r in (1, -1), r


def det3(P, Q, R):
    return sp.Matrix([[P[0], P[1], 1], [Q[0], Q[1], 1], [R[0], R[1], 1]]).det()


def tri_form(P0, P1, P2, X):
    """canonical form of a triangle (vertices in the plane), positive inside: D^2/(<X12><0X2><01X>) * sign D"""
    D = sp.simplify(det3(P0, P1, P2))
    sg = sp.sign(D)
    return sg * D**2 / (det3(X, P1, P2) * det3(P0, X, P2) * det3(P0, P1, X))


def cone(av, bv, wv):
    hv = bv - av; s = sp.sign(hv)
    Q = wv**2*(z - av)**2 - hv**2*(x**2 + y**2)
    B = s*(bv - z)
    return hv, s, Q, B


def half_cone_form(av, bv, wv, c=None):
    hv, s, Q, B = cone(av, bv, wv)
    cv = 2*wv*hv**2 if c is None else c
    return cv / (Q*B*y)


def halfdisc(wv):            # ABL half-disc of radius w (y >= 0)
    return 2*wv / ((wv**2 - x**2 - y**2)*y)


def lateral_res(Omega, Q, av, bv, wv):
    """Leray residue of Omega dx dy dz on the cone Q = 0, as the coefficient of dm dz (x = rho C, y = rho S, rho = w(z-a)/h)."""
    hv = bv - av
    num = sp.cancel(sp.together(Omega*Q))
    dQdr = sp.diff(Q.subs({x: rho*C, y: rho*S}), rho)
    e = num.subs({x: rho*C, y: rho*S}) * rho * DTH / dQdr
    return sp.simplify(e.subs(rho, wv*(z - av)/hv))


def checks_half_cone(av, bv, wv, tag):
    """A1 axial residue = yantra triangle; A2 base = half-disc; A3 lateral = arc x segment; A4 positivity; A5 factorisation."""
    out = []
    hv, s, Q, B = cone(av, bv, wv)
    Om = half_cone_form(av, bv, wv)
    # A1: residue on y = 0 (Jacobian 1) against the triangle apex (0,a), base (+-w, b) in (x, z)
    res_ax = sp.cancel(sp.together(Om*y)).subs(y, 0)
    T = tri_form((0, av), (wv, bv), (-wv, bv), (x, z))
    out.append((f'{tag} A1 Res(yantra plane) = triangle form', zero(res_ax - T)))
    Qax = sp.factor(Q.subs(y, 0))
    out.append((f'{tag} A1b Q on the yantra plane = product of the two legs', len(sp.factor_list(Qax)[1]) == 2))
    # A2: residue on the base z = b (|dB/dz| = 1)
    res_b = sp.cancel(sp.together(Om*B)).subs(z, bv)
    out.append((f'{tag} A2 Res(base) = half-disc form', zero(res_b - halfdisc(wv))))
    # A3: lateral residue = +-(dm/m) * segment form of the ruling (z from a to b)
    L = lateral_res(Om, Q, av, bv, wv)
    ok3, ratio = pm1(L / ((1/m) * hv/((z - av)*(bv - z))))
    out.append((f'{tag} A3 Res(cone) = (dm/m) ^ ruling segment form (ratio {ratio})', ok3))
    # A4: positive inside (numeric instances only): point on the far side of the axis plane at mid height
    if hv.is_number:
        zm = (av + bv)/2; rm = wv*(zm - av)/hv
        val = Om.subs({x: rm/5, y: rm/3, z: zm})
        out.append((f'{tag} A4 Omega > 0 inside', val > 0))
    # A5: Omega = |det M| * Omega_halfdisc(X1, X2, X3) / X4 with X = (x, y, w(z-a)/h, s(b-z)) (homogeneous chart t = 1)
    X1, X2, X3, X4 = x, y, wv*(z - av)/hv, s*(bv - z)
    Ohd = 2/((X3**2 - X1**2 - X2**2)*X2)
    detM = sp.Abs(s*wv) if hv.is_number else wv
    out.append((f'{tag} A5 half-cone = half-disc cone x ray (|det| {detM})', zero(Om - detM*Ohd/X4)))
    return out


def sector_form(av, bv, wv, d1, d2):
    """pizza slice of the cone between half-planes with unit directions d1 -> d2 (counterclockwise, angle < pi); numerator by ansatz."""
    hv, s, Q, B = cone(av, bv, wv)
    L1 = -d1[1]*x + d1[0]*y; L2 = d2[1]*x - d2[0]*y
    n = sp.symbols('n0:4'); N = n[0]*x + n[1]*y + n[2]*z + n[3]
    Om = N/(Q*B*L1*L2)
    R = tri_form((0, av), (wv, bv), (0, bv), (rho, z))     # right triangle on each half-plane
    eqs = []
    f1 = {x: rho*d1[0] - t*d1[1], y: rho*d1[1] + t*d1[0]}
    f2 = {x: rho*d2[0] + t*d2[1], y: rho*d2[1] - t*d2[0]}
    for f, Lk in ((f1, L1), (f2, L2)):
        e = sp.together(sp.cancel(sp.together(Om*Lk)).subs(f).subs(t, 0) - R)
        num = sp.expand(sp.numer(e))
        eqs += sp.Poly(num, rho, z).coeffs()
    sol = sp.solve(eqs, n, dict=True)
    if len(sol) != 1:
        return None, None
    return sp.simplify(Om.subs(sol[0])), (Q, B, L1, L2)


def mpar(d):        # stereographic parameter of a unit direction
    return sp.S(d[1])/(1 + sp.S(d[0]))


def checks_sectors(av, bv, wv, tag):
    out = []
    hv, s, Q, B = cone(av, bv, wv)
    e1, e2, e3, e4 = (1, 0), (0, 1), (-1, 0), (0, -1)
    p, q = (sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(-5, 13), sp.Rational(12, 13))
    F = {}
    for k, (d1, d2) in {'e1e2': (e1, e2), 'e2e3': (e2, e3), 'e3e4': (e3, e4), 'e4e1': (e4, e1), 'e1p': (e1, p), 'pe2': (p, e2),
                        'e1q': (e1, q), 'pq': (p, q)}.items():
        F[k], parts = sector_form(av, bv, wv, d1, d2)
        if F[k] is None:
            out.append((f'{tag} S0 sector {k}: ansatz has a unique solution', False)); return out
    out.append((f'{tag} S0 every sector ansatz solved uniquely (residues on both half-planes = right triangles)', True))
    # base residue of slice e1->p = pizza slice: its residues on the circle = arc form (m from 0 to 1/2), on the radii = segment [0, w]
    Om = F['e1p']; Lb = sp.cancel(sp.together(Om*B)).subs(z, bv)
    q2 = sp.cancel(sp.together(Lb*(wv**2 - x**2 - y**2)))       # remove the circle factor
    arc = sp.simplify((q2.subs({x: rho*C, y: rho*S})*rho*DTH/sp.diff(wv**2 - rho**2, rho)).subs(rho, wv))
    m1, m2 = mpar(e1), mpar(p)
    ok1, r1 = pm1(arc / ((m2 - m1)/((m - m1)*(m2 - m))))
    out.append((f'{tag} S1 pizza slice: Res(circle) = arc form m in [{m1},{m2}] (ratio {r1})', ok1))
    rad = sp.cancel(sp.together(Lb*y)).subs(y, 0).subs(x, rho)
    ok2, r2 = pm1(rad / (wv/(rho*(wv - rho))))
    out.append((f'{tag} S2 pizza slice: Res(radius) = segment [0, w] (ratio {r2})', ok2))
    # lateral residue of the slice = arc form x ruling segment form
    Lat = lateral_res(Om, Q, av, bv, wv)
    ok3, r3 = pm1(Lat / ((m2 - m1)/((m - m1)*(m2 - m)) * hv/((z - av)*(bv - z))))
    out.append((f'{tag} S3 slice: Res(cone) = arc form ^ ruling segment form (ratio {r3})', ok3))
    out.append((f'{tag} S4 joins: S(e1,p) + S(p,e2) = S(e1,e2) (pole on the inner half-plane cancels)', zero(F['e1p'] + F['pe2'] - F['e1e2'])))
    out.append((f'{tag} S5 joins: S(e1,p) + S(p,q) = S(e1,q)', zero(F['e1p'] + F['pq'] - F['e1q'])))
    out.append((f'{tag} S6 two quarter slices = half-cone', zero(F['e1e2'] + F['e2e3'] - half_cone_form(av, bv, wv))))
    out.append((f'{tag} S7 four quarter slices round the axis sum to 0', zero(F['e1e2'] + F['e2e3'] + F['e3e4'] + F['e4e1'])))
    return out


def checks_120(av, bv, wv, tag):
    r3 = sp.sqrt(3)
    d = [(1, 0), (-sp.Rational(1, 2), r3/2), (-sp.Rational(1, 2), -r3/2)]
    tot = 0
    for k in range(3):
        f, _ = sector_form(av, bv, wv, d[k], d[(k+1) % 3])
        if f is None:
            return [(f'{tag} S8 120-degree slice solved', False)]
        tot += f
    return [(f'{tag} S8 the three 120-degree slices (the three stella positions, #103 Prop. 4) sum to 0', zero(tot))]


def check_zero_ring(c1, c2, tag):
    """Solid of revolution between two coaxial cones: Omega = N/(Q1 Q2 B1 B2), deg N = 2; residues must be 0 on both cones
    (their bands are bounded by full circles) -> N vanishes on both cones -> N = 0."""
    mons = [x**i*y**j*z**k for i in range(3) for j in range(3) for k in range(3) if i + j + k <= 2]   # 10 (t = 1 chart)
    rows = []
    for (av, bv, wv) in (c1, c2):
        hv = bv - av
        for zz in [av + (bv - av)*sp.Rational(k, 7) for k in range(1, 6)]:
            for mm in [sp.Rational(j, 3) for j in range(-3, 4)]:
                rr = wv*(zz - av)/hv
                pt = {x: rr*C.subs(m, mm), y: rr*S.subs(m, mm), z: zz}
                rows.append([mo.subs(pt) for mo in mons])
    M = sp.Matrix(rows)
    return [(f'{tag} Z2 ring between two cones: residue-zero conditions leave only N = 0 (nullity {len(mons) - M.rank()})', M.rank() == len(mons))]


def check_zero_annulus(tag):
    mons = [x**i*y**j for i in range(2) for j in range(2) if i + j <= 1]    # deg N = 4 - 3 = 1
    rows = []
    for rad in (1, sp.Rational(5, 2)):
        for mm in [sp.Rational(j, 3) for j in range(-3, 4)]:
            rows.append([mo.subs({x: rad*C.subs(m, mm), y: rad*S.subs(m, mm)}) for mo in mons])
    M = sp.Matrix(rows)
    return [(f'{tag} Z1 annulus: only N = 0 (disc and full cone: numerator degree < 0, Omega = 0 outright)', M.rank() == len(mons))]


def universal():
    """least point of Omega(H0), H0 = {x^2+y^2 <= (1-z)^2, 0 <= z <= 1, y >= 0}; Omega_min vol / 3!"""
    out = []
    Om = half_cone_form(sp.Integer(1), sp.Integer(0), sp.Integer(1))
    D = sp.together(1/Om)
    crit = sp.solve([sp.diff(D, v) for v in (x, y, z)], [x, y, z], dict=True)
    real = [c for c in crit if all(v.is_real for v in c.values())]
    inside = [c for c in real if c[y] > 0 and 0 < c[z] < 1 and c[x]**2 + c[y]**2 < (1 - c[z])**2]
    out.append(('U1 one critical point of Omega(H0) inside', len(inside) == 1))
    p = inside[0]
    Hs = sp.hessian(sp.log(Om), (x, y, z)).subs(p)
    minors = [sp.simplify(Hs[:k, :k].det()) for k in (1, 2, 3)]
    out.append((f'U2 it is a minimum (leading minors of the Hessian of log Omega: {minors})', all(v > 0 for v in minors)))
    Omin = sp.nsimplify(sp.simplify(Om.subs(p)))
    prod = sp.simplify(Omin * (sp.pi/6) / 6)
    out.append((f'U3 least point {p}, Omega_min = {Omin}, Omega_min*vol/3! = {prod} = {sp.N(prod, 15)}', sp.simplify(prod - 64*sp.sqrt(3)*sp.pi/81) == 0))
    return out, p, prod


def checks_instance(i, cone_i, prod):
    av, bv, wv = cone_i
    out = checks_half_cone(av, bv, wv, f'cone {i}')
    hv = bv - av
    Om = half_cone_form(av, bv, wv)
    p = {x: 0, y: wv*sp.sqrt(3)/4, z: bv - hv/4}     # image of the H0 least point
    grad = [sp.simplify(sp.diff(sp.log(Om), v).subs(p)) for v in (x, y, z)]
    val = sp.simplify(Om.subs(p) * (sp.pi*wv**2*sp.Abs(hv)/6) / 6)
    out.append((f'cone {i} U4 least point at (0, w sqrt3/4, b - h/4), Omega_min*vol/3! = 64 sqrt3 pi/81', all(g == 0 for g in grad) and sp.simplify(val - prod) == 0))
    return out


def controls_exact():
    out = []
    # ABL half-disc: residue on y=0 is 2/(1-x^2), whose residues at x = -1, 1 are +-1
    Om = halfdisc(1)
    r = sp.cancel(sp.together(Om*y)).subs(y, 0)
    out.append(('C1 ABL half-disc: Res(y=0) = segment form 2/(1-x^2)', zero(r - 2/(1 - x**2))))
    out.append(('C1b ... its residues at x = -1, 1 are +-1', sp.limit((x + 1)*r, x, -1) == 1 and sp.limit((x - 1)*r, x, 1) == -1))
    # Mazzucchelli-Raman (55): canonical function c/(q l), l = x2 + a x3, residues +-1 at L n Q -> c = 2 sqrt(1 - a^2); a = 1/2: sqrt3
    av = sp.Rational(1, 2); cc = sp.Symbol('cc')
    rr = sp.cancel(sp.together(cc/((1 - x**2 - y**2)*(y + av))*(y + av))).subs(y, -av)
    xe = sp.sqrt(1 - av**2)
    c_sol = sp.solve(sp.limit((x - xe)*rr, x, xe) + 1, cc)
    out.append((f'C2 M-R (55) at a = 1/2: residue code gives c = {c_sol} (expect sqrt3)', c_sol == [sp.sqrt(3)]))
    return out


def negatives():
    out = []
    # N1 wrong constant
    Om = half_cone_form(a, a + h, w, c=3*w*h**2)
    hv, s, Q, B = cone(a, a + h, w)
    d1 = sp.factor(sp.cancel(sp.together(Om*B)).subs(z, a + h) - halfdisc(w))
    out.append((f'N1 wrong constant 3wh^2: base residue minus half-disc form = {d1} (nonzero: caught)', d1.is_finite is not False and d1 != 0 and d1 != sp.nan))
    # N2 level cut not through the apex: Q at z = a + h/2 is definite in (x, y): no real lines
    Qz = sp.expand(Q.subs(z, a + h/2))
    P = sp.Poly(Qz, x, y)
    out.append(('N2 a level cut gives a circle, not a triangle (quadratic part definite, no real line factors) (caught)',
                P.coeff_monomial(x**2) * P.coeff_monomial(y**2) - (P.coeff_monomial(x*y)/2)**2 > 0))
    # N3 mis-joined halves: H+ of cone(a) + H- of cone(a + 1/7): pole left on y = 0
    Hp = half_cone_form(a, a + h, w); Hm = -half_cone_form(a + sp.Rational(1, 7), a + h, w)
    res = sp.cancel(sp.together((Hp + Hm)*y)).subs(y, 0)
    val = res.subs({a: 0, h: 1, w: 1, x: sp.Rational(1, 5), z: sp.Rational(1, 2)})
    out.append((f'N3 mis-joined halves (apex moved 1/7) leave a pole on the yantra plane: residue at a sample point = {val} (caught)', val.is_number and val != 0 and val != sp.nan))
    # Z3: the true join H+ + H- = 0 (pole cancels and the whole cone has Omega = 0)
    # Z3: H- is the mirror image y -> -y of H+ (|det| 1), so Omega(H-)(x, y, z) = Omega(H+)(x, -y, z); the true join cancels
    out.append(('Z3 H+ + H- = 0 identically: the pole on the cut cancels and the full cone has Omega = 0', zero(Hp + Hp.subs(y, -y))))
    return out


# ---------------- part D: dual volumes (numerical, mpmath) ----------------
def dual_task(args):
    import mpmath as mp
    kind, xv, dps = args
    mp.mp.dps = dps
    x1, x2, x3 = [mp.mpf(v) for v in xv]
    lin = lambda A, Bv: x1*A + x2*Bv + x3
    f = lambda A, Bv, mu: 2*mu/lin(A, Bv)**3
    def disc(mu, cut=0):     # integral over the unit disc, polar; split where the weight jumps on the circle (sin phi = cut)
        g = lambda r, ph: f(r*mp.cos(ph), r*mp.sin(ph), mu(r*mp.cos(ph), r*mp.sin(ph), r))*r
        c0 = mp.asin(cut)
        return mp.quad(g, [0, 1], sorted(set([c0, mp.pi - c0, mp.pi, 2*mp.pi + c0])) if cut else [0, mp.pi, 2*mp.pi])
    q = x3**2 - x1**2 - x2**2
    if kind == 'lorentz':
        return kind, xv, disc(lambda A, Bv, r: 1), 2*mp.pi/q**mp.mpf(1.5)
    if kind == 'triangle':   # dual slice triangle with vertices v (cone generated by (v, 1))
        V = [(mp.mpf(0), mp.mpf(-1)), (mp.mpf(1), mp.mpf(1)), (mp.mpf(-1), mp.mpf(1))]
        (ax, ay), (bx, by), (cx, cy) = V
        jac = abs((bx - ax)*(cy - by) - (by - ay)*(cx - bx))      # P = A + s(B - A) + s u (C - B), dP = s jac ds du
        g = lambda s_, u_: f(ax + s_*(bx - ax) + s_*u_*(cx - bx), ay + s_*(by - ay) + s_*u_*(cy - by), 1)*s_*jac
        I = mp.quad(g, [0, 1], [0, 1])
        L = [(vx, vy, 1) for vx, vy in V]
        det = mp.matrix([list(r) for r in L]); dd = abs(mp.det(det))
        expect = dd / mp.fprod([l[0]*x1 + l[1]*x2 + l[2]*x3 for l in L])
        return kind, xv, I, expect
    if kind.startswith('half'):          # a = 0: slice = disc U strip {|A| <= 1, B >= 0}
        mode = kind.split('-')[1]
        sg = {'MR': 1, 'flip': -1, 'plain': 0}[mode]
        mu_d = (lambda A, Bv, r: mp.mpf(1)) if sg == 0 else (lambda A, Bv, r: mp.mpf(1)/2 + sg*mp.atan(Bv/mp.sqrt(1 - r**2))/mp.pi)
        I = disc(mu_d)
        I += mp.quad(lambda Bv: mp.quad(lambda A: f(A, Bv, 1), [-1, -mp.sqrt(1 - Bv**2)]) + mp.quad(lambda A: f(A, Bv, 1), [mp.sqrt(1 - Bv**2), 1]), [0, 1])
        I += mp.quad(lambda Bv: mp.quad(lambda A: f(A, Bv, 1), [-1, 1]), [1, mp.inf])
        return kind, xv, I, 2/(q*x2)
    if kind.startswith('pizza'):         # M-R a = 1/2: slice = conv(disc, (0, 2))
        mode = kind.split('-')[1]; aa = mp.mpf(1)/2
        sg = {'MR': 1, 'plain': 0}[mode]
        mu_d = (lambda A, Bv, r: mp.mpf(1)) if sg == 0 else (lambda A, Bv, r: mp.mpf(1)/2 + mp.atan((Bv - aa)/mp.sqrt((1 - aa**2)*(1 - r**2)))/mp.pi)
        I = disc(mu_d, cut=aa)
        s3 = mp.sqrt(3)
        I += mp.quad(lambda Bv: mp.quad(lambda A: f(A, Bv, 1), [-(2 - Bv)/s3, -mp.sqrt(1 - Bv**2)]) + mp.quad(lambda A: f(A, Bv, 1), [mp.sqrt(1 - Bv**2), (2 - Bv)/s3]), [aa, 1])
        I += mp.quad(lambda Bv: mp.quad(lambda A: f(A, Bv, 1), [-(2 - Bv)/s3, (2 - Bv)/s3]), [1, 2])
        return kind, xv, I, mp.sqrt(3)/(q*(x2 + aa*x3))


def run_task(task):
    kind, arg = task
    if kind == 'dual':
        return ('dual', dual_task(arg))
    return ('checks', run_checks(kind, arg))


def run_checks(kind, arg):
    if kind == 'generic_half':
        return checks_half_cone(a, a + h, w, 'generic')
    if kind == 'generic_sectors':
        return checks_sectors(a, a + h, w, 'generic')
    if kind == 'generic_120':
        return checks_120(a, a + h, w, 'generic')
    if kind == 'controls':
        return controls_exact() + check_zero_annulus('generic')
    if kind == 'negatives':
        return negatives()
    if kind == 'instance':
        i, ci, prod = arg
        return checks_instance(i, ci, prod)
    if kind == 'instance_sectors':
        i, ci = arg
        return checks_sectors(*ci, f'cone {i}')
    if kind == 'ring':
        (i, ci), (j, cj) = arg
        return check_zero_ring(ci, cj, f'cones {i},{j}')


if __name__ == '__main__':
    T0 = time.time()
    data = json.load(open(os.path.join(HERE, '..', 'data', 'gf1-cones.json')))
    cones = {int(k): (sp.Rational(v['apex']), sp.Rational(v['base']), sp.Rational(v['halfwidth'])) for k, v in data['cones'].items()}
    print(f'DICTO Yantra GF1, u = {data["u"]} (degree 160): nine cones (apex, base, half-width) as exact 40-digit rationals', flush=True)
    for k, (av, bv, wv) in sorted(cones.items()):
        print(f'  cone {k}: apex {float(av):.10f} base {float(bv):.10f} w {float(wv):.10f} {"apex up" if bv < av else "apex down"}', flush=True)
    OK = True
    def rep(lines):
        global OK
        for name, ok in lines:
            print(('ok   ' if ok else 'FAIL ') + name, flush=True); OK &= bool(ok)
    uni, p0, prod = universal(); rep(uni)
    print('PROGRESS 0.10 universal', flush=True)
    idx = [3, 7] if PILOT else sorted(cones)
    dps = 12 if PILOT else 20
    pts_half = [('0.1', '0.3', '1'), ('-0.2', '0.5', '1')] if not PILOT else [('0.1', '0.3', '1')]
    pts_pz = [('0.1', '-0.3', '1'), ('0.2', '0.4', '1')] if not PILOT else [('0.2', '0.4', '1')]
    tasks = [('generic_half', None), ('generic_sectors', None), ('generic_120', None), ('controls', None), ('negatives', None)]
    tasks += [('instance', (i, cones[i], prod)) for i in idx]
    tasks += [('instance_sectors', (i, cones[i])) for i in (idx[:1] if PILOT else [1, 3, 7])]
    tasks += [('ring', ((1, cones[1]), (2, cones[2])))]
    dual = [('lorentz', ('0.1', '0.2', '1')), ('lorentz', ('0.3', '-0.1', '1')), ('triangle', ('0.1', '0.2', '1'))]
    dual += [(f'half-{mo}', p) for p in pts_half for mo in ('MR', 'plain', 'flip')]
    dual += [(f'pizza-{mo}', p) for p in pts_pz for mo in ('MR', 'plain')]
    tasks += [('dual', (k, p, dps)) for k, p in dual]
    ctx = get_context('fork')
    done = 0; ND = len(tasks)
    duals = []
    with ctx.Pool(4) as pool:
        for typ, res in pool.imap_unordered(run_task, tasks):
            done += 1
            if typ == 'dual':
                duals.append(res)
            else:
                rep(res)
            print(f'PROGRESS {0.1 + 0.9*done/ND:.2f} task {done}/{ND} ({time.time() - T0:.0f} s)', flush=True)
    import mpmath as mp
    mp.mp.dps = dps
    tol = mp.mpf(10)**(-(dps - 6))
    print(f'Part D, dual volumes (NUMERICAL ONLY, mpmath {dps} digits; tolerance {mp.nstr(tol, 3)}):', flush=True)
    for kind, xv, I, E in sorted(duals, key=lambda r: (r[0], r[1])):
        rel = abs(I - E)/abs(E)
        expect_match = kind.endswith('MR') or kind in ('lorentz', 'triangle')
        ok = (rel < tol) if expect_match else (rel > mp.mpf('1e-3'))
        what = 'matches' if expect_match else 'must NOT match (negative control)'
        print(('ok   ' if ok else 'FAIL ') + f'D {kind} at x = {xv}: integral {mp.nstr(I, 15)} vs Omega {mp.nstr(E, 15)}, rel diff {mp.nstr(rel, 3)} ({what})', flush=True)
        OK &= bool(ok)
    print(f'time {time.time() - T0:.0f} s', flush=True)
    print('PROGRESS 1.00 done', flush=True)
    print('FINAL ok: all checks and controls held' if OK else 'FINAL FAIL: a check or control failed', flush=True)
