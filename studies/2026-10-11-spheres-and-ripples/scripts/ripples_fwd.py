# Forward test of DICTO's icosahedral ripples (parallel orientation): all ripple face planes from the 13 centres at
# rho = r_in * phi^k, k in KS; every triple crossing inside the Lotus seed's gap; compared with the 92 piece corners.
import json, sys, math, itertools, numpy as np
from scipy.spatial import ConvexHull
P = json.load(open(sys.argv[1])); PHI = (1 + 5 ** .5) / 2; KS = [int(k) for k in sys.argv[2].split(',')]
icos = [p for p in P if p['role'] == 'ico']
def nrm(p):
    V = np.array(p['vertices']); c = V.mean(0); out = []
    for f in p['faces']:
        a, b, d = V[f[0]], V[f[1]], V[f[2]]; n = np.cross(b - a, d - a); n /= np.linalg.norm(n); out.append(n if n @ (a - c) > 0 else -n)
    return np.array(out), c
N0, _ = nrm(icos[0]); V0 = np.array(icos[0]['vertices']); rin = float(np.mean(N0 @ (V0 - V0.mean(0)).T, axis=1).max())
rin = abs(float(N0[0] @ (V0[icos[0]['faces'][0][0]] - V0.mean(0))))
cen = [np.mean(p['vertices'], 0) for p in icos]
planes = {}
for c in cen:
    for n in N0:
        for k in KS:
            d = n @ c + rin * PHI ** k
            key = tuple(np.round(np.r_[n, d], 7)); key2 = tuple(np.round(np.r_[-n, -d], 7))
            if key2 not in planes: planes[key] = (n, d)
PL = list(planes.values()); A = np.array([p[0] for p in PL]); D = np.array([p[1] for p in PL])
print('distinct ripple planes', len(PL), flush=True)
allV = np.array([v for p in P for v in p['vertices']]); H = ConvexHull(allV); HN = H.equations[:, :3]; HD = -H.equations[:, 3]
solids = [(nrm(p)[0], np.array([nrm(p)[0][i] @ np.array(p['vertices'])[f[0]] for i, f in enumerate(p['faces'])])) for p in icos]
def in_gap(X):
    ok = np.all(X @ HN.T <= HD + 1e-7, axis=1)
    for N, Dd in solids: ok &= np.any(X @ N.T >= Dd - 1e-7, axis=1)
    return ok
pts = set()
n = len(PL)
for i in range(n):
    for j in range(i + 1, n):
        u = np.cross(A[i], A[j])
        if np.linalg.norm(u) < 1e-9: continue
        ks = np.arange(j + 1, n)
        M = np.stack([np.broadcast_to(A[i], (len(ks), 3)), np.broadcast_to(A[j], (len(ks), 3)), A[ks]], 1)
        det = np.linalg.det(M); good = np.abs(det) > 1e-9
        if not good.any(): continue
        rhs = np.stack([np.full(good.sum(), D[i]), np.full(good.sum(), D[j]), D[ks][good]], 1)
        X = np.linalg.solve(M[good], rhs[..., None])[..., 0]
        X = X[in_gap(X)]
        for x in np.round(X, 6): pts.add(tuple(x))
    if i % 50 == 0: print(f'  plane {i}/{n}, points so far {len(pts)}', flush=True)
corners = {tuple(np.round(v, 6)) for p in P if p['role'] != 'ico' for v in p['vertices']}
hit = len(corners & pts)
print(f'crossing points in the gap: {len(pts)}; piece corners among them: {hit} of {len(corners)}; extra points: {len(pts) - hit}')
json.dump({'points': [list(p) for p in pts], 'corners': [list(c) for c in corners]}, open('ripple-points.json', 'w'))
