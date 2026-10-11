# DICTO's infinite Lotus expansion: build(n) fills phi^(2n) x I0 exactly; every icosahedron of the Lotus seed is replaced
# by build(n-1), the gap pieces (AXE, FUJI, CLEO) stay whole at their own size.
import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
L = json.load(open(sys.argv[1])); NMAX = int(sys.argv[2])
allV = np.array([v for p in L for v in p['vertices']]); O = allV.mean(0)
for p in L: p['vertices'] = (np.array(p['vertices']) - O).tolist()
allV = allV - O
d = np.linalg.norm(allV, axis=1); I0 = np.unique(np.round(allV[d > d.max() - 1e-6], 9), axis=0) / PHI ** 2
assert len(I0) == 12
I0f = ConvexHull(I0).simplices.tolist()
def vol(V, F):
    V = np.array(V); c = V.mean(0)
    return sum(abs(np.dot(V[f[0]] - c, np.cross(V[f[1]] - c, V[f[2]] - c))) / 6 for f in F) if all(len(f) == 3 for f in F) else \
        sum(abs(np.dot(V[f[0]] - c, np.cross(V[f[i]] - c, V[f[i + 1]] - c))) / 6 for f in F for i in range(1, len(f) - 1))
def similarity(V):                       # x -> c + e R x, sending I0 onto the icosahedron with vertices V
    V = np.array(V); c = V.mean(0); e = np.linalg.norm(V[0] - V[np.argsort(np.linalg.norm(V - V[0], axis=1))[1]])
    W = (V - c) / e
    a = 0; nb = [j for j in range(12) if abs(np.linalg.norm(I0[j] - I0[a]) - 1) < 1e-6]; b = nb[0]
    c3 = [j for j in nb if abs(np.linalg.norm(I0[j] - I0[b]) - 1) < 1e-6][0]
    A = np.array([I0[a], I0[b], I0[c3]]).T
    for i, j, k in itertools.permutations(range(12), 3):
        B = np.array([W[i], W[j], W[k]]).T
        if abs(np.linalg.norm(W[i] - W[j]) - 1) > 1e-6 or abs(np.linalg.norm(W[j] - W[k]) - 1) > 1e-6 or abs(np.linalg.norm(W[i] - W[k]) - 1) > 1e-6: continue
        R = B @ np.linalg.inv(A)
        if abs(np.linalg.det(R) - 1) > 1e-6: continue
        Y = I0 @ R.T
        if all(np.min(np.linalg.norm(W - y, axis=1)) < 1e-6 for y in Y): return c, e, R
    raise ValueError('no rotation')
icoMaps = [similarity(p['vertices']) for p in L if p['role'] == 'ico']
gaps = [p for p in L if p['role'] != 'ico']
print('icosahedra in the Lotus seed:', len(icoMaps), ' edges:', sorted(round(e, 4) for _, e, _ in icoMaps)[:2], '...',
      ' turned relative to the hull:', sum(not np.allclose(R, np.eye(3)) for _, _, R in icoMaps))
def build(n):
    if n == 0: return [{'role': 'ico', 'vertices': I0.tolist(), 'faces': I0f, 'path': []}]
    lam = PHI ** (2 * (n - 1)); sub = build(n - 1); out = []
    for k, (c, e, R) in enumerate(icoMaps):
        for p in sub:
            out.append({'role': p['role'], 'vertices': (lam * c + e * (np.array(p['vertices']) @ R.T)).tolist(), 'faces': p['faces'], 'path': [k] + p['path']})
    for p in gaps:
        out.append({'role': p['role'], 'vertices': (lam * np.array(p['vertices'])).tolist(), 'faces': p['faces'], 'path': []})
    return out
v0 = vol(I0, I0f); res = {}
for n in range(1, NMAX + 1):
    B = build(n); tot = sum(vol(p['vertices'], p['faces']) for p in B)
    roles = {}
    for p in B: roles[p['role']] = roles.get(p['role'], 0) + 1
    print(f'step {n}: {len(B)} pieces {roles}; volume / (phi^{6*n} I0) = {tot / (v0 * PHI ** (6 * n)):.12f}; icosahedra share {sum(vol(p["vertices"], p["faces"]) for p in B if p["role"] == "ico") / tot:.4f}')
    res[n] = [{'r': p['role'], 'v': np.round(p['vertices'], 5).tolist(), 'f': p['faces'], 'g': p['path'][:1]} for p in B]
json.dump(res, open(sys.argv[3], 'w'), separators=(',', ':'))
