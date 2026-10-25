# Is TT (ABAC, tet piece at 5/24) congruent to the cubic octet tet piece at 5/24 (ABC)? And Fang/Chucky to anything in AB/ABC?
# Congruence by sorted pairwise corner distances (feedback: corner matching, not edge lists).
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open("reach.py").read().split("Rmax = 0")[0])
from scipy.spatial import HalfspaceIntersection
def cellV(M, S, i, lam):
    w = lambda k: lam if k == "tet" else 0.0; kp, p = M[i]; H = []
    for k, q in S:
        dv = q - p
        if np.allclose(dv, 0) or dv @ dv > 16: continue
        H.append(np.r_[2 * dv, -(q @ q - p @ p - w(k) + w(kp))])
    H = np.array(H); A, b = H[:, :3], -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if r.x[3] < 1e-7: return None
    return np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 8), axis=0)
def fp(V): return np.sort(np.round([np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2)], 6))

allp = []
for word in ("ABC", "AB", "ABAC"):
    M, S = sites_of(word)
    for lam in (5 / 24, -3 / 8):
        for i in range(len(M)):
            V = cellV(M, S, i, lam)
            if V is None: continue
            allp.append((word, round(lam, 4), M[i][0], len(V), round(ConvexHull(V).volume, 6), fp(V)))
targets = {"TT": 0.344824, "Fang": 0.021824, "Chucky": 0.705265}
for nm, vol in targets.items():
    mine = [p for p in allp if p[0] == "ABAC" and abs(p[4] - vol) < 2e-6]
    if not mine: print(nm, "not found"); continue
    p = mine[0]
    match = sorted({(o[0], o[1], o[2], o[3], o[4]) for o in allp if o[0] != "ABAC" and o[3] == p[3] and np.allclose(o[5], p[5], atol=1e-5)})
    near = sorted({(o[0], o[1], o[2], o[3], o[4]) for o in allp if o[0] != "ABAC" and o[2] == p[2] and abs(o[1] - p[1]) < 1e-9})
    print(nm, p[:5], "| congruent to:", match or "nothing in AB or ABC", "| same-kind pieces there:", near)
