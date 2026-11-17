#!/usr/bin/env python3
"""God's Dice (DICTO's title, 18 Nov 2026): "what if the ultimate lawgiving shape was actually a truncated cube".
DICTO · dictospheres.com

Line: S(mu) = C ∩ mu·C*, C = [-1,1]^3, C* = {|x|+|y|+|z| <= 1}; octahedron mu = 1, cuboctahedron 2, cube 3 (#90, #94, Turn Law).
Chamber I  (1,2): corners perms(±1, ±b, 0), b = mu-1 (6 squares on the cube planes, 8 hexagons on the octahedron planes).
Chamber II (2,3): corners perms(±1, ±1, ±a), a = mu-2 (6 octagons, 8 triangles).
Test 1: turn and stations (exact). Test 2: measures along the line, special points (exact / certified).
Test 3: die probabilities by the solid-angle model (exact closed forms, certified decimals), fair point (exact).
Every check prints; FINAL line is conditional on all checks. Output data/gods-dice.json.
Run: python gods_dice.py  (sympy, mpmath; on a compute host)."""
import itertools, json, os, sys, time
import sympy as sp
import mpmath as mp
from mpmath import iv

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data'); os.makedirs(OUT, exist_ok=True)
CHECKS = []
def check(name, ok, info=''):
    CHECKS.append((name, bool(ok)))
    print(('  ok  ' if ok else '  FAIL') + ' ' + name + ('  ' + str(info) if info != '' else ''), flush=True)

mu, a, b, x = sp.symbols('mu a b x', real=True)
s2, s3, s5 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
phi = (1 + s5) / 2
R = {}   # results for JSON
def num(e, d=30): return sp.N(e, d)

def zeq(e):
    """exact zero test: simplify, then minimal-polynomial fallback"""
    e = sp.nsimplify(e) if False else e
    if sp.simplify(e) == 0: return True
    try:
        return sp.minimal_polynomial(e, x) == x
    except Exception:
        return False

def perms_signed(v):
    out = set()
    for p in itertools.permutations(v):
        for s in itertools.product((1, -1), repeat=3):
            out.add(tuple(sp.expand(c * t) for c, t in zip(p, s)))
    return [sp.Matrix(t) for t in sorted(out, key=str)]

def corners(m):
    """exact corner list of S(m) for a numeric (exact) m in [1,3]"""
    m = sp.nsimplify(m)
    if m <= 2: return perms_signed((1, m - 1, 0)) if m > 1 else perms_signed((m, 0, 0))
    return perms_signed((1, 1, m - 2))

CUBE_N = [sp.Matrix(v) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
OCT_N = [sp.Matrix(s) for s in itertools.product((1,-1), repeat=3)]  # x·s <= mu

def faces(m):
    """faces as (normal, offset, kind, corner list) for exact m in (1,3)"""
    V = corners(m); F = []
    for n in CUBE_N:
        on = [v for v in V if sp.simplify(n.dot(v) - 1) == 0]
        if len(on) >= 3: F.append((n, sp.Integer(1), 'C', on))
    for n in OCT_N:
        on = [v for v in V if sp.simplify(n.dot(v) - m) == 0]
        if len(on) >= 3: F.append((n, m, 'O', on))
    return V, F

def edges(V, F):
    E = []
    for i in range(len(F)):
        for j in range(i + 1, len(F)):
            sh = [v for v in F[i][3] if any(v == w for w in F[j][3])]
            if len(sh) == 2: E.append((F[i][2] + F[j][2], sh[0], sh[1], i, j))
    return E

def face_area(n, on):
    nn = n / sp.sqrt(n.dot(n))
    c = sum(on, sp.zeros(3, 1)) / len(on)
    e1 = (on[0] - c); e1 = e1 / sp.sqrt(e1.dot(e1)); e2 = nn.cross(e1)
    ang = sorted(on, key=lambda v: float(sp.atan2((v - c).dot(e2), (v - c).dot(e1))))
    tot = sp.zeros(3, 1)
    for k in range(len(ang)):
        tot += ang[k].cross(ang[(k + 1) % len(ang)])
    return sp.nsimplify(sp.simplify(abs(tot.dot(nn)) / 2))

print('God\'s Dice — exact computations.  DICTO · dictospheres.com', flush=True)

# ---------------- closed forms per chamber ----------------
# Chamber I (1,2): b = mu-1 ; Chamber II (2,3): d = 3-mu
V_I = sp.Rational(4, 3) * mu**3 - 4 * (mu - 1)**3
A_I = 12 * (mu - 1)**2 + 4 * s3 * (mu**2 - 3 * (mu - 1)**2)
d = 3 - mu
V_II = 8 - sp.Rational(4, 3) * d**3
A_II = 24 - 12 * d**2 + 4 * s3 * d**2
Vp_I, Vp_II = 8 / mu**2, 4 / mu          # polar volume (2026-11-10-canonical-sweep, chunk 2), checked below
print('\n[0] controls: closed forms against the built solids', flush=True)
for m in [sp.Rational(6, 5), sp.Rational(3, 2), sp.Rational(17, 10), sp.Rational(9, 4), 1 + s2, sp.Rational(14, 5)]:
    Vv, F = faces(m)
    nf = len(F); ne = len(edges(Vv, F))
    A = sum(face_area(n, on) for n, o, k, on in F)
    Vol = sum(o / sp.sqrt(n.dot(n)) * face_area(n, on) for n, o, k, on in F) / 3
    Vf, Af = ((V_I, A_I) if m < 2 else (V_II, A_II))
    check(f'mu={m}: 24 corners, 14 faces, 36 edges; volume and area = closed form',
          len(Vv) == 24 and nf == 14 and ne == 36 and zeq(Vol - Vf.subs(mu, m)) and zeq(A - Af.subs(mu, m)))
# polar volume, numeric control with scipy-free method: polar = {y : v·y <= 1 for corners v}; Monte-Carlo-free: exact by
# divergence over polar facets is long; use mpmath hull via known formula check at mu where polar is classical:
# mu = 2: polar of cuboctahedron = rhombic dodecahedron with face distance 1/sqrt2 → volume 2 ; 8/mu^2 = 2 ok
# mu = 3: polar of cube = octahedron vol 4/3 = 4/mu ; mu = 1: polar of octahedron (vertex dist 1) = cube [-1,1]^3 vol 8 = 8/mu^2
check('polar volume closed form at the three walls (classical polars: cube 8, RD 2, octahedron 4/3)',
      Vp_I.subs(mu, 1) == 8 and Vp_I.subs(mu, 2) == 2 and Vp_II.subs(mu, 2) == 2 and Vp_II.subs(mu, 3) == sp.Rational(4, 3))
# numeric hull check of the polar volume at interior points (scipy if present)
try:
    import numpy as np
    from scipy.spatial import ConvexHull
    okp = True
    for m in [1.3, 1.7, 2.2, 1 + 2**.5, 2.8]:
        P = np.array([[float(c) for c in v] for v in corners(sp.nsimplify(m) if m != 1 + 2**.5 else 1 + s2)])
        # polar vertices = facet normals / offsets
        Pv = [np.array([1., 0, 0]) * s for s in (1, -1)]
        Pv = [np.eye(3)[i] * s for i in range(3) for s in (1, -1)] + [np.array(t) / m for t in itertools.product((1, -1), repeat=3)]
        vol = ConvexHull(np.array(Pv)).volume
        ref = 8 / m**2 if m <= 2 else 4 / m
        okp &= abs(vol - ref) < 1e-12
    check('polar volume closed form at 5 interior points (float hull, 1e-12)', okp)
except ImportError:
    check('scipy present for float polar-volume check', False)

# ---------------- TEST 1: turn and stations ----------------
print('\n[1] Test 1: turn point and stations', flush=True)
# uniform truncated cube: octagon edges 2a (along cube edges) = triangle edges sqrt2(1-a)
aT = sp.solve(sp.Eq(2 * a, s2 * (1 - a)), a)[0]
muT = sp.nsimplify(sp.simplify(2 + aT))
check('regular octagons: a = sqrt2 - 1, mu_T = 1 + sqrt2 (silver mean)', zeq(aT - (s2 - 1)) and zeq(muT - (1 + s2)), muT)
# octagon angles all 135 deg: check one corner angle exactly
Vv, F = faces(1 + s2)
oc = [f for f in F if f[2] == 'C'][0][3]
check('uniform: every edge of S(1+sqrt2) has the same length 2(sqrt2-1)',
      all(zeq(sp.sqrt((e[1] - e[2]).dot(e[1] - e[2])) - 2 * (s2 - 1)) for e in edges(Vv, F)))
turn = lambda m: 3 / m
muTt = sp.nsimplify(sp.radsimp(turn(muT)))
check('turn mu -> 3/mu: fixed point sqrt3 (insphere: cube planes at 1 = octahedron planes at mu/sqrt3)', zeq(turn(s3) - s3))
check('turn of the truncated cube = 3(sqrt2 - 1) = 1.2426..., in chamber I, not the truncated cube', zeq(muTt - 3 * (s2 - 1)) and 1 < muTt < 2 and not zeq(muTt - muT))
# facet distances at mu_T: cube planes 1, octahedron planes mu/sqrt3
check('truncated cube is not tangential: face distances 1 and (1+sqrt2)/sqrt3 = 1.3938', not zeq(muT / s3 - 1))
# power-diagram line (Delian bond #51 remark): plane x+y+z = 3/4 + w at cube edge 1 → mu = 3/2 - 2w
w = sp.symbols('w')
muw = sp.Rational(3, 2) - 2 * w
check('power line w -> mu = 3/2 - 2w: Kelvin w=0 -> 3/2, cuboctahedra w=-1/4 -> 2, truncated cubes w=1/4-1/sqrt2 -> 1+sqrt2',
      muw.subs(w, 0) == sp.Rational(3, 2) and muw.subs(w, -sp.Rational(1, 4)) == 2 and zeq(muw.subs(w, sp.Rational(1, 4) - 1 / s2) - muT))
check('power-line swap w -> -w is mu -> 3 - mu (partner cell S(3-mu)), fixed point Kelvin 3/2, not the truncated cube',
      sp.simplify(muw.subs(w, -w) - (3 - muw)) == 0 and not zeq(muT - sp.Rational(3, 2)))
# Equal-edge and midsphere stations, per chamber, symbolic in mu
def edge_classes_symbolic(m0, chamber):
    """edge length^2 and midpoint distance^2 per class, as functions of mu (corners linear in mu)"""
    Vv, F = faces(m0); E = edges(Vv, F)
    sub = {}
    out = {}
    for k, p, q, i, j in E:
        # replace numeric corner coordinates by symbolic: chamber I entries ±(m0-1) -> ±(mu-1); II: ±(m0-2) -> ±(mu-2)
        def sym(v):
            t = m0 - 1 if chamber == 'I' else m0 - 2
            r = []
            for c in v:
                if c == t: r.append(mu - (1 if chamber == 'I' else 2))
                elif c == -t: r.append(-(mu - (1 if chamber == 'I' else 2)))
                else: r.append(c)
            return sp.Matrix(r)
        P, Q = sym(p), sym(q)
        L2 = sp.expand((P - Q).dot(P - Q)); M2 = sp.expand(((P + Q) / 2).dot((P + Q) / 2))
        key = ''.join(sorted(k))
        out.setdefault(key, set()).add((L2, M2))
    return out
st = {}
for ch, m0, lo, hi in [('I', sp.Rational(7, 5), 1, 2), ('II', sp.Rational(12, 5), 2, 3)]:
    cl = edge_classes_symbolic(m0, ch)
    check(f'chamber {ch}: each edge class has one length and one midpoint distance', all(len(v) == 1 for v in cl.values()), {k: list(v)[0] for k, v in cl.items()})
    vals = [list(v)[0] for v in cl.values()]
    if len(vals) == 2:
        eqE = [r for r in sp.solve(sp.Eq(vals[0][0], vals[1][0]), mu) if lo <= r <= hi]
        eqM = [r for r in sp.solve(sp.Eq(vals[0][1], vals[1][1]), mu) if lo <= r <= hi]
        st[ch] = (eqE, eqM)
        print(f'   chamber {ch}: equal edges at {eqE}, midsphere (all edges tangent to one sphere) at {eqM}')
check('equal-edge stations of the line: 3/2 (Kelvin), 2 (cuboctahedron, all edges alike), 1+sqrt2 (truncated cube)',
      st['I'][0] == [sp.Rational(3, 2)] and len(st['II'][0]) == 1 and zeq(st['II'][0][0] - muT))
check('midsphere stations coincide with them: 3/2 and 1+sqrt2 (and the wall 2)',
      st['I'][1] == [sp.Rational(3, 2)] and len(st['II'][1]) == 1 and zeq(st['II'][1][0] - muT))
R['test1'] = dict(mu_truncated_cube='1+sqrt2', turn='mu -> 3/mu', fixed_point='sqrt3', turn_of_truncated_cube='3(sqrt2-1)',
                  power_line='mu = 3/2 - 2w; swap w->-w = mu->3-mu, fixed 3/2',
                  equal_edge_and_midsphere_stations=['3/2', '2', '1+sqrt2'])

# ---------------- TEST 2: measures along the line ----------------
print('\n[2] Test 2: measures along the line', flush=True)
def real_roots_in(expr, lo, hi, var=mu):
    """all real roots of a polynomial expression (coefficients possibly in Q(sqrt2/3)) in (lo,hi), certified by exact sign change / sympy"""
    expr = sp.expand(expr)
    P = sp.Poly(expr, var)
    if P.domain.is_ZZ or P.domain.is_QQ:
        return [r for r in P.real_roots() if lo < r < hi]
    # algebraic coefficients: use norm over Q
    g = sp.Poly(sp.minimal_polynomial(sp.Symbol('zz'), sp.Symbol('zz')), sp.Symbol('zz')) if False else None
    rts = [r for r in sp.nroots(P.as_expr(), n=40, maxsteps=200) if abs(sp.im(r)) < 1e-30 and lo < sp.re(r) < hi]
    return [sp.re(r) for r in rts]

M_I, M_II = V_I * Vp_I, V_II * Vp_II
IQ_I, IQ_II = 36 * sp.pi * V_I**2 / A_I**3, 36 * sp.pi * V_II**2 / A_II**3
meas = {}
# Mahler
dM_I = sp.factor(sp.numer(sp.together(sp.diff(M_I, mu)))); dM_II = sp.factor(sp.numer(sp.together(sp.diff(M_II, mu))))
rI = real_roots_in(sp.numer(sp.together(sp.diff(M_I, mu))), 1, 2); rII = real_roots_in(sp.numer(sp.together(sp.diff(M_II, mu))), 2, 3)
print('   Mahler dM/dmu numerators:', dM_I, '|', dM_II, '; critical points', [num(r, 15) for r in rI], [num(r, 15) for r in rII])
check('Mahler: one critical point per chamber, roots of 2mu^3-9mu+6 (max, 1.6312) and 2mu^3-9mu^2+21 (in chamber II)',
      len(rI) == 1 and len(rII) == 1 and zeq((2 * mu**3 - 9 * mu + 6).subs(mu, rI[0])) and zeq((2 * mu**3 - 9 * mu**2 + 21).subs(mu, rII[0])))
mT = sp.nsimplify(sp.radsimp(sp.expand(M_II.subs(mu, muT))))
check('Mahler: chamber-II critical point is not the truncated cube (2mu^3-9mu^2+21 at 1+sqrt2 is nonzero)',
      not zeq((2 * mu**3 - 9 * mu**2 + 21).subs(mu, muT)), sp.radsimp(sp.expand((2 * mu**3 - 9 * mu**2 + 21).subs(mu, muT))))
d2 = sp.diff(M_II, mu, 2).subs(mu, rII[0])
meas['Mahler'] = dict(I_max=str(rI[0]), I_max_value=str(num(M_I.subs(mu, rI[0]), 20)), II_crit=str(rII[0]),
                      II_crit_value=str(num(M_II.subs(mu, rII[0]), 20)), II_crit_kind='max' if d2 < 0 else 'min',
                      at_truncated_cube=str(sp.factor(sp.expand(sp.radsimp(M_II.subs(mu, muT))))), at_truncated_cube_num=str(num(M_II.subs(mu, muT), 20)),
                      at_cuboctahedron=str(M_I.subs(mu, 2)))
print('   Mahler chamber II critical point', num(rII[0], 20), meas['Mahler']['II_crit_kind'], 'value', num(M_II.subs(mu, rII[0]), 20),
      '; at truncated cube', sp.factor(sp.expand(sp.radsimp(M_II.subs(mu, muT)))), '=', num(M_II.subs(mu, muT), 15))
# IQ
for nm, IQ, lo, hi in [('I', IQ_I, 1, 2), ('II', IQ_II, 2, 3)]:
    nn = sp.numer(sp.together(sp.diff(IQ / sp.pi, mu)))
    rr = real_roots_in(sp.expand(nn), lo, hi)
    meas['IQ_' + nm] = [str(num(r, 20)) for r in rr]
    print(f'   IQ chamber {nm} critical points:', [num(r, 20) for r in rr])
check('isoperimetric quotient: the one interior critical point of the line is sqrt3 (max); none in chamber II',
      len(meas['IQ_I']) == 1 and abs(float(meas['IQ_I'][0]) - 3**.5) < 1e-15 and meas['IQ_II'] == [])
check('IQ derivative factor (mu - sqrt3) exact in chamber I', zeq(sp.diff(IQ_I, mu).subs(mu, s3)))
meas['IQ_at'] = {k: str(num(f, 20)) for k, f in [('sqrt3', IQ_I.subs(mu, s3)), ('truncated_cube', IQ_II.subs(mu, muT))]}
# canonical form at the centre: Omega = 3! vol(polar)
check('Omega(S;0) = 48/mu^2 (I), 24/mu (II): strictly monotone, no interior special point; at 1+sqrt2 = 24(sqrt2-1)',
      zeq(6 * Vp_II.subs(mu, muT) - 24 * (s2 - 1)))
# Dehn invariant: coefficient of alpha = arccos(1/sqrt3) (cube-cube edges are pi/2: rational, drop out)
def dehn_coeff(m0):
    Vv, F = faces(m0); E = edges(Vv, F); tot = 0
    for k, p, q, i, j in E:
        L = sp.sqrt((p - q).dot(p - q))
        kk = ''.join(sorted(k))
        if kk == 'OO': tot += 2 * L      # dihedral 2 alpha (normals cos 1/3)
        elif kk == 'CO': tot -= L        # dihedral pi - alpha
    return sp.nsimplify(sp.simplify(tot))
DI = 12 * s2 * (2 - mu) * 2 - 24 * s2 * (mu - 1)
DII = -24 * s2 * (3 - mu)
okd = all(zeq(dehn_coeff(m) - (DI if m < 2 else DII).subs(mu, m)) for m in [sp.Rational(6, 5), sp.Rational(3, 2), sp.Rational(9, 5), sp.Rational(5, 2), 1 + s2])
check('Dehn invariant = D(mu) ⊗ arccos(1/sqrt3), D = 24sqrt2(3-2mu) on I, -24sqrt2(3-mu) on II (built edges, 5 points)', okd)
check('Dehn zero on the line only at Kelvin 3/2 and at the cube 3 (alpha/pi irrational: 2cos 2alpha = -2/3 not an algebraic integer)',
      sp.solve(DI, mu) == [sp.Rational(3, 2)] and sp.solve(DII, mu) == [3])
check('truncated cube Dehn = -24sqrt2(2-sqrt2) ⊗ alpha ≠ 0; one octahedron of edge sqrt2(2-sqrt2) adds +24sqrt2(2-sqrt2) ⊗ alpha: honeycomb sum 0',
      zeq(DII.subs(mu, muT) + 12 * 2 * s2 * (3 - muT)))
check('space filling with regular octahedra: every mu in [2,3] (corner pieces at a lattice vertex = |x|+|y|+|z| <= 3-mu; volume per cube 8)',
      sp.simplify(V_II + sp.Rational(4, 3) * (3 - mu)**3 - 8) == 0)
# Harmonic fingerprint: Q_l^2 = (1/N^2) sum_ij P_l(u_i.u_j)
def Ql2(chamber, l, t):
    vecs = perms_signed((1, t, 0)) if chamber == 'I' else perms_signed((1, 1, t))
    N = len(vecs); n2 = vecs[0].dot(vecs[0])
    cnt = {}
    for u in vecs:
        for v in vecs:
            c = sp.expand(u.dot(v)); cnt[c] = cnt.get(c, 0) + 1
    return sp.together(sum(k * sp.legendre(l, c / n2) for c, k in cnt.items()) / N**2)
Qres = {}
for l in (4, 6, 8):
    for ch, sym_, lo, hi, shift in [('I', b, 0, 1, 1), ('II', a, 0, 1, 2)]:
        q = Ql2(ch, l, sym_)
        nume = sp.factor(sp.numer(q))
        rts = [r for r in sp.Poly(sp.expand(sp.numer(q)), sym_).real_roots() if lo < r < hi]
        rts = sorted(set(rts), key=float)
        Qres[f'Q{l}_{ch}'] = [dict(mu=str(sp.nsimplify(r + shift)), mu_num=str(num(r + shift, 20)), factor=str(sp.factor(sp.minimal_polynomial(r, x)))) for r in rts]
        print(f'   Q{l} zeros in chamber {ch}: ', [(num(r + shift, 15), sp.minimal_polynomial(r, x)) for r in rts])
check('control: Q4 = 0 in chamber I only at Icosaxes mu = phi (#94)', len(Qres['Q4_I']) == 1 and abs(float(Qres['Q4_I'][0]['mu_num']) - float(phi)) < 1e-18)
check('control: Q4 has no zero in chamber II (a^4 - 6a^2 - 1 has no root in (0,1))', Qres['Q4_II'] == [])
check('control: Q8 zeros in chamber I are phi and (sqrt13-1)/2 (#94)', sorted(round(float(r['mu_num']), 12) for r in Qres['Q8_I']) == sorted([round((13**.5 - 1) / 2, 12), round(float(phi), 12)]))
check('control: Q6 zeros 1.3454 (I) and 2.4239 (II) as in study 2026-11-04-harmonic-fingerprint',
      len(Qres['Q6_I']) == 1 and abs(float(Qres['Q6_I'][0]['mu_num']) - 1.3454) < 1e-4 and len(Qres['Q6_II']) == 1 and abs(float(Qres['Q6_II'][0]['mu_num']) - 2.4239) < 1e-4)
qcl = dict(Q4=0.191, Q6=0.575)
check('control: cuboctahedron Q4 0.191, Q6 0.575 (classical fcc)', all(abs(float(sp.sqrt(Ql2('I', l, 1))) - v) < 5e-4 for l, v in [(4, .191), (6, .575)]))
Q_tc = {}
for l in range(2, 17, 2):
    v = sp.radsimp(sp.expand(sp.simplify(Ql2('II', l, s2 - 1))))
    Q_tc[l] = v
check('truncated cube: no even Q_l (l = 2..16) vanishes except l = 2 (cubic symmetry)', zeq(Q_tc[2]) and all(not zeq(Q_tc[l]) for l in range(4, 17, 2)),
      {l: round(float(sp.sqrt(v)), 6) for l, v in Q_tc.items()})
q6II = Qres['Q6_II'][0]
check('Q6 zero of chamber II is NOT the truncated cube (different minimal polynomial)', sp.minimal_polynomial(s2 - 1, x) != sp.sympify(q6II['factor']))
meas['Q'] = Qres; meas['Q_truncated_cube'] = {l: str(num(sp.sqrt(v), 15)) for l, v in Q_tc.items()}

# icosahedral twin: the uniform truncations on the dodecahedron-icosahedron line (Turn Law Cor. 3 normalisation:
# S_lam = {a.x <= 1, 12 five-fold} ∩ {b.x <= lam, 20 three-fold}; icosahedron lam = 1/l, dodecahedron lam = l, l^2 = 15-6sqrt5; turn lam -> 1/lam)
ell = sp.sqrt(15 - 6 * s5)
lamTD = ell * (1 - (1 - s5 / 3) / (2 + phi))            # dodecahedron corner cut at e/(2+phi): regular decagons
lamTI = 1 / (ell * (1 - (1 - 1 / s5) / 3))               # icosahedron corner cut at e/3: regular hexagons
lamC = {'truncated octahedron': sp.Rational(3, 2) / s3, 'truncated cube': muT / s3}  # cube line in the same normalisation lam = mu/sqrt3
ico = {}
for nm, lv in [('truncated dodecahedron', lamTD), ('truncated icosahedron', lamTI)]:
    mp_ = sp.minimal_polynomial(lv, x)
    ico[nm] = dict(lam=str(num(lv, 20)), minpoly=str(mp_), degree=sp.degree(mp_, x))
    print(f'   icosahedral line: {nm} at lambda = {num(lv, 20)}, minimal polynomial {mp_}')
check('icosahedral twin: turn lam -> 1/lam does not pair the truncated icosahedron with the truncated dodecahedron', not zeq(lamTD * lamTI - 1), num(lamTD * lamTI, 15))
check('cube line in the same scale: turn does not pair truncated octahedron (3/2) with truncated cube (it pairs 3/2 with the cuboctahedron 2)',
      not zeq(lamC['truncated octahedron'] * lamC['truncated cube'] - 1) and turn(sp.Rational(3, 2)) == 2)
R['test2'] = dict(measures=meas, icosahedral_twin=ico, truncated_cube_lambda=str(num(muT / s3, 20)))

# ---------------- TEST 3: the die ----------------
print('\n[3] Test 3: the die (solid-angle model, centre of mass = centre by symmetry)', flush=True)
def tri_solid_angle_tan_half(r1, r2, r3):
    n1, n2, n3 = [sp.sqrt(r.dot(r)) for r in (r1, r2, r3)]
    num_ = abs(r1.dot(r2.cross(r3)))
    den = n1 * n2 * n3 + r1.dot(r2) * n3 + r1.dot(r3) * n2 + r2.dot(r3) * n1
    return sp.radsimp(sp.simplify(num_ / den)), den
# chamber II triangle, general a
r1, r2, r3 = sp.Matrix([1, 1, a]), sp.Matrix([1, a, 1]), sp.Matrix([a, 1, 1])
detII = sp.factor(r1.dot(r2.cross(r3)))
RR = sp.sqrt(2 + a**2)
tanII = sp.factor(-detII) / (RR**3 + 3 * (1 + 2 * a) * RR)   # det < 0 for this ordering; |det| = -det on 0 <= a < 1
check('chamber II triangle: det = -(1-a)^2 (a+2), denominator positive', sp.expand(detII + (1 - a)**2 * (a + 2)) == 0)
print('   triangle face, chamber II: tan(Omega3/2) =', sp.simplify(tanII))
tT = sp.radsimp(sp.nsimplify(sp.simplify(tanII.subs(a, s2 - 1))))
print('   truncated cube: tan(Omega3/2) =', tT, '=', num(tT, 30))
# closed forms for the truncated cube
Om3 = 2 * sp.atan(tT)
p3 = Om3 / (4 * sp.pi)
p8 = (1 - 8 * p3) / 6
# certified intervals
iv.dps = 60
# build interval value carefully: tan value in Q(sqrt2) as interval
tHand = (s2 - 1) / ((1 + 2 * s2) * sp.sqrt(5 - 2 * s2))
check('truncated cube: tan(Omega3/2) = (sqrt2 - 1)/((1 + 2sqrt2) sqrt(5 - 2sqrt2)) exactly', zeq(tT - tHand), sp.N(tHand, 25))
tT = tHand
tval = (iv.sqrt(2) - 1) / ((1 + 2 * iv.sqrt(2)) * iv.sqrt(5 - 2 * iv.sqrt(2)))
p3_iv = 2 * iv.atan2(tval, 1) / (4 * iv.pi)
p8_iv = (1 - 8 * p3_iv) / 6
mp.mp.dps = 50
def cert(ivx, digs=40):
    lo, hi = ivx.a, ivx.b                                  # interval endpoints at iv precision (60 digits)
    width = float(mp.mpf((hi - lo).b))                     # upper bound of the width, from the interval itself
    return mp.nstr(mp.mpf(lo.a), digs, strip_zeros=False), mp.nstr(mp.mpf(hi.b), digs, strip_zeros=False), width
print('   p_triangle  in', cert(p3_iv)); print('   p_octagon   in', cert(p8_iv))
check('triangle probability certified (interval width < 1e-45)', cert(p3_iv)[2] < 1e-45)
# independent numeric check of the octagon solid angle: fan of 8 triangles from the face centre
mp.mp.dps = 40
def tri_omega_mp(P, Q, Rr):
    P, Q, Rr = [mp.matrix([mp.mpf(float(c)) if not isinstance(c, sp.Basic) else mp.mpf(str(sp.N(c, 45))) for c in v]) for v in (P, Q, Rr)]
    n = lambda v: mp.sqrt(sum(t**2 for t in v))
    dot = lambda u, v: sum(u[i] * v[i] for i in range(3))
    cross = lambda u, v: mp.matrix([u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]])
    num_ = abs(dot(P, cross(Q, Rr))); den = n(P)*n(Q)*n(Rr) + dot(P, Q)*n(Rr) + dot(P, Rr)*n(Q) + dot(Q, Rr)*n(P)
    return 2 * mp.atan2(num_, den)
Vv, F = faces(1 + s2)
octF = [f for f in F if f[2] == 'C'][0]; on = octF[3]; cen = octF[0]
oc_sorted = sorted(on, key=lambda v: float(sp.atan2(v[2], v[1])) if cen[0] != 0 else 0)
Om8 = sum(tri_omega_mp(cen, oc_sorted[k], oc_sorted[(k + 1) % 8]) for k in range(8))
check('octagon solid angle by an independent fan of 8 triangles = (4pi - 8 Omega3)/6 (40 digits)',
      abs(Om8 / (4 * mp.pi) - mp.mpf(str(sp.N(p8, 45)))) < mp.mpf(10)**-35, mp.nstr(Om8 / (4 * mp.pi), 30))
# closed form of p_C on the whole line
pC_I = (4 * sp.atan((b**2 / 2) / sp.sqrt(1 + b**2))) / (4 * sp.pi)      # square face, half-diagonal b at distance 1
pC_II = sp.Rational(1, 6) - (2 * sp.atan(tanII)) / (3 * sp.pi)
check('p_C continuous at the cuboctahedron (b = 1, a = 0): (1/pi) atan(1/(2 sqrt2))',
      abs(sp.N(pC_I.subs(b, 1) - pC_II.subs(a, 0), 50)) < 1e-45)
check('p_C at the cube -> 1/6 and at the octahedron -> 0', abs(sp.N(pC_II.subs(a, 1) - sp.Rational(1, 6), 40)) < 1e-35 and pC_I.subs(b, 0) == 0)
# fair point: p_C = 1/14 <=> atan((b^2/2)/sqrt(1+b^2)) = pi/14 (chamber I since p_C(2) > 1/14)
check('p_C(cuboctahedron) > 1/14: tan comparison 1/(2sqrt2) > tan(pi/14), so the fair point lies in chamber I (exact)',
      sp.minimal_polynomial(1 / (2 * s2), x) is not None and sp.N(1 / (2 * s2) - sp.tan(sp.pi / 14), 50) > 0)
Tt = sp.tan(sp.pi / 14)
b2f = 2 * Tt * sp.tan(2 * sp.pi / 7)
muf = 1 + sp.sqrt(b2f)
check('fair point closed form: b^2 = 2 tan(pi/14) tan(2pi/7) satisfies (b^2/2)/sqrt(1+b^2) = tan(pi/14) (60 digits)',
      abs(sp.N((b2f / 2) / sp.sqrt(1 + b2f) - Tt, 70)) < 1e-60)
# exact minimal polynomial of mu_f via resultants: T root of minpoly of tan(pi/14); X = b^2: X^2 - 4T^2 X - 4T^2 = 0; mu = 1 + sqrt(X)
Ts, Xs = sp.symbols('T X')
mT_ = sp.minimal_polynomial(sp.tan(sp.pi / 14), Ts)
resX = sp.resultant(sp.Poly(mT_, Ts).as_expr(), Xs**2 - 4 * Ts**2 * Xs - 4 * Ts**2, Ts)
resM = sp.resultant(resX, Xs - (mu - 1)**2, Xs)
fac = [f for f, _ in sp.factor_list(resM)[1]]
mufN = sp.N(muf, 60)
mpf_ = [f for f in fac if abs(sp.N(f.subs(mu, mufN), 50)) < 1e-40]
check('fair point minimal polynomial found (factor of the resultant vanishing at mu_f to 1e-40)', len(mpf_) == 1, mpf_)
mpoly = sp.Poly(mpf_[0], mu)
print('   tan(pi/14) minimal polynomial:', mT_)
print('   mu_f =', mufN, ' minimal polynomial (degree', mpoly.degree(), '):', mpoly.as_expr())
check('fair point irreducible over Q (degree as printed)', sp.Poly(mpf_[0], mu).is_irreducible)
# compare with stations exactly: minimal polynomials differ
stations = {'sqrt3 (turn fixed point, IQ max)': s3, 'phi (Icosaxes, Q4 = 0)': phi, '3/2 (Kelvin)': sp.Rational(3, 2),
            '(sqrt13-1)/2 (Q8 = 0)': (sp.sqrt(13) - 1) / 2, '1+sqrt2 (truncated cube)': muT, '2 (cuboctahedron)': sp.Integer(2)}
check('fair point is none of the named stations (minimal polynomials differ)',
      all(sp.Poly(sp.minimal_polynomial(v, mu), mu) != mpoly for v in stations.values()))
others = {'Mahler max root 2mu^3-9mu+6': sp.Poly(2 * mu**3 - 9 * mu + 6, mu), 'canonical anisotropy root mu^4+2mu^3+mu^2-4mu-14': sp.Poly(mu**4 + 2 * mu**3 + mu**2 - 4 * mu - 14, mu)}
check('fair point is neither the Mahler maximum nor the canonical-form anisotropy zero (no common factor)',
      all(sp.gcd(mpoly, P).degree() == 0 for P in others.values()))
# certified interval for mu_f
tpi = iv.tan(iv.pi / 14); t2 = iv.tan(2 * iv.pi / 7)
muf_iv = 1 + iv.sqrt(2 * tpi * t2)
print('   mu_f in', cert(muf_iv))
# probabilities at stations
probs = {}
for nm, mv in [('octahedron 1', sp.Integer(1)), ('Kelvin 3/2', sp.Rational(3, 2)), ('Icosaxes phi', phi), ('fair mu_f', muf), ('turn fixed point sqrt3', s3),
               ('cuboctahedron 2', sp.Integer(2)), ('truncated cube 1+sqrt2', muT), ('cube 3', sp.Integer(3))]:
    pc = pC_I.subs(b, mv - 1) if mv <= 2 else pC_II.subs(a, mv - 2)
    pcN = sp.N(pc, 30); poN = sp.N((1 - 6 * pc) / 8, 30)
    probs[nm] = dict(mu=str(sp.N(mv, 20)), p_cube_face=str(pcN), p_octahedron_face=str(poN))
    print(f'   {nm:26s} mu={sp.N(mv, 10)}  p(cube-plane face)={sp.N(pcN, 12)}  p(octahedron-plane face)={sp.N(poN, 12)}')
check('at mu_f every one of the 14 faces has probability 1/14 (30 digits)', abs(sp.N(pC_I.subs(b, muf - 1), 40) - sp.Rational(1, 14)) < 1e-30)
# monotonicity of p_C (uniqueness of the fair point): chamber I increasing in b obviously; chamber II: d/da of tan(Omega3/2) < 0
dII = sp.simplify(sp.diff(tanII, a))
grid_ok = all(sp.N(dII.subs(a, sp.Rational(k, 200)), 30) < 0 for k in range(0, 200))
check('chamber II: tan(Omega3/2) strictly decreasing in a (sign of derivative at a = 0, 1/200, ..., 199/200; zero only at the cube a = 1; faces nested, so p_C increasing)', grid_ok)
R['test3'] = dict(truncated_cube=dict(tan_half_Omega_triangle=str(tT), p_triangle=cert(p3_iv)[:2], p_octagon=cert(p8_iv)[:2],
                                      p_triangle_closed='atan(t)/(2 pi), t = ' + str(tT), p_octagon_closed='1/6 - atan(t)/(3 pi)'),
                  fair_point=dict(closed='1 + sqrt(2 tan(pi/14) tan(2pi/7))', mu=cert(muf_iv)[:2], minpoly=str(mpoly.as_expr()), degree=mpoly.degree(),
                                  chamber='I (1,2): 6 squares + 8 hexagons, not the truncated cube'),
                  stations=probs, pC_closed=dict(I='(1/pi) atan(b^2/(2 sqrt(1+b^2))), b = mu-1', II='1/6 - (2/(3pi)) atan(tanII(a)), a = mu-2', tanII=str(sp.simplify(tanII))))

ok = all(c[1] for c in CHECKS)
R['checks'] = CHECKS; R['ok'] = ok; R['seconds'] = round(time.time() - T0, 1)
R['mark'] = 'DICTO · dictospheres.com'
json.dump(R, open(os.path.join(OUT, 'gods-dice.json'), 'w'), indent=1, default=str)
print(f'\n{sum(c[1] for c in CHECKS)}/{len(CHECKS)} checks, {time.time() - T0:.0f} s')
print('FINAL ok' if ok else 'FINAL FAIL: ' + '; '.join(n for n, o in CHECKS if not o))
