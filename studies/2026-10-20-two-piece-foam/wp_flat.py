# DICTO 2026-10-20: a curved lattice of two rounded pieces (DICTO), starting from the Weaire-Phelan foam (Weaire and Phelan 1993): the
# cells of the A15 arrangement (points at (0,0,0), (1/2,1/2,1/2) and (1/4,0,1/2), (3/4,0,1/2), (1/2,1/4,0), (1/2,3/4,0), (0,1/2,1/4),
# (0,1/2,3/4) in the unit cube): Voronoi cells, flat-faced. Two shapes: a dodecahedron (12 pentagons) and a tetrakaidecahedron (12
# pentagons + 2 hexagons). Measured: volumes, faces, the angles where three cells meet along each edge. Also its symmetry group (Pm-3n).
import itertools, json, os, numpy as np
from scipy.spatial import Voronoi, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = np.array([(0, 0, 0), (.5, .5, .5), (.25, 0, .5), (.75, 0, .5), (.5, .25, 0), (.5, .75, 0), (0, .5, .25), (0, .5, .75)])
pts = np.array([b + np.array(o) for o in itertools.product(range(-2, 3), repeat=3) for b in BASE])
vor = Voronoi(pts)
def cell(i):
    reg = vor.regions[vor.point_region[i]]; assert -1 not in reg; return vor.vertices[reg]
centre = lambda b: next(i for i, p in enumerate(pts) if np.allclose(p, b))
cells = {k: cell(centre(b)) - b for k, b in zip(['D', 'D2', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6'], BASE)}
def faces(P):
    h = ConvexHull(P); g = {}
    for s, e in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(e, 6)), set()).update(s)
    return g
info = {}
for k, P in cells.items():
    F = faces(P); info[k] = {'volume': round(ConvexHull(P).volume, 6), 'faces': sorted(len(v) for v in F.values())}
print({k: (v['volume'], {n: v['faces'].count(n) for n in set(v['faces'])}) for k, v in info.items()})
print('volumes sum to the cube:', round(sum(v['volume'] for v in info.values()), 6))
# dihedral angles of the dodecahedron and a tetrakaidecahedron at their edges
def dihedrals(P):
    h = ConvexHull(P); planes = {}
    for s, e in zip(h.simplices, h.equations): planes.setdefault(tuple(np.round(e, 6)), (set(), e[:3]))[0].update(s)
    pl = list(planes.values()); out = []
    for (A, na), (B, nb) in itertools.combinations(pl, 2):
        if len(A & B) >= 2: out.append(180 - np.degrees(np.arccos(np.clip(na @ nb, -1, 1))))
    return out
for k in ['D', 'T1']:
    d = dihedrals(cells[k]); print(f'{k}: {len(d)} edges, angles {min(d):.2f} .. {max(d):.2f}, mean {np.mean(d):.2f} deg (foam ideal 120)')
json.dump({k: cells[k].tolist() for k in cells}, open(os.path.join(HERE, 'wp-flat-cells.json'), 'w'))
# the symmetry group: affine maps x -> R x + t (R signed permutation, t in {0, 1/2}^3) mapping the A15 points to themselves (mod 1)
def key(p): return tuple(np.round(np.mod(p, 1), 6) % 1)
S = {key(b) for b in BASE}; G = []
for p in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3):
        R = np.zeros((3, 3)); [R.__setitem__((i, p[i]), s[i]) for i in range(3)]
        for t in itertools.product((0, .5), repeat=3):
            if {key(R @ b + np.array(t)) for b in BASE} == S: G.append((R, np.array(t)))
print('symmetry operations (mod translations):', len(G))
json.dump([[R.tolist(), t.tolist()] for R, t in G], open(os.path.join(HERE, 'wp-group.json'), 'w'))
