# DICTO · dictospheres.com — math-data dataset VERSION 3 builder (2026-10-27). Created by DICTO. Licence CC BY-SA 4.0.
# Adds twelve named solids of DICTO's papers #55, #56, #57 and #59:
#   #55 David and Goliath (Q): Goliath (convex hull of Jessen's icosahedron) and David (a tetragonal disphenoid), the A15 power cells at 3/4;
#   #56 Sonsam and Lahdeli: Sonsam and Lahdeli (the twinned octet's cells at the equal-volume point, in Q(t), t the root of an
#       irreducible cubic), Ian Dury (5/24) and Blockhead (3/8) (Q);
#   #57 The Rule of Halves (Q): Chucky (-3/8) and Fang (5/24), the Janus c/h pieces of ABAC, and the Triskelion Tetrahedron (5/24);
#   #59 The Icosaxes Hexa (Q(sqrt5)): Keyaxes, Icosaxes Hexa, Lotus Hexa.
# Geometry is NOT re-derived from the papers' prose: the studies' own exact code is executed (copies in build/sources/, from the
# research branch at commit 41e1213c, files unchanged since 46cf7e09 / 7fbc9b73): exact_a15.py (the #55 cells, Fractions), the census
# engine engine.py + networks.py and stackings.py (#53/#56/#57: the exact power-diagram planes of the holes of any close-packed stacking),
# and, for #59, the #48 study objects already used by build_v2.py (golden_split_exact.py, keyed_polar_exact.py), keyed as in krp-core
# polyhedra/golden-split.js (INTO_BIG = the #48 Tricap taken out, INTO_SMALL = the Tricap mirrored in its base plane, added).
# Writes solids/<slug>.json/.off (+ unit_volume, -unit-volume.off) and build_v3.log.json.
import contextlib, io, itertools, json, os, sys
from fractions import Fraction as Fr
import numpy as np
import mpmath, sympy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
abs_ = lambda x: x if x.sign() >= 0 else -x
SRC = os.path.join(HERE, 'sources'); SOL = os.path.join(HERE, '..', 'solids')
sys.path.insert(0, SRC)
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).', 'version_added': 3}
D55, D56, D57, D59 = '10.5281/zenodo.23632358', '10.5281/zenodo.23635823', '10.5281/zenodo.23647898', '10.5281/zenodo.23677485'
RB = 'research branch (commit 41e1213c)'

def parse_any(s, d):
    e = sympy.expand(sympy.sympify(s, locals={'t': sympy.Symbol('t')}))
    if isinstance(d, tuple) and d[0] == 'alg':
        F = AlgField.get(d[2], d[3], d[4], d[1]); t = sympy.Symbol(d[1])
        cs = [Fr(int(c.p), int(c.q)) for c in reversed(sympy.Poly(e, t).all_coeffs())]
        return RF(cs, F)
    if isinstance(d, tuple):
        k = d[1]; cs = [Fr(0)] * 3; basis = {sympy.Integer(1): 0, sympy.Integer(k) ** sympy.Rational(1, 3): 1, sympy.Integer(k) ** sympy.Rational(2, 3): 2}
        for t, c in e.as_coefficients_dict().items(): cs[basis[t]] += Fr(int(c.p), int(c.q))
        return KC(*cs, k=k)
    a = Fr(0); b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        c = Fr(int(c.p), int(c.q))
        if t == 1: a += c
        elif d > 1 and t == sympy.sqrt(d): b += c
        else: raise ValueError(s)
    return QF(a, b, d)

def emit(slug, meta, V, F, published):
    V, F = canon(V, F)
    meta = dict(meta, **COMMON); meta['published_values'] = published
    r = write_solid(os.path.join(SOL, slug), meta, V, F)
    d = V[0][0].d
    if meta.get('symmetry_label') not in (None, 'auto'): log(r['cls'] == r['label'], f"{slug}: symmetry {r['cls']} order {r['order']} (classified from the solid) vs stated {r['label']}")
    for k, v in published.items():
        if k == 'volume': log(r['vol'] == parse_any(v, d), f"{slug}: volume {fmt(r['vol'])} vs published {v}")
        elif k == 'f_vector': log((r['V'], r['E'], r['F']) == tuple(v), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs published {tuple(v)}")
        elif k == 'faces_by_sides': log({str(a): b for a, b in r['fk'].items()} == v, f"{slug}: faces {r['fk']} vs published {v}")
        elif k == 'squared_edge_lengths': log(set(r['el']) == {parse_any(x, d) for x in v}, f"{slug}: squared edges {[fmt(x) for x in r['el']]} vs published {v}")
        elif k == 'symmetry_order': log(r['order'] == v, f"{slug}: symmetry order {r['order']} vs published {v}")
    log(True, f"{slug}: {r['V']}, {r['E']}, {r['F']} {dict(sorted(r['fk'].items()))}, volume {fmt(r['vol'])}, symmetry {r['cls']} ({r['order']})")
    return V, F, r

def hs_solid(planes):
    """exact solid {x : n.x <= c}; float corner guesses (Chebyshev centre + scipy) solved and tested exactly, then the exact hull."""
    from scipy.optimize import linprog
    from scipy.spatial import HalfspaceIntersection
    Nf = np.array([fv(n) for n, c in planes]); cf = np.array([c.f() for n, c in planes]); nr = np.linalg.norm(Nf, axis=1)
    res = linprog(np.r_[np.zeros(3), -1.0], A_ub=np.c_[Nf, nr], b_ub=cf, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    assert res.status == 0 and res.x[3] > 1e-9, 'empty cell'
    X = HalfspaceIntersection(np.hstack([Nf, -cf[:, None]]), res.x[:3]).intersections
    X = X[np.unique(np.round(X, 8), axis=0, return_index=True)[1]]
    C = []
    for x in X:
        tight = [i for i in np.argsort(np.abs(Nf @ x - cf)) if abs(Nf[i] @ x - cf[i]) < 1e-7 * max(1, nr[i])]
        for tri in itertools.combinations(tight, 3):
            if abs(np.linalg.det(Nf[list(tri)])) > 1e-6: break
        A = [planes[i][0] for i in tri]; b = [planes[i][1] for i in tri]; D = det3(*A)
        C.append(tuple(det3(*[tuple(b[r] if k == col else A[r][k] for k in range(3)) for r in range(3)]) / D for col in range(3)))
    C = list(dict.fromkeys(C))
    assert all((dot(n, c) - h).sign() <= 0 for c in C for n, h in planes), 'corner outside'
    V, F = hull(C)
    keys = {plane_key(n, h) for n, h in planes}
    assert all(plane_key(n, h) in keys for n, h in face_planes(V, F)), 'hull face not on a given plane'
    return V, F

# ------------------------------------------------------------------ 1. #55 David and Goliath (A15 at lambda = 3/4), in Q
with contextlib.redirect_stdout(io.StringIO()) as so:
    a15 = {}; exec(open(os.path.join(SRC, 'exact_a15.py')).read(), a15)
log('Goliath corners = Jessen set (0,±1/2,±1) cyclic: True' in so.getvalue() and '(cube of edge 2 = 8): True' in so.getvalue(),
    "#55 study exact_a15.py executed: Goliath's corners = Jessen's set (0, ±1/2, ±1) cyclic, 2 V_Si + 6 V_Cr = 8 (its own checks)")
q1 = lambda x: QF(x, 0, 1)
Vg, _ = a15['cell'](a15['Si'][0], a15['lam']); Vd, _ = a15['cell'](a15['Cr'][0], Fr(0)); cr = a15['Cr'][0]
Vg, Fg = hull([tuple(q1(x) for x in v) for v in Vg]); Vd, Fd = hull([tuple(q1(x - c) for x, c in zip(v, cr)) for v in Vd])
A15 = ('#55 frame (the #53 census units): A15 in the cubic cell of edge 2, Si at 2Z^3 and 2Z^3 + (1, 1, 1), Cr at 2Z^3 + {(1/2, 0, 1), (3/2, 0, 1), '
       '(1, 1/2, 0), (1, 3/2, 0), (0, 1, 1/2), (0, 1, 3/2)}, weights w_Si = 3/4, w_Cr = 0 (lambda = 3/4); the power cells.')
Vg, Fg, rg = emit('dicto-goliath', dict(
    name='Goliath', finding='', paper='#55 David and Goliath', dicto_doi=D55, convex=True,
    status="known shape (the classical Z12 coordination icosahedron of A15, Frank and Kasper 1958; the convex hull of Jessen's orthogonal "
           "icosahedron, Jessen 1967, scaled by 1/2); the name is DICTO's",
    scale_note=A15 + " Goliath: the power cell of the Si site at the origin, corners (0, +-1/2, +-1) and cyclic permutations (Jessen's corner set "
               "scaled by 1/2); centred at the origin.",
    source={'app': 'study', 'path': RB + ': studies/2026-10-25-david-goliath/exact_a15.py cell(Si[0], 3/4) (Fractions)', 'id': None},
    symmetry_label='Th'), Vg, Fg,
    {'volume': '7/2', 'f_vector': [12, 30, 20], 'faces_by_sides': {'3': 20}, 'squared_edge_lengths': ['1', '3/2'], 'symmetry_order': 24})
J = {tuple(q1(x) for x in v) for a, b in itertools.product((Fr(1, 2), Fr(-1, 2)), (Fr(1), Fr(-1))) for v in [(0, a, b), (b, 0, a), (a, b, 0)]}
log(set(Vg) == J, "Goliath's corners = (0, ±1/2, ±1) and cyclic permutations (#55 (iv): Jessen's corner set scaled by 1/2), exactly")
Vd, Fd, rd = emit('dicto-david', dict(
    name='David', finding='', paper='#55 David and Goliath', dicto_doi=D55, convex=True,
    status="known shape (a tetragonal disphenoid: the empty Cr4 tetrahedron of A15, moved by half a body diagonal; #55 Corollary 1); the "
           "name is DICTO's",
    scale_note=A15 + " David: the power cell of the Cr site (1/2, 0, 1), corners (0, +-1/2, 1), (1, 0, 1/2), (1, 0, 3/2) (#55 (ii)); moved by "
               "-(1/2, 0, 1) so that its Cr site, its centroid, is at the origin.",
    source={'app': 'study', 'path': RB + ': studies/2026-10-25-david-goliath/exact_a15.py cell(Cr[0], 0) (Fractions), moved by -(1/2, 0, 1)', 'id': None},
    symmetry_label='D2d'), Vd, Fd,
    {'volume': '1/6', 'f_vector': [4, 6, 4], 'faces_by_sides': {'3': 4}, 'squared_edge_lengths': ['1', '3/2'], 'symmetry_order': 8})
log(2 * rg['vol'] + 6 * rd['vol'] == 8, '2 Goliaths + 6 Davids = 8 = the cubic cell of edge 2 (#55 (iii)), exactly')

# ------------------------------------------------------------------ 2. the holes of close packing (census engine), Cartesian frame
from engine import Net
from networks import NETS
from stackings import net_for
def Lmat(nl):
    """columns a1 = (1,-1,0), a2 = (1,0,-1), a3 = (2 nl/3)(1,1,1): L^T L = 2 G for the engine's metric G of an nl-layer stacking (ball
    spacing 1, layer spacing sqrt(2/3)); so x = L f is the stacking at ball spacing sqrt2 in orthonormal coordinates, all rational."""
    c = Fr(2 * nl, 3); return [[Fr(1), Fr(1), c], [Fr(-1), Fr(0), c], [Fr(0), Fr(-1), c]]
def inv3(M):
    import sympy as sp
    Mi = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r] for r in M]).inv()
    return [[Fr(int(Mi[i, j].p), int(Mi[i, j].q)) for j in range(3)] for i in range(3)]
def hole_cell(spec, nl, i, lam, K):
    """the power cell of motif site i at weight difference lam (a field element; K maps rationals into the field), moved so that the site
    is at the origin. Engine planes (fractional f): n.f <= b0 + b1 lam; with f = c_i + L^-1 x: (L^-T n).x <= b0 + b1 lam - n.c_i."""
    G = [[Fr(x) for x in r] for r in spec['G']]; L = Lmat(nl)
    LtL = [[sum(L[k][a] * L[k][b] for k in range(3)) for b in range(3)] for a in range(3)]
    assert LtL == [[2 * G[a][b] for b in range(3)] for a in range(3)], 'L^T L = 2G'
    Li = inv3(L); net = Net(spec['name'], spec['G'], spec['T'], spec['motif'], spec['w'])
    ci = net.motif[i][1]; planes = []
    for h in net.planes(i, Fr(spec['D2'])):
        n = h['n']; nn = tuple(sum(Li[k][a] * n[k] for k in range(3)) for a in range(3))     # L^-T n
        rhs = K(h['b'][0] - sum(n[k] * ci[k] for k in range(3))) + K(h['b'][1]) * lam
        planes.append((tuple(K(x) for x in nn), rhs))
    return hs_solid(planes), net.motif[i][0]
HCP = NETS['hcpholes']
TWIN = ('frame: the holes of ideal hexagonal close packing (the twinned octet) at ball spacing sqrt2 in orthonormal rational coordinates '
        '(close-packed layers perpendicular to (1, 1, 1): a1 = (1, -1, 0), a2 = (1, 0, -1), c = (4/3)(1, 1, 1); the census cell hcpholes mapped '
        'by x = L f); the #56/#57 values are at ball spacing 1: divide lengths by sqrt2 and volumes by 2 sqrt2 (the frame of Samson and Delilah, '
        'dicto-samson). Weights w_oct = 0, w_tet = lambda as in the census (#53 units, ball spacing 1). The piece is moved so that its hole (site) '
        'is at the origin.')

# --- Sonsam and Lahdeli: lambda = t, the root of 1536 t^3 + 5184 t^2 - 3384 t + 11 in the stretch (-1/8, 5/24) (#56 Theorem 2)
FT = AlgField.get([1536, 5184, -3384, 11], Fr(-1, 8), Fr(5, 24), 't')
tt = RF([0, 1], FT); KT = lambda x: RF([x], FT)
import sympy as sp
_pt = sp.Poly(1536 * sp.Symbol('t') ** 3 + 5184 * sp.Symbol('t') ** 2 - 3384 * sp.Symbol('t') + 11)
log(_pt.is_irreducible and _pt.count_roots(sp.Rational(-1, 8), sp.Rational(5, 24)) == 1 and abs(tt.f() - 0.0032669570) < 1e-10,
    f'the equal-volume weight t: 1536 t^3 + 5184 t^2 - 3384 t + 11 irreducible over Q, one root in (-1/8, 5/24), t = {tt.dec(12)} (#56: 0.0032669570)')
FDEF = field_definition(FT)
(Vso, Fso), k1 = hole_cell(HCP, 2, 2, tt, KT); (Vla, Fla), k0 = hole_cell(HCP, 2, 0, tt, KT)
assert (k1, k0) == ('tet', 'oct')
EQV = ' At this frame volume 2/3 = sqrt2/6 at ball spacing 1 (#56: two octahedral and four tetrahedral pieces in the cell of volume sqrt2).'
Vso, Fso, rso = emit('dicto-sonsam', dict(
    name='Sonsam', finding='', paper='#56 Sonsam and Lahdeli', dicto_doi=D56, convex=True, field_definition=FDEF,
    status='new (not found in the sources checked, #56)',
    scale_note=TWIN + ' Sonsam: the tetrahedral hole (0, 0, 3/8) of the census cell (site 2) at lambda = t, the equal-volume point.' + EQV,
    source={'app': 'study', 'path': RB + ': census engine (studies/2026-10-25-relay-census/scripts engine.py, networks.py "hcpholes") planes '
            'of site 2, solved exactly at lambda = t; #56 study studies/2026-10-25-hidden-bonds/equal_volume_exact.py', 'id': None},
    symmetry_label='auto'), Vso, Fso,
    {'volume': '2/3', 'f_vector': [19, 30, 13], 'faces_by_sides': {'3': 6, '5': 3, '6': 3, '9': 1}})
Vla, Fla, rla = emit('dicto-lahdeli', dict(
    name='Lahdeli', finding='', paper='#56 Sonsam and Lahdeli', dicto_doi=D56, convex=True, field_definition=FDEF,
    status='new (not found in the sources checked, #56)',
    scale_note=TWIN + ' Lahdeli: the octahedral hole (2/3, 2/3, 1/4) of the census cell (site 0) at lambda = t, the equal-volume point.' + EQV,
    source={'app': 'study', 'path': RB + ': census engine (hcpholes) planes of site 0, solved exactly at lambda = t', 'id': None},
    symmetry_label='auto'), Vla, Fla,
    {'volume': '2/3', 'f_vector': [12, 18, 8], 'faces_by_sides': {'3': 2, '5': 6}})
log(4 * rso['vol'] + 2 * rla['vol'] == 4, '4 Sonsams + 2 Lahdelis = 4 = the hcp cell (sqrt2 at ball spacing 1), exactly in Q(t)')

# --- Ian Dury (5/24) and Blockhead (3/8), in Q
K1 = lambda x: QF(x, 0, 1)
(Vid, Fid), _ = hole_cell(HCP, 2, 2, K1(Fr(5, 24)), K1); (Vbh, Fbh), _ = hole_cell(HCP, 2, 2, K1(Fr(3, 8)), K1)
Vid, Fid, rid = emit('dicto-ian-dury', dict(
    name='Ian Dury', finding='', paper='#56 Sonsam and Lahdeli', dicto_doi=D56, convex=True,
    status='new (not found in the sources checked, #56)',
    scale_note=TWIN + ' Ian Dury: the tetrahedral hole (0, 0, 3/8) (site 2) at the stop lambda = 5/24; volume 26/27 here = 13 sqrt2/54 at ball spacing 1.',
    source={'app': 'study', 'path': RB + ': census engine (hcpholes) planes of site 2 at lambda = 5/24; #56 study twin_stops.py', 'id': None},
    symmetry_label='auto'), Vid, Fid,
    {'volume': '26/27', 'f_vector': [16, 27, 13], 'faces_by_sides': {'3': 6, '4': 3, '6': 4}})
Vbh, Fbh, rbh = emit('dicto-blockhead', dict(
    name='Blockhead', finding='', paper='#56 Sonsam and Lahdeli', dicto_doi=D56, convex=True,
    status='new (not found in the sources checked, #56)',
    scale_note=TWIN + ' Blockhead: the tetrahedral hole (0, 0, 3/8) (site 2) at the stop lambda = 3/8 (the octahedral cells have shrunk to '
                      'points); volume 1 here = sqrt2/4 at ball spacing 1.',
    source={'app': 'study', 'path': RB + ': census engine (hcpholes) planes of site 2 at lambda = 3/8; #56 study twin_stops.py', 'id': None},
    symmetry_label='auto'), Vbh, Fbh,
    {'volume': '1', 'f_vector': [10, 18, 10], 'faces_by_sides': {'3': 6, '4': 3, '6': 1}})
(Vrh, Frh), _ = hole_cell(HCP, 2, 0, K1(Fr(5, 24)), K1)
log(4 * rid['vol'] + 2 * volume(Vrh, Frh) == 4 and volume(Vrh, Frh) == Fr(2, 27) and len(Vrh) == 8,
    "at 5/24: 4 Ian Durys + 2 60-degree rhombohedra (8 corners, volume 2/27 here = sqrt2/54) = 4, the cell, exactly (#56 Theorem 3)")

# ------------------------------------------------------------------ 3. #57: Chucky, Fang, Triskelion Tetrahedron (ABAC), in Q
AB4 = net_for('ABAC')
ST = ('frame: the holes of the double-hexagonal stacking ABAC (layers h, c, h, c; #57) at ball spacing sqrt2 in orthonormal rational coordinates '
      '(layers perpendicular to (1, 1, 1): a1 = (1, -1, 0), a2 = (1, 0, -1), period (8/3)(1, 1, 1); stackings.py net_for("ABAC") mapped by '
      'x = L f); the #57 values are for balls of diameter 1: divide lengths by sqrt2 and volumes by 2 sqrt2 (the frame of dicto-samson and '
      'dicto-sonsam). Weights w_oct = 0, w_tet = lambda. The piece is moved so that its hole is at the origin.')
(Vch, Fch), _ = hole_cell(AB4, 4, 0, K1(Fr(-3, 8)), K1); (Vfa, Ffa), _ = hole_cell(AB4, 4, 0, K1(Fr(5, 24)), K1)
(Vtt, Ftt), ktt = hole_cell(AB4, 4, 2, K1(Fr(5, 24)), K1); assert ktt == 'tet'
Vch, Fch, rch = emit('dicto-chucky', dict(
    name='Chucky', finding='', paper='#57 The Rule of Halves', dicto_doi=D57, convex=True,
    status='new (a Janus c/h piece; not found in the sources checked, #57)',
    scale_note=ST + ' Chucky: the octahedral hole of the gap between layer 0 (A, type c) and layer 1 (B, type h) (site 0), hexagonal top half and '
                    'cubic bottom half, at the stop lambda = -3/8; volume 383/192 here = 383 sqrt2/768 at ball diameter 1, the mean of the cubic '
                    'rhombic dodecahedron and the hexagonal 24-corner piece (#57 Corollary (ii)).',
    source={'app': 'study', 'path': RB + ': studies/2026-10-25-stackings/scripts stackings.py net_for("ABAC") + census engine, planes of site 0 at '
            'lambda = -3/8 (exact_named.py: the same site and weight)', 'id': None},
    symmetry_label='auto'), Vch, Fch,
    {'volume': '383/192', 'f_vector': [19, 30, 13], 'faces_by_sides': {'3': 3, '4': 3, '5': 6, '9': 1}})
Vfa, Ffa, rfa = emit('dicto-fang', dict(
    name='Fang', finding='', paper='#57 The Rule of Halves', dicto_doi=D57, convex=True,
    status='new (a Janus c/h piece; not found in the sources checked, #57)',
    scale_note=ST + ' Fang: the same octahedral hole (site 0) at the stop lambda = 5/24; volume 5/81 here = 5 sqrt2/324 at ball diameter 1, the '
                    'mean of the cubic octahedron and the hexagonal 60-degree rhombohedron (#57 Corollary (ii)).',
    source={'app': 'study', 'path': RB + ': stackings.py net_for("ABAC") + census engine, planes of site 0 at lambda = 5/24', 'id': None},
    symmetry_label='auto'), Vfa, Ffa,
    {'volume': '5/81', 'f_vector': [7, 12, 7], 'faces_by_sides': {'3': 4, '4': 3}})
Vtt, Ftt, rtt = emit('dicto-triskelion-tetrahedron', dict(
    name='Triskelion Tetrahedron', finding='', paper='#57 The Rule of Halves', dicto_doi=D57, convex=True,
    status="new (the cubic octet's tetrahedral piece at lambda = 5/24, a member of Samson's sliding family of #51; met in ABAC, #57)",
    scale_note=ST + ' Triskelion Tetrahedron (TT): the tetrahedral hole over position B of the gap between layers 0 and 1 (site 2; its nearest '
                    'layer, layer 0, is of type c, so by the rule of halves it is the cubic piece) at lambda = 5/24; volume 79/81 here = 79 sqrt2/324 '
                    'at ball diameter 1.',
    source={'app': 'study', 'path': RB + ': stackings.py net_for("ABAC") + census engine, planes of site 2 at lambda = 5/24', 'id': None},
    symmetry_label='auto'), Vtt, Ftt,
    {'volume': '79/81', 'f_vector': [16, 24, 10], 'faces_by_sides': {'3': 4, '6': 6}})
# cross-checks of #57's statements, exact: TT is the cubic octet's piece; Chucky and Fang are the means of their parents
OCT = net_for('ABC')
(Vc, Fc), _ = hole_cell(OCT, 3, 2, K1(Fr(5, 24)), K1)
log(sorted(len(f) for f in Fc) == sorted(len(f) for f in Ftt) and volume(Vc, Fc) == rtt['vol'] and similar_float([fv(v) for v in Vc], [fv(v) for v in Vtt]) is not None,
    'TT = the cubic octet (ABC) tetrahedral piece at 5/24: same faces, same exact volume, corners congruent (float corner matching)')
for nm, lam, r in (('Chucky', Fr(-3, 8), rch), ('Fang', Fr(5, 24), rfa)):
    (Va, Fa), _ = hole_cell(OCT, 3, 0, K1(lam), K1); (Vb, Fb), _ = hole_cell(HCP, 2, 0, K1(lam), K1)
    log(r['vol'] == (volume(Va, Fa) + volume(Vb, Fb)) / 2, f'{nm} = the mean of the cubic ({fmt(volume(Va, Fa))}) and hexagonal ({fmt(volume(Vb, Fb))}) '
        f'octahedral pieces at lambda = {lam}, exactly (#57 Corollary (ii))')

# ------------------------------------------------------------------ 4. #59 The Icosaxes Hexa (Q(sqrt5)): the #48 objects as in build_v2.py
ns = {}
gs = open(os.path.join(SRC, 'golden_split_exact.py')).read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(gs.split("print('AXEs generated:'")[0], ns)
    exec('def hull_facets' + gs.split('def hull_facets')[1].split('def poly_volume')[0], ns)
    kp = open(os.path.join(SRC, 'keyed_polar_exact.py')).read()
    exec(kp.split('ok_all = True')[1].split('def vol(P):')[0].replace("global ok_all; ok_all &= bool(ok); ", ""), ns)
    exec(next(l for l in kp.split('\n') if l.startswith('TRI = [[add(v, sub(')), ns)
q = lambda x: QF(x.a, x.b, 5); qv = lambda v: tuple(q(x) for x in v)
UC = qv(ns['UC']); Z = QF(0); H = PHI / 2
SIGNS = list(itertools.product((1, -1), repeat=3))
ICOS = [qv(v) for v in ns['ICOSAXES']]; UNBS = [sub(qv(v), UC) for v in ns['UNBAXES']]
TRI = [[qv(v) for v in t] for t in ns['TRI']]                 # TRI[k]: the #48 Tricap of the Unborn at (phi/2) SIGNS[k], facing the origin
VT = Q(Fr(1, 8), Fr(-1, 24))
def mirror(T):
    a, B = T[0], T[1:]; n = cross(sub(B[1], B[0]), sub(B[2], B[0])); k = 2 * dot(n, sub(a, B[0])) / dot(n, n)
    return [sub(a, mul(k, n))] + list(B)
MIR = [mirror(T) for T in TRI]
log(all(abs_(det3(sub(T[1], T[0]), sub(T[2], T[0]), sub(T[3], T[0]))) / 6 == VT for T in TRI + MIR), 'the 8 Tricaps and their 8 mirror images in their base planes have volume (3 - sqrt5)/24 exactly')
Vi0, Fi0 = hull(ICOS); Vu0, Fu0 = hull(UNBS)
log(volume(Vi0, Fi0) == 1 + Q(0, Fr(2, 3)) and volume(Vu0, Fu0) == 1 + Q(0, Fr(1, 3)), 'Icosaxes 1 + 2 sqrt5/3, Unborn Axes 1 + sqrt5/3 (as dicto-icosaxes, dicto-unborn-axes)')

def plane_of(V, f):
    n = (zero(V[0][0].d),) * 3
    for i in range(len(f)): n = add(n, cross(V[f[i]], V[f[(i + 1) % len(f)]]))
    k = next(x for x in n if x.sign() != 0); kk = k if k.sign() > 0 else -k
    return tuple(x / kk for x in n) + (dot(n, V[f[0]]) / kk,)
def merge_coplanar(V, F):
    par = list(range(len(F)))
    def root(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    pk = [plane_of(V, f) for f in F]; owner = {}
    for i, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]): owner[(a, b)] = i
    for (a, b), i in owner.items():
        j = owner[(b, a)]
        if pk[i] == pk[j]: par[root(i)] = root(j)
    groups = {}
    for i in range(len(F)): groups.setdefault(root(i), []).append(i)
    out = []
    for g in groups.values():
        if len(g) == 1: out.append(F[g[0]]); continue
        E = {(a, b) for i in g for a, b in zip(F[i], F[i][1:] + F[i][:1])}
        bd = {a: b for a, b in E if (b, a) not in E}
        start = next(iter(bd)); cyc = [start]
        while bd[cyc[-1]] != start: cyc.append(bd[cyc[-1]])
        assert len(cyc) == len(bd), 'merged face is not one simple polygon'
        out.append(cyc)
    return out
def drop_straight(V, F):
    """remove corners that are straight (collinear with their two neighbours) in every face that holds them; drop unused corners."""
    while True:
        straight = {}
        for f in F:
            for k, v in enumerate(f):
                a, c = V[f[k - 1]], V[f[(k + 1) % len(f)]]
                s = all(x.sign() == 0 for x in cross(sub(V[v], a), sub(c, V[v])))
                straight.setdefault(v, []).append(s)
        kill = {v for v, ss in straight.items() if all(ss)}
        if not kill: break
        F = [[v for v in f if v not in kill] for f in F]
    used = sorted({v for f in F for v in f}); m = {v: i for i, v in enumerate(used)}
    return [V[v] for v in used], [[m[v] for v in f] for f in F]
def assemble(parts):
    """the union of interior-disjoint convex parts meeting face to face: all faces, every face cancelled against its exact reverse."""
    V = []; idx = {}; F = []
    for Vp, Fp in parts:
        for f in Fp:
            g = []
            for i in f:
                p = Vp[i]
                if p not in idx: idx[p] = len(V); V.append(p)
                g.append(idx[p])
            F.append(g)
    canon_c = lambda f: (lambda k: tuple(f[k:] + f[:k]))(f.index(min(f)))
    keys = {}
    for i, f in enumerate(F): keys.setdefault(canon_c(f), []).append(i)
    dead = set()
    for i, f in enumerate(F):
        r = canon_c(f[::-1])
        if r in keys: dead.add(i); dead |= set(keys[r])
    F = [f for i, f in enumerate(F) if i not in dead]
    log(True, f'assembled {len(parts)} parts: {len(dead)} faces cancelled in pairs, {len(F)} left')
    return V, F
def apply_caps(V, F, caps):
    """dents / keys on hexagons: each cap's 3 base corners are alternate corners of one hexagonal face (the v2 keyed() rule)."""
    V = list(V); idx = {v: i for i, v in enumerate(V)}; faces = [list(f) for f in F]
    for T in caps:
        a, B = T[0], T[1:]; bi = {idx[b] for b in B}
        fi = [k for k, f in enumerate(faces) if bi <= set(f)]; assert len(fi) == 1 and len(faces[fi[0]]) == 6
        f = faces.pop(fi[0]); k0 = next(k for k in range(6) if {f[k], f[(k + 2) % 6], f[(k + 4) % 6]} == bi); h = f[k0:] + f[:k0]
        V.append(a); ia = len(V) - 1
        faces += [[h[0], h[1], h[2]], [h[2], h[3], h[4]], [h[4], h[5], h[0]], [h[0], h[2], ia], [h[2], h[4], ia], [h[4], h[0], ia]]
    return V, faces
def finish(V, F, label):
    n0 = len(F); F = merge_coplanar(V, F); V, F = drop_straight(V, F)
    log(True, f'{label}: {n0} faces before merging coplanar neighbours, {len(F)} after; {len(V)} corners')
    return V, F
I3 = lambda: [[fmt(QF(1 if i == j else 0)) for j in range(3)] for i in range(3)]
def tet_json(T, u, kind): return {'kind': kind, 'unborn_centre': [fmt(x) for x in u], 'apex': [fmt(x) for x in T[0]], 'base': [[fmt(x) for x in b] for b in T[1:]]}
move = lambda T, t: [add(v, t) for v in T]
COMPNOTE = ('Version 3 composition: the solid is the union of the convex `pieces` (dataset solids placed by x -> R x + t; interior-disjoint, '
            'meeting face to face), minus the tetrahedra in `minus` (dents), plus those in `plus` (keys). "tricap": the #48 Tricap of the Unborn '
            'centred at unborn_centre (as in dicto-lotus-jewel-axes); "mirrored tricap": that Tricap mirrored in its base plane (krp-core '
            'golden-split.js INTO_SMALL: the key of a big piece). Re-proved by check.py.')
FR59 = ('#59 frame = #48 frame (regular icosahedron of edge 1, lattice spacing phi): Icosaxes at the points (phi/2)(2Z)^3, Unborn Axes at '
        '(phi/2)(2Z+1)^3.')

# --- Keyaxes: Icosaxes, dents (INTO_BIG) on the hexagons facing +-(1,1,1), mirrored Tricap keys (INTO_SMALL) on the other six
kd = [SIGNS.index((1, 1, 1)), SIGNS.index((-1, -1, -1))]; kk = [k for k in range(8) if k not in kd]
Vk, Fk = finish(*apply_caps(Vi0, Fi0, [TRI[k] for k in kd] + [MIR[k] for k in kk]), 'Keyaxes')
Vk, Fk, rk = emit('dicto-keyaxes', dict(
    name='Keyaxes', finding='', paper='#59 The Icosaxes Hexa', dicto_doi=D59, convex=False,
    status='new (the piece of the keyed Icosaxes Kagome network; not found in the sources searched, #59)',
    scale_note=FR59 + ' Keyaxes: the Icosaxes (dicto-icosaxes) at the origin with the #48 Tricap taken out of the two opposite hexagons facing '
                      '+-(1, 1, 1) (dents, filled in the network by the keys of the two Dodecaxes at its two cluster centres) and the mirrored Tricap '
                      'added on the other six hexagons (keys into the network\'s open spaces): Icosaxes - 2 Tricaps + 6 Tricaps.',
    source={'app': 'study', 'path': RB + ': studies/2026-10-27-icosaxes-twenty (NK2, export-net-keyed.mjs); exact from the #48 objects '
            '(keyed_polar_exact.py ICOSAXES, TRI) keyed as krp-core golden-split.js INTO_BIG / INTO_SMALL', 'id': None},
    composition={'pieces': [{'solid': 'dicto-icosaxes', 'rotation': I3(), 'translation': [fmt(Z)] * 3}],
                 'minus': [tet_json(TRI[k], tuple(H * s for s in SIGNS[k]), 'tricap') for k in kd],
                 'plus': [tet_json(MIR[k], tuple(H * s for s in SIGNS[k]), 'mirrored tricap') for k in kk],
                 'tricap_volume': fmt(VT), 'note': COMPNOTE},
    symmetry_label='auto'), Vk, Fk,
    {'volume': '3/2 + sqrt(5)/2'})
log(rk['vol'] == PHI * PHI and rk['vol'] == volume(Vi0, Fi0) + 4 * VT, 'Keyaxes = phi^2 = Icosaxes + 4 Tricaps, exactly (#59 section 6)')

# --- Icosaxes Hexa: 8 Icosaxes at (phi/2) c, c in {+-1}^3, round the Unborn Axes at the origin (#59 section 5; bloom-geometry.js hexa())
CORN = [tuple(H * x for x in c) for c in SIGNS]
parts = [(Vu0, Fu0)] + [([add(v, t) for v in Vi0], Fi0) for t in CORN]
VH0, FH0 = assemble(parts)
VH, FH = finish(VH0, FH0, 'Icosaxes Hexa')
HP = [{'solid': 'dicto-unborn-axes', 'rotation': I3(), 'translation': [fmt(Z)] * 3}] + \
     [{'solid': 'dicto-icosaxes', 'rotation': I3(), 'translation': [fmt(x) for x in t]} for t in CORN]
VH, FH, rh = emit('dicto-icosaxes-hexa', dict(
    name='Icosaxes Hexa', finding='', paper='#59 The Icosaxes Hexa', dicto_doi=D59, convex=False,
    status='new (eight Icosaxes round an Unborn Axes as one solid, the node of the Icosaxes Kagome network; not found in the sources searched, #59)',
    scale_note=FR59 + ' Icosaxes Hexa: the eight Icosaxes on the corners (phi/2)(+-1, +-1, +-1) of a cube round the Unborn Axes at its centre, '
                      'the origin, joined into one solid (the same solid as nine Icosaxes passing through each other, #59 section 5).',
    source={'app': 'study', 'path': RB + ': studies/2026-10-27-icosaxes-twenty (H2); k-mix src/app/bloom-geometry.js hexa(false); exact from the '
            '#48 objects', 'id': None},
    composition={'pieces': HP, 'minus': [], 'plus': [], 'tricap_volume': fmt(VT), 'note': COMPNOTE},
    symmetry_label='auto'), VH, FH,
    {'volume': '9 + 17*sqrt(5)/3'})
log(rh['vol'] == 8 * volume(Vi0, Fi0) + volume(Vu0, Fu0), 'Icosaxes Hexa = 8 Icosaxes + 1 Unborn Axes = 9 + 17 sqrt5/3 (#59 v2 section 5), exactly')

# --- Lotus Hexa: each corner piece dented towards the centre (the Dodecaxes key fills it) and keyed outward (mirrored Tricap) on its other
#     seven hexagons, round a Dodecaxes (bloom-geometry.js hexa(true)) = the Icosaxes Hexa + 56 mirrored Tricaps
outk = []; outj = []
for c, t in zip(SIGNS, CORN):
    for k, s in enumerate(SIGNS):
        if s == tuple(-x for x in c): continue
        outk.append(move(MIR[k], t)); outj.append(tet_json(move(MIR[k], t), add(t, tuple(H * x for x in s)), 'mirrored tricap'))
VL, FL = finish(*apply_caps(VH0, FH0, outk), 'Lotus Hexa')
VL, FL, rl = emit('dicto-lotus-hexa', dict(
    name='Lotus Hexa', finding='', paper='#59 The Icosaxes Hexa', dicto_doi=D59, convex=False,
    status='new (the keyed Icosaxes Hexa; not found in the sources searched, #59)',
    scale_note=FR59 + ' Lotus Hexa: the keyed Icosaxes Hexa: round a Dodecaxes at the origin, each of the eight corner pieces at (phi/2)(+-1, +-1, '
                      '+-1) is dented on the hexagon facing the centre (the Dodecaxes\' key fills the dent) and carries the mirrored Tricap as a key '
                      'outward on its other seven hexagons. So it is the Icosaxes Hexa plus 56 mirrored Tricaps.',
    source={'app': 'study', 'path': RB + ': studies/2026-10-27-icosaxes-twenty (K2, export-keyed.mjs); k-mix src/app/bloom-geometry.js hexa(true); '
            'exact from the #48 objects', 'id': None},
    composition={'pieces': HP, 'minus': [], 'plus': outj, 'tricap_volume': fmt(VT),
                 'note': COMPNOTE + ' The 8 inner Tricaps (the corner pieces\' dents and the Dodecaxes\' keys) only change owner inside the solid, '
                                    'so they do not appear.'},
    symmetry_label='auto'), VL, FL,
    {})
log(rl['vol'] == rh['vol'] + 56 * VT, f'Lotus Hexa = Icosaxes Hexa + 56 Tricaps = {fmt(rl["vol"])} = {rl["vol"].dec(4)} (study K2: 23.454; #59 states no value)')

# ------------------------------------------------------------------ 5. unit-volume copies (as build_v2.py; centre = the corner centroid)
mpmath.mp.dps = 60
def mpx(x):
    if isinstance(x, (KC, RF)): return x.mp()
    return mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(x.d)
def dec15(m):
    from decimal import Decimal
    qd = Decimal(mpmath.nstr(m, 50, strip_zeros=False, min_fixed=-mpmath.inf, max_fixed=mpmath.inf)).quantize(Decimal(1).scaleb(-15))
    return format(qd, 'f') if qd != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-15)), 'f')
ALL = [('dicto-goliath', Vg), ('dicto-david', Vd), ('dicto-sonsam', Vso), ('dicto-lahdeli', Vla), ('dicto-ian-dury', Vid), ('dicto-blockhead', Vbh),
       ('dicto-chucky', Vch), ('dicto-fang', Vfa), ('dicto-triskelion-tetrahedron', Vtt), ('dicto-keyaxes', Vk), ('dicto-icosaxes-hexa', VH),
       ('dicto-lotus-hexa', VL)]
for slug, V in ALL:
    p = os.path.join(SOL, slug + '.json'); doc = json.load(open(p))
    d = V[0][0].d; vol = parse_any(doc['volume']['exact'], d)
    c = tuple(sum((v[k] for v in V), zero(d)) / len(V) for k in range(3))
    s = mpmath.power(mpx(vol), mpmath.mpf(-1) / 3)
    W = [[mpx(c[k]) + s * (mpx(v[k]) - mpx(c[k])) for k in range(3)] for v in V]
    at_origin = all(x.sign() == 0 for x in c)
    uv = {'scale_exact': f"({doc['volume']['exact']})**(-1/3)", 'scale_decimal': dec15(s),
          'centre': {'exact': [fmt(x) for x in c], 'decimal': [x.dec() for x in c],
                     'kind': 'origin of the frame (= the corner centroid)' if at_origin else 'corner centroid (mean of the corners; the frame origin is not the centre)'},
          'note': 'x -> centre + s (x - centre), s = V^(-1/3) with V the exact volume above; s is symbolic and the corners are decimals (15 places, '
                  'as elsewhere). Same corner order and faces as above; volume 1.',
          'vertices_decimal': [[dec15(x) for x in w] for w in W]}
    if 'field_definition' in doc: uv['note'] += ' The volume is rational, so s is a plain cube root.'
    out = {}
    for k, v in doc.items():
        if k == 'field_definition': continue
        out[k] = v
        if k == 'field' and 'field_definition' in doc: out['field_definition'] = doc['field_definition']
        if k == 'volume': out['unit_volume'] = uv
    out['checks'] = dict(out['checks'], unit_volume='decimal unit-volume copy has volume 1 (1e-12) and is the solid scaled by s (check.py)')
    if 'composition' in doc: out['checks']['composition'] = 'union of convex dataset pieces -/+ Tricaps, exact (check.py)'
    json.dump(out, open(p, 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(SOL, slug + '-unit-volume.off'), 'w') as fh:
        fh.write('OFF\n# ' + doc['name'] + ', unit volume (scaled by V^(-1/3) about ' + ('the origin' if at_origin else 'its corner centroid')
                 + ') — Created by DICTO · dictospheres.com — CC BY-SA 4.0\n')
        fh.write(f"{len(V)} {len(doc['faces'])} {doc['f_vector']['edges']}\n")
        for w in uv['vertices_decimal']: fh.write(' '.join(w) + '\n')
        for f in doc['faces']: fh.write(str(len(f)) + ' ' + ' '.join(map(str, f)) + '\n')
    log(True, f'{slug}: unit-volume copy, s = {uv["scale_decimal"]}, centre {uv["centre"]["kind"]}')

json.dump({'log': LOG}, open(os.path.join(HERE, 'build_v3.log.json'), 'w'), indent=1, ensure_ascii=False)
print(f"{sum(l.startswith('PASS') for l in LOG)} PASS, {sum(l.startswith('FAIL') for l in LOG)} FAIL")
