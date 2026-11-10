"""Is the 601 / 601 balance of the bitruncated 600-cell's swaps direction-independent? (DICTO 10 Nov "yes test 601 in other directions").
Eight random generic directions: births, deaths, swaps by kind (R = truncated icosahedron, W = truncated tetrahedron)."""
import sys, numpy as np
from collections import Counter
sys.argv = ['t600_scutoid.py', 'stages.py', 'bitruncated']
exec(open('t600_scutoid.py').read().split('results = {}')[0])
lab = lambda e: '-'.join(sorted('W' if cells[c][0] == 'tt' else 'R' for c in e))
rng = np.random.default_rng(2026); ok = True
print('START 8 random directions', flush=True)
import os
ONLY = os.environ.get('ONLY')
for t in range(8):
    d = rng.normal(size=4); d /= np.linalg.norm(d)
    if ONLY and str(t + 1) != ONLY: continue
    H = X @ d; hs = np.unique(np.round(H, 9))
    assert len(hs) == len(X), 'not generic'
    C = Counter(); prev = tiling(H, (hs[0] + hs[1]) / 2)
    for k in range(1, len(hs) - 1):
        cur = tiling(H, (hs[k] + hs[k + 1]) / 2)
        lost = [e for e in prev[1] - cur[1] if e[0] in cur[0] and e[1] in cur[0]]; gained = [e for e in cur[1] - prev[1] if e[0] in prev[0] and e[1] in prev[0]]
        C['births'] += len(cur[0] - prev[0]); C['deaths'] += len(prev[0] - cur[0])
        if lost or gained: C[f'{lab(lost[0])} -> {lab(gained[0])}'] += 1
        prev = cur
    print(f'direction {t + 1}: ' + ', '.join(f'{k}: {v}' for k, v in sorted(C.items())), flush=True)
    ok &= C['W-W -> R-R'] == C['R-R -> W-W']
print('FINAL ok' if ok else 'FINAL FAIL: unbalanced in some direction')
