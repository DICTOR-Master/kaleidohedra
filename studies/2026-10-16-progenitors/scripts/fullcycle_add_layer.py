# DICTO 2026-10-17 (the cover: "draw the 60 pieces"): the outer layer M -> I·φ³ of the twelve-station figure, its 60 pieces of one kind
# (data/gap-pieces.json, from gap_member.py's cone cut; exact volumes in gap-pieces-exact.txt), added to data/full-cycle.json as
# st.L60, each piece with its faces merged by plane, for render_full.html (&layer=1).
import json, numpy as np
from scipy.spatial import ConvexHull
d = json.load(open('data/gap-pieces.json')); J = json.load(open('data/full-cycle.json'))
IP = np.array(J['st']['Ip3']['v']); assert abs(max(np.linalg.norm(np.array(v)) for pc in d['G -> icosahedron'] for v in pc) - np.linalg.norm(IP, axis=1).max()) < 1e-6
def faces(V):
    h = ConvexHull(V); out, seen = [], []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q in seen): continue
        seen.append(e); idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-6]
        c = V[idx].mean(0); u = V[idx[0]] - c; w = np.cross(e[:3], u)
        idx.sort(key=lambda i: np.arctan2((V[i] - c) @ w, (V[i] - c) @ u)); out.append(idx)
    return out
L = []
for pc in d['G -> icosahedron']:
    V = np.array(pc); L.append({'v': np.round(V, 7).tolist(), 'f': faces(V)})
J['st']['L60'] = L; json.dump(J, open('data/full-cycle.json', 'w')); print(len(L), 'pieces,', sorted({len(p['f']) for p in L}), 'faces each')
