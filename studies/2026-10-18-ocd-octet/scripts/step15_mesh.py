# DICTO 2026-10-18 octet study -- STEP 15 meshes (dicto-node, manifold3d): split the middle piece into the Penrose core and the rest.
# usage: python3 step15_mesh.py step10-input.json step15-input.json step10-meshes.json OUT.json
import sys, json, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2])); old = json.load(open(sys.argv[3]))
V = np.array(D['V']); R = D['R']; hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
OCD = hull(V); keyed = m3.Manifold.batch_boolean([OCD] + [hull(K) for K in D['keys'].values()], m3.OpType.Add)
r = np.linalg.norm(V, axis=1); i1 = [i for i in range(len(V)) if r[i] > r.max() - 1e-9 and abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
o = np.array([0, R, R]); star = V[sorted({j for f in D['faces'] if i1 in f for j in f})]
M1 = hull(np.vstack([star, o - star])) - keyed - keyed.translate(o)
rh = np.array(C['rh']); a = np.array(C['a']); a /= np.linalg.norm(a); prism = hull(np.vstack([rh - 1.0 * a, rh + 1.0 * a]))
core = M1 ^ prism; rest = M1 - prism
out = dict(old)
for k, mf in (('core', core), ('rest', rest)):
    mesh = mf.to_mesh(); parts = sorted([p.volume() for p in mf.decompose()], reverse=True)
    out[k] = dict(volume=mf.volume(), parts=len([p for p in parts if p > 1e-9]), part_volumes=parts[:6], v=np.round(mesh.vert_properties[:, :3], 6).tolist(), t=mesh.tri_verts.tolist())
    print(k, 'volume %.6f' % mf.volume(), 'parts', parts[:6], flush=True)
json.dump(out, open(sys.argv[4], 'w'))
