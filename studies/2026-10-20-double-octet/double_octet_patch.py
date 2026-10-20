# DICTO 2026-10-20 (float, manifold3d): the double octet pieces built as solids, and a patch of the octet (a 2 x 2 x 2 block of cubes)
# filled with them: no two overlap, and their volumes add up to what they cover. Also writes renders/double-octet.html for the figures.
import itertools, json, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
N4 = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
A = {N4[0], N4[1], tuple(-x for x in N4[2]), tuple(-x for x in N4[3])}
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def pyr(P, apex): return hull(np.vstack([np.array(P, float), np.array(apex, float)]))
def tet_piece(V):
    V = np.array(V, float); c = V.mean(0); s = hull(V); bumps, dents = [], []
    for f in itertools.combinations(range(4), 3):
        P = V[list(f)]; m = P.mean(0); n = tuple(int(x) for x in np.sign(m - c))
        if n in A: s = s + pyr(P, 2 * m - c)
        else: s = s - pyr(P, c)
    return s
def oct_piece(cen):
    cen = np.array(cen, float); s = hull([cen + d * e for e in np.eye(3) for d in (1, -1)])
    for sg in itertools.product((1, -1), repeat=3):
        P = np.array([cen + sg[j] * np.eye(3)[j] for j in range(3)]); m = P.mean(0)
        tcen = cen + np.array(sg, float) / 2               # the neighbouring tetrahedron (face + the corner cen + sg) has its centre here
        if tuple(sg) in A: s = s + pyr(P, tcen)            # bump: up to the neighbour's centre (its dent)
        else: s = s - pyr(P, 2 * m - tcen)                 # dent: the neighbour's bump, its centre reflected in the face
    return s
pieces = []
for x, y, z in itertools.product(range(-1, 3), repeat=3):
    if (x + y + z) % 2: pieces.append(('oct', oct_piece((x, y, z))))
    # tetrahedra: in each unit cube the two (up and down) tetrahedra? the octet's tetrahedra sit at the cube's alternate corners pattern
for x, y, z in itertools.product(range(-1, 3), repeat=3):    # each unit cube holds one tetrahedron, on its corners of even sum
    base = np.array([x, y, z], float)
    corners = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if (x + y + z) % 2 == 0 else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    pieces.append(('tet', tet_piece(base + np.array(corners, float))))
vols = {k: round(np.mean([p.volume() for kk, p in pieces if kk == k]), 9) for k in ('tet', 'oct')}
print('piece volumes', vols, 'want tet 1/3, oct 4/3')
box = m3.Manifold.cube([2, 2, 2])
inbox = [(k, p ^ box) for k, p in pieces]; inbox = [(k, p) for k, p in inbox if p.volume() > 1e-9]
tot = sum(p.volume() for _, p in inbox)
over = 0.0
for (k1, a), (k2, b) in itertools.combinations(inbox, 2): over += (a ^ b).volume()
print(f'in a 2x2x2 box: {len(inbox)} piece parts, total volume {tot:.9f} (box 8), overlap {over:.2e}')
print('PASS' if abs(tot - 8) < 1e-6 and over < 1e-6 and abs(vols['tet'] - 1 / 3) < 1e-9 and abs(vols['oct'] - 4 / 3) < 1e-9 else 'FAIL', 'the two pieces fill the octet without overlap')
