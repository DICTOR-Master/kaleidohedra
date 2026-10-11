# How many ripple planes (and from how many centres) pass through each crossing point: corners vs extra points.
import json, sys, numpy as np, collections
PHI = (1 + 5 ** .5) / 2
P = json.load(open('lotus-pieces.json')); R = json.load(open('ripple-points.json'))
icos = [p for p in P if p['role'] == 'ico']
V0 = np.array(icos[0]['vertices']); c0 = V0.mean(0); f0 = icos[0]['faces']
N0 = []
for f in f0:
    a, b, d = V0[f[0]], V0[f[1]], V0[f[2]]; n = np.cross(b - a, d - a); n /= np.linalg.norm(n); N0.append(n if n @ (a - c0) > 0 else -n)
N0 = np.array(N0); rin = abs(N0[0] @ (V0[f0[0][0]] - c0))
cen = np.array([np.mean(p['vertices'], 0) for p in icos]); KS = [-3, -2, 0, 1]
X = np.array(R['points']); C = {tuple(c) for c in R['corners']}
isc = np.array([tuple(x) in C for x in X])
mult = np.zeros(len(X), int); ncen = np.zeros(len(X), int)
for c in cen:
    vals = (X - c) @ N0.T                                   # (points, 20)
    on = np.zeros(len(X), int)
    for k in KS: on += np.sum(np.abs(vals - rin * PHI ** k) < 1e-6, axis=1)
    mult += on; ncen += on > 0
for name, sel in (('corners', isc), ('extra points', ~isc)):
    print(name, 'planes through each point:', dict(sorted(collections.Counter(mult[sel]).items())))
    print(name, 'centres whose ripples pass through it:', dict(sorted(collections.Counter(ncen[sel]).items())))
for m in range(3, 13):
    sel = mult >= m
    print(f'  points with >= {m} planes: {sel.sum():6d}, of which corners {int((sel & isc).sum())}')
