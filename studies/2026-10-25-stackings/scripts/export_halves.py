# Figures for #57: Fang (ABAC octahedral site 0, λ = 5/24) and Chucky (λ = −3/8) cut at the site's mid-plane; the lower half is
# cubic (layer 0 of ABAC is c), the upper half hexagonal (layer 1 is h). OBJ halves for render_halves.py; floats for drawing only.
exec(open('export_new.py').read().split('want = ')[0])
import manifold3d as m3
for tag, lam in (('fang', 5 / 24), ('chucky', -3 / 8)):
    w = lambda k: lam if k == 'tet' else 0.0; kp, p = M[0][0], L.T @ M[0][1]; H = []
    for k, q in sites:
        d = q - p
        if np.allclose(d, 0) or d @ d > 6: continue
        H.append(np.r_[2 * d, -(q @ q - p @ p - w(k) + w(kp))])
    H = np.array(H); A, b = H[:, :3], -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    V = np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0) - p     # site at the origin
    P = m3.Manifold.hull_points([list(map(float, v)) for v in V])
    up = P.trim_by_plane([0, 0, 1], 0.0); dn = P.trim_by_plane([0, 0, -1], 0.0)
    for nm, m in (('hex-top', up), ('cubic-bottom', dn)):
        mesh = m.to_mesh(); trimesh.Trimesh(np.array(mesh.vert_properties)[:, :3], np.array(mesh.tri_verts)).export(f'../h-{tag}-{nm}.obj')
    print(tag, 'top', round(up.volume(), 6), 'bottom', round(dn.volume(), 6))
