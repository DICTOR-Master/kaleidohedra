# A, icosahedral, with Lotus Jewel Axes (DICTO 2026-10-27: "try the Lotus Jewel Axes version"): as twenty.py, each piece from its own
# triangles (dented, not convex). First touch, the windows closing, the hollow filling; S-files for renders as L<k>-union.obj.
import json, itertools, numpy as np, manifold3d as mf, trimesh
exec(open('twenty.py').read().split('def pieces(d)')[0].replace("I0 = np.array(json.load(open('H2.json'))[0]['vertices'])", "I0 = None"))
L = json.load(open('lja.json')); LV, LT = np.array(L['vertices']), np.array(L['tris'], dtype=np.uint32)
def pieces(d): return [mf.Manifold(mf.Mesh(vert_properties=(LV @ M.T + d * (M @ u)).astype(np.float32), tri_verts=LT)) for M in sites.values()]
def U_at(d): return mf.Manifold.batch_boolean(pieces(d), mf.OpType.Add)
def overl(d):
    P = pieces(d); return sum(max(0, (P[i] ^ P[j]).volume()) for i, j in itertools.combinations(range(20), 2))
def bisect(test, a, b):   # test true at a, false at b
    for _ in range(40):
        m = (a + b) / 2; a, b = (m, b) if test(m) else (a, m)
    return (a + b) / 2
print('piece volume', round(pieces(3)[0].volume(), 6), 'status', pieces(3)[0].status())
touch = bisect(lambda d: overl(d) < 1e-7, 6.0, 0.5)
print(f'first touch d = {touch:.6f}; Icosaxes touched at 2.267283')
for f in [1.0, 0.9, 0.8, 0.7, 0.65, 0.618, 0.6, 0.5, 0.4, 0.34, 0.33, 0.3]:
    U = U_at(touch * f); print(f'  {f:.3f} of touch: genus {U.genus()}, parts {len(U.decompose())}, volume {U.volume():.4f}')
