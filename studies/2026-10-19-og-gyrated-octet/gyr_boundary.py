# DICTO 2026-10-20: the Penrose-core kit's boundary pieces at twin planes (float first; manifold3d, dicto-node).
# #37 keyless Penrose-core kit: OG, 6 vertex caps per octahedron, a middle piece on every octet edge, tetrahedra; caps and tetrahedra
# notched by the middle pieces. Every edge is shared by two octahedra; its middle piece = hull(the two OGs' five-fold stars nearest the
# edge) minus both OGs. In the octet the second star is the first turned through the edge midpoint (M0); at a twin-plane edge it is
# the first's mirror image (Mg). Three stackings round layer 0 (octahedra centred on R(a,b,c), a+b+c = 0; slab -R <= x+y+z <= R):
#   octet    every layer a translate (sanity: #37 notched cap 0.058072, notched tetrahedron 0.265776)
#   single   one twin plane x+y+z = R; below it the octet
#   gyrated  every layer boundary a twin plane (A B A B)
# For each: the 6 caps of the origin octahedron and the 6 layer-0 tetrahedra on its side faces, minus every middle piece nearby;
# volumes, sphericity, which ones are congruent (and whether by a mirror), per-cell sum, and whether any middle piece leaves the 4 cells
# round its edge.  usage: python3 gyr_boundary.py step10-input.json
import sys, json, itertools, math, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; F = D['faces']
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
sph0 = lambda mf: math.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
sph = lambda mf: sph0(max(mf.decompose(), key=lambda q: q.volume()))   # main solid only (no float films)
r = np.linalg.norm(V, axis=1); FIVE = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
STAR = {i: sorted({j for f in F if i in f for j in f}) for i in FIVE}
J = np.ones((3, 3)); MIR = np.eye(3) - 2 / 3 * J
def mir(k): return (MIR, 2 * k * R / 3 * np.ones(3))          # mirror in x+y+z = kR
def comp(a, b): return (a[0] @ b[0], a[0] @ b[1] + a[1])       # a after b
I = (np.eye(3), np.zeros(3)); SH = lambda v: (np.eye(3), np.asarray(v, float))
def layer_maps(kind, n=2):   # affine map from layer 0 to layer k
    out = {0: I}
    for k in range(1, n + 1):
        for s in (1, -1):
            j = s * k
            if kind == 'octet' or (kind == 'single' and s < 0): out[j] = SH(np.array([1, 1, 0]) * R * j)
            elif kind == 'gyrated': out[j] = comp(mir(2 * j - s), out[j - s])                  # mirror the previous layer in its far face
            else: out[j] = comp(mir(1), out[1 - j])                                         # single, above: mirror of the octet below
    return out
OCT = np.array([[s * R if k == j else 0 for j in range(3)] for k in range(3) for s in (1, -1)])
cent0 = [np.array(c) * R for c in itertools.product(range(-3, 4), repeat=3) if sum(c) == 0]
pts0 = [np.array(c) * R for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2]
e2 = 2 * R * R
tets0 = []   # layer-0 tetrahedra: 4 octet vertices in the slab, pairwise at edge length
slab = [p for p in pts0 if abs(abs(p.sum()) - R) < 1e-9 and np.linalg.norm(p) < 2.9 * R]
for q in itertools.combinations(range(len(slab)), 4):
    Q = [slab[i] for i in q]
    if all(abs(np.dot(a - b, a - b) - e2) < 1e-9 for a, b in itertools.combinations(Q, 2)): tets0.append(np.array(Q))
OG0 = hull(V)
def ap(m, P): return np.asarray(P) @ m[0].T + m[1]
def mesh_ap(mf, m): return mf.transform(np.hstack([m[0], np.asarray(m[1], float)[:, None]]))   # float64 affine map (mirrors keep orientation)
CORNER = hull([[0, 0, 0], [0, 0, R], [R/2, 0, R/2], [-R/2, 0, R/2], [0, R/2, R/2], [0, -R/2, R/2]] + [[a*R/3, b*R/3, R/3] for a in (1, -1) for b in (1, -1)])
G48 = [np.diag(s) @ np.eye(3)[list(p)] for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
def run(kind):
    LM = layer_maps(kind)
    octs = []   # (map from the origin OG to this OG, centre)
    for k, m in LM.items():
        for c in cent0:
            mc = comp(m, SH(c)); cc = ap(mc, np.zeros(3))
            if np.linalg.norm(cc) < 3.2 * R: octs.append((mc, cc, k))
    edges = {}
    for idx, (mc, cc, k) in enumerate(octs):
        for a, b in itertools.combinations(range(6), 2):
            if abs(np.linalg.norm(OCT[a] - OCT[b]) ** 2 - e2) > 1e-9: continue
            mid = ap(mc, (OCT[a] + OCT[b]) / 2); edges.setdefault(tuple(np.round(mid, 6)), []).append(idx)
    Ms = []
    for key, ids in edges.items():
        mid = np.array(key)
        if np.linalg.norm(mid) > 2.0 * R or len(ids) != 2: continue
        stars = []
        for idx in ids:
            mc = octs[idx][0]; W = ap(mc, V); i = min(FIVE, key=lambda i: np.linalg.norm(W[i] - mid)); stars.append(W[STAR[i]])
        H = hull(np.vstack(stars)); M = H - mesh_ap(OG0, octs[ids[0]][0]) - mesh_ap(OG0, octs[ids[1]][0])
        twin = np.linalg.det(octs[ids[0]][0][0]) != np.linalg.det(octs[ids[1]][0][0])
        Ms.append(dict(mid=mid, M=M, twin=twin, ids=ids))
    Mall = U([x['M'] for x in Ms])
    caps = []
    for v in OCT:
        # the cap region at v: CORNER turned so (0,0,R) goes to v (any octahedral turn will do: the region is the Voronoi-like corner cut)
        A = next(g for g in G48 if np.linalg.det(g) > 0 and np.allclose(g @ np.array([0, 0, R]), v))   # the region has the vertex's 4-fold symmetry
        reg = mesh_ap(CORNER, (A, np.zeros(3)))
        caps.append(dict(v=v, plane=round(v.sum() / R), P=reg - OG0 - Mall, full=reg - OG0))
    tets = []
    for Q in tets0:
        cQ = Q.mean(0)
        sharesface = sum(abs(np.abs(p).sum() - R) < 1e-9 for p in Q) == 3   # three corners on the origin octahedron
        if not sharesface: continue
        up = sum(abs(p.sum() - R) < 1e-9 for p in Q) == 3
        tets.append(dict(c=cQ, face='+R' if up else '-R', P=hull(Q) - Mall))
    return Ms, caps, tets
def inv(mf):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)
    return P, T
OPS = G48 + [MIR @ g for g in G48] + [-MIR @ g for g in G48]
def centre(mf):
    P, T = inv(mf); v = 0; c = np.zeros(3)
    for i, j, k in T: x = np.linalg.det(P[[i, j, k]]) / 6; v += x; c += x * (P[i] + P[j] + P[k]) / 4
    return c / v
def same(a, b):   # congruent by one of the lattice's point maps + translation?  test: the mapped piece overlaps b in all of its volume
    if abs(a.volume() - b.volume()) > 1e-6: return None
    ca, cb = centre(a), centre(b)
    for g in OPS:
        a2 = a.transform(np.hstack([g, (cb - g @ ca)[:, None]]))
        if b.volume() - (a2 ^ b).volume() < 1e-6: return bool(np.linalg.det(g) < 0)
    return None
def classes(items, key):
    cl = []
    for it in items:
        for c in cl:
            s = same(c[0][key], it[key])
            if s is not None: c.append(it); c[-1]['mirror_of_first'] = s; break
        else: it['mirror_of_first'] = False; cl.append([it])
    return cl
REF = {}
for kind in ('octet', 'single', 'gyrated'):
    Ms, caps, tets = run(kind)
    print(f'\n== {kind}: middle pieces near the origin {len(Ms)} (twin-plane {sum(x["twin"] for x in Ms)})')
    mv = sorted({round(x['M'].volume(), 6) for x in Ms}); print('  middle-piece volumes', mv)
    for nm, items in (('caps', caps), ('tetrahedra', tets)):
        cl = classes(items, 'P')
        for c in cl:
            p = c[0]['P']; parts = len([q for q in p.decompose() if q.volume() > 1e-7])
            lab = [(f"v{tuple(int(round(t / R)) for t in it['v'])}" if nm == 'caps' else f"face {it['face']}") + ('(m)' if it['mirror_of_first'] else '') for it in c]
            print(f'  {nm}: volume {p.volume():.6f}  sphericity {sph(p):.3f}  parts {parts}  x{len(c)}: {", ".join(lab)}')
    # per-cell check (gyrated/octet: every cap and tet of the cell): OG + 6 caps + 2 tets + middle pieces' share = octahedron + 2 tetrahedra
    if kind != 'single':
        # the origin octahedron and its 6 caps own: OG + caps + (its region of the middle pieces); sum over 6 caps + 6/6 tets/3 ...
        octa = hull(OCT); allc = sum(c['P'].volume() for c in caps); tv = sum(t['P'].volume() for t in tets) / 3   # each tet touches 3 octahedra of the layer
        Mo = sum((x['M'] ^ octa).volume() for x in Ms)
        print(f'  origin octahedron: OG {OG0.volume():.6f} + caps {allc:.6f} + middle pieces inside it {Mo:.6f} = {OG0.volume() + allc + Mo:.6f} vs octahedron {octa.volume():.6f}')
    # does any middle piece leave the 4 cells round its edge?  (test: inside the union of the 2 octahedra + 2 tetrahedra at that edge)
    bad = 0
    for x in Ms:
        if np.linalg.norm(x['mid']) > 1.1 * R: continue
        P, _ = inv(x['M']); far = np.linalg.norm(P - x['mid'], axis=1).max()
        bad = max(bad, far)
    print(f'  largest reach of a middle piece from its edge midpoint {bad:.4f} (octet edge {math.sqrt(e2):.4f})')
    REF[kind] = dict(caps=[c['P'].volume() for c in caps], tets=[t['P'].volume() for t in tets])
