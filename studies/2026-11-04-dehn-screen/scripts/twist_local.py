"""Halves as a standing option (DICTO 4 Nov): in the fcc tiling by RDs (each RD = two half-cells across its 3-fold axis z), twist the upper half of
(a) ONE cell, (b) every cell of one layer, by 60° about that cell's own axis. Count overlaps with neighbours (separating axes) and holes (random points)."""
import math, itertools, numpy as np
from scipy.spatial import ConvexHull, Delaunay
import sys; sys.path.insert(0, 'scripts/_lib'); import methods as M
exec(open('scripts/halfcell.py').read().split('print("RD"')[0])
s3 = math.sqrt(3); H = math.sqrt(2/3)
T = half(RD, True); B = half(RD, False)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
POS = {0: (0, 0), 1: (1/3, 1/3), 2: (2/3, 2/3)}   # ABC layers, lattice coords
def ball(i, j, L): u, v = POS[L % 3]; return np.array([i + u + (j + v)/2, (j + v)*s3/2, L*H])
cells = [(i, j, L) for i in range(-3, 4) for j in range(-3, 4) for L in range(-2, 3)]
def pieces(twist):
    out = []
    for i, j, L in cells:
        c = ball(i, j, L); tw = twist(i, j, L)
        out.append((T @ (rz(math.pi/3).T if tw else np.eye(3)) + c, (i, j, L, 'top')))
        out.append((B + c, (i, j, L, 'bottom')))
    return out
def check(name, twist):
    P = pieces(twist); cen = [p.mean(0) for p, _ in P]
    near = [k for k, (p, tag) in enumerate(P) if np.linalg.norm(cen[k]) < 2.2]
    ov = sum(1 for a, b in itertools.combinations(range(len(P)), 2) if (a in near or b in near) and np.linalg.norm(cen[a] - cen[b]) < 1.6 and M.overlap(P[a][0], P[b][0]))
    X = np.random.default_rng(0).uniform(-1, 1, (6000, 3)); cnt = np.zeros(len(X), int)
    for p, _ in P: cnt += Delaunay(p).find_simplex(X) >= 0
    print(f'{name}: overlapping pairs {ov}, sample points covered 0x/1x/2x: {[int((cnt == k).sum()) for k in (0, 1, 2)]}')
check('no twist (fcc, calibration)', lambda i, j, L: False)
check('ONE cell twisted', lambda i, j, L: (i, j, L) == (0, 0, 0))
check('one whole LAYER twisted (L = 0)', lambda i, j, L: L == 0)
