# check: without the swapped-end placements (reflection across the perpendicular bisector of the shared edge), the edge moves of the
# 4 Nov search never leave the 30 orientations of class O; with them, the orientation count grows (52, 780, ...).
import sys, os, numpy as np
sys.argv = [sys.argv[0], '1', '1', 'RT']
src = open(os.path.expanduser('~/k-research/studies/2026-11-04-rt-pyramids/scripts/rt_pyramids.py')).read().split('maxd = int(')[0]
exec(src)
def key(t):
    s = t - t[0]; return tuple(sorted(tuple(np.round(p, 6)) for p in s[1:]))
_rp = refl_perp
for label, allow_swap in (('without swapped ends', False), ('with swapped ends', True)):
    globals()['refl_perp'] = (_rp if allow_swap else (lambda Pp, X, Y: Pp))
    seen = {key(P0): P0}; fr = [P0]
    for rnd in range(1, 3):
        nf = []
        for t in fr:
            for a, b, d in edges_of(t):
                for cs in sector_candidates(t, a, b, d):
                    for c in cs:
                        k = key(c)
                        if k not in seen: seen[k] = c; nf.append(c)
        fr = nf; print(label, 'round', rnd, 'orientations', len(seen), flush=True)
