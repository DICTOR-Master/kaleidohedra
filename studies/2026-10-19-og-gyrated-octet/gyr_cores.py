# DICTO 2026-10-20: do the Penrose-core (P2) middle pieces still work in the gyrated octet? Float first (manifold3d, dicto-node).
# Lower layer = the #37 octet (OG at the origin, octahedron |x|+|y|+|z| <= R); twin plane x+y+z = R; upper layer = its mirror image.
# Only edges lying in the twin plane change neighbours: round them the cells run O T | T O (the two OGs are mirror images across a
# shared face) instead of O T O T (two OGs facing by inversion through the edge midpoint, the P2 middle piece).
# usage: python3 gyr_cores.py step10-input.json
import sys, json, itertools, math, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; L = np.array(D['L'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
vol = lambda mf: mf.volume(); sph = lambda mf: math.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
n1 = np.ones(3) / math.sqrt(3); mir = lambda P: P - 2 * ((P @ n1 - R / math.sqrt(3))[..., None]) * n1
OG = hull(V); r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
star = lambda i: V[sorted({j for f in D['faces'] if i in f for j in f})]
octa = lambda c: hull(c + np.array([[s * R if k == j else 0 for j in range(3)] for k in range(3) for s in (1, -1)]))

# lower layer: octet octahedra with centre sum <= 0 near the joint; upper layer = their mirror images
cent = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
low = [c for c in cent if c.sum() <= 1e-9 and np.linalg.norm(c - R * n1 * math.sqrt(3) / 3) < 2.6]
def M0(c, i):  # the P2 middle piece of octahedron c at its five-fold corner i (partner OG across the edge at o)
    ci = V[i]; o = R * np.sign(np.where(np.abs(ci) < 1e-9, 0, ci)); s = star(i) + c
    return hull(np.vstack([s, 2 * c + o - s])) - OG.translate(c) - OG.translate(c + o), c + o / 2
edges = {}
for c in low:
    for i in five:
        ci = V[i]; o = R * np.sign(np.where(np.abs(ci) < 1e-9, 0, ci)); m = c + o / 2; key = tuple(np.round(m, 6))
        if key in edges: continue
        if (c + o).sum() <= 1e-9: edges[key] = ('low', c, i)            # both OGs in the lower layer: P2 piece as before
        elif abs(m.sum() - R) < 1e-9: edges[key] = ('plane', c, i)     # edge in the twin plane
print('lower octahedra', len(low), '| lower edges', sum(1 for e in edges.values() if e[0] == 'low'), '| plane edges', sum(1 for e in edges.values() if e[0] == 'plane'))

# 1. the facing corners at a plane edge: fcc partner c2 (inversion through m) vs the twin's corner c1' (mirror)
i1 = [i for i in five if (np.sign(np.round(V[i], 9)) == [1, 1, 0]).all()][0]; c1 = V[i1]; o = R * np.array([1, 1, 0]); m = o / 2
c2 = o - c1; c1m = mir(c1); u = c1 / np.linalg.norm(c1)
tw = mir(np.zeros(3)); u_m = (c1m - tw) / np.linalg.norm(c1m - tw)
for name, p, up in (('fcc partner c2', c2, -u), ('twin corner c1\'', c1m, u_m)):
    d = p - c1; print(f'{name}: |c1-p| {np.linalg.norm(d):.4f}, along c1 axis {d @ u:+.4f}, sideways {np.linalg.norm(d - (d @ u) * u):.4f}, axis angle to c1 {math.degrees(math.acos(np.clip(up @ u, -1, 1))):.2f} deg')
print(f'c1 itself: distance from the twin plane {(R / math.sqrt(3) - c1 @ n1):.4f}; distance from edge midpoint {np.linalg.norm(c1 - m):.4f}')

# 2. does the old P2 piece survive at a plane edge? (it assumes an OG at o, which the twin layer does not have)
TW = hull(mir(V)); M0p, _ = M0(np.zeros(3), i1)
big = 30

# 3. the mirror middle piece Mg at a plane edge: hull(star + its mirror) minus both OGs
def Mg(c, i):
    s = star(i) + c; return hull(np.vstack([s, mir(s)])) - OG.translate(c) - hull(mir(V + c))
G = Mg(np.zeros(3), i1)
print(f'mirror middle piece Mg: volume {vol(G):.6f} (P2 piece 0.079735), sphericity {sph(G):.3f} (P2 0.579), parts {len([p for p in G.decompose() if p.volume() > 1e-9])}')
# 4. clashes: every piece against every other, against all OGs (lower + twin), and lower pieces crossing the plane
pieces = []
for key, (kind, c, i) in edges.items():
    if kind == 'low':
        p, mm = M0(c, i); pieces.append(('low', mm, p))
    else: pieces.append(('plane', np.array(key), Mg(c, i)))
# mirror images of lower pieces as real solids (mesh reflection keeps volume; hull would not, pieces are not convex)
def reflect(mf):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)[:, ::-1]
    return m3.Manifold(m3.Mesh(vert_properties=np.ascontiguousarray(mir(P), dtype=np.float32), tri_verts=np.ascontiguousarray(T, dtype=np.uint32)))
pieces += [('up', mir(mm), reflect(p)) for k, mm, p in list(pieces) if k == 'low']
OGs = [OG.translate(c) for c in low] + [reflect(OG.translate(c)) for c in low]
near = [(k, mm, p) for k, mm, p in pieces if np.linalg.norm(mm - m) < 1.6]
print('pieces near the test edge', len(near), {k: sum(1 for x in near if x[0] == k) for k in ('low', 'plane', 'up')})
over = {}
for (ka, ma, pa), (kb, mb, pb) in itertools.combinations(near, 2):
    if np.linalg.norm(ma - mb) > 1.4: continue
    v = vol(pa ^ pb)
    if v > 1e-7: over[(ka, kb)] = over.get((ka, kb), 0) + v
print('piece-piece overlaps by kind (total volume):', {k: round(v, 6) for k, v in over.items()} or 'none')
ogc = {}
for k, mm, p in near:
    v = sum(vol(p ^ g) for g in OGs)
    if v > 1e-7: ogc[k] = ogc.get(k, 0) + v
print('pieces inside any OG:', {k: round(v, 6) for k, v in ogc.items()} or 'none')
# lower P2 pieces poking across the twin plane (into the upper layer)
# build the upper half-space as a hull of a big box placed beyond the plane
box = hull([R / math.sqrt(3) * n1 + big * (s1 * e1 + s2 * e2) + t * n1 for s1 in (-1, 1) for s2 in (-1, 1) for t in (0, big)
            for e1, e2 in [(np.cross(n1, [1, 0, 0]) / np.linalg.norm(np.cross(n1, [1, 0, 0])), np.cross(n1, np.cross(n1, [1, 0, 0])) / np.linalg.norm(np.cross(n1, np.cross(n1, [1, 0, 0]))))]])
cross_ = sum(vol(p ^ box) for k, mm, p in near if k == 'low')
print(f'lower P2 pieces reaching across the twin plane: total {cross_:.6f}')
print(f'Mg above the plane {vol(G ^ box):.6f} below {vol(G) - vol(G ^ box):.6f} (a mirror piece splits evenly)')
print(f'old P2 piece at the plane edge: above the plane {vol(M0p ^ box):.6f}, of which inside the twin OG {vol(M0p ^ TW):.6f}')
