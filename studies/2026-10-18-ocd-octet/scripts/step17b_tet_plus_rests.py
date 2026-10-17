# DICTO 2026-10-18 octet study -- STEP 17b (dicto-node): alternative merge, since the vertex piece (step 17) came out spiky and in 2 parts.
# Cut each middle rest by the mirror plane through its edge and the five-fold axis (x = 0 for the base edge): the two halves face the two
# tetrahedra on that edge (swapped by the inversion through m). Merge each tetrahedron with the 6 half-rests on its 6 edges.
# usage: python3 step17b_tet_plus_rests.py step10-input.json step15-input.json OUT.json
import sys, json
exec(open('step17_vertex_piece.py').read().split('v = np.array([0, 0, R])')[0])
c_t = Tp.mean(0); halves = []; base_dir = np.array([0, 1, -1.0])
for a_, b_ in itertools.combinations(range(4), 2):
    p = (Tp[a_] + Tp[b_]) / 2; w = Tp[b_] - Tp[a_]; found = None
    for G in ops:
        gd = G @ base_dir
        if np.allclose(gd, w / R) or np.allclose(gd, -w / R):
            t = p - G @ m
            if is_lattice(t): found = (G, t); break
    assert found
    G, t = found; piece = place(rest, G, t)
    n = c_t - p; n -= (n @ w) / (w @ w) * w; n /= np.linalg.norm(n)       # plane through the edge, normal towards the tetrahedron centre
    halves.append(piece.trim_by_plane(n.tolist(), float(n @ p)))
merged = U([T] + halves)
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
parts = sorted([p.volume() for p in merged.decompose()], reverse=True)
out = dict(volume=merged.volume(), expected=T.volume() + 3 * rest.volume(), sphericity=sph(merged), parts=len([p for p in parts if p > 1e-9]), part_volumes=parts[:4])
print(out); mesh = merged.to_mesh(); out['mesh'] = dict(v=np.round(mesh.vert_properties[:, :3] - c_t, 6).tolist(), t=mesh.tri_verts.tolist())
json.dump(out, open(sys.argv[3], 'w'))
