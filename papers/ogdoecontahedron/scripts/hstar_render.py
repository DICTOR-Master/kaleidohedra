# The dual of the DICTO Hecatodihedron on its own (render data): 20 regular hexagons and 60 kites, whole faces.
import json, numpy as np
from scipy.spatial import ConvexHull
C = {n: np.array(V) for n, V in json.load(open('data/reversed-chain.json'))}
H = C['dual of the Hecatodihedron']; H = H / np.linalg.norm(H, axis=1).min()     # inner sphere of 90 corners at radius 1
h = ConvexHull(H); pl = []
for e in h.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
F = []
for e in pl:
    idx = [i for i in range(len(H)) if abs(H[i] @ e[:3] + e[3]) < 1e-7]; Q = H[idx]; c = Q.mean(0)
    a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
    F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
assert sorted(len(f) for f in F) == [4] * 60 + [6] * 20
json.dump({'v': H.tolist(), 'f': F}, open('data/hstar-render.json', 'w'))
