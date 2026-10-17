# Squares in the layer, entering late (after the flip), so the scutoids keep their Y: the 6 square planes start their sweep outside the
# truncated icosahedron (d0 = (1 + q) × its axis support), arriving only after the paired-hexagon flip. Float search over s, p, k, q;
# a bundle counts only if the layer still has its 24 scutoids (inner and outer face sides differ, with a free corner).
import itertools, numpy as np, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/scutoid_squares.py').read().split("R = []")[0])
def bundle_late(s, p, k, q):
    t = s * max(dA[i] for i in range(32) if G[i] == 'Hd') / 3
    TO = np.array([[sg[0] * a[0], sg[1] * a[1], sg[2] * a[2]] for a in itertools.permutations([0, t, 2 * t]) for sg in itertools.product((1, -1), repeat=3)])
    supT = (TO @ N.T).max(0)
    d0 = dA38.copy(); d0[32:] = d0[32:] * (1 + q)
    dB = np.r_[[3 * t if g == 'Hd' else 0 for g in G], np.full(6, 2 * t)].astype(float)
    for i, g in enumerate(G):
        if g == 'P': dB[i] = dA[i] + p * (supT[i] - dA[i])
        if g == 'Ho': dB[i] = min(dA[i] * k * s, supT[i] - 1e-6)
    if not (dB > d0 + 1e-9).all(): return None
    L = sweep_cells(NN, d0, dB, GG)
    d1c = dB.copy()
    for i, g in enumerate(G):
        if g in ('P', 'Ho'): d1c[i] = supT[i]
    C = sweep_cells(NN, dB, d1c, GG, skip=[i for i, g in enumerate(GG) if g in ('Hd', 'Sq')])
    per, scut = {}, 0; swapP = swapHo = 0
    gi = [i for i in range(38) if (dB - d0)[i] > 1e-12]
    for (g, V), i in zip(L, gi):
        if V is None or len(V) < 4: continue
        inn = sum(1 for v in V if abs(NN[i] @ v - d0[i]) < 1e-7); out = sum(1 for v in V if abs(NN[i] @ v - dB[i]) < 1e-7)
        free = len(V) - inn - out
        # strict (DICTO's swap): a pentagon cell becomes a hexagon, a paired-hexagon cell a pentagon, each through a Y (a free corner)
        if g == 'P' and inn == 5 and out == 6 and free > 0: swapP += 1
        if g == 'Ho' and inn == 6 and out == 5 and free > 0: swapHo += 1
        per[f'layer {g}'] = min(per.get(f'layer {g}', 1), chunk(V))
    for g, V in C:
        if V is not None and len(V) >= 4: per[f'close {g}'] = min(per.get(f'close {g}', 1), chunk(V))
    return dict(s=s, p=p, k=k, q=q, scutoids=swapP + swapHo, worst=min(per.values()), per={a: round(b, 3) for a, b in per.items()}, core=ConvexHull(TI).volume / (32 * t ** 3))
R = []
for s_ in (1.25, 1.35, 1.5, 1.65, 1.8, 2.0, 2.2):
    for p_ in (0.15, 0.25, 0.35, 0.5, 0.65, 0.8):
        for k_ in (flip * 1.01, 1.17, 1.24, 1.32, 1.45):
            for q_ in (0.02, 0.06, 0.12, 0.2, 0.3):
                try: b = bundle_late(s_, p_, k_, q_)
                except Exception: b = None
                if b and b['scutoids'] >= 24: R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Late squares, STRICT: bundles whose 12 pentagon cells become hexagons and 12 paired-hexagon cells pentagons, each through a Y (float)', f'  bundles found: {len(R)}']
for lo, hi in ((0.30, 1), (0.2, 0.3), (0.12, 0.2), (0.0, 0.12)):
    band = [b for b in R if lo <= b['core'] < hi]
    if band: bb = band[0]; out.append(f"  core share {lo:.2f}-{hi:.2f}: worst cell {bb['worst']:.3f} (s {bb['s']}, p {bb['p']}, k {bb['k']:.3f}, q {bb['q']}), scutoids {bb['scutoids']}; kinds {bb['per']}")
print('\n'.join(out)); open('data/scutoid-late-squares-strict.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-late-squares-strict.json', 'w'))
