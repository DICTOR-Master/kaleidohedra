#!/usr/bin/env python3
"""Swaps and fixed points (13 Nov 2026): exact checks of the fixed-point claims that can be checked cheaply.

Every decision is made in exact arithmetic (sympy: rationals, sqrt2, sqrt3, sqrt5). Floats are used only as sort keys
(ordering the corners round a face) and never decide a check.

K1  cube-octahedron line S(mu) = [-1,1]^3 cap {|x|+|y|+|z| <= mu}: isoperimetric quotient stationary exactly at the turn's
    fixed point sqrt3 (Lindelof), maximum there; closed forms controlled by an independent polytope engine.
K2  self-dual tetrahedron line: S(mu) = mu * (-S(1/mu)) (exact similarity), so IQ(mu) = IQ(1/mu); IQ largest at mu = 1 (octahedron).
K3  CsCl pair swap mu <-> 3 - mu (Kelvin's cell at mu = 3/2): the two cells tile the lattice cell (volumes add to 8); wall area
    W(mu) symmetric; A'' < 0 so W is concave and its maximum is the fixed point (symmetry + concavity).
K4  Dehn invariant on the same pair: coefficient L_hh - L_sh/2 = 12 sqrt2 (3 - 2 mu), odd under the swap, zero only at 3/2;
    dihedral relation 2 theta_sh + theta_hh = 0 mod pi checked exactly.
K5  Turn law on the C-O line: t_min(mu) = max x.y over corner pairs of S(mu) and S(3/mu), equal to #43 study Prop. D closed form;
    symmetric under mu -> 3/mu; maximum 5 - 2 sqrt3 at sqrt3.
K6  Galois swap sigma (sqrt5 -> -sqrt5, sqrt2 -> -sqrt2) on the ten golden cuts of #88: which are fixed, which are swapped.
K7  AB line t <-> 1/(2t): squares per rhombus (1 + 2t^2)/(4t) is turn-invariant and least at the fixed point 1/sqrt2.
K8  Sweep reversal i -> d - i on corner events of simple d-polytopes: Eulerian h-vectors of the permutohedra are symmetric; a
    self-reverse event class (the pure swap) exists exactly when d is even (d = 4: 26, 66, 26).
K9  NEW LOOK: the Galois-fixed golden cut (dodecahedron cut at 1/3): is its degree-6 icosahedral tone silent? Tone along the whole
    cut line x in (0, 1/2): exact zeros, compared with the cut values 1/3, x2 and their twins.
Output: PROGRESS lines, one 'ok'/'FAIL' line per check, data/swap-checks.json, last line FINAL ok / FINAL FAIL.
"""
import json, sys, time, itertools, math
import sympy as sp

T0 = time.time()
R = sp.Rational
s2, s3, s5 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
phi = (1 + s5) / 2
mu = sp.symbols('mu', positive=True)
CHECKS, DATA = [], {}
NSTEPS = 9


def check(name, cond, detail=''):
    ok = bool(cond)
    CHECKS.append((name, ok, str(detail)))
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + str(detail) if detail else ''), flush=True)


def progress(k, what):
    print(f'PROGRESS {k / NSTEPS:.2f} {what} ({time.time() - T0:.1f} s)', flush=True)


def z(e):
    return sp.simplify(sp.nsimplify(e)) == 0 if not isinstance(e, (int, sp.Rational)) else e == 0


def iszero(e):
    e = sp.radsimp(sp.expand(e))
    return sp.simplify(e) == 0


# ---------------------------------------------------------------- exact polytope engine (planes n.x <= b, n and b exact)
def polytope(planes):
    verts = []
    for (a, b, c) in itertools.combinations(range(len(planes)), 3):
        M = sp.Matrix([planes[i][0] for i in (a, b, c)])
        if M.det() == 0:
            continue
        v = M.LUsolve(sp.Matrix([planes[i][1] for i in (a, b, c)]))
        v = [sp.nsimplify(sp.radsimp(t)) for t in v]
        if all(sp.simplify(sum(n[j] * v[j] for j in range(3)) - bb) <= 0 for n, bb in planes):
            if not any(all(sp.simplify(v[j] - w[j]) == 0 for j in range(3)) for w in verts):
                verts.append(v)
    faces = []
    for k, (n, b) in enumerate(planes):
        on = [i for i, v in enumerate(verts) if sp.simplify(sum(n[j] * v[j] for j in range(3)) - b) == 0]
        if len(on) < 3:
            continue
        cen = [sum(float(verts[i][j]) for i in on) / len(on) for j in range(3)]
        nf = [float(t) for t in n]
        u = [float(verts[on[0]][j]) - cen[j] for j in range(3)]
        w = [nf[1] * u[2] - nf[2] * u[1], nf[2] * u[0] - nf[0] * u[2], nf[0] * u[1] - nf[1] * u[0]]
        def ang(i):
            d = [float(verts[i][j]) - cen[j] for j in range(3)]
            return math.atan2(sum(d[j] * w[j] for j in range(3)), sum(d[j] * u[j] for j in range(3)))
        faces.append((k, sorted(on, key=ang)))
    return verts, faces


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def measures(planes):
    """volume, surface area, edge list with the plane pair of each edge"""
    verts, faces = polytope(planes)
    V, A = 0, 0
    edges = {}
    for k, cyc in faces:
        n, b = planes[k]
        nn = sum(t * t for t in n)
        S = [0, 0, 0]
        for i in range(len(cyc)):
            p, q = verts[cyc[i]], verts[cyc[(i + 1) % len(cyc)]]
            c = cross(p, q)
            S = [S[j] + c[j] for j in range(3)]
            key = tuple(sorted((cyc[i], cyc[(i + 1) % len(cyc)])))
            edges.setdefault(key, []).append(k)
        dot = sum(n[j] * S[j] for j in range(3))
        A += sp.Abs(dot) / (2 * sp.sqrt(nn))
        V += b * sp.Abs(dot) / (6 * nn)
    return verts, sp.nsimplify(sp.radsimp(V)), sp.radsimp(A), edges


def co_planes(m, centre=(0, 0, 0)):
    cx, cy, cz = centre
    P = []
    for j in range(3):
        for sg in (1, -1):
            n = [0, 0, 0]; n[j] = sg
            P.append((n, sg * centre[j] + 1))
    for sg in itertools.product((1, -1), repeat=3):
        n = list(sg)
        P.append((n, m + sum(n[j] * centre[j] for j in range(3))))
    return P


# closed forms on 1 <= mu <= 2 (mahler-sweep study, 4 Nov)
Vco = R(4, 3) * mu**3 - 4 * (mu - 1)**3
Aco = 12 * (mu - 1)**2 + 4 * s3 * (mu**2 - 3 * (mu - 1)**2)

# ---------------------------------------------------------------- K1
progress(0, 'K1 cube-octahedron line, Lindelof')
for m in [R(11, 10), R(5, 4), R(3, 2), R(7, 4), R(19, 10)]:
    _, V, A, _ = measures(co_planes(m))
    check(f'K1 engine = closed form at mu = {m}', iszero(V - Vco.subs(mu, m)) and iszero(A - Aco.subs(mu, m)), f'V={V}, A={sp.nsimplify(A)}')
num = sp.factor(sp.expand(2 * sp.diff(Vco, mu) * Aco - 3 * Vco * sp.diff(Aco, mu)), extension=s3)
check('K1 d(V^2/A^3)/dmu = 0 at mu = sqrt3 (Lindelof: all faces tangent to the unit sphere)', iszero(num.subs(mu, s3)), f'2V\'A - 3VA\' = {num}')
roots = [r for r in sp.solve(sp.expand(2 * sp.diff(Vco, mu) * Aco - 3 * Vco * sp.diff(Aco, mu)), mu) if r.is_real and 1 < r < 2]
check('K1 the only stationary point in (1,2) is sqrt3', len(roots) == 1 and iszero(roots[0] - s3), roots)
check('K1 it is a maximum (sign + before, - after)', num.subs(mu, R(3, 2)) > 0 and num.subs(mu, R(19, 10)) < 0)
IQ = lambda m: (36 * sp.pi * Vco.subs(mu, m)**2 / Aco.subs(mu, m)**3)
DATA['K1'] = {'stationary_factor': str(num), 'IQ_at_sqrt3': str(sp.nsimplify(sp.radsimp(IQ(s3)))), 'IQ_at_sqrt3_num': float(IQ(s3))}

# ---------------------------------------------------------------- K2 tetrahedron line
progress(1, 'K2 self-dual tetrahedron line')
TV = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
def t_planes(m):
    P = [([-t for t in v], 1) for v in TV]          # T: facets opposite the corners, -v.x <= 1
    P += [(list(v), m) for v in TV]                 # m T*: v.x <= m
    return P
for m in [R(3, 2), R(2), R(5, 2)]:
    v1, V1, A1, _ = measures(t_planes(m))
    v2, V2, A2, _ = measures(t_planes(1 / m))
    img = sorted([tuple(-m * t for t in w) for w in v2])
    same = sorted([tuple(w) for w in v1]) == img
    check(f'K2 S({m}) = {m} * (-S(1/{m})) exactly (corner sets)', same, f'{len(v1)} corners')
    check(f'K2 IQ({m}) = IQ(1/{m})', iszero(V1**2 / A1**3 - V2**2 / A2**3))
# closed forms on [1,3): cut tetrahedra of scale (3-mu)/4
VT = R(8, 3) * (1 - 4 * ((3 - mu) / 4)**3)
AT = 4 * 2 * s3 * (1 - 3 * ((3 - mu) / 4)**2) + 4 * 2 * s3 * ((3 - mu) / 4)**2
for m in [R(3, 2), R(2), R(5, 2)]:
    _, V, A, _ = measures(t_planes(m))
    check(f'K2 closed form at mu = {m}', iszero(V - VT.subs(mu, m)) and iszero(A - AT.subs(mu, m)))
dT = sp.factor(sp.expand(2 * sp.diff(VT, mu) * AT - 3 * VT * sp.diff(AT, mu)))
sgn = [dT.subs(mu, m) for m in [R(11, 10), R(2), R(29, 10)]]
check('K2 IQ strictly decreasing on (1,3), stationary at mu = 1: with IQ(mu) = IQ(1/mu) the maximum on the whole line is mu = 1, the octahedron (smooth)',
      all(s < 0 for s in sgn) and iszero(dT.subs(mu, 1)) and not [r for r in sp.solve(dT, mu) if r.is_real and 1 < r < 3], f'2V\'A-3VA\' = {dT}')
DATA['K2'] = {'IQ_octahedron': str(sp.nsimplify(36 * sp.pi * VT.subs(mu, 1)**2 / AT.subs(mu, 1)**3))}

# ---------------------------------------------------------------- K3 CsCl pair, Kelvin
progress(2, 'K3 CsCl pair swap and Kelvin')
for m in [R(6, 5), R(3, 2), R(9, 5)]:
    _, VA, AA, _ = measures(co_planes(m))
    # B cell built from its own definition: cube round (1,1,1) cut by |x-1|+|y-1|+|z-1| <= 3 - m
    _, VB, AB, _ = measures(co_planes(3 - m, centre=(1, 1, 1)))
    check(f'K3 A cell + B cell = lattice cell (volume 8) at mu = {m}', iszero(VA + VB - 8), f'{VA} + {VB}')
    check(f'K3 B cell = A cell of 3 - mu (swap) at mu = {m}', iszero(VB - Vco.subs(mu, 3 - m)) and iszero(AB - Aco.subs(mu, 3 - m)))
W = (Aco + Aco.subs(mu, 3 - mu)) / 16
check('K3 W(mu) = W(3 - mu)', iszero(sp.expand(W - W.subs(mu, 3 - mu))))
A2 = sp.diff(Aco, mu, 2)
check('K3 A\'\' = 24 - 16 sqrt3 < 0, so W is concave on [1,2] and its maximum is the fixed point 3/2', iszero(A2 - (24 - 16 * s3)) and A2 < 0)
check('K3 W(3/2) = (3 + 6 sqrt3)/8 = 1.67404 (Kelvin), W(1) = (3 + 2 sqrt3)/4',
      iszero(W.subs(mu, R(3, 2)) - (3 + 6 * s3) / 8) and iszero(W.subs(mu, 1) - (3 + 2 * s3) / 4), float(W.subs(mu, R(3, 2))))
DATA['K3'] = {'W': str(sp.simplify(W)), 'W_kelvin': str((3 + 6 * s3) / 8)}

# ---------------------------------------------------------------- K4 Dehn on the pair
progress(3, 'K4 Dehn invariant on the pair')
def edge_lengths(m):
    P = co_planes(m)
    verts, V, A, edges = measures(P)
    L = {'hh': sp.Integer(0), 'hs': sp.Integer(0), 'ss': sp.Integer(0)}
    for (i, j), ks in edges.items():
        kinds = sorted('s' if k < 6 else 'h' for k in ks)
        d = [verts[i][t] - verts[j][t] for t in range(3)]
        L[''.join(kinds)] += sp.sqrt(sum(t * t for t in d))
    return {k: sp.radsimp(v) for k, v in L.items()}
for m in [R(6, 5), R(3, 2), R(7, 4)]:
    L = edge_lengths(m)
    check(f'K4 L_hh - L_sh/2 = 12 sqrt2 (3 - 2 mu) at mu = {m} (no square-square edges)',
          iszero(L['hh'] - L['hs'] / 2 - 12 * s2 * (3 - 2 * m)) and L['ss'] == 0, L)
cs, ss_ = -1 / s3, s2 / s3          # interior dihedral square-hexagon: cos = -1/sqrt3
ch, sh = -R(1, 3), 2 * s2 / 3      # interior dihedral hexagon-hexagon: cos = -1/3
e = sp.expand((cs + sp.I * ss_)**2 * (ch + sp.I * sh))
check('K4 2 theta_sh + theta_hh = 2 pi exactly, so theta_sh = -theta_hh/2 mod pi and D = (L_hh - L_sh/2) (x) theta_hh, zero only at mu = 3/2', iszero(e - 1), e)
check('K4 the Dehn coefficient is odd under mu -> 3 - mu: D(P_mu) + D(P_{3-mu}) = 0, so at the fixed point 2D = 0, D = 0',
      iszero((3 - 2 * mu) + (3 - 2 * (3 - mu))))

# ---------------------------------------------------------------- K5 turn law, t_min
progress(4, 'K5 turn law on the C-O line')
def tmin_closed(m):
    s = m + 3 / m
    return m if m <= R(3, 2) else (5 - s if m <= 2 else 3 / m)
for m in [R(6, 5), R(3, 2), R(8, 5), R(7, 4), R(2), R(5, 2)]:
    v1, _ = polytope(co_planes(m))
    v2, _ = polytope(co_planes(3 / m))
    t = max(sum(a[j] * b[j] for j in range(3)) for a in v1 for b in v2)
    check(f'K5 max x.y over corners of S({m}) x S({3 / m}) = closed form = closed form at the turn', iszero(t - tmin_closed(m)) and iszero(tmin_closed(m) - tmin_closed(3 / m)), t)
tm = 5 - (mu + 3 / mu)
check('K5 middle piece 5 - mu - 3/mu: turn-invariant, unique maximum at sqrt3, value 5 - 2 sqrt3',
      iszero(tm - tm.subs(mu, 3 / mu)) and sp.solve(sp.diff(tm, mu), mu) == [s3] and iszero(tm.subs(mu, s3) - (5 - 2 * s3)))

# ---------------------------------------------------------------- K6 Galois swap on the golden cuts
progress(5, 'K6 Galois swap on the ten golden cuts')
RA, RB = sp.symbols('RA RB', positive=True)      # stand for sqrt2, sqrt5 so that the swap acts on symbols
phs = (1 + RB) / 2
def val(e):
    return sp.radsimp(e.subs({RA: s2, RB: s5}))
def sigma(e):
    return e.subs({RA: -RA, RB: -RB}, simultaneous=True)
cuts = {}
for name, k in [('T', 1), ('O', 1), ('I', 1), ('C', RA), ('D', phs)]:
    cuts[name] = (phs / (k + 2 * phs), 1 / (phs * k + 2))
fixed = [(n, i) for n, (a, b) in cuts.items() for i, x in ((1, a), (2, b)) if iszero(val(sigma(x) - x))]
check('K6 exactly one golden cut is fixed by the Galois swap: the dodecahedron greater cut x1 = 1/3', fixed == [('D', 1)] and iszero(val(cuts['D'][0]) - R(1, 3)), fixed)
check('K6 the cube pair is swapped: sigma(x1) = x2', iszero(val(sigma(cuts['C'][0]) - cuts['C'][1])))
check('K6 dodecahedron lesser cut goes to (7 + sqrt5)/22 (the phi^3 cut)', iszero(val(sigma(cuts['D'][1])) - (7 + s5) / 22))
tri = [val(sigma(cuts['T'][i])) for i in (0, 1)]
check('K6 triangle-faced solids: both twins exceed 1/2 (over-cut, no solid)', all(t > R(1, 2) for t in tri), tri)
DATA['K6'] = {n: [str(val(a)), str(val(b)), str(val(sigma(a))), str(val(sigma(b)))] for n, (a, b) in cuts.items()}

# ---------------------------------------------------------------- K7 AB line
progress(6, 'K7 Ammann-Beenker line')
t = sp.symbols('t', positive=True)
f = (1 + 2 * t**2) / (4 * t)
check('K7 squares per rhombus is invariant under t -> 1/(2t)', iszero(sp.simplify(f - f.subs(t, 1 / (2 * t)))))
check('K7 least at the fixed point 1/sqrt2, value 1/sqrt2', sp.solve(sp.diff(f, t), t) == [1 / s2] and iszero(f.subs(t, 1 / s2) - 1 / s2))

# ---------------------------------------------------------------- K8 sweep reversal on events
progress(7, 'K8 reversal of corner events, Eulerian h-vectors')
def eulerian(n):
    return [sum((-1)**j * sp.binomial(n + 1, j) * (k + 1 - j)**n for j in range(k + 2)) for k in range(n)]
rows = {}
for n in range(3, 9):
    h = eulerian(n); d = n - 1
    rows[d] = [int(v) for v in h]
    check(f'K8 permutohedron of dimension {d}: h symmetric (i -> d - i), self-reverse middle class {"exists: " + str(h[d // 2]) if d % 2 == 0 else "absent"}',
          h == h[::-1] and (d % 2 == 0) == (len(h) % 2 == 1))
check('K8 d = 4 gives births, swaps, deaths 26, 66, 26 (#104, #105); d = 5 gives 57, 302, 302, 57 (no pure swap)',
      rows[4][1:4] == [26, 66, 26] and rows[5][1:5] == [57, 302, 302, 57])
DATA['K8'] = rows

# ---------------------------------------------------------------- K9 new look: tone of the golden-cut dodecahedra
progress(8, 'K9 degree-6 tone along the dodecahedron cut line')
x = sp.symbols('x')
DV = [sp.Matrix(v) for v in itertools.product((1, -1), repeat=3)]
for a, b in itertools.product((1, -1), repeat=2):
    for c in range(3):
        v = [0, 0, 0]; v[(c + 1) % 3] = a / phi; v[(c + 2) % 3] = b * phi; DV.append(sp.Matrix(v))
el = min(sp.radsimp((DV[0] - w).dot(DV[0] - w)) for w in DV[1:])
edges = [(i, j) for i in range(20) for j in range(i + 1, 20) if iszero((DV[i] - DV[j]).dot(DV[i] - DV[j]) - el)]
axes = []
for a, b in itertools.product((1, -1), repeat=2):
    for c in range(3):
        v = [0, 0, 0]; v[(c + 1) % 3] = a; v[(c + 2) % 3] = b * phi; axes.append(sp.Matrix(v))
axes = [a for k, a in enumerate(axes) if not any(iszero((a + b).dot(a + b)) for b in axes[:k])]
def H6(p):
    rr = p.dot(p); out = 0
    for a in axes:
        aa = a.dot(a); ca = p.dot(a)
        out += (231 * ca**6 / aa**3 - 315 * ca**4 * rr / aa**2 + 105 * ca**2 * rr**2 / aa - 5 * rr**3) / 16
    return out
i, j = edges[0]
p = DV[i] + x * (DV[j] - DV[i])
tone_expr = sp.expand(sp.radsimp(sp.expand(H6(p))))
fac = sp.factor_list(tone_expr, x, extension=s5)
zs = sorted([r for r in sp.Poly(tone_expr, x).nroots(n=30) if abs(sp.im(r)) < 1e-20 and 0 < sp.re(r) < 0.5], key=lambda r: sp.re(r))
x1, x2 = val(cuts['D'][0]), val(cuts['D'][1])
vals = {str(k): sp.radsimp(sp.expand(tone_expr.subs(x, v))) for k, v in [('1/3', x1), ('x2', x2), ('(7+sqrt5)/22', (7 + s5) / 22), ('1/2', R(1, 2)), ('0', 0)]}
check('K9 control: tone at x = 0 (the dodecahedron) and x = 1/2 (the icosidodecahedron) both nonzero (neither is a 6-design)',
      not iszero(vals['0']) and not iszero(vals['1/2']), {k: float(v) for k, v in vals.items()})
silent13 = iszero(vals['1/3'])
check('K9 RESULT: the Galois-fixed cut x = 1/3 is ' + ('SILENT' if silent13 else 'not silent') + ' in degree 6; zeros of the tone in (0,1/2): '
      + ', '.join(f'{float(sp.re(r)):.10f}' for r in zs), True, f'factors {fac}')
DATA['K9'] = {'tone_values': {k: str(v) for k, v in vals.items()}, 'zeros_in_(0,1/2)': [str(sp.re(r)) for r in zs], 'factors': str(fac)}

progress(9, 'done')
nfail = sum(1 for c in CHECKS if not c[1])
json.dump({'checks': [{'name': n, 'ok': o, 'detail': d} for n, o, d in CHECKS], 'data': {k: (v if isinstance(v, (dict, list)) else str(v)) for k, v in DATA.items()},
           'seconds': round(time.time() - T0, 1)}, open(sys.argv[1] if len(sys.argv) > 1 else 'data/swap-checks.json', 'w'), indent=1, default=str)
print(f'{len(CHECKS)} checks, {nfail} failed, {time.time() - T0:.1f} s')
print('FINAL ok' if nfail == 0 else 'FINAL FAIL')
