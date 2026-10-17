# DICTO 2026-10-18 octet study -- STEP 25 (dicto-node, manifold3d): meshes of the refined envelope kit for the 3D page: the phi^-2 vertex
# cuboctahedron at (0,0,R), the two wedges of the +z outer corner, and the tetrahedron T+ minus its 4 key dents and its 4 phi^-2 corners.
# usage: python3 step25_refined_meshes.py step10-input.json step22-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); RT = np.array(json.load(open(sys.argv[2]))['RT']); R = D['R']; L = np.array(D['L']); Tp = np.array(D['Tp'])
PHI = (1 + 5 ** .5) / 2; s = 1 / PHI ** 2
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
env = hull(RT); octa = hull([[t * R if i == j else 0 for j in range(3)] for i in range(3) for t in (1, -1)])
v = np.array([0, 0, R]); e = R * s
cubo = hull([v + e * np.array(p) for p in itertools.permutations([1, 1, 0]) for p in [p]] + [v + e * np.array(p) * np.array(sg) for p in [(1, 1, 0), (1, 0, 1), (0, 1, 1)] for sg in itertools.product((1, -1), repeat=3)])
oc = max((octa - env).decompose(), key=lambda p: np.asarray(p.to_mesh().vert_properties[:, :3])[:, 2].mean())
pyr = octa ^ m3.Manifold.cube([3, 3, 3], True).translate([0, 0, 2 / 3 + 1.5])
wedges = sorted([p for p in (oc - pyr).decompose() if p.volume() > 1e-9], key=lambda p: np.asarray(p.to_mesh().vert_properties[:, :3])[:, 0].mean())
sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
allenv = U([env.translate(t) for t in sh if np.linalg.norm(t) < 2.6])
corners = U([hull([p + s * (q_ - p) for q_ in Tp]) for p in Tp])
tet = hull(Tp) - allenv - corners
def mesh(mf):
    m = mf.to_mesh(); return dict(volume=mf.volume(), v=np.round(np.asarray(m.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(m.tri_verts).tolist())
out = dict(cubo=mesh(cubo), wedge1=mesh(wedges[0]), wedge2=mesh(wedges[1]), tet_trunc=mesh(tet))
for k, x in out.items(): print(k, round(x['volume'], 6), len(x['t']))
json.dump(out, open(sys.argv[3], 'w'))
