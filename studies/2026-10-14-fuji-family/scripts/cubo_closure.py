# Cuboctahedral closure test (DICTO, 2026-10-14): the cubic analogue of DICTO's 63-piece Lotus seed (dodecahedron + 12 J11 on its
# pentagons + 30 AXE in the grooves + 20 FUJI at the corners). Here: a unit cube + 6 unit cuboctahedra, each sharing a square with
# a face of the cube. Measures the hull, the gaps at the cube's 12 edges and 8 corners, and compares the corner pocket with
# FUJI((sqrt3 - 1)/2). DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cube = np.array(list(itertools.product((-.5, .5), repeat=3)))
cubo0 = np.array([p for p in set(itertools.permutations((1, 1, 0))) | set(itertools.permutations((1, -1, 0))) | set(itertools.permutations((-1, -1, 0)))] , float)
cubo0 = np.unique(np.round(cubo0, 9), axis=0) / math.sqrt(2)  # edge 1 (vertices at distance 1 from centre)
assert len(cubo0) == 12
# a square face of cubo0 lies at x = 1/sqrt2; shift so it sits on the cube face x = 0.5 (and its square must match the cube face:
# the cuboctahedron's square has edge 1 and corners (1/sqrt2, +-1/sqrt2... ) -> rotate 45 degrees about x so the square is axis-aligned)
c, s = math.cos(math.pi / 4), math.sin(math.pi / 4)
Rx = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
cub = cubo0 @ Rx.T
sq = cub[np.isclose(cub[:, 0], cub[:, 0].max())]
assert len(sq) == 4 and np.allclose(np.sort(np.abs(sq[:, 1:]).ravel()), .5), sq
shift = .5 - cub[:, 0].max() + cub[:, 0].max() * 0  # place that square on x = +0.5 from outside: the cuboctahedron is outside the cube
pieces = [('cube', cube)]
for axis in range(3):
    for sgn in (1, -1):
        P = cub.copy(); P[:, 0] = -P[:, 0] + cub[:, 0].max()   # mirror so the square is at x = 0, body at x > 0... then move
        P[:, 0] += .5
        P = P[:, [(0 - axis) % 3, (1 - axis) % 3, (2 - axis) % 3]] if False else np.roll(P, axis, axis=1)
        P *= np.where(np.arange(3) == axis, sgn, 1)
        pieces.append((f'cubo{axis}{"+" if sgn > 0 else "-"}', P))
vol = lambda P: ConvexHull(P).volume
allv = np.vstack([P for _, P in pieces]); H = ConvexHull(allv)
V_pieces = sum(vol(P) for _, P in pieces)
out = dict(cubeVolume=vol(cube), cuboVolume=vol(pieces[1][1]), hullVolume=H.volume, piecesVolume=V_pieces, gapVolume=H.volume - V_pieces)
# overlaps (separating axis on convex hulls, cheap test by sampling)
rng = np.random.default_rng(1); pts = rng.uniform(allv.min(0), allv.max(0), size=(300000, 3))
def inside(P, X):
    h = ConvexHull(P); return np.all(X @ h.equations[:, :3].T + h.equations[:, 3] <= 1e-9, axis=1)
ins = np.array([inside(P, pts) for _, P in pieces]); out['overlapSamples'] = int((ins.sum(0) > 1).sum())
inhull = inside(allv, pts); gap = inhull & (ins.sum(0) == 0)
out['gapFractionSampled'] = float(gap.sum() / inhull.sum())
# hull faces
eq = np.unique(np.round(H.equations, 6), axis=0); out['hullFaces'] = len(eq)
# corner pocket: gap samples near the corner (+,+,+)
corner = gap & np.all(pts > .5 - 1e-9, axis=1) & (np.linalg.norm(pts - .5, axis=1) < 1.2)
out['cornerGapVolumeEstimate'] = float(corner.sum() / len(pts) * np.prod(allv.max(0) - allv.min(0)))
r = (3 ** .5 - 1) / 2; R2 = (1 + r + r * r) / 3; h = math.sqrt(1 - R2)
out['FUJI_cubo_volume'] = math.sqrt(3) / 12 * (1 + 4 * r + r * r) * h
json.dump(out, open(os.path.join(ROOT, 'cubo-closure.json'), 'w'), indent=1)
for k, v in out.items(): print(k, v)
