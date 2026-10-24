# DICTO · dictospheres.com — math-data dataset VERSION 2 builder (2026-10-24). Created by DICTO. Licence CC BY-SA 4.0.
# Adds the six DICTONIC SOLIDS of #48 The Golden Split and #51 The Delian Bond, and their three DICTONIC BONDS (fills):
#   Q(sqrt5): Icosaxes, Unborn Axes (convex), Lotus Jewel Axes (= Icosaxes minus 8 Tricaps), Dodecaxes (= Unborn Axes plus 8 Tricaps);
#   Q(2**(1/3)): Samson and Delilah (the octet's tetra and octa pieces at the Delian bond t = 1 - (2/3) 2^(-1/3)).
# Geometry is NOT re-derived: the study's own exact code is executed (copies in build/sources/, from the research branch,
# studies/2026-10-23-shadow-forms, commit e9aed63): golden_split_exact.py (Q5, ICO, UNB, UC), keyed_polar_exact.py (ICOSAXES,
# UNBAXES, tricap(), TR, TRI; #48's cyclic Tricap orientation) and octet_special_exact.py (field class K, the weighted cells).
# Writes solids/<slug>.json/.off (+ unit_volume, -unit-volume.off), packings/dicto-{golden,keyed,delian}-bond.json, build_v2.log.json.
import glob, itertools, json, os, sys
from fractions import Fraction as Fr
import mpmath
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
abs_ = lambda x: x if x.sign() >= 0 else -x
SRC = os.path.join(HERE, 'sources'); SOL = os.path.join(HERE, '..', 'solids'); PK = os.path.join(HERE, '..', 'packings')
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).', 'version_added': 2}
MARK = {'credit': 'DICTO', 'creator_mark': 'Created by DICTO · dictospheres.com', 'licence': 'CC BY-SA 4.0'}
D48 = '10.5281/zenodo.23596362'; D51 = '10.5281/zenodo.23606828'
STUDY = 'research branch studies/2026-10-23-shadow-forms (commit e9aed63)'

# ------------------------------------------------------------------ 1. the study's exact objects (#48)
ns = {}
gs = open(os.path.join(SRC, 'golden_split_exact.py')).read()
exec(gs.split("print('AXEs generated:'")[0], ns)                                  # Q5, PHI, IPHI, H, HALF, ICO, UNB, UC, helpers
exec('def hull_facets' + gs.split('def hull_facets')[1].split('def poly_volume')[0], ns)
kp = open(os.path.join(SRC, 'keyed_polar_exact.py')).read()
exec(kp.split('ok_all = True')[1].split('def vol(P):')[0].replace("global ok_all; ok_all &= bool(ok); ", ""), ns)   # perms, ICOSAXES, UNBAXES, tricap, TR
exec(next(l for l in kp.split('\n') if l.startswith('TRI = [[add(v, sub(')), ns)                                   # the 8 Tricaps facing the origin
q = lambda x: QF(x.a, x.b, 5)
qv = lambda v: tuple(q(x) for x in v)
UC = qv(ns['UC']); Z = QF(0); HALF = QF(Fr(1, 2)); H = PHI / 2
ICOSAXES = [qv(v) for v in ns['ICOSAXES']]
UNBAXES = [sub(qv(v), UC) for v in ns['UNBAXES']]                                  # Unborn Axes about its own centre
SIGNS = list(itertools.product((1, -1), repeat=3))                                   # the order the study uses for TR, TRI
TR = [[sub(qv(v), UC) for v in t] for t in ns['TR']]                               # keys of the Unborn Axes at the origin (Unborn centre 0)
TRI = [[qv(v) for v in t] for t in ns['TRI']]                                      # dents of the Icosaxes at the origin
TRI_C = [tuple(H * s for s in sg) for sg in SIGNS]                                  # ... their Unborns sit at (phi/2) s
log(len(ICOSAXES) == 24 and len(UNBAXES) == 24 and len(TR) == 8 and len(TRI) == 8, 'study objects loaded: Icosaxes 24 corners, Unborn Axes 24, 8 keys, 8 dents')

def emit(slug, meta, V, F, published):
    V, F = canon(V, F)
    meta = dict(meta, **COMMON); meta['published_values'] = published
    r = write_solid(os.path.join(SOL, slug), meta, V, F)
    log(r['cls'] == r['label'], f"{slug}: symmetry {r['cls']} order {r['order']} (classified from the solid: corners and faces) vs stated {r['label']}")
    for k, v in published.items():
        if k == 'volume': log(r['vol'] == parse_any(v, V[0][0].d), f"{slug}: volume {fmt(r['vol'])} vs published {v}")
        elif k == 'f_vector': log((r['V'], r['E'], r['F']) == tuple(v), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs published {tuple(v)}")
        elif k == 'faces_by_sides': log({str(a): b for a, b in r['fk'].items()} == v, f"{slug}: faces {r['fk']} vs published {v}")
        elif k == 'squared_edge_lengths': log(set(r['el']) == {parse_any(x, V[0][0].d) for x in v}, f"{slug}: squared edges {[fmt(x) for x in r['el']]} vs published {v}")
        elif k == 'symmetry_order': log(r['order'] == v, f"{slug}: symmetry order {r['order']} vs published {v}")
    print(slug, r['V'], r['E'], r['F'], r['fk'], fmt(r['vol']), r['cls'], flush=True)
    return V, F, r

def parse_any(s, d):
    import sympy
    e = sympy.expand(sympy.sympify(s))
    if isinstance(d, tuple):
        k = d[1]; cs = [Fr(0)] * 3; basis = {sympy.Integer(1): 0, sympy.Integer(k) ** sympy.Rational(1, 3): 1, sympy.Integer(k) ** sympy.Rational(2, 3): 2}
        for t, c in e.as_coefficients_dict().items(): cs[basis[t]] += Fr(int(c.p), int(c.q))
        return KC(*cs, k=k)
    a = Fr(0); b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        c = Fr(int(c.p), int(c.q))
        if t == 1: a += c
        elif t == sympy.sqrt(d): b += c
        else: raise ValueError(s)
    return QF(a, b, d)

# ------------------------------------------------------------------ 2. Icosaxes and Unborn Axes (convex, Oh)
TO_EDGES = ['1/2', '3/4 - sqrt(5)/4']                                              # 1/sqrt2 and 1/(phi sqrt2), squared (#48 (c))
Vi, Fi = hull(ICOSAXES)
Vi, Fi, ri = emit('dicto-icosaxes', dict(
    name='Icosaxes', finding='', paper='#48 The Golden Split', dicto_doi=D48, status='known shape (Koca et al. 2015, non-regular truncated octahedron x = tau); new route', convex=True,
    scale_note='#48 frame: regular icosahedron of edge 1 at the origin (corners (0, +-1/2, +-phi/2) and cyclic), lattice spacing phi; the Icosaxes is '
               'that icosahedron with its 12 AXE pyramids (golden split t = 1/phi); corners all permutations of (+-1/2, +-phi/2, 0).',
    source={'app': 'study', 'path': STUDY + ': polar/keyed_polar_exact.py ICOSAXES (proved = icosahedron + 12 pyramids in exact/golden_split_exact.py)', 'id': None},
    symmetry_label='Oh'), Vi, Fi,
    {'volume': '1 + 2*sqrt(5)/3', 'f_vector': [24, 36, 14], 'faces_by_sides': {'4': 6, '6': 8}, 'squared_edge_lengths': TO_EDGES, 'symmetry_order': 48})
Vu, Fu = hull(UNBAXES)
Vu, Fu, ru = emit('dicto-unborn-axes', dict(
    name='Unborn Axes', finding='', paper='#48 The Golden Split', dicto_doi=D48, status='known shape (Koca et al. 2015, non-regular truncated octahedron x = 1/tau); new route', convex=True,
    scale_note='#48 frame (icosahedron edge 1, lattice spacing phi), moved so that its centre, the cube centre c = (phi/2)(1, 1, 1) of #48, is at the '
               'origin: corners all permutations of (+-1/(2 phi), +-phi/2, 0). It is the Unborn (corners c + cyclic permutations of '
               '(+-phi/2, +-1/(2 phi), 0)) with its 12 AXE pyramids (golden split).',
    source={'app': 'study', 'path': STUDY + ': polar/keyed_polar_exact.py UNBAXES - UC', 'id': None},
    symmetry_label='Oh'), Vu, Fu,
    {'volume': '1 + sqrt(5)/3', 'f_vector': [24, 36, 14], 'faces_by_sides': {'4': 6, '6': 8}, 'squared_edge_lengths': TO_EDGES, 'symmetry_order': 48})
def perms(a, b):
    out = set()
    for p in itertools.permutations((a, b, Z)):
        for sg in itertools.product((1, -1), repeat=3): out.add(tuple(p[k] * sg[k] for k in range(3)))
    return out
log(set(Vi) == perms(HALF, H), 'Icosaxes corners = all permutations of (+-1/2, +-phi/2, 0) (#48 (a))')
log(set(Vu) == perms((PHI - 1) / 2, H), 'Unborn Axes corners = all permutations of (+-1/(2 phi), +-phi/2, 0) (#48 (b))')

# ------------------------------------------------------------------ 3. the keyed pair (non-convex)
def plane_of(V, f):
    n = (zero(), zero(), zero())
    for i in range(len(f)):
        c = cross(V[f[i]], V[f[(i + 1) % len(f)]]); n = add(n, c)
    k = next(x for x in n if x.sign() != 0); s = 1 if k.sign() > 0 else -1
    kk = k * s
    return tuple(x / kk for x in n) + (dot(n, V[f[0]]) / kk,)

def merge_coplanar(V, F):
    """merge faces that share an edge and lie in the same oriented plane (true face list)."""
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

def keyed(Vh, Fh, caps, label):
    V = list(Vh); idx = {v: i for i, v in enumerate(V)}; faces = [list(f) for f in Fh]
    for T in caps:
        a, B = T[0], T[1:]
        bi = {idx[b] for b in B}
        fi = [k for k, f in enumerate(faces) if bi <= set(f)]; assert len(fi) == 1 and len(faces[fi[0]]) == 6
        f = faces.pop(fi[0])
        k0 = next(k for k in range(6) if {f[k], f[(k + 2) % 6], f[(k + 4) % 6]} == bi)
        h = f[k0:] + f[:k0]
        V.append(a); ia = len(V) - 1
        faces += [[h[0], h[1], h[2]], [h[2], h[3], h[4]], [h[4], h[5], h[0]],          # the hexagon minus the base triangle: 3 triangles
                  [h[0], h[2], ia], [h[2], h[4], ia], [h[4], h[0], ia]]                 # the Tricap's three side faces (dent walls / key sides)
    n0 = len(faces); faces = merge_coplanar(V, faces)
    log(True, f'{label}: {n0} faces before merging coplanar neighbours, {len(faces)} after (true face list)')
    return V, faces

def tricap_json(T, u):
    return {'unborn_centre': [fmt(x) for x in u], 'apex': [fmt(x) for x in T[0]], 'base': [[fmt(x) for x in b] for b in T[1:]]}

VT = Q(Fr(1, 8), Fr(-1, 24))   # (3 - sqrt5)/24 = 1/(12 phi^2), #48
log(all(abs_(det3(sub(T[1], T[0]), sub(T[2], T[0]), sub(T[3], T[0]))) / 6 == VT for T in TR + TRI), 'all 16 Tricaps have volume (3 - sqrt5)/24 exactly (#48)')
VL, FL = keyed(Vi, Fi, TRI, 'Lotus Jewel Axes')
VL, FL, rl = emit('dicto-lotus-jewel-axes', dict(
    name='Lotus Jewel Axes', finding='', paper='#48 The Golden Split', dicto_doi=D48, status='new', convex=False,
    scale_note='#48 frame (icosahedron edge 1 at the origin, lattice spacing phi). The Icosaxes (dicto-icosaxes) with the 8 Tricaps of the '
               'neighbouring Unborns removed: a dent on each of its 8 hexagons. Each Tricap belongs to the Unborn centred at (phi/2) s, s in {+-1}^3, '
               'and points towards the origin (#48 cyclic orientation). Each hexagon minus its dent triangle leaves 3 coplanar triangles.',
    source={'app': 'study', 'path': STUDY + ': polar/keyed_polar_exact.py ICOSAXES and TRI (Tricaps facing the origin)', 'id': None},
    decomposition={'base_solid': 'dicto-icosaxes', 'operation': 'minus', 'tricap_volume': fmt(VT),
                   'note': '#48 Theorem 3: Lotus Jewel Axes = Icosaxes minus its 8 Tricaps (dents). Tricap = tile t3 of Mosseri-Sadoc scaled by 1/tau: '
                           'apex u + s/2 (a corner of the cube of the Unborn\'s dodecahedron), base u + (s_x phi/2, s_y/(2 phi), 0), '
                           'u + (0, s_y phi/2, s_z/(2 phi)), u + (s_x/(2 phi), 0, s_z phi/2), u the Unborn\'s centre, s the direction.',
                   'tricaps': [tricap_json(T, u) for T, u in zip(TRI, TRI_C)]},
    symmetry_label='Th'), VL, FL,
    {'volume': 'sqrt(5)', 'symmetry_order': 24})
VD, FD = keyed(Vu, Fu, TR, 'Dodecaxes')
VD, FD, rd = emit('dicto-dodecaxes', dict(
    name='Dodecaxes', finding='', paper='#48 The Golden Split', dicto_doi=D48, status='new', convex=False,
    scale_note='#48 frame (icosahedron edge 1, lattice spacing phi), centred like dicto-unborn-axes (its centre (phi/2)(1, 1, 1) of #48 moved to '
               'the origin). The Unborn Axes with the 8 Tricaps of its own Unborn added: a key on each of its 8 hexagons; the Unborn with its 8 '
               'Tricaps is the regular dodecahedron of edge 1/phi, so the Dodecaxes holds a whole regular dodecahedron (#48).',
    source={'app': 'study', 'path': STUDY + ': polar/keyed_polar_exact.py UNBAXES and TR, moved by -UC', 'id': None},
    decomposition={'base_solid': 'dicto-unborn-axes', 'operation': 'plus', 'tricap_volume': fmt(VT),
                   'note': '#48 Theorem 3: Dodecaxes = Unborn Axes plus its 8 Tricaps (keys); Tricaps as for dicto-lotus-jewel-axes, here of the '
                           'Unborn centred at the origin.',
                   'tricaps': [tricap_json(T, (Z, Z, Z)) for T in TR]},
    symmetry_label='Th'), VD, FD,
    {'volume': '2', 'symmetry_order': 24})
log(rl['vol'] == ri['vol'] - 8 * VT and rd['vol'] == ru['vol'] + 8 * VT, 'Lotus Jewel Axes = Icosaxes - 8 Tricaps and Dodecaxes = Unborn Axes + 8 Tricaps, by volume, exactly')
# dodecahedron inside the Dodecaxes: Unborn corners + the 8 apices = the regular dodecahedron of edge 1/phi (#48)
unb0 = [sub(qv(v), UC) for v in ns['UNB']]
Vdod, Fdod = hull(unb0 + [T[0] for T in TR])
log(len(Vdod) == 20 and all(len(f) == 5 for f in Fdod) and len({dot(sub(Vdod[a], Vdod[b]), sub(Vdod[a], Vdod[b])) for a, b in edges_of(Fdod)}) == 1
    and dot(sub(Vdod[edges_of(Fdod)[0][0]], Vdod[edges_of(Fdod)[0][1]]), sub(Vdod[edges_of(Fdod)[0][0]], Vdod[edges_of(Fdod)[0][1]])) == (PHI - 1) * (PHI - 1),
    'Unborn + its 8 Tricaps = regular dodecahedron of edge 1/phi (20 corners, 12 pentagons, one edge length), exactly')

# ------------------------------------------------------------------ 4. Samson and Delilah in Q(2**(1/3)) (#51)
oc = open(os.path.join(SRC, 'octet_special_exact.py')).read()
on = {}
exec(oc.split('fails = 0')[0], on)                                                   # class K, setup, cell, volume, edges2
Kc = on['K']; Kc.n, Kc.k = 3, 2
toKC = lambda x: KC(*x.c, k=2)
tD = Kc([1, 0, Fr(-1, 3)])                                                           # t = 1 - r^2/3 = 1 - (2/3) 2^(-1/3)
S = on['setup']()
def piece(kind, site):
    c = tuple(Kc(x) for x in site)
    Pk, Fk = on['cell'](S, kind, c, tD)
    return [tuple(toKC(x) - Fr(s) for x, s in zip(p, site)) for p in Pk]          # moved so the site (the piece's centre) is at the origin
TSITE = (Fr(1, 2), Fr(1, 2), Fr(1, 2)); OSITE = (Fr(1), Fr(0), Fr(0))
Vs, Fs = hull(piece('T', TSITE)); Vo, Fo = hull(piece('O', OSITE))
r2 = KC(0, 1, 0)                                                                     # 2**(1/3)
SCALE = ('frame of octet_special_exact.py (#51 study): the octet in the cube of side 2, octahedron centres (1,0,0), (0,1,0), (0,0,1), (1,1,1) '
         'and tetrahedron centres (1/2 or 3/2, 1/2 or 3/2, 1/2 or 3/2) mod 2, so the octet edge is sqrt2 (#51 uses octet edge 1: divide lengths by '
         'sqrt2 and volumes by 2 sqrt2). The cut is the Delian bond t = 1 - (2/3) 2^(-1/3). The piece is moved so that its centre is at the origin. '
         'sqrt2 is not in Q(2**(1/3)); this frame keeps every coordinate exact in the one field.')
Vs, Fs, rs = emit('dicto-samson', dict(
    name='Samson', finding='', paper='#51 The Delian Bond', dicto_doi=D51, status='new (a new proportion: the cube with four alternate corners cut, at the Delian bond)', convex=True,
    scale_note=SCALE + ' Samson: the tetrahedron piece T(t) round the tetrahedron centre (1/2, 1/2, 1/2); volume 2/3 here = sqrt2/6 at octet edge 1; '
                       'edges 2^(1/6) = sqrt2/cbrt2 (his triangles, Delilah\'s faces) and 1 - 2^(-1/3) (= sqrt2 (1 - 2^(-1/3))/sqrt2).',
    source={'app': 'study', 'path': STUDY + ': octet/octet_special_exact.py cell(S, "T", (1/2,1/2,1/2), t) in Q(2**(1/3))', 'id': None},
    symmetry_label='Td'), Vs, Fs,
    {'volume': '2/3', 'f_vector': [16, 24, 10], 'faces_by_sides': {'3': 4, '6': 6}, 'squared_edge_lengths': ['2**(1/3)', '1 + 2**(1/3)/2 - 2**(2/3)'], 'symmetry_order': 24})
Vo, Fo, ro = emit('dicto-delilah', dict(
    name='Delilah', finding='', paper='#51 The Delian Bond', dicto_doi=D51, status='known shape (regular octahedron); DICTO\'s name at the Delian bond', convex=True,
    scale_note=SCALE + ' Delilah: the octahedron piece O(t) round the octahedron centre (1, 0, 0): the regular octahedron of edge 2^(1/6) here '
                       '(= 2^(-1/3) at octet edge 1: the octet\'s octahedron shrunk by 2^(-1/3)), corners (+-2^(-1/3), 0, 0) and permutations; volume 2/3 '
                       'here = sqrt2/6 at octet edge 1, half the octet\'s octahedron.',
    source={'app': 'study', 'path': STUDY + ': octet/octet_special_exact.py cell(S, "O", (1,0,0), t) in Q(2**(1/3))', 'id': None},
    symmetry_label='Oh'), Vo, Fo,
    {'volume': '2/3', 'f_vector': [6, 12, 8], 'faces_by_sides': {'3': 8}, 'squared_edge_lengths': ['2**(1/3)'], 'symmetry_order': 48})
half_r2 = r2 * r2 / 2                                                                # 2^(-1/3)
log(set(Vo) == {tuple(half_r2 * s if k == i else KC(0) for k in range(3)) for i in range(3) for s in (1, -1)}, 'Delilah corners = (+-2^(-1/3), 0, 0) and permutations, exactly')
# the other tetrahedron orientation: the cell at (3/2, 1/2, 1/2) is Samson turned by the quarter turn about z
RZ = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
rot = lambda R, v: tuple(sum((v[k] * R[i][k] for k in range(3)), KC(0)) for i in range(3))
Vdown = set(piece('T', (Fr(3, 2), Fr(1, 2), Fr(1, 2))))
log(Vdown == {rot(RZ, v) for v in Vs}, 'the tetrahedron piece at (3/2, 1/2, 1/2) is Samson turned by the quarter turn about z (exact corner sets)')

# ------------------------------------------------------------------ 5. unit-volume copies (as build_extra.py, field-generic)
mpmath.mp.dps = 60
def mpx(x):
    if isinstance(x, KC): return x.mp()
    return mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(x.d)
def dec15(m):
    from decimal import Decimal
    qd = Decimal(mpmath.nstr(m, 50, strip_zeros=False, min_fixed=-mpmath.inf, max_fixed=mpmath.inf)).quantize(Decimal(1).scaleb(-15))
    return format(qd, 'f') if qd != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-15)), 'f')
for slug, V, F in [('dicto-icosaxes', Vi, Fi), ('dicto-unborn-axes', Vu, Fu), ('dicto-lotus-jewel-axes', VL, FL), ('dicto-dodecaxes', VD, FD),
                   ('dicto-samson', Vs, Fs), ('dicto-delilah', Vo, Fo)]:
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
    if 'decomposition' in doc: out['checks']['decomposition'] = 'convex base -/+ 8 Tricaps, exact (check.py)'
    json.dump(out, open(p, 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(SOL, slug + '-unit-volume.off'), 'w') as fh:
        fh.write('OFF\n# ' + doc['name'] + ', unit volume (scaled by V^(-1/3) about ' + ('the origin' if at_origin else 'its corner centroid')
                 + ') — Created by DICTO · dictospheres.com — CC BY-SA 4.0\n')
        fh.write(f"{len(V)} {len(doc['faces'])} {doc['f_vector']['edges']}\n")
        for w in uv['vertices_decimal']: fh.write(' '.join(w) + '\n')
        for f in doc['faces']: fh.write(str(len(f)) + ' ' + ' '.join(map(str, f)) + '\n')
    log(at_origin, f'{slug}: unit-volume copy, s = {uv["scale_decimal"]}, centre {uv["centre"]["kind"]}')

# ------------------------------------------------------------------ 6. the three DICTONIC BONDS (fills)
vec = lambda v: {'exact': [fmt(x) for x in v], 'decimal': [x.dec() for x in v]}
num = lambda x: {'exact': fmt(x), 'decimal': x.dec()}
def I3(d): return [[fmt(zero(d) + (1 if i == j else 0)) for j in range(3)] for i in range(3)]
def O3(d): return [fmt(zero(d))] * 3
def bond(slug, doc, L, pieces, vols):
    cell = abs_(det3(*L)); vs = sum(vols, zero(L[0][0].d))
    log(vs == cell, f'{slug}: piece volumes sum {fmt(vs)} = cell volume {fmt(cell)}')
    doc = dict(doc); doc.update({'field': field_name(L[0][0].d), 'lattice_vectors': [vec(b) for b in L], 'cell_volume': num(cell),
                                 'pieces': [{'solid': s, 'rotation': R, 'translation': t} for s, R, t in pieces]})
    doc.update(MARK); doc['version_added'] = 2
    doc.setdefault('checks', {'volume_sum_equals_cell_volume': True, 'no_overlaps_exact': True, 'verified_by': 'check.py'})
    json.dump(doc, open(os.path.join(PK, slug + '.json'), 'w'), indent=1, ensure_ascii=False)
LG = [(PHI, Z, Z), (Z, PHI, Z), (Z, Z, PHI)]
bond('dicto-golden-bond', {'name': 'DICTO golden bond: Icosaxes and Unborn Axes', 'finding': '', 'paper': '#48 The Golden Split', 'dicto_doi': D48,
     'status': 'published fill (#48 Main theorem (f))',
     'note': '#48: Icosaxes at the points of phi Z^3 and Unborn Axes at the cube centres (phi/2)(1, 1, 1) + phi Z^3 fill space face to face '
             '(Icosaxes meet Icosaxes on squares, Unborn Axes meet Unborn Axes on squares, the two meet on the hexagons). One of each per cell.'},
     LG, [('dicto-icosaxes', I3(5), O3(5)), ('dicto-unborn-axes', I3(5), [fmt(x) for x in UC])], [ri['vol'], ru['vol']])
bond('dicto-keyed-bond', {'name': 'DICTO keyed bond: Lotus Jewel Axes and Dodecaxes', 'finding': '', 'paper': '#48 The Golden Split', 'dicto_doi': D48,
     'status': 'published fill (#48 Theorem 3)', 'kind': 'fill by non-convex (keyed) pieces, proved by decomposition',
     'proof': 'decomposition', 'base_packing': 'dicto-golden-bond',
     'keying': 'every Tricap on the dodecahedron side: each Icosaxes carries 8 dents, each Unborn Axes 8 keys',
     'note': '#48 Theorem 3: in the Lotus Jewel network the golden split gives the Lotus Jewel Axes (the Icosaxes minus its 8 Tricaps) and the '
             'Dodecaxes (the Unborn Axes plus its 8 Tricaps); every way of giving each Tricap to one side or the other fills space. This file fixes '
             'one keying, every Tricap on the dodecahedron side (the Lotus Jewel network itself). Same lattice and placements as '
             'dicto-golden-bond. Proof checked by check.py: the golden bond tiles (convex pieces, exact), and every dent of a Lotus Jewel Axes is '
             'exactly one key of a Dodecaxes moved by a lattice vector, so the Tricaps only change owner.',
     'checks': {'base_fill_tiles': True, 'dents_equal_keys_mod_lattice': True, 'volume_sum_equals_cell_volume': True, 'verified_by': 'check.py'}},
     LG, [('dicto-lotus-jewel-axes', I3(5), O3(5)), ('dicto-dodecaxes', I3(5), [fmt(x) for x in UC])], [rl['vol'], rd['vol']])
two = KC(2)
LD = [(two, KC(0), KC(0)), (KC(0), two, KC(0)), (KC(0), KC(0), two)]
dpieces = []
for i, j, k in itertools.product((0, 1), repeat=3):
    site = (Fr(1, 2) + i, Fr(1, 2) + j, Fr(1, 2) + k)
    R = I3(('cbrt', 2)) if (i + j + k) % 2 == 0 else [[fmt(KC(x)) for x in row] for row in RZ]
    dpieces.append(('dicto-samson', R, [fmt(KC(x)) for x in site]))
for site in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]:
    dpieces.append(('dicto-delilah', I3(('cbrt', 2)), [fmt(KC(x)) for x in site]))
bond('dicto-delian-bond', {'name': 'DICTO Delian bond: Samson and Delilah', 'finding': '', 'paper': '#51 The Delian Bond', 'dicto_doi': D51,
     'status': 'published fill (#51 Main theorem and Theorem 3)',
     'note': '#51: the octet cut at the Delian bond t = 1 - (2/3) 2^(-1/3): 8 Samsons (at the tetrahedron centres; those with an odd sum of '
             'integer parts turned by the quarter turn about z) and 4 Delilahs (at the octahedron centres) per cube of side 2 (the frame of '
             'octet_special_exact.py, octet edge sqrt2). Equal volumes 2/3 each, 8 in all.'},
     LD, dpieces, [rs['vol']] * 8 + [ro['vol']] * 4)

json.dump({'log': LOG}, open(os.path.join(HERE, 'build_v2.log.json'), 'w'), indent=1, ensure_ascii=False)
print(f"{sum(l.startswith('PASS') for l in LOG)} PASS, {sum(l.startswith('FAIL') for l in LOG)} FAIL")
