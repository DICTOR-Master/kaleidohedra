# DICTO 2026-10-20: the S-curved double octet ("spherical S-curved lattice"; "the shapes will change but the relationship should remain").
# The folding set (folding_octet.py: octahedra dome next to hollow, tetrahedra 2 domes + 2 hollows) carried through one smooth bend of
# space, x -> x + E (sin 2 pi y, sin 2 pi z, sin 2 pi x): it fixes every lattice corner and every edge midpoint (all coordinates
# multiples of 1/2), and along an edge its displacement is odd about the midpoint, so every straight edge becomes an S-curve, shared by the
# pieces round it. A one-to-one map of space (its Jacobian det = 1 + (2 pi E)^3 c1 c2 c3 > 0 for 2 pi E < 1), so the pieces still fill
# space with every face shared. Period 1, so pieces one lattice step apart stay congruent. Float, manifold3d; block test.
import itertools, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "if __name__ == " + "'__main__':"
exec(open(os.path.join(HERE, 'folding_octet.py')).read().split(MAIN)[0])   # the folding set, with domed_octet's patch() and solid()
E = 0.07
bend = lambda P: P + E * np.stack([np.sin(2 * np.pi * P[:, 1]), np.sin(2 * np.pi * P[:, 2]), np.sin(2 * np.pi * P[:, 0])], 1)
NG = 20                                                 # finer grid, so the S-curves come out smooth
def solid(faces):
    """as domed_octet.solid, but every mesh vertex bent first (shared vertices bend alike, so neighbours still meet exactly)"""
    V, T, key = [], [], {}
    for P, sign, out in faces:
        pts, tris = patch(np.array(P, float), sign, out); loc = []
        for p in pts:
            k = tuple(np.round(p, 9))
            if k not in key: key[k] = len(V); V.append(p)
            loc.append(key[k])
        for a, b, c in tris:
            n = np.cross(V[loc[b]] - V[loc[a]], V[loc[c]] - V[loc[a]])
            T.append([loc[a], loc[b], loc[c]] if n @ out >= 0 else [loc[a], loc[c], loc[b]])
    W = bend(np.array(V, float))
    return m3.Manifold(m3.Mesh(vert_properties=np.array(W, np.float32), tri_verts=np.array(T, np.uint32)))
if __name__ == '__main__':
    assert 2 * np.pi * E < 1
    edge = np.array([[t, t, 0] for t in np.linspace(0, 1, 9)])
    print('an edge (0,0,0)-(1,1,0) bent, displacement:', np.round(bend(edge) - edge, 3).tolist())
    pieces = [('oct', octa((x, y, z))) for x, y, z in itertools.product(range(-1, 3), repeat=3) if (x + y + z) % 2] + [('tet', tet(V)) for _, V in tets_in(range(-1, 3))]
    print('all solids valid:', all(p.status() == m3.Error.NoError for _, p in pieces), '; volumes tet', sorted({round(p.volume(), 4) for k, p in pieces if k == 'tet'}), 'oct', sorted({round(p.volume(), 4) for k, p in pieces if k == 'oct'}))
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 box: volume {tot:.5f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 2e-3 and over < 1e-4 else 'FAIL')
