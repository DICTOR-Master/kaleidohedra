# DICTO · dictospheres.com — math-data dataset VERSION 4 builder (2026-10-28). Created by DICTO. Licence CC BY-SA 4.0.
# Adds three named solids of DICTO's papers #61, #62 and #63:
#   #61 The Swap Rule (Q(sqrt3)): Ganesha, the mixed (Janus c/h) tetrahedral piece of the squashed stacking ACBC, at the parameters of
#       the paper's Figure 1 (layer spacing^2 = (3/4)(2/3), i.e. s = 3/4; lambda = 1/10);
#   #62 Shadows of the Fourth Dimension (Q(sqrt5)): Shadow-17, two J11 (Johnson's gyroelongated pentagonal pyramid) glued on their pentagons;
#   #63 The White Queen 600-cell (Q(sqrt5)): Humpty Dumpty, the real 48-vertex cell-first slice of the 600-cell (convex).
# Geometry is NOT re-derived from the papers' prose: the studies' own exact code is executed (copies in build/sources/, from the
# research branch at commit 0620db53): splash.py net_for (#61: the #57 stacking with the layer spacing as a parameter) with the census
# engine engine.py already used by build_v3.py; q5.py + polytopes.py (#62/#63: the exact 600-cell and its four directions, as in
# atlas600.py). Shadow-17 is exact by its construction in #62 (two J11 of edge 1, shadow17_j11.py), here built from the icosahedron
# (0, +-1/2, +-phi/2) and checked against the study's numerical equilateral form (eqreal_600-cell_edge-first_slice_V17.npy).
# Writes solids/<slug>.json/.off (+ unit_volume, -unit-volume.off) and build_v4.log.json.
import contextlib, io, itertools, json, os, sys
from fractions import Fraction as Fr
import numpy as np
import mpmath, sympy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
SRC = os.path.join(HERE, 'sources'); SOL = os.path.join(HERE, '..', 'solids')
sys.path.insert(0, SRC)
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).', 'version_added': 4}
D61, D62, D63 = '10.5281/zenodo.23682596', '10.5281/zenodo.23687223', '10.5281/zenodo.23690856'
RB = 'research branch (commit 0620db53)'

def parse_any(s, d):
    e = sympy.expand(sympy.sympify(s)); a = Fr(0); b = Fr(0)
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
    """exact solid {x : n.x <= c} (as build_v3.py): float corner guesses solved and tested exactly, then the exact hull."""
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

# ------------------------------------------------------------------ 1. #61 Ganesha (ACBC, s = 3/4, lambda = 1/10), in Q(sqrt3)
from engine import Net
_sp = open(os.path.join(SRC, 'splash.py')).read()
SPL = {'Fr': Fr}
exec(_sp[_sp.index('POS = '):_sp.index("L = sp.Symbol")], SPL)
exec(_sp[_sp.index('def net_for'):_sp.index('def words')], SPL)
S61, LAM61, W61 = Fr(3, 4), Fr(1, 10), 'ACBC'
R3 = lambda x: QF(x, 0, 3)
def hole_cell_s(spec, nl, i, lam):
    """the power cell of motif site i of a stacking at layer spacing^2 = s (2/3) (ball spacing 1), in orthonormal coordinates at ball
    spacing sqrt2: a1 = (1, -1, 0), a2 = (1, 0, -1), a3 = nl h (1, 1, 1)/sqrt3 with h^2 = 4s/3 = 1 for s = 3/4, so a3 = nl (sqrt3/3)(1, 1, 1);
    a_j . a_k = 2 G_jk. Engine planes n.f <= b0 + b1 lam, f = c_i + L^-1 x: y.x <= b0 + b1 lam - n.c_i with a_k . y = n_k."""
    c = QF(0, Fr(nl, 3), 3); a = [(R3(1), R3(-1), R3(0)), (R3(1), R3(0), R3(-1)), (c, c, c)]
    G = spec['G']; assert all(dot(a[j], a[k]) == R3(2 * Fr(G[j][k])) for j in range(3) for k in range(3)), 'a_j . a_k = 2 G_jk'
    D = det3(*a); cr = [cross(a[1], a[2]), cross(a[2], a[0]), cross(a[0], a[1])]
    net = Net(spec['name'], spec['G'], spec['T'], spec['motif'], spec['w']); ci = net.motif[i][1]; planes = []
    for h in net.planes(i, Fr(spec['D2'])):
        n = h['n']; y = tuple(sum((cr[k][j] * Fr(n[k]) for k in range(3)), R3(0)) / D for j in range(3))
        planes.append((y, R3(Fr(h['b'][0]) - sum(Fr(n[k]) * ci[k] for k in range(3))) + R3(Fr(h['b'][1])) * lam))
    return planes, net.motif[i][0]
spec = SPL['net_for'](W61, S61); st = SPL['steps'](W61); nl = len(W61)
ltype = lambda k: 'c' if st[(k - 1) % nl] == st[k % nl] else 'h'           # as the study's export_swap.py / swap_cut.py
i61 = next(i for i, (k, p) in enumerate(spec['motif']) if k == 'tet' and i % 3 == 1 and (ltype(i // 3), ltype(i // 3 + 1)) == ('c', 'h'))
g61 = i61 // 3
pl61, k61 = hole_cell_s(spec, nl, i61, R3(LAM61)); assert k61 == 'tet'
Vga, Fga = hs_solid(pl61)
log(True, f'#61 Ganesha: ACBC site {i61} (the tetrahedral hole over X at 3/4 of gap {g61}: lower layer {ltype(g61)}, upper layer {ltype(g61 + 1)}), '
          f'{len(pl61)} engine planes at lambda = 1/10, s = 3/4')
# the gap's mid-plane, relative to the site (at 3/4 of the gap): (1, 1, 1).x = -sqrt3/4
one = (R3(1), R3(1), R3(1)); mid = QF(0, Fr(-1, 4), 3)
Vb, Fb = hs_solid(pl61 + [(one, mid)]); Vt, Ft = hs_solid(pl61 + [(tuple(-x for x in one), -mid)])
k22 = 2 * 2 ** .5
vb, vt, vg = volume(Vb, Fb), volume(Vt, Ft), volume(Vga, Fga)
log(vb + vt == vg and abs(vb.f() / k22 - 0.058005) < 5e-7 and abs(vt.f() / k22 - 0.196269) < 5e-7,
    f'Ganesha cut at its gap\'s mid-plane: bottom {vb.f() / k22:.6f} + top {vt.f() / k22:.6f} at ball spacing 1 (#61 Figure 1: 0.058005 and 0.196269), exactly additive')
FR61 = ('frame: the holes of the stacking ACBC with its layers squashed to layer spacing^2 = (3/4)(2/3) (s = 3/4, #61 Figure 1), at ball spacing '
        'sqrt2 in orthonormal coordinates (layers perpendicular to (1, 1, 1): a1 = (1, -1, 0), a2 = (1, 0, -1), period 4 (sqrt3/3)(1, 1, 1), layer '
        'spacing 1; splash.py net_for("ACBC", 3/4) mapped by x = L f); the #61 values are at ball spacing 1: divide lengths by sqrt2 and volumes '
        'by 2 sqrt2. Weights w_oct = 0, w_tet = lambda = 1/10. The piece is moved so that its hole is at the origin.')
Vga, Fga, rga = emit('dicto-ganesha', dict(
    name='Ganesha', finding='', paper='#61 The Swap Rule', dicto_doi=D61, convex=True,
    status='new (a Janus c/h tetrahedral piece of a squashed stacking; not found in the sources checked, #61)',
    scale_note=FR61 + f' Ganesha: the tetrahedral hole over X at 3/4 of the gap between layer 1 (C, type c) and layer 2 (B, type h) (site {i61}), the '
                      'piece of #61 Figure 1: its part below the gap\'s mid-plane (1, 1, 1).x = -sqrt3/4 is the pure cubic bottom, its part above the '
                      f'pure hexagonal top. Volume {vg.dec(6)} here = {vg.f() / k22:.6f} at ball spacing 1 (parts 0.058005 + 0.196269, #61).',
    parameters={'stacking': 'ACBC', 'layer_spacing_squared': '(3/4)*(2/3) = 1/2 at ball spacing 1 (s = 3/4)', 'lambda': '1/10', 'site': i61},
    source={'app': 'study', 'path': RB + ': studies/2026-10-27-splash-rules/scripts splash.py net_for("ACBC", 3/4) + census engine (engine.py), '
            f'planes of site {i61} at lambda = 1/10 (the piece of export_swap.py 3/4 1/10)', 'id': None},
    symmetry_label='auto'), Vga, Fga, {})

# ------------------------------------------------------------------ 2. #62 Shadow-17: two J11 glued on their pentagons, in Q(sqrt5)
q = lambda a, b=0: QF(a, b, 5); H = PHI / 2; h2 = q(Fr(1, 2))
ICO = list({v for s1 in (1, -1) for s2 in (1, -1) for v in [(q(0), s1 * h2, s2 * H), (s2 * H, q(0), s1 * h2), (s1 * h2, s2 * H, q(0))]})
Vi, Fi = hull(ICO); assert len(Vi) == 12 and len(Fi) == 20
top = (q(0), h2, H); it = Vi.index(top)
pent = sorted({v for f in Fi if it in f for v in f} - {it})
nn = dot(top, top); hp = dot(top, Vi[pent[0]]); assert all(dot(top, Vi[k]) == hp for k in pent)
cen = tuple(hp / nn * x for x in top)
refl = lambda p: tuple(p[k] - 2 * (dot(top, p) - hp) / nn * top[k] for k in range(3))
J = [f for f in Fi if it not in f]                                              # J11 = the icosahedron minus the pyramid on `top`
pts = {}; V17 = []
def ix(p):
    p = tuple(x - c for x, c in zip(p, cen))
    if p not in pts: pts[p] = len(V17); V17.append(p)
    return pts[p]
F17 = [[ix(Vi[k]) for k in f] for f in J] + [[ix(refl(Vi[k])) for k in f][::-1] for f in J]
log(len(V17) == 17 and len(F17) == 30, 'Shadow-17 = two J11 of edge 1 (the icosahedron (0, +-1/2, +-phi/2) and cyclic, less one corner) glued on their '
    'pentagons, the second the mirror image of the first in the pentagon\'s plane (as in shadow17_j11.py): 17 corners, 30 triangles, exactly')
A = np.load(os.path.join(SRC, 'eqreal_600-cell_edge-first_slice_V17.npy'))
dA = np.sort(np.linalg.norm(A[:, None] - A[None], axis=2)[np.triu_indices(17, 1)])
B = np.array([[x.f() for x in v] for v in V17]); dB = np.sort(np.linalg.norm(B[:, None] - B[None], axis=2)[np.triu_indices(17, 1)])
log(A.shape == (17, 3) and np.abs(dA - dB).max() < 1e-12, f'Shadow-17: all 136 corner distances agree with the study\'s numerical equilateral form '
    f'of the 600-cell\'s edge-first slice (eqreal_..._V17.npy) to {np.abs(dA - dB).max():.1e} (#62: 4e-16)')
Vs17, Fs17, rs17 = emit('dicto-shadow-17', dict(
    name='Shadow-17', finding='', paper='#62 Shadows of the Fourth Dimension', dicto_doi=D62, convex=False,
    status='known shape (two J11 glued on their pentagons; J11 = the gyroelongated pentagonal pyramid, Johnson 1966, the diminished icosahedron; '
           'an obvious gluing, not claimed new in #62); what #62 adds is that it is the equal-edged form of the 600-cell\'s edge-first slices at '
           'the outer heights (17 vertices, 30 triangles); the name is a placeholder of #62',
    scale_note='edge 1: the J11 is the icosahedron with corners (0, +-1/2, +-phi/2) and cyclic permutations less its corner (0, 1/2, phi/2); the '
               'second J11 is its mirror image in the plane of the pentagon round that corner; moved so that the pentagon\'s centre is at the '
               'origin. Non-convex: the five edges of the shared pentagon are folded inward (dihedral 2 x 100.81 = 201.62 degrees, #62).',
    source={'app': 'study', 'path': RB + ': studies/2026-10-27-4d-shadows/scripts/shadow17_j11.py (two J11 base to base, edge 1, exact in Q(sqrt5) by '
            'construction); checked against data/eqreal_600-cell_edge-first_slice_V17.npy', 'id': None},
    symmetry_label='D5h'), V17, F17,
    {'f_vector': [17, 45, 30], 'faces_by_sides': {'3': 30}, 'squared_edge_lengths': ['1']})
J11 = q(5, 0) * (3 + q(0, 1)) / 12 - (5 + q(0, 1)) / 24
log(rs17['vol'] == 2 * J11, f'Shadow-17 volume = 2 J11 = 2 ((5/12)(3 + sqrt5) - (5 + sqrt5)/24) = {fmt(rs17["vol"])} (icosahedron less a pentagonal pyramid, twice)')

# ------------------------------------------------------------------ 3. #63 Humpty Dumpty: the 48-vertex cell-first slice of the 600-cell, Q(sqrt5)
import q5 as q5m
from polytopes import polytope
P600 = polytope('600-cell'); V4 = P600['V']; d4 = P600['dirs']['cell-first']['d']
hv = q5m.Q5(1, Fr(1, 2)); heights = [q5m.dot(v, d4) for v in V4]
P4 = [v for v, x in zip(V4, heights) if x == hv]
for a, b in P600['st']['E']:                                                   # as atlas600.py: the vertices on the cut + every edge crossing it
    ha, hb = heights[a], heights[b]
    if ((ha - hv) * (hb - hv)).sign() < 0:
        t = (hv - ha) / (hb - ha); P4.append(tuple(x + t * (y - x) for x, y in zip(V4[a], V4[b])))
cq = lambda x: QF(x.a, x.b, 5)
dq = tuple(cq(x) for x in d4); dot4 = lambda u, v: sum((x * y for x, y in zip(u, v)), q(0)); N = dot4(dq, dq)   # exactlib dot is 3-dimensional
def qmul_conj_d(p):
    """conj(d) * p (quaternions w + xi + yj + zk): real part d.p, imaginary part d0 p_v - p0 d_v - d_v x p_v."""
    p = tuple(cq(x) for x in p); a0, av, b0, bv = dq[0], dq[1:], p[0], p[1:]
    return dot4(dq, p), tuple(a0 * bv[k] - b0 * av[k] for k in range(3)), cross(av, bv)
YH = []
for p in P4:
    re, lin, cr = qmul_conj_d(p); YH.append(tuple(lin[k] - cr[k] for k in range(3))); assert re == cq(hv)
log(len(P4) == 48 and len(set(YH)) == 48 and N == q(Fr(7, 4), Fr(3, 4)), '#63 Humpty Dumpty: the 600-cell (circumradius 2, edge sqrt5 - 1) cut at height '
    '1 + sqrt5/2 along the cell-first direction d (|d|^2 = 7/4 + 3sqrt5/4): 48 points (vertices on the cut and edge crossings), exactly in Q(sqrt5)')
Vh, Fh = hull(YH)
at = json.load(open(os.path.join(SRC, 'atlas600-cell-first-V48.json')))[0]
el_at = {parse_any(s.replace('√5', '*sqrt(5)'), 5) for s in at['edge_len2_exact']}
el_h = {dot(sub(Vh[a], Vh[b]), sub(Vh[a], Vh[b])) for a, b in edges_of(Fh)}
log({x / N for x in el_h} == el_at, 'Humpty Dumpty: its squared edge lengths / |d|^2 = the eight values of the study\'s atlas (atlas600.json), exactly')
FR63 = ('frame: the 600-cell of #62/#63 (vertices the permutations of (+-2, 0, 0, 0), (+-1, +-1, +-1, +-1) and the even permutations of (+-phi, +-1, '
        '+-1/phi, 0); circumradius 2, edge sqrt5 - 1), cut by the 3-space at height 1 + sqrt5/2 along the cell-first direction d = the centre of '
        'the cell (0, 24, 25, 40) = (7/8 + 3sqrt5/8, 3/8 + sqrt5/8, 0, 1/4). Coordinates: the imaginary part of the quaternion product conj(d) p of '
        'each point p of the cut, which is the slice turned into R^3 (centre at the origin) and scaled by |d| = sqrt((7 + 3sqrt5)/4) = 1.8512: '
        'the scale at which the slice is exact in Q(sqrt5) (unscaled, an orthonormal frame needs sqrt(7 + 3sqrt5) as well). Divide lengths by |d| '
        'and squared lengths by 7/4 + 3sqrt5/4 for the 600-cell of circumradius 2.')
Vh, Fh, rh = emit('dicto-humpty-dumpty', dict(
    name='Humpty Dumpty', finding='', paper='#63 The White Queen 600-cell', dicto_doi=D63, convex=True,
    status='new (the real 48-vertex cell-first slice of the 600-cell, a convex egg of 92 triangles; not found in the sources checked, #63)',
    scale_note=FR63 + ' Humpty Dumpty: 48 corners (12 of degree 8, 36 of degree 5), 138 edges of eight lengths (ratio up to (5 + sqrt5)/2), 92 '
                      'triangles; tetrahedral symmetry Td (#63 section 7).',
    source={'app': 'study', 'path': RB + ': studies/2026-10-27-white-queen-600/scripts/atlas600.py (the cut, with the exact modules q5.py and '
            'polytopes.py of studies/2026-10-27-4d-shadows); checked against data/atlas600.json (cell-first, 48 vertices)', 'id': None},
    symmetry_label='Td'), Vh, Fh,
    {'f_vector': [48, 138, 92], 'faces_by_sides': {'3': 92}, 'symmetry_order': 24,
     'squared_edge_lengths': [fmt(x * N) for x in sorted(el_at, key=lambda z: z.f())]})

# ------------------------------------------------------------------ 4. unit-volume copies (as build_v3.py; centre = the corner centroid)
mpmath.mp.dps = 60
def mpx(x): return mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(x.d)
def dec15(m):
    from decimal import Decimal
    qd = Decimal(mpmath.nstr(m, 50, strip_zeros=False, min_fixed=-mpmath.inf, max_fixed=mpmath.inf)).quantize(Decimal(1).scaleb(-15))
    return format(qd, 'f') if qd != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-15)), 'f')
ALL = [('dicto-ganesha', Vga), ('dicto-shadow-17', Vs17), ('dicto-humpty-dumpty', Vh)]
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
    out = {}
    for k, v in doc.items():
        out[k] = v
        if k == 'volume': out['unit_volume'] = uv
    out['checks'] = dict(out['checks'], unit_volume='decimal unit-volume copy has volume 1 (1e-12) and is the solid scaled by s (check.py)')
    json.dump(out, open(p, 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(SOL, slug + '-unit-volume.off'), 'w') as fh:
        fh.write('OFF\n# ' + doc['name'] + ', unit volume (scaled by V^(-1/3) about ' + ('the origin' if at_origin else 'its corner centroid')
                 + ') — Created by DICTO · dictospheres.com — CC BY-SA 4.0\n')
        fh.write(f"{len(V)} {len(doc['faces'])} {doc['f_vector']['edges']}\n")
        for w in uv['vertices_decimal']: fh.write(' '.join(w) + '\n')
        for f in doc['faces']: fh.write(str(len(f)) + ' ' + ' '.join(map(str, f)) + '\n')
    log(True, f'{slug}: unit-volume copy, s = {uv["scale_decimal"]}, centre {uv["centre"]["kind"]}')

json.dump({'log': LOG}, open(os.path.join(HERE, 'build_v4.log.json'), 'w'), indent=1, ensure_ascii=False)
print(f"{sum(l.startswith('PASS') for l in LOG)} PASS, {sum(l.startswith('FAIL') for l in LOG)} FAIL")
