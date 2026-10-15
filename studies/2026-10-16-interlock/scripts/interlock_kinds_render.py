# Render data for the interlock kind galleries (one piece of each kind, cleaned float corners; faces as ordered loops).
# -> data/interlock-kinds-render-<setting>.json in the render_pieces.html format ({layers: [{name, pieces: [{v, f}]}]}).
import json, re, collections
import numpy as np
from scipy.spatial import ConvexHull
COLS = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
for setting in ('ends', 'middle'):
    d = json.load(open(f'data/interlock-{setting}.json'))
    groups = collections.defaultdict(list)
    for p in d['pieces']: groups[round(p['vol'], 7)].append(p)
    layers = []
    for vol in sorted(groups, reverse=True):
        ps = groups[vol]; P = np.array(ps[0]['v']); U = []
        for x in P:
            if all(np.linalg.norm(x - y) > 1e-6 for y in U): U.append(x)
        P = np.array(U); H = ConvexHull(P)
        keep = [i for i in range(len(P)) if np.linalg.matrix_rank(np.array([e[:3] for e in H.equations if abs(P[i] @ e[:3] + e[3]) < 1e-7]), tol=1e-6) == 3]
        P = P[keep]; H = ConvexHull(P); faces = []
        for e in H.equations:
            on = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7]
            if sorted(on) in [sorted(f) for f in faces]: continue
            c = P[on].mean(0); u = P[on[0]] - c; u /= np.linalg.norm(u); w = np.cross(e[:3], u)
            faces.append([on[i] for i in np.argsort([np.arctan2((P[j] - c) @ w, (P[j] - c) @ u) for j in on])])
        layers.append({'name': f'{len(ps)} x {vol:.6f}', 'olayer': ps[0]['o'][0], 'pieces': [{'v': P.tolist(), 'f': faces}]})
    json.dump({'layers': layers}, open(f'data/interlock-kinds-render-{setting}.json', 'w'))
    print(setting, len(layers))
