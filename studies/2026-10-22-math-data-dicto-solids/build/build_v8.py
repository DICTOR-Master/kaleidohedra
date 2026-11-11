# DICTO · dictospheres.com — math-data dataset VERSION 8 builder (2026-11-08). Created by DICTO. Licence CC BY-SA 4.0.
# Adds the numbered solids of papers #75, #86, #88 and #89 (D-numbers and names exactly as in the DICTO Concordance), exact:
#   #75 HexOct: Two Tiles for Every Stacking: D111 HexOct h-tile (lambda = 1/10, one solid of four pieces; also member E's h-tile in #86).
#        D110 HexOct c-tile is NOT a solid: its two towers touch at one point (#86, Section 1), so it is no closed 2-manifold; left out.
#   #86 The HexOct Family (members A-E, pairs.json of studies/2026-11-02-hexoct-connected): D112 Twisted cube (A, lambda = 3/8, h-tile),
#        D113/D114 B · HexOct -1/8 c-/h-tile (whole octahedra), D115/D116 C · HexOct -1/8 c-/h-tile, D117 D · HexOct -11/24 c-tile,
#        D118 E · HexOct 1/10 c-tile. Exact in Q (the frame of Chucky and Fang: ball spacing sqrt2, layers perpendicular to (1, 1, 1)).
#        The pieces are the census-engine cells of tiles.py (#75), shifted per pairs.json, joined by exactfaces.union_faces (exact).
#   #88 Every Platonic Solid Has Exactly Two Golden Cuts: D119-D126 Greater/Lesser Golden Cut Dodecahedron, Icosahedron, Cube,
#        Tetrahedron: every corner cut at x along its edges, x = phi/(k + 2 phi) (greater) and 1/(phi k + 2) (lesser). Q(sqrt5), and for
#        the cube Q(t), t = sqrt2 + sqrt5 (the cube's cuts need sqrt2 and sqrt5 together, #89 Section 9).
#   #89 All Five Golden Pairs Are Slices of Four-Dimensional Solids: D127/D128 Greater/Lesser Golden Cut Rhombic Dodecahedron (Q(t),
#        t = sqrt2 + sqrt3 + sqrt5), D129/D130 ... Rhombic Triacontahedron (Q(w), w = sqrt(2 + phi)), D131/D132 ... Snub Dodecahedron L/R
#        (Q(xi), xi^3 - 2 xi = phi; one file per D-number, one hand; the other hand is its mirror image).
#   #96 (D133 DICTO Void Keeper, D134 DICTO Golden Skin): left out; the paper states their exact forms are still open (Section 6).
# Every solid is checked against the numbers its paper (and the paper's own study data) prints; see build_v8.log.json.
# Usage (compute-host, in a copy of dataset-v7 as dataset-v8): python3 build/build_v8.py
import json, os, sys, itertools, math
from fractions import Fraction as Fr
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); SRC = os.path.join(HERE, 'sources'); sys.path.insert(0, SRC)
from exactlib import *
import exactlib, sympy as sp, numpy as np, mpmath
SOL = os.path.join(HERE, '..', 'solids')
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok

# ------------------------------------------------------------------ exact hull (as build_v7.py: exact gift-wrapped faces)
def exact_order(V, f, n):
    start = min(f, key=lambda j: tuple(x.f() for x in V[j])); order = [start]
    while True:
        a = order[-1]; cand = None
        for b in f:
            if b == a: continue
            if cand is None: cand = b; continue
            if dot(cross(sub(V[cand], V[a]), sub(V[b], V[a])), n).sign() < 0: cand = b
        if cand == start: break
        order.append(cand); assert len(order) <= len(f)
    return order
def hull_exact_order(points):
    P = list(dict.fromkeys(tuple(p) for p in points))
    from scipy.spatial import ConvexHull
    X = np.array([fv(p) for p in P]); ch = ConvexHull(X); planes = {}
    for simp in ch.simplices:
        a, b, c = (P[i] for i in simp); n = cross(sub(b, a), sub(c, a))
        if all(x.sign() == 0 for x in n): continue
        planes[plane_key(n, dot(n, a))] = (n, dot(n, a))
    good = {}
    for key, (n, cc) in planes.items():
        sg = [(dot(n, p) - cc).sign() for p in P]
        if all(x <= 0 for x in sg): good[key] = (n, cc, [i for i, x in enumerate(sg) if x == 0])
        elif all(x >= 0 for x in sg): good[key] = (mul(-1, n), -cc, [i for i, x in enumerate(sg) if x == 0])
        else: raise AssertionError('float facet is not a supporting plane')
    on = {i: [] for i in range(len(P))}
    for key, (n, cc, idx) in good.items():
        for i in idx: on[i].append(n)
    corners = [i for i in range(len(P)) if len(on[i]) >= 3 and any(det3(*t).sign() != 0 for t in itertools.combinations(on[i], 3))]
    V = [P[i] for i in corners]; vid = {i: k for k, i in enumerate(corners)}; F = []
    for key, (n, cc, idx) in good.items():
        f = [vid[i] for i in idx if i in vid]; assert len(f) >= 3
        order = exact_order(V, f, n); assert len(order) == len(f), 'a face point is not a corner of the face'
        F.append(order)
    exactlib.check_closed(V, F)
    return V, F
exactlib.hull = hull_exact_order; hull = hull_exact_order

# ------------------------------------------------------------------ fields
def multiquad(ps, name):
    """Q(t), t = sum of sqrt(p) for p in ps: minimal polynomial, a rational isolating interval, and each sqrt(p) as an element."""
    t = sp.Symbol(name); a = sum(sp.sqrt(p) for p in ps)
    P = sp.Poly(sp.minimal_polynomial(a, t), t); n = P.degree(); af = float(a)
    lo, hi = next((lo, hi) for (lo, hi), m in P.intervals() if lo <= af <= hi)
    F = AlgField.get([int(c) for c in P.all_coeffs()], Fr(int(lo.p), int(lo.q)), Fr(int(hi.p), int(hi.q)), name)
    S = sp.symbols('s0:%d' % len(ps)); mons = [m for r in range(len(ps) + 1) for m in itertools.combinations(range(len(ps)), r)]
    assert len(mons) == n
    def coords(expr):      # expand in s_i, reduce s_i^2 = p_i: coefficients on the square-free monomials
        out = [Fr(0)] * n
        for e, c in sp.Poly(sp.expand(expr), *S).terms():
            k = Fr(int(c)) * math.prod(Fr(ps[i]) ** (e[i] // 2) for i in range(len(ps)))
            out[mons.index(tuple(i for i in range(len(ps)) if e[i] % 2))] += k
        return out
    M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in coords(sum(S) ** k)] for k in range(n)]).T   # columns: t^k
    root = {}
    for i, p in enumerate(ps):
        e = sp.zeros(n, 1); e[mons.index((i,)), 0] = 1; c = M.solve(e)
        root[p] = RF([Fr(int(x.p), int(x.q)) for x in c], F); assert root[p] * root[p] == p
    return F, root
def conv5(q, s5):
    """an element a + b sqrt5 of Q(sqrt5) (QF, d = 5, or d = 1) as an element of a larger field (s5 its sqrt5)."""
    return s5 * 0 + q.a + (s5 * q.b if q.b != 0 else 0)
def ev(e, K):
    """a sympy expression in rationals and square roots of integers, evaluated in the field K (dict of square roots; key 1 = unit)."""
    e = sp.sympify(e)
    if e.is_Rational: return K[1] * Fr(int(e.p), int(e.q))
    if e.is_Add: return sum((ev(a, K) for a in e.args), K[1] * 0)
    if e.is_Mul:
        out = K[1]
        for a in e.args: out = out * ev(a, K)
        return out
    if e.is_Pow and e.exp == sp.Rational(1, 2) and e.base.is_Integer:
        out = K[1]
        for p, m in sp.factorint(int(e.base)).items():
            out = out * (p ** (m // 2)) * (K[p] if m % 2 else 1)
        return out
    if e.is_Pow and e.exp.is_Integer:
        b = ev(e.base, K); out = K[1]
        for _ in range(abs(int(e.exp))): out = out * b
        return out if e.exp > 0 else K[1] / out
    if e.is_Pow and e.exp == -sp.Rational(1, 2): return K[1] / ev(sp.sqrt(e.base), K)
    raise ValueError(f'cannot evaluate {e}')
def to_sympy(x, K):
    """an element of Q(t) as a sympy number (t written as its radical expression K['expr'])."""
    if isinstance(x, QF): return sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator) * sp.sqrt(x.d)
    return sum(sp.Rational(c.numerator, c.denominator) * K['expr'] ** i for i, c in enumerate(x.c))
def same(x, e, K):
    """exact: the field element x equals the sympy algebraic number e (minimal polynomial of the difference is the variable)."""
    z = sp.Symbol('z'); d = sp.nsimplify(0) + to_sympy(x, K) - sp.sympify(e)
    if abs(sp.N(d, 60)) > sp.Float(10) ** -40: return False
    return sp.minimal_polynomial(d, z) == z

# ------------------------------------------------------------------ writing, with the published values compared
def emit(slug, meta, V, F, published, checks=()):
    V, F = canon(V, F)
    meta = dict(meta); meta['published_values'] = published
    r = write_solid(os.path.join(SOL, slug), meta, V, F)
    if 'f_vector' in published: log((r['V'], r['E'], r['F']) == tuple(published['f_vector']), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs published {published['f_vector']}")
    if 'faces' in published: log(r['F'] == published['faces'], f"{slug}: {r['F']} faces vs published {published['faces']}")
    if 'faces_by_sides' in published: log({str(a): b for a, b in r['fk'].items()} == published['faces_by_sides'], f"{slug}: faces by sides {dict(sorted(r['fk'].items()))} vs published {published['faces_by_sides']}")
    if 'volume' in published: log(fmt(r['vol']) == published['volume'], f"{slug}: volume {fmt(r['vol'])} vs published (in this frame) {published['volume']}")
    if 'squared_edge_lengths' in published: log({fmt(x) for x in r['el']} == set(published['squared_edge_lengths']), f"{slug}: squared edge lengths {[fmt(x) for x in r['el']]} vs published (in this frame) {published['squared_edge_lengths']}")
    if 'symmetry_order' in published: log(r['order'] == published['symmetry_order'], f"{slug}: symmetry order {r['order']} vs published {published['symmetry_order']}")
    for ok, msg in checks: log(ok, f'{slug}: {msg}')
    log(True, f"{slug}: written: {r['V']}, {r['E']}, {r['F']}, faces {dict(sorted(r['fk'].items()))}, volume {r['vol'].dec(9)}, symmetry {r['label']} ({r['order']})")
    BUILT.append((slug, V)); return V, F, r
BUILT = []
CREDIT = 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).'
DOI = {'75': '10.5281/zenodo.23737639', '86': '10.5281/zenodo.23896076', '88': '10.5281/zenodo.23896439', '89': '10.5281/zenodo.23917931'}
TITLE = {'75': '#75 HexOct: Two Tiles for Every Stacking', '86': '#86 The HexOct Family',
         '88': '#88 Every Platonic Solid Has Exactly Two Golden Cuts', '89': '#89 All Five Golden Pairs Are Slices of Four-Dimensional Solids'}
def base(paper, convex, path):
    return {'credit_note': CREDIT, 'version_added': 8, 'paper': TITLE[paper], 'dicto_doi': DOI[paper], 'finding': '', 'convex': convex,
            'source': {'app': 'study', 'path': path, 'id': None}}

# ================================================================== 1. HexOct tiles (#75, #86), exact in Q
from tiles import tile, build as tbuild, corners as tcorners
from stackings import POS
from engine import Cell
import exactfaces as E
PAIRS = {p['name']: p for p in json.load(open(os.path.join(SRC, 'hexoct-pairs.json')))}
def tshift(X, t): return [(p[0] + t[0], p[1] + t[1], p[2]) for p in X]
def whole_oct(word, L, idx, lam):
    """split W of #86 Section 6 (alt_split.py whole()): the whole octahedral piece idx of the gap above layer L, centred on L's ball."""
    net, spec = tbuild(word); n = len(word); m = spec['motif']; c = Cell(net, idx, (lam,), Fr(12)); X = tcorners(c, lam)
    site = m[idx][1]; sh = round((site[2] * n - L) / n) * n; ball = (*POS[word[L]], Fr(L))
    return [(p[0] - ball[0], p[1] - ball[1], (p[2] - Fr(sh, n)) * n - ball[2]) for p in X]
def tile_pieces(t, lam, split, tr):
    w, L = {'c': ('ABC', 1), 'h': ('AB', 0)}[t]
    T = tile(w, L, lam)[0]
    P = [p[3] for p in T] if split == 'RoH' else [p[3] for p in T if p[0] == 'tet'] + [whole_oct(w, L, 3 * (L % len(w)), lam)]
    assert len(P) == len(tr), (t, lam, len(P), tr)
    return [tshift(X, s) for X, s in zip(P, tr)]
A1, A2, C3 = (1, -1, 0), (1, 0, -1), (Fr(2, 3),) * 3
def frame(p):
    """lattice (u, v, z; z in layer units, ball spacing 1) -> orthonormal rational frame at ball spacing sqrt2: u a1 + v a2 + z (2/3)(1,1,1)."""
    return tuple(QF(p[0] * A1[k] + p[1] * A2[k] + p[2] * C3[k], 0, 1) for k in range(3))
def tile_solid(pieces):
    """the union of the tile's convex pieces as one closed surface: exact merged faces (exactfaces.union_faces), corners lying inside
    another face's side inserted into that side (so that every side is shared by exactly two faces), in the rational frame."""
    faces = E.union_faces(pieces)
    assert all(len(f['loops']) == 1 for f in faces), 'a face with a hole'
    segs, bad = E.edge_multiplicity(faces); assert not bad, 'a side not shared by exactly two faces'
    pts = sorted({p for f in faces for p in f['loops'][0]})
    idx = {p: i for i, p in enumerate(pts)}; F = []
    for f in faces:
        lp = f['loops'][0]; g = []
        for i in range(len(lp)):
            p, q = lp[i], lp[(i + 1) % len(lp)]; d = E.sub(q, p); g.append(idx[p])
            mid = [x for x in pts if x not in (p, q) and E.cross(E.sub(x, p), d) == (0, 0, 0) and 0 < E.dot(E.sub(x, p), d) < E.dot(d, d)]
            g += [idx[x] for x in sorted(mid, key=lambda x: E.dot(E.sub(x, p), d))]
        F.append(g)
    for v in range(len(pts)):                                          # every corner's faces form one cycle (no pinch at a corner)
        nxt = {}
        for f in F:
            if v in f: k = f.index(v); nxt[f[k - 1]] = f[(k + 1) % len(f)]
        s0 = next(iter(nxt)); cur = nxt[s0]; steps = 1
        while cur != s0: cur = nxt[cur]; steps += 1
        assert steps == len(nxt), f'pinched at the corner {tuple(str(x) for x in pts[v])} (lattice units)'
    V = [frame(p) for p in pts]
    sizes = sorted(len(f['loops'][0]) for f in faces)
    return V, F, sizes, sum(E.piece_volume6(X) for X in pieces)
CONN = os.path.join('research:studies/2026-11-02-hexoct-connected/data')
HX = ('frame: the close-packed layers at ball spacing sqrt2 in orthonormal rational coordinates (layers perpendicular to (1, 1, 1): '
      'in-layer lattice a1 = (1, -1, 0), a2 = (1, 0, -1), one layer = (2/3)(1, 1, 1); the frame of Chucky and Fang); the papers\' values are '
      'at ball spacing 1: divide lengths by sqrt2 and volumes by 2 sqrt2 (so the volume 2 here is one layer cell, 1/sqrt2). The layer\'s ball '
      'is at the origin. Pieces: tiles.py of #75 (census engine of #53/#57, unchanged), weights w_oct = 0, w_tet = lambda; ')
TILE_DATA = {}
for fn in ('conn_3_8', 'conn_-1_8', 'conn_-11_24', 'conn_1_10'):
    p = os.path.join(SRC, 'hexoct-' + fn + '.json')
    if os.path.exists(p): TILE_DATA[fn] = json.load(open(p))
ALT = json.load(open(os.path.join(SRC, 'hexoct-alt_split.json'))) if os.path.exists(os.path.join(SRC, 'hexoct-alt_split.json')) else {}
def data_class(member, t):
    """the study's own record of the chosen tile (connect.py / alt_split.py output), for a cross-check of the face sizes."""
    pr = PAIRS[member]; tr = pr['tc'] if t == 'c' else pr['th']
    if pr['split'] == 'W': cl = ALT['W_' + t]['classes']
    else: cl = TILE_DATA['conn_' + pr['lam'].replace('/', '_')][t]['classes']
    return next(c for c in cl if c['translates'] == tr)
HEXOCT = [  # slug, name, member, tile, D, status, paper; published (#86 table: faces, hull ratio; volume one layer cell)
    ('dicto-hexoct-h-tile', 'HexOct h-tile', 'E', 'h', 'D111', '75'),
    ('dicto-twisted-cube', 'Twisted cube', 'A', 'h', 'D112', '86'),
    ('dicto-hexoct-b-c-tile', 'B · HexOct −1/8 c-tile', 'B', 'c', 'D113', '86'),
    ('dicto-hexoct-b-h-tile', 'B · HexOct −1/8 h-tile', 'B', 'h', 'D114', '86'),
    ('dicto-hexoct-c-c-tile', 'C · HexOct −1/8 c-tile', 'C', 'c', 'D115', '86'),
    ('dicto-hexoct-c-h-tile', 'C · HexOct −1/8 h-tile', 'C', 'h', 'D116', '86'),
    ('dicto-hexoct-d-c-tile', 'D · HexOct −11/24 c-tile', 'D', 'c', 'D117', '86'),
    ('dicto-hexoct-e-c-tile', 'E · HexOct 1/10 c-tile', 'E', 'c', 'D118', '86')]
PUB86 = {('A', 'h'): (12, '1'), ('B', 'c'): (8, '6/7'), ('B', 'h'): (10, '6/7'), ('C', 'c'): (10, '0.800'), ('C', 'h'): (14, '0.735'),
         ('D', 'c'): (18, '0.783'), ('E', 'c'): (24, '0.745'), ('E', 'h'): (30, '0.778')}
ST86 = ("not found in the sources checked (#86 Section 8: library and web searches, Grünbaum–Shephard 1980, Gabbrielli–Jiao–Torquato 2012, "
        "Fedorov 1885, Lalvani 1990); #86 claims nothing as new until Goldberg's lists of space-filling polyhedra are read")
for slug, name, mem, t, dn, paper in HEXOCT:
    pr = PAIRS[mem]; lam = Fr(pr['lam']); tr = pr['tc'] if t == 'c' else pr['th']
    pieces = tile_pieces(t, lam, pr['split'], tr)
    V, F, sizes, pv6 = tile_solid(pieces)
    nf, hr = PUB86[(mem, t)]
    Vh, Fh = hull(V); vol = volume(V, F); ratio = vol / volume(Vh, Fh)
    hr_ok = (ratio == QF(Fr(hr), 0, 1)) if '/' in hr or hr == '1' else (f'{ratio.f():.3f}' == hr)
    dc = data_class(mem, t)
    convex = ratio == QF(1, 0, 1)
    split = ('the Rule of Halves split (#57): the top half of the octahedral piece below, the two tetrahedral pieces, the bottom half of the '
             'octahedral piece above' if pr['split'] == 'RoH' else 'split W (#86 Section 6, whole octahedra): the two tetrahedral pieces and the '
             'whole octahedral piece of the gap above')
    note = (HX + f"tile {t} of layer {'1 of ABC (c)' if t == 'c' else '0 of AB (h)'} at lambda = {pr['lam']}, {split}; in-layer lattice "
            f"shifts per piece (tiles.py order) {tr} (#86 pairs.json, member {mem}); joined exactly by exactfaces.union_faces (coplanar faces "
            "merged; a corner of one face lying inside a side of the next face is a corner of both, so faces may list such straight corners).")
    if slug == 'dicto-hexoct-h-tile':
        status = ('new: the h-tile of #75 at lambda = 1/10 (the weight of #75 Figure 1), one solid of four pieces; no earlier statement of '
                  'layer tiles of this kind found in the sources checked (#75 Section 6); unchanged in #86, where it is member E\'s h-tile')
    elif slug == 'dicto-twisted-cube':
        status = ('new as far as the sources checked go: member A\'s h-tile (lambda = 3/8), convex, 6 squares and 6 triangles; ' + ST86
                  + '; its c-tile partner, the brick of two cubes, is classical')
    else:
        status = f"new: member {mem} of the HexOct family, its {t}-tile, one solid; " + ST86
    meta = dict(base(paper, convex, CONN), name=name, status=status, scale_note=note)
    if paper == '75': meta['paper'] = TITLE['75'] + '; also #86 The HexOct Family (member E)'
    pub = {'faces': nf, 'hull_ratio': hr, 'volume': '2'}
    if slug == 'dicto-twisted-cube':
        pub.update({'f_vector': [11, 21, 12], 'faces_by_sides': {'3': 6, '4': 6}, 'squared_edge_lengths': ['1', '4/3']})
    zs = Counter(fmt(dot(v, (QF(1, 0, 1),) * 3) / 2) for v in V)      # height in layers = x.(1,1,1)/2 in this frame
    checks = [(vol == QF(pv6 / 3, 0, 1), 'volume of the merged surface = the sum of the piece volumes, exactly'),
              (hr_ok, f'hull ratio {fmt(ratio)} = {ratio.dec(4)} vs published {hr} (#86 Section 4 table)'),
              (sizes == dc['sizes'] and len(F) == dc['faces'] and dc['manifold'], f"merged face sizes {sizes} = the study's record (connect.py / alt_split.py)"),
              (convex == bool(dc['convex']), f'convex {convex} as the study records')]
    if slug == 'dicto-twisted-cube':
        checks.append((dict(zs) == {'-1': 1, '-1/2': 3, '0': 3, '1/2': 3, '1': 1}, f'corners at heights -1, -1/2, 0, 1/2, 1 layers, 1 + 3 + 3 + 3 + 1 of them (#86 Section 5): {dict(zs)}'))
    meta['convex'] = convex
    Vo, Fo, r = emit(slug, meta, V, F, pub, checks)
    log(r['vol'] == QF(2, 0, 1), f'{slug}: volume 2 here = 1/sqrt2 at ball spacing 1, one layer cell (#86 Section 5)')
# the c-tile of #75 (D110): its two towers touch only at the layer's ball, so it is no closed 2-manifold: record why it is left out
P0 = tile_pieces('c', Fr(1, 10), 'RoH', [(0, 0)] * 4)
try:
    tile_solid(P0); log(False, 'D110 HexOct c-tile unexpectedly one closed surface')
except AssertionError as e:
    log(True, f'D110 HexOct c-tile (#75, lambda = 1/10, no shift): not a closed 2-manifold ({e}); left out of the dataset, as #86 Section 1 states (two towers touching at a point)')

# ================================================================== 2. #88 golden cuts of the Platonic solids
S5 = Q(0, 1); K5 = {1: Q(1), 5: S5}
def platonic(name, K1):
    """Platonic solid as an exact hull (dodecahedron/icosahedron at edge 1 in Q(sqrt5); tetrahedron of edge 2 sqrt2; cube of edge 1)."""
    P = []
    if name == 'Dodecahedron':
        h = PHI / 2
        P = [tuple(Q(s) * h for s in sg) for sg in itertools.product((1, -1), repeat=3)]
        for a, b in itertools.product((1, -1), repeat=2):
            for k in range(3):
                v = [Q(0), Q(a) / PHI * h, Q(b) * PHI * h]; P.append(tuple(v[(i - k) % 3] for i in range(3)))
    elif name == 'Icosahedron':
        for a, b in itertools.product((1, -1), repeat=2):
            for k in range(3):
                v = [Q(0), Q(Fr(a, 2)), Q(b) * PHI / 2]; P.append(tuple(v[(i - k) % 3] for i in range(3)))
    elif name == 'Tetrahedron':
        P = [tuple(Q(x) for x in v) for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
    elif name == 'Cube':
        P = [tuple(K1 * Fr(s, 2) for s in sg) for sg in itertools.product((1, -1), repeat=3)]
    return hull(P)
def cut(V, F, y):
    """every corner v cut by the plane through the points at fraction y[v] of each edge from v: hull of v + y[v] (w - v)."""
    pts = []
    for a, b in edges_of(F):
        pts.append(add(V[a], mul(y[a], sub(V[b], V[a])))); pts.append(add(V[b], mul(y[b], sub(V[a], V[b]))))
    return hull(pts)
PATH88 = 'research:papers/golden-truncated-triangles (golden_cuts_exact.py, golden-cuts-exact.md)'
PATH89 = 'research:studies/2026-11-03-golden-cuts-beyond-plato'
MD88 = {  # golden-cuts-exact.md (#88's exact table, edge 1): cut x, face sides (corner, original), volume
 ('Dodecahedron', 'G'): ('1/3', '1/6 + sqrt(5)/6', '1/3', '1205/324 + 557*sqrt(5)/324'),
 ('Dodecahedron', 'L'): ('7/22 - sqrt(5)/22', '1/22 + 3*sqrt(5)/22', 'sqrt(5)/11 + 4/11', '20095/5324 + 27581*sqrt(5)/15972'),
 ('Icosahedron', 'G'): ('3/2 - sqrt(5)/2', '3/2 - sqrt(5)/2', '-2 + sqrt(5)', '-45/4 + 71*sqrt(5)/12'),
 ('Icosahedron', 'L'): ('1/2 - sqrt(5)/10', '1/2 - sqrt(5)/10', 'sqrt(5)/5', '19/20 + 31*sqrt(5)/60'),
 ('Cube', 'G'): ('(-3*sqrt(2) - 2 + sqrt(10) + 2*sqrt(5))/4', '-3/2 + (-sqrt(2) + sqrt(5) + sqrt(10))/2', '(-2*sqrt(5) - sqrt(10) + 3*sqrt(2))/2 + 2', '(-19*sqrt(5) - 13*sqrt(10) + 30*sqrt(2))/3 + 44/3'),
 ('Cube', 'L'): ('(-2*sqrt(5) - 2 + sqrt(10) + 3*sqrt(2))/4', '(-sqrt(10) - sqrt(2) + sqrt(5))/2 + 3/2', '(-3*sqrt(2) - sqrt(10) + 2*sqrt(5))/2 + 2', '(-30*sqrt(2) - 13*sqrt(10) + 19*sqrt(5))/3 + 44/3'),
 ('Tetrahedron', 'G'): ('3/2 - sqrt(5)/2', '3/2 - sqrt(5)/2', '-2 + sqrt(5)', '(-35*sqrt(2) + 16*sqrt(10))/12'),
 ('Tetrahedron', 'L'): ('1/2 - sqrt(5)/10', '1/2 - sqrt(5)/10', 'sqrt(5)/5', '(5*sqrt(2) + 8*sqrt(10))/300')}
TAB2 = {'Dodecahedron': ('20 triangles, 12 truncated pentagons', {'3': 20, '10': 12}, 'x = 1/3', 'x = (7 − √5)/22 ≈ 0.2165', 60, 90, 32),
        'Icosahedron': ('12 pentagons, 20 truncated triangles', {'5': 12, '6': 20}, 'x = 1/φ²', 'x = 1/(φ√5)', 60, 90, 32),
        'Cube': ('8 triangles, 6 truncated squares', {'3': 8, '8': 6}, 'x ≈ 0.3479', 'x ≈ 0.2332', 24, 36, 14),
        'Tetrahedron': ('4 triangles, 4 truncated triangles', {'3': 4, '6': 4}, 'x = 1/φ²', 'x = 1/(φ√5)', 12, 18, 8)}
KC_ = {'Dodecahedron': 'phi', 'Icosahedron': '1', 'Cube': 'sqrt(2)', 'Tetrahedron': '1'}
# the cube's field: t = sqrt2 + sqrt5 (#89 Section 9: the Golden Cut Cubes need Q(sqrt2, sqrt5))
FC, RC = multiquad([2, 5], 't'); KCUBE = {1: RF([1], FC), 2: RC[2], 5: RC[5], 'expr': sp.sqrt(2) + sp.sqrt(5)}
log(fmt(RF([0, 1], FC)) == 't' and field_definition(FC)['minimal_polynomial'] == 't**4 - 14*t**2 + 9', f"cube field: t = sqrt2 + sqrt5, minimal polynomial {field_definition(FC)['minimal_polynomial']}, interval {field_definition(FC)['isolating_interval']}; sqrt2 = {fmt(RC[2])}, sqrt5 = {fmt(RC[5])}")
def fdef(F, what):
    fd = field_definition(F)
    fd['note'] = (f'{F.name} is the only real root of the minimal polynomial in the open isolating interval; the polynomial is irreducible over Q; '
                  f'exact strings are polynomials in {F.name} of degree below {F.n} with rational coefficients. ' + what)
    return fd
for nm in ('Dodecahedron', 'Icosahedron', 'Cube', 'Tetrahedron'):
    cube = nm == 'Cube'
    K = KCUBE if cube else dict(K5, expr=None)
    one = K[1]; s5 = K[5]; phi = (one + s5) / 2
    k = {'Dodecahedron': phi, 'Icosahedron': one, 'Cube': K.get(2), 'Tetrahedron': one}[nm]
    V0, F0 = platonic(nm, one)
    edge2 = dot(sub(V0[F0[0][0]], V0[F0[0][1]]), sub(V0[F0[0][0]], V0[F0[0][1]]))
    for g in ('G', 'L'):
        x = phi / (k + 2 * phi) if g == 'G' else one / (phi * k + 2)
        V, F = cut(V0, F0, {i: x for i in range(len(V0))})
        xs, cs, os_, vs = MD88[(nm, g)]
        scale = 1 if nm != 'Tetrahedron' else 8                      # edge^2 of the frame (tetrahedron of edge 2 sqrt2)
        Kev = K if cube else K5
        pub_vol = ev(sp.expand(sp.sympify(vs) * (2 * sp.sqrt(2) if nm == 'Tetrahedron' else 1) ** 3), Kev)     # edge 1 -> this frame
        el_pub = [ev(sp.expand(sp.sympify(cs) ** 2 * scale), Kev), ev(sp.expand(sp.sympify(os_) ** 2 * scale), Kev)]
        long_, short = (el_pub[0], el_pub[1]) if g == 'G' else (el_pub[1], el_pub[0])
        full = ('Greater' if g == 'G' else 'Lesser') + ' Golden Cut ' + nm
        slug = 'dicto-' + full.lower().replace(' ', '-')
        tb = TAB2[nm]
        meta = base('88', True, PATH88)
        meta.update(name=full, status=("new: one of the ten DICTO-Kepler golden truncations, the eight of them other than the octahedral pair "
                    "(Icosaxes, Unborn Axes) being new within #88's checks (#88 Section 9: truncation at any depth is classical, Kepler 1619; "
                    "non-uniform truncations, Zefiro 2011; Lalvani's \"φ-truncated icosahedron\", US 4,723,382, defines no depth)"),
                    scale_note=(f"the {nm.lower()} " + ('of edge 2 sqrt2 (corners (1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)); #88 values are at edge 1: '
                    'divide lengths by 2 sqrt2 and volumes by 16 sqrt2' if nm == 'Tetrahedron' else 'of edge 1, centred at the origin') +
                    f"; every corner cut off by the plane through the points at x = {'phi/(k + 2 phi)' if g == 'G' else '1/(phi k + 2)'} of its edges, "
                    f"k = {KC_[nm]} (#88 Theorem 2): x = {xs} ({'deeper cut, corner sides long' if g == 'G' else 'lighter cut, original sides long'})"))
        if cube: meta['field_definition'] = fdef(FC, 't = sqrt2 + sqrt5; sqrt2 = (t**3 - 11*t)/6, sqrt5 = (17*t - t**3)/6.')
        pub = {'f_vector': [tb[4], tb[5], tb[6]], 'faces_by_sides': tb[1], 'volume': fmt(pub_vol), 'squared_edge_lengths': sorted({fmt(z) for z in el_pub}),
               'cut_x': xs, 'faces_as_published': tb[0] + ' (#88 Table 2)', 'volume_edge_1': vs + ' (golden-cuts-exact.md, #88 study)'}
        el = sorted({dot(sub(V[a], V[b]), sub(V[a], V[b])) for a, b in edges_of(F)}, key=lambda q: q.f())
        checks = [(same(x, xs, K) if cube else (x == ev(xs, K5)), f'cut x = {xs} exactly (#88 Theorem 2, golden-cuts-exact.md)'),
                  (len(el) == 2 and long_ == short * (phi * phi), 'two edge lengths, long/short = phi exactly (squared: phi^2)')]
        if g == 'G' and nm in ('Icosahedron', 'Tetrahedron'): checks.append((x == 1 / (phi * phi), 'x = 1/phi^2 (#88 Table 2)'))
        if g == 'L' and nm in ('Icosahedron', 'Tetrahedron'): checks.append((x == 1 / (phi * s5), 'x = 1/(phi sqrt5) (#88 Table 2)'))
        if g == 'L' and nm == 'Dodecahedron': checks.append((x == (7 - s5) / 22 and abs(x.f() - 0.2165) < 5e-5, 'x = (7 - sqrt5)/22 = 0.2165 (#88 Table 2)'))
        if g == 'G' and nm == 'Dodecahedron': checks.append((x == Q(Fr(1, 3)), 'x = 1/3, trisecting every edge (#88 Table 2)'))
        if cube: checks.append((f"{x.f():.4f}" == ('0.3479' if g == 'G' else '0.2332'), f"x = {x.dec(6)} (#88 Table 2: {tb[2] if g == 'G' else tb[3]})"))
        emit(slug, meta, V, F, pub, checks)
# control (not written): the octahedron's two golden cuts are Icosaxes and Unborn Axes (volumes 1 + 2 sqrt5/3, 1 + sqrt5/3 at the #48 frame)
Vo = [tuple(Q(s if i == k else 0) for i in range(3)) for k in range(3) for s in (1, -1)]; Vo, Fo = hull(Vo)
for g, ref in (('G', 'dicto-icosaxes'), ('L', 'dicto-unborn-axes')):
    x = PHI / (1 + 2 * PHI) if g == 'G' else Q(1) / (PHI + 2)
    V, F = cut(Vo, Fo, {i: x for i in range(6)})
    m = json.load(open(os.path.join(SOL, ref + '.json')))
    log(similar_float([fv(v) for v in V], [[float(s) for s in w['decimal']] for w in m['vertices']]) is not None,
        f'control: the octahedron cut at x = {fmt(x)} is {ref} up to similarity (#88 Theorem 2)')

# ================================================================== 3. #89 golden cuts of the rhombic dodecahedron and triacontahedron
FD8, R8 = multiquad([2, 3, 5], 't'); K8 = {1: RF([1], FD8), 2: R8[2], 3: R8[3], 5: R8[5], 'expr': sp.sqrt(2) + sp.sqrt(3) + sp.sqrt(5)}
log(True, f"rhombic dodecahedron field: t = sqrt2 + sqrt3 + sqrt5, minimal polynomial {field_definition(FD8)['minimal_polynomial']}, interval {field_definition(FD8)['isolating_interval']}")
FW = AlgField.get([1, 0, -5, 0, 5], Fr(3, 2), 2, 'w'); w = RF([0, 1], FW); s5w = 2 * w * w - 5
KW = {1: RF([1], FW), 5: s5w, 'expr': sp.sqrt(2 + (1 + sp.sqrt(5)) / 2)}
_pw = sp.Poly(sp.Symbol('w') ** 4 - 5 * sp.Symbol('w') ** 2 + 5)
log(_pw.is_irreducible and _pw.count_roots(sp.Rational(3, 2), 2) == 1 and s5w * s5w == 5 and w * w == 2 + (1 + s5w) / 2,
    f'rhombic triacontahedron field: w = sqrt(2 + phi), w^4 - 5 w^2 + 5 irreducible, one root in (3/2, 2), w = {w.dec(12)}; sqrt5 = 2 w^2 - 5')
def polar_hull(V, F):
    return hull(polar(V, F, Q(1)))
co = [tuple(Q(x) for x in p) for p in set(itertools.permutations((1, 1, 0))) | set(itertools.permutations((1, -1, 0))) | set(itertools.permutations((-1, -1, 0)))]
co = list(dict.fromkeys(co)); Vco, Fco = hull(co); log(len(Vco) == 12 and len(Fco) == 14, 'cuboctahedron (+-1, +-1, 0): 12 corners, 14 faces')
idd = []
seeds = [(Q(0), Q(0), PHI), (Q(Fr(1, 2)), PHI / 2, PHI * PHI / 2)]
for s_ in seeds:
    for k in range(3):
        p = (s_[k % 3], s_[(k + 1) % 3], s_[(k + 2) % 3])
        for sg in itertools.product((1, -1), repeat=3):
            idd.append(tuple(Q(sg[i]) * p[i] for i in range(3)))
idd = list(dict.fromkeys(idd)); Vid, Fid = hull(idd)
log(len(Vid) == 30 and Counter(len(f) for f in Fid) == Counter({3: 20, 5: 12}) and {dot(sub(Vid[a], Vid[b]), sub(Vid[a], Vid[b])) for a, b in edges_of(Fid)} == {Q(1)},
    'icosidodecahedron (0, 0, phi), (1/2, phi/2, phi^2/2) even permutations: 30 corners, 20 triangles, 12 pentagons, edge 1')
RHOMBIC = []
for cat, Varch, Farch, K, valA, slugpart in (('Rhombic Dodecahedron', Vco, Fco, K8, 4, 'rhombic-dodecahedron'),
                                             ('Rhombic Triacontahedron', Vid, Fid, KW, 5, 'rhombic-triacontahedron')):
    one = K[1]; s5 = K[5]; phi = (one + s5) / 2
    Vr, Fr_ = polar_hull(Varch, Farch)
    Vr = [tuple(conv5(x, s5) for x in v) for v in Vr]
    val = Counter(i for f in Fr_ for i in f)
    e2 = {dot(sub(Vr[a], Vr[b]), sub(Vr[a], Vr[b])) for a, b in edges_of(Fr_)}; assert len(e2) == 1; e2 = next(iter(e2))
    # half-angle sines of the rhombus (side 1): RD cos(alpha) = 1/3, RT tan(alpha/2) = 1/phi
    if valA == 4: sn, cs = one / K[3], K[2] * K[3] / 3
    else: sn, cs = one / w, phi / w
    Kk = (one / sn + one / cs) / 2
    for g in ('G', 'L'):
        b = one / (1 + phi * Kk) if g == 'G' else one / (1 + Kk / phi)
        a = phi * b if g == 'G' else b / phi
        ys, yb = a / (2 * sn), a / (2 * cs)
        V, F = cut(Vr, Fr_, {i: (ys if val[i] == valA else yb) for i in range(len(Vr))})
        full = ('Greater' if g == 'G' else 'Lesser') + ' Golden Cut ' + cat
        RHOMBIC.append((full, 'dicto-' + full.lower().replace(' ', '-'), V, F, a, b, ys, yb, e2, K, phi, g, cat, valA, sn))
# published (#89 Table 2, edge 1, six figures) and the faces
T2 = {('Rhombic Dodecahedron', 'G'): ('0.477001', '0.294803', '0.413095', '0.292102', '2.94509'),
      ('Rhombic Dodecahedron', 'L'): ('0.322952', '0.522548', '0.279685', '0.197767', '3.03758'),
      ('Rhombic Triacontahedron', 'G'): ('0.463634', '0.286541', '0.440942', '0.272517', '11.9873'),
      ('Rhombic Triacontahedron', 'L'): ('0.316769', '0.512543', '0.301265', '0.186192', '12.2076')}
for full, slug, V, F, a, b, ys, yb, e2, K, phi, g, cat, valA, sn in RHOMBIC:
    rd = cat == 'Rhombic Dodecahedron'
    pa, pb, pys, pyb, pvol = T2[(cat, g)]
    vol = volume(V, F); vol1 = vol.f() / e2.f() ** 1.5
    fb = {'3': 8, '4': 6, '8': 12} if rd else {'3': 20, '5': 12, '8': 30}
    nV, nE, nF = (48, 72, 26) if rd else (120, 180, 62)
    meta = base('89', True, PATH89 + ' (s2b_rhombic_exact.py)')
    meta.update(name=full, field_definition=fdef(K[1].F, ('t = sqrt2 + sqrt3 + sqrt5 (the rhombus half-angles of the rhombic dodecahedron bring '
                'in sqrt3 and sqrt6, the golden ratio sqrt5).' if rd else 'w = sqrt(2 + phi) = sqrt((5 + sqrt5)/2); sqrt5 = 2 w**2 - 5, phi = w**2 - 2.')),
                status=("new: one of the four golden rhombic cuts that join the DICTO-Kepler golden truncations, new within #89's checks "
                        "(#89 Section 8; web searches found no golden-ratio truncation of Catalan solids; Zefiro 2011 cut the cubic Archimedean "
                        "solids looking for regular faces, without golden ratios)"),
                scale_note=(f"the {cat.lower()} as the polar of the {'cuboctahedron (+-1, +-1, 0)' if rd else 'icosidodecahedron of edge 1'} in the unit "
                            f"sphere (edge^2 = {fmt(e2)} here; #89 Table 2 is at edge 1: divide lengths by sqrt({fmt(e2)})); each corner cut by the plane "
                            f"through the points at y of its edges, y_sharp = a/(2 sin(alpha/2)) at the {valA}-valent (acute) corners and y_blunt = "
                            f"a/(2 cos(alpha/2)) at the 3-valent ones, b = 1/(1 + {'phi K' if g == 'G' else 'K/phi'}), a = {'phi b' if g == 'G' else 'b/phi'}, "
                            f"K = {'(2 sqrt3 + sqrt6)/4' if rd else 'phi sqrt(2 + phi)/2'} (#89 Theorem 3)"))
    pub = {'f_vector': [nV, nE, nF], 'faces_by_sides': fb, 'squared_edge_lengths': sorted({fmt(a * a * e2), fmt(b * b * e2)}),
           'a_edge_1': pa, 'b_edge_1': pb, 'y_sharp_edge_1': pys, 'y_blunt_edge_1': pyb, 'volume_edge_1': pvol + ' (#89 Table 2)',
           'faces_as_published': ('12 octagons, 6 squares, 8 triangles' if rd else '30 octagons, 12 pentagons, 20 triangles') + ' (#89 Table 2)'}
    # every corner face regular of side a, octagon sides alternate a, b
    corner_ok = all(len({dot(sub(V[f[i]], V[f[(i + 1) % len(f)]]), sub(V[f[i]], V[f[(i + 1) % len(f)]])) for i in range(len(f))}) == 1
                    and dot(sub(V[f[0]], V[f[1]]), sub(V[f[0]], V[f[1]])) == a * a * e2 for f in F if len(f) != 8)
    def sides(f): return [dot(sub(V[f[i]], V[f[(i + 1) % len(f)]]), sub(V[f[i]], V[f[(i + 1) % len(f)]])) for i in range(len(f))]
    oct_ok = all(set(sides(f)) == {a * a * e2, b * b * e2} and all(sides(f)[i] != sides(f)[(i + 1) % 8] for i in range(8)) for f in F if len(f) == 8)
    checks = [(f'{a.f():.6f}' == pa and f'{b.f():.6f}' == pb, f'a = {a.dec(6)}, b = {b.dec(6)} at edge 1 (#89 Table 2: {pa}, {pb})'),
              (f'{ys.f():.6f}' == pys and f'{yb.f():.6f}' == pyb, f'y_sharp = {ys.dec(6)}, y_blunt = {yb.dec(6)} (#89 Table 2: {pys}, {pyb})'),
              (f'{vol1:.{6 - len(str(int(vol1)))}f}' == pvol, f'volume at edge 1 = {vol1:.7f} (#89 Table 2: {pvol})'),
              (corner_ok, 'every corner face regular, of side a (#89 Table 2)'),
              (oct_ok, 'every octagon alternates sides a, b, a/b = ' + ('phi' if g == 'G' else '1/phi') + ' exactly'),
              ((a == phi * b) if g == 'G' else (b == phi * a), ('a = phi b' if g == 'G' else 'b = phi a') + ' exactly')]
    if (cat, g) == ('Rhombic Triacontahedron', 'L'): checks.append((b == 2 / (2 + w), 'b = 2/(2 + sqrt(2 + phi)) exactly (#89 Table 2)'))
    emit(slug, meta, V, F, pub, checks)
for cat in ('Rhombic Dodecahedron', 'Rhombic Triacontahedron'):
    G_ = next(r for r in RHOMBIC if r[12] == cat and r[11] == 'G'); L_ = next(r for r in RHOMBIC if r[12] == cat and r[11] == 'L')
    log(G_[6].f() > L_[6].f() and G_[7].f() > L_[7].f() and volume(G_[2], G_[3]).f() < volume(L_[2], L_[3]).f(),
        f'{cat}: the greater cut is deeper at both kinds of corner and leaves less volume (#89 Section 5)')

# ================================================================== 4. #89 golden cuts of the snub dodecahedron, in Q(xi), xi^3 - 2 xi = phi
FX = AlgField.get([1, 0, -4, -1, 4, 2, -1], Fr(17, 10), Fr(9, 5), 'xi'); xi = RF([0, 1], FX)
phiX = xi * xi * xi - 2 * xi; s5X = 2 * phiX - 1
_px = sp.Poly(sp.Symbol('xi') ** 6 - 4 * sp.Symbol('xi') ** 4 - sp.Symbol('xi') ** 3 + 4 * sp.Symbol('xi') ** 2 + 2 * sp.Symbol('xi') - 1)
log(_px.is_irreducible and _px.count_roots(sp.Rational(17, 10), sp.Rational(9, 5)) == 1 and phiX * phiX == phiX + 1 and s5X * s5X == 5,
    f'snub field: xi^6 - 4 xi^4 - xi^3 + 4 xi^2 + 2 xi - 1 (= (xi^3 - 2 xi)^2 - (xi^3 - 2 xi) - 1) irreducible, one root in (17/10, 9/5), xi = {xi.dec(12)}; phi = xi^3 - 2 xi')
# the rotation group I, exact, from the icosahedron of #88's frame
Vic, Fic = platonic('Icosahedron', Q(1))
GI = [M for M, s_ in sym_group(Vic, Fic) if s_ > 0]; log(len(GI) == 60, 'rotation group of the icosahedron: 60 exact matrices in Q(sqrt5)')
mpmath.mp.dps = 120
def mq(q): return mpmath.mpf(q.a.numerator) / q.a.denominator + mpmath.mpf(q.b.numerator) / q.b.denominator * mpmath.sqrt(5)
GM = [mpmath.matrix([[mq(M[i][j]) for j in range(3)] for i in range(3)]) for M in GI]
Gf = [np.array([[float(mq(M[i][j])) for j in range(3)] for i in range(3)]) for M in GI]
from scipy.optimize import minimize
from scipy.spatial import ConvexHull
def orbit_f(p): return np.array([M @ p for M in Gf])
def obj(q):
    p = np.array([1.0, q[0], q[1]]); P = orbit_f(p); d = np.sort(np.linalg.norm(P - P[0], axis=1))[1:7]
    return float(np.var(d[:5] / d[:5].mean())) + (0 if d[5] > 1.05 * d[4] else 1)
rng = np.random.default_rng(1); best = None
for _ in range(2000):
    r = minimize(obj, rng.normal(size=2) * 2, method='Nelder-Mead', options=dict(xatol=1e-14, fatol=1e-30, maxiter=20000))
    if r.fun < 1e-20:
        P = orbit_f(np.array([1.0, *r.x])); ch = ConvexHull(P)
        if len(P) == 60 and len(np.unique(np.round(P, 8), axis=0)) == 60: best = r.x; break
assert best is not None, 'snub vertex not found'
p0 = np.array([1.0, *best]); P = orbit_f(p0); nb = np.argsort(np.linalg.norm(P - P[0], axis=1))[1:6]
def dists(y, z):
    p = mpmath.matrix([1, y, z]); return [mpmath.norm(GM[j] * p - p) ** 2 for j in nb]
# |p - g p| = |p - g^-1 p|, so the five distances hold only two independent equations: try the pairs until Newton converges
for i, k in itertools.combinations(range(1, 5), 2):
    try:
        sol = mpmath.findroot(lambda y, z: [dists(y, z)[0] - dists(y, z)[i], dists(y, z)[0] - dists(y, z)[k]], (mpmath.mpf(best[0]), mpmath.mpf(best[1])))
    except (ZeroDivisionError, ValueError): continue
    dd = dists(sol[0], sol[1])
    if max(abs(x - dd[0]) for x in dd) < mpmath.mpf(10) ** -100: break
yv, zv = sol[0], sol[1]
pm = mpmath.matrix([1, yv, zv]); dd = [mpmath.norm(GM[j] * pm - pm) ** 2 for j in nb]
log(max(abs(x - dd[0]) for x in dd) < mpmath.mpf(10) ** -100, 'snub vertex (1, y, z): five equal nearest distances to 100 digits (mpmath)')
xv = mpmath.findroot(lambda s: s ** 3 - 2 * s - (1 + mpmath.sqrt(5)) / 2, 1.7155)
def recog(v):
    rel = mpmath.pslq([v] + [xv ** k for k in range(6)], maxcoeff=10 ** 12, maxsteps=10 ** 6)
    assert rel and rel[0] != 0, 'no relation'
    return RF([Fr(-c, rel[0]) for c in rel[1:]], FX)
Y, Z = recog(yv), recog(zv)
GX = [[[conv5(M[i][j], s5X) for j in range(3)] for i in range(3)] for M in GI]
p = (RF([1], FX), Y, Z)
SN = list(dict.fromkeys(tuple(sum((M[i][k] * p[k] for k in range(3)), RF([0], FX)) for i in range(3)) for M in GX))
Vs, Fs = hull(SN)
els = {dot(sub(Vs[a], Vs[b]), sub(Vs[a], Vs[b])) for a, b in edges_of(Fs)}
log(len(Vs) == 60 and Counter(len(f) for f in Fs) == Counter({3: 80, 5: 12}) and len(els) == 1,
    f'snub dodecahedron, exact in Q(xi): y = {fmt(Y)}, z = {fmt(Z)} (found by PSLQ, then proved): 60 corners, 80 triangles, 12 pentagons, all 150 edges equal exactly')
GS = sym_group(Vs, Fs); log(len(GS) == 60 and all(s_ > 0 for _, s_ in GS), 'snub dodecahedron: symmetry group of order 60, rotations only (chiral, I)')
e2s = next(iter(els)); oneX = RF([1], FX)
for g in ('G', 'L'):
    x = oneX / 3 if g == 'G' else (5 - s5X) / 10
    V, F = cut(Vs, Fs, {i: x for i in range(60)})
    full = ('Greater' if g == 'G' else 'Lesser') + ' Golden Cut Snub Dodecahedron L/R'
    slug = 'dicto-' + ('greater' if g == 'G' else 'lesser') + '-golden-cut-snub-dodecahedron'
    meta = base('89', True, PATH89 + ' (s1_platonic_archimedean.py; Theorem 2)')
    meta.update(name=full, field_definition=fdef(FX, 'xi is the real root of xi**3 - 2*xi = phi (the snub dodecahedron\'s cubic); phi = xi**3 - 2*xi, sqrt5 = 2*xi**3 - 4*xi - 1.'),
                status=("new: one of the six DICTO Golden-Regular Cuts (#89 Theorem 2: every face golden or regular), which DICTO named; "
                        + ("the lesser one, whose truncated triangles have ratio exactly phi, DICTO added to the DICTO-GTT-Solids; " if g == 'L' else '')
                        + "not found in the sources checked (#89 Section 8)"),
                scale_note=("the snub dodecahedron as the orbit of (1, y, z) under the 60 rotations of the icosahedron (0, +-1/2, +-phi/2) cyclic, "
                            f"y = {fmt(Y)}, z = {fmt(Z)} (edge^2 = {fmt(e2s)} here, {e2s.dec(9)}); every corner cut at x = "
                            + ('1/3' if g == 'G' else '1/(phi sqrt5) = (5 - sqrt5)/10') + " of its edges (#89 Theorem 2). Chiral: this file is one hand; "
                            "the other hand (L/R, one D-number for both, as in the Concordance) is its mirror image (x, y, z) -> (-x, y, z)."))
    nb_ = Counter(len(f) for f in F)
    x2 = x * x * e2s; o2 = (1 - 2 * x) * (1 - 2 * x) * e2s; p2 = phiX * phiX * x * x * e2s
    if g == 'G': want = {x2: 240 + 150, p2: 60}        # x = 1/3: corner sides on triangles x, on pentagons phi x; original sides 1/3
    else: want = {x2: 240, o2: 210}                    # original sides 1 - 2x = phi x = sqrt5/5: the pentagons become regular decagons
    elc = Counter(dot(sub(V[a], V[b]), sub(V[a], V[b])) for a, b in edges_of(F))
    pub = {'f_vector': [300, 450, 152], 'faces_by_sides': {'5': 60, '6': 80, '10': 12}, 'symmetry_order': 60,
           'faces_as_published': ('80 regular hexagons, 12 golden truncated pentagons (corner sides long)' if g == 'G' else
                                  '80 truncated triangles of ratio phi (original sides long), 12 regular decagons') + ', 60 corner pentagons (#89 Theorem 2)',
           'cut_x': '1/3' if g == 'G' else '1/(phi sqrt5) = (5 - sqrt5)/10'}
    def face_sides(f): return [dot(sub(V[f[i]], V[f[(i + 1) % len(f)]]), sub(V[f[i]], V[f[(i + 1) % len(f)]])) for i in range(len(f))]
    hexes = [face_sides(f) for f in F if len(f) == 6]; decs = [face_sides(f) for f in F if len(f) == 10]
    checks = [(dict(elc) == want, 'edge lengths and counts as Theorem 2 implies: ' + ', '.join(f'{z.dec(6)} x {c}' for z, c in elc.items())),
              ((all(len(set(h)) == 1 for h in hexes) and all(len(set(d_)) == 2 for d_ in decs)) if g == 'G' else
               (all(len(set(h)) == 2 for h in hexes) and all(len(set(d_)) == 1 for d_ in decs)),
               ('triangles became regular hexagons, pentagons golden decagons' if g == 'G' else 'pentagons became regular decagons, triangles truncated triangles')),
              ((p2 == phiX * phiX * x2 and x2 * 9 == e2s) if g == 'G' else (o2 == phiX * phiX * x2),
               'long/short = phi exactly on the golden faces' + (' (pentagons: phi x against 1/3)' if g == 'G' else ' (triangles: (1 - 2x)/x = (1 + sqrt5)/2)'))]
    emit(slug, meta, V, F, pub, checks)
# controls (not written): #89's exact volumes of the Lesser and Greater Golden Cut Icosidodecahedra (Zefiro's stages), edge 1
for g, x, ref in (('L', (5 - S5) / 10, '13/2 + 97*sqrt(5)/30'), ('G', Q(Fr(1, 3)), '395/54 + 17*sqrt(5)/6')):
    V, F = cut(Vid, Fid, {i: x for i in range(30)})
    log(volume(V, F) == ev(ref, K5), f'control: icosidodecahedron cut at x = {fmt(x)}: volume {fmt(volume(V, F))} = {ref} (#89 Theorem 2)')

# ================================================================== 5. unit-volume copies (as build_v5.py; centre = the corner centroid)
mpmath.mp.dps = 60
def mpx(x):
    if isinstance(x, RF): return x.mp()
    return mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(x.d)
def dec15(m):
    from decimal import Decimal
    qd = Decimal(mpmath.nstr(m, 50, strip_zeros=False, min_fixed=-mpmath.inf, max_fixed=mpmath.inf)).quantize(Decimal(1).scaleb(-15))
    return format(qd, 'f') if qd != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-15)), 'f')
def parse_field(s, x0):
    if isinstance(x0, RF):
        t = sp.Symbol(x0.F.name); cs = sp.Poly(sp.expand(sp.sympify(s, locals={x0.F.name: t})), t).all_coeffs()
        return RF([Fr(int(c.p), int(c.q)) for c in reversed(cs)], x0.F)
    e = sp.expand(sp.sympify(s)); a = b = Fr(0)
    for tt, c in e.as_coefficients_dict().items():
        if tt == 1: a += Fr(int(c.p), int(c.q))
        else: b += Fr(int(c.p), int(c.q))
    return QF(a, b, x0.d)
for slug, V in BUILT:
    p_ = os.path.join(SOL, slug + '.json'); doc = json.load(open(p_))
    z0 = V[0][0] * 0; vol = parse_field(doc['volume']['exact'], z0)
    c = tuple(sum((v[k] for v in V), z0) / len(V) for k in range(3))
    s = mpmath.power(mpx(vol), mpmath.mpf(-1) / 3)
    W = [[mpx(c[k]) + s * (mpx(v[k]) - mpx(c[k])) for k in range(3)] for v in V]
    at_origin = all(x.sign() == 0 for x in c)
    uv = {'scale_exact': f"({doc['volume']['exact']})**(-1/3)", 'scale_decimal': dec15(s),
          'centre': {'exact': [fmt(x) for x in c], 'decimal': [x.dec() for x in c],
                     'kind': 'origin of the frame (= the corner centroid)' if at_origin else 'corner centroid (mean of the corners; the frame origin is not the centre)'},
          'note': 'x -> centre + s (x - centre), s = V^(-1/3) with V the exact volume above; s is symbolic and the corners are decimals (15 places, '
                  'as elsewhere). Same corner order and faces as above; volume 1.',
          'vertices_decimal': [[dec15(x) for x in w_] for w_ in W]}
    out = {}
    for k, v in doc.items():
        out[k] = v
        if k == 'volume': out['unit_volume'] = uv
    out['checks'] = dict(out['checks'], unit_volume='decimal unit-volume copy has volume 1 (1e-12) and is the solid scaled by s (check.py)')
    json.dump(out, open(p_, 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(SOL, slug + '-unit-volume.off'), 'w') as fh:
        fh.write('OFF\n# ' + doc['name'] + ', unit volume (scaled by V^(-1/3) about ' + ('the origin' if at_origin else 'its corner centroid')
                 + ') — Created by DICTO · dictospheres.com — CC BY-SA 4.0\n')
        fh.write(f"{len(V)} {len(doc['faces'])} {doc['f_vector']['edges']}\n")
        for w_ in uv['vertices_decimal']: fh.write(' '.join(w_) + '\n')
        for f in doc['faces']: fh.write(str(len(f)) + ' ' + ' '.join(map(str, f)) + '\n')
    log(True, f'{slug}: unit-volume copy, s = {uv["scale_decimal"]}, centre {uv["centre"]["kind"]}')

log(True, 'left out: D110 HexOct c-tile (not a closed surface, above); D133 DICTO Void Keeper and D134 DICTO Golden Skin (#96 Section 6: '
          '"Still open: exact forms of the Void Keeper and the Golden Skin"; the densest lattice of the cut OG is found in floating point, '
          'and the Golden Skin is one piece per brick size)')
json.dump(LOG, open(os.path.join(HERE, 'build_v8.log.json'), 'w'), indent=1, ensure_ascii=False)
print(f"{sum(l.startswith('PASS') for l in LOG)} PASS, {sum(l.startswith('FAIL') for l in LOG)} FAIL")
