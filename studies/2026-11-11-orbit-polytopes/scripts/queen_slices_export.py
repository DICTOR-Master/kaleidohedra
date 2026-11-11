"""Export one mirror slice per stage (600-cell, bitruncated 600-cell, 120-cell) for the figure: the 3D section (hull faces) and the
2-faces lying in the mirror, in 3D coordinates of the mirror."""
import sys, json, numpy as np
from scipy.spatial import ConvexHull, cKDTree
sys.argv = ['x', 'none']
exec(open('vacuus_queens.py').read().split('out = []')[0])
res = {}
for name in ['600-cell', 'bitruncated 600-cell', '120-cell']:
    X, F = stage(name); X = X / np.linalg.norm(X, axis=1).max()
    nn = cKDTree(X).query(X, k=2)[0][:, 1].min(); E = list(cKDTree(X).query_pairs(nn * 1.0001))
    # a mirror: the normal shared by the most faces
    N = {}
    for f in F:
        n = normal_of(X[f]); k = tuple(np.round(n, 5)); N.setdefault(k, []).append(f)
    key = max(N, key=lambda k: len(N[k])); n = normal_of(X[N[key][0]])      # exact normal of a carried face, not the rounded key
    Bs = np.linalg.svd(n.reshape(1, -1))[2][1:]
    pts = [X[i] for i in range(len(X)) if abs(X[i] @ n) < 1e-7]
    for a, b in E:
        sa, sb = X[a] @ n, X[b] @ n
        if abs(sa) > 1e-7 and abs(sb) > 1e-7 and sa * sb < 0: pts.append(X[a] + (X[b] - X[a]) * sa / (sa - sb))
    Q = np.unique(np.round(np.array(pts) @ Bs.T, 7), axis=0); h = ConvexHull(Q)
    G = {}
    for simp, eq in zip(h.simplices, h.equations): G.setdefault(tuple(np.round(eq, 5)), set()).update(simp)
    hull_faces = []
    for eq, vs in G.items():
        P = Q[list(vs)]; c = P.mean(0); nrm = np.array(eq[:3]); u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(nrm, u)
        order = sorted(vs, key=lambda i: np.arctan2((Q[i] - c) @ w, (Q[i] - c) @ u)); hull_faces.append([Q[i].tolist() for i in order])
    carried = []
    for f in N[key]:
        P = X[f] @ Bs.T; c = P.mean(0); nrm = np.linalg.svd(P - c)[2][-1]; u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(nrm, u)
        order = sorted(range(len(f)), key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); carried.append([P[i].tolist() for i in order])
    res[name] = {'hull': hull_faces, 'carried': carried}
    print(name, 'slice corners', len(Q), 'hull faces', len(hull_faces), 'carried faces', len(carried), sorted({len(c) for c in carried}))
json.dump(res, open('queen_slices.json', 'w'))
