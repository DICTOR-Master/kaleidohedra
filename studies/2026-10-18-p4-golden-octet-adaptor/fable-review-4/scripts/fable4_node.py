# Fable review 4 (2026-10-18), dicto-node part (manifold3d + numpy): build the keyed star-centred W from data/keyed-W-geometry.json and check it.
# Keyed W = cell − OCD0 − OCD1 − dents + bumps. Checks: one solid, genus, volume (= W_star), dihedrals; the pair across face 1 (neighbour
# g(W)): no overlap, union = both cells minus OCDs (bump fills dent exactly); the 12 W round one OCD: pairwise overlaps, union; separation
# directions (pair and ring); dense sampling of the periodic tiling OCD + keyed W. Meshes for the page. usage: fable4_node.py GEOM.json OUT.json
import sys, json, itertools, time, numpy as np, manifold3d as m3
t0 = time.time(); D = json.load(open(sys.argv[1])); R = D['R']; m = np.array(D['m']); cell = np.array(D['cell']); V = np.array(D['ocd_V']); PL = np.array(D['ocd_planes']); PN, PD = PL[:, :3], PL[:, 3]
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
def log(*a): print(round(time.time() - t0, 1), 's |', *a, flush=True)
L = np.array([[R, R, 0], [R, 0, R], [0, R, R]]); OCD = hull(V)
ocd_centres = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]
bumps = [np.array(v) for v in D['bumps'].values()]; dents = [np.array(v) for v in D['dents'].values()]
def keyed(G=np.eye(3)):
    """keyed W for the cell at G m (G a Th operation about the OCD centre at the origin)"""
    T = lambda X: X @ G.T
    base = hull(T(cell)) - OCD - OCD.translate(T(np.array([0, R, R])))
    W = base - U([hull(T(d)) for d in dents]); W = W + U([hull(T(b)) for b in bumps]); return W
W = keyed(); Wstar = hull(cell) - OCD - OCD.translate([0, R, R])
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
def dihedrals(mf):
    M = mf.to_mesh(); Vv = np.asarray(M.vert_properties[:, :3], float); T = np.asarray(M.tri_verts, int)
    N = np.cross(Vv[T[:, 1]] - Vv[T[:, 0]], Vv[T[:, 2]] - Vv[T[:, 0]]); N /= np.linalg.norm(N, axis=1)[:, None]; edges = {}
    for ti, t in enumerate(T):
        for k in range(3):
            a, b = t[k], t[(k + 1) % 3]; edges.setdefault((min(a, b), max(a, b)), []).append((ti, t[(k + 2) % 3]))
    out = []
    for (a, b), tri in edges.items():
        if len(tri) != 2: continue
        (t1, c1), (t2, c2) = tri; cs = np.clip(N[t1] @ N[t2], -1, 1); ang = np.degrees(np.arccos(cs))
        if ang < 1e-5: continue
        convex = (Vv[c2] - Vv[a]) @ N[t1] < 0; out.append((180 - ang if convex else 180 + ang, np.linalg.norm(Vv[a] - Vv[b])))
    return out
parts = W.decompose(); dh = dihedrals(W); angs = np.array([a for a, l in dh])
hist = {}
for a in angs: hist[str(round(a, 1))] = hist.get(str(round(a, 1)), 0) + 1
bump_vol = sum(hull(b).volume() for b in bumps); dent_vol = sum(hull(d).volume() for d in dents)
out = dict(mark='DICTO · dictospheres.com', keyed_W=dict(volume=W.volume(), W_star_volume=Wstar.volume(), volume_difference=W.volume() - Wstar.volume(), parts=len(parts), solid_parts=len([p for p in parts if p.volume() > 1e-9]),
           genus=W.genus(), area=W.surface_area(), sphericity=sph(W), bump_volume_total=bump_vol, dent_volume_total=dent_vol, one_bump_volume=hull(bumps[0]).volume(),
           sharpest_edge_deg=float(angs.min()), bluntest_reflex_deg=float(angs.max()), dihedral_histogram=dict(sorted(hist.items(), key=lambda kv: float(kv[0]))),
           corners=len(np.unique(np.round(np.asarray(W.to_mesh().vert_properties[:, :3]), 6), axis=0))))
log('keyed W', {k: v for k, v in out['keyed_W'].items() if k != 'dihedral_histogram'})
# the neighbour across face 1: g = (x,y,z) -> (y,z,x), as a matrix G with G m = (R/2, R/2, 0)
G = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float); assert np.allclose(G @ m, [R / 2, R / 2, 0])
Wj = keyed(G); inter = (W ^ Wj).volume(); uni = (W + Wj).volume()
both_cells = (hull(cell) + hull(cell @ G.T)) - OCD - OCD.translate([0, R, R]) - OCD.translate([R, R, 0])
out['pair_face1'] = dict(overlap_volume=inter, union_volume=uni, two_W=2 * W.volume(), cells_minus_OCDs_volume=both_cells.volume(), union_equals_cells_minus_OCDs=abs(uni - both_cells.volume()) < 1e-9,
                         gap_volume=both_cells.volume() - uni, contact_area_estimate=None)
log('pair', out['pair_face1'])
# separation directions for the pair: move Wj by eps*d; blocked if it overlaps W
rng = np.random.default_rng(3); dirs = rng.normal(size=(600, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
nface = np.array([1, 0, -1]) / np.sqrt(2); eps = 0.02; free = []
for d in dirs:
    if d @ nface <= 0: continue                                   # moving into W is blocked by the flat face anyway
    if (W ^ Wj.translate(eps * d)).volume() < 1e-9: free.append(np.degrees(np.arccos(np.clip(d @ nface, -1, 1))))
out['pair_separation'] = dict(directions_tested_outward=int((dirs @ nface > 0).sum()), free_directions=len(free), max_angle_from_face_normal_deg=float(max(free)) if free else None, wall_angle_deg=D['relief']['wall_deg_off_normal'])
log('separation', out['pair_separation'])
# the 12 W round the OCD at the origin: Th operations with distinct images of m
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        Gk = np.zeros((3, 3))
        for i in range(3): Gk[i, pm[i]] = sg[i]
        ops.append(Gk)
ring = {}
for Gk in ops:
    key = tuple(np.round(Gk @ m, 6))
    if key not in ring: ring[key] = Gk
ring_ops = list(ring.values()); assert len(ring_ops) == 12
pieces = [keyed(Gk) for Gk in ring_ops]
ov = 0.0; pairs = 0
for a, b in itertools.combinations(range(12), 2):
    v = (pieces[a] ^ pieces[b]).volume(); pairs += 1; ov = max(ov, v)
ocd_ov = max((p ^ OCD).volume() for p in pieces)
ring_union = U(pieces + [OCD]); out['ring12'] = dict(pairs_tested=pairs, max_pairwise_overlap=ov, max_overlap_with_OCD=ocd_ov, union_volume=ring_union.volume(), expected=12 * W.volume() + OCD.volume(),
                                                     union_equals_sum=abs(ring_union.volume() - 12 * W.volume() - OCD.volume()) < 1e-8)
log('ring', out['ring12'])
# can one W leave the ring (others + OCD fixed)? test outward directions
others = U(pieces[1:] + [OCD]); freed = 0; tested = 0
for d in dirs:
    tested += 1
    if (pieces[0].translate(eps * d) ^ others).volume() < 1e-9: freed += 1
out['ring12_piece_removal'] = dict(directions_tested=tested, free_directions=freed, note='translation of one W by 0.02 in each direction with the other 11 W and the OCD fixed')
# the same for the unkeyed W_star ring, for comparison
plain = [hull(cell @ Gk.T) - OCD - OCD.translate(Gk @ np.array([0, R, R])) for Gk in ring_ops]; others_p = U(plain[1:] + [OCD]); freed_p = 0
for d in dirs:
    if (plain[0].translate(eps * d) ^ others_p).volume() < 1e-9: freed_p += 1
out['ring12_piece_removal']['free_directions_unkeyed_W_star'] = freed_p
log('ring removal', out['ring12_piece_removal'])
# meshes (relative to the piece centre m) for the page
for nm, mf in (('keyed_W', W), ('W_star', Wstar)):
    M = mf.to_mesh(); out[nm + '_mesh'] = dict(v=np.round(np.asarray(M.vert_properties[:, :3], float) - m, 6).tolist(), t=np.asarray(M.tri_verts).tolist())
M = OCD.to_mesh(); out['ocd_mesh'] = dict(v=np.round(np.asarray(M.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(M.tri_verts).tolist())
json.dump(out, open(sys.argv[2], 'w')); log('meshes saved')
# ---------------------------------------------------------------- sampling of the periodic tiling OCD + keyed W
# piece at site s = G m + t (G in Th, t fcc translation) = G W + t. Membership: p in piece iff (p in its cell and outside OCDs and not in a dent) or (p in a bump).
# Convex frusta as half-space sets (hull planes), transformed with the piece.
def hull_planes(P):
    h = m3.Manifold.hull_points(P).to_mesh(); Vv = np.asarray(h.vert_properties[:, :3]); T = np.asarray(h.tri_verts)
    N = np.cross(Vv[T[:, 1]] - Vv[T[:, 0]], Vv[T[:, 2]] - Vv[T[:, 0]]); N /= np.linalg.norm(N, axis=1)[:, None]; d = (N * Vv[T[:, 0]]).sum(1); return N, d
cellN, celld = hull_planes(cell); bumpP = [hull_planes(b) for b in bumps]; dentP = [hull_planes(d) for d in dents]
sites = []; seen = set()                                        # each edge midpoint belongs to two OCDs: keep one (G, t) per site
for t in [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]:
    for Gk in ring_ops:
        s = Gk @ m + t; key = tuple(np.round(s, 6))
        if np.linalg.norm(s) < 2.6 * R and key not in seen: seen.add(key); sites.append((Gk, t, s))
log('sites', len(sites))
def inside(P, N, d, G, t):
    X = (P - t) @ G                                            # back to the reference frame: G^T (p - t)
    return ((X @ N.T) <= d + 1e-12).all(1)
def membership(P):
    cnt = np.zeros(len(P), int)
    inocd = np.zeros(len(P), int)
    for c in ocd_centres:
        near = np.linalg.norm(P - c, axis=1) < 0.7
        if near.any(): inocd[near] += (((P[near] - c) @ PN.T) <= PD + 1e-12).all(1)
    for Gk, t, s in sites:
        near = np.linalg.norm(P - s, axis=1) < 0.95
        if not near.any(): continue
        Q = P[near]; incell = inside(Q, cellN, celld, Gk, t)
        indent = np.zeros(len(Q), bool)
        for N, d in dentP: indent |= inside(Q, N, d, Gk, t)
        inbump = np.zeros(len(Q), bool)
        for N, d in bumpP: inbump |= inside(Q, N, d, Gk, t)
        cnt[near] += ((incell & (inocd[near] == 0) & ~indent) | inbump)
    return cnt + inocd, inocd
rng = np.random.default_rng(20261018)
def cell_points(n): return rng.random((n, 3)) @ L
def in_cell(P):
    """fold into the lattice parallelepiped and centre it on the origin (all points within 1.9 R of the origin, inside the site coverage)"""
    f = np.linalg.solve(L.T, P.T).T; f -= np.floor(f); return f @ L - np.array([R, R, R])
def near_relief_points(n):
    """points near the bump/dent walls of the reference piece and its ring copies, folded into the lattice cell"""
    out_ = []
    for Gk in ring_ops:
        for B in bumps + dents:
            Bq = B @ Gk.T; k = max(1, n // (12 * len(bumps + dents)))
            w1 = rng.random((k, 8)); w1 /= w1.sum(1)[:, None]; X = w1 @ Bq; X += (10 ** rng.uniform(-6, -2, k) * rng.choice([-1, 1], k))[:, None] * rng.normal(size=(k, 3)) / np.sqrt(3)
            out_.append(X)
    return in_cell(np.vstack(out_))
samp = {}
for kind in ('uniform', 'near_relief', 'near_faces'):
    acc = None
    for rep in range(20):
        if kind == 'uniform': P = in_cell(cell_points(100000))
        elif kind == 'near_relief': P = near_relief_points(100000)
        else:
            P = cell_points(100000); i = rng.integers(0, len(cellN), len(P)); X = P - m; X = X - ((X * cellN[i]).sum(1) - celld[i])[:, None] * cellN[i] + m
            P = in_cell(X + (10 ** rng.uniform(-6, -2, len(P)) * rng.choice([-1, 1], len(P)))[:, None] * cellN[i])
        tot, inocd = membership(P); r = dict(n=len(P), in_no_piece=int((tot == 0).sum()), in_exactly_one=int((tot == 1).sum()), in_two_or_more=int((tot >= 2).sum()))
        acc = r if acc is None else {k: acc[k] + r[k] for k in r}
    samp[kind] = acc; log('sampling', kind, acc)
out['sampling'] = samp; out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(sys.argv[2], 'w')); log('done')
