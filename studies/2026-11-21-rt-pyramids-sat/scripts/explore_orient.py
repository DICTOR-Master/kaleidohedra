# exploration: closure of the edge-to-edge moves of the old DFS on orientations (apex moved to origin)
import sys, os, numpy as np
sys.argv = [sys.argv[0], '1', '1', sys.argv[1] if len(sys.argv) > 1 else 'RT']
src = open(os.path.expanduser('~/k-research/studies/2026-11-04-rt-pyramids/scripts/rt_pyramids.py')).read().split('maxd = int(')[0]
exec(src)
def key(t):
    s = t - t[0]; return tuple(sorted(tuple(np.round(p, 6)) for p in s[1:]))
seen = {key(P0): P0}; frontier = [P0]; it = 0
while frontier and len(seen) < 3000:
    nf = []
    for t in frontier:
        for a, b, d in edges_of(t):
            for cs in sector_candidates(t, a, b, d):
                for c in cs:
                    k = key(c)
                    if k not in seen: seen[k] = c; nf.append(c)
    frontier = nf; it += 1; print('round', it, 'orientations', len(seen), flush=True)
# apex displacement module: collect apex positions of one-step neighbours of P0
ap = {tuple(np.round(c[0], 6)) for a, b, d in edges_of(P0) for cs in sector_candidates(P0, a, b, d) for c in cs}
print('distinct apexes one step from P0:', len(ap)); print(sorted(ap))
