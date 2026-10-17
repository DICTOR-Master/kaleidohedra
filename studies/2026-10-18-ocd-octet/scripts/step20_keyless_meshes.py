# DICTO 2026-10-18 octet study -- STEP 20 (dicto-node, manifold3d): meshes of the keyless full kit with the three Penrose cores, for the
# 3D page: plain OCD, notched cap, notched tetrahedron (no key dents), central core, flanking cores (left, right), rest.
# usage: python3 step20_keyless_meshes.py step10-input.json step19-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2]))
V = np.array(D['V']); R = D['R']; L = np.array(D['L']); Tp = np.array(D['Tp']); hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
OCD = hull(V); r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
def M0(i):
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in D['faces'] if i in f for j in f})]
    return hull(np.vstack([star, o - star])) - OCD - OCD.translate(o)
Mb = {i: M0(i) for i in five}; shifts = [np.array(ijk) @ L for ijk in itertools.product(range(-2, 3), repeat=3)]
Mall = U([Mb[i].translate(s) for s in shifts if np.linalg.norm(s) < 2.3 for i in five])
corner = hull([[0, 0, 0], [0, 0, R], [R/2, 0, R/2], [-R/2, 0, R/2], [0, R/2, R/2], [0, -R/2, R/2]] + [[a*R/3, b*R/3, R/3] for a in (1, -1) for b in (1, -1)])
cap = corner - OCD - Mall; tet = hull(Tp) - Mall
i1 = [i for i in five if abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]; M1 = Mb[i1]
ax = np.array(C['a']); ax /= np.linalg.norm(ax)
cores = {k: M1 ^ hull(np.vstack([np.array(Q) - ax, np.array(Q) + ax])) for k, Q in C['rhombi'].items()}
rest = M1
for k in cores: rest = rest - cores[k]
def mesh(mf):
    m = mf.to_mesh(); return dict(volume=mf.volume(), v=np.round(np.asarray(m.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(m.tri_verts).tolist())
out = dict(ocd=mesh(OCD), cap=mesh(cap), tet=mesh(tet), core_c=mesh(cores['central']), core_f1=mesh(cores['flank1']), core_f2=mesh(cores['flank2']), rest3=mesh(rest))
for k, v in out.items(): print(k, round(v['volume'], 6), len(v['t']))
json.dump(out, open(sys.argv[3], 'w'))
