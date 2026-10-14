# Tetrapods, new shapes (DICTO, 2026-10-14). DICTO asked for shapes made for the group, not more rhombic dodecahedra: one polyhedron,
# part of its own space filling, with four meeting at a point or four round one. Two candidates, checked numerically:
#  A. the diamond cell: the Voronoi cell of the diamond pattern (each point has four nearest neighbours in tetrahedral directions);
#  B. a keyed truncated octahedron: pyramids out on four alternate hexagons, the same pyramids in on the other four, so it still
#     tiles by translation (the bump across each hexagon fits the dent of the neighbour).
# Checks: faces, volume, the five-piece cluster, cells per corner of the tiling, and (B) a sampled no-gap/no-overlap test by
# winding numbers. Writes ../new/new-shapes.json. DICTO · dictospheres.com
import json, itertools, os
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'new')
rng = np.random.default_rng(14)

def voronoi_cell(c, pts):
    """Convex Voronoi cell of point c among pts, as (vertices, faces) with faces as outward loops."""
    hs = []
    for p in pts:
        d = p - c
        if not d.any(): continue
        m = (p + c) / 2
        hs.append(np.r_[d, -d @ m])           # d·x - d·m <= 0
    hi = HalfspaceIntersection(np.array(hs), c.astype(float))
    return hull_faces(hi.intersections)

def hull_faces(P):
    P = np.unique(np.round(P, 9), axis=0); h = ConvexHull(P)
    planes = {}
    for eq, simp in zip(h.equations, h.simplices):
        key = tuple(np.round(eq, 6)); planes.setdefault(key, set()).update(simp)
    faces = []
    for key, idx in planes.items():
        n = np.array(key[:3]); idx = list(idx); ctr = P[idx].mean(0)
        u = P[idx[0]] - ctr; u /= np.linalg.norm(u); v = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((P[i] - ctr) @ v, (P[i] - ctr) @ u))
        faces.append([int(i) for i in idx])
    return P, faces

def volume(V, F):
    s = 0
    for f in F:
        for k in range(1, len(f) - 1): s += np.dot(V[f[0]], np.cross(V[f[k]], V[f[k + 1]]))
    return s / 6

def tris(V, F):
    return np.array([[V[f[0]], V[f[k]], V[f[k + 1]]] for f in F for k in range(1, len(f) - 1)])

def winding(T, X):
    """Winding numbers of points X (n,3) for the closed triangle soup T (m,3,3) (van Oosterom-Strackee)."""
    a = T[None, :, 0, :] - X[:, None, :]; b = T[None, :, 1, :] - X[:, None, :]; c = T[None, :, 2, :] - X[:, None, :]
    la, lb, lc = (np.linalg.norm(x, axis=2) for x in (a, b, c))
    num = np.einsum('ijk,ijk->ij', a, np.cross(b, c))
    den = la * lb * lc + np.einsum('ijk,ijk->ij', a, b) * lc + np.einsum('ijk,ijk->ij', b, c) * la + np.einsum('ijk,ijk->ij', c, a) * lb
    return (2 * np.arctan2(num, den)).sum(1) / (4 * np.pi)

def solid_angle_at(V, F, vi):
    """Solid angle of the corner vi of a polyhedron (from its winding contribution at a point just inside, scaled)."""
    T = tris(V, F); x = V[vi][None, :]
    # small sphere around the corner: fraction of directions pointing inside
    d = rng.normal(size=(4000, 3)); d /= np.linalg.norm(d, axis=1)[:, None]
    w = winding(T, x + 1e-3 * d)
    return 4 * np.pi * float((np.abs(w - 1) < 0.5).mean())

def corner_degrees(cells):
    """For a patch of cells (list of (V,F)), how many cells share each vertex (vertices well inside the patch only)."""
    cnt = {}
    for V, F in cells:
        for v in np.round(V, 6): cnt[tuple(v)] = cnt.get(tuple(v), 0) + 1
    return cnt

res = {'credit': 'DICTO (design study with Claude), 2026-10-14', 'shapes': {}}

# ---------------- A. the diamond cell ----------------
R = range(-8, 9)
fcc = np.array([p for p in itertools.product(R, R, R) if all(x % 2 == 0 for x in p) and sum(p) % 4 == 0])
dia = np.vstack([fcc, fcc + 1])
near = lambda c, r=6: dia[np.linalg.norm(dia - c, axis=1) <= r]
V, F = voronoi_cell(np.zeros(3), near(np.zeros(3)))
kinds = {}
for f in F: kinds[len(f)] = kinds.get(len(f), 0) + 1
bonds = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
hexes = [f for f in F if len(f) == 6]
hexdirs = sorted(tuple(np.sign(np.round(V[f].mean(0), 6)).astype(int)) for f in hexes)
volA = volume(V, F)
# the neighbour across each hexagon is the cell of the bonded point, the same cell turned (the diamond's two sublattices)
nb = voronoi_cell(np.array([1, 1, 1]), near(np.array([1, 1, 1])))
turned = (-V + 1)                                    # point inversion at the bond midpoint
same = np.allclose(np.sort(np.round(nb[0], 6), axis=0), np.sort(np.round(turned, 6), axis=0))
# corners: cells meeting at each corner, from a patch of cells round the origin
patch = [voronoi_cell(c, near(c)) for c in dia if np.linalg.norm(c) <= 3.5]
deg = corner_degrees(patch)
degV = sorted({deg[tuple(v)] for v in np.round(V, 6)})
edge = sorted({round(float(np.linalg.norm(V[f[k]] - V[f[(k + 1) % len(f)]])), 4) for f in F for k in range(len(f))})
res['shapes']['diamond-cell'] = dict(
    name='diamond cell (Voronoi cell of the diamond pattern; classically the triakis truncated tetrahedron)',
    scale='cube of the diamond pattern = 4 (bond length √3)', faces=len(F), face_kinds=kinds, vertices=len(V),
    volume=round(volA, 6), volume_check=round(4 ** 3 / 8, 6), edge_lengths=edge,
    hexagons_point_along_the_four_bonds=hexdirs == sorted(map(tuple, bonds)),
    neighbour_across_hexagon_is_the_same_cell_turned=bool(same),
    cells_meeting_at_its_corners=degV,
    four_round_one=bool(hexdirs == sorted(map(tuple, bonds)) and same),
    four_meeting_at_a_point=bool(degV == [4]))
json.dump({'vertices': V.round(6).tolist(), 'faces': F}, open(os.path.join(OUT, 'diamond-cell.json'), 'w'))
print('A diamond cell', res['shapes']['diamond-cell'])

# ---------------- B. the keyed truncated octahedron ----------------
Rb = range(-6, 7)
bcc = np.array([p for p in itertools.product(Rb, Rb, Rb) if all(x % 2 == 0 for x in p) or all(x % 2 == 1 for x in p)])
nearb = lambda c, r=3: bcc[np.linalg.norm(bcc - c, axis=1) <= r]
TV, TF = voronoi_cell(np.zeros(3), nearb(np.zeros(3)))
volTO = volume(TV, TF)

def keyed(h):
    Vs = [v for v in TV]; Fs = []
    for f in TF:
        if len(f) != 6: Fs.append(list(f)); continue
        c = TV[f].mean(0); n = c / np.linalg.norm(c)
        up = np.prod(np.sign(np.round(c, 6))) > 0            # four alternate hexagons (tetrahedral set) bump out, the others dent in
        Vs.append(c + (h if up else -h) * n); a = len(Vs) - 1
        for k in range(6): Fs.append([f[k], f[(k + 1) % 6], a])
    return np.array(Vs), Fs

def tiling_check(V, F, n=3000):
    T = tris(V, F)
    X = rng.uniform(0, 2, size=(n, 3))                       # one cube of the bcc lattice holds two cells
    tot = np.zeros(n)
    for t in bcc[np.linalg.norm(bcc - 1, axis=1) <= 4]: tot += np.round(winding(T + t, X))
    return dict(samples=n, covered_once=int((tot == 1).sum()), gaps=int((tot == 0).sum()), overlaps=int((tot > 1).sum()), negative=int((tot < 0).sum()))

edgeTO = float(np.linalg.norm(TV[TF[0][0]] - TV[TF[0][1]]))
out = {}
for h in (0.25, 0.4, 0.5, 0.6):
    KV, KF = keyed(h)
    chk = tiling_check(KV, KF)
    # four round one: the neighbour across a bump hexagon is a translate by that hexagon's bond vector; its dent receives the bump
    out[h] = dict(volume=round(volume(KV, KF), 6), tiling=chk)
    print('B keyed TO h', h, out[h])
h = 0.5
KV, KF = keyed(h)
patchK = [(KV + t, KF) for t in bcc if np.linalg.norm(t) <= 2.5]
degK = corner_degrees(patchK)
degKV = sorted({degK[tuple(v)] for v in np.round(KV, 6)})
res['shapes']['keyed-TO'] = dict(
    name='keyed truncated octahedron (a DICTO design study shape; name to be given by DICTO)',
    scale='bcc lattice points 2Z³ ∪ 2Z³+(1,1,1); truncated octahedron edge %.6f; pyramid height h (shown h = 0.5)' % edgeTO,
    faces=len(KF), face_kinds={'squares': 6, 'triangles': len(KF) - 6}, vertices=len(KV), volume_TO=round(volTO, 6),
    by_height=out, cells_meeting_at_corners=degKV,
    four_round_one='yes: four pieces round one, each across a bump hexagon, a plain translate (its dent takes the bump)',
    four_meeting_at_a_point='at its 24 truncated-octahedron corners (see cells_meeting_at_corners; the 8 pyramid apexes are where 2 meet)')
json.dump({'vertices': KV.round(6).tolist(), 'faces': KF, 'h': h}, open(os.path.join(OUT, 'keyed-to.json'), 'w'))
json.dump(res, open(os.path.join(OUT, 'new-shapes.json'), 'w'), indent=1, ensure_ascii=False)
print('B corners', degKV)
