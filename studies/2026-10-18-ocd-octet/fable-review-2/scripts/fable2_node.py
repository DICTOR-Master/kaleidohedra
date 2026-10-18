# Fable review 2 (2026-10-18), dicto-node part (manifold3d + numpy): float meshes and dense sampling for steps 21-27.
# G = cube(R) at the tetrahedron centre minus the golden envelopes (step 27); W = fcc rhombic dodecahedron at the octet vertex minus the
# envelopes (Fable's achiral alternative); G' = G minus the four phi^-2 vertex cuboctahedra (step-24 style refinement of G).
# For each: solid parts, volume, area, sphericity, genus, dihedral angles (sharpest edges), slivers. Sampling: 2M uniform + 2M near-face
# points per kit, counted into envelopes and glue pieces. usage: python3 fable2_node.py INPUT.json OUT.json
import sys, json, itertools, time, numpy as np, manifold3d as m3
t0 = time.time(); D = json.load(open(sys.argv[1])); RT = np.array(D['RT']); R = D['R']; L = np.array(D['L']); s = D['s']; PHI = (1 + 5 ** .5) / 2
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
def log(*a): print(round(time.time() - t0, 1), 's |', *a, flush=True)
env = hull(RT); sh = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]
allenv = U([env.translate(t) for t in sh if np.linalg.norm(t) < 3.4])
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
def dihedrals(mf):
    """interior dihedral angle at every mesh edge between non-coplanar triangles (degrees); convex < 180 < reflex"""
    M = mf.to_mesh(); V = np.asarray(M.vert_properties[:, :3], float); T = np.asarray(M.tri_verts, int)
    N = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); N /= np.linalg.norm(N, axis=1)[:, None]
    edges = {}
    for ti, t in enumerate(T):
        for k in range(3):
            a, b = t[k], t[(k + 1) % 3]; edges.setdefault((min(a, b), max(a, b)), []).append((ti, t[(k + 2) % 3]))
    out = []
    for (a, b), tri in edges.items():
        if len(tri) != 2: continue
        (t1, c1), (t2, c2) = tri; cs = np.clip(N[t1] @ N[t2], -1, 1); ang = np.degrees(np.arccos(cs))
        if ang < 1e-6: continue
        convex = (V[c2] - V[a]) @ N[t1] < 0
        out.append((180 - ang if convex else 180 + ang, np.linalg.norm(V[a] - V[b])))
    return out
def describe(name, mf, extra=None):
    parts = mf.decompose(); solid = [p for p in parts if p.volume() > 1e-9]
    dh = dihedrals(mf); angs = np.array([a for a, l in dh]); lens = np.array([l for a, l in dh])
    hist = {}
    for a in angs: hist[str(round(a, 1))] = hist.get(str(round(a, 1)), 0) + 1
    M = mf.to_mesh(); V = np.asarray(M.vert_properties[:, :3], float); T = np.asarray(M.tri_verts, int)
    d = dict(volume=mf.volume(), area=mf.surface_area(), sphericity=sph(mf), parts=len(parts), solid_parts=len(solid), slivers=len(parts) - len(solid), genus=mf.genus(),
             corners=len(np.unique(np.round(V, 6), axis=0)), sharpest_edge_deg=float(angs.min()) if len(angs) else None, bluntest_reflex_deg=float(angs.max()) if len(angs) else None,
             dihedral_histogram=dict(sorted(hist.items(), key=lambda kv: float(kv[0]))), edges_below_60deg=int((angs < 60).sum()), total_edge_length_below_60deg=float(lens[angs < 60].sum()))
    if extra: d.update(extra)
    log(name, {k: v for k, v in d.items() if k != 'dihedral_histogram'}); return d
out = dict(mark='DICTO · dictospheres.com', review='Fable review 2 node part')
# G: cube of edge R round the T+ centre
m = np.array([R / 2] * 3); cube = m3.Manifold.cube([R, R, R], True).translate(m); G = cube - allenv
out['G'] = describe('G', G, dict(expected_volume=(1 - 10 / PHI ** 6) * abs(np.linalg.det(L)) / 2))
out['envelope'] = describe('envelope', env)
# W: fcc rhombic dodecahedron (Voronoi cell of the octet vertex v0 = (R,0,0)) minus the envelopes
v0 = np.array([R, 0, 0])
rdpts = [v0 + R * np.eye(3)[k] * sg for k in range(3) for sg in (1, -1)] + [v0 + R / 2 * np.array(sg) for sg in itertools.product((1, -1), repeat=3)]
RD = hull(rdpts); W = RD - allenv
out['W'] = describe('W', W, dict(RD_volume=RD.volume(), RD_sphericity=sph(RD), expected_volume=abs(np.linalg.det(L)) - env.volume()))
# G' = G minus the four phi^-2 vertex cuboctahedra at the cube's octet-vertex corners
def cubo(c):
    pts = []
    for perm in ((0, 1), (0, 2), (1, 2)):
        for sa, sb in itertools.product((1, -1), repeat=2):
            p = c.copy(); p[perm[0]] += s * sa; p[perm[1]] += s * sb; pts.append(p)
    return hull(pts)
vcorners = [np.array(c) for c in itertools.product((0, R), repeat=3) if sum(1 for x in c if x == R) % 2 == 1]
Gp = G - U([cubo(c) for c in vcorners]); out['G_prime'] = describe("G' = G minus 4 cuboctahedron corners", Gp, dict(cubo_volume=cubo(vcorners[0]).volume(), cubo_sphericity=sph(cubo(vcorners[0]))))
out['cuboctahedron'] = describe('vertex cuboctahedron', cubo(vcorners[0]))
# meshes for the record (G and W)
for nm, mf in (('G', G), ('W', W)):
    M = mf.to_mesh(); out[nm]['mesh'] = dict(v=np.round(np.asarray(M.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(M.tri_verts).tolist())
json.dump(out, open(sys.argv[2], 'w')); log('meshes saved')
# ---------------------------------------------------------------- sampling: kit A (envelope + G) and kit B (envelope + W)
rng = np.random.default_rng(20261018)
planes = np.array(D['planes'])        # the 30 exact face planes (unit normal, offset), from fable2_exact's RT
PN, PD = planes[:, :3], planes[:, 3]
ocd_centres = np.array([np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)])
def n_envelopes(P):
    cnt = np.zeros(len(P), int)
    for c in ocd_centres:
        near = np.linalg.norm(P - c, axis=1) < 0.79
        if near.any(): cnt[near] += ((P[near] - c) @ PN.T <= PD + 1e-12).all(1)
    return cnt
def cell_points(n):
    return rng.random((n, 3)) @ L
def boundary_points(n):
    """points near piece faces: half near a random envelope face plane (random envelope), half near a random cube / RD face plane"""
    P = cell_points(n); k = n // 2
    i = rng.integers(0, 30, k); c = ocd_centres[rng.integers(0, len(ocd_centres), k)]
    # project onto the plane of face i of the envelope at c (restricted to its rhombus by rejecting points far from the face centre), then push off
    X = P[:k] - c; X = X - ((X @ PN[i].T).diagonal() - PD[i])[:, None] * PN[i] if False else X - ((X * PN[i]).sum(1) - PD[i])[:, None] * PN[i]
    X = X + c; off = 10 ** rng.uniform(-6, -2, k) * rng.choice([-1, 1], k); X = X + off[:, None] * PN[i]
    Y = P[k:].copy(); ax = rng.integers(0, 3, n - k); Y[np.arange(n - k), ax] = np.round(Y[np.arange(n - k), ax] / R) * R + 10 ** rng.uniform(-6, -2, n - k) * rng.choice([-1, 1], n - k)
    return np.vstack([X, Y])
def in_cell(P):
    """fold points into the fundamental cell spanned by L"""
    f = np.linalg.solve(L.T, P.T).T; f -= np.floor(f); return f @ L
def count_kit(P, glue):
    ne = n_envelopes(P)
    # glue membership: a point outside all envelopes lies in exactly one glue region generically (nearest tet centre for G, nearest vertex for W);
    # count how many glue regions claim it (ties on region boundaries are measure zero)
    if glue == 'G': cen = np.array([np.array(c) * R / 2 for c in itertools.product((-3, -1, 1, 3), repeat=3)])
    else: cen = np.array([R * np.array(c) for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2 == 1])
    d = np.linalg.norm(P[:, None, :] - cen[None], axis=2); dmin = d.min(1); ng = (d <= dmin[:, None] + 1e-12).sum(1) * (ne == 0)
    tot = ne + ng
    return dict(n=len(P), in_no_piece=int((tot == 0).sum()), in_exactly_one=int((tot == 1).sum()), in_two_or_more=int((tot >= 2).sum()), in_two_envelopes=int((ne >= 2).sum()))
samp = {}
for kit in ('G', 'W'):
    for kind in ('uniform', 'boundary'):
        acc = None
        for rep in range(20):
            P = cell_points(100000) if kind == 'uniform' else in_cell(boundary_points(100000)); r = count_kit(P, kit)
            acc = r if acc is None else {k: acc[k] + r[k] for k in r}
        samp[f'{kit}_{kind}'] = acc; log('sampling', kit, kind, acc)
out['sampling'] = samp
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(sys.argv[2], 'w')); log('done')
