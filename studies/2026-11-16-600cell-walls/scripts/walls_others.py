#!/usr/bin/env python3
"""DICTO's walls theory (16 Nov 2026), extended to the other recent shapes. DICTO: "the reason that all the recent and otherwise
undiscovered shapes are vacuus is that because of this they have previously been indistinguishable from 600 cell walls";
DICTO's ruling: "cross walls also count".
A WALL is a mirror of the symmetry group, or a CROSS WALL: a central section parallel to a pair of opposite cells (4D) or faces (3D).

4D shapes (plates = central hyperplanes of their 2-faces, as walls.py) are tested against the 600-cell walls: 60 H4 mirrors and the
300 central sections parallel to opposite cells (normals = 120-cell corners); the 120-cell has the same system (checked).
3D shapes (plates = central planes through one edge each, the fins of #87) are tested
  (i) against the walls of the matching 3D figure:
      icosahedral: 15 mirrors; cross walls parallel to opposite faces of the dodecahedron (6, normals 5-fold), icosahedron (10,
      normals 3-fold); the rhombic triacontahedron's face-parallel sections are the 15 mirrors themselves;
      octahedral: 9 mirrors; cross walls parallel to opposite faces of the octahedron (4, normals 3-fold); the cube's and the rhombic
      dodecahedron's face-parallel sections are mirrors themselves;
  (ii) where natural, against the 600-cell walls seen in the 3D central section d-perp that carries the shape's frame:
      wall W (normal w) meets d-perp in the plane with normal = w projected; a plate is in it iff its spanning vectors are orthogonal to w.
      For central sections of the 600-cell or 120-cell this is FORCED (each 2-face of either spans a mirror), so (ii) is a consistency
      check there; for GET it is a real test.
Exact: Q(sqrt5) as a + b phi (Fraction pairs, echo_lib.Q5): every zero decided exactly; a nonzero is certified when the float value
exceeds 1e-6 (rounding error < 1e-11 at these sizes, asserted), otherwise decided exactly. A second, independent pass in sympy
(as walls_exact.py) re-decides every (plate, wall) pair of the shapes with at most ~250 plates and must agree.
The octahedral Goldberg GP(2,0) polar lives in Q(sqrt2) and is done in sympy only.
Sources of coordinates (read, not re-derived): S5 orbits and the 600-/120-cell from ../../2026-11-15-echo-shapes/scripts/shadow_echoes.py;
remaining-silence sets from ../../2026-11-16-remaining-silences/data/remaining-silences.json (indices into the census universes of
../../2026-11-15-hidden-zeros-h4/scripts/hz_core.py); GET A, GET B, the triacontahedron and the flip-search surfaces from
../../2026-11-15-grunbaum-k10/data/search6.json; GP(2,0) from the echo-shapes README (cube [-1,1]^3 cut by |x| + |y| <= sqrt2).
Usage: walls_others.py out.json [--pilot]"""
import sys, os, json, time, itertools, io, contextlib, runpy
import numpy as np
from fractions import Fraction as Fr
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ST, '2026-11-15-echo-shapes', 'scripts'))
sys.path.insert(0, os.path.join(ST, '2026-11-15-hidden-zeros-h4', 'scripts'))
_argv = sys.argv; sys.argv = ['shadow_echoes.py', 'unused.json']
import shadow_echoes as SE            # cell600, cell120, s5_orbits, edges4, basis_perp, hull4_dirs (no output at import)
sys.argv = _argv
from echo_lib import Q5, q5, PHI, dot, vsub, vadd, vscale, to_np, hull3, fvec, face_census
import hz_core
OUT = sys.argv[1]; PILOT = '--pilot' in sys.argv
T0 = time.time(); FAILS = []; RES = []
def check(c, msg):
    print(('CHECK ok   ' if c else 'CHECK FAIL ') + msg, flush=True)
    if not c: FAILS.append(msg)
def log(*a): print(*a, flush=True)
Z = Q5(0)

# ------------------------------------------------------------------ exact helpers
def canon_dir(v):
    """exact key of the line through v: divide by the first nonzero coordinate"""
    for x in v:
        if not x.iszero(): return tuple((y/x).key() for y in v)
    raise ValueError('zero vector')
def dirs_of(V):
    out = {}
    for v in V: out.setdefault(canon_dir(v), v)
    return list(out.values())
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]))
def gcross4(a, b, c):
    """vector orthogonal to a, b, c in R^4 (cofactors)"""
    out = []
    for i in range(4):
        cols = [j for j in range(4) if j != i]
        m = [[r[j] for j in cols] for r in (a, b, c)]
        out.append(det3(m) * (1 if i % 2 == 0 else -1))
    return tuple(out)
def vfloat(V): return np.array([[float(x) for x in v] for v in V])

# ------------------------------------------------------------------ classification (Q5 pass)
def classify(plates, walls):
    """plates: list of lists of exact spanning vectors (relative to the centre); walls: list of (kind, [normals]).
    Returns per plate the first kind with a normal orthogonal to every spanning vector (exact), else None."""
    out = []
    Wf = [(k, vfloat(N), N) for k, N in walls]
    big = max(1.0, max(np.abs(vfloat(pl)).max() for pl in plates), max(np.abs(F).max() for _, F, _ in Wf if len(F)))
    assert big < 1e3, big                                    # keeps float rounding < 1e-11, so |value| > 1e-6 certifies nonzero
    for pl in plates:
        Pf = vfloat(pl); hit = None
        for k, F, N in Wf:
            if not len(F): continue
            D = np.abs(Pf @ F.T).max(0)                          # per normal: worst spanning vector
            for j in np.nonzero(D < 1e-6)[0]:
                if all(dot(v, N[j]).iszero() for v in pl): hit = k; break
            if hit: break
        out.append(hit)
    return out

# ------------------------------------------------------------------ independent sympy pass
R5 = sp.sqrt(5); SPHI = (1 + R5)/2
def s_(x): return sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator)*SPHI
def svec(v): return [s_(x) for x in v]
def sym_classify(plates, walls):
    out = []
    Wf = [(k, vfloat(N), [svec(n) for n in N]) for k, N in walls]
    for pl in plates:
        Pf = vfloat(pl); Ps = [svec(v) for v in pl]; hit = None
        for k, F, Ns in Wf:
            for j, n in enumerate(Ns):
                vals = np.abs(Pf @ F[j])
                order = np.argsort(-vals)                         # try the likeliest nonzero first: one nonzero suffices
                zero = True
                for i in order:
                    if sp.expand(sum(a*b for a, b in zip(Ps[i], n))) != 0: zero = False; break
                if zero: hit = k; break
            if hit: break
        out.append(hit)
    return out

def tally(cls, kinds):
    t = {k: 0 for k in kinds}; t['none'] = 0
    for c in cls: t[c if c else 'none'] += 1
    return t

def record(name, family, role, plates, walls, comparison, extra=None, sym=True):
    cls = classify(plates, walls)
    t = tally(cls, [k for k, _ in walls])
    rec = {'shape': name, 'family': family, 'role': role, 'comparison': comparison, 'plates': len(plates), 'tally': t}
    if extra: rec.update(extra)
    if sym:
        cs = sym_classify(plates, walls); rec['sympy_agrees'] = cs == cls
        check(cs == cls, f'{name} [{comparison}]: sympy pass agrees with the Q5 pass')
    RES.append(rec)
    log(f'RESULT {name} [{comparison}] {role}: plates {len(plates)} ' + ' '.join(f'{k} {v}' for k, v in t.items())
        + (f' | {extra}' if extra else ''))
    return rec

# ------------------------------------------------------------------ 4D: 2-faces and plates
def faces2_fast(Vf, dec=7):
    from scipy.spatial import ConvexHull
    h = ConvexHull(Vf); eqs = {}
    for e, s in zip(h.equations, h.simplices):
        eqs.setdefault(tuple(np.round(e, dec) + 0.0), set()).update(s.tolist())
    fac = [sorted(x) for x in eqs.values()]
    M = np.zeros((len(fac), len(Vf)), np.int32)
    for i, f in enumerate(fac): M[i, f] = 1
    C = M @ M.T; out = set()
    for i, j in zip(*np.nonzero(np.triu(C, 1) >= 3)):
        c = sorted(set(fac[i]) & set(fac[j]))
        if np.linalg.matrix_rank(Vf[c] - Vf[c].mean(0), tol=1e-7) == 2: out.add(tuple(c))
    return fac, sorted(out)

def plates4(V, Vf):
    """V exact (in R^4 or sum-zero R^5), Vf float 4D coordinates. Returns plates (one per distinct central hyperplane; exact
    coplanarity of every 2-face with the centre checked), number of 2-faces, and the corner counts."""
    fac, rid = faces2_fast(Vf); planes = {}; bad = 0
    for c in rid:
        M = Vf[list(c)]; _, s, vt = np.linalg.svd(M)
        if s[2] < 1e-7: bad += 1; continue                     # 2-face whose plane contains the centre: no plate
        n = vt[3]; n = n * np.sign(n[np.argmax(np.abs(n) > 1e-9)])
        planes.setdefault(tuple(np.round(n, 7) + 0.0), set()).update(c)
    plates = []
    for key, idx in planes.items():
        idx = sorted(idx); pl = [V[i] for i in idx]; plates.append(pl)
    return plates, len(rid), bad, len(fac)

def exact_coplanar(pl):
    """rank of the spanning vectors is exactly 3 (4D) or 2 (3D)"""
    if len(pl[0]) == 3:
        a = pl[0]; b = next(v for v in pl[1:] if any(not x.iszero() for x in vcross(a, v)))
        n = vcross(a, b); return all(dot(v, n).iszero() for v in pl)
    for a, b, c in itertools.combinations(pl, 3):
        n = gcross4(a, b, c)
        if any(not x.iszero() for x in n): return all(dot(v, n).iszero() for v in pl)
    return False
def plane2_exact(pl, d):
    """3D plate given by 4D vectors inside d-perp: all in d-perp and in one 2-plane (exact)"""
    if not all(dot(v, d).iszero() for v in pl): return False
    for a, b in itertools.combinations(pl, 2):
        n = gcross4(d, a, b)
        if any(not x.iszero() for x in n): return all(dot(v, n).iszero() for v in pl)
    return False
def vcross(a, b): return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

# ------------------------------------------------------------------ the 600-cell wall system, standard frame
P6 = SE.cell600(); P12 = SE.cell120()
check(len(P6) == 120 and len(P12) == 600, '600-cell 120 corners, 120-cell 600 corners (shadow_echoes coordinates)')
M60 = dirs_of(P6); check(len(M60) == 60, f'60 H4 mirror normals ({len(M60)})')
cc = SE.hull4_dirs(P6); C300 = dirs_of(cc); check(len(cc) == 600 and len(C300) == 300, f'600 cells, 300 cell-parallel cross walls ({len(C300)})')
c12 = SE.hull4_dirs(P12); check(len(c12) == 120, '120-cell: 120 cells')
same_m = {canon_dir(v) for v in dirs_of(c12)} == {canon_dir(v) for v in M60}
log(f'standard 120-cell (shadow_echoes) dual-aligned with the standard 600-cell: {same_m} (if not, it carries its own copy of the system)')
W4 = [('mirror', M60), ('cross', C300)]
M60b = dirs_of(c12); C300b = dirs_of(P12)
check(len(M60b) == 60 and len(C300b) == 300, '120-cell walls: 60 mirrors (cell centres = corners of its dual 600-cell), 300 cross walls (its corners)')
W4b = [('mirror', M60b), ('cross', C300b)]
log(f'PROGRESS 0.05 wall systems ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ 4D part A: S5 orbits (5-coordinate frame, as walls.py)
orb, ncl = SE.s5_orbits(); check(ncl == 120, 'S5 frame: closure of C1 = 120 points')
P5 = orb['C1'] + orb['C2'] + orb['C3'] + orb['C4'] + orb['C5']
Qb = np.linalg.qr(np.vstack([np.ones(5), np.eye(5)[:4]]).T)[0][:, 1:5]
def f4(V): return vfloat(V) @ Qb
from scipy.spatial import ConvexHull
M60s = dirs_of(P5)
hP = ConvexHull(f4(P5)); cc5 = [tuple(sum((P5[i][t] for i in s), Z) for t in range(5)) for s in hP.simplices]
C300s = dirs_of(cc5); check(len(M60s) == 60 and len(C300s) == 300 and len(hP.simplices) == 600, 'S5 frame: 60 mirrors, 300 cross walls')
W5 = [('mirror', M60s), ('cross', C300s)]
def run4(name, family, role, V, Vf, walls, sym=True, expect=None):
    plates, nrid, bad, nfac = plates4(V, Vf)
    ok = all(exact_coplanar(pl) for pl in plates); check(ok, f'{name}: every plate exactly coplanar with the centre')
    r = record(name, family, role, plates, walls, '600-cell walls (4D)', {'cells': nfac, '2-faces': nrid, '2-faces through centre': bad}, sym=sym)
    if expect is not None: check(r['tally'] == expect, f'{name}: expected {expect}')
    return r
P2 = PHI*PHI
def cen(v): m = sum(v, Z)/5; return tuple(x - m for x in v)
def s5orbit(base): return [cen(tuple(t)) for t in sorted(set(itertools.permutations(base)), key=lambda t: tuple(x.key() for x in t))]
shapes4 = [('solid A (C1, perms (phi^2,phi^2,phi^2,phi,0))', 'S5 orbits', 'positive control', orb['C1'], {'mirror': 30, 'cross': 0, 'none': 0}),
           ('solid B (C4, perms (phi^2,phi^2,1,1,0))', 'S5 orbits', 'positive control', orb['C4'], {'mirror': 40, 'cross': 40, 'none': 0}),
           ('R = C3, third 20-point twisted class of 2I', 'S5 orbits', 'test', orb['C3'], None)]
if not PILOT:
    shapes4 += [('-A (C2)', 'S5 orbits', 'test (congruent to A by -1)', orb['C2'], {'mirror': 30, 'cross': 0, 'none': 0}),
                ('-B (C5)', 'S5 orbits', 'test (congruent to B by -1)', orb['C5'], {'mirror': 40, 'cross': 40, 'none': 0}),
                ('ordinary orbit (phi^2,phi^2,phi^2,3/2,0)', 'S5 orbits', 'negative control', s5orbit((P2, P2, P2, Q5(Fr(3, 2)), Z)), None),
                ('ordinary orbit (phi^2,phi^2,6/5,6/5,0)', 'S5 orbits', 'negative control', s5orbit((P2, P2, Q5(Fr(6, 5)), Q5(Fr(6, 5)), Z)), None)]
for name, fam, role, V, exp in shapes4:
    run4(name, fam, role, V, f4(V), W5, expect=exp)
# reproduce walls_exact.log per 2-face for A and B: plates = 2-faces there
check(RES[0]['2-faces'] == 30 and RES[1]['2-faces'] == 80, 'A has 30 and B 80 2-faces, one plate each (walls_exact.log)')
log(f'PROGRESS 0.20 S5 orbits ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ 4D part B: remaining-silence sets (census universes)
Xh = hz_core.cell600()                                       # (120,4,2) integer pairs a + b phi, scaled by 2
def hz_pt(r, s): return tuple(Q5(Fr(int(r[c, 0]), s), Fr(int(r[c, 1]), s)) for c in range(r.shape[0]))
X6 = [hz_pt(Xh[i], 2) for i in range(120)]
check({canon_dir(v) for v in X6} == {canon_dir(v) for v in M60} and all(dot(v, v) == 1 for v in X6), 'census 600-cell = the same unit 600-cell (same frame)')
# 120-cell of the census: one corner per tetrahedral cell, phi^-2 * (sum of the 4 corners), cells sorted (as hz_universes.cell120_from)
a_, b_ = hz_core.ip_pairs(Xh, Xh); adj = (a_ == 0) & (b_ == 2); nb = [set(np.nonzero(adj[i])[0]) for i in range(120)]
tets = set()
for i in range(120):
    for j in nb[i]:
        for k in nb[i] & nb[j]:
            for l in nb[i] & nb[j] & nb[k]: tets.add(tuple(sorted((i, j, k, l))))
tets = sorted(tets); check(len(tets) == 600, 'census 120-cell: 600 cells of the 600-cell')
IP2 = Q5(2, -1)
Y6 = [tuple(IP2*sum((X6[i][t] for i in T_), Z)*2 for t in range(4)) for T_ in tets]   # scale is irrelevant for walls
check({canon_dir(v) for v in Y6} == {canon_dir(v) for v in C300}, 'census 120-cell corners lie on the 600-cell cross-wall normals (same wall system)')
RS = json.load(open(os.path.join(ST, '2026-11-16-remaining-silences', 'data', 'remaining-silences.json')))
lab = {(30, 15): '[C3 x C5] 30-point union', (60, 60): '[C3 x C10] 60-point union', (30, 50): '[C5 x C5] 30-point union',
       (60, 200): '[C5 x C5].2 60-point union', (240, 120): '[C5 x 2T] 240-point union'}
seen = {}
cases = [c for c in RS['cases'] if c['universe'] in ('600-cell', '120-cell')]
if PILOT: cases = cases[:1]
for c in cases:
    key = (c['size'], c['stab_order']); seen[key] = seen.get(key, 0) + 1
    U = X6 if c['universe'] == '600-cell' else Y6
    V = [U[i] for i in c['rep']]
    run4(f"{c['universe']} {lab[key]} ({'abcd'[seen[key]-1]})", 'remaining silences', 'test', V, vfloat(V), W4, sym=len(V) <= 60)
rng = np.random.default_rng(20261116)
BASE = {}
if not PILOT:
    # baseline, not a must-fail control: random subsets of the same polytope (A, B, R and the silence sets are all such subsets)
    for size, U, un, n in ((20, X6, '600-cell', 100), (30, X6, '600-cell', 100), (60, X6, '600-cell', 100), (240, Y6, '120-cell', 10)):
        rows = []
        for t in range(n):
            pick = sorted(rng.choice(len(U), size, replace=False).tolist()); V = [U[i] for i in pick]
            plates, nrid, bad, nfac = plates4(V, vfloat(V))
            if bad: continue                                     # hull with a 2-face through the centre: skip
            tl = tally(classify(plates, W4), ['mirror', 'cross']); rows.append((len(plates), tl['mirror'], tl['cross'], tl['none']))
        R_ = np.array(rows); key = f'random {size}-subsets of the {un}'
        BASE[key] = {'samples': len(rows), 'mean plates': float(R_[:, 0].mean()), 'mean share in no wall': float((R_[:, 3] / R_[:, 0]).mean()),
                     'share of samples with every plate a wall': float((R_[:, 3] == 0).mean()),
                     'mean share mirror': float((R_[:, 1] / R_[:, 0]).mean()), 'mean share cross': float((R_[:, 2] / R_[:, 0]).mean())}
        log(f'BASELINE {key}: {BASE[key]}')
        check(len(rows) >= n // 2, f'{key}: at least half the samples usable ({len(rows)}/{n})')
log(f'PROGRESS 0.45 remaining-silence sets ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ 3D frames inside d-perp
def frame(d, kind, mirrors=None):
    """restricted mirrors (H4 mirrors containing d) and the axes where they meet, all exact in R^4 (inside d-perp)"""
    Mr = [m for m in (mirrors or M60) if dot(m, d).iszero()]
    lines = {}
    for m1, m2 in itertools.combinations(Mr, 2):
        L = gcross4(d, m1, m2); k = canon_dir(L)
        if k not in lines: lines[k] = (L, sum(1 for m in Mr if dot(m, L).iszero()))
    by = {}
    for L, cnt in lines.values(): by.setdefault(cnt, []).append(L)
    if kind == 'I':
        check(len(Mr) == 15 and sorted((k, len(v)) for k, v in by.items()) == [(2, 15), (3, 10), (5, 6)],
              f'icosahedral frame: 15 mirrors; axes 15 two-fold, 10 three-fold, 6 five-fold ({[(k, len(v)) for k, v in sorted(by.items())]})')
        figw = [('mirror', Mr), ('cross dodecahedron', by.get(5, [])), ('cross icosahedron', by.get(3, []))]
        return figw, by
    check(len(Mr) == 6 and sorted((k, len(v)) for k, v in by.items()) == [(2, 3), (3, 4)],
          f'tetrahedral stabiliser: 6 mirrors; 3 two-fold (4-fold of O_h), 4 three-fold axes ({[(k, len(v)) for k, v in sorted(by.items())]})')
    figw = [('mirror', Mr + by.get(2, [])), ('cross octahedron', by.get(3, []))]   # O_h: 6 + 3 mirrors
    return figw, by

dI = tuple(Q5(x) for x in (1, 0, 0, 0)); check(any(vfloat([v])[0].tolist() == [1, 0, 0, 0] for v in P6), 'd = (1,0,0,0) is a 600-cell corner')
figI, axI = frame(dI, 'I')
dO = sorted(C300, key=lambda v: [x.key() for x in v])[0]; figO, axO = frame(dO, 'O')

def edges3(Pts, d):
    """edges of the 3D hull of exact points inside the hyperplane x.d = t: float hull, exact points"""
    B = SE.basis_perp(d, 4); X = vfloat(Pts) @ B; H = hull3(X)
    E = set()
    for f in H['faces']:
        for t in range(len(f)): E.add(tuple(sorted((f[t-1], f[t]))))
    return sorted(E), H
def plates3(Pts, E, c):
    planes = {}; degen = 0
    for i, j in E:
        a = vsub(Pts[i], c); b = vsub(Pts[j], c); af, bf = vfloat([a, b])
        if np.linalg.matrix_rank(np.vstack([af, bf]), tol=1e-9) < 2: degen += 1; continue
        Q_ = np.linalg.qr(np.vstack([af, bf]).T)[0]; key = tuple(np.round((Q_ @ Q_.T).ravel(), 7) + 0.0)
        planes.setdefault(key, []).append((a, b))
    plates = []
    for key, ab in planes.items():
        vs = []
        for a, b in ab: vs += [a, b]
        plates.append(vs)
    return plates, degen

def slice_of(S, E4, d, t):
    s = [dot(x, d) - t for x in S]; pts = {}
    for i, x in enumerate(S):
        if s[i].iszero(): pts[tuple(y.key() for y in x)] = x
    for i, j in E4:
        if s[i].sign()*s[j].sign() < 0:
            u = s[i]/(s[i] - s[j]); p = tuple(a + u*(b - a) for a, b in zip(S[i], S[j])); pts[tuple(y.key() for y in p)] = p
    return list(pts.values())

def induced(W, d):
    """4D walls seen inside d-perp: drop the wall whose normal is d itself (its hyperplane IS d-perp and would hold every plate)"""
    k = canon_dir(d); return [(kind, [w for w in N if canon_dir(w) != k]) for kind, N in W]
def run_cut(name, role, S, E4, d, t, figw, figname, expect_f=None, sym=True, w4=None):
    Pts = slice_of(S, E4, d, t); E, H = edges3(Pts, d); fv = fvec(H)
    if expect_f: check(fv == expect_f, f'{name}: f-vector {fv} = {expect_f} (echo-shapes README)')
    c = vscale(t/dot(d, d), d)
    plates, degen = plates3(Pts, E, c)
    check(all(plane2_exact(pl, d) for pl in plates), f'{name}: every plate exactly one plane through the centre')
    extra = {'f-vector': fv, 'faces': {str(k): v for k, v in face_census(H).items()}, 'edges': len(E), 'edges through centre': degen, 'height': str(t)}
    record(name, 'echo shapes', role, plates, figw, f'3D figure walls ({figname})', extra, sym=sym)
    record(name, 'echo shapes', role, plates, induced(w4 or W4, d), '600-cell walls through the section', extra, sym=False)

log(f'PROGRESS 0.50 frames ({time.time()-T0:.0f}s)')
# ------------------------------------------------------------------ echo shapes: central cuts and off-centre controls
E600 = SE.edges4(P6); check(len(E600) == 720, '600-cell: 720 edges')
run_cut('600-cell central cut across a vertex axis', 'test', P6, E600, dI, Z, figI, 'icosahedral', (42, 120, 80))
if not PILOT:
    run_cut('600-cell slice across a vertex axis at height 3/10', 'negative control', P6, E600, dI, Q5(Fr(3, 10)), figI, 'icosahedral')
    E120 = SE.edges4(P12); check(len(E120) == 1200, '120-cell: 1200 edges')
    dI12 = sorted(M60b, key=lambda v: [x.key() for x in v])[0]; figI12, _ = frame(dI12, 'I', M60b)   # a 120-cell cell axis
    h12 = max(dot(x, dI12) for x in P12)
    run_cut('120-cell central cut across a cell axis', 'test', P12, E120, dI12, Z, figI12, 'icosahedral', (80, 120, 42), w4=W4b)
    run_cut('120-cell slice across a cell axis at 3/10 of the top', 'negative control', P12, E120, dI12, h12*Q5(Fr(3, 10)), figI12, 'icosahedral', w4=W4b)
    run_cut('600-cell central cut across a cell axis', 'test', P6, E600, dO, Z, figO, 'octahedral', (84, 240, 158))
    h6 = max(dot(x, dO) for x in P6)
    run_cut('600-cell slice across a cell axis at 3/10 of the top', 'negative control', P6, E600, dO, h6*Q5(Fr(3, 10)), figO, 'octahedral')
    dO12 = sorted(C300b, key=lambda v: [x.key() for x in v])[0]; figO12, _ = frame(dO12, 'O', M60b)   # a 120-cell corner axis
    h12v = max(dot(x, dO12) for x in P12)
    run_cut('120-cell central cut across a vertex axis', 'test', P12, E120, dO12, Z, figO12, 'octahedral', (78, 120, 44), w4=W4b)
    run_cut('120-cell slice across a vertex axis at 3/10 of the top', 'negative control', P12, E120, dO12, h12v*Q5(Fr(3, 10)), figO12, 'octahedral', w4=W4b)
    # positive control for the octahedral frame: the octahedron on the three 4-fold axes (its edges' plates are the coordinate mirrors)
    ax4 = axO[2]; octa = [vscale(Q5(s), a) for a in ax4 for s in (1, -1)]
    Eo = [(i, j) for i, j in itertools.combinations(range(6), 2) if dot(octa[i], octa[j]).iszero()]
    check(len(Eo) == 12, 'octahedron: 12 edges')
    pl_o, _ = plates3(octa, Eo, (Z, Z, Z, Z))
    record('octahedron on the 4-fold axes', 'echo shapes', 'positive control', pl_o, figO, '3D figure walls (octahedral)', {'edges': len(Eo)})
log(f'PROGRESS 0.70 echo cuts ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ GET (and its family) placed in the icosahedral frame
S6 = json.load(open(os.path.join(ST, '2026-11-15-grunbaum-k10', 'data', 'search6.json')))
T12 = json.load(open(os.path.join(ST, '2026-11-15-grunbaum-k10', 'data', 'tile12.json')))
check([r['tiles'] for r in T12['results']][:2] == [True, True], 'GET A, GET B = candidates 0 and 1 of search6.json (tile12: both tile)')
AX = [(1, 'p', 0), (-1, 'p', 0), (0, 1, 'p'), (0, -1, 'p'), ('p', 0, 1), ('-p', 0, 1)]
def qq(x): return PHI if x == 'p' else (-PHI if x == '-p' else Q5(x))
AXq = [tuple(qq(x) for x in a) for a in AX]
# similarity Phi: R^3 (GET frame) -> d-perp, sending the six 5-fold axes to 5-fold axes of the frame (600-cell corners at x0 = phi/2)
ico = [(Z,) + v[1:] for v in P6 if v[0] == PHI/2]; check(len(ico) == 12, '12 corners at height phi/2 (an icosahedron in d-perp)')
A3 = [AXq[0], AXq[2], AXq[4]]
def inv3(M):
    D = det3(M); C = [[None]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            m = [[M[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
            C[j][i] = (m[0][0]*m[1][1] - m[0][1]*m[1][0]) * (1 if (i + j) % 2 == 0 else -1) / D
    return C
Am = [[A3[c][r] for c in range(3)] for r in range(3)]; Ai = inv3(Am)
Phi = None; s_ratio = dot(ico[0], ico[0]) / dot(A3[0], A3[0])
for b0, b1, b2 in itertools.permutations(ico, 3):
    if not all((dot(x, y) - s_ratio*dot(u, w)).iszero() for (x, u), (y, w) in itertools.combinations(zip((b0, b1, b2), A3), 2)): continue
    Bm = [[b[r + 1] for b in (b0, b1, b2)] for r in range(3)]
    Ph = [[sum((Bm[r][k]*Ai[k][c] for k in range(3)), Z) for c in range(3)] for r in range(3)]
    def ap(v, Ph=Ph): return (Z,) + tuple(sum((Ph[r][c]*v[c] for c in range(3)), Z) for r in range(3))
    icok = {canon_dir(v) for v in ico}
    if all(canon_dir(ap(a)) in icok for a in AXq): Phi = ap; break
check(Phi is not None, 'similarity found sending all six GET axes onto 5-fold axes of the frame')
E3 = [tuple(Q5(int(i == j)) for j in range(3)) for i in range(3)]
ok = Phi is not None and all((dot(Phi(u), Phi(w)) - s_ratio*dot(u, w)).iszero() for u in E3 for w in E3)
check(ok, 'Phi is an exact similarity (Phi^T Phi = s I)')
def surf_edges(faces):
    E = set()
    for p, a, b, sgn in faces:
        p = tuple(p); ea = tuple(int(i == a) for i in range(6)); eb = tuple(int(i == b) for i in range(6))
        E |= {(p, a), (p, b), (tuple(np.add(p, eb).tolist()), a), (tuple(np.add(p, ea).tolist()), b)}
    return sorted(E)
def pos6(p, ax=None): ax = ax or AXq; return tuple(sum((ax[i][r]*Q5(p[i]) for i in range(6)), Z) for r in range(3))
def run_surface(name, role, faces, centre6, figw, sym=True, centre_label='centre of the parent triacontahedron', expect=None, ax=None):
    ax = ax or AXq; E = surf_edges(faces); O = pos6(centre6, ax)
    pts = []
    for p, a in E:
        P0 = vsub(pos6(p, ax), O); P1 = vadd(P0, ax[a]); pts.append((Phi(P0), Phi(P1)))
    planes = {}; degen = 0
    for a, b in pts:
        af, bf = vfloat([a, b])
        if np.linalg.matrix_rank(np.vstack([af, bf]), tol=1e-9) < 2: degen += 1; continue
        Q_ = np.linalg.qr(np.vstack([af, bf]).T)[0]; planes.setdefault(tuple(np.round((Q_ @ Q_.T).ravel(), 7) + 0.0), []).extend([a, b])
    plates = list(planes.values())
    check(all(plane2_exact(pl, dI) for pl in plates), f'{name}: every plate exactly one plane through the centre')
    ex = {'edges': len(E), 'edges through centre': degen, 'centre': centre_label}
    r1 = record(name, 'GET', role, plates, figw, '3D figure walls (icosahedral)', ex, sym=sym)
    r2 = record(name, 'GET', role, plates, induced(W4, dI), '600-cell walls through its vertex-axis central section', ex, sym=False)
    if expect: check(r1['tally'] == expect, f'{name}: expected {expect}')
    return r1, r2
def vmean(faces):
    V = set()
    for p, a, b, s in faces:
        for da, db in ((0, 0), (1, 0), (0, 1), (1, 1)):
            V.add(tuple(p[i] + da*(i == a) + db*(i == b) for i in range(6)))
    return [sum(Fr(v[i]) for v in V)/len(V) for i in range(6)], len(V)
rt = S6['examples_noncoplanar'][0]; check(rt['depth'] == 0, 'depth-0 surface = the rhombic triacontahedron')
O6, nv = vmean(rt['faces']); check(nv == 32, 'triacontahedron: 32 corners')
run_surface('rhombic triacontahedron', 'positive control', rt['faces'], O6, figI, expect={'mirror': 15, 'cross dodecahedron': 0, 'cross icosahedron': 0, 'none': 0})
cands = S6['candidates_rank_le_3']
for idx, nm in ((0, 'GET A'), (1, 'GET B')):
    f = cands[idx]['faces']; check(len(f) == 30, f'{nm}: 30 faces')
    run_surface(nm, 'test', f, O6, figI)
    if not PILOT:
        Ov, _ = vmean(f); run_surface(nm + ' (own corner centroid)', 'test, other centre', f, Ov, figI, centre_label='its own corner centroid')
        # perturbed shape of the same family: the same surface on the six-axis star with phi replaced by 8/5 (as the ordinary S5 orbits
        # replace phi by 3/2), compared with the same golden frame
        run_surface(nm + ' on the star with phi -> 8/5', 'negative control', f, O6, figI, sym=False,
                    ax=[tuple(Q5(Fr(8, 5)) if x == 'p' else (Q5(Fr(-8, 5)) if x == '-p' else Q5(x)) for x in a) for a in AX])
if not PILOT:
    for idx in range(2, len(cands)):
        run_surface(f'k = 10 candidate {idx} (undecided tiler, depth {cands[idx]["depth"]})', 'test (not certified)', cands[idx]['faces'], O6, figI, sym=False)
FLIP = S6['examples_noncoplanar'][1:] if not PILOT else S6['examples_noncoplanar'][1:60:20]
for k, ex in enumerate(FLIP, 1):
    run_surface(f'flip-search surface #{k} (depth {ex["depth"]})', 'same family, ordinary (flip search)', ex['faces'], O6, figI, sym=False)
log(f'PROGRESS 0.90 GET ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ octahedral GP(2,0) polar, Q(sqrt2), sympy only
def gp20(tval):
    """cube [-1,1]^3 cut by the 12 planes +-x +-y <= t (and cyclic): exact corners from plane triples, float hull for edges"""
    planes = [((s, 0, 0), 1) for s in (1, -1)] + [((0, s, 0), 1) for s in (1, -1)] + [((0, 0, s), 1) for s in (1, -1)]
    for i, j in ((0, 1), (1, 2), (0, 2)):
        for si, sj in itertools.product((1, -1), repeat=2):
            n = [0, 0, 0]; n[i] = si; n[j] = sj; planes.append((tuple(n), tval))
    pts = {}
    for p1, p2, p3 in itertools.combinations(planes, 3):
        M = sp.Matrix([p1[0], p2[0], p3[0]])
        if M.det() == 0: continue
        x = M.LUsolve(sp.Matrix([p1[1], p2[1], p3[1]])); x = [sp.nsimplify(sp.expand(v)) for v in x]
        if all(sp.simplify(sum(a*b for a, b in zip(n, x)) - c) <= 0 for n, c in planes):
            pts[tuple(sp.srepr(v) for v in x)] = x
    P = list(pts.values()); H = hull3(np.array([[float(v) for v in p] for p in P]))
    E = set()
    for f in H['faces']:
        for t in range(len(f)): E.add(tuple(sorted((f[t-1], f[t]))))
    return P, sorted(E), H
OH = {'mirror': [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, -1, 0), (0, 1, 1), (0, 1, -1), (1, 0, 1), (1, 0, -1)],
      'cross octahedron': [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]}
def run_gp(name, role, tval, expect_f=None, expect=None):
    P, E, H = gp20(tval); fv = fvec(H)
    if expect_f: check(fv == expect_f, f'{name}: f-vector {fv} = {expect_f}')
    planes = {}
    for i, j in E:
        n = sp.Matrix(P[i]).cross(sp.Matrix(P[j])); n = [sp.nsimplify(sp.expand(v)) for v in n]
        k = next(v for v in n if v != 0); key = tuple(sp.srepr(sp.nsimplify(sp.radsimp(v/k))) for v in n)
        planes.setdefault(key, (P[i], P[j]))
    t = {'mirror': 0, 'cross octahedron': 0, 'none': 0}
    for a, b in planes.values():
        hit = 'none'
        for kind, N in OH.items():
            if any(sp.expand(sum(x*y for x, y in zip(a, n))) == 0 and sp.expand(sum(x*y for x, y in zip(b, n))) == 0 for n in N): hit = kind; break
        t[hit] += 1
    RES.append({'shape': name, 'family': 'echo shapes', 'role': role, 'comparison': '3D figure walls (octahedral), sympy in Q(sqrt2)',
                'plates': len(planes), 'tally': t, 'f-vector': fv, 'edges': len(E)})
    log(f'RESULT {name} [octahedral, Q(sqrt2)] {role}: plates {len(planes)} ' + ' '.join(f'{k} {v}' for k, v in t.items()) + f' | f {fv}')
    if expect: check(t == expect, f'{name}: expected {expect}')
run_gp('octahedral GP(2,0) polar (cube cut at sqrt2)', 'test', sp.sqrt(2), (32, 48, 18))
if not PILOT:
    run_gp('cube cut at 3/2 (same family, ordinary)', 'negative control', sp.Rational(3, 2), (32, 48, 18))
    run_gp('cube (cut at 2 is inactive: 12 edges)', 'positive control', sp.Integer(3), (8, 12, 6), {'mirror': 6, 'cross octahedron': 0, 'none': 0})
log(f'PROGRESS 1.00 done ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ controls that must pass / fail
def find(name, comp=None): return [r for r in RES if r['shape'] == name and (comp is None or r['comparison'].startswith(comp))]
negs = [r for r in RES if r['role'] == 'negative control' and r['comparison'].startswith(('600-cell walls (4D)', '3D figure'))]
neg_ok = all(r['tally']['none'] > r['plates'] / 2 for r in negs)
log('NEGATIVE CONTROLS (must be mostly no wall): ' + '; '.join(f"{r['shape']} [{r['comparison'][:12]}] none {r['tally']['none']}/{r['plates']}" for r in negs))
if not PILOT: check(len(negs) >= 6 and neg_ok, f'every negative control has most plates in no wall ({sum(r["tally"]["none"] > r["plates"]/2 for r in negs)}/{len(negs)})')
forced = [r for r in RES if r['comparison'] == '600-cell walls through the section' and r['height'] == '0']
check(all(r['tally']['none'] == 0 for r in forced), 'central sections of the 600-/120-cell: every plate in an induced 600-cell wall (forced, consistency)')
json.dump({'results': RES, 'baselines': BASE, 'fails': FAILS, 'pilot': PILOT, 'seconds': time.time() - T0}, open(OUT, 'w'), indent=1, default=str)
fam = [r for r in RES if r['role'].startswith('same family') and r['comparison'].startswith('3D figure')]
log(f'GET FAMILY: {len(fam)} ordinary flip-search surfaces; all plates in mirror walls for {sum(r["tally"]["none"] == 0 for r in fam)}; '
    f'plates per surface {sorted(set(r["plates"] for r in fam))}')
log(f'{len(RES)} results, {len(FAILS)} failed checks, {time.time()-T0:.0f} s')
print('FINAL ok' if not FAILS else 'FINAL FAIL ' + '; '.join(FAILS))
