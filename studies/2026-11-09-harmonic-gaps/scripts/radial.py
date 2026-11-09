# DICTO 2026-11-09 harmonic-gaps study: radial functions r(u) of star-shaped polyhedral solids and their real spherical-harmonic
# coefficients a_lm = ∫ f(u) Y_lm(u) dΩ, l <= LMAX, by exact-geometry-free but high-order quadrature:
#   1. visible boundary: for each front face F (a convex planar polygon), remove the central projections of every part of another face
#      lying beyond F's plane (shapely); what is left is where the ray from the centre leaves the solid through F.
#   2. the visible pieces are triangulated; each triangle is mapped to the sphere by central projection, so the integrand
#      f(u) dΩ = f(x/|x|) (n.x)/|x|^3 dA is smooth on the planar triangle: collapsed Gauss-Legendre (Duffy) rule, with subdivision.
#   Checks built in: total solid angle 4π and ∫ r^3/3 dΩ = the solid's volume.
import numpy as np
from scipy.special import sph_harm_y
import shapely
from shapely.geometry import Polygon
from shapely.ops import unary_union
LMAX = 30
GRID = 1e-9          # shapely precision grid for the visible-boundary boolean operations
def basis2d(n, d):
    n = np.asarray(n, float); nn = np.linalg.norm(n); n = n / nn; d = d / nn
    a = np.array([1., 0, 0]) if abs(n[0]) < .9 else np.array([0, 1., 0]); u = np.cross(n, a); u /= np.linalg.norm(u); w = np.cross(n, u)
    return n, d, u, w
def clip_beyond(G, n, d, eps=1e-12):
    """part of polygon G (k x 3) with n.y >= d (Sutherland-Hodgman)"""
    out = []; k = len(G)
    for i in range(k):
        a, b = G[i], G[(i + 1) % k]; sa, sb = a @ n - d, b @ n - d
        if sa >= -eps: out.append(a)
        if (sa >= -eps) != (sb >= -eps):
            t = sa / (sa - sb); out.append(a + t * (b - a))
    return np.array(out)
def visible(faces, tol=1e-11):
    """faces: list of (k x 3 float array) convex planar polygons (any orientation) of a star-shaped solid's cells or surface.
    returns list of (n_unit, d, list of 3D triangles) visible from the centre."""
    F = [np.asarray(f, float) for f in faces]
    planes = []
    for f in F:
        n = np.cross(f[1] - f[0], f[2] - f[0])
        for i in range(2, len(f) - 1):
            m = np.cross(f[i] - f[0], f[i + 1] - f[0])
            if np.linalg.norm(m) > np.linalg.norm(n): n = m
        n /= np.linalg.norm(n); d = n @ f[0]
        if d < 0: n, d = -n, -d
        planes.append((n, d))
    caps = []                                                   # angular caps: skip occluders that cannot overlap
    for f in F:
        U = f / np.linalg.norm(f, axis=1)[:, None]; c = U.mean(0); nc = np.linalg.norm(c)
        caps.append((c / nc, np.arccos(np.clip(U @ (c / nc), -1, 1)).max()) if nc > 1e-9 else (np.array([0, 0, 1.]), np.pi))
    CC = np.array([c for c, _ in caps]); CR = np.array([r for _, r in caps])
    out = []
    for i, f in enumerate(F):
        n, d = planes[i]
        if d < 1e-12: continue
        cand = np.where(np.arccos(np.clip(CC @ CC[i], -1, 1)) <= CR + CR[i] + 1e-6)[0]
        _, _, u, w = basis2d(n, d); o = n * d
        to2 = lambda X: np.c_[(X - o) @ u, (X - o) @ w]
        base = Polygon(to2(f)).buffer(0)
        if base.area < 1e-14: continue
        occ = []
        for j in cand:
            g = F[j]
            if j == i: continue
            ng, dg = planes[j]
            if abs(ng @ n - 1) < 1e-12 and abs(dg - d) < 1e-12: continue   # coplanar: same plane, never beyond
            G = clip_beyond(g, n, d * (1 + 1e-13))
            if len(G) < 3: continue
            X = G * (d / (G @ n))[:, None]
            pg = Polygon(to2(X)).buffer(0)
            if pg.area > 1e-15 and pg.intersects(base): occ.append(pg)
        vis = base.difference(unary_union(occ), grid_size=GRID) if occ else base
        vis = clean(shapely.set_precision(vis, GRID)) if occ else vis
        if vis.area < tol: continue
        tris = []
        for t in shapely.constrained_delaunay_triangles(vis).geoms:
            if t.area < 1e-15: continue
            c = np.array(t.exterior.coords)[:3]
            tris.append(o + c[:, :1] * u + c[:, 1:2] * w)
        out.append((n, d, tris))
    return snap_float(out, planes)
def snap_float(vis, planes, tol=1e-6):
    """move every corner of the visible triangles onto the exact meet of the face planes through it (least squares over the planes
    within tol; corners lie on >= 3 planes), removing the ~1e-9 shapely grid error"""
    N = np.array([n for n, d in planes]); D = np.array([d for n, d in planes]); cache = {}; bad = 0
    def sp(x):
        k = tuple(np.round(x, 6))
        if k in cache: return cache[k]
        idx = np.abs(N @ x - D) < tol; y = x
        if idx.sum() >= 3 and np.linalg.matrix_rank(N[idx], 1e-9) == 3:
            y = np.linalg.lstsq(N[idx], D[idx], rcond=None)[0]
        cache[k] = y; return y
    out = []
    for n, d, tris in vis:
        T = []
        for t in tris:
            y = np.array([sp(x) for x in t]); y = y - np.outer(y @ n - d, n); T.append(y)
        out.append((n, d, T))
    return out
def _ring(c, tol=1e-7):
    c = np.asarray(c)[:-1]; changed = True
    while changed and len(c) > 3:
        changed = False
        for i in range(len(c)):
            a, b, d = c[i - 1], c[i], c[(i + 1) % len(c)]
            e1, e2 = b - a, d - b
            if abs(e1[0] * e2[1] - e1[1] * e2[0]) < tol * np.linalg.norm(e1) * np.linalg.norm(e2) and e1 @ e2 > 0:
                c = np.delete(c, i, 0); changed = True; break
    return c
def clean(geom):
    """drop vertices lying in the middle of a straight edge (artefacts of the boolean operations)"""
    polys = [geom] if geom.geom_type == 'Polygon' else [g for g in getattr(geom, 'geoms', []) if g.geom_type == 'Polygon']
    out = [Polygon(_ring(p.exterior.coords), [_ring(h.coords) for h in p.interiors]) for p in polys if p.area > 1e-14]
    return shapely.MultiPolygon(out) if len(out) != 1 else out[0]
def gauss_tri(order):
    x, wx = np.polynomial.legendre.leggauss(order); x = (x + 1) / 2; wx = wx / 2
    xi, eta = np.meshgrid(x, x, indexing='ij'); W = np.outer(wx, wx)
    a = xi; b = eta * (1 - xi); J = (1 - xi)
    return a.ravel(), b.ravel(), (W * J).ravel()        # weights sum to 1/2 (area of the unit triangle)
def subdivide(tri, maxang):
    A, B, C = tri
    ang = lambda p, q: np.arccos(np.clip(p @ q / np.linalg.norm(p) / np.linalg.norm(q), -1, 1))
    if max(ang(A, B), ang(B, C), ang(C, A)) <= maxang: return [tri]
    ab, bc, ca = (A + B) / 2, (B + C) / 2, (C + A) / 2
    return [t for s in ([A, ab, ca], [ab, B, bc], [ca, bc, C], [ab, bc, ca]) for t in subdivide(np.array(s), maxang)]
def quad_points(vis, order=24, maxang=0.3):
    """points x on the visible surface with solid-angle weights: returns X (N x 3), wΩ (N)"""
    a, b, wq = gauss_tri(order); Xs, Ws = [], []
    for n, d, tris in vis:
        for t in tris:
            for s in subdivide(np.asarray(t), maxang):
                A, B, C = s; area2 = np.linalg.norm(np.cross(B - A, C - A))
                X = A + a[:, None] * (B - A) + b[:, None] * (C - A); r = np.linalg.norm(X, axis=1)
                Xs.append(X); Ws.append(wq * area2 * d / r ** 3)
    return np.vstack(Xs), np.concatenate(Ws)
def real_Y_slow(U, lmax=LMAX):
    """reference: real orthonormal Y_lm from scipy (used only to check real_Y)"""
    th = np.arccos(np.clip(U[:, 2], -1, 1)); ph = np.arctan2(U[:, 1], U[:, 0]); out = {}
    for l in range(lmax + 1):
        rows = []
        for m in range(-l, l + 1):
            y = sph_harm_y(l, abs(m), th, ph)
            rows.append(np.sqrt(2) * (-1) ** m * (y.imag if m < 0 else y.real) if m != 0 else y.real)
        out[l] = np.array(rows)
    return out
def real_Y(U, lmax=LMAX):
    """real orthonormal spherical harmonics (no Condon-Shortley phase) by the fully normalised Legendre recurrence:
    dict l -> (2l+1) x N array, rows m = -l..l (m<0: sin |m| phi, m>0: cos m phi)"""
    x = np.clip(U[:, 2], -1, 1); s = np.sqrt(np.maximum(0, 1 - x * x)); ph = np.arctan2(U[:, 1], U[:, 0])
    Pb = {(0, 0): np.full(len(x), 1 / np.sqrt(4 * np.pi))}
    for m in range(1, lmax + 1): Pb[(m, m)] = np.sqrt((2 * m + 1) / (2 * m)) * s * Pb[(m - 1, m - 1)]
    for m in range(0, lmax):
        Pb[(m + 1, m)] = np.sqrt(2 * m + 3) * x * Pb[(m, m)]
        for l in range(m + 2, lmax + 1):
            a = np.sqrt((4 * l * l - 1) / (l * l - m * m)); b = np.sqrt(((l - 1) ** 2 - m * m) / (4 * (l - 1) ** 2 - 1))
            Pb[(l, m)] = a * (x * Pb[(l - 1, m)] - b * Pb[(l - 2, m)])
    C = [np.cos(m * ph) for m in range(lmax + 1)]; S = [np.sin(m * ph) for m in range(lmax + 1)]; out = {}
    for l in range(lmax + 1):
        out[l] = np.array([np.sqrt(2) * Pb[(l, -m)] * S[-m] if m < 0 else (Pb[(l, 0)] if m == 0 else np.sqrt(2) * Pb[(l, m)] * C[m]) for m in range(-l, l + 1)])
    return out
def coeffs(X, W, f, lmax=LMAX, Y=None, chunk=60000):
    """a_lm of f (array on the points X) and the power spectrum P_l = sum_m a_lm^2 (points taken in chunks to bound memory)"""
    U = X / np.linalg.norm(X, axis=1)[:, None]
    if Y is not None: a = {l: Y[l] @ (W * f) for l in range(lmax + 1)}
    else:
        a = {l: np.zeros(2 * l + 1) for l in range(lmax + 1)}
        for i in range(0, len(W), chunk):
            Yc = real_Y(U[i:i + chunk], lmax); wf = (W * f)[i:i + chunk]
            for l in range(lmax + 1): a[l] += Yc[l] @ wf
    return a, np.array([np.sum(a[l] ** 2) for l in range(lmax + 1)])
def radial_at(vis, U):
    """r(u) at unit vectors U by the farthest hit on the visible triangles' planes (brute force; for plots and cross-checks)"""
    r = np.zeros(len(U))
    for n, d, tris in vis:
        cos = U @ n; ok = cos > 1e-12; t = np.where(ok, d / np.where(ok, cos, 1), 0)
        for A, B, C in tris:
            X = U * t[:, None]
            # barycentric test in the plane
            v0, v1 = B - A, C - A; v2 = X - A
            d00, d01, d11 = v0 @ v0, v0 @ v1, v1 @ v1; d20, d21 = v2 @ v0, v2 @ v1; den = d00 * d11 - d01 * d01
            bb = (d11 * d20 - d01 * d21) / den; cc = (d00 * d21 - d01 * d20) / den
            hit = ok & (bb >= -1e-12) & (cc >= -1e-12) & (bb + cc <= 1 + 1e-12)
            r = np.where(hit & (t > r), t, r)
    return r
def union_boundary(cells_faces, tol=1e-10):
    """boundary of a union of interior-disjoint convex cells. cells_faces: list (per cell) of face polygons (k x 3), any orientation.
    returns list of (outward unit normal n, d = n.x on the face (signed), list of 3D triangles): each cell face minus the coplanar
    faces of other cells lying on its other side."""
    allf = []
    for ci, faces in enumerate(cells_faces):
        cc = np.vstack(faces).mean(0)
        for f in faces:
            f = np.asarray(f, float); n = np.cross(f[1] - f[0], f[2] - f[0])
            for i in range(2, len(f) - 1):
                m = np.cross(f[i] - f[0], f[i + 1] - f[0])
                if np.linalg.norm(m) > np.linalg.norm(n): n = m
            n /= np.linalg.norm(n)
            if n @ (f.mean(0) - cc) < 0: n = -n                 # outward from its own cell
            allf.append((ci, f, n, n @ f[0]))
    from collections import defaultdict
    byplane = defaultdict(list)
    for k, (ci, f, n, d) in enumerate(allf):
        s = 1 if (n[np.argmax(np.abs(n))] > 0) else -1
        byplane[tuple(np.round(np.r_[s * n, s * d], 7))].append(k)
    out = []
    for key, ks in byplane.items():
        for k in ks:
            ci, f, n, d = allf[k]; _, _, u, w = basis2d(n, abs(d) if abs(d) > 0 else 1.0); o = n * d
            to2 = lambda X: np.c_[(X - o) @ u, (X - o) @ w]
            base = Polygon(to2(f)).buffer(0)
            opp = [Polygon(to2(allf[j][1])).buffer(0) for j in ks if j != k and allf[j][0] != ci and allf[j][2] @ n < 0]
            rem = base.difference(unary_union(opp), grid_size=GRID) if opp else base
            if rem.area < tol: continue
            rem = clean(shapely.set_precision(rem, GRID)) if opp else rem
            tris = [o + np.array(t.exterior.coords)[:3][:, :1] * u + np.array(t.exterior.coords)[:3][:, 1:2] * w
                    for t in shapely.constrained_delaunay_triangles(rem).geoms if t.area > 1e-15]
            out.append((n, d, tris))
    return snap_float(out, [(n, d) for _, _, n, d in allf])
def signed_mass_coeffs(bnd, lmax=LMAX, order=24, maxang=0.3, power=3):
    """coefficients of the angular mass m(u) = ∫ 1_solid(t u) t^2 dt = sum over boundary crossings (+-) t^3/3 (power = 3), or of the
    crossing count (power = 0: 0 when every ray crosses the boundary once more outward than inward ... i.e. returns the net count 1);
    also returns the total solid angle swept by outward crossings minus inward ones (= 4π for a solid containing O)"""
    a, b, wq = gauss_tri(order); Xs, Ws = [], []
    for n, d, tris in bnd:
        if abs(d) < 1e-12: continue
        for t in tris:
            for sdiv in subdivide(np.asarray(t), maxang):
                A, B, C = sdiv; area2 = np.linalg.norm(np.cross(B - A, C - A))
                X = A + a[:, None] * (B - A) + b[:, None] * (C - A); r = np.linalg.norm(X, axis=1)
                Xs.append(X); Ws.append(wq * area2 * d / r ** 3)          # signed: d > 0 exit, d < 0 entry
    X = np.vstack(Xs); W = np.concatenate(Ws); r = np.linalg.norm(X, axis=1)
    f = r ** power / 3 if power == 3 else np.ones(len(r))
    return coeffs(X, W, f, lmax), W.sum(), (W * r ** 3).sum() / 3, len(W)
