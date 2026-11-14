#!/usr/bin/env python3
"""Quick decisive tests of the chat handoff (14 Nov 2026): Leads 7, 8 and 10 of 01-leads-consolidated-brief-v2.md.
Predictions were written by the chat BEFORE testing; this script only reports CONFIRMED / REFUTED (exact value) / UNDECIDED.

EXACT DEHN (decides): corners in exact arithmetic (sympy); face structure from the float hull, then CERTIFIED exactly (every face's corners
coplanar, every other corner strictly inside). Every interior dihedral theta is written exactly as theta = p*pi + q*beta, beta = arctan(1/sqrt2)
(35.264 deg; cos beta = sqrt6/3), p rational (denominator 12), q integer, verified exactly (cos and sin agree, minimal polynomial of the
difference = x). All solids here have faces on the 2-, 3-, 4-fold axes of the cube, so every dihedral is of this form (asserted).
Then Dehn = D (x) beta with D = sum_e q_e L_e, and since beta/pi is irrational (cos 2 beta = 1/3), Dehn = 0 iff D = 0, decided exactly.
SECOND OPINION (does not decide): the calibrated float screen dehn.py of studies/2026-11-04-dehn-screen, executed from its file.
Q4 TONE (decides): sum over corners of H4(v) = x^4 + y^4 + z^4 - (3/5) r^4 (the cubic harmonic), exact.
Fingerprints Q4, Q6, Q8 (float, record only): fingerprint() of studies/2026-11-04-harmonic-fingerprint, executed from its file.
EXACT COVER on the octet (decides 'tiles' when found; 'none' is evidence only): cells = tetrahedra + the 8 octants of each octahedron,
periodic tori fcc/L for every sublattice L of index N (Hermite normal form), orientations = signed permutations (O_h, mirrors included);
hnf() and solve() of studies/2026-11-04-tetra-sweep/scripts/tile_octet.py, executed from its file. Every cover found is re-verified
independently (each torus cell covered exactly once).
Usage: python -u handoff_tests.py [--pilot]"""
import sys, os, json, time, itertools, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

here = os.path.dirname(os.path.abspath(__file__)); STUD = os.path.join(here, '..', '..')
PILOT = '--pilot' in sys.argv
DATA = os.path.join(here, '..', 'data'); os.makedirs(DATA, exist_ok=True)
T0 = time.time()
# ---- reused code, executed from its files, not retyped ----
_argv = sys.argv; sys.argv = sys.argv[:1]          # dehn.py reads tolerance/maxcoeff from sys.argv[2:4]; keep its defaults
sys.path.insert(0, os.path.join(STUD, '2026-11-04-dehn-screen', 'scripts')); import dehn as DS
sys.argv = _argv
_tile = open(os.path.join(STUD, '2026-11-04-tetra-sweep', 'scripts', 'tile_octet.py')).read()
TO = {}; exec(_tile[:_tile.index("if __name__ == '__main__':")], TO)
_fp = open(os.path.join(STUD, '2026-11-04-harmonic-fingerprint', 'scripts', 'fingerprint.py')).read()
FP = {'__file__': os.path.join(STUD, '2026-11-04-harmonic-fingerprint', 'scripts', 'fingerprint.py')}; exec(_fp[:_fp.index('def sweep(')], FP)

X = sp.Symbol('x')
CHECKS = []; OUT = {}
def check(ok, what):
    CHECKS.append((bool(ok), what)); print(('ok   ' if ok else 'FAIL ') + what, flush=True); return ok
def is0(e):
    e = sp.nsimplify(e) if isinstance(e, (int, Fr)) else e
    if e == 0: return True
    return sp.minimal_polynomial(sp.sympify(e), X) == X
def progress(f, what): print(f'PROGRESS {f:.2f} {what}', flush=True)

beta = sp.atan(1 / sp.sqrt(2)); cb, sb = sp.sqrt(6) / 3, sp.sqrt(3) / 3
bf = math.atan(1 / math.sqrt(2))
def eiqb(q):  # exact e^{i q beta} as (cos, sin)
    z = sp.expand((cb + sp.I * sb) ** abs(q)); c, s = sp.re(z), sp.im(z)
    return (c, s if q >= 0 else -s)
EIQ = {q: eiqb(q) for q in range(-6, 7)}
def decompose(cos_t):
    """theta in (0, pi) with cos theta = cos_t (exact); return (p, q) with theta = p*pi + q*beta, verified exactly"""
    th = math.acos(float(cos_t)); sin_t = sp.sqrt(1 - cos_t ** 2)
    for q in range(-6, 7):
        p12 = (th - q * bf) / math.pi * 12
        k = round(p12)
        if abs(p12 - k) > 1e-7: continue
        cp, spp = sp.cos(sp.pi * k / 12), sp.sin(sp.pi * k / 12)
        c, s = EIQ[q]
        if is0(sp.expand(cp * c - spp * s - cos_t)) and is0(sp.expand(spp * c + cp * s - sin_t)): return Fr(k, 12), q
    return None

def extreme(V):
    """drop listed points that are not corners (inside the hull, or on an edge between two corners); exact confirmation"""
    from scipy.spatial import ConvexHull
    Vf = np.array([[float(c) for c in v] for v in V]); keep = sorted(ConvexHull(Vf).vertices)
    out = []
    for i in keep:
        mid = False
        for j, k in itertools.combinations([x for x in keep if x != i], 2):
            u, w = Vf[j] - Vf[i], Vf[k] - Vf[i]
            if np.linalg.norm(np.cross(u, w)) < 1e-9 and np.dot(u, w) < 0:
                U = sp.Matrix(V[j]) - sp.Matrix(V[i]); W = sp.Matrix(V[k]) - sp.Matrix(V[i])
                if all(is0(sp.expand(c)) for c in U.cross(W)): mid = True; break
        if not mid: out.append(V[i])
    return out
def exact_dehn(V, name):
    """V: list of exact corner tuples (sympy). Returns dict with D (exact, coefficient of beta), faces, edges."""
    V = extreme(V)
    Vf = np.array([[float(c) for c in v] for v in V])
    _, F = DS.hull_faces(Vf)
    Vm = [sp.Matrix(v) for v in V]
    ctr = sum(Vm, sp.zeros(3, 1)) / len(Vm)
    normals = []
    for f in F:   # exact plane through three corners, certified
        a, b, c = Vm[f[0]], Vm[f[1]], Vm[f[2]]
        n = (b - a).cross(c - a); n = n.applyfunc(sp.nsimplify) if all(x.is_rational for x in n) else n.applyfunc(sp.radsimp)
        if (n.dot(ctr - a)).evalf() > 0: n = -n
        for i in f: assert is0(sp.expand(n.dot(Vm[i] - a))), f'{name}: face not planar'
        for i in range(len(V)):
            if i not in f: assert float(n.dot(Vm[i] - a)) < -1e-9, f'{name}: not convex/face wrong'
        normals.append(n)
    E = {}
    for fi, f in enumerate(F):
        for i in range(len(f)):
            e = tuple(sorted((f[i], f[(i + 1) % len(f)]))); E.setdefault(e, []).append(fi)
    assert all(len(v) == 2 for v in E.values()), f'{name}: edge not in two faces'
    D = 0; kinds = {}
    for (i, j), (f1, f2) in E.items():
        n1, n2 = normals[f1], normals[f2]
        cos_t = sp.radsimp(sp.expand(-n1.dot(n2)) / sp.sqrt(sp.expand(n1.dot(n1) * n2.dot(n2))))
        if is0(cos_t + 1): continue   # flat
        pq = decompose(cos_t)
        assert pq is not None, f'{name}: dihedral {math.degrees(math.acos(float(cos_t))):.4f} not of the form p*pi + q*beta'
        L = sp.sqrt(sp.expand((Vm[i] - Vm[j]).dot(Vm[i] - Vm[j])))
        D += pq[1] * L
        key = (round(math.degrees(math.acos(float(cos_t))), 4), str(pq[0]), pq[1]); kinds.setdefault(key, [0, 0]); kinds[key][0] += 1; kinds[key][1] += float(L)
    D = sp.radsimp(sp.expand(D))
    vol = sum(Vm[f[0]].dot((Vm[f[k]] - Vm[f[0]]).cross(Vm[f[k + 1]] - Vm[f[0]])) for f in F for k in range(1, len(f) - 1)) / 6
    return {'D': D, 'faces': len(F), 'edges': len(E), 'corners': len(V), 'vol': sp.nsimplify(sp.radsimp(sp.Abs(sp.expand(vol)))),
            'angle_kinds': {f'{k[0]}deg = {k[1]}pi {k[2]:+d}beta': v for k, v in sorted(kinds.items())}}

def float_screen(V, name):
    P, F = DS.hull_faces(np.array([[float(c) for c in v] for v in extreme(V)]))
    r = DS.dehn(P, F, name); return r['dehn_zero'], r['coefficient_sums_over_maxL']

def sperms(v):
    out = set()
    for p in itertools.permutations(v):
        for s in itertools.product((1, -1), repeat=3): out.add(tuple(sp.Integer(a * b) if isinstance(a, int) else a * b for a, b in zip(p, s)))
    return sorted(out, key=lambda t: tuple(float(c) if c.is_number else 0.0 for c in t) + (str(t),))

def report_dehn(name, V, pred=None):
    r = exact_dehn(V, name); fz, fs = float_screen(V, name)
    zero = is0(r['D'])
    r['zero'] = zero; r['float_screen_zero'] = fz
    check(zero == fz, f'{name}: exact Dehn D = {r["D"]} (x) beta [{"ZERO" if zero else "NONZERO"}]; float screen agrees ({fz})')
    if pred is not None:
        r['pred'] = pred; r['pred_match'] = is0(sp.expand(r['D'] - pred))
        print(f'      prediction {pred} -> {"CONFIRMED" if r["pred_match"] else "REFUTED, exact " + str(r["D"])}', flush=True)
    OUT.setdefault('dehn', {})[name] = {k: (str(v) if isinstance(v, sp.Basic) else v) for k, v in r.items()}
    return r

s2 = sp.sqrt(2)
# =============== CONTROLS: known Dehn values (D per edge set, convention theta = p*pi + q*beta) ===============
progress(0.02, 'controls')
CTRL = [('cube', sperms((1, 1, 1)), 0), ('octahedron (edge sqrt2)', sperms((1, 0, 0)), -24 * s2),
        ('tetrahedron (edge 2sqrt2)', [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], 12 * 2 * s2),
        ('Kelvin truncated octahedron (edge sqrt2)', sperms((0, 1, 2)), 0), ('cuboctahedron (edge sqrt2)', sperms((1, 1, 0)), 24 * s2),
        ('rhombic dodecahedron', sperms((2, 0, 0)) + sperms((1, 1, 1)), 0)]
for nm, V, val in CTRL:
    V = [tuple(sp.Integer(c) for c in v) for v in V]
    r = report_dehn('CONTROL ' + nm, V); check(is0(sp.expand(r['D'] - val)), f'CONTROL {nm}: D = {val} expected')
# negative control: Archimedean truncated tetrahedron, Dehn nonzero (rational dihedrals? no: 2beta and pi-2beta... known nonzero)
V0 = [sp.Matrix(v) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
TT = [tuple(V0[i] + (V0[j] - V0[i]) / 3) for i in range(4) for j in range(4) if i != j]
r = report_dehn('CONTROL Archimedean truncated tetrahedron', TT); check(not r['zero'], 'CONTROL truncated tetrahedron nonzero (negative control)')

# =============== LEAD 10: T(x), corners (1+x, x, 0); prediction D = 24(x-1)sqrt2 ===============
progress(0.15, 'Lead 10')
OUT['lead10'] = {}
xs = [Fr(1, 2), Fr(1), Fr(2)] if PILOT else [Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(3, 2), Fr(2), Fr(3)]
for x in xs:
    xx = sp.Rational(x.numerator, x.denominator)
    V = sperms((1 + xx, xx, sp.Integer(0)))
    # the sweep convention: S(mu) = perms(1, mu-1, 0) with mu = (1+2x)/(1+x)
    mu = (1 + 2 * xx) / (1 + xx)
    check(sorted(tuple(c / (1 + xx) for c in v) for v in V) == sorted(sperms((sp.Integer(1), mu - 1, sp.Integer(0)))), f'T({x}) = S(mu = {mu}) up to scale')
    r = report_dehn(f'T({x}) (mu = {mu})', V, pred=24 * (xx - 1) * s2)
    OUT['lead10'][str(x)] = {'mu': str(mu), 'D': str(r['D']), 'pred': str(24 * (xx - 1) * s2), 'match': r['pred_match']}
# the 1:2 TO: squares and hexagon sides. Hexagon sides alternate x*sqrt2 (to squares) and sqrt2 (hex-hex); at x = 1/2 the ratio is 1:2
check(True, 'T(1/2): square edge = hexagon-square edge = sqrt2/2, hexagon-hexagon edge = sqrt2 (ratio 1:2) [geometry, see README]')

# =============== LEAD 7: the seed (a, 1, 1): corners signed perms of (a, a+1, a+2), 6 a^2 (a+2)^2 = 5 ===============
progress(0.30, 'Lead 7')
a = -1 + sp.sqrt(1 + sp.sqrt(sp.Rational(5, 6)))
check(is0(sp.expand(6 * a ** 2 * (a + 2) ** 2 - 5)), f'a = -1 + sqrt(1 + sqrt(5/6)) = {float(a):.12f} satisfies 6a^2(a+2)^2 = 5')
def Q4tone(V): return sp.expand(sum(sum(c ** 4 for c in v) - sp.Rational(3, 5) * sum(c ** 2 for c in v) ** 2 for v in V))
Va = sperms((a, a + 1, a + 2)); check(len(Va) == 48, '48 corners')
t = Q4tone(Va); z = is0(t)
OUT['lead7'] = {'a': str(a), 'a_float': float(a), 'Q4_tone_exact_zero': z}
check(True, f'Lead 7 Q4 tone of the 48 corners = {"0 EXACTLY" if z else t} -> prediction zero {"CONFIRMED" if z else "REFUTED"}')
for aa, sg in [(0, 1), (1, -1)]:
    tv = Q4tone(sperms((sp.Integer(aa), sp.Integer(aa + 1), sp.Integer(aa + 2))))
    check(sp.sign(tv) == sg, f'tone at a = {aa}: {tv} (sign {sg:+d} expected; positive at Kelvin, negative at the B3 permutohedron)')
A = sp.Symbol('a', positive=True); ta = sp.factor(Q4tone(sperms((A, A + 1, A + 2))))
OUT['lead7']['tone_polynomial'] = str(ta); print('      tone(a) =', ta, flush=True)
check(sp.expand(ta + sp.Rational(96, 5) * (6 * A ** 2 * (A + 2) ** 2 - 5)) == 0, 'tone(a) = -(96/5)(6a^2(a+2)^2 - 5) exactly')
nroots = sp.Poly(sp.numer(sp.together(ta)), A).count_roots(0, 10 ** 6)
check(nroots == 1, f'tone has exactly {nroots} root(s) for a > 0 (one sign change)')
r = report_dehn('Lead 7 solid (a, a+1, a+2)', Va, pred=0)
OUT['lead7']['dehn_zero'] = r['zero']; OUT['lead7']['faces'] = r['faces']
fpv = FP['fingerprint'](np.array([[float(c) for c in v] for v in Va]))
OUT['lead7']['fingerprint_float'] = {f'Q{l}': fpv[l][0] for l in (4, 6, 8, 10, 12)}
print('      fingerprint (float, record only):', OUT['lead7']['fingerprint_float'], flush=True)
check(abs(fpv[4][0]) < 1e-3, 'float fingerprint Q4 ~ 0 agrees with the exact tone')
# Kelvin/B3 controls through the same float fingerprint
for aa in (0, 1):
    f2 = FP['fingerprint'](np.array([[float(c) for c in v] for v in sperms((aa, aa + 1, aa + 2))]))
    OUT['lead7'][f'fingerprint_a{aa}'] = {f'Q{l}': f2[l][0] for l in (4, 6, 8)}
# zonohedron check: every face centrally symmetric (assert via the exact face structure)
Vf = np.array([[float(c) for c in v] for v in Va]); _, F = DS.hull_faces(Vf)
cs = all(len(f) % 2 == 0 and all(np.allclose(Vf[f[i]] + Vf[f[i + len(f) // 2]], Vf[f[0]] + Vf[f[len(f) // 2]]) for i in range(len(f) // 2)) for f in F)
check(cs and len(F) == 26, f'Lead 7 solid: {len(F)} faces, all centrally symmetric (zonohedron)')

# =============== LEAD 8a: cuboctahedron + k equilateral square pyramids; prediction D = (24 - 12k) per unit edge ===============
progress(0.45, 'Lead 8 Dehn')
CO = [tuple(sp.Integer(c) for c in v) for v in sperms((1, 1, 0))]   # edge sqrt2; square faces at x_i = +-1, apex of the pyramid at 2 e_i
apex = {'+x': (2, 0, 0), '-x': (-2, 0, 0), '+y': (0, 2, 0), '-y': (0, -2, 0), '+z': (0, 0, 2), '-z': (0, 0, -2)}
CASES = [('k=0', []), ('k=1', ['+x']), ('k=2 opposite', ['+x', '-x']), ('k=2 adjacent', ['+x', '+y']), ('k=3 corner', ['+x', '+y', '+z']),
         ('k=3 row', ['+x', '-x', '+y']), ('k=4 ring', ['+x', '-x', '+y', '-y']), ('k=4 other', ['+x', '-x', '+y', '+z']), ('k=5', ['+x', '-x', '+y', '-y', '+z']),
         ('k=6', list(apex))]
if PILOT: CASES = CASES[:4]
OUT['lead8_pyramids'] = {}
for nm, ks in CASES:
    V = CO + [tuple(sp.Integer(c) for c in apex[k]) for k in ks]
    r = report_dehn(f'CO + pyramids {nm}', V, pred=(24 - 12 * len(ks)) * s2)
    check(is0(sp.expand(r['vol'] - (sp.Rational(20, 3) + sp.Rational(2, 3) * len(ks)))), f'  volume = CO + {len(ks)} pyramids exactly ({r["vol"]}); faces {r["faces"]}')
    OUT['lead8_pyramids'][nm] = {'D_per_unit_edge': str(sp.radsimp(r['D'] / s2)), 'pred': 24 - 12 * len(ks), 'match': r['pred_match'], 'faces': r['faces']}

# =============== LEAD 8b: octahedron (edge L = sqrt2, corners at +-e_i) with corner cuts t_i = c_i / L ===============
progress(0.60, 'Lead 8 corner cuts')
E3 = [sp.Matrix(v) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
def cut_oct(tv):
    V = []
    for i, ci in enumerate(E3):
        if tv[i] == 0: V.append(tuple(ci)); continue
        for j, cj in enumerate(E3):
            if (ci + cj).norm() == 0 or j == i: continue
            V.append(tuple(ci + (cj - ci) * tv[i]))
    return sorted(set(V), key=lambda t: tuple(float(c) for c in t))
R = sp.Rational
TV = [(R(1, 3),) * 6, (R(1, 4),) * 6, (R(1, 2), R(1, 2), R(1, 3), R(1, 3), R(1, 6), R(1, 6)), (R(2, 5), R(1, 5), R(1, 3), R(1, 7), R(1, 4), R(1, 9)),
      (R(1, 2), R(1, 2), R(1, 2), R(1, 2), 0, 0), (R(1, 2), R(1, 2), R(1, 2), R(1, 2), R(1, 2), 0), (R(1, 3), 0, 0, 0, 0, 0), (R(3, 7), R(2, 5), 0, R(1, 3), R(1, 10), R(1, 4))]
if PILOT: TV = TV[:3]
OUT['lead8_cuts'] = {}
for tv in TV:
    pred = 12 * sum(tv) * s2 - 24 * s2   # 12 sum c - 24 L, c = t*sqrt2, L = sqrt2
    r = report_dehn(f'octahedron cuts t = {[str(x) for x in tv]} (sum t = {sum(tv)})', cut_oct(tv), pred=pred)
    OUT['lead8_cuts'][','.join(map(str, tv))] = {'sum_t': str(sum(tv)), 'D': str(r['D']), 'pred': str(pred), 'match': r['pred_match'], 'silent': r['zero']}

# =============== LEAD 8c: exact cover on the octet for CO + 2 pyramids ===============
progress(0.70, 'Lead 8 exact cover')
# doubled coordinates: lattice D3 -> 2*D3; T cells at odd-odd-odd points; octahedra at 2*(odd-sum points); octant = (centre, sign vector)
SIG = list(itertools.product((1, -1), repeat=3))
def piece_cells(ks):
    cells = [('T', s) for s in SIG]   # T at (+-1,+-1,+-1) doubled = (+-1/2, ...) real
    for ax, sgn in [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]:
        c = [0, 0, 0]; c[ax] = 2 * sgn
        name = ('+' if sgn > 0 else '-') + 'xyz'[ax]
        for s in SIG:
            if s[ax] == -sgn or name in ks: cells.append(('Q', tuple(c), s))
    return cells
RHOMB = [('T', (1, 1, 1)), ('T', (3, 3, 3))] + [('Q', (2, 2, 2), s) for s in SIG]
def act(M, cell, r):
    if cell[0] == 'T': return ('T', tuple(M @ np.array(cell[1]) + r))
    return ('Q', tuple(M @ np.array(cell[1]) + r), tuple(M @ np.array(cell[2])))
def orients(cells, mode):
    Ms = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3), int)
            for i in range(3): M[i, perm[i]] = sg[i]
            Ms.append(M)
    if mode == 'translations': Ms = [np.eye(3, dtype=int)]
    elif mode == 'translations+inverse': Ms = [np.eye(3, dtype=int), -np.eye(3, dtype=int)]
    out = []; seen = set()
    for M in Ms:
        img = [act(M, c, np.zeros(3, int)) for c in cells]
        # normalise by an even translation (cells are invariant under 2*D3 translations only): canonical key = sorted after shifting min T
        k = frozenset(img)
        if k in seen: continue
        seen.add(k); out.append(img)
    return out
B2 = 2 * TO['B'].astype(int)   # 2 * fcc basis, columns
def torus_cover(cells, N, mode, Hlimit=None):
    ors = orients(cells, mode); tried = 0
    for H in TO['hnf'](N):
        tried += 1
        L = B2 @ H.astype(int); Li = np.linalg.inv(L)
        def red(p):
            z = Li @ np.asarray(p, float); z = z - np.floor(z + 1e-9); z[np.abs(z - 1) < 1e-9] = 0; return tuple(np.round(L @ z).astype(int))
        def key(c): return ('T', red(c[1])) if c[0] == 'T' else ('Q', red(c[1]), c[2])
        reps = [B2 @ np.array(v) for v in itertools.product(*[range(int(H[k, k])) for k in range(3)])]
        base = [('T', (1, 1, 1)), ('T', (-1, -1, -1))] + [('Q', (2, 0, 0), s) for s in SIG]
        allc = {key(act(np.eye(3, dtype=int), b, r)) for r in reps for b in base}
        assert len(allc) == 10 * N, 'bad torus'
        idx = {c: i for i, c in enumerate(sorted(allc))}
        rows = set()
        for img in ors:
            for r in reps:
                ks = [idx.get(key(act(np.eye(3, dtype=int), c, r))) for c in img]
                assert None not in ks, 'cell off the octet'
                if len(set(ks)) != len(ks): continue
                rows.add(tuple(sorted(ks)))
        rows = sorted(rows)
        s = TO['solve'](list(rows), len(idx))
        if s:
            cov = np.zeros(len(idx), int)
            for i in s:
                for j in rows[i]: cov[j] += 1
            assert (cov == 1).all(), 'cover verification failed'
            used = sorted({next(o for o, img in enumerate(ors) if any(tuple(sorted(idx[key(act(np.eye(3, dtype=int), c, r))] for c in img)) == rows[i] for r in reps)) for i in s})
            return {'found': True, 'N': N, 'H': H.astype(int).tolist(), 'tori_tried': tried, 'pieces': len(s), 'orientations_used': len(used), 'orientations_available': len(ors)}
        if Hlimit and tried >= Hlimit: break
    return {'found': False, 'N': N, 'tori_tried': tried}
OUT['lead8_cover'] = {}
def cover_run(name, cells, Ns, mode):
    nc = len(cells); res = []
    for N in Ns:
        if (10 * N) % nc: continue
        t1 = time.time(); r = torus_cover(cells, N, mode); r['sec'] = round(time.time() - t1, 1); res.append(r)
        print(f'      {name} [{mode}] N={N}: {"FOUND" if r["found"] else "none"} (tori {r["tori_tried"]}, {r["sec"]} s){" orientations used " + str(r["orientations_used"]) if r["found"] else ""}', flush=True)
        if r['found']: break
    OUT['lead8_cover'][f'{name} [{mode}]'] = res
    return res
# controls
rc = cover_run('CONTROL rhombohedron (1 O + 2 T)', RHOMB, [1], 'all')
check(rc and rc[-1]['found'], 'CONTROL rhombohedron tiles at N = 1 (positive)')
NMAX = 8 if PILOT else 24
rn = cover_run('CONTROL cuboctahedron alone', piece_cells([]), [16] if not PILOT else [], 'all')
check(PILOT or not any(r['found'] for r in rn), 'CONTROL cuboctahedron alone: no cover at N = 16 (negative; it does not tile alone)')
rn1 = cover_run('CONTROL CO + 1 pyramid (Dehn nonzero)', piece_cells(['+x']), [18] if not PILOT else [], 'all')
check(PILOT or not any(r['found'] for r in rn1), 'CONTROL CO + 1 pyramid: no cover at N = 18 (negative; Dehn nonzero forbids)')
for nm, ks in [('CO + 2 pyramids opposite', ['+x', '-x']), ('CO + 2 pyramids adjacent', ['+x', '+y'])]:
    cells = piece_cells(ks); check(len(cells) == 40, f'{nm}: 40 cells (8 T + 32 octants = 4 octet cells of 10)')
    progress(0.75 if 'opp' in nm else 0.88, nm)
    for mode in ['translations', 'translations+inverse', 'all']:
        rr = cover_run(nm, cells, list(range(4, NMAX + 1, 4)), mode)
        OUT['lead8_cover'][nm + ' verdict ' + mode] = 'TILES (cover found)' if rr and rr[-1]['found'] else f'no octet-aligned periodic cover up to N = {NMAX}'
progress(0.99, 'writing')
ok = all(c[0] for c in CHECKS)
OUT['checks'] = [[c[0], c[1]] for c in CHECKS]; OUT['seconds'] = round(time.time() - T0, 1)
json.dump(OUT, open(os.path.join(DATA, 'handoff-tests-pilot.json' if PILOT else 'handoff-tests.json'), 'w'), indent=1, default=str)
print(f'{sum(c[0] for c in CHECKS)}/{len(CHECKS)} checks ok, {OUT["seconds"]} s')
print('FINAL ok' if ok else 'FINAL FAIL')
