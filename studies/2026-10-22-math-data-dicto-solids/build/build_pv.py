# DICTO · dictospheres.com — builds the dataset solids whose geometry lives in Polyhedraverse (krp-core POLYHEDRA), 2026-10-22.
# Either an exact construction matched to Polyhedraverse's float corners by a corner-matching similarity test, or Polyhedraverse's
# float corners recovered exactly in Q(sqrt5) (sympy nsimplify) and then PROVED: exact planarity of every face, closure, Euler,
# exact volume equal to the published value. Also writes the lattice packings of the parallelohedra (F1, F7).
import itertools, json, os, sys
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
import sympy

OUT = os.path.join(HERE, '..', 'solids'); PK = os.path.join(HERE, '..', 'packings')
os.makedirs(PK, exist_ok=True)
PV = json.load(open(os.path.join(HERE, 'sources', 'pv-selected.json')))
LOG = []; SUMMARY = {}
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True)
z, one = QF(0), QF(1)
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).'}
KREC = '10.5281/zenodo.23173809'   # Kaleidohedra by DICTO (findings archive), concept DICTO DOI

def parse(s):
    e = sympy.expand(sympy.sympify(s)); a = Fr(0); b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        c = Fr(int(sympy.fraction(c)[0]), int(sympy.fraction(c)[1]))
        if t == 1: a += c
        elif t == sympy.sqrt(5): b += c
        else: raise ValueError(s)
    return QF(a, b)

def recover(x, tol):
    if abs(x) < tol: return z
    e = sympy.nsimplify(x, [sympy.sqrt(5)], tolerance=tol)
    q = parse(str(e)); assert abs(q.f() - x) < tol, (x, e)
    return q

def emit(slug, meta, V, F, published=None, pvid=None):
    V, F = canon(V, F)
    meta = dict(meta); meta['published_values'] = dict(published or {})
    r = write_solid(os.path.join(OUT, slug), meta, V, F)
    log(r['cls'] == r['label'], f"{slug}: symmetry {r['cls']} (classified) vs stated {r['label']}")
    for k, v in (published or {}).items():
        if k == 'volume': log(r['vol'] == parse(v), f"{slug}: volume {fmt(r['vol'])} vs published {v}")
        elif k == 'f_vector': log((r['V'], r['E'], r['F']) == tuple(v), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs published {tuple(v)}")
        elif k == 'faces_by_sides': log({str(a): b for a, b in r['fk'].items()} == {str(a): b for a, b in v.items()}, f"{slug}: faces {r['fk']} vs published {v}")
    if pvid:
        s = similar_float([[x.f() for x in v] for v in V], PV[pvid]['vertices'])
        log(s is not None, f'{slug}: matches Polyhedraverse {pvid} corner for corner up to similarity (scale PV/dataset, max error) = {s}')
    SUMMARY[slug] = {'V': r['V'], 'E': r['E'], 'F': r['F'], 'volume': fmt(r['vol']), 'order': r['order'], 'rot': r['proper'], 'inv': r['inv'], 'faces': r['fk'], 'sym': r['cls']}
    print(slug, SUMMARY[slug], flush=True)
    return V, F

# ------------------------------------------------------------------ F1 / F7 parallelohedra on icosahedral two-fold directions
Ic = []
for v in [(z, one, PHI)]:
    for c in [v, (v[2], v[0], v[1]), (v[1], v[2], v[0])]:
        for s in itertools.product((1, -1), repeat=3):
            Ic.append(tuple(x * si for x, si in zip(c, s)))
Ic = list(dict.fromkeys(Ic)); Vi, Fi = hull(Ic)
axes = []
for a, b in edges_of(Fi):
    m = mul(one / (2 * PHI), add(Vi[a], Vi[b]))          # unit vector (midradius phi)
    assert dot(m, m) == one
    if not any(m == mul(-1, w) for w in axes): axes.append(m)
assert len(axes) == 15
C60, C72, C36 = QF(Fr(1, 2)), QF(Fr(-1, 4), Fr(1, 4)), PHI / 2
def acos_kind(u, v):
    c = dot(u, v); c = c if c.sign() >= 0 else -c
    return {C60: 60, C72: 72, C36: 36, z: 90}.get(c)
def zonotope(E):
    pts = [tuple(sum((s[i] * E[i][k] / 2 for i in range(len(E))), z) for k in range(3)) for s in itertools.product((1, -1), repeat=len(E))]
    return hull(pts)
rd = None
for S4 in itertools.combinations(range(15), 4):
    kinds = sorted(acos_kind(axes[i], axes[j]) for i, j in itertools.combinations(S4, 2))
    if kinds == [60, 60, 60, 72, 72, 72]:
        V, F = zonotope([axes[i] for i in S4])
        if volume(V, F) == PHI * PHI: rd = S4; break
log(rd is not None, 'F1: four icosahedral two-fold directions meeting at 60 deg three times and 72 deg three times; zonotope volume phi^2 exactly')
E4 = [axes[i] for i in rd]
DIRNOTE = ('Exact frame: edge 1; the edge directions are unit vectors along two-fold axes of the icosahedron (0, +-1, +-phi) cyclic '
           '(its edge midpoints divided by phi). The solid is the zonotope sum of the segments [-e/2, e/2] of its edge directions e (centred at the origin).')
def lattice_of(V, F):
    T = [mul(QF(2), tuple(sum((V[i][k] for i in f), z) / len(f) for k in range(3))) for f in F]
    vol = volume(V, F)
    for B in itertools.combinations(T, 3):
        dt = det3(*B)
        if dt == vol or dt == -vol:
            ok = True
            for t in T:                                   # every face translation an integer combination of B
                co = [det3(*(t if k == c else B[k] for k in range(3))) / dt for c in range(3)]
                if not all(x.b == 0 and x.a.denominator == 1 for x in co): ok = False; break
            if ok: return list(B), T
    raise AssertionError('no lattice basis')
def emit_packing(slug, solid_slug, V, F, name, finding, doi, note):
    B, T = lattice_of(V, F)
    doc = {'name': name, 'finding': finding, 'dicto_doi': doi, 'status': 'published fill (lattice tiling by translation)',
           'field': 'Q(sqrt(5))', 'lattice_vectors': [{'exact': [fmt(x) for x in b], 'decimal': [x.dec() for x in b]} for b in B],
           'cell_volume': {'exact': fmt(abs_(det3(*B))), 'decimal': abs_(det3(*B)).dec()},
           'pieces': [{'solid': solid_slug, 'rotation': [['1', '0', '0'], ['0', '1', '0'], ['0', '0', '1']], 'translation': ['0', '0', '0']}],
           'note': note + ' Lattice basis chosen among the face-pair translations (twice each face centre); every face-pair translation is an integer combination of it.',
           'credit': 'DICTO', 'creator_mark': 'Created by DICTO · dictospheres.com', 'licence': 'CC BY-SA 4.0',
           'checks': {'volume_sum_equals_cell_volume': True, 'no_overlaps_exact': True, 'verified_by': 'check.py'}}
    json.dump(doc, open(os.path.join(PK, slug + '.json'), 'w'), indent=1, ensure_ascii=False)
abs_ = lambda x: x if x.sign() >= 0 else -x

V, F = zonotope(E4)
emit('dicto-skewed-rhombic-dodecahedron', dict(name='DICTO skewed rhombic dodecahedron', finding='F1', paper='Kaleidohedra findings archive', dicto_doi=KREC,
     status='new member of a known family (rhombic-dodecahedron parallelohedra: Fedorov 1885; Lalvani US 5,623,790, 1997)', convex=True, symmetry_label='auto',
     scale_note=DIRNOTE + ' Four directions, meeting at 60 deg three times and 72 deg three times.',
     source={'app': 'Polyhedraverse', 'path': 'krp-core src/geometry-extensions/dicto-fcc.js', 'id': 'DICTO_SKEWED_RD'}, **COMMON),
     V, F, published={'volume': '(3 + sqrt(5))/2', 'f_vector': (14, 24, 12)}, pvid='DICTO_SKEWED_RD')
Vrd, Frd = canon(V, F)
emit_packing('dicto-skewed-rhombic-dodecahedron-lattice', 'dicto-skewed-rhombic-dodecahedron', Vrd, Frd, 'DICTO FCC: the DICTO skewed rhombic dodecahedron tiling a sheared FCC lattice', 'F1', KREC,
             'F1: the solid tiles space by translation (DICTO FCC).')
eds = {}
for i in range(15):
    if i in rd: continue
    ks = sorted(acos_kind(axes[i], axes[j]) for j in rd)
    if ks.count(36) == 2 and ks.count(90) == 0:
        V, F = zonotope(E4 + [axes[i]]); vol = volume(V, F)
        if vol == PHI * PHI + 2: eds.setdefault('16', (V, F, i))
        if vol == PHI * PHI * PHI + QF(Fr(1, 2)): eds.setdefault('18', (V, F, i))
log(set(eds) == {'16', '18'}, 'F7: fifth directions (36 deg twice) giving volumes phi^2 + 2 (ED F16) and phi^3 + 1/2 (ED F18) found exactly')
for key, vol, fk in [('16', 'sqrt(5)/2 + 7/2', {4: 8, 6: 4}), ('18', '2 + sqrt(5) + 1/2', {4: 8, 6: 4})]:
    V, F, i = eds[key]
    emit(f'dicto-skewed-ed-{key}', dict(name=f'DICTO skewed elongated dodecahedron (ED F{key})', finding='F7', paper='Kaleidohedra findings archive', dicto_doi=KREC,
         status='new member of a known family (elongated-dodecahedron parallelohedra: Fedorov 1885; Lalvani US 5,623,790)', convex=True, symmetry_label='auto',
         scale_note=DIRNOTE + ' The four directions of the DICTO skewed rhombic dodecahedron plus a fifth meeting two of them at 36 deg.',
         source={'app': 'Polyhedraverse', 'path': 'krp-core src/geometry-extensions/dicto-fcc.js', 'id': f'DICTO_SKEWED_ED_{key}'}, **COMMON),
         V, F, published={'volume': vol, 'f_vector': (18, 28, 12), 'faces_by_sides': fk}, pvid=f'DICTO_SKEWED_ED_{key}')
    Vc, Fc = canon(V, F)
    emit_packing(f'dicto-skewed-ed-{key}-lattice', f'dicto-skewed-ed-{key}', Vc, Fc, f'DICTO skewed ED F{key} lattice tiling', 'F7', KREC,
                 f'F7: ED F{key} is a parallelohedron and tiles space by translation.')

# ------------------------------------------------------------------ recovered from Polyhedraverse floats, proved exactly
def from_pv(pvid, tol, convex):
    P = PV[pvid]; Vx = [tuple(recover(x, tol) for x in v) for v in P['vertices']]
    if convex: return hull(Vx)
    F = [list(f) for f in P['faces']]
    # exact planarity of the given faces, closure, orientation
    for f in F:
        n = cross(sub(Vx[f[1]], Vx[f[0]]), sub(Vx[f[2]], Vx[f[0]]))
        assert all(dot(n, sub(Vx[i], Vx[f[0]])).sign() == 0 for i in f), 'face not planar'
    check_closed(Vx, F)
    if volume(Vx, F).sign() < 0: F = [f[::-1] for f in F]
    return Vx, F

V, F = from_pv('DRAGON_JEWEL', 1e-12, False)
emit('dicto-jewel', dict(name='DICTO Jewel (EKP windows; first called Dragon Jewel)', finding='F10', paper='#41 The DICTO Jewel', dicto_doi='10.5281/zenodo.23496353',
     status='new', convex=False, symmetry_label='auto',
     scale_note='Polyhedraverse frame: the regular dodecahedron of edge 1, corners (+-phi/2, +-phi/2, +-phi/2) and (0, +-1/2, +-phi^2/2) cyclic, in its EKP cell (cube of edge phi); the Jewel is this dodecahedron with its six face-neighbours\' stella octangulas carved out. #41 states volume 12 on cells of edge 2 (3/16 when the Hexa cube has edge 1); at this scale (cell edge phi) that is 12 (phi/2)^3 = 3 + 3 sqrt5/2.',
     source={'app': 'Polyhedraverse', 'path': 'krp-core src/polyhedra (DRAGON_JEWEL)', 'id': 'DRAGON_JEWEL'}, **COMMON),
     V, F, published={'faces_by_sides': {3: 48, 4: 12}, 'volume': '3 + 3*sqrt(5)/2'})
for pvid, slug, nm, vol in [('DICTO_DODECA13_WEDGE', 'dicto-dodeca-13-wedge', 'DICTO Dodeca-13 Wedge', '(2 + sqrt(5))/20'),
                            ('DICTO_DODECA13_NEEDLE', 'dicto-dodeca-13-needle', 'DICTO Dodeca-13 Needle', '(45 - 19*sqrt(5))/600')]:
    V, F = from_pv(pvid, 2e-9, True)
    emit(slug, dict(name=nm, finding='F13', paper='#13 The DICTO Dodeca-13', dicto_doi='10.5281/zenodo.23284281', status='new', convex=True, symmetry_label='auto',
         scale_note='Polyhedraverse frame of the 13-dodecahedron cluster, dodecahedra of edge 1 (Polyhedraverse corners recovered exactly in Q(sqrt5) and proved; #13 volumes are at edge 1: wedge phi^3/20, needle (45 - 19 sqrt5)/600).',
         source={'app': 'Polyhedraverse', 'path': 'krp-core src/polyhedra/dodeca13Data.js', 'id': pvid}, **COMMON), V, F, published={'volume': vol})
# The four #43 rays/Aktis (OTT_TRIANGLE_RAY, OTT_RHOMBIC_RAY, DELTOID_AKTIS, HEX_AKTIS) were tried: Polyhedraverse stores them in a turned
# frame whose coordinates are not in Q(sqrt5) (nsimplify gives nested radicals), so they are left out (see REPORT.md).

json.dump({'log': LOG, 'summary': SUMMARY}, open(os.path.join(HERE, 'build_pv.log.json'), 'w'), indent=1)
print('FAILS:', sum(1 for l in LOG if l.startswith('FAIL')))
