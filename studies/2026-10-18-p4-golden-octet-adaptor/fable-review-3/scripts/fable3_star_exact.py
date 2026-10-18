# Fable review 3 (2026-10-18): OCD + W_star. W_star = Voronoi cell of the octahedron-edge midpoint m = (0, R/2, R/2) among all edge
# midpoints (R/2)(a,b,c) (exactly two odd), minus the two OCDs at the edge ends (p4 step 7). Exact Q(sqrt5) verification: Voronoi cell,
# tiling, bite volumes, connectivity, symmetry group, faces/corners/edges/dihedrals, OCD-OCD gap, Penrose cores (central + flanks) and
# the middle piece M0 inside W_star, buildability at 60 mm octahedron edge. Output: data/fable3-star-exact.json.
import sys, os, json, itertools, time, math, functools
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fable3_engine import *
from fable3_engine import OUT, STUDY, loadS, f3, qv, qstr, Poly, hull_poly, intersect, same_plane
from q5 import q, qs_, qa, qs, qm, qn, qr, qd, qinv, qf, sgn, vadd, vsub, vmul, dot, cross, det3, PHI, ONE, Z, MARK
import fable3_exact_lib as Lb
t0 = time.time(); CH = {}
def log(*a): print(round(time.time() - t0, 1), 's |', *a, flush=True)
qsum, qabs, rank_pts, tight, face_polygon, poly_order, polygon_area, area_float, cos_angle, polys_min_dist2, sym_test, SP, qmat, apply_lin = (
    Lb.qsum, Lb.qabs, Lb.rank_pts, Lb.tight, Lb.face_polygon, Lb.poly_order, Lb.polygon_area, Lb.area_float, Lb.cos_angle, Lb.polys_min_dist2, Lb.sym_test, Lb.SP, Lb.qmat, Lb.apply_lin)
S1 = loadS('step1-ocd-exact.json'); V = [qv(v) for v in S1['V']]; R = q(S1['R']); faces = S1['faces']
OCD = hull_poly(V, 'OCD'); L = [[R, R, Z], [R, Z, R], [Z, R, R]]; cell = qabs(det3(*L))
half = qd(R, qr(2)); m = [Z, half, half]
# ------------------------------------------------------------------ Voronoi cell of m among the edge midpoints
sites = []
for a, b, c in itertools.product(range(-6, 7), repeat=3):
    if sum(1 for x in (a, b, c) if x % 2) != 2: continue
    p = [qm(half, qr(a)), qm(half, qr(b)), qm(half, qr(c))]
    if p != m and np.linalg.norm(f3(p) - f3(m)) < 2.5 * qf(R): sites.append(p)
bis = []
for p in sites:
    n = vsub(p, m); c = vmul(vadd(p, m), qr(Fr(1, 2))); bis.append((n, dot(n, c)))
VOR = tight(Poly(bis, name='Vor'))
CH['voronoi_corners'] = len(VOR.corners); CH['voronoi_faces'] = len(VOR.planes); CH['voronoi_vol'] = qstr(VOR.vol); CH['voronoi_vol_equals_cell_over_6'] = VOR.vol == qd(cell, qr(6))
claimed = [[Z, Z, Z], [Z, R, R], [Z, R, Z], [Z, Z, R], [half, half, half], [qn(half), half, half]]
CH['voronoi_corners_as_claimed'] = sorted(tuple(c) for c in VOR.corners) == sorted(tuple(c) for c in claimed)
CH['voronoi_face_corner_counts'] = sorted(len(face_polygon(VOR, pl)) for pl in VOR.planes)
CH['voronoi_faces_pass_through_an_OCD_centre'] = all(any(dot(pl[0], c) == pl[1] for c in ([Z, Z, Z], [Z, R, R])) for pl in VOR.planes)
# ------------------------------------------------------------------ tiling: OCDs meeting the cell
rO = math.sqrt(max(qf(dot(v, v)) for v in V))
def lattice_pts(nmax):
    for ijk in itertools.product(range(-nmax, nmax + 1), repeat=3):
        t = [Z, Z, Z]
        for c, Lv in zip(ijk, L): t = vadd(t, vmul(Lv, qr(c)))
        yield t
bites = []
for c in lattice_pts(3):
    if np.linalg.norm(f3(c) - f3(m)) > rO + qf(R) + 1e-6: continue
    E = OCD.shifted(c); X = intersect(E, VOR, 'bite')
    if X.vol != Z: bites.append((c, E, X))
CH['OCDs_meeting_cell'] = [[qs_(x) for x in c] for c, E, X in bites]; CH['OCDs_meeting_cell_are_the_edge_ends'] = sorted(tuple(c) for c, E, X in bites) == sorted([(Z, Z, Z), (Z, R, R)])
CH['bite_volumes'] = sorted({qstr(X.vol) for c, E, X in bites}); CH['each_bite_is_OCD_over_12'] = all(X.vol == qd(OCD.vol, qr(12)) for c, E, X in bites)
# the OCD at 0 split over its 12 edge-midpoint cells sums to OCD
tot = Z
for s in itertools.product((1, -1), repeat=2):
    for perm in ((0, 1), (0, 2), (1, 2)):
        mm = [Z, Z, Z]; mm[perm[0]] = qm(half, qr(s[0])); mm[perm[1]] = qm(half, qr(s[1]))
        t = vsub(mm, m); VORm = Poly([(n, qa(d, dot(n, t))) for n, d in VOR.planes], name='Vm')
        tot = qa(tot, intersect(OCD, VORm).vol)
CH['OCD_split_over_its_12_cells_sums_to_OCD'] = tot == OCD.vol
vW = qs(VOR.vol, qsum([X.vol for c, E, X in bites])); CH['W_star_vol'] = qstr(vW); CH['W_star_vol_float'] = qf(vW)
CH['W_star_vol_equals_cell_minus_OCD_over_6'] = vW == qd(qs(cell, OCD.vol), qr(6)); CH['W_star_vol_matches_claim_1412_minus_164sqrt5_over_4617'] = vW == q('1412/4617|-164/4617')
log('tiling', qf(vW))
# ------------------------------------------------------------------ connectivity, symmetry
cells = [VOR]
for c, E, X in bites:
    new = []
    for X0 in cells:
        if intersect(X0, E).vol == Z: new.append(X0); continue
        new += Lb.split_outside(X0, E)
    cells = new; log('split by OCD at', [round(qf(x), 3) for x in c], '-> cells', len(cells))
CH['W_star_convex_cells'] = len(cells); CH['W_star_cells_volume_sum_equals_W'] = qsum([X.vol for X in cells]) == vW
CH['W_star_connected_components_exact'] = Lb.components(cells)
symS = sym_test(m, bites, VOR.planes); CH['W_star_symmetries_of_48_cube_ops'] = symS
ops = []
for M in SP:
    Mq = qmat(M)
    if Lb.plane_set_equal(Lb.map_planes_about(VOR.planes, Mq, m), VOR.planes) and all(any(Lb.plane_set_equal(Lb.map_planes_about(E.planes, Mq, m), E2.planes) for c2, E2, X2 in bites) for c, E, X in bites): ops.append(M.tolist())
CH['W_star_symmetry_operations'] = ops; CH['W_star_point_group'] = '2/m (identity, inversion through m, 2-fold about the x-axis through m, mirror x = 0)' if len(ops) == 4 else f'{len(ops)} operations'
# ------------------------------------------------------------------ faces, corners, edges, dihedrals
imp = []
for c, E, X in bites:
    for n, d in E.planes:
        poly = face_polygon(X, (n, d))
        if poly:
            lam, nn = polygon_area(poly, n); full = face_polygon(E, (n, d)); lamf, nnf = polygon_area(full, n)
            imp.append(dict(plane=([qn(x) for x in n], qn(d)), poly=poly, lam=lam, nn=nn, whole=lam == lamf, ocd_face_corners=len(full)))
bk = {}
for f in imp:
    key = f"{'whole' if f['whole'] else 'cut'} {f['ocd_face_corners']}-gon -> {len(f['poly'])} corners"; bk[key] = bk.get(key, 0) + 1
CH['W_star_imprint_faces'] = len(imp); CH['W_star_imprint_whole'] = sum(1 for f in imp if f['whole']); CH['W_star_imprint_breakdown'] = dict(sorted(bk.items()))
imp_area = sum(area_float(f['lam'], f['nn']) for f in imp); ocd_area = sum(area_float(*polygon_area(face_polygon(OCD, pl), pl[0])) for pl in OCD.planes)
CH['W_star_imprint_area_is_one_sixth_OCD_surface'] = abs(imp_area - ocd_area / 6) < 1e-10
cut_area = 0.0; cut_parts = []
for n, d in VOR.planes:
    full = face_polygon(VOR, (n, d)); a = area_float(*polygon_area(full, n)); secs = []
    for c, E, X in bites:
        poly = face_polygon(X, (n, d))
        if poly: secs.append(poly); a -= area_float(*polygon_area(poly, n))
    cut_parts.append((len(secs), a)); cut_area += a
CH['W_star_cut_face_sections_per_face'] = sorted(k for k, a in cut_parts); CH['W_star_cut_face_part_areas'] = sorted({round(a, 12) for k, a in cut_parts})
A_W = imp_area + cut_area; CH['W_star_surface_area_float'] = A_W; CH['W_star_sphericity'] = math.pi ** (1 / 3) * (6 * qf(vW)) ** (2 / 3) / A_W
corner_set = {}
for f in imp:
    for p in f['poly']: corner_set[tuple(p)] = 1
for c in VOR.corners:
    if not any(all(sgn(qs(d, dot(n, c))) >= 0 for n, d in E.planes) for cc, E, X in bites): corner_set[tuple(c)] = 1
edges = set()
for f in imp:
    poly = f['poly']
    for i in range(len(poly)): edges.add(frozenset((tuple(poly[i]), tuple(poly[(i + 1) % len(poly)]))))
vor_edges = set()
for pl1, pl2 in itertools.combinations(VOR.planes, 2):
    on = [c for c in VOR.corners if dot(pl1[0], c) == pl1[1] and dot(pl2[0], c) == pl2[1]]
    if len(on) == 2: vor_edges.add(frozenset(tuple(c) for c in on))
for e in vor_edges:
    a_, b_ = [list(x) for x in e]; ina = [E for c, E, X in bites if all(sgn(qs(d, dot(n, a_))) >= 0 for n, d in E.planes)]; inb = [E for c, E, X in bites if all(sgn(qs(d, dot(n, b_))) >= 0 for n, d in E.planes)]
    if ina and inb: continue
    if not ina and not inb: edges.add(frozenset((tuple(a_), tuple(b_)))); continue
    if inb: a_, b_ = b_, a_; ina = inb
    E = ina[0]; dirv = vsub(b_, a_); ts = [qd(qs(d, dot(n, a_)), dot(n, dirv)) for n, d in E.planes if sgn(dot(n, dirv)) > 0]; t = min(ts, key=qf)
    ex = vadd(a_, vmul(dirv, t)); corner_set[tuple(ex)] = 1; edges.add(frozenset((tuple(ex), tuple(b_))))
CH['W_star_corners'] = len(corner_set); CH['W_star_edges'] = len(edges); CH['W_star_faces'] = len(imp) + len(VOR.planes); CH['W_star_euler'] = CH['W_star_corners'] - CH['W_star_edges'] + CH['W_star_faces']
all_faces = [(f['plane'], f['poly']) for f in imp] + [(pl, None) for pl in VOR.planes]
dihed, sharp = Lb.dihedrals(edges, all_faces)
CH['W_star_dihedral_angles_with_multiplicity'] = {str(k): v for k, v in sorted(dihed.items(), key=lambda kv: str(kv[0]))}
CH['W_star_sharpest_dihedral'] = min(k for k in dihed if not isinstance(k, str)); CH['W_star_edges_below_90_deg'] = sorted(sharp)
log('faces done', CH['W_star_corners'], CH['W_star_edges'], CH['W_star_faces'], CH['W_star_sphericity'])
# ------------------------------------------------------------------ thin places
c2 = [Z, R, R]; E2 = OCD.shifted(c2)
sec1 = Poly(OCD.planes + [([ONE, Z, Z], Z), ([qn(ONE), Z, Z], Z)], name='s1'); sec2 = Poly(E2.planes + [([ONE, Z, Z], Z), ([qn(ONE), Z, Z], Z)], name='s2')
gap2 = polys_min_dist2(sec1.corners, sec2.corners, [ONE, Z, Z]); CH['OCD_OCD_gap_squared'] = qstr(gap2); CH['OCD_OCD_gap_float'] = math.sqrt(qf(gap2))
sup = max((qa(v[1], v[2]) for v in V), key=qf); CH['OCD_support_along_edge_axis_y_plus_z'] = qstr(sup); CH['OCDs_stay_on_their_sides_of_the_mid_plane'] = sgn(qs(R, sup)) > 0
CH['mid_plane_margin_each_side_float'] = (qf(R) - qf(sup)) / math.sqrt(2)
five = [v for v in V if dot(v, v) == max((dot(w, w) for w in V), key=qf)]; c1 = [v for v in five if v[0] == Z and sgn(v[1]) > 0 and sgn(v[2]) > 0][0]
CH['facing_five_fold_corners_gap_equals_OCD_gap'] = gap2 == dot(vsub(vsub(c2, c1), c1), vsub(vsub(c2, c1), c1))
# inscribed ball at m and distance from m to the cut faces
CH['W_star_centre_distance_to_bites_float'] = min(Lb.dist_point_convex(m, E) for c, E, X in bites)
CH['W_star_centre_distance_to_cut_faces_float'] = min(abs(qf(qs(d, dot(n, m)))) / math.sqrt(qf(dot(n, n))) for n, d in VOR.planes)
# ------------------------------------------------------------------ Penrose: H, M0 and the three cores inside the cell?
star = [V[j] for j in sorted({j for f in faces if V.index(c1) in f for j in f})]
H = hull_poly(star + [vsub(c2, p) for p in star], 'H'); CH['H_vol'] = qstr(H.vol)
def minus_ocds(P):
    v = P.vol
    for c, E, X in bites: v = qs(v, intersect(P, E).vol)
    return v
M0 = minus_ocds(H); CH['M0_vol'] = qstr(M0); CH['M0_matches_step19'] = qs_(M0) == loadS('step19-flank-cores.json')['checks']['M0']
HC = intersect(H, VOR); M0_in = minus_ocds(HC); CH['M0_inside_W_star'] = qstr(M0_in); CH['M0_share_inside_W_star'] = qf(M0_in) / qf(M0); CH['M0_wholly_inside'] = M0_in == M0
# where does M0 poke out? which Voronoi faces does H cross (star tips beyond the cut planes)
CH['H_corners_outside_cell'] = sum(1 for p in H.corners if not all(sgn(qs(d, dot(n, p))) >= 0 for n, d in VOR.planes)); CH['H_corners'] = len(H.corners)
S19 = loadS('step19-flank-cores.json'); a = c1; aa = dot(a, a)
def side_planes(Q):
    cen = [qd(qsum([p[k] for p in Q]), qr(4)) for k in range(3)]; out = []
    for k in range(4):
        n = cross(vsub(Q[(k + 1) % 4], Q[k]), a); dd = dot(n, Q[k])
        if sgn(qs(dot(n, cen), dd)) > 0: n = [qn(x) for x in n]; dd = qn(dd)
        out.append((n, dd))
    return out
cores = {}
for name, Q in S19['rhombi'].items():
    Qq = [qv(p) for p in Q]; PH = Poly(side_planes(Qq) + H.planes, name='prism&H'); core = minus_ocds(PH)
    PHC = intersect(PH, VOR); core_in = minus_ocds(PHC)
    cores[name] = dict(core=qstr(core), matches_step19=qs_(core) == S19['checks']['cores'][name], inside_W_star=qstr(core_in), wholly_inside=core_in == core, share_inside=qf(core_in) / qf(core))
CH['penrose_cores'] = cores
# ------------------------------------------------------------------ buildability at 60 mm octahedron edge
scale = 60.0 / (qf(R) * math.sqrt(2)); CH['mm_per_unit'] = scale
CH['mm'] = dict(OCD_OCD_gap_at_centre=CH['OCD_OCD_gap_float'] * scale, mid_plane_margin_each_side=CH['mid_plane_margin_each_side_float'] * scale,
                W_star_span_between_edge_ends=60.0, W_star_span_between_tet_sites=qf(R) * scale, inscribed_ball_at_centre=min(CH['W_star_centre_distance_to_bites_float'], CH['W_star_centre_distance_to_cut_faces_float']) * scale)
CH['seconds'] = round(time.time() - t0, 1)
json.dump(dict(mark=MARK, review='Fable review 3, 2026-10-18: OCD + W_star exact verification', prescreen_tolerance=TOL_PRESCREEN, checks=CH, W_star_corner_list=sorted([qs_(x) for x in p] for p in corner_set)),
          open(os.path.join(OUT, 'fable3-star-exact.json'), 'w'), indent=1, ensure_ascii=False, default=str)
print(json.dumps(CH, indent=1, ensure_ascii=False, default=str)); log('done')
