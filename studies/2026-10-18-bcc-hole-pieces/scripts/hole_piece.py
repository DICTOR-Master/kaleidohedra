# DICTO 2026-10-18: the resin round the OCD double network (Golden Bodhi Pyrochlore "double" view = bcc packing, 77.43%) cut into
# pieces at the holes between 6 OCDs ("five double T bars crossing is the shape between 6 OCDs"; "a central double T bar in the gap
# between two widely and narrowly spaced OCDs ... you can also visualise the double Ts as double crescents").
# OCD frame: joint hexagons on |x|+|y|+|z| = R (R = 2phi/3); bcc cube edge a = 4R/3; OCD sites (a/2)(i,j,k), all even or all odd.
# 6-OCD holes (bcc octahedral holes) = (a/2)(i,j,k) with one or two odd entries (3 per OCD): the narrow pair at a/2 (across a slab),
# four at a/sqrt2. Piece = Voronoi cell of the hole among all holes, minus the OCDs. Checks: one solid? volume = gap/3 per OCD,
# sphericity, symmetry. dicto-node, manifold3d. usage: python3 hole_piece.py step10-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
from scipy.spatial import HalfspaceIntersection
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; a = 4 * R / 3
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
h0 = np.array([a / 2, 0, 0])
holes = [np.array(s) * a / 2 for s in itertools.product(range(-5, 6), repeat=3) if sum(x % 2 for x in s) in (1, 2)]
hs = [np.r_[p - h0, -(p - h0) @ ((p + h0) / 2)] for p in holes if 1e-9 < np.linalg.norm(p - h0) < 3 * a]
C = HalfspaceIntersection(np.array(hs), h0).intersections; cell = hull(C)
ocd_sites = [np.array(s) * a / 2 for s in itertools.product(range(-4, 5), repeat=3) if len({x % 2 for x in s}) == 1]
OCD = hull(V); near = [p for p in ocd_sites if np.linalg.norm(p - h0) < 2.2 * a]
piece = cell - U([OCD.translate(p) for p in near])
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
gap_per_ocd = a ** 3 / 2 - OCD.volume()
inv = piece.translate(-h0).transform(np.c_[-np.eye(3), np.zeros(3)]).translate(h0)
mx = piece.translate(-h0).transform(np.c_[np.diag([-1, 1, 1]), np.zeros(3)]).translate(h0)
me = piece.to_mesh(); bites = [p for p in near if (cell ^ OCD.translate(p)).volume() > 1e-9]
net = lambda s: 0 if (round(sum(s) / (a / 2)) % 4) in (0, 3) else 1
out = dict(a=a, cell_corners=len(C), cell_volume=cell.volume(), ocds_biting=len(bites), bite_distances=sorted({round(float(np.linalg.norm(p - h0)), 4) for p in bites}),
           volume=piece.volume(), expected=gap_per_ocd / 3, parts=len([p for p in piece.decompose() if p.volume() > 1e-9]), genus=piece.genus(), sphericity=sph(piece),
           centrosymmetric=abs((inv ^ piece).volume() - piece.volume()) < 1e-9, mirror_x=abs((mx ^ piece).volume() - piece.volume()) < 1e-9,
           v=np.round(np.asarray(me.vert_properties[:, :3], float) - h0, 6).tolist(), t=np.asarray(me.tri_verts).tolist(), centre=h0.tolist(),
           ocds=[dict(p=(p - h0).tolist(), net=net(p)) for p in bites], ocd_mesh=dict(v=np.round(V, 6).tolist(), t=np.asarray(OCD.to_mesh().tri_verts).tolist()))
print({k: out[k] for k in out if k not in ('v', 't', 'ocds', 'ocd_mesh')}); json.dump(out, open(sys.argv[2], 'w'))
