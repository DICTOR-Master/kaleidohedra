# Atlas of the five stages between the queens (DICTO 2026-10-30, paper #76): for each stage (built from the 600-cell's corners as in
# the app, queen-stages-geometry.js) and each of the four main directions of #63 (vertex, edge middle, triangle centre, cell centre),
# every slice from the centre to the tip: at each corner height and halfway between neighbouring heights (one pattern per gap, as
# #63's lemma). A slice is the 3D convex polygon/polyhedron where the hyperplane x.d = h meets the solid: its corners are the solid's
# corners at height h and the crossing points of its edges; faces are merged coplanar hull facets. Also the four shadows (hull of the
# projection along d). Checks: Euler V - E + F = 2 for every 3D slice and shadow; the counts at the queens' ends equal #63/#65's.
import numpy as np, itertools, json, sys
from scipy.spatial import ConvexHull, cKDTree
exec(open(__file__.replace('atlas.py', 'stages.py')).read().split('keys = ')[0])   # V (120), D, e0, phi
adj = {i: set(j for j in range(120) if abs(D[i, j] - e0) < 1e-9) for i in range(120)}
E = [(i, j) for i in range(120) for j in adj[i] if j > i]
T = [(i, j, k) for i, j in E for k in adj[i] & adj[j] if k > j]
C = [(i, j, k, l) for i, j, k in T for l in adj[i] & adj[j] & adj[k] if l > k]
face = {}
for ci, c in enumerate(C):
    for f in itertools.combinations(c, 3): face.setdefault(f, []).append(ci)
P2 = list(face.values()); cen = lambda q: V[list(q)].mean(0); CEN = np.array([cen(c) for c in C])
mix = lambda p, q, s: (1 - s) * p + s * q
BUILD = {'600-cell': lambda: V.copy(),
         'truncated 600-cell': lambda: np.array([mix(V[a], V[b], 1 / 3) for x, y in E for a, b in ((x, y), (y, x))]),
         'rectified 600-cell': lambda: np.array([(V[a] + V[b]) / 2 for a, b in E]),
         'bitruncated': lambda: np.array([mix((V[a] + V[b]) / 2, cen(t), 3 / 5) for t in T for a, b in itertools.combinations(t, 2)]),
         'rectified 120-cell': lambda: np.array([cen(t) for t in T]),
         'truncated 120-cell': lambda: np.array([mix(CEN[a], CEN[b], (5 - 5 ** .5) / 10) for x, y in P2 for a, b in ((x, y), (y, x))]),
         '120-cell': lambda: CEN.copy()}
c0 = C[0]; t0 = c0[:3]
DIRS = {'vertex-first': V[c0[0]], 'edge-first': (V[c0[0]] + V[c0[1]]) / 2, 'face-first': cen(t0), 'cell-first': cen(c0)}
def edges_of(X):
    d, _ = cKDTree(X).query(X, 2); m = d[:, 1].min()
    pairs = cKDTree(X).query_pairs(m * (1 + 1e-7)); return np.array(sorted(pairs)), m
def frame(u):
    u = u / np.linalg.norm(u); Q, _ = np.linalg.qr(np.column_stack([u, np.eye(4)[:, :3]]))
    return Q[:, 1:4] if abs(abs(Q[:, 0] @ u) - 1) < 1e-9 else None
def poly3(Y, tol=1e-7):
    Y = np.unique(np.round(Y, 9), axis=0)
    if len(Y) < 4: return {'dim': len(Y) - 1 if len(Y) else -1, 'V': len(Y)}
    r = np.linalg.matrix_rank(Y[1:] - Y[0], tol=1e-7)
    if r < 3: return {'dim': int(r), 'V': len(Y)}
    h = ConvexHull(Y); planes = {}
    for k, s in enumerate(h.simplices):
        n = h.equations[k]; key = None
        for kk in planes:
            if np.allclose(kk, n, atol=1e-6): key = kk; break
        planes.setdefault(key if key is not None else tuple(n), set()).update(s)
    # each face's true corners: the 2D hull of its points in its plane (points in the middle of an edge are not corners)
    used = set(); sizes = {}
    for n, vs in planes.items():
        vs = sorted(vs); Z = Y[vs]; c = Z.mean(0); nn = np.array(n[:3]); a = Z[0] - c; a -= (a @ nn) * nn; a /= np.linalg.norm(a); b = np.cross(nn, a)
        W = np.column_stack([(Z - c) @ a, (Z - c) @ b]); k2 = list(ConvexHull(W).vertices)   # counter-clockwise
        cr2 = lambda p, q: p[0] * q[1] - p[1] * q[0]
        # drop corners where the boundary runs straight on (a point on an edge, kept by rounding)
        k2 = [k for i, k in enumerate(k2) if abs(cr2(W[k] - W[k2[i - 1]], W[k2[(i + 1) % len(k2)]] - W[k])) > 1e-7 * np.linalg.norm(W[k] - W[k2[i - 1]]) * np.linalg.norm(W[k2[(i + 1) % len(k2)]] - W[k])]
        used.update(vs[i] for i in k2)
        sizes[len(k2)] = sizes.get(len(k2), 0) + 1
    Vn = len(used); F = len(planes); Ed = sum(k * n for k, n in sizes.items()) // 2
    assert Vn - Ed + F == 2, ('euler', Vn, Ed, F)
    return {'dim': 3, 'V': Vn, 'E': Ed, 'F': F, 'faces': {str(k): n for k, n in sorted(sizes.items())}}
out = {}
for name, f in BUILD.items():
    X = f(); X = X / np.linalg.norm(X[0]); Ed, m = edges_of(X); out[name] = {'V': len(X), 'E': len(Ed), 'directions': {}}
    for dn, d in DIRS.items():
        u = d / np.linalg.norm(d); B = frame(u); hgt = X @ u
        hs = np.unique(np.round(hgt[hgt > -1e-9], 9)); stops = sorted(set(list(hs) + [(a + b) / 2 for a, b in zip(hs[:-1], hs[1:])]))
        sl = []
        for h in stops:
            pts = list(X[np.abs(hgt - h) < 1e-9])
            a, b = hgt[Ed[:, 0]] - h, hgt[Ed[:, 1]] - h; cr = (a * b < 0) & (np.abs(a) > 1e-9) & (np.abs(b) > 1e-9)
            for (i, j), x, y in zip(Ed[cr], a[cr], b[cr]): pts.append(X[i] + (X[j] - X[i]) * (x / (x - y)))
            try: r = poly3(np.array(pts) @ B)
            except AssertionError as ex: r = {'dim': 'FAIL', 'why': str(ex)}; print('FAIL', name, dn, round(float(h), 9), ex, flush=True)
            r['h'] = round(float(h), 9); r['atVertex'] = bool(np.isclose(hs, h).any()); sl.append(r)
        pat = {json.dumps({k: v for k, v in r.items() if k not in ('h', 'atVertex')}, sort_keys=True) for r in sl}
        try: sh = poly3(X @ B)
        except AssertionError as ex: sh = {'dim': 'FAIL', 'why': str(ex)}; print('FAIL shadow', name, dn, ex, flush=True)
        out[name]['directions'][dn] = {'stops': len(sl), 'patterns': len(pat), 'shadow': sh, 'slices': sl}
        print(name, dn, 'stops', len(sl), 'patterns', len(pat), 'shadow', sh.get('V'), sh.get('F'), flush=True)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'atlas.json', 'w'))
