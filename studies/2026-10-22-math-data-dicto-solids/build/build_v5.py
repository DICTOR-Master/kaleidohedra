# DICTO · dictospheres.com — math-data dataset VERSION 5 builder (2026-10-28). Created by DICTO. Licence CC BY-SA 4.0.
# Adds the named slices of DICTO's papers #63 (The White Queen 600-cell, version 3) and #65 (The Red Queen 120-cell, version 2), in Q(sqrt5).
# Names are DICTO's (28 October 2026). Codes W1-W62 and R1-R124 are the rows of the papers' appendix tables (direction order vertex-,
# edge-, face-, cell-first; heights from the centre to the tip). A cut inside a gap between two corner layers is taken at the gap's
# midpoint, as in the atlases (every height in the gap gives the same pattern of faces, with other lengths).
# Geometry is NOT re-derived from the papers' prose: q5.py + polytopes.py (the exact 600-cell and its directions, as in atlas600.py and
# build_v4.py's Humpty Dumpty) are executed; the 120-cell is built from the same 600-cell exactly as in atlas120.py: its corners are the
# centres of the 600 cells (mean of their 4 corners), two corners joined when their cells share a triangle; its directions are those of
# atlas120.json. Each slice: the corners at the cut height plus every edge crossing it, turned into R^3 by the quaternion map
# p -> Im(conj(d) p) (exact in Q(sqrt5), scaled by |d|), exact hull; checked against the atlas: f-vector, faces by sides, and the
# squared edge lengths / |d|^2 = the atlas values, exactly.
import json, os, sys
from fractions import Fraction as Fr
import mpmath, sympy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
SRC = os.path.join(HERE, 'sources'); SOL = os.path.join(HERE, '..', 'solids')
sys.path.insert(0, SRC)
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).', 'version_added': 5}
D63, D65 = '10.5281/zenodo.23690856', '10.5281/zenodo.23716140'
RB = 'research branch (k-research)'

def parse_any(s, d):
    e = sympy.expand(sympy.sympify(s)); a = Fr(0); b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        c = Fr(int(c.p), int(c.q))
        if t == 1: a += c
        elif d > 1 and t == sympy.sqrt(d): b += c
        else: raise ValueError(s)
    return QF(a, b, d)
def p5(s):
    import re
    return parse_any(re.sub(r'(^|[+\-(] *)√5', r'\g<1>1√5', s.strip()).replace('√5', '*sqrt(5)'), 5)

def emit(slug, meta, V, F, published):
    V, F = canon(V, F)
    meta = dict(meta, **COMMON); meta['published_values'] = published
    r = write_solid(os.path.join(SOL, slug), meta, V, F)
    for k, v in published.items():
        if k == 'f_vector': log((r['V'], r['E'], r['F']) == tuple(v), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs published {tuple(v)}")
        elif k == 'faces_by_sides': log({str(a): b for a, b in r['fk'].items()} == v, f"{slug}: faces {r['fk']} vs published {v}")
        elif k == 'squared_edge_lengths': log(set(r['el']) == {parse_any(x, 5) for x in v}, f"{slug}: squared edges vs published")
    log(True, f"{slug}: {r['V']}, {r['E']}, {r['F']} {dict(sorted(r['fk'].items()))}, volume {fmt(r['vol'])}, symmetry {r['cls']} ({r['order']})")
    return V, F, r

import q5 as q5m
from polytopes import polytope
P600 = polytope('600-cell'); V600 = P600['V']; E600 = P600['st']['E']
cq = lambda x: QF(x.a, x.b, 5)
q = lambda a, b=0: QF(Fr(a), Fr(b), 5)
# the 120-cell (Red Queen) from the 600-cell, as atlas120.py
K4 = P600['st']['K4']; T3 = P600['st']['T']
R120 = [tuple(sum((V600[i][k] for i in c), q5m.Q5(0)) / q5m.Q5(4) for k in range(4)) for c in K4]
tri_cells = {}
for ci, c in enumerate(K4):
    for t in ((c[0], c[1], c[2]), (c[0], c[1], c[3]), (c[0], c[2], c[3]), (c[1], c[2], c[3])): tri_cells.setdefault(tuple(sorted(t)), []).append(ci)
E120 = sorted({tuple(sorted(v)) for v in tri_cells.values() if len(v) == 2})
log(len(R120) == 600 and len(set(R120)) == 600 and len(E120) == 1200, 'the 120-cell: 600 corners (the 600-cell\'s cell centres), 1200 edges (cells sharing a triangle)')
A600 = json.load(open(os.path.join(SRC, 'atlas600.json'))); A120 = json.load(open(os.path.join(SRC, 'atlas120.json')))
ORDER = ['vertex-first', 'edge-first', 'face-first', 'cell-first']
def coded(items, P):
    out = {}; n = 0
    for d in ORDER:
        for o in sorted([o for o in items if o['direction'] == d], key=lambda o: o['h']):
            n += 1; out[P + str(n)] = o
    return out
CW, CR = coded(A600, 'W'), coded(A120['slices'], 'R')
DIRW = {k: v['d'] for k, v in P600['dirs'].items()}
DIRR = {k: tuple(q5m.Q5(p5(x).a, p5(x).b) for x in v['d_exact']) for k, v in A120['directions'].items()}

def cut(V, E, d, hv):
    hts = [q5m.dot(v, d) for v in V]
    P = [v for v, x in zip(V, hts) if x == hv]
    for a, b in E:
        ha, hb = hts[a], hts[b]
        if ((ha - hv) * (hb - hv)).sign() < 0:
            t = (hv - ha) / (hb - ha); P.append(tuple(x + t * (y - x) for x, y in zip(V[a], V[b])))
    dq = tuple(cq(x) for x in d); dot4 = lambda u, v: sum((x * y for x, y in zip(u, v)), q(0)); N = dot4(dq, dq)
    Y = []
    for p in P:
        pq = tuple(cq(x) for x in p); a0, av, b0, bv = dq[0], dq[1:], pq[0], pq[1:]
        assert dot4(dq, pq) == cq(hv)
        lin = tuple(a0 * bv[k] - b0 * av[k] for k in range(3)); cr = cross(av, bv); Y.append(tuple(lin[k] - cr[k] for k in range(3)))
    return Y, N

BS = 'Alicia Boole Stott, "On certain series of sections of the regular four-dimensional hypersolids", Verh. Kon. Akad. Wetensch. Amsterdam (1e Sectie) 7 no. 3 (1900)'
LIST = [  # code, slug, name, status (new / known), note
 ('W1', 'dicto-lion', 'Lion', 'new', 'the vertex-first central slice of the 600-cell (corner layer)'),
 ('W3', 'dicto-jabberwock', 'Jabberwock', 'new', 'vertex-first, corner layer: the largest all-triangle slice (72 corners, 140 triangles)'),
 ('W5', 'dicto-tweedledum', 'Tweedledum', 'new', 'vertex-first, corner layer; same counts as Tweedledee, another shape'),
 ('W22', 'dicto-tweedledee', 'Tweedledee', 'new', 'edge-first, corner layer; same counts as Tweedledum, another shape'),
 ('W28', 'dicto-mad-hatter', 'Mad Hatter', 'new', 'face-first, in a gap (cut at its midpoint); one of the four 144-corner slices, all different'),
 ('W30', 'dicto-march-hare', 'March Hare', 'new', 'face-first, in a gap (cut at its midpoint); one of the four 144-corner slices'),
 ('W43', 'dicto-jubjub', 'Jubjub', 'new', 'face-first, corner layer; all triangles'),
 ('W48', 'dicto-alicia', 'Alicia', 'known', 'the cell-first central slice: the middle section of ' + BS + '; named after her'),
 ('W49', 'dicto-alice', 'Alice', 'new', 'cell-first, in a gap (cut at its midpoint); one of the four 144-corner slices'),
 ('W51', 'dicto-white-rabbit', 'White Rabbit', 'new', 'cell-first, in a gap (cut at its midpoint); one of the four 144-corner slices'),
 ('W58', 'dicto-unicorn', 'Unicorn', 'known', 'cell-first, corner layer: one of the sections of ' + BS + '; same counts as the Lion, another shape'),
 ('W60', 'dicto-bandersnatch', 'Bandersnatch', 'known', 'cell-first, corner layer: one of the sections of ' + BS),
 ('R33', 'dicto-haigha', 'Haigha', 'new', 'Red Queen edge-first, the only slice with nine-sided faces'),
 ('R35', 'dicto-hatta', 'Hatta', 'new', 'Red Queen edge-first, the other 114-corner slice'),
 ('R77', 'dicto-red-king', 'Red King', 'new', 'Red Queen pentagon-first central slice, two regular decagons; the polar of the White Queen\'s edge-first shadow'),
 ('R80', 'dicto-walrus', 'Walrus', 'new', 'Red Queen pentagon-first, 120 corners'),
 ('R113', 'dicto-red-knight', 'Red Knight', 'new', 'Red Queen cell-first, in a gap (cut at its midpoint), 120 corners'),
 ('R115', 'dicto-white-knight', 'White Knight', 'new', 'Red Queen cell-first, in a gap (cut at its midpoint), 120 corners'),
]
BUILT = []
for code, slug, name, st, note in LIST:
    W = code[0] == 'W'; o = (CW if W else CR)[code]
    d = (DIRW if W else DIRR)[o['direction']]; hv = q5m.Q5(p5(o['height']).a, p5(o['height']).b)
    Y, N = cut(V600 if W else R120, E600 if W else E120, d, hv)
    if not W or not o['at_vertex_layer']:
        pass
    Vs, Fs = hull(list(dict.fromkeys(Y)))
    el_at = {p5(s) for s in o['edge_len2_exact']}
    el = {dot(sub(Vs[a], Vs[b]), sub(Vs[a], Vs[b])) for a, b in edges_of(Fs)}
    log({x / N for x in el} == el_at, f'{code} {name}: squared edge lengths / |d|^2 = the atlas values, exactly ({len(el_at)} values)')
    paper, doi = ('#63 The White Queen 600-cell (version 3)', D63) if W else ('#65 The Red Queen 120-cell (version 2)', D65)
    frame = ('frame: the 600-cell of #63 (circumradius 2, edge sqrt5 - 1)' if W else
             'frame: the 120-cell of #65, its corners the centres of the cells of the 600-cell of #63 (corner radius^2 7/4 + 3sqrt5/4, edge 1/2)') + \
            f", cut by the 3-space at height {o['height']} along the {o['direction']} direction d (atlas row {code}" + \
            ('' if o['at_vertex_layer'] else ', the midpoint of its gap') + '). Coordinates: Im(conj(d) p) for each point p of the cut, the slice turned into R^3 ' \
            'and scaled by |d|; divide lengths by |d| for the polytope\'s own scale.'
    status = ('known (' + note + '; the exact solid and the name are #63\'s and DICTO\'s)') if st == 'known' else \
             ('new (an exact slice of the ' + ('600-cell' if W else '120-cell') + ': ' + note + '; not found as a solid in the sources checked, ' + ('#63' if W else '#65') + ')')
    Vs, Fs, r = emit(slug, dict(name=name, finding='', paper=paper, dicto_doi=doi, convex=True, status=status, scale_note=frame,
        source={'app': 'study', 'path': RB + (': studies/2026-10-27-white-queen-600/scripts/atlas600.py' if W else ': studies/2026-10-27-white-queen-polar/scripts/atlas120.py')
                + ' (the cut); checked against data/' + ('atlas600.json' if W else 'atlas120.json') + f' row {code}', 'id': code},
        symmetry_label=None), Vs, Fs,
        {'f_vector': [o['V'], o['E'], o['F']], 'faces_by_sides': o['face_sizes'], 'squared_edge_lengths': [fmt(x * N) for x in sorted(el_at, key=lambda z: z.f())]})
    BUILT.append((slug, Vs))

# ------------------------------------------------------------------ 4. unit-volume copies (as build_v3.py; centre = the corner centroid)
mpmath.mp.dps = 60
def mpx(x): return mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(x.d)
def dec15(m):
    from decimal import Decimal
    qd = Decimal(mpmath.nstr(m, 50, strip_zeros=False, min_fixed=-mpmath.inf, max_fixed=mpmath.inf)).quantize(Decimal(1).scaleb(-15))
    return format(qd, 'f') if qd != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-15)), 'f')
ALL = BUILT
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

json.dump({'log': LOG}, open(os.path.join(HERE, 'build_v5.log.json'), 'w'), indent=1, ensure_ascii=False)
print(f"{sum(l.startswith('PASS') for l in LOG)} PASS, {sum(l.startswith('FAIL') for l in LOG)} FAIL")
