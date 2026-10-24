# Positive search (DICTO 10-24): can the polars of the Icosaxes and the Unborn Axes (cubes with face pyramids of height h = 1/phi and
# 1/phi^2, in half cube edges; any size, any turn) fill space together? Step 1: their edge (dihedral) angles, and every way copies of
# them can close up round an edge: n1 copies of angles of P1 + n2 of P2 (+ one straight 180° if the edge runs inside a neighbour's face) = 360°.
import numpy as np, itertools
phi = (1 + 5**.5) / 2
def dihedrals(h):
    c = np.array([1.0, 0, 0]); apex = np.array([1 + h, 0, 0])
    A, B, C = np.array([1., 1, 1]), np.array([1., 1, -1]), np.array([1., -1, 1])
    def normal(p, q, r):
        n = np.cross(q - p, r - p); return n / np.linalg.norm(n) * np.sign(n @ (p + q + r))
    n1 = normal(apex, A, B); n2 = normal(apex, A, C)                   # two triangles of the +x pyramid meeting along apex-A
    apy = np.array([0, 1 + h, 0]); n3 = normal(apy, A, B * np.array([1, 1, 1]))
    n3 = normal(apy, np.array([1., 1, 1]), np.array([1., 1, -1]))    # +y pyramid triangle on the cube edge A-B
    lat = 180 - np.degrees(np.arccos(np.clip(n1 @ n2, -1, 1)))       # interior angle along a pyramid's side edge
    cub = 180 - np.degrees(np.arccos(np.clip(n1 @ n3, -1, 1)))       # interior angle along a cube edge (between two pyramids)
    return lat, cub
P1, P2 = dihedrals(1/phi), dihedrals(1/phi**2)
print('polar of the Icosaxes (h = 1/φ):   side-edge angle %.6f°, cube-edge angle %.6f°' % P1)
print('polar of the Unborn Axes (h = 1/φ²): side-edge angle %.6f°, cube-edge angle %.6f°' % P2)
print('check, rhombic dodecahedron (h = 1): ', '%.3f°, %.3f°' % dihedrals(1.0))
angles = [('P1 side', P1[0]), ('P1 cube', P1[1]), ('P2 side', P2[0]), ('P2 cube', P2[1])]
found = []
for ns in itertools.product(range(0, 7), repeat=4):
    if sum(ns) == 0: continue
    s = sum(n * a for n, (_, a) in zip(ns, angles))
    for flat in (0, 1):
        if abs(s + 180 * flat - 360) < 1e-7:
            found.append((ns, flat))
print(f'{len(found)} ways to close up round an edge:')
for ns, flat in found:
    uses = [f'{n}×{name}' for n, (name, _) in zip(ns, angles) if n]
    print('  ' + ' + '.join(uses) + (' + a flat face (180°)' if flat else '') + ('   <- mixes both solids' if (ns[0] or ns[1]) and (ns[2] or ns[3]) else ''))
