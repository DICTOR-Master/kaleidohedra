# Render data for the nine-station golden cycle I ⊂ ID ⊂ O ⊂ rTI ⊂ TI ⊂ H ⊂ hull ⊂ RT ⊂ I·φ³ (float corners of the exact stations of
# core_hull_in_cycle.py), whole faces merged by plane, plus the next turn in (scaled φ⁻³) for the rings. -> data/nine-render.json
import json, numpy as np
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
from scipy.spatial import ConvexHull
def faces(P):
    P = np.array(P); h = ConvexHull(P); P = P[h.vertices]; h = ConvexHull(P); pl = []; F = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q in pl): continue
        pl.append(e); idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7]; Q = P[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return {'v': P.round(7).tolist(), 'f': F}
st9 = [C[0], C[1], C[2], ('rTI', core), C[3], C[4], ('hull', hull), C[5], C[6]]
view = json.load(open('../2026-10-16-interlock/data/p4-render-ends.json'))['views']['B']
sl = json.load(open('../2026-10-16-interlock/data/p4-render-ends.json'))['slice']
json.dump({'stations': [{'name': n, **faces([[x.f() for x in v] for v in V])} for n, V in st9], 'view': view, 'slice': sl}, open('data/nine-render.json', 'w'))
print([ (n, len(V)) for n, V in st9])
