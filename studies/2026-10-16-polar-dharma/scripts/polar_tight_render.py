# Render data for the tightened nest (step 4): same layout as polar-render.json, whole faces merged by plane.
import json, numpy as np
from scipy.spatial import ConvexHull
CL = json.load(open('data/reversed-chain-tight.json')); PC = json.load(open('data/polar-tight-pieces.json'))
def solid(V):
    V = np.array(V); h = ConvexHull(V); F = []
    for e in h.equations:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(f) for f in F): continue
        Q = V[idx]; c = Q.mean(0); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return {'v': V.tolist(), 'f': F, 'c': V.mean(0).tolist()}
R = {'layers': [{'name': k, 'pieces': [solid(V) for V in L]} for k, L in PC.items()], 'core': solid(CL[0][1]), 'outer': solid(CL[-1][1])}
json.dump(R, open('data/polar-tight-render.json', 'w'))
