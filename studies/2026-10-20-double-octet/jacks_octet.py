# DICTO 2026-10-20: rounded interlocking jacks that fill space ("smooth washed broken coral, six legs and four legs", octet places):
#   a SIX-LEGGED JACK at every octahedron centre, thick tapering legs to the octahedron's 6 corners;
#   a TETRAPOD (four legs) at every tetrahedron centre, legs out through the tetrahedron's 4 faces into the jacks' hollows (between
#   the jack's legs), so the legs interlock: each jack has 6 legs out and 8 tetrapod legs in. (Legs to the corners as well, tried
#   first, only gave back the octahedron and tetrahedron: both pieces' legs met at the same corners.)
# DICTO: "form the lattice in the structure you want the legs to be". So the legs are drawn first, as a skeleton: a segment from every
# octahedron centre to each of its 6 corners and from every tetrahedron centre to each of its 4 corners. Each leg is a fat tapering
# rod (radius RHO0 at the body, RHO1 at the tip); every point of space goes to the piece whose rods it is nearest (distance to the rod's
# axis minus the rod's radius there; legs blended smoothly at the body). An argmin, so no gaps and no overlaps by construction, and no
# piece can break apart (each piece holds its own skeleton). Meshed by marching cubes; checked: one jack shape, one tetrapod shape,
# volumes add up to space.
import itertools, sys, numpy as np, manifold3d as m3
from skimage.measure import marching_cubes
from scipy.ndimage import gaussian_filter
RHO_OCT, TIP_OCT, RHO_TET, TIP_TET, TET_LEN, K, STEP = 0.21, 0.06, 0.17, 0.06, 0.78, 0.04, 0.02
if len(sys.argv) > 4: RHO_OCT, TIP_OCT, RHO_TET, TIP_TET = map(float, sys.argv[1:5])
AX = np.vstack([np.eye(3), -np.eye(3)])
def tet_legs(t):
    t = np.array(t, float); C = np.array([t + .5 * np.array(s) for s in itertools.product((1, -1), repeat=3)])
    C = C[[int(round(p.sum())) % 2 == 0 for p in C]]; L = C - t; return L / np.linalg.norm(L, axis=1)[:, None]
def centres_near(c, rad):
    """(centre, legs, A, W) for octahedron centres (odd-sum integer points) and tetrahedron centres (half-integer points) near c"""
    c = np.array(c, float); out = []; lo = np.floor(c - rad).astype(int); hi = np.ceil(c + rad).astype(int)
    for p in itertools.product(*[range(a, b + 1) for a, b in zip(lo, hi)]):
        p = np.array(p, float)
        if int(p.sum()) % 2 and np.linalg.norm(p - c) <= rad: out.append((p, AX, RHO_OCT, TIP_OCT))
        q = p + .5
        if np.linalg.norm(q - c) <= rad: out.append((q, -tet_legs(q), RHO_TET, TIP_TET))
    return out
def field(X, c, L, RHO0, RHO1):
    """distance to c's skeleton of fat tapering legs (legs end at the corners), legs blended smoothly (soft minimum, width K)"""
    R0 = 1.0 if len(L) == 6 else TET_LEN; D = X - c; ds = []
    for l in L:
        t = np.clip(D @ l / R0, 0, 1); ds.append(np.linalg.norm(D - np.outer(t * R0, l), axis=1) - (RHO0 * (1 - t) + RHO1 * t))
    ds = np.array(ds); m = ds.min(0); return m - K * np.log(np.exp(-(ds - m) / K).sum(0))
# the texture (DICTO: flattened triangles and hexagons, interlocking with the opposite piece): a relief added to the boundary between the
# pieces, + on the Oktjiru's distance and - on the Tetjiru's, so where one rises the other has the matching hollow (still a partition).
# The pattern: three waves at 120 deg on any face (from the four tetrahedral directions), flattened into plateaus: raised hexagons and
# sunk triangles, the impression of the triangle-hexagon tiling on the curved walls. TEX = 0 turns it off.
import os as _os
TEX = float(_os.environ.get('TEX', '0')); TEX_N, TEX_SHARP = 7, 4.0
# wave vectors pi N (+-1, +-1, +-1): a whole number of waves along every lattice step (1,1,0) etc., so every Oktjiru (and every Tetjiru
# of a turn) carries the same texture: still one shape each. Wavelength 2 / (N sqrt3) = 0.165.
_TD = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
def texture(X):
    w = np.cos(np.pi * TEX_N * (X @ _TD.T)).sum(1); return np.tanh(TEX_SHARP * w)
_field = field
def field(X, c, L, RHO0, RHO1):
    f = _field(X, c, L, RHO0, RHO1)
    return f if not TEX else f + (TEX if len(L) == 6 else -TEX) * texture(X)
_cache = {}
def piece_mesh(c, legs, A, W, half=1.35):
    """the piece of centre c: marching cubes on g = f_c - min over the others, on a grid round c"""
    c = np.array(c, float); n = int(round(2 * half / STEP)) + 1; ax = np.linspace(-half, half, n)
    G = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3) + c
    others = [o for o in centres_near(c, 2 * half + .2) if np.linalg.norm(o[0] - c) > 1e-9]
    fc = field(G, c, legs, A, W); m = np.full(len(G), np.inf)
    for o in others: m = np.minimum(m, field(G, *o))
    g = gaussian_filter((fc - m).reshape(n, n, n), 0.8 if TEX else 1.2)          # smooths the grid steps away (about 0.02 wide), not the shape
    g[0], g[-1], g[:, 0], g[:, -1], g[:, :, 0], g[:, :, -1] = 1, 1, 1, 1, 1, 1
    V, F, _, _ = marching_cubes(g, 0.0, spacing=(STEP,) * 3); V = V - half + c
    mf = m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(F, np.uint32)))
    if mf.volume() < 0 or mf.status() != m3.Error.NoError:
        mf = m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(F[:, ::-1], np.uint32)))
    return mf
def jack(c):
    if 'jack' not in _cache: _cache['jack'] = piece_mesh((1, 0, 0), AX, RHO_OCT, TIP_OCT)
    return _cache['jack'].translate(list(np.array(c, float) - [1, 0, 0]))
def tetrapod_at(t):
    t = np.array(t, float); key = ('tet', int(round(t.sum() - 1.5)) % 2)
    if key not in _cache: _cache[key] = (t, piece_mesh(t, -tet_legs(t), RHO_TET, TIP_TET))
    t0, mf = _cache[key]; return mf.translate(list(t - t0))
sphere_piece = jack
filler = lambda V: tetrapod_at(np.array(V, float).mean(0))
def tets_in(rng):
    for x, y, z in itertools.product(rng, repeat=3):
        t = np.array([x, y, z], float) + .5; L = tet_legs(t); yield t, t + L * np.sqrt(3) / 2
if __name__ == '__main__':
    J = jack((1, 0, 0)); T0 = tetrapod_at((.5, .5, .5)); T1 = tetrapod_at((1.5, .5, .5))
    print(f'rods: jack {RHO_OCT}->{TIP_OCT}, tetrapod {RHO_TET}->{TIP_TET}; valid', J.status() == m3.Error.NoError, T0.status() == m3.Error.NoError, T1.status() == m3.Error.NoError)
    print(f'volumes: jack {J.volume():.4f}, tetrapods {T0.volume():.4f} {T1.volume():.4f}; jack + 2 tetrapods = {J.volume() + T0.volume() + T1.volume():.4f} (space per jack: 2)')
    # reach: how far each leg goes (along the leg axis) from the centre
    def reach(mf, c, l):
        me = mf.to_mesh(); V = np.asarray(me.vert_properties[:, :3]) - c; return float((V @ l).max())
    print('jack leg reach', round(reach(J, np.array([1., 0, 0]), np.array([1., 0, 0])), 3), '(corner at 1); tetrapod leg reach', round(reach(T0, np.full(3, .5), -tet_legs((.5, .5, .5))[0]), 3), f'(leg {TET_LEN}; face at 0.289, jack centre at 0.866)')
    box = m3.Manifold.cube([2, 2, 2]); pieces = [jack(p) for p in itertools.product(range(-1, 4), repeat=3) if sum(p) % 2] + [tetrapod_at(t) for t, _ in tets_in(range(-1, 3))]
    inb = [p ^ box for p in pieces]; inb = [p for p in inb if p.volume() > 1e-9]; tot = sum(p.volume() for p in inb)
    over = sum((a ^ b).volume() for a, b in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 box: volume {tot:.4f} (8), overlap {over:.2e} (marching-cubes mesh, step {STEP})')
