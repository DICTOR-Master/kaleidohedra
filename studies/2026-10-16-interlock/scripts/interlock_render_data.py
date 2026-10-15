# Render data for the interlock: whole faces per piece (merged by plane), the layer tags, the chain's axes for oriented views.
import json, sys, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, '../_lib'); import geomcheck as gc
J = json.load(open('data/interlock-ends.json')); C = {n: np.array(V) for n, V in json.load(open('data/orig-chain.json'))}
ax = gc.icosa_axes(C['icosahedron'])
def faces(V):
    V = np.array(V); h = ConvexHull(V); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    F = []
    for e in pl:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]; Q = V[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return F
P = [{'v': [[round(x, 6) for x in v] for v in q['v']], 'f': faces(q['v']), 'o': q['o'][0], 'g': q['f'][0] * 10 + q['f'][1]} for q in J['pieces']]
def up_for(a):   # a two-fold axis perpendicular to the view axis: the picture's up, so every view is left-right symmetric
    return next(u for u in ax['2'] if abs(u @ a) < 1e-9).tolist()
views = {k: {'axis': ax[k][0].tolist(), 'up': up_for(ax[k][0])} for k in '532'}
radii = {n: float(np.linalg.norm(C[n], axis=1).max()) for n in C}
json.dump({'pieces': P, 'views': views, 'radii': radii, 'orig_layers': J['orig_layers'], 'flip_layers': J['flip_layers']}, open('data/interlock-render.json', 'w'))
print(len(P), 'pieces;', {k: round(float(np.dot(v['axis'], v['up'])), 9) for k, v in views.items()})
