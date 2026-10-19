# DICTO 2026-10-20: float check that DICTO Fill set 2 (OTT) F2 has no mirror symmetry of its own (so F2 and F3 are true left and
# right hands): the piece against its image under every improper map of the cube's 48 (about its centre); smallest mismatch reported.
import json, itertools, numpy as np, manifold3d as m3
H = '/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'; d = json.load(open(H + 'fill-cut8-octet-tet.json'))
mf = m3.Manifold(m3.Mesh(vert_properties=np.ascontiguousarray(d['v'], dtype=np.float32), tri_verts=np.ascontiguousarray(d['t'], dtype=np.uint32)))
c = np.array(d['c']); best = []
for p in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3):
        A = np.diag(s) @ np.eye(3)[list(p)]
        if np.linalg.det(A) > 0: continue
        m2 = mf.transform(np.hstack([A, (c - A @ c)[:, None]])); best.append((mf.volume() - (mf ^ m2).volume()) / mf.volume())
print(f'volume {mf.volume():.6f}; improper maps tried {len(best)}; smallest mismatch {min(best):.4f} (0 would mean a mirror symmetry)')
