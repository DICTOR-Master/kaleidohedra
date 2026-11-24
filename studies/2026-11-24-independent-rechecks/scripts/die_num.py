# Numerical die geometry in double precision (screen only; exact work is in shadow_exact.py). Own code.
import numpy as np, itertools


def unit(v): v = np.asarray(v, float); return v / np.linalg.norm(v)


def build(U, d, tol=1e-9):
    """U: (N,3) unit normals, d: depths. Returns vertices (array) and per face the ordered vertex index cycle."""
    N = len(U); tri = np.array(list(itertools.combinations(range(N), 3)))
    A = U[tri]; b = d[tri]
    det = np.linalg.det(A); ok = np.abs(det) > 1e-12
    X = np.linalg.solve(A[ok], b[ok][..., None])[..., 0]
    feas = np.all(X @ U.T <= d + tol, axis=1); X = X[feas]
    # cluster
    V = []
    for x in X:
        if not any(np.linalg.norm(x - y) < 1e-7 for y in V): V.append(x)
    V = np.array(V)
    S = V @ U.T - d
    faces = []
    for i in range(N):
        on = np.where(np.abs(S[:, i]) < 1e-7)[0]
        if len(on) < 3: faces.append([]); continue
        c = V[on].mean(0); e1 = unit(V[on[0]] - c); e2 = np.cross(U[i], e1)
        ang = np.arctan2((V[on] - c) @ e2, (V[on] - c) @ e1)
        faces.append(list(on[np.argsort(ang)]))
    return V, faces


def girard(P):
    k = len(P); tot = 0.0
    for a in range(k):
        A, B, C = P[a - 1], P[a], P[(a + 1) % k]
        B = unit(B); tA = A - (A @ B) * B; tC = C - (C @ B) * B
        tot += np.arctan2(np.linalg.norm(np.cross(tA, tC)), tA @ tC)
    return tot - (k - 2) * np.pi


def solid_angles(V, faces): return [girard(V[f]) if f else 0.0 for f in faces]


def edges(faces):
    E = set()
    for f in faces:
        for a in range(len(f)):
            e = tuple(sorted((f[a], f[(a + 1) % len(f)]))); E.add(e)
    return sorted(E)


def mirror_miss(V, E, M):
    """For each edge, the smallest over mirrors m of max(|m.v^|, |m.w^|); return the largest such value."""
    Vh = V / np.linalg.norm(V, axis=1)[:, None]
    worst = 0.0
    for a, b in E:
        m = np.max(np.abs(np.stack([M @ Vh[a], M @ Vh[b]])), axis=0).min()
        worst = max(worst, m)
    return worst
