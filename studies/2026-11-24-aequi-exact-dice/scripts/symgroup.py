# full orthogonal symmetry group of a finite set of unit vectors (double precision), and its orbits
import numpy as np, itertools
def symgroup(U, tol=1e-9):
    n = len(U); a = 0; b = next(j for j in range(n) if abs(abs(U[0] @ U[j]) - 1) > 1e-6)
    def frame(x, y):
        e1 = x; e2 = y - (y @ x) * x; e2 /= np.linalg.norm(e2); return np.array([e1, e2, np.cross(e1, e2)]).T
    F0 = frame(U[a], U[b]); G = []
    for i in range(n):
        for j in range(n):
            if i == j or abs(U[i] @ U[j] - U[a] @ U[b]) > 1e-9: continue
            for s in (1, -1):
                F = frame(U[i], U[j]); F[:, 2] *= s; M = F @ F0.T
                img = U @ M.T; d = np.abs(img[:, None, :] - U[None, :, :]).max(2)
                if (d.min(1) < tol).all() and len(set(d.argmin(1))) == n: G.append(M)
    return G
def orbits(U, G):
    seen = set(); out = []
    for i in range(len(U)):
        if i in seen: continue
        o = {int(np.abs(U - M @ U[i]).max(1).argmin()) for M in G}; seen |= o; out.append(sorted(o))
    return out
