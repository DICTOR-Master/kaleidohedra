# DICTO 2026-10-18 keyed star-centred W (3D model): "I want this piece ... to have the rhombi pattern continued along its edges as a key
# with itself" -> "I want a 3d model". The rhombus pattern of the OCD imprint (its kites: long edge 0.2379, the two kite-edge directions
# that pierce the face, 61.62 deg and 118.38 deg in the face) is continued as a rhombus lattice over the free part of each flat face.
# Bump faces {0,1,6,7} (exact pairing, data/p4-key-pairing.json) carry every other rhombus raised by H; each neighbouring W (the same
# piece, moved by a symmetry of the structure) pushes its raised rhombi into this W's dent faces {2,3,4,5}. All W stay identical.
# dicto-node, manifold3d. usage: python3 p4_keyed_W.py step10-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
from scipy.spatial import HalfspaceIntersection
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; L = np.array(D['L'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
H, S_EDGE, MARGIN = 0.05, 0.2379, 0.02
m0 = np.array([0, R / 2, R / 2])
def cell(m):
    sites = [np.array(s) * R / 2 for s in itertools.product(range(-6, 7), repeat=3) if sum(1 for x in s if x % 2) == 2]
    hs = [np.r_[p - m, -(p - m) @ ((p + m) / 2)] for p in sites if 1e-9 < np.linalg.norm(p - m) < 2.5 * R]
    return hull(HalfspaceIntersection(np.array(hs), m).intersections)
OCD = hull(V); sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
W0 = cell(m0) - U([OCD.translate(t) for t in sh if np.linalg.norm(t - m0) < 1.5])
# face 0: A (OCD centre), E (edge end), T (tetrahedron centre); outward normal away from m0
A, E, T = np.zeros(3), np.array([0, R, 0]), np.array([-R / 2, R / 2, R / 2])
u = (E - A) / R; nrm = np.cross(E - A, T - A); nrm /= np.linalg.norm(nrm)
if nrm @ (m0 - A) > 0: nrm = -nrm
w = np.cross(nrm, u)
to3 = lambda p: A + p[0] * u + p[1] * w
d1 = np.array([np.cos(np.radians(61.62)), np.sin(np.radians(61.62))]); d2 = np.array([np.cos(np.radians(118.38)), np.sin(np.radians(118.38))])
anchor = np.array([0.588, 0.2913])                     # where an OCD kite edge pierces the face
tri = np.array([[0, 0], [R, 0], [R / 2, (np.linalg.norm(T - A) ** 2 - (R / 2) ** 2) ** .5]])
OCDf = np.array(json.load(open(sys.argv[3]))['ocd']) if len(sys.argv) > 3 else None
def in_tri(p, mg):
    a, b, c = tri; cen = tri.mean(0)
    for P, Q in ((a, b), (b, c), (c, a)):
        e = Q - P; nn = np.array([e[1], -e[0]]); nn /= np.linalg.norm(nn)
        if (cen - P) @ nn < 0: nn = -nn
        if (p - P) @ nn < mg: return False
    return True
def outside_ocd(p):   # the OCD imprint on this face = OCD section; test in 3D with the OCD's planes, margin MARGIN
    q = to3(p); eqs = np.array(OCDeq); return np.max(eqs[:, :3] @ q + eqs[:, 3]) > MARGIN
from scipy.spatial import ConvexHull
OCDeq = ConvexHull(V).equations
tiles = []
for i, j in itertools.product(range(-8, 9), repeat=2):
    if (i + j) % 2: continue                            # every other rhombus (checkerboard), clipped to the free part of the face
    p0 = anchor + i * S_EDGE * d1 + j * S_EDGE * d2; Q = [p0, p0 + S_EDGE * d1, p0 + S_EDGE * (d1 + d2), p0 + S_EDGE * d2]
    if any(in_tri(q, -S_EDGE) for q in Q): tiles.append(Q)
prisms = [hull([to3(q) - nrm * 0.004 for q in Q] + [to3(q) + nrm * H for q in Q]) for Q in tiles]
# clip: above the face triangle (shrunk by MARGIN) and away from the OCD (OCD grown by MARGIN)
tri_in = []
cen = tri.mean(0)
for k in range(3):
    pass
shr = [cen + (q - cen) * (1 - 2.2 * MARGIN / np.linalg.norm(q - cen)) for q in tri]
slab = hull([to3(q) - nrm * 0.004 for q in shr] + [to3(q) + nrm * H for q in shr])
OCDg = hull(V * (1 + MARGIN / np.linalg.norm(V, axis=1))[:, None])
P0 = (U(prisms) ^ slab) - OCDg
P0 = U([p for p in P0.decompose() if p.volume() > 2e-5])
# W0's own symmetry (2/m about m0): identity, inversion through m0, half-turn about the x axis through m0, mirror x = 0
def aff(M, c): return np.c_[M, c - M @ c]
Sym = [np.eye(3), -np.eye(3), np.diag([1, -1, -1]), np.diag([-1, 1, 1])]
P = U([P0.transform(aff(M, m0)) for M in Sym])
Wb = W0 + P
# neighbours: every edge midpoint near m0; a structure symmetry g (Th about the origin + fcc translation) with g(m0) = m_j
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
lat = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]
sites = [np.array(s) * R / 2 for s in itertools.product(range(-5, 6), repeat=3) if sum(1 for x in s if x % 2) == 2]
sites = [p for p in sites if 1e-9 < np.linalg.norm(p - m0) < 2.0 * R]
intr = []
for mj in sites:
    g = next(((G, t) for G in ops for t in lat if np.allclose(G @ m0 + t, mj)), None)
    if g is None: continue
    G, t = g; Pj = P.transform(np.c_[G, t])
    if (Pj ^ cell(m0)).volume() > 1e-12: intr.append(Pj)
Wk = Wb - U(intr) if intr else Wb
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
me = Wk.to_mesh()
out = dict(tiles_per_face=len(tiles), bump_volume_total=P.volume(), dents_from_neighbours=len(intr), W0_volume=W0.volume(), keyed_volume=Wk.volume(),
           volume_conserved=abs(Wk.volume() - W0.volume()) < 1e-6, parts=len([p for p in Wk.decompose() if p.volume() > 1e-9]), sphericity=sph(Wk),
           relief_height=H, rhombus_edge=S_EDGE, v=np.round(np.asarray(me.vert_properties[:, :3], float) - m0, 6).tolist(), t=np.asarray(me.tri_verts).tolist(), centre=m0.tolist())
print({k: out[k] for k in out if k not in ('v', 't')}); json.dump(out, open(sys.argv[2], 'w'))
pv = sorted([p.volume() for p in Wk.decompose()], reverse=True); print('part volumes', [round(x, 6) for x in pv[:20]])
# keep the main solid; report what is dropped
main = max(Wk.decompose(), key=lambda p: p.volume()); out['dropped_volume'] = Wk.volume() - main.volume(); out['parts_volumes'] = pv[:20]
me = main.to_mesh(); out['v'] = np.round(np.asarray(me.vert_properties[:, :3], float) - m0, 6).tolist(); out['t'] = np.asarray(me.tri_verts).tolist()
out['main_volume'] = main.volume(); out['main_sphericity'] = sph(main)
json.dump(out, open(sys.argv[2], 'w')); print('main', main.volume(), 'dropped', out['dropped_volume'])
