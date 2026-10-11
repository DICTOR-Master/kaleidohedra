# Find Kramer's seven tiles (Mosseri-Sadoc t1..t6 + T2) at base scale 1/tau (edges 1/tau and 1; T2 also tau) as vertex
# sets of the Lotus seed point cloud, so they sit in the Lotus frame's icosahedral orientation. Writes ms-kit.json with
# the Lotus pieces plus one copy of each tile (role = tile name).
import json, sys, itertools, numpy as np
from scipy.spatial import cKDTree
PHI = (1 + 5 ** .5) / 2; s = 1 / PHI
L = json.load(open(sys.argv[1]))
pts = [v for p in L for v in p['vertices']]
if len(sys.argv) > 2: pts += [v for p in json.load(open(sys.argv[2]))['2'] for v in p['v']]   # Chain of Karma step 2
P = np.unique(np.round(np.array(pts), 9), axis=0)
want = {  # sorted edge multisets at scale s
    't1': [s] * 5 + [s * PHI], 't2': [s] * 4 + [s * PHI] * 2, 't3': [s] * 3 + [s * PHI] * 3,
    't4': [s] * 3 + [s * PHI] * 3, 't5': [s] * 2 + [s * PHI] * 4, 't6': [s] + [s * PHI] * 5,
    'T2': [s] + [s * PHI] * 4 + [s * PHI ** 2]}
# t3 and t4 share the edge multiset: t3 has the tau edges in a triangle (base tau), t4 has them at one vertex
def kind(Q):
    d = {(i, j): np.linalg.norm(Q[i] - Q[j]) for i, j in itertools.combinations(range(4), 2)}
    ms = sorted(d.values())
    out = []
    for k, w in want.items():
        if not np.allclose(ms, sorted(w), atol=1e-6): continue
        if k in ('t3', 't4'):
            longs = [e for e, l in d.items() if abs(l - s * PHI) < 1e-5]
            if len(longs) != 3: continue
            star = len(set.intersection(*[set(e) for e in longs])) == 1
            if (k == 't4') != star: continue
        out.append(k)
    return out
tree = cKDTree(P); found = {}
for i, p in enumerate(P):
    nb = [j for j in tree.query_ball_point(p, s * PHI ** 2 + 1e-6) if j > i]
    for a, b, c in itertools.combinations(nb, 3):
        Q = P[[i, a, b, c]]
        vol = abs(np.linalg.det(Q[1:] - Q[0])) / 6
        if vol < 1e-6: continue
        for k in kind(Q):
            found.setdefault(k, Q)
    if len(found) == len(want): break
print('found in Lotus frame:', sorted(found), 'missing:', sorted(set(want) - set(found)))
out = L + [{'role': k, 'vertices': Q.tolist(), 'faces': [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]} for k, Q in found.items()]
json.dump(out, open('ms-kit.json', 'w'))
