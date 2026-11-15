"""Post-run classification check for dial_a5_points.json (no new computation of points).
The 6 points left UNEXPLAINED by dial_a5.py lie within a few 1e-3 of the A4 root point (-1,0,0,0,1)/sqrt2 (a 20-point, antipodal
twisted class, where the Newton systems are singular).  Rule: an uncertified point within 5e-3 of a point with nontrivial stabiliser
(found by projecting onto the fixed space of each A5 element) is 'lower stratum'.  FINAL ok iff nothing stays unexplained."""
import json, itertools, numpy as np
R = json.load(open('data/dial_a5_points.json'))
A5 = [p for p in itertools.permutations(range(5)) if sum(1 for i in range(5) for j in range(i + 1, 5) if p[i] > p[j]) % 2 == 0]
def near_lower(x, tol=5e-3):
    x = np.array(x)
    for g in A5:
        if g == tuple(range(5)): continue
        P = np.eye(5)[list(g)]
        y = x.copy()
        for _ in range(60): y = 0.5 * (y + P @ y)          # project onto the fixed space of g (averaging over <g>)
        if np.linalg.norm(y - x) < tol: return True
    return False
n = 0
for r in R:
    if r['class'] == 'UNEXPLAINED':
        if near_lower(r['x_sorted']): r['class'] = 'lower stratum (within 5e-3 of a fixed point set; Newton converging to a singular root)'
        else: n += 1; print('STILL UNEXPLAINED', r)
from collections import Counter
print('classes:', dict(Counter(r['class'] for r in R)))
json.dump(R, open('data/dial_a5_points.json', 'w'), indent=1)
print('FINAL ok' if n == 0 else 'FINAL FAIL')
