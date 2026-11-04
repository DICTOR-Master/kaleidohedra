"""Fair test (DICTO 4 Nov, halves as a standing option): every ball's cell = top half turned 0° or 60° to face its actual upper neighbours, and bottom
half likewise for the lower ones, in a mixed stacking word; check the cells fill space (no overlaps, every sample point covered once)."""
import math, itertools, numpy as np
from scipy.spatial import Delaunay
import sys; sys.path.insert(0, 'scripts/_lib'); import methods as M
exec(open('scripts/halfcell.py').read().split('print("RD"')[0])
s3 = math.sqrt(3); H = math.sqrt(2/3); T = half(RD, True); B = half(RD, False)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
OFF = {'A': (0, 0), 'B': (1/3, 1/3), 'C': (2/3, 2/3)}
def run(word, name):
    n = len(word); P = []
    for L in range(-2, 3):
        me, up, dn = word[L % n], word[(L + 1) % n], word[(L - 1) % n]
        d_up = np.subtract(OFF[up], OFF[me]) % 1; d_dn = np.subtract(OFF[dn], OFF[me]) % 1
        tt = np.eye(3) if np.allclose(d_up, [1/3, 1/3]) else rz(math.pi/3).T    # T was built for the layer above at +1/3
        bb = np.eye(3) if np.allclose(d_dn, [2/3, 2/3]) else rz(math.pi/3).T    # B for the layer below at -1/3
        for i, j in itertools.product(range(-3, 4), repeat=2):
            u, v = OFF[me]; c = np.array([i + u + (j + v)/2, (j + v)*s3/2, L*H]); P += [T @ tt + c, B @ bb + c]
    cen = [p.mean(0) for p in P]; near = [k for k in range(len(P)) if np.linalg.norm(cen[k]) < 2.2]
    ov = sum(1 for a, b in itertools.combinations(range(len(P)), 2) if (a in near or b in near) and np.linalg.norm(cen[a] - cen[b]) < 1.6 and M.overlap(P[a], P[b]))
    X = np.random.default_rng(0).uniform(-1, 1, (6000, 3)); cnt = np.zeros(len(X), int)
    for p in P: cnt += Delaunay(p).find_simplex(X) >= 0
    print(f'{name} ({word}): overlapping pairs {ov}, covered 0x/1x/2x {[int((cnt == k).sum()) for k in (0, 1, 2)]}', flush=True)
run('ABC', 'fcc, all c (calibration)')
run('AB', 'hcp, all h')
run('ABCB', 'mixed c h c h')
run('ABCACB', 'mixed')
run('ABACBCAC', 'Fibonacci approximant (chcchchc)')
