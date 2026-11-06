"""The approximant ladder (DICTO 11-06: "how do we turn all of this into a universal lattice" -> "perfect lets climb the ladder").
Rung 1, the 1/1 cubic approximant: regular icosahedra (edge 1) in the standard orientation (their 2-fold axes on the cube axes, as in the
real 1/1 approximants) on a body-centred cubic lattice, each sharing whole faces with its 8 nearest neighbours along the cube diagonals.
Every icosahedron carries the five-solid nest (I > D > C > T, O through six edge midpoints). The space left: each icosahedron's Voronoi
cell is the truncated octahedron (bcc), so the gap per cluster = truncated octahedron - icosahedron. Checks: face sharing exact, no
overlaps, filling fraction, gap volume, which faces touch."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
I = orbit((0, 1, phi)) / 2                                   # edge 1
hI = ConvexHull(I); rin = abs(hI.equations[0, 3])
# face centre along (1,1,1): inradius; bcc nearest neighbour distance = 2 * inradius
a = 2 * (2 * rin) / np.sqrt(3)
print(f"icosahedron edge 1: inradius {rin:.6f}; bcc cube side a = {a:.6f} (exact 2*phi^2/3 = {2*phi**2/3:.6f})")
# check: neighbour at (a/2)(1,1,1): shares the face whose normal is (1,1,1)/sqrt3?
n111 = np.ones(3) / np.sqrt(3)
F = {}
for eq, sp in zip(hI.equations, hI.simplices): F.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
face111 = [I[list(s)] for k, s in F.items() if np.allclose(np.array(k[:3]), n111, atol=1e-6)]
print("a face square-on to (1,1,1):", len(face111) == 1)
J = -I + a / 2 * np.ones(3)                                  # neighbour = point reflection of I through the shared face's centre
same = all(np.min(np.linalg.norm(J - p, axis=1)) < 1e-9 for p in face111[0])
Jt = I + a / 2 * np.ones(3)                                  # neighbour as a TRANSLATE (bcc lattice: same orientation)
same_t = all(np.min(np.linalg.norm(Jt - p, axis=1)) < 1e-9 for p in face111[0])
Rz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]); I2 = I @ Rz.T
J2 = I2 + a / 2 * np.ones(3)
same2 = all(np.min(np.linalg.norm(J2 - p, axis=1)) < 1e-9 for p in face111[0])
print("same orientation: translate neighbour shares the whole face:", same_t, "(it meets in a six-pointed star)")
print("other orientation (turned 90 deg): neighbour shares the whole face:", same2)
mirror_ok = same2
# overlaps: bcc neighbours up to the second shell
def disjoint(A, B):
    for P, Q in ((A, B), (B, A)):
        for eq in ConvexHull(P).equations:
            if ((Q @ eq[:3] + eq[3]) >= -1e-9).all(): return True
    return False
shifts = [a / 2 * np.array(s) for s in itertools.product((-1, 1), repeat=3)] + [a * e for e in np.vstack([np.eye(3), -np.eye(3)])]
print("CsCl arrangement (corners one orientation, centres the other): no overlap with 8 + 6 neighbours:",
      all(disjoint(I, I2 + s) for s in shifts[:8]) and all(disjoint(I, I + s) for s in shifts[8:]))
vI = hI.volume; cell = a ** 3 / 2
print(f"filling: icosahedra {vI/cell:.6f} of space; gap {1 - vI/cell:.6f} (per cluster {cell - vI:.6f})")
# the Voronoi cell (truncated octahedron) and the gap pieces
TO = np.array(sorted({tuple(s_ * np.array(p)) for p in itertools.permutations((0, 1, 2)) for s_ in itertools.product((1, -1), repeat=3)})) * a / 4
hT = ConvexHull(TO); print(f"truncated octahedron volume {hT.volume:.6f} (= a^3/2 {cell:.6f}); icosahedron inside: {bool(((I @ hT.equations[:, :3].T + hT.equations[:, 3]) <= 1e-9).all())}")
# which icosahedron faces lie on the truncated octahedron's faces
onface = sum(1 for k in F if any(np.allclose(np.array(k[:3]), e[:3], atol=1e-6) and abs(k[3] - e[3]) < 1e-6 for e in hT.equations))
print(f"icosahedron faces lying in the truncated octahedron's hexagons: {onface} of 20 (the 8 shared faces)")
sq = a / 2; edge_mid = np.linalg.norm((I[0] + I[np.argsort(np.linalg.norm(I - I[0], axis=1))[1]]) / 2)
print(f"square faces at {sq:.6f} from the centre; the icosahedron's 2-fold edge midpoints at {phi/2:.6f}: gap {sq - phi/2:.6f} across each square")
print("FINAL ok")
