# Fable review 2 (2026-10-18) of the OCD octet study, steps 21-27 (golden envelopes, outer corners, vertex cuboctahedron, plane trick,
# two-shape kit). INDEPENDENT exact verification in Q(sqrt5) with the engine of fable-review (fable2_engine.py). Light: runs on the Pi.
# Output: data/fable2-exact.json (all checks), stdout log.
import sys, os, json, itertools, time, math, functools
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fable2_engine import *
from fable2_engine import OUT, STUDY, loadS, f3, qv, qstr, Poly, hull_poly, intersect, enumerate_corners, exact_volume, same_plane, solve3
from q5 import q, qs_, qa, qs, qm, qn, qr, qd, qinv, qf, sgn, vadd, vsub, vmul, dot, cross, det3, PHI, ONE, Z, MARK
t0 = time.time(); CH = {}
def log(*a): print(round(time.time() - t0, 1), 's |', *a, flush=True)
def qsum(xs): return functools.reduce(qa, xs, Z)
def qabs(x): return x if sgn(x) >= 0 else qn(x)
def qsqrt(x):
    """exact square root in Q(sqrt5) if it exists, else None"""
    a, b = x
    def frsqrt(r):
        if r < 0: return None
        n, d = r.numerator, r.denominator; sn, sd = math.isqrt(n), math.isqrt(d)
        return Fr(sn, sd) if sn * sn == n and sd * sd == d else None
    if b == 0:
        c = frsqrt(a)
        if c is not None: return (c, Fr(0))
        d_ = frsqrt(a / 5)
        return (Fr(0), d_) if d_ is not None else None
    disc = frsqrt(a * a - 5 * b * b)
    if disc is None: return None
    for c2 in ((a + disc) / 2, (a - disc) / 2):
        c = frsqrt(c2)
        if c is not None and c != 0:
            d_ = b / (2 * c); cand = (c, d_)
            if qm(cand, cand) == x: return cand if qf(cand) > 0 else qn(cand)
    return None
def rank_pts(P):
    """exact affine rank of a point list (0 for a point, 1 line, 2 plane, 3 solid)"""
    if len(P) < 2: return 0
    D = [vsub(p, P[0]) for p in P[1:]]
    r = 0; basis = []
    for v in D:
        if all(x == Z for x in v): continue
        if not basis: basis = [v]; r = 1; continue
        if r == 1:
            if any(x != Z for x in cross(basis[0], v)): basis.append(v); r = 2
            continue
        if r == 2:
            if det3(basis[0], basis[1], v) != Z: return 3
    return r
def tight(P, name=''):
    """drop planes that carry no facet (fewer than 3 non-collinear corners); exact"""
    keep = []
    for n, d in P.planes:
        on = [c for c in P.corners if dot(n, c) == d]
        if len(on) >= 3 and rank_pts(on) == 2 and not any(same_plane((n, d), k) for k in keep): keep.append((n, d))
    return Poly(keep, P.corners, name or P.name)
def face_polygon(P, plane):
    """exact corners of the facet of P in the given plane (ordered by float angle); [] if not a facet"""
    n, d = plane; on = [c for c in P.corners if dot(n, c) == d]
    if len(on) < 3 or rank_pts(on) != 2: return []
    cf = np.array([f3(c) for c in on]); cen = cf.mean(0); nf = f3(n); u = cf[0] - cen; u -= nf * (u @ nf) / (nf @ nf); w = np.cross(nf, u)
    order = np.argsort(np.arctan2((cf - cen) @ w, (cf - cen) @ u))
    return [on[i] for i in order]
def polygon_area(poly, n):
    """exact area of a planar convex polygon with corners ordered round, plane normal n: returns (lambda, n.n) with area = |lambda| sqrt(n.n) / 2"""
    S = [Z, Z, Z]
    for i in range(len(poly)): S = vadd(S, cross(poly[i], poly[(i + 1) % len(poly)]))
    nn = dot(n, n); lam = qd(dot(S, n), nn)
    assert all(x == Z for x in vsub(S, vmul(n, lam))), 'polygon not planar / not perpendicular to n'
    return qabs(lam), nn
def area_float(lam, nn): return qf(lam) * math.sqrt(qf(nn)) / 2
def area_exact_str(lam, nn):
    r = qsqrt(nn)
    return qs_(qm(lam, qm(r, qr(Fr(1, 2))))) if r is not None else f'({qs_(qm(lam, qr(Fr(1, 2))))})*sqrt({qs_(nn)})'
def cos_angle(u, w):
    """exact cos^2 with sign, and float degrees"""
    uw = dot(u, w); c2 = qd(qm(uw, uw), qm(dot(u, u), dot(w, w)))
    deg = math.degrees(math.acos(max(-1, min(1, qf(uw) / math.sqrt(qf(dot(u, u)) * qf(dot(w, w)))))))
    return c2, sgn(uw), round(deg, 4)
sign_sets = list(itertools.product([1, -1], repeat=3))
SP = [np.array(Pm) * np.array(s)[:, None] for Pm in itertools.permutations(np.eye(3, dtype=int)) for s in sign_sets]   # 48 signed permutations
def qmat(M): return [[qr(int(M[i][j])) for j in range(3)] for i in range(3)]
def apply_lin(M, v): return [dot(M[i], v) for i in range(3)]
def map_planes_about(P, M, m):
    """planes of the image of P under x -> M (x - m) + m (M exact orthogonal integer matrix): n.x <= d  ->  (M n).(x) <= d + (M n).(m - M m)"""
    Mm = apply_lin(M, m); t = vsub(m, Mm)
    return [(apply_lin(M, n), qa(d, dot(apply_lin(M, n), t))) for n, d in P]
def plane_set_equal(A, B):
    return len(A) == len(B) and all(any(same_plane(a, b) for b in B) for a in A)

# ------------------------------------------------------------------ frame and envelope, rebuilt from the sources
S1 = loadS('step1-ocd-exact.json'); R = q(S1['R']); assert R == qm(qr(Fr(2, 3)), PHI)
G = json.load(open(os.path.join(STUDY, '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json'))); RTpts = [qv(v) for v in G['RT']]
RT = hull_poly(RTpts, 'RT'); assert len(RT.planes) == 30 and len(RT.corners) == 32
s = qd(R, qm(PHI, PHI))                                     # R / phi^2 = 2/(3 phi)
twothirds = qr(Fr(2, 3)); assert qa(twothirds, s) == R, 'R = 2/3 + R/phi^2'
CH['frame'] = dict(R=qstr(R), s_equals_R_over_phi2=qstr(s), R_equals_2over3_plus_s=True)
# RT facts: inradius 2/3 on every face, normal classes, vertex classes
inr = {qs_(qd(qm(d, d), dot(n, n))) for n, d in RT.planes}; CH['RT_inradius_squared_all_faces'] = sorted(inr)
assert inr == {qs_(qr(Fr(4, 9)))}
def nclass(n):
    nz = [x for x in n if x != Z]
    if len(nz) == 1: return 'axis'
    return 'oblique'
CH['RT_face_normal_classes'] = {k: sum(1 for n, d in RT.planes if nclass(n) == k) for k in ('axis', 'oblique')}
# oblique normals are (1, phi, 1/phi)-cyclic up to scale and sign: check |n|^2 ratios -> components squared in ratio 1 : phi^2 : phi^-2
def oblique_ok(n):
    a = sorted([qd(qm(x, x), dot(n, n)) for x in n], key=qf); return a == [qr(Fr(1, 4)) if False else qd(qm(qinv(PHI), qinv(PHI)), qr(4)), qr(Fr(1, 4)), qd(qm(PHI, PHI), qr(4))]
CH['RT_oblique_normals_are_1_phi_invphi'] = all(oblique_ok(n) for n, d in RT.planes if nclass(n) == 'oblique')
r2 = sorted({qs_(dot(v, v)) for v in RT.corners}, key=lambda x: qf(q(x))); CH['RT_vertex_radii_squared'] = r2
r3sq = qm(qr(3), qm(s, s)); r5sq = qm(qa(ONE, qm(PHI, PHI)), qm(s, s))
CH['RT_vertex_radii_identified'] = dict(threefold_3s2=qs_(r3sq), fivefold_1plusphi2_s2=qs_(r5sq), match=sorted([qs_(r3sq), qs_(r5sq)], key=lambda x: qf(q(x))) == r2)
CH['RT_vol'] = qstr(RT.vol); assert RT.vol == q('-320/27|160/27')
L = [[R, R, Z], [R, Z, R], [Z, R, R]]; cell = det3(*L); cell = qabs(cell); CH['cell'] = qstr(cell)
R3 = qm(R, qm(R, R)); CH['cell_equals_2R3'] = cell == qm(qr(2), R3)
phi6 = qm(qm(PHI, PHI), qm(qm(PHI, PHI), qm(PHI, PHI)))
CH['envelope_share_exact'] = qstr(qd(RT.vol, cell)); CH['envelope_share_is_10_over_phi6'] = qd(RT.vol, cell) == qd(qr(10), phi6) and qd(RT.vol, cell) == q('90|-40')
def lattice_pts(nmax):
    for ijk in itertools.product(range(-nmax, nmax + 1), repeat=3):
        t = [Z, Z, Z]
        for c, Lv in zip(ijk, L): t = vadd(t, vmul(Lv, qr(c)))
        yield t
r5 = math.sqrt(qf(r5sq)); CH['RT_circumradius_float'] = r5
log('setup done; RT planes', len(RT.planes))

# ------------------------------------------------------------------ step 21: envelopes pairwise interior-disjoint; exact gap to the nearest neighbours
centres = [t for t in lattice_pts(2) if 0 < np.linalg.norm(f3(t)) < 2 * r5 + 1e-6]
ov = {}
for c in centres:
    v = intersect(RT, RT.shifted(c)).vol
    ov[qs_(dot(c, c))] = ov.get(qs_(dot(c, c)), 0) + (1 if v != Z else 0)
CH['envelope_neighbours_tested'] = len(centres); CH['envelope_pairs_with_positive_overlap_by_distance2'] = ov
# nearest neighbour (R,R,0): supporting plane x+y = R for both; the gap. Both RTs are mirror-symmetric in z=0 (an RT mirror plane), so the
# minimum distance is attained in z=0: the two octagonal sections. Exact min distance^2 between the two convex octagons (vertex-edge pairs).
c1 = [R, R, Z]; RT2 = RT.shifted(c1)
sup1 = max((qa(v[0], v[1]) for v in RT.corners), key=qf); sup2 = min((qa(v[0], v[1]) for v in RT2.corners), key=qf)
CH['nn_separating_plane_x_plus_y_eq_R'] = dict(max_RT1=qstr(sup1), min_RT2=qstr(sup2), both_equal_R=sup1 == R and sup2 == R,
                                               RT1_contact_points=[[qs_(x) for x in v] for v in RT.corners if qa(v[0], v[1]) == R],
                                               RT2_contact_points=[[qs_(x) for x in v] for v in RT2.corners if qa(v[0], v[1]) == R])
oct1 = [v for v in RT.corners if v[2] == Z]; oct2 = [v for v in RT2.corners if v[2] == Z]
CH['RT_section_z0_vertices'] = len(oct1)
# no RT edge crosses z=0 properly: every corner has z=0 or the corner set is symmetric and edges join same-side corners -- check via the
# facets: a facet with corners on both strict sides would cross; count such facets
cross_e = 0
for pl in RT.planes:
    fc = face_polygon(RT, pl)
    for i in range(len(fc)):
        if sgn(fc[i][2]) * sgn(fc[(i + 1) % len(fc)][2]) < 0: cross_e += 1
CH['RT_edges_crossing_z0_properly'] = cross_e // 2
def seg_dist2(p, a, b):
    ab = vsub(b, a); ap = vsub(p, a); t = qd(dot(ap, ab), dot(ab, ab))
    if sgn(t) < 0: t = Z
    if sgn(qs(t, ONE)) > 0: t = ONE
    d = vsub(ap, vmul(ab, t)); return dot(d, d)
def poly_order(pts, n):
    """order the corners of a planar CONVEX polygon round its centroid (plane normal n)"""
    cf = np.array([f3(p) for p in pts]); cen = cf.mean(0); nf = f3(n); u = cf[0] - cen; u = u - nf * (u @ nf) / (nf @ nf); w = np.cross(nf, u)
    order = np.argsort(np.arctan2((cf - cen) @ w, (cf - cen) @ u)); return [pts[i] for i in order]
def polys_min_dist2(P, Q, n):
    """exact min distance^2 between two disjoint convex coplanar polygons (attained at a corner-edge pair)"""
    P = poly_order(P, n); Q = poly_order(Q, n); best = None
    for A, B in ((P, Q), (Q, P)):
        for p in A:
            for i in range(len(B)):
                d2 = seg_dist2(p, B[i], B[(i + 1) % len(B)])
                if best is None or sgn(qs(d2, best)) < 0: best = d2
    return best
gap2 = polys_min_dist2(oct1, oct2, [Z, Z, ONE])
CH['nn_envelope_gap_squared'] = qstr(gap2); CH['nn_envelope_gap_float'] = math.sqrt(qf(gap2)); CH['nn_envelope_gap_over_R'] = math.sqrt(qf(gap2)) / qf(R)
# the formula gap = 2 / (3 phi^3 sqrt(phi sqrt5)) : gap^2 = 4 / (9 phi^7 sqrt5) = 4 sqrt5 / (45 phi^7)
phi7 = qm(phi6, PHI); CH['nn_envelope_gap_squared_formula_4sqrt5_over_45phi7'] = gap2 == qd(qm(qr(4), (Fr(0), Fr(1))), qm(qr(45), phi7))
# which pair of features realises it: parallel edges A1B1 and A2B2 in z=0
A1 = [twothirds, s, Z]; B1 = [qd(s, PHI), twothirds, Z]; A2 = vsub(c1, A1); B2 = vsub(c1, B1)
CH['nn_gap_edges'] = dict(A1=[qs_(x) for x in A1], B1=[qs_(x) for x in B1], A1B1_is_RT_edge=rank_pts([A1, B1]) == 1 and sum(1 for pl in RT.planes if dot(pl[0], A1) == pl[1] and dot(pl[0], B1) == pl[1]) == 2,
                          parallel=all(x == Z for x in cross(vsub(B1, A1), vsub(B2, A2))),
                          A2_to_line_A1B1_dist2=qs_(qd(dot(cross(vsub(A2, A1), vsub(B1, A1)), cross(vsub(A2, A1), vsub(B1, A1))), dot(vsub(B1, A1), vsub(B1, A1)))),
                          line_dist2_equals_gap2=qd(dot(cross(vsub(A2, A1), vsub(B1, A1)), cross(vsub(A2, A1), vsub(B1, A1))), dot(vsub(B1, A1), vsub(B1, A1))) == gap2)
log('step 21 checks done; gap', CH['nn_envelope_gap_float'])

# ------------------------------------------------------------------ step 27: the cube regions and the grown piece G
m = [qd(R, qr(2))] * 3                                       # tetrahedron centre = cube centre
K = Poly([([ONE, Z, Z], R), ([qn(ONE), Z, Z], Z), ([Z, ONE, Z], R), ([Z, qn(ONE), Z], Z), ([Z, Z, ONE], R), ([Z, Z, qn(ONE)], Z)], name='cube')
assert len(K.corners) == 8 and K.vol == R3
cube_corners = K.corners; odd = lambda c: sum(1 for x in c if x == R) % 2 == 1
CH['cube_corners_OCD_centres'] = [[qs_(x) for x in c] for c in cube_corners if not odd(c)]; CH['cube_corners_octet_vertices'] = [[qs_(x) for x in c] for c in cube_corners if odd(c)]
# every OCD centre within reach: which envelopes meet the cube (exact volume)?
bites = []
for c in lattice_pts(3):
    if np.linalg.norm(f3(c) - f3(m)) > r5 + math.sqrt(3) / 2 * qf(R) + 1e-6: continue
    E = RT.shifted(c); X = intersect(E, K, 'bite')
    if X.vol != Z: bites.append((c, E, X))
CH['envelopes_meeting_cube'] = [[qs_(x) for x in c] for c, E, X in bites]; CH['envelopes_meeting_cube_count'] = len(bites)
CH['envelopes_meeting_cube_are_its_OCD_corners'] = sorted(tuple(c) for c, E, X in bites) == sorted(tuple(c) for c in cube_corners if not odd(c))
CH['bite_volumes'] = [qstr(X.vol) for c, E, X in bites]; CH['each_bite_is_RT_over_8'] = all(X.vol == qd(RT.vol, qr(8)) for c, E, X in bites)
vG = qs(R3, qsum([X.vol for c, E, X in bites]))
CH['G_vol'] = qstr(vG); CH['G_vol_equals_cube_minus_half_RT'] = vG == qs(R3, qd(RT.vol, qr(2)))
CH['G_vol_equals_1_minus_10phi6_times_cell_over_2'] = vG == qd(qm(qs(ONE, qd(qr(10), phi6)), cell), qr(2))
CH['G_vol_closed_form_176_minus_72sqrt5_over_27'] = vG == q('176/27|-72/27'); CH['G_vol_float'] = qf(vG)
# the T- piece is the point reflection of the T+ piece (exact): the cube at -m has OCD corners -c_k, and RT = -RT
CH['Tminus_piece_is_inversion_exact'] = sorted(tuple(qn(x) for x in c) for c, E, X in bites) == sorted(tuple(c) for c in [[qn(x) for x in cc] for cc in cube_corners if not odd(cc)]) and sorted(tuple(qn(x) for x in v) for v in RT.corners) == sorted(tuple(v) for v in RT.corners)
log('cube/bites done', len(bites))

# exact convex decomposition of G = K - union(bites): sequential split by each envelope's facets
def split_outside(X, E):
    """convex pieces of X - E (interior-disjoint, exact): beyond face i and not beyond faces j < i"""
    pieces = []; done = []
    for n, d in E.planes:
        Y = Poly(X.planes + [([qn(x) for x in n], qn(d))] + done, name='c')
        if Y.corners and Y.vol != Z: pieces.append(tight(Y))
        done.append((n, d))
    return pieces
cells = [K]
for c, E, X in bites:
    new = []
    for X0 in cells:
        if intersect(X0, E).vol == Z: new.append(X0); continue
        new += split_outside(X0, E)
    cells = new
    log('split by envelope at', [round(qf(x), 3) for x in c], '-> cells', len(cells))
CH['G_convex_cells'] = len(cells); vs = qsum([X.vol for X in cells]); CH['G_cells_volume_sum_equals_G'] = vs == vG
# adjacency: two cells share a 2D face iff they have the same plane with opposite orientation and the common polygon has rank 2
def adjacent(A, B):
    for pa in A.planes:
        for pb in B.planes:
            if same_plane(pa, ([qn(x) for x in pb[0]], qn(pb[1]))):
                X = Poly(A.planes + B.planes, name='f')
                return len(X.corners) >= 3 and rank_pts(X.corners) == 2
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
CH['G_connected_components_exact'] = components(cells); log('G connectivity', CH['G_connected_components_exact'])

# faces of G: envelope-face parts (convex) + cube-face parts (square minus bites)
faces = []            # (kind, plane(outward from G), ordered corners, lam, nn)
for c, E, X in bites:
    for n, d in E.planes:
        poly = face_polygon(X, (n, d))
        if poly: faces.append(('envelope', ([qn(x) for x in n], qn(d)), poly, *polygon_area(poly, n)))
env_faces = [f for f in faces if f[0] == 'envelope']
CH['G_envelope_face_parts'] = len(env_faces)
sizes = {}
for kind, pl, poly, lam, nn in env_faces: sizes[len(poly)] = sizes.get(len(poly), 0) + 1
CH['G_envelope_face_parts_by_corner_count'] = sizes
rh_area = None
for pl in RT.planes:
    poly = face_polygon(RT, pl); lam, nn = polygon_area(poly, pl[0]); a = (qs_(lam), qs_(nn))
    rh_area = rh_area or (lam, nn)
    assert area_float(lam, nn) - area_float(*rh_area) < 1e-12
CH['golden_rhombus_area'] = area_exact_str(*rh_area)
quads = [f for f in env_faces if len(f[2]) == 4]; tris = [f for f in env_faces if len(f[2]) == 3]
CH['G_whole_rhombi'] = len(quads); CH['G_whole_rhombi_are_full_golden_rhombi'] = all(abs(area_float(f[3], f[4]) - area_float(*rh_area)) < 1e-12 for f in quads)
CH['G_triangles'] = len(tris); CH['G_triangles_are_quarter_rhombi'] = all(abs(4 * area_float(f[3], f[4]) - area_float(*rh_area)) < 1e-12 for f in tris)
# the triangles: right triangles with legs s and s/phi? exact squared edge lengths
def edge_len2s(poly): return sorted([qs_(dot(vsub(poly[(i + 1) % len(poly)], poly[i]), vsub(poly[(i + 1) % len(poly)], poly[i]))) for i in range(len(poly))], key=lambda x: qf(q(x)))
CH['G_triangle_edge_lengths_squared'] = edge_len2s(tris[0][2]); CH['G_triangle_legs_s_and_s_over_phi'] = sorted([qs_(qm(s, s)), qs_(qm(qd(s, PHI), qd(s, PHI)))], key=lambda x: qf(q(x))) == CH['G_triangle_edge_lengths_squared'][:2]
env_area = sum(area_float(f[3], f[4]) for f in env_faces); CH['G_envelope_face_area_float'] = env_area
CH['G_envelope_area_is_half_RT_surface'] = abs(env_area - 15 * area_float(*rh_area)) < 1e-12
# cube faces: square minus the two bite sections
cube_face_parts = []; face_area_total = Z
for n, d in K.planes:
    sections = []
    for c, E, X in bites:
        poly = face_polygon(X, (n, d))
        if poly: sections.append((poly, *polygon_area(poly, n)))
    a_bites = qsum([lam for poly, lam, nn in sections])          # nn = 1 for cube faces
    assert all(nn == ONE for poly, lam, nn in sections)
    part_area = qs(qm(R, R), qd(a_bites, qr(2)))
    cube_face_parts.append(((n, d), sections, part_area)); face_area_total = qa(face_area_total, part_area)
CH['cube_face_bite_sections_per_face'] = [len(sec) for pl, sec, a in cube_face_parts]
CH['cube_face_section_corner_counts'] = sorted({len(poly) for pl, sec, a in cube_face_parts for poly, lam, nn in sec})
CH['cube_face_part_area_exact'] = qstr(cube_face_parts[0][2]); CH['cube_face_parts_all_equal'] = len({a for pl, sec, a in cube_face_parts}) == 1
A_G = qf(face_area_total) + env_area; CH['G_surface_area_float'] = A_G
CH['G_surface_area_exact'] = f'{qs_(face_area_total)} + 15 golden rhombi ({CH["golden_rhombus_area"]})'
CH['G_sphericity_exact_area'] = math.pi ** (1 / 3) * (6 * qf(vG)) ** (2 / 3) / A_G
CH['RT_sphericity'] = math.pi ** (1 / 3) * (6 * qf(RT.vol)) ** (2 / 3) / (30 * area_float(*rh_area))
# the 10-gon on a cube face: corners and interior angles (exact cosines), neck width between the two bites (exact 2D distance)
pl, sec, a = cube_face_parts[[i for i, (pl, sec, a) in enumerate(cube_face_parts) if pl[0] == [Z, Z, qn(ONE)]][0]]   # face z = 0
sq = [c for c in K.corners if c[2] == Z]
bite_pts = [p for poly, lam, nn in sec for p in poly]
tenagon = [p for p in sq if not any(all(x == y for x, y in zip(p, b)) for b in bite_pts)] + [p for p in bite_pts if not any(all(x == y for x, y in zip(p, c)) for c in sq)]
CH['cube_face_part_corners'] = len(tenagon)
# interior angles of the face part: surviving square corners 90; a bite corner on a square edge gives 180 - bite angle; a bite corner inside the square 360 - bite angle
angs = [90.0] * sum(1 for p in sq if not any(all(x == y for x, y in zip(p, b)) for b in bite_pts))
for poly, lam, nn in sec:
    for i in range(len(poly)):
        p = poly[i]
        if any(all(x == y for x, y in zip(p, c)) for c in sq): continue
        c2, sg, deg = cos_angle(vsub(poly[i - 1], p), vsub(poly[(i + 1) % len(poly)], p))
        on_edge = any(x == Z or x == R for x in p[:2]); angs.append(round(180 - deg if on_edge else 360 - deg, 3))
CH['cube_face_part_interior_angles'] = sorted(angs)
half_golden = math.degrees(math.atan(1 / qf(PHI)))
CH['cube_face_part_angles_named'] = '90 x6, 180+31.72 x2 (= 180 + half golden acute), 180+58.28 x2 (= 270 - 31.72)' if all(abs(a - b) < 1e-2 for a, b in zip(sorted(angs), sorted([90.0] * 6 + [180 + half_golden] * 2 + [270 - half_golden] * 2))) else 'see list'
neck2 = polys_min_dist2(sec[0][0], sec[1][0], [Z, Z, ONE]); CH['cube_face_neck_width_squared'] = qstr(neck2); CH['cube_face_neck_width_float'] = math.sqrt(qf(neck2))
CH['cube_face_neck_equals_envelope_gap'] = neck2 == gap2
# corners and edges of G
corner_set = {}
for kind, pl, poly, lam, nn in env_faces:
    for p in poly: corner_set[tuple(p)] = 1
for p in tenagon: corner_set[tuple(p)] = 1
for pl, sec, a in cube_face_parts:
    for poly, lam, nn in sec:
        for p in poly:
            if not any(all(sgn(qs(d, dot(n, p))) > 0 for n, d in E.planes) for c, E, X in bites): corner_set[tuple(p)] = 1   # the OCD centres are inside their bites, not corners of G
for c in K.corners:
    if odd(c): corner_set[tuple(c)] = 1
CH['G_corners'] = len(corner_set)
edges = set()
for kind, pl, poly, lam, nn in env_faces:
    for i in range(len(poly)): edges.add(frozenset((tuple(poly[i]), tuple(poly[(i + 1) % len(poly)]))))
# cube-edge remnants: from the axis point (2/3 along the edge from the OCD corner) to the octet vertex corner
for c in K.corners:
    if odd(c): continue
    for k in range(3):
        v = list(c); v[k] = R if c[k] == Z else Z; a_ = list(c); a_[k] = twothirds if c[k] == Z else qs(R, twothirds)
        edges.add(frozenset((tuple(a_), tuple(v))))
CH['G_edges'] = len(edges); CH['G_faces'] = len(env_faces) + 6; CH['G_euler_V_minus_E_plus_F'] = CH['G_corners'] - CH['G_edges'] + CH['G_faces']
# dihedral angles of G at every edge: faces = env_faces (outward normals stored) + cube faces (outward normals K.planes)
all_faces = [(pl, poly) for kind, pl, poly, lam, nn in env_faces] + [(pl, None) for pl, sec, a in cube_face_parts]
def faces_at_edge(e):
    p, qq = [list(x) for x in e]; out = []
    for pl, poly in all_faces:
        n, d = pl
        if dot(n, p) == d and dot(n, qq) == d:
            if poly is None or (tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly}): out.append(pl)
    return out
dihed = {}
for e in edges:
    fs = faces_at_edge(e)
    if len(fs) != 2: dihed.setdefault('edge_with_%d_faces' % len(fs), 0); dihed['edge_with_%d_faces' % len(fs)] += 1; continue
    (n1, d1), (n2, d2) = fs; c2, sg, deg = cos_angle(n1, n2); p, qq = [list(x) for x in e]
    # convex edge iff each face lies inside the other face's half-space (exact, on the face polygons); the solid is locally the
    # intersection of the two half-spaces. Reflex iff each face lies outside the other's half-space (locally the union).
    polys = [poly for pl, poly in all_faces if pl in fs and poly is not None]
    if len(polys) == 0: convex = True                                   # two cube faces
    else:
        other = [pl for pl in fs if not any(pl is p2 for p2, poly in all_faces if poly is polys[0])]
        tests = []
        for pl_, poly_ in [(pl, poly) for pl, poly in all_faces if pl in fs and poly is not None and tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly}]:   # two bites can have coplanar faces: keep the polygon that carries this edge
            pl_other = [f for f in fs if f != pl_][0]; tests.append(all(sgn(qs(pl_other[1], dot(pl_other[0], x))) >= 0 for x in poly_))
        if len(set(tests)) != 1:
            CH.setdefault('G_dihedral_inconsistent_edges', []).append(dict(edge=[[qs_(x) for x in p] for p in (p, qq)], planes=[[qs_(x) for x in f[0]] + [qs_(f[1])] for f in fs], tests=tests)); continue
        convex = tests[0]
    ang = round(180 - deg if convex else 180 + deg, 3); dihed[ang] = dihed.get(ang, 0) + 1
CH['G_dihedral_angles_with_multiplicity'] = {str(k): v for k, v in sorted(dihed.items(), key=lambda kv: str(kv[0]))}
# hull of G: cube truncated at the 4 OCD corners by x+y+z = 2/3 -type planes
HG = hull_poly([list(p) for p in corner_set], 'hullG')
CH['hull_G_faces'] = len(HG.planes); CH['hull_G_vol'] = qstr(HG.vol)
trunc = [pl for pl in HG.planes if not any(same_plane(pl, k) for k in K.planes)]
CH['hull_G_truncation_planes'] = [(qs_(pl[0][0]), qs_(pl[0][1]), qs_(pl[0][2]), qs_(pl[1])) for pl in trunc]
def axis_pts(c): return [[(qa(c[k], twothirds) if c[k] == Z else qs(c[k], twothirds)) if k == i else c[k] for k in range(3)] for i in range(3)]
CH['hull_G_truncation_at_2over3_along_edges'] = len(trunc) == 4 and all(any(all(dot(pl[0], p) == pl[1] for p in axis_pts(c)) for pl in trunc) for c in K.corners if not odd(c))
log('G structure done: corners', CH['G_corners'], 'edges', CH['G_edges'], 'faces', CH['G_faces'], 'psi', CH['G_sphericity_exact_area'])

# chirality: all 48 signed permutations about the cube centre m; a map is a symmetry of G iff it maps the set of bites (centre + RT planes) to itself
def sym_test(cube_centre, bite_list, Kplanes):
    res = dict(proper=0, improper=0, proper_list=[], improper_list=[])
    for M in SP:
        Mq = qmat(M); det = int(round(np.linalg.det(M)))
        imgK = map_planes_about(Kplanes, Mq, cube_centre)
        if not plane_set_equal(imgK, Kplanes): continue
        ok = True
        for c, E, X in bite_list:
            img = map_planes_about(E.planes, Mq, cube_centre)
            if not any(plane_set_equal(img, E2.planes) for c2, E2, X2 in bite_list): ok = False; break
        if ok: res['proper' if det > 0 else 'improper'] += 1; res['proper_list' if det > 0 else 'improper_list'].append(M.tolist())
    return res
symG = sym_test(m, bites, K.planes); CH['G_symmetries_of_48_cube_ops'] = dict(proper=symG['proper'], improper=symG['improper'])
CH['G_is_chiral'] = symG['improper'] == 0 and symG['proper'] == 12
symH = sym_test(m, [], HG.planes); CH['hull_G_symmetries'] = dict(proper=symH['proper'], improper=symH['improper'])
# corner-set confirmation: an improper op maps G's corner set onto itself?
cs = sorted(corner_set); impr_corner = 0
for M in SP:
    if int(round(np.linalg.det(M))) > 0: continue
    Mq = qmat(M); Mm = apply_lin(Mq, m); t = vsub(m, Mm)
    img = sorted(tuple(vadd(apply_lin(Mq, list(p)), t)) for p in cs)
    if img == cs: impr_corner += 1
CH['G_improper_ops_preserving_corner_set'] = impr_corner
log('chirality done', CH['G_symmetries_of_48_cube_ops'])

# ------------------------------------------------------------------ step 26: the central cell, from the 12 whole-rhombus planes
whole = [(c, pl) for c, E, X in bites for pl in E.planes if len(face_polygon(X, pl)) == 4]
CH['whole_rhombi_per_envelope'] = {str([round(qf(x), 3) for x in c]): sum(1 for cc, pl in whole if cc == c) for c, E, X in bites}
TP = hull_poly([[R, Z, Z], [Z, R, Z], [Z, Z, R], [R, R, R]], 'T+')
C26 = Poly([([qn(x) for x in n], qn(d)) for c, (n, d) in whole] + TP.planes, name='C26'); C26 = tight(C26)
CH['C26_corners'] = len(C26.corners); CH['C26_faces'] = len(C26.planes); CH['C26_vol'] = qstr(C26.vol)
S26 = loadS('step26-tet-cells.json'); CH['C26_vol_matches_step26'] = qs_(C26.vol) == S26['checks']['summary'][0]['volume']
CH['C26_Tplus_planes_redundant'] = not any(any(same_plane(pl, tp) for tp in TP.planes) for pl in C26.planes)
CH['C26_strictly_inside_Tplus'] = all(all(sgn(qs(d, dot(n, p))) > 0 for n, d in TP.planes) for p in C26.corners)
CH['C26_face_corner_counts'] = sorted(len(face_polygon(C26, pl)) for pl in C26.planes)
cen26 = [qd(qsum([p[k] for p in C26.corners]), qr(len(C26.corners))) for k in range(3)]; CH['C26_centroid_is_cube_centre'] = cen26 == m
CH['C26_inside_G_by_construction'] = 'every point beyond all three whole-rhombus planes of an envelope lies outside that envelope; C26 lies in T+ which lies in the cube'
sym26 = sym_test(m, [], C26.planes); CH['C26_symmetries_of_48'] = dict(proper=sym26['proper'], improper=sym26['improper'])
e26 = {}
for pl in C26.planes:
    poly = face_polygon(C26, pl)
    for i in range(len(poly)):
        e = frozenset((tuple(poly[i]), tuple(poly[(i + 1) % len(poly)]))); l2 = qs_(dot(vsub(poly[i], poly[(i + 1) % len(poly)]), vsub(poly[i], poly[(i + 1) % len(poly)])))
        e26[e] = l2
cls = {}
for e, l2 in e26.items(): cls[l2] = cls.get(l2, 0) + 1
CH['C26_edges'] = len(e26); CH['C26_edge_length_classes_sq_with_multiplicity'] = {k: v for k, v in sorted(cls.items(), key=lambda kv: qf(q(kv[0])))}
CH['C26_edge_lengths_float'] = sorted(math.sqrt(qf(q(k))) for k in cls)
pent = face_polygon(C26, C26.planes[0]); CH['C26_pentagon_edges_in_order'] = [round(math.sqrt(qf(dot(vsub(pent[(i + 1) % 5], pent[i]), vsub(pent[(i + 1) % 5], pent[i])))), 5) for i in range(5)]
CH['C26_pentagon_angles_deg'] = [cos_angle(vsub(pent[i - 1], pent[i]), vsub(pent[(i + 1) % 5], pent[i]))[2] for i in range(5)]
CH['C26_is_tetartoid'] = sym26['proper'] == 12 and sym26['improper'] == 0 and len(cls) == 3 and sorted(cls.values()) == [6, 12, 12]
a26 = sum(area_float(*polygon_area(face_polygon(C26, pl), pl[0])) for pl in C26.planes)
CH['C26_sphericity'] = math.pi ** (1 / 3) * (6 * qf(C26.vol)) ** (2 / 3) / a26; CH['C26_share_of_G'] = qf(C26.vol) / qf(vG)
CH['C26_face_plane_distance_from_centre'] = sorted({qs_(qd(qm(qs(d, dot(n, m)), qs(d, dot(n, m))), dot(n, n))) for n, d in C26.planes})
r26 = sorted({qs_(dot(vsub(p, m), vsub(p, m))) for p in C26.corners}, key=lambda x: qf(q(x))); CH['C26_corner_radii_squared'] = r26
log('C26 done', CH['C26_symmetries_of_48'], CH['C26_edge_length_classes_sq_with_multiplicity'])

# ------------------------------------------------------------------ step 24 / 24d: outer corner, pyramid, cuboctahedron, cusps
OCTA = Poly([([qr(a), qr(b), qr(c)], R) for a, b, c in sign_sets], name='octa')
pyr = Poly(OCTA.planes + [([Z, Z, qn(ONE)], qn(twothirds))], name='pyr')
CH['pyramid_vol'] = qstr(pyr.vol); CH['pyramid_is_phi2_corner'] = pyr.vol == qm(qd(OCTA.vol, qr(2)), qd(ONE, qm(phi6, ONE))) and qs(R, twothirds) == s
outer = qd(qs(OCTA.vol, intersect(RT, OCTA).vol), qr(6)); CH['outer_corner_vol'] = qstr(outer); CH['outer_corner_matches_step24'] = outer == q('112/81|-16/27')
CH['pyramid_share_of_outer_corner'] = qf(pyr.vol) / qf(outer)
CH['RT_in_octa_plus_8_keys_equals_RT'] = qa(intersect(RT, OCTA).vol, qm(qr(8), q(loadS('step3-key-candidate.json')['checks']['key_volume']))) == RT.vol
# cusps: the RT vertex (2/3, 0, s) lies on the octahedron edge from (0,0,R) to (R,0,0); the edge meets RT only there
Acands = [v for v in RT.corners if v[1] == Z and qa(v[0], v[2]) == R]; assert len(Acands) == 1; A = Acands[0]
CH['cusp_point'] = [qs_(x) for x in A]; CH['cusp_is_s_0_2over3'] = A == [s, Z, twothirds]
CH['cusp_is_pyramid_base_corner'] = A[2] == twothirds and qa(qabs(A[0]), qabs(A[1])) == s
CH['edge_plane_x_plus_z_eq_R_supports_RT'] = max((qa(v[0], v[2]) for v in RT.corners), key=qf) == R and sum(1 for v in RT.corners if qa(v[0], v[2]) == R) == 1
# solid angle of the outer corner at the cusp (float): fraction of a tiny sphere round A inside octa and outside RT
rng = np.random.default_rng(1); dirs = rng.normal(size=(400000, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]; pts = f3(A) + 1e-4 * dirs
octa_n = np.array([[a, b, c] for a, b, c in sign_sets], float); in_octa = (pts @ octa_n.T <= qf(R) + 1e-15).all(1)
rt_n = np.array([f3(n) for n, d in RT.planes]); rt_d = np.array([qf(d) for n, d in RT.planes]); in_rt = (pts @ rt_n.T <= rt_d + 1e-15).all(1)
CH['outer_corner_solid_angle_at_cusp_sr'] = float((in_octa & ~in_rt).mean() * 4 * math.pi); CH['solid_angle_reference'] = dict(cube_corner=math.pi / 2, regular_tetrahedron_corner=0.5513)
# the two outer corners of the edge both touch A (upper: +z corner; lower: +x corner): points of the edge on either side of A are outside RT
for lab, t in (('towards_+z_corner', qr(Fr(-1, 100))), ('towards_+x_corner', qr(Fr(1, 100)))):
    p = vadd(A, vmul([ONE, Z, qn(ONE)], t)); CH['edge_point_' + lab + '_outside_RT'] = not all(sgn(qs(d, dot(n, p))) >= 0 for n, d in RT.planes)
# vertex cuboctahedron at (R,0,0): hull of v + s*(+-1,+-1,0) perms
v0 = [R, Z, Z]; cpts = []
for perm in ((0, 1), (0, 2), (1, 2)):
    for sa, sb in itertools.product((1, -1), repeat=2):
        p = list(v0); p[perm[0]] = qa(p[perm[0]], qm(s, qr(sa))); p[perm[1]] = qa(p[perm[1]], qm(s, qr(sb))); cpts.append(p)
CUBO = hull_poly(cpts, 'cubo'); CH['cubo_corners'] = len(CUBO.corners); CH['cubo_faces'] = len(CUBO.planes); CH['cubo_vol'] = qstr(CUBO.vol)
CH['cubo_vol_is_RT_over_3'] = CUBO.vol == qd(RT.vol, qr(3)); CH['cubo_vol_is_20_over_3_s3'] = CUBO.vol == qm(qr(Fr(20, 3)), qm(s, qm(s, s)))
cubo_ov = [qstr(intersect(CUBO, RT.shifted(c)).vol) for c in lattice_pts(2) if np.linalg.norm(f3(c) - f3(v0)) < r5 + 0.9]
CH['cubo_overlap_with_each_nearby_envelope'] = sorted(set(cubo_ov)); CH['cubo_outside_all_envelopes'] = all(x.startswith('0|0') for x in cubo_ov)
# face-to-face contact: RT's rhombus x = 2/3 lies inside the cuboctahedron's square face x = 2/3 (the diamond |y|+|z| <= s)
rh = face_polygon(RT, ([ONE, Z, Z], twothirds)); CH['RT_rhombus_x_face_inside_cubo_square'] = all(sgn(qs(s, qa(qabs(p[1]), qabs(p[2])))) >= 0 for p in rh)
CH['cubo_shares_full_rhombus_with_6_envelopes'] = CH['RT_rhombus_x_face_inside_cubo_square']
CH['cubo_sphericity'] = math.pi ** (1 / 3) * (6 * qf(CUBO.vol)) ** (2 / 3) / sum(area_float(*polygon_area(face_polygon(CUBO, pl), pl[0])) for pl in CUBO.planes)
log('step 24 done')

# ------------------------------------------------------------------ improvement W: glue piece centred at the octet vertex (Voronoi cell = fcc rhombic dodecahedron)
# RD of the vertex v0 = (R,0,0): bisector planes to its 12 nearest vertices (R,0,0) + R(+-1,+-1,0)-perms
RDpl = []
for perm in ((0, 1), (0, 2), (1, 2)):
    for sa, sb in itertools.product((1, -1), repeat=2):
        n = [Z, Z, Z]; n[perm[0]] = qr(sa); n[perm[1]] = qr(sb); RDpl.append((n, qa(dot(n, v0), R)))      # n.(x - v0) <= R  (|n|^2 = 2, half-distance R/sqrt2)
RD = Poly(RDpl, name='RD'); CH['RD_corners'] = len(RD.corners); CH['RD_vol'] = qstr(RD.vol); CH['RD_vol_equals_cell'] = RD.vol == cell
CH['RD_4valent_corners_are_OCD_centres'] = sorted(tuple(c) for c in RD.corners if sum(1 for pl in RD.planes if dot(pl[0], c) == pl[1]) == 4) == sorted(tuple(vadd(v0, vmul([ONE if i == k else Z for i in range(3)], qm(R, qr(sg))))) for k in range(3) for sg in (1, -1))
CH['RD_3valent_corners_are_tet_sites'] = all(all(qabs(qs(x, v0[i])) == qd(R, qr(2)) for i, x in enumerate(c)) for c in RD.corners if sum(1 for pl in RD.planes if dot(pl[0], c) == pl[1]) == 3)
wb = []
for c in lattice_pts(3):
    if np.linalg.norm(f3(c) - f3(v0)) > r5 + qf(R) + 1e-6: continue
    E = RT.shifted(c); X = intersect(E, RD, 'wbite')
    if X.vol != Z: wb.append((c, E, X))
CH['W_bites'] = len(wb); CH['W_bites_each_RT_over_6'] = all(X.vol == qd(RT.vol, qr(6)) for c, E, X in wb)
vW = qs(RD.vol, qsum([X.vol for c, E, X in wb])); CH['W_vol'] = qstr(vW); CH['W_vol_equals_cell_minus_RT'] = vW == qs(cell, RT.vol); CH['W_vol_equals_2G'] = vW == qm(qr(2), vG); CH['W_vol_float'] = qf(vW)
# cuboctahedron inside W
CH['cubo_inside_RD'] = all(all(sgn(qs(d, dot(n, p))) >= 0 for n, d in RD.planes) for p in CUBO.corners)
# faces of W
wfaces = []
for c, E, X in wb:
    for n, d in E.planes:
        poly = face_polygon(X, (n, d))
        if poly: wfaces.append(('envelope', ([qn(x) for x in n], qn(d)), poly, *polygon_area(poly, n)))
CH['W_envelope_face_parts'] = len(wfaces); wsz = {}
for kind, pl, poly, lam, nn in wfaces: wsz[len(poly)] = wsz.get(len(poly), 0) + 1
CH['W_envelope_face_parts_by_corner_count'] = wsz
w_env_area = sum(area_float(f[3], f[4]) for f in wfaces); CH['W_envelope_area_is_one_RT_surface'] = abs(w_env_area - 30 * area_float(*rh_area)) < 1e-12
w_whole = sum(1 for f in wfaces if abs(area_float(f[3], f[4]) - area_float(*rh_area)) < 1e-12); CH['W_whole_rhombi'] = w_whole
rd_parts = []; w_rd_area = 0.0; necks = []
for n, d in RD.planes:
    full = face_polygon(RD, (n, d)); lam, nn = polygon_area(full, n); a = area_float(lam, nn); secs = []
    for c, E, X in wb:
        poly = face_polygon(X, (n, d))
        if poly: secs.append(poly); a -= area_float(*polygon_area(poly, n))
    rd_parts.append((len(secs), a)); w_rd_area += a
    if len(secs) == 2: necks.append(polys_min_dist2(secs[0], secs[1], n))
CH['W_RD_face_bite_sections'] = sorted(k for k, a in rd_parts); CH['W_RD_face_part_area_float'] = rd_parts[0][1]
CH['W_RD_face_neck_width_float'] = sorted({round(math.sqrt(qf(x)), 6) for x in necks}); CH['W_RD_face_neck_squared'] = sorted({qs_(x) for x in necks})
A_W = w_rd_area + w_env_area; CH['W_surface_area_float'] = A_W; CH['W_sphericity_exact_area'] = math.pi ** (1 / 3) * (6 * qf(vW)) ** (2 / 3) / A_W
# W corners / edges / faces
wcorners = {}
for kind, pl, poly, lam, nn in wfaces:
    for p in poly: wcorners[tuple(p)] = 1
for c in RD.corners:
    if sum(1 for pl in RD.planes if dot(pl[0], c) == pl[1]) == 3: wcorners[tuple(c)] = 1
wedges = set()
for kind, pl, poly, lam, nn in wfaces:
    for i in range(len(poly)): wedges.add(frozenset((tuple(poly[i]), tuple(poly[(i + 1) % len(poly)]))))
# RD-edge remnants: each RD edge joins a 4-valent corner (OCD centre, inside a bite) to a 3-valent corner; remnant from the RT exit point to the 3-valent corner
rd_edges = set()
for pl1, pl2 in itertools.combinations(RD.planes, 2):
    on = [c for c in RD.corners if dot(pl1[0], c) == pl1[1] and dot(pl2[0], c) == pl2[1]]
    if len(on) == 2: rd_edges.add(frozenset(tuple(c) for c in on))
CH['RD_edges'] = len(rd_edges)
for e in rd_edges:
    a_, b_ = [list(x) for x in e]
    if sum(1 for pl in RD.planes if dot(pl[0], a_) == pl[1]) == 3: a_, b_ = b_, a_          # a_ = 4-valent (OCD centre)
    E = [EE for c, EE, X in wb if c == a_][0]
    # exit point: the edge leaves RT where some RT plane is met: t = min over planes of (d - n.a)/(n.(b-a)) with n.(b-a) > 0
    dirv = vsub(b_, a_); ts = [qd(qs(d, dot(n, a_)), dot(n, dirv)) for n, d in E.planes if sgn(dot(n, dirv)) > 0]; t = min(ts, key=qf)
    ex = vadd(a_, vmul(dirv, t)); wcorners[tuple(ex)] = 1; wedges.add(frozenset((tuple(ex), tuple(b_))))
CH['W_corners'] = len(wcorners); CH['W_edges'] = len(wedges); CH['W_faces'] = len(wfaces) + 12; CH['W_euler'] = CH['W_corners'] - CH['W_edges'] + CH['W_faces']
# W connectivity (exact decomposition) and symmetry
wcells = [RD]
for c, E, X in wb:
    new = []
    for X0 in wcells:
        if intersect(X0, E).vol == Z: new.append(X0); continue
        new += split_outside(X0, E)
    wcells = new
CH['W_convex_cells'] = len(wcells); CH['W_cells_volume_sum_equals_W'] = qsum([X.vol for X in wcells]) == vW
CH['W_connected_components_exact'] = components(wcells)
symW = sym_test(v0, wb, RD.planes); CH['W_symmetries_of_48_cube_ops'] = dict(proper=symW['proper'], improper=symW['improper']); CH['W_is_achiral'] = symW['improper'] > 0
# W dihedral angles
wall = [(pl, poly) for kind, pl, poly, lam, nn in wfaces] + [(pl, None) for pl in RD.planes]
wd = {}
for e in wedges:
    p, qq = [list(x) for x in e]; fs = []
    for pl, poly in wall:
        n, d = pl
        if dot(n, p) == d and dot(n, qq) == d and (poly is None or (tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly})): fs.append(pl)
    if len(fs) != 2: wd['edge_with_%d_faces' % len(fs)] = wd.get('edge_with_%d_faces' % len(fs), 0) + 1; continue
    (n1, d1), (n2, d2) = fs; c2, sg, deg = cos_angle(n1, n2)
    tests = []
    for pl_, poly_ in [(pl, poly) for pl, poly in wall if pl in fs and poly is not None and tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly}]:
        pl_other = [f for f in fs if f != pl_][0]; tests.append(all(sgn(qs(pl_other[1], dot(pl_other[0], x))) >= 0 for x in poly_))
    if len(set(tests)) > 1:
        CH.setdefault('W_dihedral_inconsistent_edges', []).append(dict(edge=[[qs_(x) for x in p] for p in (p, qq)], tests=tests)); continue
    convex = tests[0] if tests else True
    ang = round(180 - deg if convex else 180 + deg, 3); wd[ang] = wd.get(ang, 0) + 1
CH['W_dihedral_angles_with_multiplicity'] = {str(k): v for k, v in sorted(wd.items(), key=lambda kv: str(kv[0]))}
log('W done: vol', qf(vW), 'psi', CH['W_sphericity_exact_area'], 'components', CH['W_connected_components_exact'], 'sym', CH['W_symmetries_of_48_cube_ops'])

def dist_point_convex(p, P):
    pf = f3(p); best = np.inf
    for pl in P.planes:
        poly = face_polygon(P, pl)
        if not poly: continue
        Q = np.array([f3(x) for x in poly]); nf = f3(pl[0]); nf = nf / np.linalg.norm(nf)
        foot = pf - ((pf - Q[0]) @ nf) * nf
        # inside the convex polygon? (all cross products same sign)
        inside = True
        for i in range(len(Q)):
            a, b = Q[i], Q[(i + 1) % len(Q)]
            if np.cross(b - a, foot - a) @ nf < -1e-12: inside = False; break
        if inside: best = min(best, abs((pf - Q[0]) @ nf))
        for i in range(len(Q)):
            a, b = Q[i], Q[(i + 1) % len(Q)]; t = np.clip((pf - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1); best = min(best, np.linalg.norm(pf - a - t * (b - a)))
    return float(best)
CH['G_centre_distance_to_bites_float'] = min(dist_point_convex(m, E) for c, E, X in bites); CH['G_centre_distance_to_cube_faces_float'] = qf(R) / 2
CH['G_inscribed_ball_at_centre_float'] = min(CH['G_centre_distance_to_bites_float'], CH['G_centre_distance_to_cube_faces_float'])
CH['W_centre_distance_to_bites_float'] = min(dist_point_convex(v0, E) for c, E, X in wb); CH['W_centre_distance_to_RD_faces_float'] = qf(R) / math.sqrt(2)
CH['W_inscribed_ball_at_centre_float'] = min(CH['W_centre_distance_to_bites_float'], CH['W_centre_distance_to_RD_faces_float'])
CH['C26_inradius_exact'] = qs_(qd(s, qr(2))) + ' = s/2 = R/(2 phi^2)' if CH['C26_face_plane_distance_from_centre'] == [qs_(qm(qd(s, qr(2)), qd(s, qr(2))))] else 'see C26_face_plane_distance_from_centre'
CH['G_corner_list'] = sorted([qs_(x) for x in p] for p in corner_set)
CH['C26_corner_list'] = sorted([qs_(x) for x in p] for p in C26.corners)
CH['seconds'] = round(time.time() - t0, 1)
json.dump(dict(mark=MARK, review='Fable review 2, 2026-10-18: exact verification of steps 21-27 (two-shape kit) in Q(sqrt5)', prescreen_tolerance=TOL_PRESCREEN, checks=CH),
          open(os.path.join(OUT, 'fable2-exact.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(CH, indent=1, ensure_ascii=False, default=str)); log('done')
