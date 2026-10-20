# DICTO 2026-10-20 (variant, DICTO: "spheres with 8 dimples, small rounded tetrahedra"): every sphere has 8 dimples, every filler 4
# bumps; no turning: all spheres one shape, all fillers one shape. Was: two rounded pieces on the octet (DICTO: "1 piece a sphere with 8 bumps/dimples", 4 bumps + 4 dimples; the second
# piece "fills between the spheres"):
#   the SPHERE: each octahedron cut down to the ball through the midpoints of its edges (radius 1/sqrt2 at edge sqrt2): a sphere with 8
#     flat round patches (the faces' inscribed circles, radius 1/sqrt6); on them 4 bumps and 4 dimples, checkerboard, the octahedra turned
#     on two of the four sublattices so every filler meets 2 bumps and 2 dimples (folding_octet.py);
#   the FILLER: a tetrahedron plus, across each of its faces, the part of the neighbouring octahedron outside its ball in that face's
#     octant (the octahedron's eight octants each go to the tetrahedron on their face): one piece that wraps the spheres.
# A partition of space by construction. Bump: H (1 - (r/a)^2)^2 over the patch (a = 1/sqrt6), flat to the sphere at its rim.
# Float, manifold3d: a block filled exactly, pieces congruent.
import itertools, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
T_PLUS = set(); T_MINUS = set()                     # the spheres' bump set is empty: all 8 faces dimpled
plus = lambda c: True
plus_ = lambda c: sum(int(round(x)) % 2 for x in c) == 1 and (int(round(c[0])) % 2 == 1 or int(round(c[1])) % 2 == 1)
RB = 1 / np.sqrt(2); A = 1 / np.sqrt(6); H = 0.14; SEG = 96; NR, NA = 10, 48
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
ball = lambda c: m3.Manifold.sphere(RB, SEG).translate(list(np.array(c, float)))
def bump(c, s):
    """the solid between an octahedron's face patch (normal s, at distance 1/sqrt3 from the centre c) and the bump surface above it"""
    c = np.array(c, float); n = np.array(s, float) / np.sqrt(3); f0 = c + n / np.sqrt(3)
    u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
    top, bot = [], []
    for i in range(NR + 1):
        r = A * i / NR
        for j in range(NA if i else 1):
            t = 2 * np.pi * j / NA; p = f0 + r * (np.cos(t) * u + np.sin(t) * w)
            top.append(p + H * (1 - (r / A) ** 2) ** 2 * n); bot.append(p - 1e-4 * n)
    return hull(np.vstack([top, bot]))            # the bump is convex (a smooth cap), so its hull is it
def octa_solid(c):
    c = np.array(c, float); return hull([c + d * e for e in np.eye(3) for d in (1, -1)])
def sphere_piece(c):
    D = T_PLUS if plus(c) else T_MINUS; m = octa_solid(c) ^ ball(c)
    for s in itertools.product((1, -1), repeat=3):
        m = (m + bump(c, s)) if tuple(s) in D else (m - mirror_bump(c, s))
    return m
def mirror_bump(c, s):
    """the dimple on face s: the neighbouring filler's bump into this sphere = the bump surface reflected into the octahedron"""
    c = np.array(c, float); n = np.array(s, float) / np.sqrt(3); f0 = c + n / np.sqrt(3)
    u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
    top, bot = [], []
    for i in range(NR + 1):
        r = A * i / NR
        for j in range(NA if i else 1):
            t = 2 * np.pi * j / NA; p = f0 + r * (np.cos(t) * u + np.sin(t) * w)
            top.append(p - H * (1 - (r / A) ** 2) ** 2 * n); bot.append(p + 1e-4 * n)
    return hull(np.vstack([top, bot]))
def filler(V):
    """tetrahedron V + the octant of each face-neighbour octahedron outside its ball, with the bumps/dimples swapped"""
    V = np.array(V, float); c = V.mean(0); m = hull(V)
    for k in range(4):
        P = V[[i for i in range(4) if i != k]]; oc = (P.sum(0) - V[k]) / 2           # the octahedron across this face
        s = tuple(int(x) for x in np.sign(P.mean(0) - oc))                             # this face's octant of that octahedron
        rim = hull(np.vstack([P, oc])) - ball(oc); m = m + rim
        D = T_PLUS if plus(oc) else T_MINUS
        m = m - bump(oc, s) if s in D else m + mirror_bump(oc, s)
    return m
def tets_in(rng):
    for x, y, z in itertools.product(rng, repeat=3):
        base = np.array([x, y, z], float)
        yield base, base + np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if (x + y + z) % 2 == 0 else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)], float)
if __name__ == '__main__':
    pieces = [('sph', sphere_piece((x, y, z))) for x, y, z in itertools.product(range(-1, 3), repeat=3) if (x + y + z) % 2] + [('fill', filler(V)) for _, V in tets_in(range(-1, 3))]
    print('valid:', all(p.status() == m3.Error.NoError for _, p in pieces), '; volumes sphere', sorted({round(p.volume(), 4) for k, p in pieces if k == 'sph'}), 'filler', sorted({round(p.volume(), 4) for k, p in pieces if k == 'fill'}))
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 box: volume {tot:.5f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 2e-3 and over < 2e-3 else 'FAIL')
