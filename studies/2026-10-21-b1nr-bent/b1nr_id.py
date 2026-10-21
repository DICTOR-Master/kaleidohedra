# DICTO 2026-10-21: B1NRs with icosidodecahedra, as in his real builds: every B1NR pentagon is SHARED with an icosidodecahedron (ID,
# edge 1, made of 20 ring triangles); they "group all around the B1NRs filling each others pentagons, not full space but rhythmic
# packing". DICTO: "just do float fit for now". The ID's pentagons are regular, the straightened B1NR's are not, so the B1NR is
# refitted (least squares) with every edge near 1 AND every pentagon near regular (diagonals near phi); each ID is then set on a
# B1NR pentagon by the best rigid fit of its own pentagon. Reports: the fit, the misfit at each shared pentagon, ID clashes.
import os, json, itertools, numpy as np
from scipy.optimize import least_squares
from scipy.spatial import ConvexHull, Delaunay
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'b1nr_flat.py')).read(); exec(src[:src.index('def mvc')])
phi = (1 + 5 ** .5) / 2; X0 = np.load(os.path.join(HERE, 'b1nr-flat.npy'))
pents = [f for k, f in faces if k == 'pent']; diag = [(f[i], f[(i + 2) % 5]) for f in pents for i in range(5)]
L = lambda X, pr: np.array([np.linalg.norm(X[a] - X[b]) for a, b in pr])
res = lambda x: np.concatenate([L(x.reshape(-1, 3), edges) - 1, L(x.reshape(-1, 3), diag) - phi])
B = least_squares(res, X0.ravel(), xtol=1e-13, ftol=1e-13).x.reshape(-1, 3); B -= B.mean(0)
print(f'B1NR refit: edges {L(B, edges).min():.4f}..{L(B, edges).max():.4f}, pentagon diagonals {L(B, diag).min():.4f}..{L(B, diag).max():.4f} (phi {phi:.4f})')
# icosidodecahedron, edge 1
I = [p for p in itertools.product(*[(0,)] * 2 + [(-phi, phi)])]
I = [np.roll(v, k) for v in [np.array(p, float) for p in I] for k in range(3)]
I += [np.roll(np.array([a * .5, b * phi / 2, c * phi * phi / 2]), k) for a, b, c in itertools.product((1, -1), repeat=3) for k in range(3)]
I = np.unique(np.round(np.array(I), 9), axis=0); assert len(I) == 30
IH = ConvexHull(I); IF = []                                 # ID faces from the hull (merge coplanar)
for ids in sorted({tuple(i for i in range(30) if abs(I[i] @ eq[:3] + eq[3]) < 1e-6) for eq in IH.equations}):
    ids = list(ids); n = np.cross(I[ids[1]] - I[ids[0]], I[ids[2]] - I[ids[0]]); n /= np.linalg.norm(n); c = I[ids].mean(0)
    u = np.cross(n, [.3, .5, .8]); u /= np.linalg.norm(u); w = np.cross(n, u)
    IF.append([ids[k] for k in np.argsort([np.arctan2((I[i] - c) @ w, (I[i] - c) @ u) for i in ids])])
IP = next(f for f in IF if len(f) == 5); assert sum(len(f) == 5 for f in IF) == 12 and len(IF) == 32
def kabsch(P, Q):                                            # rotation+translation taking P onto Q (proper or improper; the ID is mirror-symmetric)
    pc, qc = P.mean(0), Q.mean(0); U, s, Wt = np.linalg.svd((P - pc).T @ (Q - qc)); R = (U @ Wt).T
    return R, qc - pc @ R.T
IDs, mis = [], []
for f in pents:
    Q = B[f]; out = Q.mean(0)
    best = None
    for rot in range(5):
        for rev in (1, -1):
            order = [IP[(rot + rev * k) % 5] for k in range(5)]; R, t = kabsch(I[order], Q); W = I @ R.T + t
            if (W.mean(0) - out) @ out <= 0: continue          # the ID must sit outside the B1NR
            e = np.sqrt(((I[order] @ R.T + t - Q) ** 2).sum(1).mean())
            if best is None or e < best[0]: best = (e, W)
    mis.append(best[0]); IDs.append(best[1])
print(f'shared pentagons: misfit rms {min(mis):.4f}..{max(mis):.4f} (edge 1)')
def clash(A, Bp):                                            # rough overlap: share of B's corners and sample points inside A's hull
    D = Delaunay(A); rng = np.random.default_rng(0); S = Bp[rng.integers(0, len(Bp), (4000, 4))]; w = rng.dirichlet(np.ones(4), 4000)
    S = (S * w[:, :, None]).sum(1); return (D.find_simplex(S) >= 0).mean()
cl = [round(clash(IDs[i], IDs[j]), 3) for i, j in itertools.combinations(range(6), 2)]
cb = [round(clash(B, W), 3) for W in IDs]
print('ID-ID overlap (share of sample points):', sorted(set(cl))[-4:], '| B1NR-ID overlap:', sorted(set(cb))[-3:])
cen = [W.mean(0) for W in IDs]; dd = sorted(round(float(np.linalg.norm(cen[i] - cen[j])), 4) for i, j in itertools.combinations(range(6), 2))
print('ID centre distances', dd, '| ID face-to-face distance (pentagons 2x', round(float(abs(np.linalg.norm(I[IP].mean(0)))), 4), ', triangles 2x', round(float(np.linalg.norm(I[next(f for f in IF if len(f) == 3)].mean(0))), 4), ')')
np.save(os.path.join(HERE, 'b1nr-regpent.npy'), B)
GOLD, PURPLE, LILAC, TEAL, DTEAL = '#d9a441', '#6b3fa0', '#9a78c8', '#4f9e96', '#2f6f69'
def mesh(W, F, col, shift=0):
    v, t, c = [], [], []
    for f in F:
        o = len(v); v += (W[f] + shift).tolist(); t += [[o, o + a, o + a + 1] for a in range(1, len(f) - 1)]; c += [col(f)] * (len(f) - 2)
    E = sorted({tuple(sorted((f[a], f[(a + 1) % len(f)]))) for f in F for a in range(len(f))}); o = len(v); v += (W + shift).tolist()
    return {'v': np.round(v, 5).tolist(), 't': t, 'c': c, 'e': [[o + a, o + b] for a, b in E], 'a': 1.0}
kindof = {tuple(f): k for k, f in faces}
bpart = lambda s=0: mesh(B, [f for _, f in faces], lambda f: {'tri': GOLD, 'sq': LILAC, 'pent': PURPLE}[kindof[tuple(f)]], s)
ipart = lambda W, s=0: mesh(W, IF, lambda f: TEAL if len(f) == 3 else DTEAL, s)
scenes = [{'title': 'B1NR, pentagons made regular', 'sub': 'float fit: edges and pentagons within about 1%', 'parts': [bpart()]},
          {'title': 'Six icosidodecahedra', 'sub': 'one on each B1NR pentagon, shared', 'parts': [bpart()] + [ipart(W) for W in IDs]},
          {'title': 'Drawn apart', 'sub': 'each icosidodecahedron moved out from its pentagon', 'parts': [bpart()] + [ipart(W, .45 * W.mean(0) / np.linalg.norm(W.mean(0))) for W in IDs]}]
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.75, 0.35, 0.55); const _unused = new THREE.Vector3(')
open(os.path.join(HERE, 'renders', 'b1nr-id.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'b1nr-id-labels.json'), 'w'), indent=1)
print('b1nr-id.html', len(scenes))
