# Keyed blocks: each piece from its own triangles (not convex), exact-ish volumes, overlaps, and the joined solid (manifold3d).
import json, sys, itertools, numpy as np, manifold3d as mf, trimesh
def man(p): return mf.Manifold(mf.Mesh(vert_properties=np.array(p['vertices'], dtype=np.float32), tri_verts=np.array(p['tris'], dtype=np.uint32)))
for name in sys.argv[1:]:
    J = json.load(open(name + '.json')); M = [man(p) for p in J]
    bad = [k for k, m in enumerate(M) if m.status() != mf.Error.NoError or m.volume() <= 0]
    vols = [m.volume() for m in M]; ov = [(i, j, (M[i] ^ M[j]).volume()) for i, j in itertools.combinations(range(len(M)), 2)]
    ov = [x for x in ov if x[2] > 1e-6]; U = mf.Manifold.batch_boolean(M, mf.OpType.Add)
    T = U.to_mesh(); t = trimesh.Trimesh(T.vert_properties[:, :3], T.tri_verts); t.merge_vertices()
    print(name, '| bad pieces', bad, '| piece volumes', sorted(set(round(v, 5) for v in vols)), '| sum', round(sum(vols), 5),
          '| overlaps', len(ov), round(sum(x[2] for x in ov), 5), '| joined', round(U.volume(), 5), 'genus', U.genus(), 'closed', t.is_watertight,
          'flat faces', len(t.facets) + len(t.faces) - sum(len(f) for f in t.facets))
    t.export(name + '-union.obj')
