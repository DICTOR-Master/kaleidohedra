# DICTO 2026-10-18 Project 2, Penrose-core octet (keyless; whole middle piece, DICTO) -- meshes (dicto-node, manifold3d):
# notched octahedron (OCD + its 6 notched caps fused = octahedron minus its 12 middle-piece shares), middle piece M0 = H - both OCDs
# (H = hull of two facing five-kite stars), notched tetrahedron T+ (T+ minus its 6 middle-piece shares); T- is its mirror image.
# usage: python3 p2_meshes.py step10-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; L = np.array(D['L']); Tp = np.array(D['Tp'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
OCD = hull(V); r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
def M0(i):
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in D['faces'] if i in f for j in f})]
    return hull(np.vstack([star, o - star])) - OCD - OCD.translate(o), o
Mb = {i: M0(i) for i in five}; sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
Mall = U([Mb[i][0].translate(s) for s in sh if np.linalg.norm(s) < 2.3 for i in five])
octa = hull([[s * R if i == j else 0 for j in range(3)] for i in range(3) for s in (1, -1)])
nocta = octa - Mall; tet = hull(Tp) - Mall
i1 = [i for i in five if abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]; mid, o1 = Mb[i1]; m = o1 / 2
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
def mesh(mf, c):
    me = mf.to_mesh(); return dict(volume=mf.volume(), sphericity=sph(mf), parts=len([p for p in mf.decompose() if p.volume() > 1e-9]),
                                   v=np.round(np.asarray(me.vert_properties[:, :3], float) - c, 6).tolist(), t=np.asarray(me.tri_verts).tolist())
out = dict(R=R, notched_octahedron=mesh(nocta, np.zeros(3)), middle_piece=mesh(mid, m), notched_tetrahedron=mesh(tet, Tp.mean(0)), middle_centre=m.tolist(), tet_centre=Tp.mean(0).tolist())
for k in ('notched_octahedron', 'middle_piece', 'notched_tetrahedron'): print(k, {x: round(y, 6) for x, y in out[k].items() if x in ('volume', 'sphericity', 'parts')})
json.dump(out, open(sys.argv[2], 'w'))
