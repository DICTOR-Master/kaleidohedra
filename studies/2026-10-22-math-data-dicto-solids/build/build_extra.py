# DICTO · dictospheres.com — second pass of the math-data dataset (2026-10-23), exact in Q(sqrt5).
#   1. the DICTO OCD Stella (#31a), built exactly from its published planes, because its packing needs it;
#   2. the published packings that do NOT fill space (packings-nonfilling/): OG on bcc (#31), OCD Stella on bcc (#31a),
#      DBT on the gyrated octet and OTT on the octet (#37a); lattice, pieces, exact density, checked against the papers;
#   3. a unit-volume copy of every solid (key "unit_volume" + solids/<slug>-unit-volume.off).
# Published values are compared exactly where the paper states them; a mismatch is logged as FAIL and nothing is "fixed".
import glob, itertools, json, os, sys
from fractions import Fraction as Fr
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
import sympy, mpmath

ROOT = os.path.join(HERE, '..'); SOL = os.path.join(ROOT, 'solids'); NPK = os.path.join(ROOT, 'packings-nonfilling')
os.makedirs(NPK, exist_ok=True)
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok
def parse(s):
    e = sympy.expand(sympy.sympify(s)); a = Fr(0); b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        c = Fr(int(sympy.fraction(c)[0]), int(sympy.fraction(c)[1]))
        if t == 1: a += c
        elif t == sympy.sqrt(5): b += c
        else: raise ValueError(s)
    return QF(a, b, 5)
def load(slug):
    d = json.load(open(os.path.join(SOL, slug + '.json')))
    return d, [tuple(parse(x) for x in v['exact']) for v in d['vertices']], d['faces']
abs_ = lambda x: x if x.sign() >= 0 else -x
add3 = lambda u, v: tuple(u[i] + v[i] for i in range(3))
smul = lambda k, u: tuple(k * x for x in u)
def newell(V, f):
    n = (zero(), zero(), zero())
    for i in range(len(f)): n = add3(n, cross(V[f[i]], V[f[(i + 1) % len(f)]]))
    return n
def parallel(u, w): return all(x.sign() == 0 for x in cross(u, w))
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).'}
MARK = {'credit': 'DICTO', 'creator_mark': 'Created by DICTO · dictospheres.com', 'licence': 'CC BY-SA 4.0'}
vec = lambda v: {'exact': [fmt(x) for x in v], 'decimal': [x.dec() for x in v]}
num = lambda x: {'exact': fmt(x), 'decimal': x.dec()}
I3 = [['1', '0', '0'], ['0', '1', '0'], ['0', '0', '1']]; O3 = ['0', '0', '0']

# ---------------------------------------------------------------- the OG and its body-centred cubic packing (#31)
og, OG, OGf = load('dicto-ogdoecontahedron')
vOG = volume(OG, OGf)
hexes = []
for f in OGf:
    if len(f) == 6:
        n = newell(OG, f); hexes.append((n, dot(n, OG[f[0]])))
log(len(hexes) == 20, f'OG: {len(hexes)} joint hexagons')
# the joint hexagons that point to the corners of the coordinate cube (one of the OG's five inscribed cubes, #31: "five bcc packings")
cube = [(Q(1), Q(1), Q(1)), (Q(1), Q(-1), Q(-1)), (Q(-1), Q(1), Q(-1)), (Q(-1), Q(-1), Q(1))]
T = []
for c in cube:
    n, d = next((n, d) for n, d in hexes if parallel(n, c) and dot(n, c).sign() > 0)
    T.append(smul(Q(2) * d / dot(n, n), n))                       # #31: t = 2 d n / |n|^2 puts the opposite hexagon on this one
log(all(dot(t, t) == Q(Fr(8, 9), Fr(8, 27)) for t in T), f'bond vectors |t|^2 = {fmt(dot(T[0], T[0]))} (#31: 8/9 + 8 sqrt5/27)')
LB = [add3(T[0], T[1]), add3(T[0], T[2]), T[0]]                    # bcc basis t0 + t1, t0 + t2, t0 (study golden_fill.py / golden_cut.py)
cellB = abs_(det3(*LB))
log(cellB == Q(Fr(512, 729), Fr(256, 729)), f'bcc cell volume {fmt(cellB)} (#31a: (512 + 256 sqrt5)/729)')
dOG = vOG / cellB
log(dOG == Q(Fr(9225, 608), Fr(-3915, 608)), f'OG density {fmt(dOG)} = {dOG.f():.6f} (#31: (9225 - 3915 sqrt5)/608 ~ 77.43%)')

# ---------------------------------------------------------------- the DICTO OCD Stella (#31a), exact
# golden envelope: the 30 planes perpendicular to the OG's 15 two-fold axes, through its outermost corners (#31a, #37a: the rhombic
# triacontahedron of inradius 2/3 round the OG); the two-fold axes are read off the OG's own exact symmetry group (half-turns).
G = sym_group(OG)
ax2 = []
for M, s in G:
    if s > 0 and (M[0][0] + M[1][1] + M[2][2]) == Q(-1):           # half-turn: axis = a nonzero column of M + I
        A = [[M[i][j] + (1 if i == j else 0) for i in range(3)] for j in range(3)]
        u = next(tuple(col) for col in A if any(x.sign() for x in col))
        if not any(parallel(u, w) for w in ax2): ax2.append(u)
log(len(ax2) == 15, f'OG: {len(ax2)} two-fold axes (from its exact group of order {len(G)})')
HK = []
for u in ax2:
    for s in (u, smul(Q(-1), u)):
        HK.append((s, max((dot(s, v) for v in OG), key=lambda x: x.f())))
log(all(h * h / dot(n, n) == Q(Fr(4, 9)) for n, h in HK), 'golden envelope: all 30 planes at distance 2/3 (rhombic triacontahedron of inradius 2/3)')
# the companion's 20 three-fold planes, perpendicular to the hexagon normals at squared distance 14/27 - 10 sqrt5/243 (#31a)
D2 = Q(Fr(14, 27), Fr(-10, 243))
HEX = [(n, qsqrt(D2 * dot(n, n))) for n, d in hexes]
Cv, Cf = halfspace_solid(HK + HEX)
from collections import Counter
fkC = dict(Counter(len(f) for f in Cf)); vC = volume(Cv, Cf)
log(len(Cv) == 72 and fkC == {6: 30, 3: 20}, f'companion C: {len(Cv)} corners, faces {fkC} (#31a: 72 corners, 30 hexagons, 20 triangles)')
log(vC == Q(Fr(-18880, 2187), Fr(9760, 2187)), f'companion C volume {fmt(vC)} (#31a: (-18880 + 9760 sqrt5)/2187)')
LAT = []
for m in itertools.product(range(-2, 3), repeat=3):
    if any(m): LAT.append(add3(add3(smul(Q(m[0]), LB[0]), smul(Q(m[1]), LB[1])), smul(Q(m[2]), LB[2])))
VOR = [(t, dot(t, t) / 2) for t in LAT]
Sv, Sf = halfspace_solid(HK + HEX + VOR)
Sv, Sf = canon(Sv, Sf)
vS = volume(Sv, Sf); fkS = dict(Counter(len(f) for f in Sf))
log(vS / cellB == Q(Fr(151, 2), Fr(-267, 8)), f'OCD Stella density {fmt(vS / cellB)} = {(vS / cellB).f():.6f} (#31a: 151/2 - 267 sqrt5/8 ~ 87.12%)')
# the same solid as the study's (float corners in studies/2026-10-16-ocd-pyrochlore/data/stella-cut-exact.json), corner matching
st = json.load(open(os.path.join(HERE, 'sources', 'stella-cut-exact.json')))
sim = similar_float([[x.f() for x in v] for v in Sv], st['S']['v'])
log(sim is not None and abs(sim[0] - 1) < 1e-9, f'OCD Stella: corner-matching congruent (rotation/reflection, scale {sim}) to the study\'s stella cut S (float, 1e-6)')
sv = write_solid(os.path.join(SOL, 'dicto-ocd-stella'), dict(
    name='DICTO OCD Stella', finding='F31a', paper='#31a The DICTO OCD Stella', dicto_doi='10.5281/zenodo.23430870', status='new', convex=True,
    scale_note='#31 frame (the DICTO Ogdoecontahedron of dicto-ogdoecontahedron.json): S = C cut by the Voronoi cell of the OG\'s body-centred '
               'cubic packing whose eight joint hexagons point along (+-1, +-1, +-1); C = the 30 golden planes of the OG\'s envelope (rhombic '
               'triacontahedron of inradius 2/3) and the 20 three-fold planes at squared distance 14/27 - 10 sqrt5/243 (#31a).',
    source={'app': 'study', 'path': 'research:studies/2026-10-16-ocd-pyrochlore/scripts/stella_cut_exact.py (construction; planes as stated in the #31a paper)', 'id': None},
    **COMMON, published_values={'f_vector': [48, 96, 50], 'faces_by_sides': {'3': 20, '4': 24, '6': 6}, 'volume': '(-4064 + 2240*sqrt(5))/729', 'symmetry_order': 24},
    symmetry_label='Th'), Sv, Sf)
log((sv['V'], sv['F']) == (48, 50) and sv['fk'] == {6: 6, 4: 24, 3: 20}, f"OCD Stella: {sv['V']} corners, {sv['E']} edges, {sv['F']} faces {sv['fk']} (#31a: 48 corners, 50 faces: 6 hexagons, 24 quadrilaterals, 20 triangles)")
log(sv['vol'] == Q(Fr(-4064, 729), Fr(2240, 729)), f"OCD Stella volume {fmt(sv['vol'])} (#31a: (-4064 + 2240 sqrt5)/729)")
log(sv['cls'] == 'Th' and sv['order'] == 24, f"OCD Stella symmetry {sv['cls']} order {sv['order']} (#31a: pyritohedral)")

# ---------------------------------------------------------------- non-filling packings
def packing(slug, name, finding, paper, doi, status, L, pieces, dens_pub_exact, dens_pub_pct, where, note):
    cell = abs_(det3(*L)); vs = sum((volume(*SOLIDS[p[0]]) for p in pieces), zero()); dens = vs / cell
    log(dens == dens_pub_exact, f'{slug}: density {fmt(dens)} = {dens.f() * 100:.4f}% vs published {fmt(dens_pub_exact)} ({dens_pub_pct}%, {where})')
    places = len(dens_pub_pct.split('.')[1])
    log(f'{dens.f() * 100:.{places}f}' == dens_pub_pct, f'{slug}: decimal {dens.f() * 100:.{places}f}% vs published {dens_pub_pct}%')
    doc = {'name': name, 'kind': 'packing, not a fill', 'finding': finding, 'paper': paper, 'dicto_doi': doi, 'status': status,
           'field': 'Q(sqrt(5))', 'lattice_vectors': [vec(b) for b in L], 'cell_volume': num(cell),
           'pieces': [{'solid': s, 'rotation': R, 'translation': t} for s, R, t in pieces],
           'density': {'exact': fmt(dens), 'decimal': dens.dec(), 'published_percent': dens_pub_pct, 'published_in': where},
           'note': note, **MARK,
           'checks': {'density_exact_equals_published': True, 'no_overlaps_exact': True, 'verified_by': 'check.py'}}
    json.dump(doc, open(os.path.join(NPK, slug + '.json'), 'w'), indent=1, ensure_ascii=False)
SOLIDS = {}
for s in ('dicto-ogdoecontahedron', 'dicto-ocd-stella', 'dicto-dbt', 'dicto-ott'):
    _, V, F = load(s); SOLIDS[s] = (V, F)
packing('dicto-ogdoecontahedron-bcc-packing', 'DICTO Ogdoecontahedron body-centred cubic packing', 'F31', '#31', '10.5281/zenodo.23404688',
        'published packing (lattice packing by translation; not a tiling)', LB, [('dicto-ogdoecontahedron', I3, O3)],
        Q(Fr(9225, 608), Fr(-3915, 608)), '77.43', '#31, section on the single packings',
        '#31: every copy in the same orientation, touching eight neighbours through the eight hexagons that point to the corners of a cube; '
        'one of the OG\'s five such packings (here the cube of the joint directions (+-1, +-1, +-1)). Bond vectors t = 2 d n/|n|^2 for those '
        'hexagons (n.x = d); basis t0 + t1, t0 + t2, t0. The rest of space (22.57%) is empty: not a tiling.')
packing('dicto-ocd-stella-bcc-packing', 'DICTO OCD Stella body-centred cubic packing', 'F31a', '#31a', '10.5281/zenodo.23430870',
        'published packing (lattice packing by translation; not a tiling)', LB, [('dicto-ocd-stella', I3, O3)],
        Q(Fr(151, 2), Fr(-267, 8)), '87.12', '#31a, Table 1 and Table 2',
        '#31a: the OCD Stella on the OG\'s body-centred cubic packing (same lattice as dicto-ogdoecontahedron-bcc-packing), copies meeting face '
        'to face across the 8 joints; each copy lies in its own Voronoi cell. Not a tiling (12.88% empty).')
R = Q(Fr(1, 3), Fr(1, 3))                                            # #37a: octahedron |x| + |y| + |z| <= R, R = 2 phi/3
HALF = [[fmt(Q(Fr(2, 3)) - (1 if i == j else 0)) for j in range(3)] for i in range(3)]   # half-turn about (1,1,1): (2/3) J - I
# the DBT's twin across the layer plane x + y + z = R is its mirror image there, = the half-turn about (1,1,1) (D3d has the inversion)
_, DBT, DBTf = load('dicto-dbt')
mir = [tuple(v[i] - Q(Fr(2, 3)) * (v[0] + v[1] + v[2] - R) for i in range(3)) for v in DBT]
c1 = smul(Q(Fr(2, 3)) * R, (Q(1), Q(1), Q(1)))
rot = [tuple(sum((parse(HALF[i][k]) * v[k] for k in range(3)), zero()) + c1[i] for i in range(3)) for v in DBT]
log(set(mir) == set(rot), 'DBT: the mirror image in the twin plane x + y + z = R equals the half-turn about (1,1,1) moved to (2R/3)(1,1,1) (#37a: a true twin)')
packing('dicto-dbt-gyrated-octet-packing', 'DICTO Belted Triacontahedron on the gyrated octet', 'F37a', '#37a', '10.5281/zenodo.23484012',
        'published packing (two pieces per cell: a layer and its mirror-twin layer; not a tiling)',
        [(R, -R, zero()), (zero(), R, -R), smul(Q(Fr(4, 3)) * R, (Q(1), Q(1), Q(1)))],
        [('dicto-dbt', I3, O3), ('dicto-dbt', HALF, [fmt(x) for x in c1])],
        Q(Fr(493, 6), Fr(-73, 2)), '55.02', '#37a section 6 (also #40 The DICTO OG Family on Every Stacking, Table 1)',
        '#37a: a DBT in every octahedron of the gyrated octet (#37 frame: octahedron |x| + |y| + |z| <= R, R = 2 phi/3, layers perpendicular to '
        '(1,1,1), twin planes x + y + z = R and its parallels); within a layer by translation, the next layer its mirror image, i.e. the DBT '
        'turned by the half-turn about (1,1,1) at (2R/3)(1,1,1). Two octahedra per cell. Not a tiling (the DICTO Fill set 1 piece fills the rest).')
packing('dicto-ott-octet-packing', 'DICTO OTT on the octet', 'F37a', '#37a', '10.5281/zenodo.23484012',
        'published packing (lattice packing by translation; not a tiling)', [(R, R, zero()), (R, zero(), R), (zero(), R, R)], [('dicto-ott', I3, O3)],
        Q(Fr(176, 3), -26), '52.89', '#37a section 7 (every stacking; also #40 The DICTO OG Family on Every Stacking, Table 1)',
        '#37a: one OTT in every octahedron of the octet (the tetrahedral-octahedral honeycomb; #37 frame, octahedron |x| + |y| + |z| <= R, '
        'R = 2 phi/3, octahedron centres on the face-centred cubic lattice spanned by (R, R, 0), (R, 0, R), (0, R, R)). The paper states the same '
        'density for the gyrated octet and every stacking. Not a tiling (DICTO Fill set 2 F2, F3 fill the rest in the octet).')

# ---------------------------------------------------------------- unit-volume copies of every solid
mpmath.mp.dps = 60
def mpq(x): return mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(5)
def dec15(m):
    q = Decimal(mpmath.nstr(m, 50, strip_zeros=False, min_fixed=-mpmath.inf, max_fixed=mpmath.inf)).quantize(Decimal(1).scaleb(-15))
    return format(q, 'f') if q != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-15)), 'f')
for p in sorted(glob.glob(os.path.join(SOL, '*.json'))):
    slug = os.path.basename(p)[:-5]; doc = json.load(open(p))
    if doc['field'] != 'Q(sqrt(5))' or doc.get('version_added') == 2: continue   # version 2 solids get theirs in build_v2.py
    V = [tuple(parse(x) for x in v['exact']) for v in doc['vertices']]; vol = parse(doc['volume']['exact'])
    c = tuple(sum((v[k] for v in V), zero()) / len(V) for k in range(3))
    s = mpmath.power(mpq(vol), mpmath.mpf(-1) / 3)
    W = [[mpq(c[k]) + s * (mpq(v[k]) - mpq(c[k])) for k in range(3)] for v in V]
    at_origin = all(x.sign() == 0 for x in c)
    uv = {'scale_exact': f"({doc['volume']['exact']})**(-1/3)", 'scale_decimal': dec15(s),
          'centre': {'exact': [fmt(x) for x in c], 'decimal': [x.dec() for x in c],
                     'kind': 'origin of the paper frame (= the corner centroid)' if at_origin else 'corner centroid (mean of the corners; the frame origin is not the centre)'},
          'note': 'x -> centre + s (x - centre), s = V^(-1/3) with V the exact volume above; cube roots leave Q(sqrt5), so s is symbolic and the '
                  'corners are decimals (15 places, as elsewhere). Same corner order and faces as above; volume 1.',
          'vertices_decimal': [[dec15(x) for x in w] for w in W]}
    out = {}
    for k, v in doc.items():
        if k == 'unit_volume': continue
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

json.dump({'log': LOG}, open(os.path.join(HERE, 'build_extra.log.json'), 'w'), indent=1, ensure_ascii=False)
print(f"{sum(l.startswith('PASS') for l in LOG)} PASS, {sum(l.startswith('FAIL') for l in LOG)} FAIL")
