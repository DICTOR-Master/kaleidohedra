# The Cleo-star pattern on the Kepler–Poinsot shells (float): valleys = inward pyramids (hull face -> core corner beneath) + valley
# tetrahedra (core edge + the two spike tips beside it); checked by volume and by random points (each in exactly one piece).
import itertools, numpy as np
from collections import Counter
from scipy.spatial import Delaunay
exec(open('kp.py').read().split('from scipy.sparse.csgraph')[0])
def pattern(core, spk, hull, name):
    tips = np.array([p[-1] for p in spk]); n, d = planes(hull); pyr = []
    for k in range(len(d)):
        F = hull[np.abs(hull @ n[k] - d[k]) < 1e-9]; c = core[np.argmax(core @ n[k])]; pyr.append(np.vstack([F, [c]]))
    e = min(np.linalg.norm(a - b) for a, b in itertools.combinations(core, 2)); tets = []
    for i, j in itertools.combinations(range(len(core)), 2):
        if abs(np.linalg.norm(core[i] - core[j]) - e) > 1e-9: continue
        two = [s[-1] for s in spk if sum(np.min(np.linalg.norm(s[:-1] - core[x], axis=1)) < 1e-9 for x in (i, j)) == 2]
        if len(two) == 2: tets.append(np.array([core[i], core[j], *two]))
    pieces = pyr + tets; vol = hv(hull) - hv(core) - sum(hv(p) for p in spk)
    tot = sum(hv(p) for p in pieces)
    P = gap_points(hull, spk, core, n=600000, seed=3)
    cnt = sum((Delaunay(p).find_simplex(P) >= 0).astype(int) for p in pieces)
    print(f'{name}: {len(pyr)} inward pyramids ({hv(pyr[0]):.5f} each) + {len(tets)} valley tetrahedra ({hv(tets[0]):.5f} each) = {tot:.5f}; valley {vol:.5f}; '
          f'sample points per piece count {dict(Counter(cnt))}')
pattern(I, GSD, D1, 'great stellated shell (I -> D1)')
pattern(D1, SSD, I2, 'small stellated shell (D1 -> I2)')
