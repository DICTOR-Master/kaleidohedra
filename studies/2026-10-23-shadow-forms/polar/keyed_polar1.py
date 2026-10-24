# Hull-and-remainder polar of the keyed pair (DICTO 10-24: "fill them in, maybe invert, then work out the remainder").
# Frame of #48 (icosahedron edge 1, lattice spacing phi): Icosaxes = all perms of (±1/2, ±phi/2, 0) at the origin; Unborn Axes = all
# perms of (±1/(2phi), ±phi/2, 0) at c = (phi/2)(1,1,1). Tricap = corner of a dodecahedron of edge 1/phi: apex + its 3 neighbours.
import numpy as np, itertools
from scipy.spatial import ConvexHull
phi = (1 + 5**.5) / 2
def perms(a, b):
    return np.array(sorted({tuple(sg[i] * p[i] for i in range(3)) for p in itertools.permutations((a, b, 0)) for sg in itertools.product((1, -1), repeat=3)}))
ICO = perms(.5, phi/2); UNB = perms(1/(2*phi), phi/2)
vol = lambda P: ConvexHull(P).volume
def tricap(sx, sy, sz):   # Tricap of the Unborn Axes at its corner direction (sx,sy,sz), in the Unborn frame
    S = np.diag([sx, sy, sz]); ap = S @ np.array([.5, .5, .5])
    nb = [S @ np.array(v) for v in [(0, 1/(2*phi), phi/2), (phi/2, 0, 1/(2*phi)), (1/(2*phi), phi/2, 0)]]
    return np.array([ap] + nb)
TR = [tricap(*s) for s in itertools.product((1, -1), repeat=3)]
vt = vol(TR[0])
print('Tricap volume %.6f = 1/(12 phi^2) %.6f; 8 Tricaps %.6f' % (vt, 1/(12*phi**2), 8*vt))
print('Icosaxes %.6f (1+2√5/3 = %.6f); minus 8 Tricaps = %.6f (Lotus Jewel Axes √5 = %.6f)' % (vol(ICO), 1+2*5**.5/3, vol(ICO) - 8*vt, 5**.5))
print('Unborn Axes %.6f (1+√5/3 = %.6f); plus 8 Tricaps = %.6f (Dodecaxes 2)' % (vol(UNB), 1+5**.5/3, vol(UNB) + 8*vt))
# where the Tricap sits: its base triangle's corners are Unborn Axes corners (so the base lies in a hexagon face)
U = {tuple(np.round(v, 9)) for v in UNB}
print('base corners are Unborn Axes corners:', all(tuple(np.round(v, 9)) in U for t in TR for v in t[1:]))
hexn = np.ones(3)/3**.5; print('base plane distance %.6f, hexagon distance %.6f, apex %.6f (outside: key)' % (TR[0][1] @ hexn, max(UNB @ hexn), TR[0][0] @ hexn))
# and in the Icosaxes frame the same Tricap (moved by -c) lies inside the Icosaxes against its hexagon: a dent
c = np.full(3, phi/2); T0 = TR[7] + c   # the (-,-,-) Tricap of the Unborn at c faces the Icosaxes at the origin
E = ConvexHull(ICO).equations
print('Tricap inside Icosaxes:', bool(((T0 @ E[:, :3].T + E[:, 3]) <= 1e-9).all()), '| base on its hexagon:', np.allclose([v @ hexn for v in T0[1:]], max(ICO @ hexn)))
def polar(P):
    E = ConvexHull(P).equations; return ConvexHull(-E[:, :3] / E[:, 3:4]).points[ConvexHull(-E[:, :3] / E[:, 3:4]).vertices]
for name, P in [('Icosaxes', ICO), ('Unborn Axes', UNB)]:
    Q = polar(P); r = sorted(set(np.round(np.linalg.norm(Q, axis=1), 6)))
    print(f'polar of {name}: {len(Q)} corners at distances {r}')
g = TR[0].mean(0); Q = polar(TR[0] - g)
print('polar of a Tricap about its centroid: %d corners (a tetrahedron), edges' % len(Q), sorted(set(np.round([np.linalg.norm(a-b) for a, b in itertools.combinations(Q, 2)], 4))))
