# Fable review 4 (2026-10-18): the KEYED star-centred W (DICTO: "rhombi pattern continued along its edges as a key with itself").
# W_star = Voronoi octahedron of the edge midpoint m = (0, R/2, R/2) minus the two OCDs. Its 8 flat W-W faces pair bipartitely
# (p4_key_pairing): faces (A0,E0,T+-), (A1,E1,T+-) carry BUMPS, faces (A0,E1,T+-), (A1,E0,T+-) carry DENTS.
# Continuation of the star pattern: on each bump face exactly two rim edges of the socket's five-fold star (long kite edges, 0.2379)
# pierce the face plane inside the face triangle. The key tile is a planar kite congruent to the star's kite, with its 55.69-degree
# apex at the piercing point (pushed a clearance delta along the edge) and one long edge continuing the pierced star edge's line.
# Bump = kite frustum of height h with walls 30 degrees off the face normal; dents = the bumps carried over by the structure
# symmetry g (3-fold turn about the OCD centre) so that every W is identical and the bump of one W fills the dent of its neighbour.
# Pattern on face 1 -> faces 0, 6, 7 by W's own 2/m symmetry; dents on faces 3, 2, 5, 4. -> data/keyed-W-geometry.json (float, from exact data)
import sys, os, json, math, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', '..', 'fable-review-3', 'scripts'))
from fable3_engine import *
from fable3_engine import loadS, f3, qv, hull_poly, Poly
from q5 import *
from scipy.spatial import ConvexHull
HREL, WALL_DEG = 0.05, 30.0                                     # relief height, wall angle off the face normal
S1 = loadS('step1-ocd-exact.json'); V = [qv(v) for v in S1['V']]; OCD = hull_poly(V, 'OCD'); Vf = np.array([f3(v) for v in V]); R = qf(q(S1['R']))
idx = {tuple(v): i for i, v in enumerate(V)}
def poly_of(pl):
    on = [idx[tuple(c)] for c in OCD.corners if dot(pl[0], c) == pl[1]]; P = Vf[on]; c0 = P.mean(0); nf = f3(pl[0]); a = P[0] - c0; a -= nf * (a @ nf) / (nf @ nf); b = np.cross(nf, a)
    return [on[i] for i in np.argsort(np.arctan2((P - c0) @ b, (P - c0) @ a))]
polys = [poly_of(pl) for pl in OCD.planes]
ocd_planes = []
for n_, d_ in OCD.planes:
    nf = f3(n_); L = np.linalg.norm(nf); ocd_planes.append((nf / L).tolist() + [qf(d_) / L])
m = np.array([0, R / 2, R / 2]); A0, A1, E0, E1, Tp, Tm = np.zeros(3), np.array([0, R, R]), np.array([0, R, 0]), np.array([0, 0, R]), np.array([R / 2, R / 2, R / 2]), np.array([-R / 2, R / 2, R / 2])
cell = np.array([A0, A1, E0, E1, Tp, Tm])
# face 1 = (A0, E0, T+), plane z = x, outward normal N
U = np.array([0, 1, 0.]); Wv = np.array([1, 0, 1.]) / np.sqrt(2); N = np.array([1, 0, -1.]) / np.sqrt(2)
uv = lambda P: np.array([P @ U, P @ Wv]); xyz = lambda p: p[0] * U + p[1] * Wv
tri = np.array([uv(A0), uv(E0), uv(Tp)])
r = np.linalg.norm(Vf, axis=1); i1 = [i for i in range(len(V)) if abs(r[i] - r.max()) < 1e-9 and abs(Vf[i, 0]) < 1e-9 and Vf[i, 1] > 0 and Vf[i, 2] > 0][0]; c1 = Vf[i1]
star = [p for p in polys if i1 in p]; assert len(star) == 5
# kite shape from the star kite: edges at c1 are the short ones (b), far apex between the long ones (a)
p = star[0]; k = p.index(i1); P = Vf[[p[k], p[(k + 1) % 4], p[(k + 2) % 4], p[(k + 3) % 4]]]
b_len = np.linalg.norm(P[1] - P[0]); a_len = np.linalg.norm(P[2] - P[1]); ang = lambda X, Y, Zz: math.degrees(math.acos(np.clip((X - Y) @ (Zz - Y) / np.linalg.norm(X - Y) / np.linalg.norm(Zz - Y), -1, 1)))
alpha = ang(P[1], P[2], P[3]); beta = ang(P[1], P[0], P[3]); side = ang(P[0], P[1], P[2]); diag_long = np.linalg.norm(P[2] - P[0])
kite = dict(long_edge=a_len, short_edge=b_len, apex_between_long_edges_deg=alpha, apex_between_short_edges_deg_at_star_centre=beta, side_angle_deg=side, long_diagonal=diag_long, area=0.5 * diag_long * 2 * a_len * math.sin(math.radians(alpha / 2)))
# socket rim (section) and shadow in the face plane
sec = Poly(OCD.planes + [([ONE, Z, qn(ONE)], Z), ([qn(ONE), Z, ONE], Z)], name='sec'); S = np.array([uv(f3(c)) for c in sec.corners]); S = S[ConvexHull(S).vertices]
Sh = np.array([uv(v) for v in Vf]); Sh = Sh[ConvexHull(Sh).vertices]
# star rim edges piercing the plane inside the triangle
star_edges = {(min(a, b), max(a, b)) for q_ in star for kk in range(4) for a, b in [(q_[kk], q_[(kk + 1) % 4])]}
def in_tri(pt, margin=0.0):
    u_, w_ = pt; return w_ >= margin and w_ <= np.sqrt(2) * min(u_, R - u_) - margin * np.sqrt(3)
def dist_to_segs(pt, poly):
    best = np.inf
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]; t = np.clip((pt - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1); best = min(best, np.linalg.norm(pt - a - t * (b - a)))
    return best
def inside_poly(pt, poly):
    cr2 = lambda a, b: a[0] * b[1] - a[1] * b[0]
    s = [cr2(poly[(i + 1) % len(poly)] - poly[i], pt - poly[i]) for i in range(len(poly))]; return all(x >= -1e-12 for x in s) or all(x <= 1e-12 for x in s)
pierce = []
for a, b in star_edges:
    za, zb = Vf[a] @ N, Vf[b] @ N
    if za * zb < 0:
        t = za / (za - zb); Q = Vf[a] + t * (Vf[b] - Vf[a]); d = Vf[b] - Vf[a]; d = d if zb < 0 else -d; din = d - (d @ N) * N; din /= np.linalg.norm(din)
        quv = uv(Q)
        if in_tri(quv): pierce.append(dict(edge=[int(a), int(b)], Q=quv.tolist(), dir=uv(din).tolist(), dir_deg=math.degrees(math.atan2(din @ Wv, din @ U))))
assert len(pierce) == 2, pierce
def kite_at(Q, dvec, sign):
    """planar kite: apex (angle alpha) at Q, first long edge along dvec, second long edge turned by sign*alpha, far apex along the axis"""
    th = math.atan2(dvec[1], dvec[0]); a1 = th; a2 = th + sign * math.radians(alpha); ax = th + sign * math.radians(alpha / 2)
    P0 = np.array(Q); P1 = P0 + a_len * np.array([math.cos(a1), math.sin(a1)]); P3 = P0 + a_len * np.array([math.cos(a2), math.sin(a2)]); P2 = P0 + diag_long * np.array([math.cos(ax), math.sin(ax)])
    return np.array([P0, P1, P2, P3])
def quality(K):
    """clearances: to the triangle edges (want >= HREL) and to the OCD shadow (want >= 0.025), all corners inside the triangle, outside the shadow"""
    ok_tri = all(in_tri(c) for c in K); ok_sh = not any(inside_poly(c, Sh) for c in K)
    # also the kite's edges vs the shadow: sample
    pts = np.vstack([K[i] + (K[(i + 1) % 4] - K[i]) * np.linspace(0, 1, 25)[:, None] for i in range(4)])
    d_sh = min(dist_to_segs(c, Sh) for c in pts); d_tri = min(dist_to_segs(c, tri) for c in pts); ok_sh = ok_sh and not any(inside_poly(c, Sh) for c in pts)
    return dict(inside_triangle=ok_tri, outside_shadow=ok_sh, clearance_to_cell_edges=d_tri, clearance_to_shadow=d_sh)
# the continued edge line is the OCD's silhouette there (the shadow boundary runs along it), so the kite must stand a clearance c beside
# that line (parallel, into the face) and a shift delta along it (off the rim). Small grid search: maximise the smaller of the two clearances
# (to the cell edges, want >= 0.035 = 1.4 mm; to the OCD shadow, want >= 0.025 = 1 mm); an optional small turn rho about the apex is allowed.
cands = []
for pc in pierce:
    perp = np.array([-pc['dir'][1], pc['dir'][0]]); perp = perp if in_tri(np.array(pc['Q']) + 0.05 * perp) else -perp
    for sign in (1, -1):
        for delta in np.arange(0.0, 0.081, 0.01):
            for c in np.arange(0.015, 0.061, 0.005):
                for rho in (0.0, 2.0, 4.0, 6.0, -2.0, -4.0):
                    th = math.radians(pc['dir_deg'] + rho); dv = np.array([math.cos(th), math.sin(th)])
                    Q = np.array(pc['Q']) + delta * np.array(pc['dir']) + c * perp; K = kite_at(Q, dv, sign); qd_ = quality(K)
                    cands.append(dict(pierce=pc, sign=sign, delta=float(delta), c=float(c), rho_deg=rho, kite=K.tolist(), **qd_))
good = [c for c in cands if c['inside_triangle'] and c['outside_shadow'] and c['clearance_to_cell_edges'] >= 0.035 and c['clearance_to_shadow'] >= 0.025]
assert good, 'no placement'
# prefer the exact continuation (rho = 0), then the largest minimum clearance
best = max(good, key=lambda c: (c['rho_deg'] == 0.0, min(c['clearance_to_cell_edges'], c['clearance_to_shadow'])))
K = np.array(best['kite'])
# frustum: bottom = kite in the plane, top = kite scaled about its incentre by (1 - t_in / r_in), lifted by HREL along N
area = 0.5 * abs((K[2] - K[0])[0] * (K[3] - K[1])[1] - (K[2] - K[0])[1] * (K[3] - K[1])[0]); semi = a_len + b_len; r_in = area / semi; t_in = HREL * math.tan(math.radians(WALL_DEG)); scale = 1 - t_in / r_in
# incentre of a kite lies on its axis at distance r_in / sin(alpha/2) from the apex P0
axis = (K[2] - K[0]) / np.linalg.norm(K[2] - K[0]); inc = K[0] + axis * r_in / math.sin(math.radians(alpha / 2))
assert all(abs(dist_to_segs(inc, np.array([K[i], K[(i + 1) % 4]])) - r_in) < 1e-9 for i in range(4)), 'incentre check'
Ktop = inc + (K - inc) * scale
bottom3 = np.array([xyz(c) for c in K]); top3 = np.array([xyz(c) for c in Ktop]) + HREL * N
B1 = np.vstack([bottom3, top3])                                 # 8 vertices of the bump frustum on face 1 (outside the cell, in the neighbour's cell)
# symmetry operations
sigma = lambda X: X * np.array([-1, 1, 1])                       # mirror x = 0 (W's own)
iota = lambda X: 2 * m - X                                       # inversion through m (W's own)
g = lambda X: X[..., [1, 2, 0]]                                  # (x,y,z) -> (y,z,x): 3-fold turn about the OCD centre A0; g(m) = (R/2,R/2,0) = neighbour across face 1
ginv = lambda X: X[..., [2, 0, 1]]
assert np.allclose(g(m), [R / 2, R / 2, 0]) and np.allclose(ginv(m), [R / 2, 0, R / 2])
bumps = {'face1 (A0,E0,T+)': B1, 'face0 (A0,E0,T-)': sigma(B1), 'face7 (A1,E1,T-)': iota(B1), 'face6 (A1,E1,T+)': iota(sigma(B1))}
dents = {'face3 (A0,E1,T+)': ginv(B1), 'face2 (A0,E1,T-)': sigma(ginv(B1)), 'face5 (A1,E0,T-)': iota(ginv(B1)), 'face4 (A1,E0,T+)': iota(sigma(ginv(B1)))}
# checks: cell planes (outward), bumps outside the cell on one face plane, dents inside the cell on one face plane
hc = ConvexHull(cell); cplanes = []
for eq in hc.equations:
    if not any(np.allclose(eq, e2) for e2 in cplanes): cplanes.append(eq)
def side(X, eq): return X @ eq[:3] + eq[3]
def face_of(X):
    on = [i for i, eq in enumerate(cplanes) if np.abs(side(X[:4], eq)).max() < 1e-9]; return on
chk = {}
for nm, Bf in bumps.items():
    f = face_of(Bf); eq = cplanes[f[0]]; chk[nm] = dict(bottom_on_one_cell_face=len(f) == 1, top_outside_cell=bool((side(Bf[4:], eq) > 1e-9).all()), inside_other_cell_planes=bool(all((side(Bf, e2) <= 1e-9).all() for i, e2 in enumerate(cplanes) if i != f[0])))
for nm, Df in dents.items():
    f = face_of(Df); eq = cplanes[f[0]]; chk[nm] = dict(bottom_on_one_cell_face=len(f) == 1, top_inside_cell=bool((side(Df[4:], eq) < -1e-9).all()), inside_other_cell_planes=bool(all((side(Df, e2) <= 1e-9).all() for i, e2 in enumerate(cplanes) if i != f[0])))
PN = np.array([p_[:3] for p_ in ocd_planes]); PD = np.array([p_[3] for p_ in ocd_planes])
def outside_ocd(X, c): return bool((((X - c) @ PN.T) > PD + 1e-9).any(1).all())
chk['all_bumps_and_dents_vertices_outside_both_OCDs'] = all(outside_ocd(X, c) for X in list(bumps.values()) + list(dents.values()) for c in (A0, A1))
scale_mm = 60.0 / (R * np.sqrt(2))
out = dict(mark='DICTO · dictospheres.com', R=R, m=m.tolist(), cell=cell.tolist(), frame=dict(U=U.tolist(), W=Wv.tolist(), N=N.tolist()), face1_triangle_uv=tri.tolist(),
           section_uv=S.tolist(), shadow_uv=Sh.tolist(), kite=kite, pierce=pierce, n_candidates=len(cands), n_good=len(good), chosen=best,
           relief=dict(height=HREL, wall_deg_off_normal=WALL_DEG, top_inset=t_in, top_scale=scale, kite_inradius=r_in),
           bumps={k_: v_.tolist() for k_, v_ in bumps.items()}, dents={k_: v_.tolist() for k_, v_ in dents.items()}, checks=chk, ocd_planes=ocd_planes, ocd_V=Vf.tolist(),
           mm=dict(scale=scale_mm, relief_height=HREL * scale_mm, kite_long_edge=a_len * scale_mm, kite_short_edge=b_len * scale_mm, kite_long_diagonal=diag_long * scale_mm, top_kite_long_edge=a_len * scale * scale_mm,
                   clearance_to_cell_edges=best['clearance_to_cell_edges'] * scale_mm, clearance_to_socket_shadow=best['clearance_to_shadow'] * scale_mm, top_inset=t_in * scale_mm, kite_offset_beside_star_edge_line=best['c'] * scale_mm, kite_shift_along_edge=best['delta'] * scale_mm))
json.dump(out, open(os.path.join(H, '..', 'data', 'keyed-W-geometry.json'), 'w'), indent=1)
print(json.dumps(dict(kite=kite, pierce=pierce, chosen={k_: v_ for k_, v_ in best.items() if k_ != 'kite'}, relief=out['relief'], checks=chk, mm=out['mm']), indent=1, default=str))
