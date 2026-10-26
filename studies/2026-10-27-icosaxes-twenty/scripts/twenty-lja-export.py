exec(open('twenty-lja.py').read().split("print('piece volume'")[0])
touch = 2.267283
for k, f in enumerate([1.0, 0.8, 0.6175, 0.3333]):
    T = U_at(touch * f).to_mesh(); t = trimesh.Trimesh(T.vert_properties[:, :3], T.tri_verts); t.merge_vertices(); t.export(f'L{k}-union.obj')
print('ok')
