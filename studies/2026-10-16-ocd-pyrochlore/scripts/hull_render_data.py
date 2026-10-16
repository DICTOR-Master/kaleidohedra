# Render data for the OCD + 60 GBPC hull (scripts/ocd_gbpc_hull.py): the hull (faces tagged hexagon/triangle), the OCD and the 60 GBPCs,
# each as corners + ordered faces. -> data/hull-render.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
d = json.load(open('data/adapter-render.json')); O = np.array(d['ocd']['v']); Ad = [np.array(a['v']) for a in d['adapters']]
key = lambda V: frozenset(map(tuple, np.round(V, 6)))
ops = []
for perm in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3))
        for i, p in enumerate(perm): M[i, p] = s[i]
        if key(O @ M.T) == key(O): ops.append(M)
G = list({key(a @ M.T): a @ M.T for a in Ad for M in ops}.values())
def solid(P):
    P = np.array(P); h = ConvexHull(P); P = P[h.vertices]; h = ConvexHull(P); E = []; F = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-6) for q in E): continue
        E.append(e); idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-6]; Q = P[idx]; c = Q.mean(0); a = Q[0] - c; b = np.cross(e[:3], a)
        F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return {'v': P.round(8).tolist(), 'f': F}
hull = solid(np.vstack([O] + G))
json.dump({'hull': hull, 'ocd': solid(O), 'gbpc': [solid(g) for g in G]}, open('data/hull-render.json', 'w'))
print('hull faces', len(hull['f']), 'gbpc', len(G))
