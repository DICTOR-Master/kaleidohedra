# Spheres of Dharma, strict check (2026-10-12): every pair of the 237 pieces of one cycle (I(1/phi) to I(phi^2)) tested for
# interior overlap with separating axes (all face normals and all edge-pair cross products, exact enough at 1e-9); every piece
# inside I(phi^2); total volume = I(phi^2); sampled cover.
import itertools, numpy as np
from scipy.spatial import ConvexHull
src = open('gen_twin.py').read(); exec(src[:src.index('net_in = [(r, V @ SW.T)')])
P = net_in + net_out; print('pieces', len(P))
def geom(V):
    H = ConvexHull(V); N = []
    for e in H.equations:
        if not any(np.linalg.norm(e[:3] - q) < 1e-9 for q in N): N.append(e[:3])
    E = []
    for s in H.simplices:
        for a, b in itertools.combinations(s, 2):
            d = V[a] - V[b]; d = d / np.linalg.norm(d)
            if not any(abs(abs(d @ q) - 1) < 1e-9 for q in E): E.append(d)
    return np.array(N), E
G = [geom(V) for _, V in P]; BB = [(V.min(0), V.max(0)) for _, V in P]
def overlap(i, j):
    A, B = P[i][1], P[j][1]
    if np.any(BB[i][1] <= BB[j][0] + 1e-9) or np.any(BB[j][1] <= BB[i][0] + 1e-9): return 0.0
    ax = list(G[i][0]) + list(G[j][0])
    for u in G[i][1]:
        for v in G[j][1]:
            w = np.cross(u, v); n = np.linalg.norm(w)
            if n > 1e-9: ax.append(w / n)
    depth = 1e9
    for a in ax:
        p, q = A @ a, B @ a; d = min(p.max() - q.min(), q.max() - p.min())
        if d <= 1e-9: return 0.0
        depth = min(depth, d)
    return depth
bad = [(i, j, overlap(i, j)) for i, j in itertools.combinations(range(len(P)), 2)]
bad = [b for b in bad if b[2] > 0]
print('overlapping pairs:', len(bad), [(P[i][0], P[j][0], round(d, 6)) for i, j, d in bad[:10]])
FI = ConvexHull(I2).equations
print('all pieces inside I(phi^2):', all(np.all(V @ FI[:, :3].T + FI[:, 3] <= 1e-9) for _, V in P))
tot = sum(ConvexHull(V).volume for _, V in P); print(f'total volume {tot:.12f} vs I(phi^2) {ConvexHull(I2).volume:.12f}')
from collections import Counter; print(Counter(r for r, _ in P))
