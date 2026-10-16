# Render data for the pyrochlore two-solid crystal: the stella cut and the icosahedron (of the OCD's hexagon planes) as solids with faces,
# and the sites of both networks within radius 2.6 (network.json frame). -> data/crystal-render.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
N = json.load(open('data/network.json')); T = np.array(N['T']); Lb = np.array(N['Lb']).T
S = np.array(json.load(open('data/stella-cut-exact.json'))['S']['v'])
r = np.linalg.norm(S, axis=1); U = S[r > r.max() - 1e-6]; U /= np.linalg.norm(U, axis=1)[:, None]
d_hex = 0.6227818927704104   # the OCD hexagon-plane distance (exact: √(2/9 + 2√5/27))
I = U * d_hex / 0.7946544722917661   # icosahedron with inradius d_hex (inradius / circumradius = 0.79465)
def solid(P):
    P = np.array(P); h = ConvexHull(P); E = []; F = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-6) for q in E): continue
        E.append(e); idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-6]; Q = P[idx]; c = Q.mean(0); a = Q[0] - c; b = np.cross(e[:3], a)
        F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return {'v': P.round(7).tolist(), 'f': F}
A = [Lb @ np.array(m, float) for m in itertools.product(range(-3, 4), repeat=3)]
n1 = [a for a in A] + [a + T[0] for a in A]; n2 = [a + 2 * T[0] for a in A] + [a + 3 * T[0] for a in A]
c0 = (np.zeros(3) + T[0]) / 2   # centre the patch on a joint between two network-1 copies
R = 2.6
json.dump({'stella': solid(S), 'ico': solid(I), 'net1': [list(p - c0) for p in n1 if np.linalg.norm(p - c0) < R],
           'net2': [list(p - c0) for p in n2 if np.linalg.norm(p - c0) < R], 'axis': list(T[0] / np.linalg.norm(T[0]))}, open('data/crystal-render.json', 'w'))
print('stella', len(S), 'ico edge', round(min(np.linalg.norm(I[0] - I[j]) for j in range(1, 12)), 5), 'sites', sum(np.linalg.norm(p - c0) < R for p in n1), sum(np.linalg.norm(p - c0) < R for p in n2))
