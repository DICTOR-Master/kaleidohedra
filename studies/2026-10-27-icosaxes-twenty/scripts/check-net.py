import json, sys, itertools, numpy as np, manifold3d as mf
for name in sys.argv[1:]:
    J = json.load(open(name + '.json'))
    M = [mf.Manifold(mf.Mesh(vert_properties=np.array(p['vertices'], dtype=np.float32), tri_verts=np.array(p['tris'], dtype=np.uint32))) for p in J]
    bad = [k for k, m in enumerate(M) if m.status() != mf.Error.NoError or m.volume() <= 0]
    C = [np.mean(p['vertices'], 0) for p in J]
    ov = max(((M[i] ^ M[j]).volume() for i, j in itertools.combinations(range(len(M)), 2) if np.linalg.norm(C[i] - C[j]) < 3), default=0)
    vols = sorted(set(round(m.volume(), 5) for m in M))
    print(name, '| broken pieces', bad, '| piece volumes', vols, '| largest overlap between any two pieces', round(ov, 7))
