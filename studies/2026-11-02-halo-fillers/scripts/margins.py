# Margins (DICTO 2026-11-02): for each new halo, the edge that fails the single-halo edge test by the widest gap: the distance from
# 2 pi - a and from pi - a to the nearest sum of the halo's dihedral angles. Float error of the angles is below 1e-12 rad, so a gap
# far above 1e-7 rad is a proof that the edge test fails.   Usage: margins.py <out>
import json, sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import screen as S
H = S.load_halos(); out = {}
for k, h in H.items():
    A = S.classes(S.dihedrals(h['P'])); R = S.reach([a for a, n in A]); keys = np.array(sorted(R)); best = None
    for a, n in A:
        g = min(np.min(np.abs(keys - (S.TAU - a))), np.min(np.abs(keys - (math.pi - a))))
        if best is None or g > best[1]: best = (math.degrees(a), g)
    out[k] = dict(edge_deg=best[0], gap_rad=float(best[1]))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
g = sorted(v['gap_rad'] for v in out.values()); print('smallest of the widest gaps', g[:3], 'median', g[len(g) // 2])
