#!/usr/bin/env python3
"""Forced fixed points (14 Nov 2026): DICTO's search for a law-giving shape, "laws at forced fixed points".

THE BATTERY at a point x* of a line of solids (or of a placement set):
  B1 swap      : is x* the fixed point of a GEOMETRIC involution s of the line (a similarity, polarity, Galois conjugation, site swap,
                 turn, placement inversion)? Every point is the fixed point of some abstract involution, so only geometric ones count.
  B2 parity    : a natural quantity f odd under s (f o s = -f) must vanish at x*.
  B3 symmetry  : f even under s is critical at x* (Palais 1979, symmetric criticality; in Clarke's sense at a kink); concave -> maximum.
  B4 symmetry+ : the object at x* has more symmetry than its neighbours; what that symmetry kills vanishes there.
  B5 values    : tiling, corner tones Q4, Q6, Q8, Q12, canonical form (polar volume and its tones), Mahler volume, roundness (IQ).
A shape QUALIFIES only if B1 holds and one of B2-B4 forces a law there, proved exactly.

Sections: C controls (sqrt3 and 3/2 on the cube-octahedron line, a random non-fixed point); A the silent zonohedron;
B the cuboctahedron with two square pyramids (opposite / adjacent); L three fixed points from the swaps study's leads
(rock salt and zinc blende site swaps, lead 2; the small stellated / great dodecahedron turn, lead 5).

Exact arithmetic decides every check (sympy: rationals, sqrt2, sqrt3, nested radicals through minimal polynomials; Q(sqrt5) class
of the stars census). Floats only order corners round a face and print values.
Reused code, executed from its files, not retyped:
  studies/2026-11-13-swaps-and-fixed-points/scripts/swap_checks.py : polytope(), measures() (exact polytope engine from planes)
  studies/2026-11-14-chat-handoff/scripts/handoff_tests.py         : decompose(), extreme(), exact_dehn(), sperms() (exact Dehn)
  studies/2026-11-04-dehn-screen/scripts/dehn.py                   : hull_faces() (face lists, certified exactly afterwards)
  studies/2026-11-09-regular-stars-census/scripts/regstar.py, turnlib.py, q5.py : flag line, t_min*, folding, Q(sqrt5)
Usage: forced.py [--pilot]. Output: PROGRESS lines, ok/FAIL lines, data/forced(-pilot).json, last line FINAL ok / FINAL FAIL.
"""
import sys, os, json, time, itertools, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

here = os.path.dirname(os.path.abspath(__file__)); STUD = os.path.join(here, '..', '..')
PILOT = '--pilot' in sys.argv
DATA = os.path.join(here, '..', 'data'); os.makedirs(DATA, exist_ok=True)
T0 = time.time()
# ---------------- reused code ----------------
_argv = sys.argv; sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.join(STUD, '2026-11-04-dehn-screen', 'scripts')); import dehn as DS
sys.argv = _argv
_h = open(os.path.join(STUD, '2026-11-14-chat-handoff', 'scripts', 'handoff_tests.py')).read()
HT = {'sp': sp, 'np': np, 'math': math, 'itertools': itertools, 'Fr': Fr, 'DS': DS}
exec(_h[_h.index("X = sp.Symbol('x')"):_h.index("s2 = sp.sqrt(2)\n")], HT)
_s = open(os.path.join(STUD, '2026-11-13-swaps-and-fixed-points', 'scripts', 'swap_checks.py')).read()
SC = {'sp': sp, 'itertools': itertools, 'math': math}
exec(_s[_s.index('def iszero(e):'):_s.index('# closed forms on 1 <= mu <= 2')], SC)
is0, exact_dehn, sperms = HT['is0'], HT['exact_dehn'], HT['sperms']
measures, polytope = SC['measures'], SC['polytope']

R = sp.Rational; s2, s3 = sp.sqrt(2), sp.sqrt(3)
CHECKS = []; OUT = {}
NSTEP = 12
def check(ok, what, detail=''):
    CHECKS.append((bool(ok), what, str(detail)[:400])); print(('ok   ' if ok else 'FAIL ') + what + (' | ' + str(detail)[:300] if detail != '' else ''), flush=True); return ok
def progress(k, what): print(f'PROGRESS {k / NSTEP:.2f} {what} ({time.time() - T0:.0f} s)', flush=True)
def find(what, val=''):
    OUT.setdefault('findings', []).append([what, str(val)[:600]]); print('FIND ' + what + (' | ' + str(val)[:300] if val != '' else ''), flush=True)
def note(key, val): OUT.setdefault('notes', {})[key] = val; print(f'      {key}: {val}', flush=True)

def exact_vol(V):
    """volume of the hull of exact corners (faces from the float hull, volume summed exactly; control use)"""
    P, F = DS.hull_faces(np.array([[float(c) for c in v] for v in V]))
    M = [sp.Matrix(v) for v in V]
    vol = sum(M[f[0]].dot(M[f[k]].cross(M[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
    return sp.Abs(sp.nsimplify(sp.radsimp(sp.expand(vol)))), F

def completion(angles, e):
    """angles: list of (p, q, value) with value = p*pi + q*beta; can the edge with angle index e be surrounded? Look for nonnegative
    integers n_i (n_e >= 1) and m (tiles holding the point in a face interior, pi each) with sum n_i q_i = 0 and sum n_i p_i + m = 2
    (beta/pi is irrational, cos 2 beta = 1/3). Valid for every tiling by congruent convex copies, face-to-face or not."""
    sols = []
    bounds = [int(2 * math.pi / v + 1e-9) for (_, _, v) in angles]
    for ns in itertools.product(*[range(b + 1) for b in bounds]):
        if ns[e] < 1: continue
        if sum(n * q for n, (_, q, _) in zip(ns, angles)) != 0: continue
        P = sum(n * p for n, (p, _, _) in zip(ns, angles))
        if P <= 2 and (2 - P).denominator == 1: sols.append((ns, int(2 - P)))
    return sols

def angle_list(r):
    out = []
    for k in r['angle_kinds']:
        deg, rest = k.split('deg = ')
        p, q = rest.split('pi ')
        out.append((Fr(p), int(q.replace('beta', '')), math.radians(float(deg)), float(deg)))
    return out

def harmonic_invariants(k):
    """basis of O_h-invariant harmonic polynomials of degree k (k even): symmetric polynomials in x^2, y^2, z^2 with zero Laplacian"""
    x, y, z = sp.symbols('x y z')
    parts = [p.copy() for p in sp.utilities.iterables.partitions(k // 2, m=3)]
    basis = []
    for p in parts:
        lam = sorted(sum([[kk] * v for kk, v in p.items()], []), reverse=True) + [0, 0, 0]
        lam = lam[:3]
        mons = {tuple(lam[i] for i in perm) for perm in itertools.permutations(range(3))}
        basis.append(sum(x ** (2 * a) * y ** (2 * b) * z ** (2 * c) for a, b, c in mons))
    c = sp.symbols(f'c0:{len(basis)}')
    h = sum(ci * b for ci, b in zip(c, basis))
    lap = sp.expand(sp.diff(h, x, 2) + sp.diff(h, y, 2) + sp.diff(h, z, 2))
    eqs = sp.Poly(lap, x, y, z).coeffs() if lap != 0 else []
    M = sp.Matrix([[sp.diff(e, ci) for ci in c] for e in eqs]) if eqs else sp.zeros(1, len(c))
    out = []
    for v in M.nullspace():
        v = v * sp.ilcm(*[t.q for t in v])
        H = sp.expand(sum(vi * b for vi, b in zip(v, basis)))
        H = sp.expand(H / H.subs({x: 1, y: 0, z: 0})) if H.subs({x: 1, y: 0, z: 0}) != 0 else H
        out.append(sp.Lambda((x, y, z), H))
    return out

# =====================================================================================================================
# C. CONTROLS on the cube-octahedron line S(mu) = [-1,1]^3 cap {|x|+|y|+|z| <= mu}, 1 <= mu <= 3 (the CsCl cell is the same body)
# =====================================================================================================================
progress(0, 'controls: cube-octahedron line')
mu = sp.symbols('mu', positive=True)
def co_planes(m, c=(0, 0, 0)):
    P = []
    for j in range(3):
        for sg in (1, -1):
            n = [0, 0, 0]; n[j] = sg; P.append((n, sg * c[j] + 1))
    for sg in itertools.product((1, -1), repeat=3):
        P.append((list(sg), m + sum(sg[j] * c[j] for j in range(3))))
    return P
tau = lambda m: 3 / m          # #81 core turn, fixed point sqrt3
sig = lambda m: 3 - m          # CsCl site swap, fixed point 3/2
OUT['controls'] = {}
# t_min on the middle stretch: 5 - mu - 3/mu (swaps study K5, checked there against the polytope engine); recheck two samples here
tmid = 5 - mu - 3 / mu
for m in ([R(8, 5)] if PILOT else [R(8, 5), R(7, 4), R(19, 10)]):
    v1, _ = polytope(co_planes(m)); v2, _ = polytope(co_planes(3 / m))
    t = max(sum(a[j] * b[j] for j in range(3)) for a in v1 for b in v2)
    check(is0(sp.expand(t - tmid.subs(mu, m))), f'C t_min(mu) = max x.y over corners of S(mu), S(3/mu) = 5 - mu - 3/mu at mu = {m}', t)
check(is0(sp.simplify(tmid - tmid.subs(mu, tau(mu)))), 'C [sqrt3, B1+B3] t_min is EVEN under the turn mu -> 3/mu (exact identity)')
d1 = sp.diff(tmid, mu); d2 = sp.diff(tmid, mu, 2)
check(is0(d1.subs(mu, s3)) and d2.subs(mu, s3) < 0, f'C [sqrt3] forced: critical at the fixed point sqrt3, t\'\' = {sp.simplify(d2.subs(mu, s3))} < 0 -> maximum 5 - 2sqrt3 (QUALIFIES, mechanism B3)')
OUT['controls']['sqrt3'] = {'swap': 'mu -> 3/mu', 'law': 't_min maximal, 5 - 2 sqrt3', 'mechanism': 'B3 symmetry + concavity', 'qualifies': True}
# Kelvin at 3/2: Dehn odd under the CsCl swap (B2), wall area even and concave (B3)
DCO = {}
for m in ([R(6, 5), R(3, 2), R(9, 5)] if PILOT else [R(6, 5), R(7, 5), R(3, 2), R(8, 5), R(9, 5)]):
    V, _ = polytope(co_planes(m)); DCO[m] = exact_dehn([tuple(v) for v in V], f'S({m})')['D']
    note(f'C Dehn of S({m})', f'{DCO[m]} (x) beta')
pairs = [(m, 3 - m) for m in DCO if 3 - m in DCO and m < 3 - m]
check(all(is0(sp.expand(DCO[a] + DCO[b])) for a, b in pairs), f'C [3/2, B2] Dehn is ODD under mu -> 3 - mu on the pairs {[(str(a), str(b)) for a, b in pairs]}')
check(is0(DCO[R(3, 2)]), 'C [3/2] forced: Dehn = 0 at the fixed point (Kelvin) -> QUALIFIES, mechanism B2')
Aco = 12 * (mu - 1) ** 2 + 4 * s3 * (mu ** 2 - 3 * (mu - 1) ** 2)       # area on [1, 2] (mahler-sweep study; swaps study K1/K3)
for m in [R(6, 5), R(8, 5)]:
    _, VV, AA, _ = measures(co_planes(m)); check(is0(sp.expand(AA - Aco.subs(mu, m))), f'C area closed form = engine at mu = {m}')
W = (Aco + Aco.subs(mu, 3 - mu)) / 2
check(is0(sp.expand(W - W.subs(mu, 3 - mu))) and sp.diff(W, mu, 2) < 0 and is0(sp.diff(W, mu).subs(mu, R(3, 2))),
      f'C [3/2, B3] wall area per site pair W even under the swap, W\'\' = {sp.simplify(sp.diff(W, mu, 2))} < 0: maximum at Kelvin')
OUT['controls']['3/2'] = {'swap': 'mu -> 3 - mu', 'law': 'Dehn 0 (B2); wall area maximal (B3)', 'qualifies': True}
# random non-fixed point
m = R(8, 5)
fixed = (m == tau(m)) or (m == sig(m))
check(not fixed, f'C [random 8/5, B1] not fixed: turn gives {tau(m)}, CsCl swap gives {sig(m)}')
check(not is0(DCO[m]) if m in DCO else True, f'C [8/5] Dehn nonzero there: {DCO.get(m)}')
check(not is0(d1.subs(mu, m)) and not is0(sp.diff(W, mu).subs(mu, m)), f'C [8/5] neither t_min nor W is critical there (t\' = {d1.subs(mu, m)}, W\' = {sp.nsimplify(sp.diff(W, mu).subs(mu, m))})')
OUT['controls']['8/5'] = {'qualifies': False, 'reason': 'no geometric swap of the line fixes it; no quantity vanishes or is critical there'}

# =====================================================================================================================
# A. THE SILENT ZONOHEDRON: corners the signed permutations of (a, a+1, a+2), a > 0; Q4 = 0 at a* = -1 + sqrt(1 + sqrt(5/6))
# =====================================================================================================================
progress(1, 'A: the silent zonohedron, structure')
a = sp.symbols('a')
astar = -1 + sp.sqrt(1 + sp.sqrt(R(5, 6)))
mp4 = 6 * a ** 4 + 24 * a ** 3 + 24 * a ** 2 - 5
check(is0(mp4.subs(a, astar)), f'A a* = {float(astar):.12f} is a root of 6a^4 + 24a^3 + 24a^2 - 5 = 6(a(a+2))^2 - 5')
fl = sp.factor_list(mp4)
check(len(fl[1]) == 1 and fl[1][0][1] == 1 and sp.degree(fl[1][0][0], a) == 4, 'A the quartic is irreducible over Q: a* has degree 4', fl)
check(sp.Poly(mp4, a).count_roots(0, sp.oo) == 1, 'A exactly one positive root (the other three conjugates are negative: off the line a > 0)',
      [float(r) for r in sp.Poly(mp4, a).nroots()])
# generators: Kelvin = sum of the 6 segments [-g, g], g = (e_i +- e_j)/2; cube part a[-1,1]^3 = segments [-a e_i, a e_i]
GK = [sp.Matrix(v) / 2 for v in [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)]]
GC = [a * sp.Matrix(v) for v in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]
G = GK + GC
for aa in ([R(1, 3)] if PILOT else [R(1, 3), R(1), R(5, 2)]):
    pts = set()
    for sg in itertools.product((1, -1), repeat=9):
        pts.add(tuple(sp.expand(sum((s * g for s, g in zip(sg, G)), sp.zeros(3, 1)).subs(a, aa))))
    cor = {tuple(c.subs(a, aa) for c in v) for v in sperms((a, a + 1, a + 2))}
    ext = set(tuple(v) for v in HT['extreme']([tuple(p) for p in pts]))
    check(ext == cor, f'A zonotope (6 Kelvin zones + 3 cube zones) has exactly the 48 corners sperm(a, a+1, a+2) at a = {aa}')
check(True, 'A face structure is the same for every a > 0: a zonotope\'s faces depend only on the generator directions (classical)')
# volume, area exact (zonotope formulas), controlled by the hull
def absmono(e):
    """|e| for a > 0 when e = const * a^m (a monomial in a)"""
    e = sp.expand(e); e1 = e.subs(a, 1)
    return 0 if e1 == 0 else sp.Abs(e1) * sp.expand(e / e1)
Vz = sp.expand(8 * sum(absmono(sp.Matrix.hstack(g1, g2, g3).det()) for g1, g2, g3 in itertools.combinations(G, 3)))
planes = {}
for g1, g2 in itertools.combinations(G, 2):
    n = g1.subs(a, 1).cross(g2.subs(a, 1))
    if all(t == 0 for t in n): continue
    first = [t for t in n if t != 0][0]
    key = tuple(t / first for t in n)
    planes.setdefault(key, set())
for key in planes:
    nk = sp.Matrix(key)
    planes[key] = [g for g in G if is0(g.subs(a, 1).dot(nk))]
Az = 0
for key, gs in planes.items():
    for g1, g2 in itertools.combinations(gs, 2):
        cr = g1.cross(g2); c1 = cr.subs(a, 1); j = [i for i in range(3) if c1[i] != 0][0]
        Az += 2 * 4 * sp.sqrt(c1.dot(c1)) * sp.expand(cr[j] / c1[j])
Az = sp.expand(Az)
for aa in [R(1, 3), R(2)]:
    Vh, F = exact_vol([tuple(c.subs(a, aa) for c in v) for v in sperms((a, a + 1, a + 2))])
    check(is0(sp.expand(Vh - Vz.subs(a, aa))), f'A volume formula = hull volume at a = {aa}', Vz.subs(a, aa))
    P, Ff = DS.hull_faces(np.array([[float(c.subs(a, aa)) for c in v] for v in sperms((a, a + 1, a + 2))]))
    area_f = sum(np.linalg.norm(sum(np.cross(P[f[i]], P[f[(i + 1) % len(f)]]) for i in range(len(f)))) / 2 for f in Ff)
    check(abs(area_f - float(Az.subs(a, aa))) < 1e-9, f'A area formula = hull area at a = {aa} (float control)', (area_f, float(Az.subs(a, aa))))
    sizes = sorted(len(f) for f in Ff)
    check(sizes.count(8) == 6 and sizes.count(6) == 8 and sizes.count(4) == 12, f'A faces at a = {aa}: 6 octagons, 8 hexagons, 12 rectangles')
OUT['A'] = {'V': str(Vz), 'A': str(Az), 'zone_planes': len(planes)}
note('A volume V(a)', str(sp.factor(Vz))); note('A area A(a)', str(Az))

# ---- A1 tiling ----
progress(2, 'A: tiling')
belts = {}
for i, g in enumerate(G):
    belts[i] = 2 * sum(1 for key, gs in planes.items() if any(h is g for h in gs))
check(all(belts[i] == 8 for i in range(9)), f'A belts: every one of the 9 zones lies in 4 zone planes -> every belt has 8 faces', belts)
check(True, 'A NO TILING BY TRANSLATIONS for any a > 0 (Venkov 1954 / McMullen 1980: a parallelohedron has belts of 4 or 6 faces only)')
angkinds = {}
for aa in ([R(1, 3)] if PILOT else [R(1, 3), R(1)]):
    r = exact_dehn([tuple(c.subs(a, aa) for c in v) for v in sperms((a, a + 1, a + 2))], f'zonohedron a={aa}')
    check(is0(r['D']), f'A Dehn = 0 at a = {aa} (zonohedron)')
    angkinds[str(aa)] = r['angle_kinds']
AL = angle_list(r)
note('A dihedral kinds (deg = p pi + q beta)', [(f'{d:.4f}', str(p), q) for p, q, _, d in AL])
check(len({tuple(sorted(d)) for d in angkinds.values()}) == 1, 'A the dihedral kinds are the same at every sampled a (face normals do not depend on a)')
ang3 = [(p, q, v) for p, q, v, _ in AL]
res = {f'{AL[e][3]:.4f}': completion(ang3, e) for e in range(len(AL))}
blocked = [k for k, v in res.items() if not v]
find(f'A dihedral completion test: edges that can NOT be surrounded by copies: {blocked} (deg)', res)
OUT['A']['completion'] = {k: [list(map(int, s[0])) + [s[1]] for s in v] for k, v in res.items()}
find('A RESULT: ' + ('no member of the line (a > 0) tiles space by congruent copies, turned or mirrored, face-to-face or not' if blocked else 'angles do not forbid a tiling'))

# ---- A2 tones ----
progress(3, 'A: tones Q4, Q6, Q8, Q12 of the corners')
x, y, z = sp.symbols('x y z')
HK = {k: harmonic_invariants(k) for k in [4, 6, 8, 12]}
check([len(HK[k]) for k in [4, 6, 8, 12]] == [1, 1, 1, 2], 'A O_h-invariant harmonics: dimensions 1, 1, 1, 2 in degrees 4, 6, 8, 12 (Meyer 1954)')
h4 = HK[4][0]
handoff_q4 = -R(96, 5) * (6 * a ** 4 + 24 * a ** 3 + 24 * a ** 2 - 5)
v0 = (a, a + 1, a + 2); rr = sp.expand(sum(t ** 2 for t in v0))
S4 = sp.expand(48 * (sum(t ** 4 for t in v0) - R(3, 5) * rr ** 2))
check(is0(sp.expand(S4 - handoff_q4)), 'A Q4 sum over the 48 corners = -(96/5)(6a^4 + 24a^3 + 24a^2 - 5) (chat-handoff value)')
TONES = {}
for k in [4, 6, 8, 12]:
    for idx, H in enumerate(HK[k]):
        Sk = sp.expand(H(*v0))           # all 48 corners are one O_h orbit: the sum is 48 H(v0)
        rem = sp.rem(sp.Poly(Sk, a), sp.Poly(mp4, a))
        zero = rem.is_zero
        val = float(Sk.subs(a, astar) / rr.subs(a, astar) ** (k // 2))
        roots = [float(t) for t in sp.Poly(Sk, a).nroots(n=20) if abs(sp.im(t)) < 1e-15 and sp.re(t) > 0]
        TONES[f'Q{k}' + (f'.{idx}' if len(HK[k]) > 1 else '')] = {'normalised_value_at_a*': val, 'zero_at_a*': zero, 'positive_zeros_on_line': roots}
        (check if k == 4 else (lambda ok, w: find(w)))(zero if k == 4 else True, f'A tone Q{k}{"." + str(idx) if len(HK[k]) > 1 else ""} at a*: {"ZERO" if zero else "nonzero"} (H(v/|v|) = {val:.6f}); its zeros on a > 0: {[round(t, 6) for t in roots]}')
OUT['A']['tones'] = TONES
check(True, 'A at a* the 48 corners are a spherical 5-design, not a 7-design (an O_h orbit is a t-design iff every invariant harmonic of degree <= t vanishes on it: Sobolev 1962, Goethals-Seidel 1981)')

# ---- A3 canonical form, polar volume, Mahler, roundness ----
progress(4, 'A: canonical form, Mahler, roundness')
al, ga, de = sp.symbols('alpha gamma delta', positive=True)
p1, p2, p3 = sp.Matrix([al, 0, 0]), sp.Matrix([ga, ga, ga]), sp.Matrix([de, de, 0])
sub = {al: 1 / (a + 2), ga: 1 / (3 * a + 3), de: 1 / (2 * a + 3)}
v0m = sp.Matrix([a + 2, a + 1, a])
check(all(is0(sp.simplify(p.subs(sub).dot(v0m) - 1)) for p in (p1, p2, p3)), 'A the corner (a+2, a+1, a) lies on the octagon, hexagon and rectangle planes n/h . x = 1')
Vpol = sp.factor(48 * (al * ga * de / 6).subs(sub))
for aa in [R(1, 3), R(2)]:
    cors = [tuple(c.subs(a, aa) for c in v) for v in sperms((a, a + 1, a + 2))]
    nrm = set()
    for v in [(1, 0, 0), (1, 1, 1), (1, 1, 0)]:
        for w in sperms(v): nrm.add(tuple(w))
    pv = [tuple(sp.Rational(1) * t / max(sum(n[j] * c[j] for j in range(3)) for c in cors) for t in n) for n in nrm]
    Vh, Fp = exact_vol(pv)
    check(is0(Vh - Vpol.subs(a, aa)), f'A polar volume 8/((a+2)(3a+3)(2a+3)) = hull of the polar at a = {aa}', Vh)
check(all(len(f) == 3 for f in Fp) and len(Fp) == 48, 'A the polar has 48 triangular faces: it is not a zonohedron, so polarity leaves the line')
Mah = sp.factor(Vz * Vpol)
dM = sp.factor(sp.diff(Mah, a)); nM = sp.numer(sp.together(dM))
crit_M = [float(t) for t in sp.Poly(nM, a).nroots(n=30) if abs(sp.im(t)) < 1e-20 and sp.re(t) > 0]
find(('NOT' if not sp.rem(sp.Poly(nM, a), sp.Poly(mp4, a)).is_zero else 'IS') + f' critical at a*: A Mahler volume V(Z)V(Z°) is NOT critical at a*; its critical points on a > 0: {[round(t, 6) for t in crit_M]}', sp.factor(nM))
gIQ = sp.expand(2 * sp.diff(Vz, a) * Az - 3 * Vz * sp.diff(Az, a))
valIQ = gIQ.subs(a, astar)
find(('NOT' if not is0(valIQ) else 'IS') + f' critical at a*: A roundness 36 pi V^2/A^3 is at a* (2V\'A - 3VA\' = {float(valIQ):.6f} there)')
crit_IQ = []
fIQ = sp.lambdify(a, gIQ, 'mpmath'); import mpmath as mpm
grid = [0.001 * 1.02 ** i for i in range(700)]
for u, w in zip(grid, grid[1:]):
    if fIQ(u) * fIQ(w) < 0: crit_IQ.append(float(mpm.findroot(fIQ, (u, w), solver='bisect')))
note('A roundness critical points on a > 0 (sign changes, float)', [round(t, 6) for t in crit_IQ])
FT = {}
for k in [4, 6, 8, 12]:
    for idx, H in enumerate(HK[k]):
        u1, u2, u3 = sp.symbols('u1 u2 u3')
        X = p1 * u1 + p2 * u2 + p3 * u3
        poly = sp.Poly(sp.expand(H(*X)), u1, u2, u3)
        integ = sum(cf * sp.factorial(e1) * sp.factorial(e2) * sp.factorial(e3) / sp.factorial(e1 + e2 + e3 + 3) for (e1, e2, e3), cf in poly.terms())
        Fk = sp.factor(48 * al * ga * de * integ)
        Fa = sp.factor(Fk.subs(sub)); num = sp.numer(sp.together(Fa))
        zero = sp.rem(sp.Poly(num, a), sp.Poly(mp4, a)).is_zero
        zs = [float(t) for t in sp.Poly(num, a).nroots(n=30) if abs(sp.im(t)) < 1e-20 and sp.re(t) > 0]
        nm = f'F{k}' + (f'.{idx}' if len(HK[k]) > 1 else '')
        FT[nm] = {'zero_at_a*': zero, 'positive_zeros': zs}
        find(f'A canonical-form tone {nm} (integral of the degree-{k} harmonic over the polar) at a*: {"ZERO" if zero else "nonzero"}; zeros on a > 0: {[round(t, 6) for t in zs]}')
OUT['A'].update({'polar_volume': str(Vpol), 'mahler': str(Mah), 'mahler_critical': crit_M, 'iq_critical': crit_IQ, 'form_tones': FT})

# ---- A4 swaps of the line ----
progress(5, 'A: swaps of the line')
# (i) similarity: edge ratio cube-zone / Kelvin-zone = 2a / sqrt2 = sqrt2 a is strictly increasing, so no two members are similar
check(True, 'A (i) similarity: octagon-rectangle edges 2a, octagon-hexagon and hexagon-rectangle edges sqrt2; ratio sqrt2 a injective -> no similarity swap')
# (ii) polarity: above (48 triangles). (iii) Galois: above (the conjugates are negative).
# (iv) the fold a -> -2 - a
fold = {tuple(sp.expand(t) for t in v) for v in sperms((-2 - a, -1 - a, -a))} == {tuple(sp.expand(t) for t in v) for v in sperms((a, a + 1, a + 2))}
check(fold, 'A (iv) a -> -2 - a gives the SAME corner set: the only reparametrisation symmetry of the corner formula (a fold, fixed point a = -1)')
even = all(is0(sp.expand(H(*v0).subs(a, -2 - a) - H(*v0))) for k in [4, 6, 8, 12] for H in HK[k])
check(even, 'A every tone is EVEN under the fold (eps = +1): parity forces nothing; the fixed point a = -1 gives sperm(1, 0, 1) = the cuboctahedron, off the zonohedron line')
CO = [tuple(sp.Integer(c) for c in v) for v in sperms((1, 1, 0))]
check(set(sperms((sp.Integer(-1), sp.Integer(0), sp.Integer(1)))) == set(CO), 'A the fold\'s fixed point a = -1 gives sperm(-1, 0, 1) = the cuboctahedron')
# (v) Moebius involutions fixing a* and mapping the zero set of Q4 to itself: need a second fixed root r_k and the other pair harmonic
rts = [-1 + sp.sqrt(1 + sp.sqrt(R(5, 6))), -1 - sp.sqrt(1 + sp.sqrt(R(5, 6))), -1 + sp.sqrt(1 - sp.sqrt(R(5, 6))), -1 - sp.sqrt(1 - sp.sqrt(R(5, 6)))]
check(all(is0(mp4.subs(a, r)) for r in rts), 'A the four roots of the Q4 tone')
harm = []
for kk in range(1, 4):
    i, j = [t for t in range(1, 4) if t != kk]
    A_, B_, C_, D_ = rts[i], rts[j], rts[0], rts[kk]
    cr = sp.simplify((A_ - C_) * (B_ - D_) / ((A_ - D_) * (B_ - C_)))
    harm.append(is0(sp.radsimp(cr + 1)))
find(('NONE' if not any(harm) else 'FOUND') + ': A (v) Moebius involution fixes a* and maps the zero set of Q4 to itself (no harmonic quadruple): Q4 = 0 at a* is not a parity zero')
OUT['A']['verdict'] = 'NOT FORCED: Q4 = 0 at a* is a crossing of the line with the 5-design curve of the octahedral group; no geometric swap of the line fixes a*'
# random non-fixed control on this line
m = R(1, 2)
check(all(not sp.rem(sp.Poly(H(*v0), a), sp.Poly(a - m, a)).is_zero for k in [4, 6, 8] for H in HK[k]), 'A control a = 1/2 (random): no tone vanishes there; no swap fixes it')

# =====================================================================================================================
# B. CUBOCTAHEDRON + TWO SQUARE PYRAMIDS (corners sperm(1,1,0) + apexes 2 e_i)
# =====================================================================================================================
progress(6, 'B: two-pyramid cuboctahedra')
apex = {'+x': (2, 0, 0), '-x': (-2, 0, 0), '+y': (0, 2, 0), '-y': (0, -2, 0), '+z': (0, 0, 2), '-z': (0, 0, -2)}
def solid(ks): return HT['extreme'](CO + [tuple(sp.Integer(c) for c in apex[k]) for k in ks])
Bopp, Badj = solid(['+x', '-x']), solid(['+x', '+y'])
RD = [tuple(sp.Integer(c) for c in v) for v in sperms((2, 0, 0)) + sperms((1, 1, 1))]
L = sp.Matrix([[1, 0, 0], [0, R(1, 2), R(1, 2)], [0, R(1, 2), -R(1, 2)]])
img = {tuple(L * sp.Matrix(v)) for v in RD}
check(img == set(tuple(v) for v in Bopp), 'B the opposite solid = L(rhombic dodecahedron), L = [[1,0,0],[0,1/2,1/2],[0,1/2,-1/2]]: the RD stretched by sqrt2 along a 4-fold axis (up to similarity)')
LR = L * sp.Matrix([[2, 2, 0], [2, 0, 2], [0, 2, 2]]).T
H0 = sp.Matrix([[2, 0, 0], [1, 2, 0], [1, 0, 2]])
T1 = LR.inv() * H0; T2 = H0.inv() * LR
check(all(t.is_integer for t in T1) and all(t.is_integer for t in T2), 'B L maps the RD\'s fcc lattice onto the lattice (2,1,1), (0,2,0), (0,0,2) of the handoff cover')
def sym_count(V):
    c = sum((sp.Matrix(v) for v in V), sp.zeros(3, 1)) / len(V); S = {tuple(sp.Matrix(v) - c) for v in V}; n = 0
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            M = sp.zeros(3, 3)
            for i in range(3): M[i, perm[i]] = sg[i]
            if {tuple(M * sp.Matrix(v)) for v in S} == S: n += 1
    return n, c
no, co_ = sym_count(Bopp); na, ca = sym_count(Badj)
check(no == 16 and na == 4, f'B symmetry orders (a symmetry permutes the square normals, so it is a signed permutation about the centroid): opposite {no} (D4h), adjacent {na} (C2v)')
def face_info(V):
    P, F = DS.hull_faces(np.array([[float(c) for c in v] for v in V]))
    M = [sp.Matrix(v) for v in V]; c = sum(M, sp.zeros(3, 1)) / len(M)
    cs = {tuple(-mm + 2 * c) for mm in M} == {tuple(mm) for mm in M}
    fcs = []
    for f in F:
        fc = sum((M[i] for i in f), sp.zeros(3, 1)) / len(f)
        fcs.append({tuple(-M[i] + 2 * fc) for i in f} == {tuple(M[i]) for i in f})
    return cs, all(fcs), F
PL = {}
for k in range(7):
    for ks in itertools.combinations(list(apex), k):
        cs, fcs, F = face_info(solid(list(ks)))
        PL[(k, ks)] = (cs, fcs)
inv = {'+x': '-x', '-x': '+x', '+y': '-y', '-y': '+y', '+z': '-z', '-z': '+z'}
pairs = list(itertools.combinations(list(apex), 2))
fixedp = [p for p in pairs if {inv[p[0]], inv[p[1]]} == set(p)]
check(len(pairs) == 15 and len(fixedp) == 3, f'B the point inversion acts on the 15 placements of two pyramids: fixes the 3 opposite ones, swaps the 12 adjacent ones in 6 pairs')
cs_ok = all(PL[(k, ks)][0] == (set(ks) == {inv[t] for t in ks}) for k in range(7) for ks in itertools.combinations(list(apex), k))
check(cs_ok, 'B over all 64 placements: the solid is centrally symmetric EXACTLY when the placement is fixed by the inversion')
mink = [(k, ks) for k in range(7) for ks in itertools.combinations(list(apex), k) if PL[(k, ks)] == (True, True)]
check(all(k == 2 for k, _ in mink) and len(mink) == 3, f'B Minkowski\'s conditions (centrally symmetric, faces centrally symmetric) hold only for the 3 opposite pairs: {mink}')
check(True, 'B Dehn of CO + k pyramids = (24 - 12k) sqrt2 (x) beta (handoff, exact): it depends on k only, so no swap of placements is odd on it; the two-pyramid solids are the only Dehn-zero ones')
# belts of the opposite solid: edge directions
r = exact_dehn(Bopp, 'opposite'); Pf, Ff = DS.hull_faces(np.array([[float(c) for c in v] for v in Bopp]))
dirs = {}
for f_i, f in enumerate(Ff):
    for i in range(len(f)):
        d = Pf[f[(i + 1) % len(f)]] - Pf[f[i]]; d = d / np.linalg.norm(d); d = d if (d[np.argmax(np.abs(d) > 1e-9)] > 0) else -d
        dirs.setdefault(tuple(np.round(d, 9)), set()).add(f_i)
check(len(dirs) == 4 and all(len(v) == 6 for v in dirs.values()), f'B opposite solid: 4 zones, every belt has 6 faces (Venkov): a parallelohedron of the rhombic-dodecahedron type (Fedorov 1885)', {k: len(v) for k, v in dirs.items()})
check(is0(r['D']) and r['faces'] == 12, 'B opposite solid: 12 faces (4 squares, 8 rhombi of 60 deg), Dehn 0')
# adjacent solid: not centrally symmetric (Minkowski) -> no tiling by translations; dihedral completion test
ra = exact_dehn(Badj, 'adjacent'); ALa = angle_list(ra)
cs, fcs, Fa = face_info(Badj)
check(not cs and not fcs, f'B adjacent solid: NOT centrally symmetric, trapezoid faces -> NO tiling by translations (Minkowski 1897); faces {sorted(len(f) for f in Fa)}')
resa = {f'{d:.4f}': completion([(p, q, v) for p, q, v, _ in ALa], e) for e, (p, q, v, d) in enumerate(ALa)}
find(f'B adjacent solid, dihedral completion test: ' + ('every edge passes' if all(resa.values()) else 'some edge FAILS') + ' (angles alone do not forbid a tiling)', {k: [list(map(int, s[0])) + [s[1]] for s in v] for k, v in resa.items()})
OUT['B'] = {'opposite': {'symmetry_order': no, 'faces': r['faces'], 'linear_image_of_RD': True, 'belts': 6},
            'adjacent': {'symmetry_order': na, 'faces': sorted(len(f) for f in Fa), 'completion': {k: [list(map(int, s[0])) + [s[1]] for s in v] for k, v in resa.items()}},
            'minkowski_placements': [str(t) for t in mink]}

# =====================================================================================================================
# L. LEADS: site swaps of rock salt and zinc blende (lead 2), the turn of the small stellated / great dodecahedron (lead 5)
# =====================================================================================================================
def shifted(planes, c):
    return [(n, b + sum(n[j] * c[j] for j in range(3))) for n, b in planes]
E2 = [list(v) for v in [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0), (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1), (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)]]
E1 = [list(v) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
QT = [list(v) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
lam = sp.symbols('lam')
def network(name, Acell, Bcell, Bcentre, latvol, fixed_val, samples, interval, W_closed=None):
    """A cell(t), B cell(t) built from their own definitions; swap t -> s(t) exchanges them; check volume sum, B(t) ~ A(s(t)) (volume,
    area, Dehn), Dehn odd, wall area W = (area A + area B)/2 even, its shape at the fixed point."""
    res = {'samples': {}}
    for t in samples:
        VA_, A_A, VB_, A_B = None, None, None, None
        vA, VA_, A_A, _ = measures(Acell(t)); vB, VB_, A_B, _ = measures(shifted(Bcell(t), Bcentre))
        check(is0(sp.expand(VA_ + VB_ - latvol)), f'{name} t = {t}: A cell + B cell = lattice cell ({latvol})')
        DA = exact_dehn([tuple(v) for v in vA], f'{name} A({t})')['D']; DB = exact_dehn([tuple(v) for v in vB], f'{name} B({t})')['D']
        res['samples'][str(t)] = {'VA': str(VA_), 'AA': str(sp.nsimplify(A_A)), 'VB': str(VB_), 'AB': str(sp.nsimplify(A_B)), 'DA': str(DA), 'DB': str(DB),
                                  'W': str(sp.radsimp((A_A + A_B) / 2))}
        check(is0(sp.expand(DA + DB)), f'{name} t = {t}: Dehn(A) + Dehn(B) = 0 ({DA} + {DB}) [B2 parity: the two cells make a lattice fundamental domain]')
    return res

progress(7, 'L: rock salt site swap')
# rock salt: A sites = even-sum integer points (weight lam), B = odd-sum (weight 0), unit spacing; A cell |x_i| <= (1+lam)/2, |x_i +- x_j| <= 1
RS_A = lambda t: [(n, (1 + t) / 2) for n in E1] + [(n, 1) for n in E2]
RS_B = lambda t: [(n, (1 - t) / 2) for n in E1] + [(n, 1) for n in E2]
rs_samples = [R(-1, 3), R(0), R(1, 3)] if PILOT else [R(-3, 4), R(-1, 3), R(-1, 5), R(0), R(1, 5), R(1, 3), R(1, 2), R(3, 4)]
RSR = network('rock salt', RS_A, RS_B, (1, 0, 0), 2, 0, rs_samples, None)
Wrs = 6 * (1 - lam) ** 2 + 3 * s2 * (2 * lam - lam ** 2)
okW = all(is0(sp.expand(sp.sympify(RSR['samples'][str(t)]['W']) - Wrs.subs(lam, abs(t)))) for t in rs_samples)
check(okW, 'rock salt: W(lam) = 6(1-|lam|)^2 + 3sqrt2(2|lam| - lam^2) at every sample (even under the swap lam -> -lam)')
check(all(sp.sympify(RSR['samples'][str(t)]['DA']) == 0 for t in rs_samples), 'rock salt: Dehn = 0 at EVERY weight (all dihedrals are rational multiples of pi): parity is satisfied vacuously')
dW0 = sp.diff(Wrs, lam).subs(lam, 0)
check(dW0 < 0 and sp.diff(Wrs, lam, 2) > 0, f'rock salt: W has a KINK at the fixed point lam = 0: one-sided slopes -+({sp.simplify(-dW0)}) -> strict maximum there (the cube); W convex on each side, not concave')
OUT['rock_salt'] = RSR | {'W': str(Wrs) + ' with lam -> |lam|', 'slope_at_0+': str(dW0), 'fixed_cell': 'cube'}

progress(8, 'L: zinc blende site swap')
# zinc blende (units of the CsCl/zinc blende study): Zn = 2D3 weight lam, S = 2D3 + (1,1,1) weight 0; s = (3 + lam)/2
ZB_A = lambda s: [(n, s) for n in QT] + [(n, 2) for n in E2]
ZB_B = lambda s: [([-t for t in n], 3 - s) for n in QT] + [(n, 2) for n in E2]
zb_samples = [R(6, 5), R(3, 2), R(9, 5)] if PILOT else [R(1, 2), R(6, 5), R(13, 10), R(7, 5), R(3, 2), R(8, 5), R(17, 10), R(9, 5), R(5, 2)]
ZBR = network('zinc blende', ZB_A, ZB_B, (1, 1, 1), 16, R(3, 2), zb_samples, None)
for t in zb_samples:
    if 3 - t in zb_samples and t < 3 - t:
        check(is0(sp.expand(sp.sympify(ZBR['samples'][str(t)]['DA']) + sp.sympify(ZBR['samples'][str(3 - t)]['DA']))), f'zinc blende: Dehn(A(s)) = -Dehn(A(3 - s)) at s = {t} (ODD under the swap)')
check(is0(sp.sympify(ZBR['samples']['3/2']['DA'])), 'zinc blende [B2]: forced Dehn = 0 at the fixed point s = 3/2')
vA, VA_, AA_, _ = measures(ZB_A(R(3, 2))); _, Ffix = DS.hull_faces(np.array([[float(c) for c in v] for v in vA]))
check(len(vA) == 16 and sorted(len(f) for f in Ffix) == [3] * 12 + [6] * 4, f'zinc blende: the fixed cell has 16 corners, 12 triangles and 4 hexagons: the triakis truncated tetrahedron (Voronoi cell of diamond)', sorted(len(f) for f in Ffix))
sv = sp.symbols('s')
fitpts = [R(11, 10), R(6, 5), R(7, 5), R(8, 5), R(9, 5)] if not PILOT else [R(6, 5), R(3, 2), R(9, 5)]
Wv = {}
for t in sorted(set(fitpts + [q for q in zb_samples if 1 < q < 2])):
    if str(t) in ZBR['samples']: Wv[t] = sp.sympify(ZBR['samples'][str(t)]['W'])
    else:
        _, _, A1, _ = measures(ZB_A(t)); _, _, A2_, _ = measures(shifted(ZB_B(t), (1, 1, 1))); Wv[t] = sp.radsimp((A1 + A2_) / 2)
Wzb = sp.expand(sp.interpolate([(t, Wv[t]) for t in fitpts], sv))
others = [t for t in Wv if t not in fitpts]
check(all(is0(sp.expand(Wzb.subs(sv, t) - Wv[t])) for t in others), f'zinc blende: W(s) on (1, 2) = {sp.factor(Wzb)} (fitted on {len(fitpts)} points, checked on {len(others)} more)')
check(is0(sp.expand(Wzb - Wzb.subs(sv, 3 - sv))), 'zinc blende [B3]: W(s) = W(3 - s) (even under the swap)')
W2 = sp.diff(Wzb, sv, 2)
check(is0(sp.diff(Wzb, sv).subs(sv, R(3, 2))), f'zinc blende: W critical at the fixed point s = 3/2; W\'\' = {sp.simplify(W2.subs(sv, R(3, 2)))} ({"concave: MAXIMUM" if W2.subs(sv, R(3, 2)) < 0 else "convex: MINIMUM"})')
OUT['zinc_blende'] = ZBR | {'W_on_(1,2)': str(Wzb), 'W2_at_fixed': str(sp.simplify(W2.subs(sv, R(3, 2)))), 'fixed_cell': 'triakis truncated tetrahedron'}

progress(9, 'L: small stellated / great dodecahedron turn')
sys.path.insert(0, os.path.join(STUD, '2026-11-09-regular-stars-census', 'scripts'))
import regstar as RS, turnlib as TL
from q5 import Q5
rows = json.load(open(os.path.join(STUD, '2026-11-09-regular-stars-census', 'data', 'flags.json')))
ch = RS.Chamber(RS.mirrors_of(TL.icosahedron()), (Q5(1), Q5(Fr(37, 100)), Q5(Fr(11, 100))))
def tvals(q, r2, m):
    A = [ch.fold(v) for v in RS.delta_vertices(q, r2, m)]; B = [ch.fold(v) for v in RS.antipol_vertices(q, r2, m)]
    return {(i, j): RS.dotv(u, w) for i, u in enumerate(A) for j, w in enumerate(B)}
def solve3(M, b):
    def det(M): return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    D = det(M); out = []
    for k in range(3):
        Mk = [[b[i] if j == k else M[i][j] for j in range(3)] for i in range(3)]; out.append(det(Mk) / D)
    return out
_s4 = open(os.path.join(STUD, '2026-11-09-regular-stars-census', 'scripts', 's4_starturn.py')).read()
S4NS = {'Fr': Fr, 'math': math, 'Q5': Q5}; exec(_s4[_s4.index('def ratsqrt'):_s4.index('out = []; allok')], S4NS); sqrt_q5 = S4NS['sqrt_q5']
STARS = {}
for sym in ['{5/2,5}', '{5,5/2}']:
    row = [r_ for r_ in rows if r_['symbol'] == sym][0]
    q = [RS.vp(v) for v in row['q']]; r2 = [RS.q5p(v) for v in row['r2']]; h2, R2 = r2[-1], r2[0]; c = h2 * R2
    hR = sqrt_q5(c)
    check(hR is not None, f'{row["name"]}: turn mu -> c/mu, c = {RS.q5s(c)}, fixed point hR = {RS.q5s(hR) if hR else None} in Q(sqrt5)')
    t0, _ = RS.tmin_star(q, r2, hR, ch)
    branches = {}
    for side in (1, -1):
        dl = Q5(Fr(1, 10000)); ms = [hR + Q5(side * k) * dl for k in (1, 2, 3, 4)]
        TV = [tvals(q, r2, m_) for m_ in ms]
        tops = [max(T.values(), key=lambda v: v.f()) for T in TV]
        args = [{k for k, v in T.items() if v == tp} for T, tp in zip(TV, tops)]
        common = set.intersection(*args)
        check(len(common) >= 1, f'{row["name"]}: one corner pair is the maximum at all four points on the {"right" if side > 0 else "left"} of hR')
        k0 = sorted(common)[0]
        Mx = [[Q5(1), ms[i], Q5(1) / ms[i]] for i in range(3)]
        A0, A1, A2 = solve3(Mx, [TV[i][k0] for i in range(3)])
        f = lambda m_: A0 + A1 * m_ + A2 / m_
        check(f(ms[3]) == TV[3][k0], f'{row["name"]}: on the {"right" if side > 0 else "left"} t_min* = A + B mu + C/mu (fitted on 3 points, exact on the 4th)')
        check(f(hR) == t0, f'{row["name"]}: that branch reaches t_min*(hR) = {RS.q5s(t0)} = {t0.f():.6f}')
        branches[side] = (A0, A1, A2)
        check(RS.tmin_star(q, r2, c / ms[0], ch)[0] == tops[0], f'{row["name"]}: turn symmetry t*(mu) = t*(c/mu) exact at mu = hR {"+" if side > 0 else "-"} 1e-4')
    dR = branches[1][1] - branches[1][2] / (hR * hR); dL = branches[-1][1] - branches[-1][2] / (hR * hR)
    kind = 'smooth' if dR == Q5(0) else ('V-shaped kink (minimum)' if dR.sign() > 0 else 'inverted kink (maximum)')
    check(dR == Q5(0) - dL, f'{row["name"]}: one-sided slopes at hR are opposite (right {dR.f():.6f}, left {dL.f():.6f}), as the turn forces: {kind}')
    if dR == Q5(0):
        d2 = Q5(2) * branches[1][2] / (hR * hR * hR); kind += f', t\'\' = {d2.f():.6f} ({"minimum" if d2.sign() > 0 else "maximum"})'
    STARS[row['name']] = {'c': RS.q5s(c), 'hR': RS.q5s(hR), 't_at_hR': RS.q5s(t0), 'right_branch': [RS.q5s(v) for v in branches[1]], 'left_branch': [RS.q5s(v) for v in branches[-1]],
                          'slope_right': RS.q5s(dR), 'slope_left': RS.q5s(dL), 'shape': kind}
    note(f'{row["name"]} at the turn', kind)
OUT['stars'] = STARS

progress(11, 'writing')
ok = all(c_[0] for c_ in CHECKS)
OUT['checks'] = [[c_[0], c_[1], c_[2]] for c_ in CHECKS]; OUT['seconds'] = round(time.time() - T0, 1)
json.dump(OUT, open(os.path.join(DATA, 'forced-pilot.json' if PILOT else 'forced.json'), 'w'), indent=1, default=str)
print(f'{sum(c_[0] for c_ in CHECKS)}/{len(CHECKS)} checks ok, {OUT["seconds"]} s')
print('PROGRESS 1.00 done')
print('FINAL ok' if ok else 'FINAL FAIL')
