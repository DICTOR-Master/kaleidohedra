import json, itertools, numpy as np
from scipy.spatial import ConvexHull
S = json.load(open('star.json'))
P = [('ID', np.array(S['centre']))] + [('D', np.array(V)) for V in S['dodecahedra']] + [('J63', np.array(V)) for V in S['caps']]
def faces(W):
    H = ConvexHull(W); F = []
    for e in H.equations:
        idx = tuple(sorted(np.where(np.abs(W @ e[:3] + e[3]) < 1e-7)[0]))
        if idx not in [f for f, _ in F]: F.append((idx, e))
    return F
def overlap(A, B):
    ax = [e[:3] for _, e in faces(A)] + [e[:3] for _, e in faces(B)]
    EA = [A[i] - A[j] for i, j in itertools.combinations(range(len(A)), 2)]; EB = [B[i] - B[j] for i, j in itertools.combinations(range(len(B)), 2)]
    for u in EA:
        for v in EB:
            w = np.cross(u, v)
            if np.linalg.norm(w) > 1e-9: ax.append(w / np.linalg.norm(w))
    for a in ax:
        p, q = A @ a, B @ a
        if min(p.max() - q.min(), q.max() - p.min()) <= 1e-7: return False
    return True
free = []
for k, (nm, W) in enumerate(P):
    for idx, e in faces(W):
        F = W[list(idx)]; c = F.mean(0)
        # a face is free if no other piece has a face on the same plane covering its centre
        cov = False
        for j, (_, Q) in enumerate(P):
            if j == k: continue
            on = np.abs(Q @ e[:3] + e[3]) < 1e-7
            if on.sum() >= 3:
                q = Q[on]; Hq = ConvexHull(np.vstack([q, q.mean(0) + e[:3]]))
                if np.all(Hq.equations[:, :3] @ c + Hq.equations[:, 3] <= 1e-7): cov = True; break
        if not cov: free.append((nm, len(idx), F, e))
from collections import Counter
print('free faces:', Counter((nm, n) for nm, n, _, _ in free))
pyr = []
for nm, n, F, e in free:
    c = F.mean(0); R = np.linalg.norm(F[0] - c); h = np.sqrt(max(1 - R * R, 0))   # pyramid with side edges 1 (= base edge)
    pyr.append((nm, n, np.vstack([F, c + e[:3] * h])))
bad_solid = sum(overlap(Y, W) for _, _, Y in pyr for _, W in P)
bad_pyr = sum(overlap(pyr[i][2], pyr[j][2]) for i, j in itertools.combinations(range(len(pyr)), 2))
print('pyramids', Counter((nm, n) for nm, n, _ in pyr), 'overlapping a solid:', bad_solid, 'overlapping each other:', bad_pyr)
# touching pyramids: pairs sharing a whole face (3 common corners on a common plane)
key = lambda v: tuple(np.round(v, 6))
ks = [set(map(key, Y)) for _, _, Y in pyr]
share = Counter()
for i, j in itertools.combinations(range(len(pyr)), 2):
    if len(ks[i] & ks[j]) >= 3: share[(pyr[i][0], pyr[j][0])] += 1
print('pyramid pairs sharing a face:', dict(share))
# do the apices of the pyramids coincide anywhere?
ap = Counter(key(Y[-1]) for _, _, Y in pyr); print('apex points shared by several pyramids:', Counter(ap.values()))
vol = sum(ConvexHull(W).volume for _, W in P) + sum(ConvexHull(Y).volume for _, _, Y in pyr); print('total volume', round(vol, 6), 'pieces', len(P) + len(pyr))
