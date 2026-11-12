# window_tools.py: shared detector for the OG Galois-twin window test (DICTO, queued 12 Nov 2026). Float stage only: the twins it reads
# are computed exactly (or as certified balls) by the callers and rounded once.
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
PHI = (1 + 5 ** .5) / 2

def ico_axes(twin_frame=False):
    """one unit axis per class (5-, 3-, 2-fold) for the frame with icosahedron corners (0, +-1, +-phi) cyclic; twin frame phi -> 1 - phi."""
    p = 1 - PHI if twin_frame else PHI
    u = lambda v: np.array(v, float) / np.linalg.norm(v)
    return {5: u((0, 1, p)), 3: u((1, 1, 1)), 2: u((1, 0, 0))}

def covering_ratio(P, samples=20000, seed=1):
    """largest empty gap inside the hull of P relative to its size: 1D max gap / length; 3D max over random interior samples of the
    distance to the nearest point / circumradius about the hull centre. Small = the points fill their hull."""
    P = np.asarray(P, float)
    if len(P) < 2: return float('nan')
    if P.shape[1] == 1:
        x = np.sort(P[:, 0]); L = x[-1] - x[0]
        return float(np.diff(x).max() / L) if L > 0 else float('nan')
    sc = np.abs(P).max(); Q = P / sc
    if len(Q) < 5: return float('nan')
    h = ConvexHull(Q); c = Q[h.vertices].mean(0); R = np.linalg.norm(Q[h.vertices] - c, axis=1).max()
    lo, hi = Q[h.vertices].min(0), Q[h.vertices].max(0); rng = np.random.default_rng(seed); S = []
    while sum(len(s) for s in S) < samples:
        X = lo + (hi - lo) * rng.random((4 * samples, 3)); S.append(X[(X @ h.equations[:, :3].T + h.equations[:, 3]).max(1) <= 0])
    S = np.concatenate(S)[:samples]
    return float(cKDTree(Q).query(S, workers=2)[0].max() / R)

def classify(levels):
    """levels: list of twin point arrays for growing patches. Returns class + twin radius R and covering ratio rho by level."""
    R = [float(np.linalg.norm(np.asarray(P, float), axis=1).max()) for P in levels]
    rho = [covering_ratio(P) for P in levels]
    g = R[-1] / R[0]
    if g > 10: cl = 'UNBOUNDED'
    elif g < 1e-3: cl = 'COLLAPSE'
    elif np.isfinite(rho[-1]) and (rho[-1] < 0.1 or rho[-1] < 0.5 * rho[0]): cl = 'WINDOW'
    else: cl = 'BOUNDED, NOT FILLING'
    return {'class': cl, 'R': R, 'rho': rho, 'growth_last_over_first': g}

def hull_fingerprint(P, axes=None, tol=1e-9):
    """convex hull of P (scaled to size 1): corner count, faces by polygon size (coplanar facets merged), and the support h(u)/R on the
    5-, 3-, 2-fold axes (about the hull centre), R = circumradius about the centre."""
    P = np.asarray(P, float); sc = np.abs(P).max(); Q = P / sc
    h = ConvexHull(Q); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    V = set(h.vertices.tolist()); faces = {}
    for m in grp.values():
        k = len(m & V); faces[k] = faces.get(k, 0) + 1
    out = {'corners': len(V), 'faces': dict(sorted(faces.items()))}
    if axes is not None:
        c = Q[h.vertices].mean(0); C = Q[h.vertices] - c; R = np.linalg.norm(C, axis=1).max()
        out['h'] = {k: round(float((C @ u).max() / R), 6) for k, u in axes.items()}
        out['R_over_r'] = round(float(R / (-(E[:, 3] + E[:, :3] @ c)).min()), 6)
    return out
