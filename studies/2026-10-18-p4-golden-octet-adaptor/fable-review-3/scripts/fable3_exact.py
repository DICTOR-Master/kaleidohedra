# Fable review 3 (2026-10-18): OCD + W_OCD. W_OCD = fcc rhombic dodecahedron round the octet vertex v0 = (0,0,R) minus the 6 OCDs biting
# into it (p4 step 6). INDEPENDENT exact verification in Q(sqrt5) with the engine of the earlier reviews (fable3_engine.py):
# tiling (which OCDs meet the RD, exact bite volumes, total), connectivity (exact convex decomposition + adjacency), symmetry group
# (48 cube ops about v0), faces / corners / edges / dihedral angles, necks, OCD-OCD gap, inscribed ball, buildability at 60 mm edge.
# Output: data/fable3-exact.json. Light enough for the Pi.
import sys, os, json, itertools, time, math, functools
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fable3_engine import *
from fable3_engine import OUT, STUDY, loadS, f3, qv, qstr, Poly, hull_poly, intersect, enumerate_corners, exact_volume, same_plane, solve3
from q5 import q, qs_, qa, qs, qm, qn, qr, qd, qinv, qf, sgn, vadd, vsub, vmul, dot, cross, det3, PHI, ONE, Z, MARK
t0 = time.time(); CH = {}
def log(*a): print(round(time.time() - t0, 1), 's |', *a, flush=True)
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

# ------------------------------------------------------------------ OCD, frame
S1 = loadS('step1-ocd-exact.json'); V = [qv(v) for v in S1['V']]; R = q(S1['R']); assert R == qm(qr(Fr(2, 3)), PHI)
OCD = hull_poly(V, 'OCD'); assert len(OCD.planes) == 80 and len(OCD.corners) == 102
L = [[R, R, Z], [R, Z, R], [Z, R, R]]; cell = qabs(det3(*L)); CH['cell'] = qstr(cell); CH['OCD_vol'] = qstr(OCD.vol)
CH['OCD_symmetry_of_48_cube_ops_about_centre'] = sym_test([Z, Z, Z], [], OCD.planes)
fsz = {}
for pl in OCD.planes: k = len(face_polygon(OCD, pl)); fsz[k] = fsz.get(k, 0) + 1
CH['OCD_faces_by_corner_count'] = fsz
r2 = {}
for v in V: r2[qs_(dot(v, v))] = r2.get(qs_(dot(v, v)), 0) + 1
CH['OCD_corner_radii_squared_with_multiplicity'] = {k: v for k, v in sorted(r2.items(), key=lambda kv: -qf(q(kv[0])))}
rmax = max((dot(v, v) for v in V), key=qf); five = [v for v in V if dot(v, v) == rmax]; CH['OCD_outermost_corners'] = len(five)
CH['OCD_outermost_corner_example'] = [qs_(x) for x in five[0]]; CH['OCD_outermost_radius_float'] = math.sqrt(qf(rmax))
CH['OCD_outermost_on_2fold_axes_toward_octa_edge_midpoints'] = all(sum(1 for x in v if x == Z) == 1 and len({qs_(qabs(x)) for x in v if x != Z}) == 1 for v in five)
CH['octa_edge_midpoint_radius_float'] = qf(R) / math.sqrt(2); CH['octa_inradius_float'] = qf(R) / math.sqrt(3)
inr = min((qd(qm(d, d), dot(n, n)) for n, d in OCD.planes), key=qf); CH['OCD_inradius_float'] = math.sqrt(qf(inr))
def lattice_pts(nmax):
    for ijk in itertools.product(range(-nmax, nmax + 1), repeat=3):
        t = [Z, Z, Z]
        for c, Lv in zip(ijk, L): t = vadd(t, vmul(Lv, qr(c)))
        yield t
rO = math.sqrt(qf(rmax))
# ------------------------------------------------------------------ RD at the vertex v0 = (0,0,R)
v0 = [Z, Z, R]; RDpl = []
for perm in ((0, 1), (0, 2), (1, 2)):
    for sa, sb in itertools.product((1, -1), repeat=2):
        n = [Z, Z, Z]; n[perm[0]] = qr(sa); n[perm[1]] = qr(sb); RDpl.append((n, qa(dot(n, v0), R)))
RD = Poly(RDpl, name='RD'); CH['RD_corners'] = len(RD.corners); CH['RD_vol_equals_cell'] = RD.vol == cell
# ------------------------------------------------------------------ (1) tiling: which OCDs meet the RD, exact bite volumes
bites = []; tested = 0
for c in lattice_pts(3):
    if np.linalg.norm(f3(c) - f3(v0)) > rO + qf(R) + 1e-6: continue
    tested += 1; E = OCD.shifted(c); X = intersect(E, RD, 'bite')
    if X.vol != Z: bites.append((c, E, X))
CH['OCD_centres_tested'] = tested; CH['OCDs_meeting_RD'] = [[qs_(x) for x in c] for c, E, X in bites]; CH['OCDs_meeting_RD_count'] = len(bites)
CH['OCDs_meeting_RD_are_the_6_at_distance_R'] = sorted(tuple(c) for c, E, X in bites) == sorted(tuple(vadd(v0, vmul([ONE if i == k else Z for i in range(3)], qm(R, qr(sg))))) for k in range(3) for sg in (1, -1))
CH['bite_volumes'] = sorted({qstr(X.vol) for c, E, X in bites}); CH['each_bite_is_OCD_over_6'] = all(X.vol == qd(OCD.vol, qr(6)) for c, E, X in bites)
# bite = OCD & cone (the 4 RD planes at that corner), i.e. the cap region of the earlier reviews: check volume equality with cone & OCD
cone_z = Poly([([ONE, Z, qn(ONE)], Z), ([qn(ONE), Z, qn(ONE)], Z), ([Z, ONE, qn(ONE)], Z), ([Z, qn(ONE), qn(ONE)], Z), ([Z, Z, ONE], R)], name='cone')
CH['bite_equals_OCD_cap_region_volume'] = intersect(OCD, cone_z).vol == qd(OCD.vol, qr(6))
# every OCD lies inside the union of its 6 vertex RDs: sum over the 6 RDs round the OCD at 0 of vol(OCD & RD_v) == OCD
tot = Z
for k in range(3):
    for sg in (1, -1):
        v = [Z, Z, Z]; v[k] = qm(R, qr(sg)); RDv = Poly([(n, qa(dot(n, v), R)) for n, d in RDpl], name='RDv')
        tot = qa(tot, intersect(OCD, RDv).vol)
CH['OCD_split_over_its_6_vertex_RDs_sums_to_OCD'] = tot == OCD.vol
vW = qs(RD.vol, qsum([X.vol for c, E, X in bites])); CH['W_vol'] = qstr(vW); CH['W_vol_equals_cell_minus_OCD'] = vW == qs(cell, OCD.vol)
CH['W_vol_matches_claim_2824_minus_328sqrt5_over_1539'] = vW == q('2824/1539|-328/1539'); CH['W_vol_float'] = qf(vW)
log('tiling done', len(bites), qf(vW))
# ------------------------------------------------------------------ (2) connectivity: exact convex decomposition
def split_outside(X, E):
    pieces = []; done = []
    for n, d in E.planes:
        if not any(sgn(qs(dot(n, c), d)) > 0 for c in X.corners): continue        # no part of X beyond this face
        Y = Poly(X.planes + [([qn(x) for x in n], qn(d))] + done, name='c')
        if Y.corners and Y.vol != Z: pieces.append(tight(Y))
        done.append((n, d))
    return pieces
cells = [RD]
for c, E, X in bites:
    new = []
    for X0 in cells:
        if intersect(X0, E).vol == Z: new.append(X0); continue
        new += split_outside(X0, E)
    cells = new; log('split by OCD at', [round(qf(x), 3) for x in c], '-> cells', len(cells))
CH['W_convex_cells'] = len(cells); CH['W_cells_volume_sum_equals_W'] = qsum([X.vol for X in cells]) == vW
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
CH['W_connected_components_exact'] = components(cells); log('connectivity', CH['W_connected_components_exact'])
# symmetry group
symW = sym_test(v0, bites, RD.planes); CH['W_symmetries_of_48_cube_ops'] = symW; CH['W_is_m3bar_achiral'] = symW == dict(proper=12, improper=12)
# ------------------------------------------------------------------ (3) faces: OCD imprints and RD-face parts
ocd_face_area = {}
for pl in OCD.planes:
    poly = face_polygon(OCD, pl); lam, nn = polygon_area(poly, pl[0]); ocd_face_area[len(poly)] = ocd_face_area.get(len(poly), set()); ocd_face_area[len(poly)].add(round(area_float(lam, nn), 12))
CH['OCD_face_areas_by_corner_count'] = {k: sorted(v) for k, v in ocd_face_area.items()}
faces = []
for c, E, X in bites:
    for n, d in E.planes:
        poly = face_polygon(X, (n, d))
        if poly:
            lam, nn = polygon_area(poly, n); full = face_polygon(E, (n, d)); lamf, nnf = polygon_area(full, n)
            faces.append(dict(kind='imprint', plane=([qn(x) for x in n], qn(d)), poly=poly, lam=lam, nn=nn, whole=lam == lamf, ocd_face_corners=len(full)))
imp = faces
CH['W_imprint_faces'] = len(imp); CH['W_imprint_whole_faces'] = sum(1 for f in imp if f['whole']); CH['W_imprint_cut_faces'] = sum(1 for f in imp if not f['whole'])
bk = {}
for f in imp:
    key = f"{'whole' if f['whole'] else 'cut'} {f['ocd_face_corners']}-gon -> {len(f['poly'])} corners"; bk[key] = bk.get(key, 0) + 1
CH['W_imprint_faces_breakdown'] = dict(sorted(bk.items()))
imp_area = sum(area_float(f['lam'], f['nn']) for f in imp); ocd_area = sum(area_float(*polygon_area(face_polygon(OCD, pl), pl[0])) for pl in OCD.planes)
CH['W_imprint_area_float'] = imp_area; CH['W_imprint_area_equals_one_OCD_surface'] = abs(imp_area - ocd_area) < 1e-10; CH['OCD_surface_area_float'] = ocd_area
# hexagon thirds: the joint hexagons (6-gons on the octahedron faces) are cut by the cone edges through their centres
rd_parts = []; w_rd_area = 0.0; necks = []
for n, d in RD.planes:
    full = face_polygon(RD, (n, d)); lam, nn = polygon_area(full, n); a = area_float(lam, nn); secs = []
    for c, E, X in bites:
        poly = face_polygon(X, (n, d))
        if poly: secs.append(poly); a -= area_float(*polygon_area(poly, n))
    rd_parts.append((len(secs), a, secs)); w_rd_area += a
    if len(secs) == 2: necks.append(polys_min_dist2(secs[0], secs[1], n))
CH['W_RD_face_bite_sections'] = sorted(k for k, a, s in rd_parts); CH['W_RD_face_part_area_float'] = sorted({round(a, 12) for k, a, s in rd_parts})
CH['RD_face_area_float'] = area_float(*polygon_area(face_polygon(RD, RD.planes[0]), RD.planes[0][0]))
CH['W_RD_face_neck_squared'] = sorted({qs_(x) for x in necks}); CH['W_RD_face_neck_float'] = sorted({round(math.sqrt(qf(x)), 9) for x in necks})
CH['W_RD_section_corner_counts'] = sorted({len(p) for k, a, s in rd_parts for p in s})
A_W = w_rd_area + imp_area; CH['W_surface_area_float'] = A_W; CH['W_sphericity'] = math.pi ** (1 / 3) * (6 * qf(vW)) ** (2 / 3) / A_W
CH['OCD_sphericity'] = math.pi ** (1 / 3) * (6 * qf(OCD.vol)) ** (2 / 3) / ocd_area
CH['RD_sphericity'] = math.pi ** (1 / 3) * (6 * qf(RD.vol)) ** (2 / 3) / (12 * CH['RD_face_area_float'])
# corners / edges / Euler
corner_set = {}
for f in imp:
    for p in f['poly']: corner_set[tuple(p)] = 1
for c in RD.corners:
    if sum(1 for pl in RD.planes if dot(pl[0], c) == pl[1]) == 3: corner_set[tuple(c)] = 1
edges = set()
for f in imp:
    poly = f['poly']
    for i in range(len(poly)): edges.add(frozenset((tuple(poly[i]), tuple(poly[(i + 1) % len(poly)]))))
rd_edges = set()
for pl1, pl2 in itertools.combinations(RD.planes, 2):
    on = [c for c in RD.corners if dot(pl1[0], c) == pl1[1] and dot(pl2[0], c) == pl2[1]]
    if len(on) == 2: rd_edges.add(frozenset(tuple(c) for c in on))
for e in rd_edges:
    a_, b_ = [list(x) for x in e]
    if sum(1 for pl in RD.planes if dot(pl[0], a_) == pl[1]) == 3: a_, b_ = b_, a_
    E = [EE for c, EE, X in bites if c == a_][0]; dirv = vsub(b_, a_)
    ts = [qd(qs(d, dot(n, a_)), dot(n, dirv)) for n, d in E.planes if sgn(dot(n, dirv)) > 0]; t = min(ts, key=qf)
    ex = vadd(a_, vmul(dirv, t)); corner_set[tuple(ex)] = 1; edges.add(frozenset((tuple(ex), tuple(b_))))
    CH.setdefault('RD_edge_exit_parameter_t', set()).add(qs_(t))
CH['RD_edge_exit_parameter_t'] = sorted(CH['RD_edge_exit_parameter_t'])
CH['W_corners'] = len(corner_set); CH['W_edges'] = len(edges); CH['W_faces'] = len(imp) + 12; CH['W_euler'] = CH['W_corners'] - CH['W_edges'] + CH['W_faces']
# dihedral angles
all_faces = [(f['plane'], f['poly']) for f in imp] + [(pl, None) for pl in RD.planes]
dihed = {}; sharp_edges = []
for e in edges:
    p, qq = [list(x) for x in e]; fs = []
    for pl, poly in all_faces:
        n, d = pl
        if dot(n, p) == d and dot(n, qq) == d and (poly is None or (tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly})):
            if not any(same_plane(pl, g) for g in fs): fs.append(pl)
    if len(fs) != 2: dihed['edge_with_%d_faces' % len(fs)] = dihed.get('edge_with_%d_faces' % len(fs), 0) + 1; continue
    (n1, d1), (n2, d2) = fs; deg = cos_angle(n1, n2)
    tests = []
    for pl_, poly_ in [(pl, poly) for pl, poly in all_faces if pl in fs and poly is not None and tuple(p) in {tuple(x) for x in poly} and tuple(qq) in {tuple(x) for x in poly}]:
        pl_other = [f for f in fs if f != pl_][0]; tests.append(all(sgn(qs(pl_other[1], dot(pl_other[0], x))) >= 0 for x in poly_))
    if len(set(tests)) > 1: dihed['inconsistent'] = dihed.get('inconsistent', 0) + 1; continue
    convex = tests[0] if tests else True
    ang = round(180 - deg if convex else 180 + deg, 2); dihed[ang] = dihed.get(ang, 0) + 1
    if ang < 90: sharp_edges.append((ang, round(math.sqrt(qf(dot(vsub(p, qq), vsub(p, qq)))), 5)))
CH['W_dihedral_angles_with_multiplicity'] = {str(k): v for k, v in sorted(dihed.items(), key=lambda kv: str(kv[0]))}
CH['W_sharpest_dihedral'] = min(k for k in dihed if not isinstance(k, str)); CH['W_edges_below_90_deg'] = sorted(sharp_edges)
CH['OCD_dihedral_angles_with_multiplicity'] = None
od = {}
for pl1, pl2 in itertools.combinations(OCD.planes, 2):
    on = [c for c in OCD.corners if dot(pl1[0], c) == pl1[1] and dot(pl2[0], c) == pl2[1]]
    if len(on) == 2: a = round(180 - cos_angle(pl1[0], pl2[0]), 2); od[a] = od.get(a, 0) + 1
CH['OCD_dihedral_angles_with_multiplicity'] = {str(k): v for k, v in sorted(od.items())}
log('faces done', CH['W_corners'], CH['W_edges'], CH['W_faces'], CH['W_sphericity'])
# ------------------------------------------------------------------ thin places: OCD-OCD gap, section necks, inscribed ball, hexagon thirds
# neighbouring OCDs at 0 and (R,0,R) (both bite this W): mirror plane y = 0 is a symmetry of both -> min distance attained in y = 0
c1 = [R, Z, R]; E2 = OCD.shifted(c1)
sec1 = Poly(OCD.planes + [([Z, ONE, Z], Z), ([Z, qn(ONE), Z], Z)], name='s1'); sec2 = Poly(E2.planes + [([Z, ONE, Z], Z), ([Z, qn(ONE), Z], Z)], name='s2')
CH['OCD_section_y0_corners'] = len(sec1.corners)
gap2 = polys_min_dist2(sec1.corners, sec2.corners, [Z, ONE, Z]); CH['OCD_OCD_gap_squared'] = qstr(gap2); CH['OCD_OCD_gap_float'] = math.sqrt(qf(gap2))
# is the gap realised between the two facing outermost (five-fold) corners on the shared octahedron edge's midpoint axis?
f1 = [v for v in five if v[1] == Z and sgn(v[0]) > 0 and sgn(v[2]) > 0]; assert len(f1) == 1; f1 = f1[0]; f2 = vsub(c1, f1)
CH['facing_outer_corners'] = [[qs_(x) for x in f1], [qs_(x) for x in f2]]; CH['facing_outer_corners_distance_squared'] = qstr(dot(vsub(f1, f2), vsub(f1, f2)))
CH['gap_is_between_facing_outer_corners'] = gap2 == dot(vsub(f1, f2), vsub(f1, f2))
CH['outer_corner_to_octa_edge_midpoint_float'] = qf(R) / math.sqrt(2) - math.sqrt(qf(rmax))
CH['outer_corners_lie_on_RD_face_plane_z_eq_x'] = f1[0] == f1[2]
# supporting plane x + z = R of the octahedron edge: OCD stays strictly inside? (max over corners of x+z vs R)
mx = max((qa(v[0], v[2]) for v in V), key=qf); CH['OCD_max_x_plus_z'] = qstr(mx); CH['OCD_strictly_inside_octahedron_edge_plane'] = sgn(qs(R, mx)) > 0
CH['OCD_corners_on_octahedron_surface'] = sum(1 for v in V if qa(qa(qabs(v[0]), qabs(v[1])), qabs(v[2])) == R)
# inscribed ball at v0: distance to the bites
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
CH['W_centre_distance_to_bites_float'] = min(dist_point_convex(v0, E) for c, E, X in bites); CH['W_centre_distance_to_RD_faces_float'] = qf(R) / math.sqrt(2)
CH['W_inscribed_ball_at_centre_float'] = min(CH['W_centre_distance_to_bites_float'], CH['W_centre_distance_to_RD_faces_float'])
CH['W_centre_distance_to_bites_equals_R_minus_2over3'] = abs(CH['W_centre_distance_to_bites_float'] - (qf(R) - 2 / 3)) < 1e-9   # the OCD's 2-fold points (90 corners at radius 2/3) face the vertex
# hexagon thirds: the imprint faces that are parts of the 8 joint hexagons
hexparts = [f for f in imp if f['ocd_face_corners'] == 6]; CH['W_hexagon_imprint_parts'] = len(hexparts); CH['W_hexagon_part_corner_counts'] = sorted({len(f['poly']) for f in hexparts})
CH['W_cut_hexagon_parts_are_exact_thirds'] = all(qm(qr(3), qm(f['lam'], f['lam'])) == qm(qr(3), qm(f['lam'], f['lam'])) and abs(3 * area_float(f['lam'], f['nn']) - min(CH['OCD_face_areas_by_corner_count'][6])) < 1e-10 for f in hexparts if not f['whole'])
CH['W_cut_hexagon_parts'] = sum(1 for f in hexparts if not f['whole'])
# ------------------------------------------------------------------ (4) buildability at 60 mm octahedron edge
scale = 60.0 / (qf(R) * math.sqrt(2)); CH['mm_per_unit_at_60mm_octahedron_edge'] = scale
CH['mm'] = dict(OCD_OCD_gap=CH['OCD_OCD_gap_float'] * scale, RD_face_neck=[x * scale for x in CH['W_RD_face_neck_float']], inscribed_ball_radius_at_vertex=CH['W_inscribed_ball_at_centre_float'] * scale,
                W_extent_between_opposite_OCD_centres=2 * qf(R) * scale, W_extent_between_opposite_tet_sites=qf(R) * math.sqrt(3) * scale, RD_edge=qf(R) * math.sqrt(3) / 2 * scale,
                OCD_diameter_outer=2 * math.sqrt(qf(rmax)) * scale, octahedron_edge=60.0, cell_edge_R=qf(R) * scale)
CH['seconds'] = round(time.time() - t0, 1)
json.dump(dict(mark=MARK, review='Fable review 3, 2026-10-18: OCD + W_OCD exact verification', prescreen_tolerance=TOL_PRESCREEN, checks=CH, W_corner_list=sorted([qs_(x) for x in p] for p in corner_set)),
          open(os.path.join(OUT, 'fable3-exact.json'), 'w'), indent=1, ensure_ascii=False, default=str)
print(json.dumps(CH, indent=1, ensure_ascii=False, default=str)); log('done')
