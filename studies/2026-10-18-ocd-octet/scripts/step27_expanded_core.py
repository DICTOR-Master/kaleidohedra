# DICTO 2026-10-18 octet study -- STEP 27: "could this core dodecahedron be expanded to form a smaller kit with the OCD?"
# Grow each tetrahedron-centred piece as far as it can go: give every point outside the golden envelopes to its nearest tetrahedron
# centre. The tetrahedron centres (R/2)(odd, odd, odd) form a simple cubic lattice of spacing R, so the nearest-centre regions are cubes
# of edge R (corners at OCD centres and octet vertices). Piece = that cube minus the envelopes. Checks (dicto-node, manifold3d): one solid?
# volume (expect (1 - 10/phi^6) x cell / 2), sphericity, does it contain the step-26 core dodecahedron, and is it chiral.
# usage: python3 step27_expanded_core.py step10-input.json step22-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); RT = np.array(json.load(open(sys.argv[2]))['RT']); R = D['R']; L = np.array(D['L'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
env = hull(RT); sh = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]
allenv = U([env.translate(t) for t in sh if np.linalg.norm(t) < 3.2])
c = np.array([R / 2] * 3); cube = m3.Manifold.cube([R, R, R], True).translate(c)
piece = cube - allenv; parts = [p for p in piece.decompose() if p.volume() > 1e-9]
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
PHI = (1 + 5 ** .5) / 2; cell = abs(np.linalg.det(L))
out = dict(parts=len(parts), volume=piece.volume(), expected=(1 - 10 / PHI ** 6) * cell / 2, sphericity=sph(piece),
           envelope_sphericity=sph(env))
# chirality: is the mirror image (through the cube's centre: inversion) the same piece up to a turn? The tetrahedron sites alternate
# T+ / T-, and T- = -T+; compare this piece with the piece at the T- centre -c turned back by inversion.
other = (m3.Manifold.cube([R, R, R], True).translate(-c) - allenv)
inv = other.transform(np.c_[-np.eye(3), np.zeros(3)])
out['T_minus_piece_is_inversion_of_T_plus_piece'] = abs((inv ^ piece).volume() - piece.volume()) < 1e-9
m = piece.to_mesh(); out['mesh'] = dict(v=np.round(np.asarray(m.vert_properties[:, :3], float) - c, 6).tolist(), t=np.asarray(m.tri_verts).tolist())
print({k: v for k, v in out.items() if k != 'mesh'})
json.dump(out, open(sys.argv[3], 'w'))
