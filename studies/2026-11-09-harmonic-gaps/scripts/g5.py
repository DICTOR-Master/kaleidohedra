# DICTO 2026-11-09 harmonic-gaps study: shared exact geometry in Q(sqrt5) (on top of q5.py / exactpoly.py, copied from
# studies/2026-10-18-ocd-octet/scripts) -- regular solids, faces, stellation faces of the Kepler-Poinsot solids, polars, and exact
# volume of (convex piece) ∩ (star-shaped solid given as cones from the centre over its visible boundary).
import itertools, numpy as np
from fractions import Fraction as Fr
from q5 import *
from exactpoly import planes_of, intersect, volume
P = PHI; IP = qs(P, ONE); H = qr(Fr(1, 2))
V3 = lambda a, b, c: [x if isinstance(x, tuple) else qr(Fr(x)) for x in (a, b, c)]
key = lambda p: tuple(tuple(x) for x in p)
fl = lambda p: np.array([qf(x) for x in p])
def vsum(xs):
    t = Z
    for x in xs: t = qa(t, x)
    return t
def cyc(v):
    out = {}
    for k in range(3):
        p = v[k:] + v[:k]
        for s in itertools.product((1, -1), repeat=3):
            q = [qm(qr(a), b) for a, b in zip(s, p)]; out[key(q)] = q
    return list(out.values())
def scale(Pts, s): return [vmul(p, s) for p in Pts]
def cent(Pts): return [qd(vsum(p[i] for p in Pts), qr(len(Pts))) for i in range(3)]
def icosahedron(): return cyc([Z, H, qm(P, H)])                                  # edge 1
def dodecahedron_cube():                                                          # Euclid: cube (+-1)^3 + 6 roofs, edge 2/phi
    C8 = [V3(*s) for s in itertools.product((1, -1), repeat=3)]
    return C8 + cyc([Z, IP, P])
def faces(Pts):
    """exact face polygons (ordered, float angle sort) of the convex hull: list of (plane (n,d), [corners])"""
    out = []
    for n, d in planes_of(Pts):
        F = [p for p in Pts if dot(n, p) == d]; c = fl(cent(F)); nf = fl(n); u = fl(F[0]) - c; w = np.cross(nf, u)
        F = [p for _, p in sorted(((np.arctan2((fl(p) - c) @ w, (fl(p) - c) @ u), i), p) for i, p in enumerate(F))]
        out.append(((n, d), F))
    return out
def polar(Pts, rho2=ONE):
    """corners of the polar body {y: x.y <= rho2 for x in hull(Pts)}: one corner per face plane n.x = d -> rho2 n / d"""
    return [vmul(n, qd(rho2, d)) for n, d in planes_of(Pts)]
def same_set(A, B): return {key(p) for p in A} == {key(p) for p in B}
def inside_hull(p, planes): return all(sgn(qs(d, dot(n, p))) >= 0 for n, d in planes)
def star_faces(hullpts, planes):
    """Kepler-Poinsot star faces: for each plane, the corners of hullpts lying on it, as a star polygon ordered by angle"""
    out = []
    for n, d in planes:
        F = [p for p in hullpts if dot(n, p) == d]
        if len(F) < 3: continue
        c = fl(cent(F)); nf = fl(n); u = fl(F[0]) - c; w = np.cross(nf, u)
        F = [p for _, p in sorted(((np.arctan2((fl(p) - c) @ w, (fl(p) - c) @ u), i), p) for i, p in enumerate(F))]
        out.append(((n, d), F))
    return out
def cone_planes(tri):
    """exact planes of the tetrahedron (O, a, b, c), outward"""
    O = [Z, Z, Z]; return planes_of([O] + list(tri))
def vol_in_star(piece_planes, cones):
    """exact volume of a convex piece inside a star-shaped solid given as interior-disjoint convex cones (list of plane lists)"""
    t = Z
    for cp in cones:
        C = intersect(piece_planes + cp)
        if C: t = qa(t, volume(C))
    return t
def snap(x, planes, tol=1e-7):
    """the exact point (intersection of three of the exact planes) at float point x"""
    near = [(n, d) for n, d in planes if abs(fl(n) @ x - qf(d)) / np.linalg.norm(fl(n)) < tol]
    for a, b, c in itertools.combinations(near, 3):
        A = [a[0], b[0], c[0]]
        if det3(*A) == Z: continue
        cols = lambda k: [[[a[1], b[1], c[1]][i] if j == k else A[i][j] for j in range(3)] for i in range(3)]
        p = [qd(det3(*cols(k)), det3(*A)) for k in range(3)]
        if np.linalg.norm(fl(p) - x) < 1e-6: return p
    raise ValueError(f'no exact corner at {x}')
def exact_cones(vis, planes):
    """exact cones (O, a, b, c) over the visible triangles; returns list of (corners, plane list, float corners)"""
    cache = {}; out = []
    def sp(x):
        k = tuple(np.round(x, 7))
        if k not in cache: cache[k] = snap(x, planes)
        return cache[k]
    for n, d, tris in vis:
        for t in tris:
            T = [sp(x) for x in t]; O = [Z, Z, Z]
            out.append((T, planes_of([O] + T), np.array([fl(p) for p in T])))
    return out
def ang_overlap(Pf, Tf):
    """cheap float pre-test: can convex piece (corners Pf) meet the cone over triangle Tf? (angular caps)"""
    def cap(V):
        U = V / np.linalg.norm(V, axis=1)[:, None]; c = U.mean(0)
        if np.linalg.norm(c) < 1e-9: return np.array([0, 0, 1.]), np.pi
        c /= np.linalg.norm(c); return c, np.arccos(np.clip(U @ c, -1, 1)).max()
    if np.any(np.linalg.norm(Pf, axis=1) < 1e-12): return True
    a, ra = cap(Pf); b, rb = cap(Tf)
    return np.arccos(np.clip(a @ b, -1, 1)) <= ra + rb + 1e-9
def vol_in(piece, cones):
    """exact volume of convex piece (exact corners) inside the star solid given by exact cones"""
    pp = planes_of(piece); Pf = np.array([fl(p) for p in piece]); t = Z
    for T, cp, Tf in cones:
        if not ang_overlap(Pf, Tf): continue
        C = intersect(pp + cp)
        if C: t = qa(t, volume(C))
    return t
