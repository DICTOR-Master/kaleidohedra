# Polar Dharma step 4 (2026-10-16): the reversed chain keeps the original cycle's closure (outer dodecahedron = inner one x phi^3),
# which leaves two loose ends: the inner dodecahedron floats inside the icosidodecahedron and the triacontahedron floats inside
# the outer dodecahedron. Here both ends are tightened: the inner dodecahedron grows until it touches the icosidodecahedron, the
# outer one shrinks until it touches the triacontahedron. The four middle stations already touch and stay as they are.
import json, numpy as np
from scipy.spatial import ConvexHull
CL = json.load(open('data/reversed-chain.json'))
def grow(A, B):   # largest s with s*A inside B
    return min(-e[3] / max(A @ e[:3]) for e in ConvexHull(B).equations)
V = [np.array(v, float) for _, v in CL]
s0 = grow(V[0], V[1]); s6 = 1 / grow(V[5], V[6])
V[0] *= s0; V[6] *= s6
lines = [f'inner dodecahedron x {s0:.9f}, outer dodecahedron x {s6:.9f}']
for (n, _), P in zip(CL, V):
    h = ConvexHull(P); r = np.linalg.norm(P, axis=1)
    lines.append(f'  {n:30s} inradius {min(-h.equations[:, 3]):.6f} circumradius {r.max():.6f} volume {h.volume:.6f}')
for k in range(6):
    lines.append(f'  layer {CL[k][0]} -> {CL[k + 1][0]}: volume {ConvexHull(V[k + 1]).volume - ConvexHull(V[k]).volume:.6f}')
lines.append(f'closure: outer / inner dodecahedron, linear {np.linalg.norm(V[6][0]) / np.linalg.norm(V[0][0]):.9f}')
print('\n'.join(lines)); open('data/polar-tight.txt', 'w').write('\n'.join(lines) + '\n')
json.dump([[n, P.tolist()] for (n, _), P in zip(CL, V)], open('data/reversed-chain-tight.json', 'w'))
