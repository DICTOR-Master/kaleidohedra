#!/usr/bin/env python3
"""PILOT (question c): Goldberg 1974 (JCTA 17, p. 378): are all space-filling pentahedra known? Closable part: pyramids over a square.
Square base [-1,1]^2 at z = 0, apex (x, y, h); by symmetry 0 <= y <= x. Dehn invariant (Dehn 1901) by #100's numerical screen
(2026-11-04-dehn-screen/scripts/dehn.py); tilers have Dehn zero (Debrunner 1980), so Dehn != 0 rules a pyramid out.
Controls: apex (0,0,1) = the cube's centre pyramid (zero; Duval 2022, arXiv:2207.01486, Thm 1: the only Dehn-zero right square pyramid);
apex (1,1,2) = one third of the cube [-1,1]^2 x [0,2] (zero, it tiles); right pyramids (0,0,h), h != 1, must be nonzero (Duval).
Grid: x, y in {0, 1/4, ..., 1}, y <= x; h in {1/4, 1/2, 3/4, 1, 3/2, 2, 3}. Prints PROGRESS and FINAL."""
import sys, json, itertools, time
import numpy as np
from fractions import Fraction as Fr
t0 = time.time()
DEHN_DIR = sys.argv[1]; OUT = sys.argv[2]
sys.path.insert(0, DEHN_DIR); sys.argv = [sys.argv[0], '', '10', '200']
import dehn as DEHN
B = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]
def pyr(x, y, h):
    V = np.array(B + [(x, y, h)], float)
    F = [[0, 3, 2, 1], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]
    return DEHN.dehn(V, F, f'apex({x},{y},{h})')
Q = [Fr(k, 4) for k in range(5)]; H = [Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1), Fr(3, 2), Fr(2), Fr(3)]
grid = [(x, y, h) for x in Q for y in Q if y <= x for h in H] + [(Fr(1), Fr(1), Fr(2))]
res = []
for n, (x, y, h) in enumerate(grid):
    r = pyr(float(x), float(y), float(h)); r['apex'] = [str(x), str(y), str(h)]; res.append(r)
    if r['dehn_zero']: print('ZERO', r['apex'], r['rational_pi_angles_deg'], flush=True)
    if n % 10 == 0: print(f'PROGRESS {n/len(grid):.3f} pyramid {n}/{len(grid)}', flush=True)
z = {tuple(r['apex']): r['dehn_zero'] for r in res}
c1 = z[('0', '0', '1')] is True; c2 = z[('1', '1', '2')] is True
c3 = all(z[('0', '0', str(h))] is False for h in H if h != 1)
json.dump({'grid_size': len(grid), 'zero': [r['apex'] for r in res if r['dehn_zero']], 'all': res,
           'controls': {'cube centre pyramid zero': c1, 'cube third zero': c2, 'right pyramids h!=1 nonzero (Duval)': c3},
           'seconds': round(time.time() - t0, 1)}, open(OUT, 'w'), indent=1)
print('ZERO SET', [r['apex'] for r in res if r['dehn_zero']])
print('CONTROLS', c1, c2, c3, f'{time.time()-t0:.0f}s')
print('FINAL ok' if (c1 and c2 and c3) else 'FINAL FAIL: a control failed')
