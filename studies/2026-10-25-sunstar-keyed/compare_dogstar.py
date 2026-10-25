# Solid-to-solid check: the app's Dogstar mesh (app-dogstar-faces.json, polygons fanned to triangles) against cube − neighbours' roofs.
import json, numpy as np, manifold3d as m3
exec(open('proof.py').read().split('app = json.load')[0].replace("print(x); ", ""))
F = json.load(open('app-dogstar-faces.json'))
V, T, idx = [], [], {}
def vid(p):
    k = tuple(round(c, 9) for c in p)
    if k not in idx: idx[k] = len(V); V.append(list(k))
    return idx[k]
for f in F:
    ids = [vid(p) for p in f]
    for i in range(1, len(ids) - 1): T.append([ids[0], ids[i], ids[i + 1]])
mesh = m3.Mesh(vert_properties=np.array(V, dtype=np.float32), tri_verts=np.array(T, dtype=np.uint32)); mesh.merge()
app = m3.Manifold(mesh)
print('app Dogstar status', app.status(), 'volume', round(abs(app.volume()), 9))
if app.volume() < 0: print('(app faces wound inward)')
d = (app - dog_built).volume() + (dog_built - app).volume()
print(f'|app Dogstar Δ (cube − roofs)| = {d:.2e}')
