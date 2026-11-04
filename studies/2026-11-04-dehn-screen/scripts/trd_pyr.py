# TRD centre pyramids: Dehn of the rhombic (= RD's R12) and the trapezoid pyramid (TRD study lead, 5 Nov)
import sys, numpy as np; sys.argv = sys.argv[:1] + ['x', '10']
from halfcell import TRD, RD
from dehn import dehn, hull_faces
for nm, C in (('RD', RD), ('TRD', TRD)):
    P, F = hull_faces(C); seen = set()
    for f in F:
        Q = P[f]; e = [np.linalg.norm(Q[i] - Q[(i+1) % 4]) for i in range(4)]
        kind = 'rhomb' if max(e) - min(e) < 1e-9 else 'trapez'
        if kind in seen: continue
        seen.add(kind); V, G = hull_faces(np.vstack([Q, [0, 0, 0]]))
        r = dehn(V, G, f'{nm} {kind} pyramid'); print(nm, kind, 'edges', np.round(e, 4), 'zero', r['dehn_zero'], r['coefficient_sums_over_maxL'])
