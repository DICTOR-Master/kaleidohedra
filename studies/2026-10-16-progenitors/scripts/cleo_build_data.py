# Render data for the Cleo star build (steps 9–10): the 20 Cleo-Icos of the Dharma icosahedron (apex at the centre), the 20 Cleo spikes, the 12
# inward pentagonal pyramids under D' = (2/3)·D, and the stations D', ID, plus the nine-station cycle for the extended cutaway. -> data/cleo-build.json
import json, numpy as np
from scipy.spatial import ConvexHull
d = json.load(open('data/cleo-star.json')); I = np.array(d['I']); Dp = np.array(d['Dp']); ID = np.array(d['ID'])
def faces(P):
    P = np.array(P); h = ConvexHull(P); P = P[h.vertices]; h = ConvexHull(P); pl = []; F = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q in pl): continue
        pl.append(e); idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7]; Q = P[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return {'v': P.round(7).tolist(), 'f': F}
hI = ConvexHull(I); tri = []
for e in hI.equations:
    idx = [i for i in range(12) if abs(I[i] @ e[:3] + e[3]) < 1e-7]
    if sorted(idx) not in [sorted(t) for t in tri]: tri.append(idx)
core = [faces(np.vstack([I[t], [[0, 0, 0]]])) for t in tri]
spikes = [faces(np.vstack([I[t], [2 * I[t].mean(0)]])) for t in tri]
hD = ConvexHull(Dp); pyr = []; seen = []
for e in hD.equations:
    if any(np.allclose(e, q, atol=1e-7) for q in seen): continue
    seen.append(e); base = Dp[[i for i in range(20) if abs(Dp[i] @ e[:3] + e[3]) < 1e-7]]; apex = I[np.argmax(I @ e[:3])]
    pyr.append(faces(np.vstack([base, [apex]])))
nine = json.load(open('data/nine-render.json'))
json.dump({'core': core, 'spikes': spikes, 'pyr': pyr, 'Dp': faces(Dp), 'ID': faces(ID), 'nine': nine['stations'], 'view': nine['view'], 'slice': nine['slice']}, open('data/cleo-build.json', 'w'))
print(len(core), len(spikes), len(pyr))
