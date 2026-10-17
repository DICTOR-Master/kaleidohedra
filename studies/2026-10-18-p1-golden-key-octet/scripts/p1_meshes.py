# DICTO 2026-10-18 Project 1, Golden-key octet -- meshes (dicto-node, manifold3d): the keyed octahedron (octahedron + its 8 golden-envelope
# corner keys; the OCD and its 6 caps fused) and the dented tetrahedron T+ (T+ minus the 4 keys entering it); T- is its point reflection.
# usage: python3 p1_meshes.py step10-input.json OUT.json   (step10-input.json from studies/2026-10-18-ocd-octet/data)
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); R = D['R']; L = np.array(D['L']); Tp = np.array(D['Tp'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
octa = hull([[s * R if i == j else 0 for j in range(3)] for i in range(3) for s in (1, -1)])
keys = [hull(K) for K in D['keys'].values()]
# for the union only: each key gets a small inward tip (inside the octahedron) so float round-off cannot leave a hair gap at its base
def tipped(K):
    K = np.asarray(K, float); base = K[1:].mean(0); return hull(np.vstack([K, base * 0.97]))
kocta = U([octa] + [tipped(K) for K in D['keys'].values()])
sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
allkeys = U([k.translate(t) for t in sh if np.linalg.norm(t) < 2.6 for k in keys])
tet = hull(Tp) - allkeys
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
def mesh(mf, c):
    m = mf.to_mesh(); return dict(volume=mf.volume(), sphericity=sph(mf), parts=len([p for p in mf.decompose() if p.volume() > 1e-9]),
                                  v=np.round(np.asarray(m.vert_properties[:, :3], float) - c, 6).tolist(), t=np.asarray(m.tri_verts).tolist())
out = dict(R=R, keyed_octahedron=mesh(kocta, np.zeros(3)), dented_tetrahedron=mesh(tet, Tp.mean(0)), tet_centre=Tp.mean(0).tolist())
for k in ('keyed_octahedron', 'dented_tetrahedron'): print(k, {x: round(y, 6) for x, y in out[k].items() if x in ('volume', 'sphericity', 'parts')})
json.dump(out, open(sys.argv[2], 'w'))
