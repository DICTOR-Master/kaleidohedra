# DICTO 2026-10-18 octet study -- STEP 23 (dicto-node, manifold3d): meshes of the envelope kit for the 3D page: the golden envelope (RT),
# the outer corner at the +z vertex (octahedron minus envelope, connected part), the dented tetrahedron T+ (T+ minus the 4 envelopes).
# usage: python3 step23_envelope_meshes.py step10-input.json step22-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); RT = np.array(json.load(open(sys.argv[2]))['RT']); L = np.array(D['L']); R = D['R']; Tp = np.array(D['Tp'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
env = hull(RT); sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
allenv = U([env.translate(s) for s in sh if np.linalg.norm(s) < 2.6])
octa = hull([[s * R if i == j else 0 for j in range(3)] for i in range(3) for s in (1, -1)])
oc = max((octa - env).decompose(), key=lambda p: np.asarray(p.to_mesh().vert_properties[:, :3])[:, 2].mean())
tet = hull(Tp) - allenv
def mesh(mf):
    m = mf.to_mesh(); return dict(volume=mf.volume(), v=np.round(np.asarray(m.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(m.tri_verts).tolist())
out = dict(envelope=mesh(env), outer_corner=mesh(oc), dented_tet=mesh(tet), ocd=mesh(hull(np.array(D['V']))))
for k, v in out.items(): print(k, round(v['volume'], 6), len(v['t']))
json.dump(out, open(sys.argv[3], 'w'))
