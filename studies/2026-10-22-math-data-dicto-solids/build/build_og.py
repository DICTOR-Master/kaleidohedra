# DICTO · dictospheres.com — builds the OG-family solids of the math-data dataset, exact in Q(sqrt5) (2026-10-22).
# Constructions follow the published papers (sources named per solid); every corner is exact, every hull proved (exactlib.hull).
# Published values are compared exactly where the paper states them; mismatches are logged, never "fixed".
import itertools, json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *

OUT = os.path.join(HERE, '..', 'solids'); os.makedirs(OUT, exist_ok=True)
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True)
def q(s):
    a, b = s.split('|'); return QF(Fr(a), Fr(b), 5)
h = QF(Fr(1, 2)); z = QF(0); one = QF(1)
SUMMARY = {}

def cyc(v): return [v, (v[2], v[0], v[1]), (v[1], v[2], v[0])]
def signs(v):
    out = set()
    for s in itertools.product((1, -1), repeat=3):
        out.add(tuple(x * si if x.sign() else x for x, si in zip(v, s)))
    return out
def orbit(base):
    S = set()
    for b in base:
        for c in cyc(b): S |= signs(c)
    return list(S)

def emit(slug, meta, V, F, published=None):
    V, F = canon(V, F)
    pub = published or {}
    meta = dict(meta); meta['published_values'] = {k: v for k, v in pub.items()}
    r = write_solid(os.path.join(OUT, slug), meta, V, F)
    for k, v in pub.items():
        if k == 'volume': log(fmt(r['vol']) == v or r['vol'] == parse(v), f"{slug}: volume {fmt(r['vol'])} vs published {v}")
        elif k == 'f_vector': log((r['V'], r['E'], r['F']) == tuple(v), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs published {tuple(v)}")
        elif k == 'faces_by_sides': log({str(a): b for a, b in r['fk'].items()} == {str(a): b for a, b in v.items()}, f"{slug}: faces by sides {r['fk']} vs published {v}")
        elif k == 'symmetry_order': log(r['order'] == v, f"{slug}: symmetry order {r['order']} vs published {v}")
        elif k == 'squared_edge_lengths': log(sorted(fmt(x) for x in r['el']) == sorted(v), f"{slug}: squared edges {[fmt(x) for x in r['el']]} vs published {v}")
    log(r['cls'] == r['label'], f"{slug}: symmetry {r['cls']} (classified) vs stated {r['label']}")
    SUMMARY[slug] = {'V': r['V'], 'E': r['E'], 'F': r['F'], 'volume': fmt(r['vol']), 'order': r['order'], 'rot': r['proper'], 'inv': r['inv'], 'faces': r['fk']}
    print(slug, SUMMARY[slug], flush=True)
    return V, F

def parse(s):
    import sympy
    e = sympy.expand(sympy.sympify(s)); cd = e.as_coefficients_dict(); a = Fr(0); b = Fr(0)
    for t, c in cd.items():
        c = Fr(int(sympy.fraction(c)[0]), int(sympy.fraction(c)[1]))
        if t == 1: a += c
        elif t == sympy.sqrt(5): b += c
        else: raise ValueError(s)
    return QF(a, b, 5)

def similar(A, B):
    """corner-matching congruence up to scale (DICTO's rule): same corner count, and B = k * P(A) for a signed coordinate
    permutation P and a scale k in Q(sqrt5) (both centred at the origin). Returns k^2 or None."""
    if len(A) != len(B): return None
    ra = max(dot(v, v) for v in A); rb = max(dot(v, v) for v in B); k2 = rb / ra
    try: k = qsqrt(k2)
    except Exception: return None
    SB = set(B)
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            if {tuple(k * sg[i] * v[perm[i]] for i in range(3)) for v in A} == SB: return k2
    return None

OGUPVOL = parse('(525 + 185*sqrt(5))/57')
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).'}

# ---------------------------------------------------------------- UP frame (#38, #39): ID of radius phi, standard coordinates
I = orbit([(z, h, PHI / 2)])                    # icosahedron edge 1 (corners (0, +-1/2, +-phi/2) cyclic)
assert len(I) == 12
VI, FI = hull(I)
ID = list({add(VI[a], VI[b]) for f in FI for a, b in itertools.combinations(f, 2)})
assert len(ID) == 30 and all(dot(v, v) == PHI * PHI for v in ID)
VID, FID = hull(ID)
RTv, RTf = ustep(ID)
GTIv, GTIf = ustep(RTv)
FPDv, FPDf = ustep(GTIv)
IDback, _ = ustep(FPDv)
k = QF(35, -15)                                  # 10/phi^4 = 35 - 15 sqrt5 (#38)
log(set(IDback) == {mul(k, v) for v in ID}, '#38 cycle: T^4(ID) = (35 - 15 sqrt5) ID = (10/phi^4) ID exactly')
UPFRAME = ('UP frame of #38/#39: icosidodecahedron of circumradius phi with corners (+-phi,0,0) cyclic and '
           '(+-1/2, +-phi/2, +-phi^2/2) cyclic (twice the edge midpoints of the icosahedron (0, +-1/2, +-phi/2) cyclic, edge 1); '
           'T(S) = {x : v.x <= v.v for every corner v of S}.')
emit('dicto-gti', dict(name='DICTO GTI (golden truncated icosahedron)', finding='F38', paper='#38 Universal PiTet', dicto_doi='10.5281/zenodo.23463305',
     status='new', convex=True, symmetry_label='Ih', scale_note=UPFRAME + ' GTI = T(T(ID)).',
     source={'app': 'study', 'path': 'research:studies/2026-10-19-five-fold-octet/exact_cycle.py', 'id': None}, **COMMON), GTIv, GTIf)
emit('dicto-fpd', dict(name='DICTO FPD (flat pentakis dodecahedron)', finding='F38', paper='#38 Universal PiTet', dicto_doi='10.5281/zenodo.23463305',
     status='new', convex=True, symmetry_label='Ih', scale_note=UPFRAME + ' FPD = T(GTI); T(FPD) = (35 - 15 sqrt5) ID.',
     source={'app': 'study', 'path': 'research:studies/2026-10-19-five-fold-octet/exact_cycle.py', 'id': None}, **COMMON), FPDv, FPDf)

# OG in the UP frame (exact_upward.py construction): 30 ID corners + 60 points 2c - v in each ID triangle + 12 apexes
T3 = [[VID[j] for j in f] for f in FID if len(f) == 3]
cent = lambda P: tuple(sum((p[k] for p in P), z) / len(P) for k in range(3))
A5 = [v for v in RTv if len([w for w in ID if (dot(v, w) - dot(w, w)).sign() == 0]) == 5]
X = list(dict.fromkeys(tuple(2 * cent(t)[k] - v[k] for k in range(3)) for t in T3 for v in t))
apex = []
for a5 in A5:
    cs = sorted(ID, key=lambda v: -dot(v, a5).f())[:5]; xs = sorted(X, key=lambda v: -dot(v, a5).f())[:5]; c0 = cs[0]
    x2 = sorted(xs, key=lambda v: sum((v[k] - c0[k]).f() ** 2 for k in range(3)))[:2]
    n = cross(sub(x2[0], c0), sub(x2[1], c0)); t_ = dot(n, c0) / dot(n, a5); apex.append(mul(t_, a5))
OGup = ID + X + apex
OGv, OGf = hull(OGup)
log(len(OGv) == 102 and len(OGf) == 80, 'UP-frame OG: 102 corners, 80 faces')
log(volume(OGv, OGf) == OGUPVOL, '#39: UP-frame OG volume = (525 + 185 sqrt5)/57 exactly (published, #39 section 1)')

# ---------------------------------------------------------------- Dharma frame (#28 V2): TI edge 1/phi, midsphere 3/2
TI = orbit([(z, one, 3 * PHI), (one, 2 + PHI, 2 * PHI), (PHI, QF(2), PHI ** 3 if False else PHI * PHI * PHI)])
TI = [mul(one / (2 * PHI), v) for v in TI]
TIv, TIf = hull(TI)
log(len(TIv) == 60 and len(TIf) == 32, 'truncated icosahedron: 60 corners, 32 faces (edge 1/phi)')
rho2 = QF(Fr(9, 4))
hexpoles = [mul(rho2 / c, n) for (n, c), f in zip(face_planes(TIv, TIf), TIf) if len(f) == 6]
Hv, Hf = hull(TIv + hexpoles)
DHARMA = ('Dharma frame of #28 V2: truncated icosahedron of edge 1/phi (midsphere radius 3/2), corners (0, +-1, +-3phi), '
          '(+-1, +-(2+phi), +-2phi), (+-phi, +-2, +-phi^3), even (cyclic) permutations, all times 1/(2phi). The Hecatodihedron is the hull '
          'of these 60 corners and the 20 poles of the hexagon planes in the midsphere (the canonical pentakis dodecahedron\'s three-fold corners).')
emit('dicto-hecatodihedron', dict(name='DICTO Truncated-Icosahedral Hecatodihedron (DICTO Hecatodihedron, TIH)', finding='F28', paper='#28',
     dicto_doi='10.5281/zenodo.23360857', status='new (derived from a known solid: the joined truncated icosahedron jtI with its 12 five-fold corners cut flat; #28 V2)',
     convex=True, symmetry_label='Ih', scale_note=DHARMA,
     source={'app': 'Polyhedraverse', 'path': 'krp-core src/polyhedra/transitional.js (float, 6 decimals)', 'id': 'TRANS_DHARMA_80',
             'exact_form': '#28 V2 construction (kaleidohedra papers/tih/data/tih_v2_check.py), matched corner for corner to the Polyhedraverse floats (see build log)'}, **COMMON),
     Hv, Hf, published={'f_vector': (80, 180, 102), 'faces_by_sides': {3: 60, 4: 30, 5: 12}})
PVS = json.load(open(os.path.join(HERE, 'sources', 'pv-selected.json')))
sH = similar_float([[x.f() for x in v] for v in Hv], PVS['TRANS_DHARMA_80']['vertices'], tol=2e-4)  # PV stores 6 decimals; corners are >= 0.1 apart, so the match is unambiguous
log(sH is not None, f'dicto-hecatodihedron matches Polyhedraverse TRANS_DHARMA_80 corner for corner up to similarity (scale, max error) = {sH}')
# OG as the polar of H: #31 frame = reciprocation in the unit sphere
Ov, Of = hull(polar(Hv, Hf, one))
emit('dicto-ogdoecontahedron', dict(name='DICTO Ogdoecontahedron (OG)', finding='F31', paper='#31', dicto_doi='10.5281/zenodo.23404688',
     status='new (face arrangement known as the dual of L0(D), Antiprism; metric solid derived from the canonical pentakis dodecahedron with its 20 three-fold corners cut flat; #31 V2)',
     convex=True, symmetry_label='Ih',
     scale_note='#31 frame ("the scale of the reversed cycle, reciprocation in the unit sphere"): the polar, in the unit sphere, of the DICTO Hecatodihedron in the Dharma frame (dicto-hecatodihedron.json).',
     source={'app': 'study', 'path': 'kaleidohedra:papers/ogdoecontahedron/scripts/polar.py', 'id': None}, **COMMON),
     Ov, Of, published={'f_vector': (102, 180, 80), 'faces_by_sides': {4: 60, 6: 20}, 'volume': '(-1000 + 1240*sqrt(5))/1539',
                        'squared_edge_lengths': [fmt(parse('2/9 - 2*sqrt(5)/27')), fmt(parse('86/3249 + 2*sqrt(5)/361'))]})
kk = similar(Ov, OGv)
log(kk is not None, f'UP-frame OG (#38/#39 construction) is the #31 OG scaled (corner-matching test), scale^2 = {kk}')

# ---------------------------------------------------------------- #39 OG family: four steps up (T) and four down (reverse step)
up = ['dicto-kre', 'dicto-phe', 'dicto-tpp', 'dicto-dphp']
upn = ['DICTO KRE (Kite-Rhombic Enneacontahedron)', 'DICTO PHE (Pentagon-Hexagon Enneacontadihedron)', 'DICTO TPP (Triangle-Pentagon Polyhedron)',
       'DICTO DPHP (Decagon-Pentagon-Hexagon Polyhedron)']
st = json.load(open(os.path.join(HERE, 'sources', 'exact_upward.json')))['solids']
sd = json.load(open(os.path.join(HERE, 'sources', 'exact_downward.json')))['solids']
def r5(s):  # study repr 'a+br5'
    t = s[:-2]; i = t.index('+', 1)
    return QF(Fr(t[:i]), Fr(t[i + 1:]))
S = OGv
OGNOTE = (UPFRAME + ' The OG here is the #31 OG at the UP size (corners: the 30 ID corners, the 60 points 2c - v in each ID triangle '
          '(c its centre), and 12 apexes on the five-fold axes in the kite planes).')
for k_, (slug, nm) in enumerate(zip(up, upn)):
    S, F = ustep(S)
    pv = st[nm.split(' (')[0]]
    log(volume(S, F) == r5(pv['volume']), f'{slug}: volume equals the #39 study value {pv["volume"]}')
    emit(slug, dict(name=nm, finding='#39 (paper; no F number)', paper='#39 The DICTO OG Family', dicto_doi='10.5281/zenodo.23488944', status='new',
         convex=True, symmetry_label='Ih', scale_note=OGNOTE + f' This solid is T^{k_ + 1}(OG).',
         source={'app': 'study', 'path': 'research:studies/2026-10-19-five-fold-octet/exact_upward.py', 'id': None}, **COMMON),
         S, F, published={'f_vector': (pv['corners'], pv['edges'], pv['faces'])})
    S = list(S) if False else [S[i] for i in range(len(S))]
dn = ['dicto-tph', 'dicto-tqh', 'dicto-tqp', 'dicto-tqhd']
dnn = ['DICTO TPH', 'DICTO TQH', 'DICTO TQP', 'DICTO TQHD']
S, F = OGv, OGf
for k_, (slug, nm) in enumerate(zip(dn, dnn)):
    S, F = hull(rstep(S, F))
    pv = sd[f'down {k_ + 1}']
    log(volume(S, F) == r5(pv['volume']), f'{slug}: volume equals the #39 study value')
    emit(slug, dict(name=nm, finding='#39 (paper; no F number)', paper='#39 The DICTO OG Family', dicto_doi='10.5281/zenodo.23488944', status='new',
         convex=True, symmetry_label='Ih', scale_note=OGNOTE + f' This solid is the reverse step applied {k_ + 1} times to the OG (corners = foot points of the face planes of the solid above).',
         source={'app': 'study', 'path': 'research:studies/2026-10-19-five-fold-octet/exact_downward.py', 'id': None}, **COMMON),
         S, F, published={'f_vector': (pv['corners'], pv['edges'], pv['faces'])})

# ---------------------------------------------------------------- #35a, #35b closed forms (icosahedron (0,+-1,+-phi) cyclic, edge 2)
Ic = orbit([(z, one, PHI)])
Dc = orbit([(one, one, one), (z, PHI, one / PHI)])
assert len(Ic) == 12 and len(Dc) == 20
kM = PHI ** 5 / 9 if False else PHI * PHI * PHI * PHI * PHI / 9
Mv, Mf = hull(Ic + [mul(kM, v) for v in Dc])
emit('dicto-metaxyhexecontahedron', dict(name='DICTO Metaxyhexecontahedron', finding='F35 (paper #35a)', paper='#35a', dicto_doi='10.5281/zenodo.23430864',
     status='new as a named, distinguished member (the dodecahedron-icosahedron hull family is known)', convex=True, symmetry_label='Ih',
     scale_note='#35a closed form: hull of the icosahedron (0, +-1, +-phi) cyclic (edge 2) and (phi^5/9) times the dodecahedron (+-1, +-1, +-1), (0, +-phi, +-1/phi) cyclic.',
     source={'app': 'study', 'path': 'kaleidohedra:studies/2026-10-16-progenitors/scripts/progenitors_exact.py; closed form from the #35a paper', 'id': None}, **COMMON),
     Mv, Mf, published={'f_vector': (32, 90, 60), 'volume': '410/27 + 550*sqrt(5)/81', 'squared_edge_lengths': [fmt(parse('94/81 + 14*sqrt(5)/27')), fmt(parse('14/9 + 2*sqrt(5)/27'))]})
kP = QF(Fr(5, 6), Fr(1, 6))
Pv, Pf = hull(Ic + [mul(kP, v) for v in Dc])
emit('dicto-palintriacontahedron', dict(name='DICTO Palintriacontahedron', finding='F35 (paper #35b)', paper='#35b', dicto_doi='10.5281/zenodo.23430866',
     status='new as a named, distinguished member (the dodecahedron-icosahedron hull family is known)', convex=True, symmetry_label='Ih',
     scale_note='#35b closed form: hull of the icosahedron (0, +-1, +-phi) cyclic (edge 2) and k = 5/6 + sqrt5/6 times the dodecahedron (+-1, +-1, +-1), (0, +-phi, +-1/phi) cyclic.',
     source={'app': 'study', 'path': 'kaleidohedra:studies/2026-10-16-progenitors/scripts/progenitors_exact.py; closed form from the #35b paper', 'id': None}, **COMMON),
     Pv, Pf, published={'f_vector': (32, 90, 60), 'volume': '50/3 + 50*sqrt(5)/9', 'squared_edge_lengths': ['5/3', '20/9']})

# ---------------------------------------------------------------- #37a DBT and OTT (#37 frame: RT inradius 2/3)
for slug, fn, nm, lab, pubv, note in [
    ('dicto-dbt', 'dbt-exact.json', 'DICTO Belted Triacontahedron (DBT)', 'D3d', {'volume': '(-872 + 440*sqrt(5))/81', 'f_vector': (30, 60, 32)},
     'a rhombic triacontahedron truncated at its two three-fold corners on the (1,1,1) axis, along the long diagonals'),
    ('dicto-ott', 'cut8-exact.json', 'DICTO OTT (Octahedrally Truncated Triacontahedron)', 'Th', {'volume': '(-608 + 320*sqrt(5))/81'},
     'a rhombic triacontahedron truncated at its eight three-fold corners on the cube diagonals (the triacontahedron intersected with its octahedron)')]:
    Dd = json.load(open(os.path.join(HERE, 'sources', fn)))
    Vv, Ff = hull([tuple(q(c) for c in v) for v in Dd['V']])
    emit(slug, dict(name=nm, finding='F37a', paper='#37a (V3 for the OTT)', dicto_doi='10.5281/zenodo.23484012', status='new', convex=True, symmetry_label=lab,
         scale_note='#37 frame: ' + note + '; the triacontahedron has inradius 2/3 and the cuts are the planes x + y + z = +-R (DBT) or +-x +-y +-z = R (OTT), R = (1 + sqrt5)/3.',
         source={'app': 'study', 'path': 'research:studies/2026-10-19-og-gyrated-octet/' + fn, 'id': None}, **COMMON), Vv, Ff, published=pubv)

json.dump({'log': LOG, 'summary': SUMMARY}, open(os.path.join(HERE, 'build_og.log.json'), 'w'), indent=1)
print('FAILS:', sum(1 for l in LOG if l.startswith('FAIL')))
