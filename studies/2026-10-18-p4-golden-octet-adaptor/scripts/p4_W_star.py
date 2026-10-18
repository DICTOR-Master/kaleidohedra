# DICTO 2026-10-18 "could the imprint be centred on the Penrose star also?!" -- glue centred on the Penrose link: the middle point m of
# every octahedron edge, where two OCDs' five-fold stars face each other (the thick Penrose rhombus between them). Sites: the 6 edge
# midpoints per cell, (R/2)(a,b,c) with exactly two of a,b,c odd. Piece = Voronoi cell of m among these sites, minus the OCDs (exact OCD
# imprints). Checks (dicto-node): cell shape, one solid?, volume (expect (cell - OCD)/6), sphericity, centrosymmetric about m, does it
# contain the whole hull of the two facing stars (the middle piece and its Penrose cores)? usage: python3 p4_W_star.py step10-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
from scipy.spatial import HalfspaceIntersection, ConvexHull
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; L = np.array(D['L'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
m = np.array([0, R / 2, R / 2])
sites = [np.array(s) * R / 2 for s in itertools.product(range(-6, 7), repeat=3) if sum(1 for x in s if x % 2) == 2]
sites = [p for p in sites if 1e-9 < np.linalg.norm(p - m) < 2.5 * R]
hs = []
for p in sites:
    n = p - m; c = (p + m) / 2; hs.append(np.r_[n, -n @ c])          # n.x <= n.c
cellpts = HalfspaceIntersection(np.array(hs), m).intersections; Vor = hull(cellpts)
OCD = hull(V); sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
bites = [t for t in sh if (Vor ^ OCD.translate(t)).volume() > 1e-9]
W = Vor - U([OCD.translate(t) for t in bites])
r = np.linalg.norm(V, axis=1); i1 = [i for i in range(len(V)) if r[i] > r.max() - 1e-9 and abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
o = np.array([0, R, R]); star = V[sorted({j for f in D['faces'] if i1 in f for j in f})]; Hm = hull(np.vstack([star, o - star])) - OCD - OCD.translate(o)
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
inv = W.translate(-m).transform(np.c_[-np.eye(3), np.zeros(3)]).translate(m)
ch = ConvexHull(cellpts); faces = len(np.unique(np.round(ch.equations, 7), axis=0))
cell = abs(np.linalg.det(L)); me = W.to_mesh()
out = dict(voronoi_corners=len(cellpts), voronoi_faces=faces, voronoi_volume=Vor.volume(), expected_voronoi=cell / 6, ocds_biting=len(bites),
           volume=W.volume(), expected=(cell - OCD.volume()) / 6, parts=len([p for p in W.decompose() if p.volume() > 1e-9]), genus=W.genus(), sphericity=sph(W),
           centrosymmetric=abs((inv ^ W).volume() - W.volume()) < 1e-9, contains_middle_piece=abs((W ^ Hm).volume() - Hm.volume()) < 1e-9,
           middle_piece_share_inside=(W ^ Hm).volume() / Hm.volume(),
           v=np.round(np.asarray(me.vert_properties[:, :3], float) - m, 6).tolist(), t=np.asarray(me.tri_verts).tolist(), centre=m.tolist())
print({k: out[k] for k in out if k not in ('v', 't')}); json.dump(out, open(sys.argv[2], 'w'))
