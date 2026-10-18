# Fable review 5, PHASE 2, dicto-node (manifold3d): build the W with the continuous creased-kite relief from data/relief-geometry.json and
# check: one solid, identical W (2/m symmetry of the piece: sigma and iota images), 12 round one OCD without overlap (union = 12 W + OCD),
# OCD + W fills space (1M uniform + 0.5M near-face points, 0/0). Meshes for the page. usage: fable5_node.py GEOM.json OUT.json
import sys, json, itertools, time, numpy as np, manifold3d as m3
t0 = time.time(); D = json.load(open(sys.argv[1])); R = D['R']; m = np.array(D['m']); cell = np.array(D['cell']); V = np.array(D['ocd_V']); F = D['faces']; REL = np.array(D['relief_triangles_uvh'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
out_pre = {}
def log(*a): print(round(time.time() - t0, 1), 's |', *a, flush=True)
L = np.array([[R, R, 0], [R, 0, R], [0, R, R]]); OCD = hull(V); DEL = 0.08; tri2 = np.array([[0, 0], [R, 0], [R / 2, R / np.sqrt(2)]])
def to3(f, u, w, h):
    A, Uv, Wv, N = (np.array(f[k]) for k in ('A', 'U', 'W', 'N')); return A + np.outer(u, Uv) + np.outer(w, Wv) + np.outer(h, N)
DEL = 0.08
def slab_mesh():
    """one watertight mesh (in u, w, h) of the slab under the relief of the reference face: top = relief triangles, bottom at -DEL, side walls"""
    key = lambda q: (round(q[0], 9), round(q[1], 9)); verts = {}; order = []
    def vid(q, h):
        k = key(q)
        if k not in verts: verts[k] = (len(order), h); order.append((k[0], k[1], h))
        return verts[k][0]
    tris = []
    for tr in REL:
        ids = [vid(q, q[2]) for q in tr]; a_, b_, c_ = (np.array(order[k][:2]) for k in ids)
        if (b_ - a_)[0] * (c_ - a_)[1] - (b_ - a_)[1] * (c_ - a_)[0] < 0: ids = [ids[0], ids[2], ids[1]]
        if len(set(ids)) == 3: tris.append(ids)
    corners = [(0.0, 0.0), (R, 0.0), (R / 2, R / np.sqrt(2))]; cen = np.mean(corners, axis=0)
    nb = len(order); bot = [nb, nb + 1, nb + 2]; order += [(c[0], c[1], -DEL) for c in corners]
    tris.append([bot[0], bot[2], bot[1]])                                                   # bottom, facing down
    for e in range(3):
        C1, C2 = np.array(corners[e]), np.array(corners[(e + 1) % 3]); d = C2 - C1; Ln = d @ d
        chain = [k for k, (u, w, h) in enumerate(order[:nb]) if abs(d[0] * (w - C1[1]) - d[1] * (u - C1[0])) / np.sqrt(Ln) < 1e-9 and -1e-9 <= ((u - C1[0]) * d[0] + (w - C1[1]) * d[1]) / Ln <= 1 + 1e-9]
        chain.sort(key=lambda k: (order[k][0] - C1[0]) * d[0] + (order[k][1] - C1[1]) * d[1])
        assert max(abs(order[k][2]) for k in chain) < 1e-9, 'relief not zero on the face boundary'
        wall = [[bot[e], chain[k], chain[k + 1]] for k in range(len(chain) - 1)] + [[bot[e], chain[-1], bot[(e + 1) % 3]]]
        out_n = np.array([-d[1], d[0]]) if (np.array([-d[1], d[0]]) @ (cen - C1)) < 0 else np.array([d[1], -d[0]])   # outward in-plane normal of this edge
        for t in wall:
            P3 = np.array([order[k] for k in t]); nrm = np.cross(P3[1] - P3[0], P3[2] - P3[0])
            tris.append(t if nrm[:2] @ out_n > 0 else [t[0], t[2], t[1]])
    return np.array(order, float), np.array(tris, np.uint32)
UVH, TRI = slab_mesh()
def slab(f, T):
    P3 = to3(f, UVH[:, 0], UVH[:, 1], f['sign'] * UVH[:, 2]); P3 = T(P3)
    Uv, Wv, N = np.array(f['U']), np.array(f['W']), np.array(f['N']); hand = np.linalg.det(np.c_[Uv, Wv, N]) * f['sign'] * np.linalg.det(np.asarray(T(np.eye(3))))
    tri = TRI if hand > 0 else TRI[:, [0, 2, 1]]
    mesh = m3.Mesh(vert_properties=np.asarray(P3, np.float32), tri_verts=np.asarray(tri, np.uint32)); M = m3.Manifold(mesh)
    assert M.volume() > 0 and M.num_vert() > 0, f'slab mesh invalid: status {M.status()}'
    return M
def keyed(G=np.eye(3)):
    T = lambda X: X @ G.T
    base = hull(T(cell)) - OCD - OCD.translate(T(np.array([0, R, R])))
    prisms = [hull(T(np.vstack([to3(f, tri2[:, 0], tri2[:, 1], -DEL * np.ones(3)), to3(f, tri2[:, 0], tri2[:, 1], DEL * np.ones(3))]))) for f in F.values()]
    slabs = [slab(f, T) for f in F.values()]
    return ((base - U(prisms)) + U(slabs)) - OCD - OCD.translate(T(np.array([0, R, R])))
W = keyed(); Wstar = hull(cell) - OCD - OCD.translate([0, R, R])
parts = W.decompose()
out = dict(mark='DICTO · dictospheres.com', W=dict(volume=W.volume(), W_star_volume=Wstar.volume(), parts=len(parts), solid_parts=len([p for p in parts if p.volume() > 1e-9]), genus=W.genus(), area=W.surface_area(),
           corners=len(np.unique(np.round(np.asarray(W.to_mesh().vert_properties[:, :3]), 6), axis=0)), relief_triangles_per_face=len(REL)))
log('W', out['W'])
# identical W: the piece's own 2/m symmetry (sigma: x -> -x; iota: inversion through m) -- symmetric difference volumes
sig = W.transform(np.c_[np.diag([-1., 1, 1]), np.zeros(3)]); iot = W.translate(-m).transform(np.c_[-np.eye(3), np.zeros(3)]).translate(m)
out['symmetry'] = dict(sigma_symdiff=(W + sig).volume() - (W ^ sig).volume(), iota_symdiff=(W + iot).volume() - (W ^ iot).volume())
log('symmetry', out['symmetry'])
# 12 round one OCD
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
ring_ops = list(ring.values()); pieces = [W.transform(np.c_[Gk, np.zeros(3)]) for Gk in ring_ops]
ov = max((pieces[a] ^ pieces[b]).volume() for a, b in itertools.combinations(range(12), 2)); ocd_ov = max((p ^ OCD).volume() for p in pieces)
ru = U(pieces + [OCD]); out['ring12'] = dict(max_pairwise_overlap=ov, max_overlap_with_OCD=ocd_ov, union_volume=ru.volume(), expected=12 * W.volume() + OCD.volume(), gap=12 * W.volume() + OCD.volume() - ru.volume())
log('ring', out['ring12'])
# pair across face 1: neighbour g(W), g = (x,y,z)->(y,z,x)
Gg = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float); Wj = W.transform(np.c_[Gg, np.zeros(3)])
both = (hull(cell) + hull(cell @ Gg.T)) - OCD - OCD.translate([0, R, R]) - OCD.translate([R, R, 0])
out['pair_face1'] = dict(overlap=(W ^ Wj).volume(), union=(W + Wj).volume(), cells_minus_OCDs=both.volume(), gap=both.volume() - (W + Wj).volume())
log('pair', out['pair_face1'])
for nm, mf in (('W', W), ('W_star', Wstar)):
    M = mf.to_mesh(); out[nm + '_mesh'] = dict(v=np.round(np.asarray(M.vert_properties[:, :3], float) - m, 6).tolist(), t=np.asarray(M.tri_verts).tolist())
M = OCD.to_mesh(); out['ocd_mesh'] = dict(v=np.round(np.asarray(M.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(M.tri_verts).tolist())
json.dump(out, open(sys.argv[2], 'w')); log('meshes saved')
# ---------------------------------------------------------------- sampling: piece at site s = G m + t is G W + t; membership by the height field
PL = []
Mh = OCD.to_mesh(); Vh = np.asarray(Mh.vert_properties[:, :3]); Th = np.asarray(Mh.tri_verts); Nn = np.cross(Vh[Th[:, 1]] - Vh[Th[:, 0]], Vh[Th[:, 2]] - Vh[Th[:, 0]]); Nn /= np.linalg.norm(Nn, axis=1)[:, None]
PN, PD = Nn, (Nn * Vh[Th[:, 0]]).sum(1)                           # triangle planes of the OCD (redundant copies are harmless)
fr = [(np.array(f['A']), np.array(f['U']), np.array(f['W']), np.array(f['N']), f['sign']) for f in F.values()]
def relief_height(u, w):
    """height field of the reference face (sign +) at points (u, w): the relief triangle containing the point (0 outside the face)"""
    hgt = np.zeros(len(u)); done = np.zeros(len(u), bool)
    for tr in REL:
        (x1, y1, h1), (x2, y2, h2), (x3, y3, h3) = tr; det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        l1 = ((y2 - y3) * (u - x3) + (x3 - x2) * (w - y3)) / det; l2 = ((y3 - y1) * (u - x3) + (x1 - x3) * (w - y3)) / det; l3 = 1 - l1 - l2
        inside = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9) & ~done
        hgt[inside] = (l1 * h1 + l2 * h2 + l3 * h3)[inside]; done |= inside
    return hgt
def in_piece(P, Gk, t):
    X = (P - t) @ Gk                                              # back to the reference frame
    ok = np.ones(len(P), bool)
    for A, Uv, Wv, N, sign in fr:
        Y = X - A; u, w, h = Y @ Uv, Y @ Wv, Y @ N
        near = np.abs(h) < 0.06
        lim = np.zeros(len(P))
        if near.any(): lim[near] = sign * relief_height(u[near], w[near])
        ok &= h <= lim + 1e-12
    return ok
ocd_centres = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]; rO = np.linalg.norm(V, axis=1).max()
sites = []; seen = set()
for t in [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]:
    for Gk in ring_ops:
        s_ = Gk @ m + t; key = tuple(np.round(s_, 6))
        if np.linalg.norm(s_) < 2.6 * R and key not in seen: seen.add(key); sites.append((Gk, t, s_))
def membership(P):
    cnt = np.zeros(len(P), int); inocd = np.zeros(len(P), int)
    for c in ocd_centres:
        near = np.linalg.norm(P - c, axis=1) < rO + 1e-6
        if near.any(): inocd[near] += (((P[near] - c) @ PN.T) <= PD + 1e-12).all(1)
    for Gk, t, s_ in sites:
        near = np.linalg.norm(P - s_, axis=1) < 0.95
        if near.any(): cnt[near] += in_piece(P[near], Gk, t) & (inocd[near] == 0)
    return cnt + inocd
rng = np.random.default_rng(20261018)
def in_cell(P):
    f = np.linalg.solve(L.T, P.T).T; f -= np.floor(f); return f @ L - np.array([R, R, R])
samp = {}
for kind, n in (('uniform', 1000000), ('near_faces', 500000)):
    acc = None
    for rep in range(n // 100000):
        P = in_cell(rng.random((100000, 3)) @ L)
        if kind == 'near_faces':
            k = rng.integers(0, 8, len(P)); fsel = [fr[i] for i in range(8)]
            A = np.array([fsel[i][0] for i in k]); N = np.array([fsel[i][3] for i in k]); h = ((P - A) * N).sum(1)
            P = in_cell(P - h[:, None] * N + (10 ** rng.uniform(-6, -1.3, len(P)) * rng.choice([-1, 1], len(P)))[:, None] * N)
        tot = membership(P); r = dict(n=len(P), in_no_piece=int((tot == 0).sum()), in_exactly_one=int((tot == 1).sum()), in_two_or_more=int((tot >= 2).sum()))
        acc = r if acc is None else {kk: acc[kk] + r[kk] for kk in r}
    samp[kind] = acc; log('sampling', kind, acc)
out['sampling'] = samp; out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(sys.argv[2], 'w')); log('done')
