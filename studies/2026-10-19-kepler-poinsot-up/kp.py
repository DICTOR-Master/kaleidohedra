# DICTO 2026-10-19 "think stellation, think Gaudí", option 2: the tall version of UP grown from the Kepler–Poinsot stars (float first look).
#   I --(great stellated dodecahedron: 20 spikes, tips at 3x the face distance)--> its hull D1 --(small stellated dodecahedron:
#   12 five-sided spires, tips at sqrt5 x the face distance)--> its hull I2 = phi^3 * I, and again.
# Shells: valleys (a hull minus its star) and spikes (the next star's points). Volumes and piece kinds, checked by random points.
import itertools, numpy as np
from collections import Counter
from scipy.spatial import ConvexHull, Delaunay
from frame import I, planes, hv, PHI
def spikes(core, f):
    n, d = planes(core); out = []
    for k in range(len(d)):
        F = core[np.abs(core @ n[k] - d[k]) < 1e-9]; out.append(np.vstack([F, n[k] * d[k] * f]))
    return out
GSD = spikes(I, 3.0); D1 = np.array([p[-1] for p in GSD])
SSD = spikes(D1, 5 ** .5); I2 = np.array([p[-1] for p in SSD])
print('I2 / I =', np.linalg.norm(I2[0]) / np.linalg.norm(I[0]), ' phi^3 =', PHI ** 3)
vI, vD1, vI2 = hv(I), hv(D1), hv(I2)
vG = vI + sum(hv(p) for p in GSD); vS = vD1 + sum(hv(p) for p in SSD)
print(f'vol: I {vI:.5f}  GSD {vG:.5f}  D1 {vD1:.5f}  SSD {vS:.5f}  I2 {vI2:.5f}')
print(f'valleys D1-GSD {vD1 - vG:.5f}   SSD spikes {vS - vD1:.5f}   valleys I2-SSD {vI2 - vS:.5f}')
# spike heights against the face size
def tall(core, f):
    n, d = planes(core); F = core[np.abs(core @ n[0] - d[0]) < 1e-9]; rf = np.linalg.norm(F - F.mean(0), axis=1).mean()
    return (f - 1) * d[0] / rf
print(f'spike height / face radius: GSD {tall(I, 3.0):.3f}, SSD {tall(D1, 5 ** .5):.3f}')
# the valleys D1 - GSD as connected pieces: sample, keep points in D1 outside I and all spikes, cluster by nearest of candidate centres
def gap_points(hull, star_parts, core, n=400000, seed=0):
    rng = np.random.default_rng(seed); R = np.linalg.norm(hull, axis=1).max()
    P = rng.uniform(-R, R, (n, 3)); P = P[Delaunay(hull).find_simplex(P) >= 0]
    out = Delaunay(core).find_simplex(P) < 0
    for s in star_parts: out &= Delaunay(s).find_simplex(P) < 0
    return P[out]
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
def components(P, h):
    t = cKDTree(P); pairs = t.query_pairs(h, output_type='ndarray')
    import scipy.sparse as sp
    A = sp.coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(len(P), len(P)))
    return connected_components(A, directed=False)
for name, hull, parts, core in [('valleys D1 - GSD', D1, GSD, I), ('valleys I2 - SSD', I2, SSD, D1)]:
    P = gap_points(hull, parts, core); nc, lab = components(P, 0.035 * np.linalg.norm(hull, axis=1).max())
    sizes = Counter(lab); big = [c for c, k in sizes.items() if k > 30]
    print(f'{name}: {len(big)} pieces, point counts per piece {sorted(Counter(sizes[c] // 50 * 50 for c in big).items())}')
