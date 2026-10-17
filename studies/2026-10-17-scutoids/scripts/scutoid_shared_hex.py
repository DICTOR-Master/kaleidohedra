# Strict scutoid bundles with B's 8 diagonal hexagons shared with T (no slab cells): the three groups grow separately in the scutoid layer,
# B = (gP·dP, gHd·dHd, gHo·dHo); T is fixed by the shared hexagons (t = B's Hd distance / 3) and must hold B along the axes; the closing
# layer B -> T moves only the pentagon, paired-hexagon and square planes. A bundle counts only with the true swap (12 pentagon cells 5 -> 6,
# 12 paired-hexagon cells 6 -> 5, each through a Y). Score: least chunky cell; compactness: core share. Float.
import itertools, numpy as np, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/scutoid_squares.py').read().split("R = []")[0])
def strict_bundle(gP, gHd, gHo):
    dB = np.array([dA[i] * {'P': gP, 'Hd': gHd, 'Ho': gHo}[G[i]] for i in range(32)])
    if not (dB > dA).all(): return None
    VB = corners(N, dB); t = max(dB[i] for i in range(32) if G[i] == 'Hd') / 3; hx = (VB @ SQ.T).max()
    if hx >= 2 * t - 1e-9: return None
    L = sweep_cells(N, dA, dB, G); gi = list(range(32)); sw = 0; per = {}
    for (g, V), i in zip(L, gi):
        if V is None or len(V) < 4: return None
        inn = sum(1 for v in V if abs(N[i] @ v - dA[i]) < 1e-7); out = sum(1 for v in V if abs(N[i] @ v - dB[i]) < 1e-7); free = len(V) - inn - out
        if (g == 'P' and inn == 5 and out == 6 and free) or (g == 'Ho' and inn == 6 and out == 5 and free): sw += 1
        per[f'layer {g}'] = min(per.get(f'layer {g}', 1), chunk(V))
    if sw < 24: return None
    TO = np.array([[sg[0] * a[0], sg[1] * a[1], sg[2] * a[2]] for a in itertools.permutations([0, t, 2 * t]) for sg in itertools.product((1, -1), repeat=3)])
    NN2 = np.vstack([N, SQ]); d0 = np.r_[dB, (VB @ SQ.T).max(0)]; d1 = np.r_[(TO @ N.T).max(0), np.full(6, 2 * t)]
    hd = np.array([g == 'Hd' for g in G] + [False] * 6); d1[hd] = d0[hd]
    if not (d1[~hd] > d0[~hd] + 1e-9).all(): return None
    C = sweep_cells(NN2, d0, d1, G + ['Sq'] * 6, skip=[i for i in range(38) if hd[i]])
    for g, V in C:
        if V is not None and len(V) >= 4: per[f'close {g}'] = min(per.get(f'close {g}', 1), chunk(V))
    return dict(gP=gP, gHd=gHd, gHo=gHo, t=t, worst=min(per.values()), per={a: round(b, 3) for a, b in per.items()}, core=ConvexHull(TI).volume / (32 * t ** 3))
R = []
for gP in np.linspace(1.05, 2.2, 12):
    for gHd in np.linspace(1.05, 2.6, 14):
        for gHo in np.linspace(1.05, 2.6, 14):
            try: b = strict_bundle(gP, gHd, gHo)
            except Exception: b = None
            if b: R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Strict scutoid bundles, diagonal hexagons shared with T (float)', f'  bundles with the true swap and no slab cells: {len(R)}']
for lo, hi in ((0.30, 1), (0.2, 0.3), (0.12, 0.2), (0.0, 0.12)):
    band = [b for b in R if lo <= b['core'] < hi]
    if band: bb = band[0]; out.append(f"  core share {lo:.2f}-{hi:.2f}: worst cell {bb['worst']:.3f} (gP {bb['gP']:.3f}, gHd {bb['gHd']:.3f}, gHo {bb['gHo']:.3f}); kinds {bb['per']}")
print('\n'.join(out)); open('data/scutoid-shared-hex.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-shared-hex.json', 'w'))
