# DICTO 2026-10-20: the double octet set as DICTO wants it: the octahedron's faces alternate (dome next to hollow, checkerboard), and the
# tetrahedron has 2 domed and 2 hollow faces ("two triangles of each, pivoting and folding into the tetrahedron"). Realised by turning the
# octahedra: their centres (integer points of odd sum) form four interleaved cubic lattices, (odd, even, even), (even, odd, even),
# (even, even, odd), (odd, odd, odd), and every tetrahedron touches one octahedron from each; on the first two the T+ faces are domed, on
# the other two the T- faces. So every tetrahedron meets 2 domes and 2 hollows: ONE octahedron piece (two turns) and ONE tetrahedron piece.
# Domes: the pillow faces of domed_octet.py (straight edges). Float, manifold3d: a 2 x 2 x 2 block, congruence of all tetrahedra; figures.
import itertools, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'domed_octet.py')).read().split("def tet(V, convex):")[0])
T_MINUS = {tuple(-x for x in n) for n in T_PLUS}
plus = lambda cen: sum(int(c) % 2 for c in cen) == 1 and (int(cen[0]) % 2 == 1 or int(cen[1]) % 2 == 1)   # (o,e,e) or (e,o,e)
def octa(cen):
    cen = np.array(cen, float); D = T_PLUS if plus(cen) else T_MINUS; F = []
    for sg in itertools.product((1, -1), repeat=3):
        P = np.array([cen + sg[j] * np.eye(3)[j] for j in range(3)]); F.append((P, 1 if tuple(sg) in D else -1, np.array(sg, float) / np.sqrt(3)))
    return solid(F)
def tet_signs(V):
    V = np.array(V, float); c = V.mean(0); out = []
    for k in range(4):
        f = [i for i in range(4) if i != k]; P = V[f]; ocen = (P.sum(0) - V[k]) / 2           # the octahedron across this face
        n = np.sign(P.mean(0) - c).astype(int); D = T_PLUS if plus(ocen) else T_MINUS
        out.append((P, -1 if tuple(-n) in D else 1))                                          # its dome there is our hollow, and back
    return out
def tet(V):
    V = np.array(V, float); c = V.mean(0); F = []
    for P, s in tet_signs(V):
        n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        if n @ (P.mean(0) - c) < 0: n = -n
        F.append((P, s, n))
    return solid(F)
def tets_in(rng):
    for x, y, z in itertools.product(rng, repeat=3):
        base = np.array([x, y, z], float)
        corners = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if (x + y + z) % 2 == 0 else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
        yield base, base + np.array(corners, float)
if __name__ == '__main__':
    counts = [sorted(s for _, s in tet_signs(V)) for _, V in tets_in(range(-2, 3))]
    print('every tetrahedron: 2 domes and 2 hollows ->', 'PASS' if all(c == [-1, -1, 1, 1] for c in counts) else 'FAIL', f'({len(counts)} checked)')
    pieces = [('oct', octa((x, y, z))) for x, y, z in itertools.product(range(-1, 3), repeat=3) if (x + y + z) % 2] + [('tet', tet(V)) for _, V in tets_in(range(-1, 3))]
    vols = {k: sorted({round(p.volume(), 6) for kk, p in pieces if kk == k}) for k in ('tet', 'oct')}
    print('piece volumes (one each = one shape by volume):', vols)
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 block: volume {tot:.6f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 1e-4 and over < 1e-5 else 'FAIL')
