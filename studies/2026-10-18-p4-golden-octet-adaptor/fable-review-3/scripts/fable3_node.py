# Fable review 3 (2026-10-18), dicto-node part (manifold3d + numpy): OCD + W_OCD (vertex-centred glue) and OCD + W_star (edge-midpoint
# glue). Float meshes: parts, genus, volume, area, sphericity, dihedral histogram, sharpest edge; dense sampling 2M uniform + 2M near-face
# points per kit. usage: python3 fable3_node.py INPUT.json OUT.json
import sys, json, itertools, time, numpy as np, manifold3d as m3
t0 = time.time(); D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; L = np.array(D['L']); planes = np.array(D['planes']); PN, PD = planes[:, :3], planes[:, 3]
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
def log(*a): print(round(time.time() - t0, 1), 's |', *a, flush=True)
OCD = hull(V); sh = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]
allocd = U([OCD.translate(t) for t in sh if np.linalg.norm(t) < 3.4])
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
def dihedrals(mf):
    M = mf.to_mesh(); Vv = np.asarray(M.vert_properties[:, :3], float); T = np.asarray(M.tri_verts, int)
    N = np.cross(Vv[T[:, 1]] - Vv[T[:, 0]], Vv[T[:, 2]] - Vv[T[:, 0]]); N /= np.linalg.norm(N, axis=1)[:, None]
    edges = {}
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
def describe(name, mf, extra=None):
    parts = mf.decompose(); solid = [p for p in parts if p.volume() > 1e-9]
    dh = dihedrals(mf); angs = np.array([a for a, l in dh]); lens = np.array([l for a, l in dh]); hist = {}
    for a in angs: hist[str(round(a, 1))] = hist.get(str(round(a, 1)), 0) + 1
    M = mf.to_mesh(); Vv = np.asarray(M.vert_properties[:, :3], float)
    d = dict(volume=mf.volume(), area=mf.surface_area(), sphericity=sph(mf), parts=len(parts), solid_parts=len(solid), slivers=len(parts) - len(solid), genus=mf.genus(),
             corners=len(np.unique(np.round(Vv, 6), axis=0)), sharpest_edge_deg=float(angs.min()), bluntest_reflex_deg=float(angs.max()),
             dihedral_histogram=dict(sorted(hist.items(), key=lambda kv: float(kv[0]))), edges_below_60deg=int((angs < 60).sum()), total_edge_length_below_60deg=float(lens[angs < 60].sum()))
    if extra: d.update(extra)
    log(name, {k: v for k, v in d.items() if k != 'dihedral_histogram'}); return d
out = dict(mark='DICTO · dictospheres.com', review='Fable review 3 node part')
out['OCD'] = describe('OCD', OCD)
# W_OCD: RD round the vertex v0 = (0,0,R)
v0 = np.array([0, 0, R]); RD = hull([v0 + R * np.eye(3)[k] * sg for k in range(3) for sg in (1, -1)] + [v0 + R / 2 * np.array(s) for s in itertools.product((1, -1), repeat=3)])
W = RD - allocd; out['W_OCD'] = describe('W_OCD', W, dict(expected_volume=abs(np.linalg.det(L)) - OCD.volume()))
# W_star: octahedron cell round the edge midpoint m = (0, R/2, R/2)
m = np.array([0, R / 2, R / 2]); cellpts = [np.zeros(3), np.array([0, R, R]), np.array([0, R, 0]), np.array([0, 0, R]), np.array([R / 2, R / 2, R / 2]), np.array([-R / 2, R / 2, R / 2])]
Vor = hull(cellpts); Ws = Vor - allocd; out['W_star'] = describe('W_star', Ws, dict(expected_volume=(abs(np.linalg.det(L)) - OCD.volume()) / 6, voronoi_volume=Vor.volume()))
for nm, mf in (('W_OCD', W), ('W_star', Ws)):
    M = mf.to_mesh(); out[nm]['mesh'] = dict(v=np.round(np.asarray(M.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(M.tri_verts).tolist())
json.dump(out, open(sys.argv[2], 'w')); log('meshes saved')
# thickness of W_star along the edge axis u = (0,1,1)/sqrt2 at radial offsets from m (float, exact planes): gap between the two OCD surfaces
u = np.array([0, 1, 1]) / np.sqrt(2); e1 = np.array([1, 0, 0]); e2 = np.array([0, 1, -1]) / np.sqrt(2); c2 = np.array([0, R, R])
def exit_along(c, p0, d):
    """largest t with p0 + t d inside OCD at c (ray from inside), or None if p0 outside"""
    x = p0 - c
    if not ((x @ PN.T) <= PD + 1e-12).all(): return None
    den = PN @ d; num = PD - PN @ x; ts = num[den > 1e-15] / den[den > 1e-15]; return ts.min()
thick = {}
for rho in (0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3):
    vals = []
    for th in np.linspace(0, 2 * np.pi, 72, endpoint=False):
        p = m + rho * (np.cos(th) * e1 + np.sin(th) * e2)
        # walk from p towards -u until entering OCD1 (surface), and towards +u until entering OCD2; thickness = sum of the two free lengths
        def free(d, c):
            x = p - c; den = PN @ d; num = PD - PN @ x
            # entry into the convex OCD along the ray p + t d, t > 0: t_in = max over planes with den<0 of num/den, valid if <= min over den>0
            tin = (num[den < -1e-15] / den[den < -1e-15]).max() if (den < -1e-15).any() else -np.inf
            tout = (num[den > 1e-15] / den[den > 1e-15]).min()
            return tin if tin <= tout and tin > 0 else np.inf
        vals.append(free(-u, np.zeros(3)) + free(u, c2))
    thick[str(rho)] = dict(min=float(np.min(vals)), max=float(np.max(vals)))
out['W_star_axial_thickness_vs_radial_offset'] = thick; log('thickness', thick)
# ---------------------------------------------------------------- sampling
rng = np.random.default_rng(20261018)
ocd_centres = np.array([np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)])
rO = np.linalg.norm(V, axis=1).max()
def n_ocds(P):
    cnt = np.zeros(len(P), int)
    for c in ocd_centres:
        near = np.linalg.norm(P - c, axis=1) < rO + 1e-6
        if near.any(): cnt[near] += ((P[near] - c) @ PN.T <= PD + 1e-12).all(1)
    return cnt
def cell_points(n): return rng.random((n, 3)) @ L
def in_cell(P):
    f = np.linalg.solve(L.T, P.T).T; f -= np.floor(f); return f @ L
verts = np.array([R * np.array(c) for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2 == 1])
mids = np.array([np.array(s) * R / 2 for s in itertools.product(range(-6, 7), repeat=3) if sum(1 for x in s if x % 2) == 2])
cut_normals = dict(W_OCD=np.array([[1, 1, 0], [1, -1, 0], [1, 0, 1], [1, 0, -1], [0, 1, 1], [0, 1, -1]], float) / np.sqrt(2),
                   W_star=np.array([[1, 1, 0], [1, -1, 0], [1, 0, 1], [1, 0, -1], [0, 1, 1], [0, 1, -1], [1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]], float))
def boundary_points(n, kit):
    P = cell_points(n); k = n // 2
    i = rng.integers(0, len(PN), k); c = ocd_centres[rng.integers(0, len(ocd_centres), k)]
    X = P[:k] - c; X = X - ((X * PN[i]).sum(1) - PD[i])[:, None] * PN[i] + c; X = X + (10 ** rng.uniform(-6, -2, k) * rng.choice([-1, 1], k))[:, None] * PN[i]
    # near a cut plane: project the point onto the nearest cut plane of its own region (bisector with a neighbouring site)
    sites = verts if kit == 'W_OCD' else mids
    Y = P[k:]; d = np.linalg.norm(Y[:, None, :] - sites[None], axis=2); order = np.argsort(d, axis=1); s1 = sites[order[:, 0]]; s2 = sites[order[:, 1]]
    nrm = s2 - s1; nrm /= np.linalg.norm(nrm, axis=1)[:, None]; mid = (s1 + s2) / 2
    Y = Y - ((Y - mid) * nrm).sum(1)[:, None] * nrm + (10 ** rng.uniform(-6, -2, n - k) * rng.choice([-1, 1], n - k))[:, None] * nrm
    return np.vstack([X, Y])
def count_kit(P, kit):
    ne = n_ocds(P); sites = verts if kit == 'W_OCD' else mids
    d = np.linalg.norm(P[:, None, :] - sites[None], axis=2); dmin = d.min(1); ng = (d <= dmin[:, None] + 1e-12).sum(1) * (ne == 0); tot = ne + ng
    return dict(n=len(P), in_no_piece=int((tot == 0).sum()), in_exactly_one=int((tot == 1).sum()), in_two_or_more=int((tot >= 2).sum()), in_two_OCDs=int((ne >= 2).sum()))
samp = {}
for kit in ('W_OCD', 'W_star'):
    for kind in ('uniform', 'boundary'):
        acc = None
        for rep in range(20):
            P = cell_points(100000) if kind == 'uniform' else in_cell(boundary_points(100000, kit)); r = count_kit(P, kit)
            acc = r if acc is None else {k: acc[k] + r[k] for k in r}
        samp[f'{kit}_{kind}'] = acc; log('sampling', kit, kind, acc)
out['sampling'] = samp; out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(sys.argv[2], 'w')); log('done')
