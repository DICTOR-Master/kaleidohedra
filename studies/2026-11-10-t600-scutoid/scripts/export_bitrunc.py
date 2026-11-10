"""Data for the 3D page of the bitruncated 600-cell scutoid build: the 3600 corners (4D), the 720 cells (corner lists, kind), two slicing
directions (cell-first: swaps in symmetric batches; generic: one swap at a time) with their exact event lists: at each corner height, which
pairs of cells stop touching and which start (swaps), and which cells enter / leave. Reuses t600_scutoid.py's construction."""
import sys, json, numpy as np
sys.argv = ['t600_scutoid.py', 'stages.py', 'bitruncated']
src = open('t600_scutoid.py').read().split('results = {}')[0]
exec(src)
out = {'X': np.round(X, 6).tolist(), 'cells': [[k, sorted(int(p) for p in S)] for k, S in cells], 'dirs': {}}
for name in ('cell-first', 'generic'):
    d = DIRS[name]; d = d / np.linalg.norm(d); H = X @ d; hs = np.unique(np.round(H, 9)); ev = []
    prev = tiling(H, (hs[0] + hs[1]) / 2)
    for k in range(1, len(hs) - 1):
        cur = tiling(H, (hs[k] + hs[k + 1]) / 2)
        lost = sorted(e for e in prev[1] - cur[1] if e[0] in cur[0] and e[1] in cur[0]); gained = sorted(e for e in cur[1] - prev[1] if e[0] in prev[0] and e[1] in prev[0])
        if lost or gained or cur[0] != prev[0]:
            ev.append({'h': round(float(hs[k]), 7), 'lost': [list(map(int, e)) for e in lost], 'gained': [list(map(int, e)) for e in gained],
                       'born': sorted(int(c) for c in cur[0] - prev[0]), 'died': sorted(int(c) for c in prev[0] - cur[0])})
        prev = cur
    nsw = sum(1 for e in ev if len(e['lost']) == len(e['gained']) and e['lost'])
    out['dirs'][name] = {'d': np.round(d, 9).tolist(), 'hmin': float(hs[0]), 'hmax': float(hs[-1]), 'events': ev}
    print(f'{name}: {len(ev)} events, {sum(len(e["lost"]) for e in ev)} pairs let go, {sum(len(e["gained"]) for e in ev)} pairs meet', flush=True)
json.dump(out, open('bitrunc_page.json', 'w'), separators=(',', ':'))
import os; print('size', os.path.getsize('bitrunc_page.json')); print('FINAL ok')
