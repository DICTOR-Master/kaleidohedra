# Figure 2 of #49 (DICTO): the void between two dodecahedra of the #47 layer on edge-sharing cubes.
# Void = hull of the pair minus the two dodecahedra (they share only an edge). Checks: edge 1,
# the two do not overlap, and the void's volume is phi^3 + 1/2 (to rounding).
import numpy as np
from scipy.spatial import ConvexHull
import mixes3 as M
phi = M.phi; D1 = M.DOD; D2 = M.DOD + np.array([phi, phi, 0])
edge = min(np.linalg.norm(a - b) for i, a in enumerate(D1) for b in D1[i + 1:])
h1 = ConvexHull(D1)
inside = lambda X: np.all(X @ h1.equations[:, :3].T + h1.equations[:, 3] < -1e-9, axis=1)
rs = np.random.default_rng(0); X = D2.mean(0) + rs.uniform(-1.5, 1.5, (400000, 3))
h2 = ConvexHull(D2); in2 = np.all(X @ h2.equations[:, :3].T + h2.equations[:, 3] < -1e-9, axis=1)
overlap = int((inside(X) & in2).sum())
vd = ConvexHull(D1).volume; vh = ConvexHull(np.vstack([D1, D2])).volume; void = vh - 2 * vd
print(f'edge {edge:.15f}  overlap samples {overlap}  dodecahedron {vd:.15f}  hull {vh:.15f}')
print(f'void {void:.15f}  phi^3+1/2 {phi**3 + 0.5:.15f}')
assert abs(edge - 1) < 1e-12 and overlap == 0 and abs(void - (phi**3 + 0.5)) < 1e-12
print('PASS')
