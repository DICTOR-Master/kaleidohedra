# Render data for the O–H compound figures: H, O (polar of H in the TI midsphere, rho = 3/2), the common core (rectified TI) and the hull
# (its dual), each as whole faces (merged by plane) with a face-type tag, plus the view bearing B of the P4 figures. -> data/oh-render.json
import json, numpy as np
from scipy.spatial import ConvexHull
d = json.load(open('data/oh-compound.json'))
def faces(P):
    P = np.array(P); h = ConvexHull(P); P = P[h.vertices]; h = ConvexHull(P); pl = []; F = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q in pl): continue
        pl.append(e); idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7]; Q = P[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    def tag(f):
        Q = P[f]; s = np.round(np.linalg.norm(Q - np.roll(Q, 1, axis=0), axis=1), 4)
        return f'{len(f)}' + ('r' if len(f) == 4 and len(set(s)) == 1 else '')
    return {'v': P.round(7).tolist(), 'f': F, 't': [tag(f) for f in F]}
hull = np.vstack([d['H'], d['O']])
view = json.load(open('../2026-10-16-interlock/data/p4-render-ends.json'))['views']['B']
json.dump({'H': faces(d['H']), 'O': faces(d['O']), 'core': faces(d['core']), 'hull': faces(hull), 'view': view}, open('data/oh-render.json', 'w'))
print({k: (len(v['v']), len(v['f']), sorted(set(v['t']))) for k, v in json.load(open('data/oh-render.json')).items() if k != 'view'})
