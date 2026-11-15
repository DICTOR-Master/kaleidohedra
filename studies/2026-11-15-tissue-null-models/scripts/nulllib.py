"""Shared tools for the tissue null models (study 2026-11-15-tissue-null-models).
Periodic Delaunay/Voronoi by replication (scipy.spatial / Qhull: Barber, Dobkin, Huhdanpaa 1996, credited),
circumcentres, edge sets, slice statistics. Every function used by the jobs lives here."""
import itertools
import numpy as np
from scipy.spatial import Delaunay


def replicate(P, margin):
    """Copies of the unit-torus points P (n x d) lying within `margin` of the box. Returns X, orig index, offset."""
    n, d = P.shape
    Xs, idx, offs = [P], [np.arange(n)], [np.zeros((n, d))]
    for off in itertools.product((-1, 0, 1), repeat=d):
        if not any(off):
            continue
        Q = P + np.array(off, float)
        keep = np.all((Q > -margin) & (Q < 1 + margin), axis=1)
        if keep.any():
            Xs.append(Q[keep]); idx.append(np.nonzero(keep)[0]); offs.append(np.tile(off, (keep.sum(), 1)))
    return np.vstack(Xs), np.concatenate(idx), np.vstack(offs)


def circumcentres(X, S):
    """Circumcentres of the simplices S (m x (d+1)) of points X; batched linear solve."""
    p0 = X[S[:, 0]]
    A = 2.0 * (X[S[:, 1:]] - p0[:, None, :])
    b = (X[S[:, 1:]] ** 2).sum(-1) - (p0 ** 2).sum(-1)[:, None]
    det = np.linalg.det(A)
    scale = np.abs(A).max(axis=(1, 2)) ** A.shape[1]
    good = np.abs(det) > 1e-12 * scale
    C = np.full((len(S), X.shape[1]), np.nan)
    C[good] = np.linalg.solve(A[good], b[good][..., None])[..., 0]
    return C   # nan = flat simplex (only on the outer hull of the replicated set)


def periodic_delaunay(P, margin_cells=4.0):
    n, d = P.shape
    ell = n ** (-1.0 / d)
    X, orig, off = replicate(P, margin_cells * ell)
    tri = Delaunay(X)
    return X, orig, tri


def edge_keys(P, margin_cells=4.0):
    """Set of Delaunay edges (contacts) of the periodic tessellation, keyed by the sorted original pair."""
    n = len(P)
    X, orig, tri = periodic_delaunay(P, margin_cells)
    S = tri.simplices
    d1 = S.shape[1]
    a = []
    for i, j in itertools.combinations(range(d1), 2):
        a.append(S[:, [i, j]])
    E = np.vstack(a)
    # keep edges with at least one endpoint in the box (an original copy)
    inbox = np.zeros(len(X), bool); inbox[:n] = True
    E = E[inbox[E[:, 0]] | inbox[E[:, 1]]]
    oi, oj = orig[E[:, 0]], orig[E[:, 1]]
    lo, hi = np.minimum(oi, oj), np.maximum(oi, oj)
    return np.unique(lo.astype(np.int64) * n + hi)


def sweep_indices(P, u, margin_cells=4.0):
    """Index census of a generic linear sweep (height u.x) of the periodic Poisson-Voronoi tessellation of P.
    Voronoi vertices = Delaunay simplices with circumcentre in the box (one per period); index i = number of the
    vertex's d+1 edges that go down (to a neighbouring vertex of lower height)."""
    n, d = P.shape
    X, orig, tri = periodic_delaunay(P, margin_cells)
    C = circumcentres(X, tri.simplices)
    h = C @ u
    with np.errstate(invalid='ignore'):
        inside = np.all((C >= 0) & (C < 1), axis=1)
    nb = tri.neighbors[inside]
    if (nb < 0).any() or np.isnan(h[nb]).any():
        raise RuntimeError('hull reached: margin too small')
    idx = (h[nb] < h[inside][:, None]).sum(1)
    return np.bincount(idx, minlength=d + 2), int(inside.sum())


def polygon_area(groups, pts):
    """Areas of convex polygons: groups = array of polygon ids (sorted any way), pts = 2D vertices."""
    order = np.argsort(groups, kind='stable')
    g, p = groups[order], pts[order]
    ids, start, cnt = np.unique(g, return_index=True, return_counts=True)
    cen = np.add.reduceat(p, start) / cnt[:, None]
    rel = p - np.repeat(cen, cnt, axis=0)
    ang = np.arctan2(rel[:, 1], rel[:, 0])
    o2 = np.lexsort((ang, g))
    g, rel = g[o2], rel[o2]
    nxt = np.arange(len(g)) + 1
    ends = start + cnt - 1
    nxt[ends] = start
    cr = rel[:, 0] * rel[nxt, 1] - rel[:, 1] * rel[nxt, 0]
    return ids, 0.5 * np.add.reduceat(cr, start)


def tissue_stats(n_of, nbr_pairs, area=None):
    """Neighbour distribution, mu2, Aboav-Weaire fit and Lewis fit for a 2D tessellation.
    n_of: sides per cell (array over cells); nbr_pairs: (k x 2) cell index pairs (each contact once)."""
    n_of = np.asarray(n_of)
    out = {}
    N = len(n_of)
    out['cells'] = int(N)
    out['mean_n'] = float(n_of.mean())
    out['mu2'] = float(((n_of - n_of.mean()) ** 2).mean())
    vals, cnt = np.unique(n_of, return_counts=True)
    out['p_n'] = {int(v): float(c / N) for v, c in zip(vals, cnt)}
    # Aboav-Weaire: m(n) = mean sides of the neighbours of n-sided cells
    s = np.zeros(N); np.add.at(s, nbr_pairs[:, 0], n_of[nbr_pairs[:, 1]]); np.add.at(s, nbr_pairs[:, 1], n_of[nbr_pairs[:, 0]])
    m = s / np.maximum(n_of, 1)
    mn = {}
    for v in vals:
        sel = n_of == v
        if sel.sum() >= 50:
            mn[int(v)] = float(m[sel].mean())
    out['m_n'] = mn
    ns = np.array(sorted(mn)); ms = np.array([mn[k] for k in ns]); w = np.array([np.sum(n_of == k) for k in ns])
    # n m(n) = (6 - a) n + 6 a + mu2  -> linear in n: slope 6 - a
    A = np.vstack([ns, np.ones_like(ns)]).T.astype(float)
    coef = np.linalg.lstsq(A * np.sqrt(w)[:, None], ns * ms * np.sqrt(w), rcond=None)[0]
    out['aboav_a'] = float(6 - coef[0]); out['aboav_intercept'] = float(coef[1])
    out['aboav_intercept_pred'] = float(6 * (6 - coef[0]) + out['mu2'])
    if area is not None:
        area = np.asarray(area) / np.mean(area)
        an = {int(v): float(area[n_of == v].mean()) for v in vals if (n_of == v).sum() >= 50}
        out['area_n'] = an
        ks = np.array(sorted(an)); wa = np.array([np.sum(n_of == k) for k in ks])
        B = np.vstack([ks, np.ones_like(ks)]).T.astype(float)
        cl = np.linalg.lstsq(B * np.sqrt(wa)[:, None], np.array([an[k] for k in ks]) * np.sqrt(wa), rcond=None)[0]
        out['lewis_slope'] = float(cl[0]); out['lewis_n0'] = float(-cl[1] / cl[0])
    return out
