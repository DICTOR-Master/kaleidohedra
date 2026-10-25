# Export the three valid keyed gyrated pairs (K = 0.8) as OBJ, whole and cut in half (for render_keyed_gyrated.py).
import os; os.environ['K'] = '0.8'
import numpy as np, trimesh
exec(open('keyed_gyrated.py').read().split('fig = plt.figure')[0])
for (d, o), (tp, op) in res.items():
    if (d, o) == ('oct->tet', 'B'): continue           # overlaps itself (genus 4): not valid
    tag = {'tet->oct': 'TO', 'oct->tet': 'OT'}[d] + o
    for nm, m in (('tet', tp), ('oct', op)):
        mesh = m.to_mesh(); V = np.array(mesh.vert_properties)[:, :3]; c = V.mean(0)
        trimesh.Trimesh(V - c, np.array(mesh.tri_verts)).export(f'kg-{tag}-{nm}.obj')
        half = m.trim_by_plane([0, 1, 0], float(c[1])).to_mesh()
        trimesh.Trimesh(np.array(half.vert_properties)[:, :3] - c, np.array(half.tri_verts)).export(f'kg-{tag}-{nm}-half.obj')
        print(tag, nm, 'exported', round(m.volume(), 6))
