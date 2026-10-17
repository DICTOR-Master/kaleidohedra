# DICTO 2026-10-18 Project 3c -- split the cut-down tetrahedron (octet step 25) into the central tetartoid-like dodecahedron + the shell
# (dicto-node, manifold3d). Is the shell one solid? volumes, sphericity.
# usage: python3 p3c_split.py step25-refined-meshes.json p3c-dodeca.json step10-input.json OUT.json
import sys, json, numpy as np, manifold3d as m3
T = json.load(open(sys.argv[1]))['tet_trunc']; Dd = json.load(open(sys.argv[2])); D = json.load(open(sys.argv[3]))
Tp = np.array(D['Tp']); c = Tp.mean(0)
tet = m3.Manifold(m3.Mesh(vert_properties=np.asarray(T['v'], np.float32), tri_verts=np.asarray(T['t'], np.uint32)))
dode = m3.Manifold.hull_points(np.asarray(Dd['corners_float'], float))
shell = tet - dode; parts = sorted([p.volume() for p in shell.decompose() if p.volume() > 1e-9], reverse=True)
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
inside = abs((tet ^ dode).volume() - dode.volume()) < 1e-7
def mesh(mf, cc):
    me = mf.to_mesh(); return dict(volume=mf.volume(), sphericity=sph(mf), v=np.round(np.asarray(me.vert_properties[:, :3], float) - cc, 6).tolist(), t=np.asarray(me.tri_verts).tolist())
out = dict(dodeca_inside_tet=inside, shell_parts=len(parts), shell_part_volumes=parts[:5], dodeca=mesh(dode, c), shell=mesh(shell, c))
print({k: v for k, v in out.items() if k not in ('dodeca', 'shell')}, 'dodeca', round(out['dodeca']['volume'], 6), round(out['dodeca']['sphericity'], 3), 'shell', round(out['shell']['volume'], 6), round(out['shell']['sphericity'], 3))
json.dump(out, open(sys.argv[4], 'w'))
