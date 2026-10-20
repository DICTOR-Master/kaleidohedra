# DICTO 2026-10-20 (reading A of "spheres with 8 dimples, small rounded tetrahedra"): two pieces fill space:
#   the SMALL ROUNDED TETRAHEDRON in every tetrahedral hole of the octet: the hull of 4 corner balls (pointing to the hole's corners)
#     and 4 face balls (one bump on each face, reaching a little into the octahedron beyond);
#   the BALL: everything else. Around each octahedron centre that is its Voronoi cell (a rhombic dodecahedron: the octahedron plus a
#     quarter of each of its 8 neighbouring tetrahedral holes) with the 8 rounded tetrahedra taken out: 8 dimples at its 3-fold corners.
#   Balls meet balls on the rhombic faces (three at every edge, 120 deg each); the 6 four-fold corners stay points.
# A partition of space by construction (the rhombic dodecahedra tile). Float, manifold3d: a block filled exactly, pieces congruent.
import itertools, numpy as np, manifold3d as m3
S_CORNER, R_CORNER, D_FACE, R_FACE, SEG = 0.50, 0.10, 0.16, 0.15, 48
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def balls(c, r):
    s = m3.Manifold.sphere(r, SEG).to_mesh(); return np.asarray(s.vert_properties[:, :3]) + c
def rd(c):
    c = np.array(c, float); return hull([c + d * e for e in np.eye(3) for d in (1, -1)] + [c + .5 * np.array(s) for s in itertools.product((1, -1), repeat=3)])
def filler(V):
    V = np.array(V, float); t = V.mean(0); P = []
    for k in range(4):
        P.append(balls(t + S_CORNER * (V[k] - t), R_CORNER))
        n = t - V[k]; n /= np.linalg.norm(n); P.append(balls(t + D_FACE * n, R_FACE))   # face k faces away from corner k
    return hull(np.vstack(P))
def tet_around(t):
    """the tetrahedral hole with centroid t (t has all coordinates = 1/2 mod 1): its 4 corners are the even-sum integer points at distance sqrt3/2"""
    t = np.array(t, float); C = [t + .5 * np.array(s) for s in itertools.product((1, -1), repeat=3)]
    return np.array([p for p in C if int(round(p.sum())) % 2 == 0])
def sphere_piece(c):
    c = np.array(c, float); m = rd(c)
    for s in itertools.product((1, -1), repeat=3): m = m - filler(tet_around(c + .5 * np.array(s)))
    return m
def tets_in(rng):
    for x, y, z in itertools.product(rng, repeat=3):
        t = np.array([x, y, z], float) + .5; yield t, tet_around(t)
if __name__ == '__main__':
    F0 = filler(tet_around((.5, .5, .5))); S0 = sphere_piece((1, 0, 0))
    print('hole inradius 0.2887; rounded tetrahedron reaches', round(D_FACE + R_FACE, 4), 'along face normals (bump into the octahedron)')
    pieces = [('ball', sphere_piece((x, y, z))) for x, y, z in itertools.product(range(-1, 4), repeat=3) if (x + y + z) % 2] + [('tet', filler(V)) for _, V in tets_in(range(-1, 3))]
    print('valid:', all(p.status() == m3.Error.NoError for _, p in pieces), '; volumes ball', sorted({round(p.volume(), 4) for k, p in pieces if k == 'ball'}), 'tet', sorted({round(p.volume(), 4) for k, p in pieces if k == 'tet'}))
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 box: volume {tot:.5f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 2e-3 and over < 2e-3 else 'FAIL')
    print('the ball is', round(S0.volume() / (S0.volume() + 2 * F0.volume()) * 100, 1), '% of space')
