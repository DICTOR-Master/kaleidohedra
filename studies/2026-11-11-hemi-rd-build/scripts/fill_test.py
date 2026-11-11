"""Does DICTO's closed build (the chamfered cube, his 14 Hemi RDs + 6 cube pyramids) fill space with cube pyramids? (DICTO 11 Nov)
Claim to test: chamfered cubes centred at the lattice 2*FCC = {(a,b,c) integers, all even, a+b+c = 0 mod 4} (contact on hexagons by
(2,2,0)), plus unit cubes centred at the lattice points + (2,0,0) (each a cube of 6 cube pyramids, between six squares), fill space with
no gaps and no overlaps. Checked by covering counts at random points (every point covered exactly once) and by volume (16 = 15 + 1).
The chamfered cube is taken from DICTO's build itself (convex hull of his 14 pieces, centred)."""
import json, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
exec(open(sys.argv[2]).read().split("A = np.vstack(P)")[0].split("hv = vol(LV, LF)")[0])   # reuse the build's pieces
A = np.vstack(P); H = ConvexHull(A); c0 = A.mean(axis=0); EQ = H.equations.copy(); EQ[:, 3] += EQ[:, :3] @ c0   # centred hull
print('hull centre', np.round(c0, 6), 'volume', round(H.volume, 6))
def in_cc(x):  return np.all(EQ[:, :3] @ x + EQ[:, 3] <= 1e-9)
def in_cc_strict(x): return np.all(EQ[:, :3] @ x + EQ[:, 3] < -1e-9)
L = [np.array(v) for v in itertools.product(range(-6, 7, 2), repeat=3) if sum(v) % 4 == 0]
rng = np.random.default_rng(7); bad = 0; N = 20000; counts = {}
for _ in range(N):
    x = rng.random(3) * 4 - 2                                     # a box larger than one lattice cell
    k = sum(in_cc_strict(x - t) for t in L) + sum(np.all(np.abs(x - t - np.array([2, 0, 0])) < 0.5 - 1e-9) for t in L)
    counts[k] = counts.get(k, 0) + 1
print('covering count of random points:', counts, '(all 1 = a tiling; 0 only on boundaries)')
print('volume per lattice point: cell det', abs(np.linalg.det(np.array([[2,2,0],[2,0,2],[0,2,2]]))), '= chamfered cube', round(H.volume, 6), '+ unit cube 1')
ok = set(counts) == {1}
print('FINAL ok' if ok else 'FINAL FAIL')
