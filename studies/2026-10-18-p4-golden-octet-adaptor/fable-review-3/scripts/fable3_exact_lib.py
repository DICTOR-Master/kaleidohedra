# Fable review 3 (2026-10-18): shared exact helpers (same code as the helper block of fable3_exact.py): facet polygons, exact areas,
# 2D polygon distances, 48 cube operations, symmetry test, sequential convex decomposition, adjacency components, dihedral angles.
import sys, os, itertools, math, functools
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fable3_engine import f3, Poly, same_plane
from q5 import q, qs_, qa, qs, qm, qn, qr, qd, qinv, qf, sgn, vadd, vsub, vmul, dot, cross, det3, PHI, ONE, Z
def qsum(xs): return functools.reduce(qa, xs, Z)
def qabs(x): return x if sgn(x) >= 0 else qn(x)
def rank_pts(P):
    if len(P) < 2: return 0
    D = [vsub(p, P[0]) for p in P[1:]]; r = 0; basis = []
    for v in D:
        if all(x == Z for x in v): continue
        if not basis: basis = [v]; r = 1; continue
        if r == 1:
            if any(x != Z for x in cross(basis[0], v)): basis.append(v); r = 2
            continue
        if r == 2 and det3(basis[0], basis[1], v) != Z: return 3
    return r
def tight(P, name=''):
    keep = []
    for n, d in P.planes:
        on = [c for c in P.corners if dot(n, c) == d]
        if len(on) >= 3 and rank_pts(on) == 2 and not any(same_plane((n, d), k) for k in keep): keep.append((n, d))
    return Poly(keep, P.corners, name or P.name)
def face_polygon(P, plane):
    n, d = plane; on = [c for c in P.corners if dot(n, c) == d]
    if len(on) < 3 or rank_pts(on) != 2: return []
    return poly_order(on, n)
def poly_order(pts, n):
    cf = np.array([f3(p) for p in pts]); cen = cf.mean(0); nf = f3(n); u = cf[0] - cen; u = u - nf * (u @ nf) / (nf @ nf); w = np.cross(nf, u)
    order = np.argsort(np.arctan2((cf - cen) @ w, (cf - cen) @ u)); return [pts[i] for i in order]
def polygon_area(poly, n):
    S = [Z, Z, Z]
    for i in range(len(poly)): S = vadd(S, cross(poly[i], poly[(i + 1) % len(poly)]))
    nn = dot(n, n); lam = qd(dot(S, n), nn)
    assert all(x == Z for x in vsub(S, vmul(n, lam))), 'polygon not planar'
    return qabs(lam), nn
def area_float(lam, nn): return qf(lam) * math.sqrt(qf(nn)) / 2
def cos_angle(u, w):
    uw = dot(u, w); deg = math.degrees(math.acos(max(-1, min(1, qf(uw) / math.sqrt(qf(dot(u, u)) * qf(dot(w, w)))))))
    return round(deg, 4)
def seg_dist2(p, a, b):
    ab = vsub(b, a); ap = vsub(p, a); t = qd(dot(ap, ab), dot(ab, ab))
    if sgn(t) < 0: t = Z
    if sgn(qs(t, ONE)) > 0: t = ONE
    d = vsub(ap, vmul(ab, t)); return dot(d, d)
def polys_min_dist2(P, Q, n):
    P = poly_order(P, n); Q = poly_order(Q, n); best = None
    for A, B in ((P, Q), (Q, P)):
        for p in A:
            for i in range(len(B)):
                d2 = seg_dist2(p, B[i], B[(i + 1) % len(B)])
                if best is None or sgn(qs(d2, best)) < 0: best = d2
    return best
sign_sets = list(itertools.product([1, -1], repeat=3))
SP = [np.array(Pm) * np.array(s)[:, None] for Pm in itertools.permutations(np.eye(3, dtype=int)) for s in sign_sets]
def qmat(M): return [[qr(int(M[i][j])) for j in range(3)] for i in range(3)]
def apply_lin(M, v): return [dot(M[i], v) for i in range(3)]
def map_planes_about(P, M, m):
    Mm = apply_lin(M, m); t = vsub(m, Mm); return [(apply_lin(M, n), qa(d, dot(apply_lin(M, n), t))) for n, d in P]
def plane_set_equal(A, B): return len(A) == len(B) and all(any(same_plane(a, b) for b in B) for a in A)
def sym_test(centre, bite_list, Kplanes):
    res = dict(proper=0, improper=0)
    for M in SP:
        Mq = qmat(M); det = int(round(np.linalg.det(M)))
        if not plane_set_equal(map_planes_about(Kplanes, Mq, centre), Kplanes): continue
        ok = all(any(plane_set_equal(map_planes_about(E.planes, Mq, centre), E2.planes) for c2, E2, X2 in bite_list) for c, E, X in bite_list)
        if ok: res['proper' if det > 0 else 'improper'] += 1
    return res


def split_outside(X, E):
    """convex pieces of X - E (interior-disjoint, exact): beyond face i and not beyond faces j < i; faces with nothing beyond are skipped"""
    pieces = []; done = []
    for n, d in E.planes:
        if not any(sgn(qs(dot(n, c), d)) > 0 for c in X.corners): continue
        Y = Poly(X.planes + [([qn(x) for x in n], qn(d))] + done, name='c')
        if Y.corners and Y.vol != Z: pieces.append(tight(Y))
        done.append((n, d))
    return pieces
def adjacent(A, B):
    for pa in A.planes:
        for pb in B.planes:
            if same_plane(pa, ([qn(x) for x in pb[0]], qn(pb[1]))):
                X = Poly(A.planes + B.planes, name='f'); return len(X.corners) >= 3 and rank_pts(X.corners) == 2
    return False
def components(cells):
    n = len(cells); parent = list(range(n))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    cen = [X.centre_radius() for X in cells]
    for i, j in itertools.combinations(range(n), 2):
        if np.linalg.norm(cen[i][0] - cen[j][0]) > cen[i][1] + cen[j][1] + 1e-6: continue
        if find(i) != find(j) and adjacent(cells[i], cells[j]): parent[find(i)] = find(j)
    return len({find(i) for i in range(n)})
def dihedrals(edges, all_faces):
    """exact interior dihedral angle at every edge; all_faces = [(outward plane, ordered polygon or None for a cut face)]"""
    dihed = {}; sharp = []
    for e in edges:
        p, qq = [list(x) for x in e]; fs = []
        for pl, poly in all_faces:
            n, d = pl
            if dot(n, p) == d and dot(n, qq) == d and (poly is None or (tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly})):
                if not any(same_plane(pl, g) for g in fs): fs.append(pl)
        if len(fs) != 2: dihed['edge_with_%d_faces' % len(fs)] = dihed.get('edge_with_%d_faces' % len(fs), 0) + 1; continue
        (n1, d1), (n2, d2) = fs; deg = cos_angle(n1, n2); tests = []
        for pl_, poly_ in [(pl, poly) for pl, poly in all_faces if pl in fs and poly is not None and tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly}]:
            pl_other = [f for f in fs if f != pl_][0]; tests.append(all(sgn(qs(pl_other[1], dot(pl_other[0], x))) >= 0 for x in poly_))
        if len(set(tests)) > 1: dihed['inconsistent'] = dihed.get('inconsistent', 0) + 1; continue
        convex = tests[0] if tests else True
        ang = round(180 - deg if convex else 180 + deg, 2); dihed[ang] = dihed.get(ang, 0) + 1
        if ang < 90: sharp.append((ang, round(math.sqrt(qf(dot(vsub(p, qq), vsub(p, qq)))), 5)))
    return dihed, sharp
def dist_point_convex(p, P):
    pf = f3(p); best = np.inf
    for pl in P.planes:
        poly = face_polygon(P, pl)
        if not poly: continue
        Q = np.array([f3(x) for x in poly]); nf = f3(pl[0]); nf = nf / np.linalg.norm(nf); foot = pf - ((pf - Q[0]) @ nf) * nf
        inside = all(np.cross(Q[(i + 1) % len(Q)] - Q[i], foot - Q[i]) @ nf >= -1e-12 for i in range(len(Q)))
        if inside: best = min(best, abs((pf - Q[0]) @ nf))
        for i in range(len(Q)):
            a, b = Q[i], Q[(i + 1) % len(Q)]; t = np.clip((pf - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1); best = min(best, np.linalg.norm(pf - a - t * (b - a)))
    return float(best)
