"""Render of DICTO's Hollow-straw transformation, C116 (own shape) -> Minana #377 (27 Nov 2026). With Claude (Anthropic).
Straw k = the region face k of P(lam) sweeps (c116_transform.py). Built from P(lam) on a grid (dense near the two swap times): between
two grid steps where face k keeps the same corners, the wall is lofted corner to corner; across a swap step, the slab is the hull of
the two face polygons (caps dropped). Drawn edges: only the real ones (the C116 face, the Minana face, and the paths of the corners).
Colours: the Aequi page's, by the Minana face each straw ends on. Panels: C116, halfway (P(1/2)), pulled apart, assembled.
Usage: python render_transform.py scenes | compose"""
import os, sys, json
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
D = os.path.join(ROOT, 'renders/c116transform')
COL = {'C': '#488e48', 'O': '#e8c852', 'T': '#cd3e28', 'D': '#8a5cc4', 'I': '#3a70cd', 'RD': '#b3a489', 'RT': '#8e9aa5'}
SOLID = {'RD': 'rhombic dodecahedron', 'D': 'dodecahedron', 'I': 'icosahedron', 'RT': 'rhombic triacontahedron'}
def mix(a, b, t): return '#' + ''.join('%02x' % round(int(a[1 + 2 * i:3 + 2 * i], 16) * (1 - t) + int(b[1 + 2 * i:3 + 2 * i], 16) * t) for i in range(3))
def colOf(key): base = COL[key.replace('2', '')]; return mix(base, '#ffffff', 0.45) if key.endswith('2') else base
if sys.argv[1] == 'scenes':
    sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, '../2026-11-21-scutoid-stand-in/renders/scripts'))
    src = open(os.path.join(HERE, 'c116_transform.py')).read(); g = {'__file__': os.path.join(HERE, 'c116_transform.py'), '__name__': 'tf'}
    exec(src[:src.index('def pairs_of')], g)
    Ak, Mk, sig, S, A = g['Ak'], g['Mk'], g['sig'], g['S'], g['A']
    from render_cells import DIR, EDGE
    from render_c116 import frame
    from scipy.spatial import HalfspaceIntersection
    import aequus_solid as AS
    Dd = json.load(open(os.path.join(ROOT, 'src/dice.json'))); e = Dd['dice'][376]; ED = AS.C.exact_dirs(Dd['dirs']); lab = {}
    for oi in e['o']:
        gr = Dd['groups'][e['g']][oi]
        for i in gr['dirs']: lab[A.key([AS.Q(c.a, c.b) for c in ED[i][0]])] = gr['col']
    mcol = [lab[A.key(u)] for u, c in S['planes']]
    col = {k: colOf(mcol[sig[k]]) for k in range(60)}
    def solid(lam):
        A_ = (1 - lam) * Ak + lam * Mk
        P = HalfspaceIntersection(np.hstack([A_, -np.ones((60, 1))]), np.zeros(3)).intersections
        sc = np.abs(P).max(); pts = []
        for p in P:
            if not any(np.linalg.norm(p - q) < 1e-9 * sc for q in pts): pts.append(p)
        P = np.array(pts); tight = np.abs(A_ @ P.T - 1) < 1e-8; faces = []
        for k in range(60):
            idx = list(np.where(tight[k])[0]); X = P[idx]; c0 = X.mean(0); n = A_[k] / np.linalg.norm(A_[k]); e1 = X[0] - c0; e2 = np.cross(n, e1)
            order = np.argsort(np.arctan2((X - c0) @ e2, (X - c0) @ e1)); idx = [idx[i] for i in order]
            faces.append([(frozenset(np.where(tight[:, i])[0]), P[i]) for i in idx])
        return faces
    ev = [0.73951, 0.75880]
    grid = sorted(set(np.round(np.concatenate([np.linspace(0, 1, 121)] + [np.linspace(t - 0.004, t + 0.004, 41) for t in ev]), 7)))
    grid = [x for x in grid if 0 <= x <= 1]
    F = [solid(l) for l in grid]
    def part(k, shift):
        V, T, C, tubes = [], [], [], []
        def add(p): V.append(list(p)); return len(V) - 1
        def poly_cap(poly):
            ids = [add(p) for _, p in poly]
            for a in range(1, len(ids) - 1): T.append([ids[0], ids[a], ids[a + 1]]); C.append(col[k])
            for a in range(len(ids)): tubes.append([ids[a], ids[(a + 1) % len(ids)], EDGE, None])
        poly_cap(F[0][k]); poly_cap(F[-1][k])
        for i in range(len(grid) - 1):
            p0, p1 = F[i][k], F[i + 1][k]
            l0, l1 = [lb for lb, _ in p0], [lb for lb, _ in p1]
            if l0 == l1 or (sorted(map(sorted, l0)) == sorted(map(sorted, l1)) and len(l0) == len(l1)):
                m = {lb: j for j, lb in enumerate(l1)}; n = len(l0)
                ia = [add(p) for _, p in p0]; ib = [add(p1[m[lb]][1]) for lb, _ in p0]
                for a in range(n):
                    b = (a + 1) % n; T.append([ia[a], ia[b], ib[b]]); C.append(col[k]); T.append([ia[a], ib[b], ib[a]]); C.append(col[k])
                    tubes.append([ia[a], ib[a], EDGE, None])
            else:   # a swap happens on this face between the two steps: hull of the two polygons, caps dropped
                X = np.array([p for _, p in p0] + [p for _, p in p1]); n0 = len(p0); h = ConvexHull(X); base = len(V)
                for p in X: V.append(list(p))
                for t in h.simplices:
                    if all(i < n0 for i in t) or all(i >= n0 for i in t): continue
                    T.append([base + int(i) for i in t]); C.append(col[k])
        Vn = np.array(V); cen = np.array([p for _, p in F[-1][k]]).mean(0)
        Vn = Vn + shift * cen
        return {'v': np.round(Vn, 6).tolist(), 't': T, 'c': C, 'a': 1.0, 'tubes': tubes, 'rad': 0.0018, 'balls': []}
    def solid_part(faces, cols, rad=0.0024):
        V, T, C, tubes = [], [], [], []
        for k, poly in enumerate(faces):
            ids = []
            for _, p in poly: V.append(list(p)); ids.append(len(V) - 1)
            for a in range(1, len(ids) - 1): T.append([ids[0], ids[a], ids[a + 1]]); C.append(cols[k])
            for a in range(len(ids)): tubes.append([ids[a], ids[(a + 1) % len(ids)], EDGE, None])
        return {'v': np.round(np.array(V), 6).tolist(), 't': T, 'c': C, 'a': 1.0, 'tubes': tubes, 'rad': rad, 'balls': []}
    core = solid_part(F[0], [col[k] for k in range(60)])
    half = solid_part(solid(0.5), [col[k] for k in range(60)])
    straws = lambda sh: [part(k, sh) for k in range(60)]
    from render3d import write
    full = [core] + straws(0.9); E = frame(full)
    scs = [{'E': E, 'dir': DIR, 'parts': [core]}, {'E': E, 'dir': DIR, 'parts': [half]}, {'E': E, 'dir': DIR, 'parts': full},
           {'E': E, 'dir': DIR, 'parts': [core] + straws(0.0)}]
    os.makedirs(D, exist_ok=True); write(os.path.join(D, 'c116transform.html'), scs)
    from collections import Counter
    json.dump(dict(Counter(mcol)), open(os.path.join(D, 'meta.json'), 'w'))
    print('scenes', len(scs), flush=True)
else:
    import types
    src = open(os.path.join(ROOT, '../2026-11-21-scutoid-stand-in/renders/scripts/compose.py')).read()
    Cp = types.ModuleType('compose_defs'); Cp.__dict__['__file__'] = os.path.join(ROOT, 'renders/x')
    exec(src[:src.index('s = lambda')], Cp.__dict__)
    Cp.OUT = os.path.join(ROOT, 'renders'); Cp.MARK = 'DICTO · dictospheres.com'
    meta = json.load(open(os.path.join(D, 'meta.json'))); hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    Cp.figure('RENDER-c116-minana-transform.png', "C116 into Minana #377: DICTO's Hollow-straw transformation",
              'Both ends fixed: C116 in its own shape inside, the die outside; every C116 face moves and turns into its die face, all together. 60 straws, 18 swaps',
              [(os.path.join(D, 'p0.png'), 'start', 'fullerene C116'), (os.path.join(D, 'p1.png'), 'halfway', 'the shape at lam = 1/2'),
               (os.path.join(D, 'p2.png'), 'pulled apart', 'C116 and its 60 straws'), (os.path.join(D, 'p3.png'), 'end', 'Minana #377')],
              [(hexrgb(colOf(k)), f"{SOLID[k.replace('2', '')]} planes ({meta[k]})") for k in ('D', 'I2', 'RD', 'RT2') if k in meta], cell=1000)
    out = os.path.join(ROOT, 'renders/RENDER-c116-minana-transform.png')
    print('FINAL ok' if os.path.exists(out) and os.path.getsize(out) > 100000 else 'FINAL FAIL (no figure)')
