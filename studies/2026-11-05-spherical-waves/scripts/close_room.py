# Close the gap room of the densest cut-OG lattice packing with one adaptor (DICTO 5 Nov 2026). The room centre (cage of the wave field)
# sits at fractional (0, 1/2, 1/2) = half the lattice vector b2 + b3 (index offset corrected), an inversion centre of the packing.
# Adaptor = Voronoi cell of the room centres (a lattice parallelohedron) minus every cut-OG copy. One room per copy -> one adaptor per copy.
import json, itertools, numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull, HalfspaceIntersection
R = "~/study-runs/og-pent/cut/data/"
B = np.array(json.load(open(R + "densest.json"))["B"]); O = np.array(json.load(open(R + "network.json"))["ocd"]); O = O - O.mean(0)
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float).tolist())
OG = hull(O); VOL = OG.volume(); cell = abs(np.linalg.det(B))
c = B @ np.array([0, 0.5, 0.5])
L = [B @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3) if any(m)]
hs = [np.r_[v, -(v @ (c + v/2))] for v in L]          # keep points closer to c than to c + v:  v.x <= v.(c + v/2)
V = HalfspaceIntersection(np.array(hs), c).intersections; Vor = hull(V)
print(f"cell {cell:.6f}, Voronoi cell of the room centres {Vor.volume():.6f}, cut OG {VOL:.6f}, gap per copy {cell - VOL:.6f}")
copies = [OG.translate(list(B @ np.array(m, float))) for m in itertools.product(range(-3, 4), repeat=3)]
copies = [x for x in copies if np.linalg.norm(np.array(x.bounding_box()[:3]) + np.array(x.bounding_box()[3:]) - 2*c) < 2*2.2]
U = m3.Manifold.batch_boolean(copies, m3.OpType.Add); Ad = Vor - U
parts = [p for p in Ad.decompose() if p.volume() > 1e-9]
print(f"adaptor volume {Ad.volume():.6f} (expected {cell - VOL:.6f}); solid pieces {len(parts)}; volumes {[round(p.volume(), 6) for p in parts]}; genus {[p.genus() for p in parts]}")
P = np.unique(np.round(np.array(Ad.to_mesh().vert_properties)[:, :3], 7), axis=0)
inv = all(np.min(np.linalg.norm(P - (2*c - p), axis=1)) < 1e-5 for p in P); print("centrally symmetric about the room centre:", inv)
# do the translates tile with the OG? total of one OG + one adaptor = one cell; overlap check on a patch
A2 = [Ad.translate(list(B @ np.array(m, float))) for m in itertools.product(range(-1, 2), repeat=3)]
ov = sum(x.volume() for x in A2) - m3.Manifold.batch_boolean(A2, m3.OpType.Add).volume(); ov2 = (m3.Manifold.batch_boolean(A2, m3.OpType.Add) ^ U).volume()
print(f"adaptor copies overlap each other {ov:.2e}, overlap the cut OGs {ov2:.2e}; OG + adaptor = {VOL + Ad.volume():.6f} vs cell {cell:.6f}")
np.save("adaptor-verts.npy", P); mm = Ad.to_mesh(); np.savez("adaptor-mesh.npz", v=np.array(mm.vert_properties)[:, :3], t=np.array(mm.tri_verts), c=c, B=B)
cv = ConvexHull(P).volume; print(f"adaptor / its convex hull = {Ad.volume()/cv:.4f}; sphericity {(np.pi**(1/3))*(6*Ad.volume())**(2/3)/Ad.surface_area():.4f}")
print("FINAL ok")
