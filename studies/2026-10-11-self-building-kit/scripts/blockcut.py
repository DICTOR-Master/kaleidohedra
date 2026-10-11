# DICTO's block idea: in the Chain of Karma (step 2, 1,569 pieces), find copies of phi^up x (CLEO, AXE, FUJI, I) whose
# boundary runs along existing faces: every block piece wholly inside or wholly outside. The inside pieces are then a
# division of the enlarged piece into kit pieces.
import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull, cKDTree
PHI = (1 + 5 ** .5) / 2
L = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2]))['2']
allV = np.array([v for p in L for v in p['vertices']]); O = allV.mean(0)
for p in L: p['V'] = np.array(p['vertices']) - O
d = np.linalg.norm(allV - O, axis=1); I0 = np.unique(np.round((allV - O)[d > d.max() - 1e-6], 9), axis=0)
e = np.min([np.linalg.norm(I0[0] - I0[m]) for m in range(1, 12)])
nb = [m for m in range(12) if abs(np.linalg.norm(I0[m] - I0[0]) - e) < 1e-6]; b = nb[0]
c = [m for m in nb if abs(np.linalg.norm(I0[m] - I0[b]) - e) < 1e-6][0]; Ai = np.linalg.inv(np.array([I0[0], I0[b], I0[c]]).T)
G = []
for i, j, k in itertools.permutations(range(12), 3):
    R = np.array([I0[i], I0[j], I0[k]]).T @ Ai
    if np.allclose(R @ R.T, np.eye(3), atol=1e-6) and all(np.min(np.linalg.norm(I0 - y, axis=1)) < 1e-6 for y in I0 @ R.T): G.append(R)
assert len(G) == 120
# block pieces padded
n = len(B); mv = max(len(p['v']) for p in B)
PV = np.full((n, mv, 3), np.nan); 
for i, p in enumerate(B): PV[i, :len(p['v'])] = p['v']; PV[i, len(p['v']):] = p['v'][0]
PC = np.nanmean(PV, 1); PR = np.max(np.linalg.norm(PV - PC[:, None], axis=2), 1)
def pvol(p):
    H = ConvexHull(np.array(p['v'])); return H.volume
VOL = np.array([pvol(p) for p in B]); tree = cKDTree(PC)
pts = np.unique(np.round(PV.reshape(-1, 3), 5), axis=0)
pts = pts[np.linalg.norm(pts, axis=1) < float(sys.argv[3])]
print('block pieces', n, 'anchor points', len(pts), flush=True)
def rep(role):
    return next(p for p in L if p['role'] == role and (role != 'ico' or np.min([np.linalg.norm(p['V'][0] - q) for q in p['V'][1:]]) > 0.9))
found = {}
for role in ('cleo', 'axe', 'fuji', 'ico'):
    V0 = rep(role)['V']; V0 = V0 - V0.mean(0)
    for up in (1, 2, 3):
        shapes, seen = [], set()
        for R in G:
            V = PHI ** up * V0 @ R.T; key = tuple(sorted(tuple(np.round(v, 4)) for v in V))
            if key not in seen: seen.add(key); shapes.append(V)
        H = ConvexHull(V0 * PHI ** up); tvol = H.volume; rad = np.max(np.linalg.norm(V0, axis=1)) * PHI ** up
        hits = []
        for V in shapes:
            E = ConvexHull(V).equations
            for p in pts:
                for j in range(len(V)):
                    W = V + (p - V[j]); cen = W.mean(0); E2 = E.copy(); E2[:, 3] = -np.sum(E[:, :3] * W[ConvexHull(V).vertices[0]], 1) if False else E[:, 3] - E[:, :3] @ (p - V[j])
                    near = tree.query_ball_point(cen, rad + PR.max())
                    if not near: continue
                    s = np.einsum('nvk,fk->nvf', PV[near], E2[:, :3]) + E2[:, 3]       # (pieces, verts, faces)
                    inn = np.all(s <= 1e-4, axis=(1, 2))
                    out = np.any(np.all(s >= -1e-4, axis=1), axis=1)
                    if np.all(inn | out) and inn.sum() > 1:
                        v = VOL[np.array(near)[inn]].sum()
                        if abs(v - tvol) < 1e-4 * tvol:
                            ids = tuple(sorted(np.array(near)[inn])); hits.append(ids)
        uniq = set(hits)
        if uniq:
            ex = sorted(uniq, key=len)[0]
            from collections import Counter
            cnt = Counter((B[i]['r'], round(float(np.cbrt(VOL[i])), 3)) for i in ex)
            print(f'phi^{up} x {role}: {len(uniq)} clean cuts found; e.g. {len(ex)} pieces {dict(cnt)}', flush=True)
            found[f'{role}-{up}'] = [{'r': B[i]['r'], 'v': B[i]['v'], 'f': B[i]['f']} for i in ex]
        else:
            print(f'phi^{up} x {role}: no clean cut in the block', flush=True)
json.dump(found, open('blockcut.json', 'w'))
