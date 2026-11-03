"""Step 9 (paper #89, "Why not the cubes"). Exact in K = Q(sqrt2, sqrt5) (cubes_lib.K) and sympy Groebner bases.
Part A. No hyperplane section of a regular 4D polytope is a cube cut at its corners (any depth 0 < x < 1/2):
  every face of a section is a plane section of one cell; tetrahedra give at most 4 sides, cubes and octahedra at most 6
  (proof in the paper; random-plane sanity here), and a regular dodecahedron has no plane section that is an
  equiangular octagon: Groebner basis = [1] for all 45 configurations of four face axes (positive control included).
Part B. Reflection groups A4, B4, F4, H4 built from their roots: group orders, rank-3 parabolic subgroup orders,
  stabiliser orders of the main directions (orbit-stabiliser). By Steinberg the stabiliser of a direction is parabolic.
Part C. Exact section sequences of the regular polytopes in their cube-symmetric (O_h) directions, and of the 600-cell
  and 120-cell in their icosahedral direction, the inscribed 24-cell's directions and the central A3 direction.
Part D. Uniform polytopes of the B4 and F4 families: every section perpendicular to e1 (the B3 direction; for F4 the
  other O_h class is e1 of the diagram-reversed polytope) and the central B4 section perpendicular to (1,1,1,1).
  Corner-cut-cube gaps: exact depth range; golden hits located exactly and matched corner to corner (as s8).
Part E. Uniform polytopes of the H4 family: the only O_h sections are central, perpendicular to a 120-cell corner
  direction (Part B); each checked (floating point classification; any cube-like hit would be checked exactly).
usage (dicto-big-brother): ~/geom/bin/python s9_why_not_cubes.py [A|B|C|D|E ...] -> ../data/s9-why-not-cubes-<part>.json
"""
import sys, os, json, itertools, time, math
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data'); sys.path.insert(0, HERE)
from cubes_lib import *          # noqa
CHECKS = []; OUT = {}
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def regname(sig, n):
    names = {(4, ((3, 4),)): 'regular tetrahedron', (8, ((4, 6),)): 'cube', (6, ((3, 8),)): 'octahedron',
             (12, ((3, 8), (4, 6))): 'cuboctahedron', (24, ((3, 8), (8, 6))): 'cube cut at the corners (truncated-cube type)',
             (24, ((4, 6), (6, 8))): 'octahedron cut at the corners (truncated-octahedron type)',
             (32, ((4, 6), (6, 12))): 'cube cut along its edges (chamfered cube)',
             (14, ((4, 12),)): 'rhombic dodecahedron', (12, ((3, 20),)): 'icosahedron', (20, ((5, 12),)): 'dodecahedron', (30, ((3, 20), (5, 12))): 'icosidodecahedron'}
    return names.get((n, tuple(sorted(sig.items()))), '')


def sequence(V, E, d, central_only=False):
    """vertex layers and the section type at each layer and inside each gap (exact faces)"""
    H = [dot(v, d) for v in V]
    hs = sorted(set([ZERO] + [h for h in H if h.sign() > 0]), key=float)     # the centre and every corner height above it
    rows = []
    def one(h, lab):
        P = section(V, E, d, h, H)
        if len(P) < 4: return {'where': lab, 'height': kstr(h), 'corners': len(P)}
        fa = faces_exact(P, d); sg = signature(fa)
        return {'where': lab, 'height': kstr(h), 'corners': len(P), 'faces': {str(k): v for k, v in sg.items()}, 'name': regname(sg, len(P))}
    if central_only:
        return [one(ZERO, 'centre')]
    for k, h in enumerate(hs):
        r = one(h, 'layer'); r['layer_corners'] = sum(1 for x in H if x == h); rows.append(r)
        if k + 1 < len(hs): rows.append(one((h + hs[k + 1]) / 2, 'gap'))
    return rows


# ------------------------------------------------------------------------------------------------ Part A
def partA():
    import sympy as sp
    n1, n2, n3, t, g = sp.symbols('n1 n2 n3 t g')
    N = (n1, n2, n3)
    def dt(a, b): return sum(x * y for x, y in zip(a, b))
    nn = dt(N, N)
    def vv(a, b): return nn * dt(a, b) - dt(N, a) * dt(N, b)        # (n x a).(n x b)
    def system(a):
        return [vv(a[0], a[2]), vv(a[1], a[3]), 2 * vv(a[0], a[1]) ** 2 - vv(a[0], a[0]) * vv(a[1], a[1]),
                t * vv(a[0], a[0]) * vv(a[1], a[1]) * vv(a[2], a[2]) * vv(a[3], a[3]) - 1, g ** 2 - g - 1]
    ax = [(0, 1, g), (0, 1, -g), (1, g, 0), (1, -g, 0), (g, 0, 1), (-g, 0, 1)]   # the six face axes of the dodecahedron
    seen = set(); res = []
    for q in itertools.permutations(range(6), 4):
        rq = tuple(reversed(q))
        k = min([q[i:] + q[:i] for i in range(4)] + [rq[i:] + rq[:i] for i in range(4)])
        if k in seen: continue
        seen.add(k)
        G = sp.groebner(system([ax[i] for i in q]), t, n1, n2, n3, g, order='grevlex')
        res.append(list(G.exprs) == [1])
    check(f'dodecahedron: for all {len(res)} configurations of four face axes (side lines 1 and 3 perpendicular, 2 and 4 '
          f'perpendicular, 1 and 2 at 45 degrees, no side degenerate) the Groebner basis over Q(phi) is [1]: no plane section '
          f'of a regular dodecahedron is an equiangular octagon', all(res) and len(res) == 45)
    ctrl = [(1, 0, 0), (1, 1, 0), (0, 1, 0), (-1, 1, 0)]
    G = sp.groebner(system(ctrl), t, n1, n2, n3, g, order='grevlex')
    check('positive control: four axes at 45 degree steps in a plane give a non-trivial Groebner basis (the method can say yes)', list(G.exprs) != [1])
    # sanity (floating point, not part of the proof): random planes through cube, octahedron, tetrahedron
    rng = np.random.default_rng(1)
    sol = {'tetrahedron': [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
           'cube': list(itertools.product((1, -1), repeat=3)),
           'octahedron': [tuple(s * (i == k) for k in range(3)) for i in range(3) for s in (1, -1)]}
    mx = {}
    for nm, Vs in sol.items():
        V = np.array(Vs, float); D = ((V[:, None] - V[None]) ** 2).sum(-1); m = D[D > 0].min()
        E = [(i, j) for i in range(len(V)) for j in range(i + 1, len(V)) if abs(D[i, j] - m) < 1e-9]
        best = 0
        for _ in range(20000):
            n = rng.normal(size=3); n /= np.linalg.norm(n); c = rng.uniform(-1, 1) * np.abs(V @ n).max()
            k = sum(1 for i, j in E if (V[i] @ n - c) * (V[j] @ n - c) < 0); best = max(best, k)
        mx[nm] = best
    check(f'sanity (floating point, 20000 random planes each): most sides of a plane section: {mx} (bounds 4, 6, 6)',
          mx['tetrahedron'] <= 4 and mx['cube'] <= 6 and mx['octahedron'] <= 6)
    OUT['A'] = {'dodecahedron_equiangular_octagon_configs': len(res), 'random_plane_max_sides': mx}


# ------------------------------------------------------------------------------------------------ Part B
GEN = (K(Fr(1, 7)), K(Fr(3, 11)), K(Fr(5, 13)), K(Fr(17, 19)))
def groups():
    out = {}
    out['B4'] = roots_B4(); out['F4'] = roots_F4(); out['H4'] = v600()
    return out


def forbit(p, roots):
    """orbit size counted in floating point (points rounded to 1e-9; orbit points are far apart), used for H4 only"""
    S = [fl(r) for r in roots]; G = [np.eye(4) - 2 * np.outer(s, s) / (s @ s) for s in S]
    p = fl(p); seen = {tuple(np.round(p, 9))}; todo = [p]
    while todo:
        q = todo.pop()
        for g in G:
            r = g @ q; k = tuple(np.round(r, 9))
            if k not in seen: seen.add(k); todo.append(r)
    return len(seen)


def partB():
    G = groups(); res = {}
    weights = {
        'B4': {'(1,0,0,0): tesseract cell-first, 16-cell corner-first': (ONE, ZERO, ZERO, ZERO),
               '(1,1,1,1): tesseract corner-first, 16-cell cell-first': (ONE, ONE, ONE, ONE),
               '(1,1,0,0): tesseract face-first, 16-cell edge-first': (ONE, ONE, ZERO, ZERO),
               '(1,1,1,0): tesseract edge-first, 16-cell face-first': (ONE, ONE, ONE, ZERO)},
        'F4': {'(1,0,0,0): 24-cell cell-first (same orbit as (1,1,1,1))': (ONE, ZERO, ZERO, ZERO),
               '(1,1,0,0): 24-cell corner-first': (ONE, ONE, ZERO, ZERO),
               '(2,1,1,0): 24-cell face-first': (K(2), ONE, ONE, ZERO),
               '(3,1,1,1): 24-cell edge-first': (K(3), ONE, ONE, ONE)}}
    V6 = v600()
    # 120-cell corner = centroid of a 600-cell tetrahedral cell; 600-cell edge midpoint; triangle centre
    F6 = np.array([fl(v) for v in V6]); D = ((F6[:, None] - F6[None]) ** 2).sum(-1); m = D[D > 1e-9].min()
    adj = [set(np.where(np.abs(D[i] - m) < 1e-9)[0]) for i in range(120)]
    a = 0; b = min(adj[a]); c = min(adj[a] & adj[b]); dd = min((adj[a] & adj[b] & adj[c]) - {a, b, c})
    cell = [V6[i] for i in (a, b, c, dd)]
    weights['H4'] = {'600-cell corner (= 120-cell cell centre; = (1,0,0,0), a corner of the inscribed 24-cells)': V6[0],
                     '600-cell cell centre (= 120-cell corner)': tuple(sum((v[k] for v in cell), ZERO) for k in range(4)),
                     '600-cell edge midpoint (= 120-cell pentagon centre)': vadd(V6[a], V6[b]),
                     '600-cell triangle centre (= 120-cell edge midpoint)': tuple(V6[a][k] + V6[b][k] + V6[c][k] for k in range(4)),
                     '(1,1,0,0): cell centre of the inscribed 24-cell with corners (±1,0,0,0), (±1/2,...) = a 120-cell corner direction': (ONE, ONE, ZERO, ZERO)}
    for name, R in G.items():
        osz = (lambda p, RR: forbit(p, RR)) if name == 'H4' else (lambda p, RR: len(orbit(p, RR)))
        simple0, _ = chain(simple_roots(R, GEN))
        order = osz(GEN, simple0)
        simple, bonds = chain(simple_roots(R, GEN))
        par = {}
        for omit in range(4):
            sub = [s for k, s in enumerate(simple) if k != omit]
            par[f'omit node {omit + 1}'] = len(orbit(GEN, sub))
        stabs = {lab: order // osz(w, simple) for lab, w in weights[name].items()}
        res[name] = {'order': order, 'diagram_bonds': bonds, 'rank3_parabolic_orders': par, 'stabiliser_orders': stabs}
        print(name, res[name], flush=True)
    # A4 (5-cell) in R^5
    R5 = roots_A4(); gen5 = (K(Fr(1, 7)), K(Fr(3, 11)), K(Fr(5, 13)), K(Fr(17, 19)), K(Fr(23, 29)))
    o5 = len(orbit(gen5, R5)); s5, b5 = chain(simple_roots(R5, gen5))
    res['A4'] = {'order': o5, 'diagram_bonds': b5, 'rank3_parabolic_orders': {f'omit node {k + 1}': len(orbit(gen5, [s for j, s in enumerate(s5) if j != k])) for k in range(4)}}
    print('A4', res['A4'], flush=True)
    check('group orders: A4 120, B4 384, F4 1152, H4 14400 (H4 orbits counted in floating point)', (o5, res['B4']['order'], res['F4']['order'], res['H4']['order']) == (120, 384, 1152, 14400))
    check('rank-3 parabolic orders: B4 {48, 24, 16, 12}; F4 {48, 48, 12, 12}; H4 {120, 24, 20, 12}; A4 {24, 12, 12, 24}',
          sorted(res['B4']['rank3_parabolic_orders'].values()) == [12, 16, 24, 48] and sorted(res['F4']['rank3_parabolic_orders'].values()) == [12, 12, 48, 48]
          and sorted(res['H4']['rank3_parabolic_orders'].values()) == [12, 20, 24, 120] and sorted(res['A4']['rank3_parabolic_orders'].values()) == [12, 12, 24, 24])
    check('only B4 and F4 have a parabolic subgroup of order divisible by 48 (B3, C3); for H4 and A4 none, and H4 has only '
          'one of order 24 (A3, the stabiliser of a 120-cell corner)',
          not any(o % 48 == 0 for o in res['H4']['rank3_parabolic_orders'].values()) and not any(o % 48 == 0 for o in res['A4']['rank3_parabolic_orders'].values()))
    st = res['H4']['stabiliser_orders']
    check(f'H4 stabilisers: 600-cell corner {list(st.values())[0]} (icosahedral), 120-cell corner {list(st.values())[1]} (A3), '
          f'inscribed 24-cell cell centre (1,1,0,0) {list(st.values())[4]}', list(st.values())[:2] == [120, 24])
    check('B4 stabiliser of (1,0,0,0) has order 48 and of (1,1,1,1) order 24; F4 stabilisers of (1,0,0,0) and (1,1,0,0) have order 48',
          list(res['B4']['stabiliser_orders'].values())[:2] == [48, 24] and list(res['F4']['stabiliser_orders'].values())[:2] == [48, 48])
    OUT['B'] = res


# ------------------------------------------------------------------------------------------------ Part C
def regular(name):
    if name == 'tesseract': V = [tuple(K(s) for s in ss) for ss in itertools.product((1, -1), repeat=4)]
    elif name == '16-cell': V = [tuple(K(s if k == i else 0) for k in range(4)) for i in range(4) for s in (1, -1)]
    elif name == '24-cell': V = [tuple(K(s if k == i else t if k == j else 0) for k in range(4)) for i, j in itertools.combinations(range(4), 2) for s in (1, -1) for t in (1, -1)]
    elif name == '600-cell': V = v600()
    elif name == '120-cell':
        V6 = v600(); F6 = np.array([fl(v) for v in V6]); D = ((F6[:, None] - F6[None]) ** 2).sum(-1); m = D[D > 1e-9].min()
        adj = [set(np.where(np.abs(D[i] - m) < 1e-9)[0]) for i in range(120)]; cells = set()
        for a in range(120):
            for b in adj[a]:
                for c in adj[a] & adj[b]:
                    for d in adj[a] & adj[b] & adj[c]: cells.add(tuple(sorted((a, b, c, d))))
        assert len(cells) == 600
        V = [tuple(sum((V6[i][k] for i in c), ZERO) for k in range(4)) for c in sorted(cells)]
    E = edges_at(V, min_d2(V))
    return V, E


def partC():
    res = {}
    V6 = v600()
    F6 = np.array([fl(v) for v in V6]); D = ((F6[:, None] - F6[None]) ** 2).sum(-1); m = D[D > 1e-9].min()
    adj = [set(np.where(np.abs(D[i] - m) < 1e-9)[0]) for i in range(120)]
    a = 0; b = min(adj[a]); c = min(adj[a] & adj[b]); dd = min((adj[a] & adj[b] & adj[c]) - {a, b, c})
    A3 = tuple(sum((V6[i][k] for i in (a, b, c, dd)), ZERO) for k in range(4))
    e1 = (ONE, ZERO, ZERO, ZERO); e1111 = (ONE, ONE, ONE, ONE); e11 = (ONE, ONE, ZERO, ZERO)
    plan = [('tesseract', '(1,0,0,0) cell-first', e1, False), ('tesseract', '(1,1,1,1) corner-first, centre', e1111, True),
            ('16-cell', '(1,0,0,0) corner-first', e1, False), ('16-cell', '(1,1,1,1) cell-first, centre', e1111, True),
            ('24-cell', '(1,0,0,0) cell-first', e1, False), ('24-cell', '(1,1,0,0) corner-first', e11, False),
            ('600-cell', '(1,0,0,0) corner-first (icosahedral; the inscribed 24-cells\' corner direction)', e1, False),
            ('600-cell', '(1,1,0,0) cell-first (A3: the inscribed 24-cell\'s cell direction)', e11, False),
            ('120-cell', '(1,0,0,0) cell-first (icosahedral)', e1, False),
            ('120-cell', '(1,1,0,0) corner-first (A3)', e11, False)]
    V12, _ = regular('120-cell')
    check('(1,1,0,0) is the direction of a 120-cell corner (some corner has x1 = x2 > 0, x3 = x4 = 0), so its stabiliser is the A3 of Part B',
          any(v[0] == v[1] and v[0].sign() > 0 and v[2].iszero() and v[3].iszero() for v in V12))
    cache = {}
    for nm, lab, d, cen in plan:
        t0 = time.time()
        if nm not in cache: cache[nm] = regular(nm)
        V, E = cache[nm]
        rows = sequence(V, E, d, cen)
        res[f'{nm} {lab}'] = rows
        print(f'--- {nm} {lab} ({len(V)} corners, {len(E)} edges; {time.time() - t0:.0f}s)', flush=True)
        for r in rows: print('   ', r, flush=True)
        cc = [r for r in rows if r.get('faces') and r['corners'] == 24 and r['faces'].get('8') == 6 and r['faces'].get('3') == 8]
        check(f'{nm} {lab}: no section in this sequence is a cube cut at the corners (8 triangles, 6 octagons)', not cc)
    OUT['C'] = res


# ------------------------------------------------------------------------------------------------ Part D
NAMES_B4 = {(1,): 'tesseract', (2,): 'rectified tesseract', (3,): 'rectified 16-cell (= 24-cell)', (4,): '16-cell',
            (1, 2): 'truncated tesseract', (1, 3): 'cantellated tesseract', (1, 4): 'runcinated tesseract',
            (2, 3): 'bitruncated tesseract', (2, 4): 'cantellated 16-cell (= rectified 24-cell)', (3, 4): 'truncated 16-cell',
            (1, 2, 3): 'cantitruncated tesseract', (1, 2, 4): 'runcitruncated tesseract', (1, 3, 4): 'runcitruncated 16-cell',
            (2, 3, 4): 'cantitruncated 16-cell (= truncated 24-cell)', (1, 2, 3, 4): 'omnitruncated tesseract'}
NAMES_F4 = {(1,): '24-cell', (2,): 'rectified 24-cell', (1, 2): 'truncated 24-cell', (1, 3): 'cantellated 24-cell',
            (1, 4): 'runcinated 24-cell', (2, 3): 'bitruncated 24-cell', (1, 2, 3): 'cantitruncated 24-cell',
            (1, 2, 4): 'runcitruncated 24-cell', (1, 2, 3, 4): 'omnitruncated 24-cell'}
def f4name(r):
    rev = tuple(sorted(5 - k for k in r))
    if r in NAMES_F4: return NAMES_F4[r], 'corner-type O_h direction' if False else None
    return NAMES_F4[rev], 'reversed'


def cube_depth(P):
    """cube axes = coordinates 2..4; A = max x2, B = max(x2+x3+x4); x = (3A - B)/(2A)"""
    A = max((p[1] for p in P), key=float); B = max((p[1] + p[2] + p[3] for p in P), key=float)
    return A, B


def partD():
    res = []; hits = []
    xG, xL = golden_x()
    for fam in ('B4', 'F4'):
        R = roots_B4() if fam == 'B4' else roots_F4()
        simple, bonds = chain(simple_roots(R, GEN))
        if fam == 'F4' and dot(simple[0], simple[0]) != K(2): simple = simple[::-1]   # node 1 = long-root end
        if fam == 'B4':          # tesseract end first: node 1 = short root e4 (4-bond end)
            assert bonds == [4, 3, 3]
        for k in range(1, 5):
            for rings in itertools.combinations(range(1, 5), k):
                t0 = time.time()
                p = wythoff_point(simple, rings)
                V = orbit(p, R); E = edges_at(V, ONE)
                if fam == 'B4': name, dirn = NAMES_B4[rings], 'B3 direction (1,0,0,0)'
                else:
                    if rings in NAMES_F4: name, dirn = NAMES_F4[rings], 'cell-type B3 direction (1,0,0,0)'
                    else: name, dirn = NAMES_F4[tuple(sorted(5 - r for r in rings))], 'corner-type C3 direction (1,0,0,0) of the diagram-reversed copy'
                d = (ONE, ZERO, ZERO, ZERO)
                H = [v[0] for v in V]; hs = sorted(set([ZERO] + [h for h in H if h.sign() > 0]), key=float)
                rows = []
                for j in range(len(hs)):
                    cands = [('layer', hs[j], None)]
                    if j + 1 < len(hs): cands.append(('gap', hs[j], hs[j + 1]))
                    for kind, h0, h1 in cands:
                        h = h0 if kind == 'layer' else (h0 + h1) / 2
                        P = section(V, E, d, h, H)
                        if len(P) < 4: continue
                        fa = faces_exact(P, d); sg = signature(fa)
                        row = {'where': kind, 'height': kstr(h0) if kind == 'layer' else f'{kstr(h0)} .. {kstr(h1)}', 'corners': len(P),
                               'faces': {str(a): b for a, b in sg.items()}, 'name': regname(sg, len(P))}
                        if len(P) == 24 and sg == {3: 8, 8: 6}:
                            if kind == 'layer':
                                A, B = cube_depth(P); row['x'] = kstr((3 * A - B) / (2 * A))
                            else:
                                q1, q3 = (3 * h0 + h1) / 4, (h0 + 3 * h1) / 4
                                A1, B1 = cube_depth(section(V, E, d, q1, H)); A3_, B3 = cube_depth(section(V, E, d, q3, H))
                                sA, sB = (A3_ - A1) / (q3 - q1), (B3 - B1) / (q3 - q1)
                                Af = lambda y: A1 + sA * (y - q1); Bf = lambda y: B1 + sB * (y - q1)
                                Am, Bm = cube_depth(P)
                                assert Am == Af(h) and Bm == Bf(h)
                                xf = lambda y: (3 * Af(y) - Bf(y)) / (2 * Af(y))
                                row['x_range'] = [kstr(xf(h0)), kstr(xf(h1))]; row['x_range_float'] = [float(xf(h0)), float(xf(h1))]
                                for lab, xt in (('Greater', xG), ('Lesser', xL)):
                                    # 3A - B - 2A xt = 0, linear in y
                                    c0 = 3 * A1 - B1 - 2 * A1 * xt; c1 = 3 * sA - sB - 2 * sA * xt
                                    if c1.iszero(): continue
                                    y = q1 - c0 / c1
                                    if (y - h0).sign() > 0 and (h1 - y).sign() > 0:
                                        S = section(V, E, d, y, H)
                                        T = cut_cube(xt)
                                        ok, lam = similar([q[1:] for q in S], T)
                                        hit = {'polytope': name, 'family': fam, 'rings': rings, 'direction': dirn, 'height': kstr(y), 'height_float': float(y),
                                               'gap': [kstr(h0), kstr(h1)], 'solid': f'{lab} Golden Cut Cube', 'x': kstr(xt), 'corners': len(S),
                                               'similar_exact': ok, 'scale_squared': kstr(lam) if ok else None}
                                        hits.append(hit); row.setdefault('golden', []).append(lab)
                                        check(f'{name} ({fam} rings {rings}), {dirn}, height {kstr(y)} = {float(y):.9f}: {len(S)} corners, '
                                              f'corner-to-corner similar to the {lab} Golden Cut Cube, all 276 squared distances scaled by one factor (exact)', ok)
                        rows.append(row)
                # central section perpendicular to (1,1,1,1) for B4 (A3 x {±1} = O_h)
                cen = None
                if fam == 'B4':
                    P = section(V, E, (ONE, ONE, ONE, ONE), ZERO)
                    if len(P) >= 4:
                        sg = signature(faces_exact(P, (ONE, ONE, ONE, ONE))); cen = {'corners': len(P), 'faces': {str(a): b for a, b in sg.items()}, 'name': regname(sg, len(P))}
                res.append({'family': fam, 'rings': rings, 'polytope': name, 'direction': dirn, 'corners': len(V), 'edges': len(E),
                            'sequence': rows, 'central_(1,1,1,1)': cen})
                cubes = [r for r in rows if r['corners'] == 24 and r['faces'] == {'3': 8, '8': 6}]
                print(f'{fam} {rings} {name}: {len(V)} corners, {len(hs)} layers >= 0, {len(cubes)} corner-cut-cube sections '
                      f'{[r.get("x_range_float", r.get("x")) for r in cubes]}; centre {cen}; {time.time() - t0:.0f}s', flush=True)
    OUT['D'] = {'polytopes': res, 'golden_hits': hits}
    check(f'uniform B4 and F4 families: {len(hits)} golden cube sections found and every one proved exactly', all(h['similar_exact'] for h in hits))


# ------------------------------------------------------------------------------------------------ Part E
def partE():
    from scipy.spatial import ConvexHull
    R = v600(); simple, bonds = chain(simple_roots(R, GEN))
    assert bonds == [5, 3, 3], bonds
    S = np.array([fl(s) for s in simple])
    w = np.linalg.solve(S, np.array([1., 0, 0, 0]))           # weight of node 1 (5-end): stabiliser A3 = 120-cell corner
    G = [np.eye(4) - 2 * np.outer(s, s) / (s @ s) for s in S]
    res = []
    for k in range(1, 5):
        for rings in itertools.combinations(range(1, 5), k):
            p = np.linalg.solve(S, np.array([0.5 * np.linalg.norm(S[i]) if (i + 1) in rings else 0 for i in range(4)]))
            pts = {tuple(np.round(p, 6)): p}; todo = [p]            # breadth-first from p, so errors stay ~1e-14
            while todo:
                nxt = []
                for q in todo:
                    for g in G:
                        r = g @ q; kk = tuple(np.round(r, 6))
                        if kk not in pts: pts[kk] = r; nxt.append(r)
                todo = nxt
            V = np.array(list(pts.values())); t = cKDTree(V); E = np.array(sorted(t.query_pairs(1 + 1e-6)))
            dn = w / np.linalg.norm(w); Hh = V @ dn
            a, b = Hh[E[:, 0]], Hh[E[:, 1]]; mk = a * b < -1e-12
            tt = a[mk] / (a[mk] - b[mk]); P = V[E[mk, 0]] + tt[:, None] * (V[E[mk, 1]] - V[E[mk, 0]])
            P = np.vstack([P, V[np.abs(Hh) < 1e-9]])
            B = np.linalg.svd(dn[None])[2][1:]; Q = np.unique(np.round(P @ B.T, 8), axis=0)
            hl = ConvexHull(Q); groups = []; reps = []
            for eq, sx in zip(hl.equations, hl.simplices):          # merge coplanar hull triangles (tolerance 1e-6)
                for gi, r in enumerate(reps):
                    if np.abs(r - eq).max() < 1e-6: groups[gi].update(sx); break
                else: reps.append(eq); groups.append(set(sx))
            groups = {i: g for i, g in enumerate(groups)}
            from collections import Counter
            sg = dict(sorted(Counter(len(g) for g in groups.values()).items())); nc = len(hl.vertices)
            res.append({'rings': rings, 'corners': len(V), 'central_A3_section_corners': nc, 'faces': {str(a): b for a, b in sg.items()}})
            print('H4', rings, len(V), len(E), nc, sg, flush=True)
    check('H4 family corner counts 600, 1200, 720, 120, 2400, 3600, 2400, 3600, 3600, 1440, 7200 x 4, 14400',
          [r['corners'] for r in res] == [600, 1200, 720, 120, 2400, 3600, 2400, 3600, 3600, 1440, 7200, 7200, 7200, 7200, 14400])
    cc = [r for r in res if r['central_A3_section_corners'] == 24 and r['faces'] == {'3': 8, '8': 6}]
    check(f'H4 family (15 uniform polytopes, floating point): no central A3 section has 24 corners, so none is a cube cut at the corners',
          not cc and all(r['central_A3_section_corners'] != 24 for r in res))
    OUT['E'] = res


if __name__ == '__main__':
    parts = sys.argv[1:] or ['A', 'B', 'C', 'D', 'E']
    for pt in parts:
        CHECKS.clear(); OUT.clear(); t0 = time.time()
        {'A': partA, 'B': partB, 'C': partC, 'D': partD, 'E': partE}[pt]()
        json.dump({'part': pt, 'result': OUT.get(pt), 'checks': CHECKS, 'seconds': round(time.time() - t0)},
                  open(os.path.join(DATA, f's9-why-not-cubes-{pt}.json'), 'w'), indent=1, default=str)
        print(f'part {pt}: {sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed ({time.time() - t0:.0f}s)', flush=True)
