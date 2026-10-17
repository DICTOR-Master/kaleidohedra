# DICTO 2026-10-17: "yes try the two thin layers in the whole RD". The swap is 6 edge flips (one per axis), one orbit of the bundle's Th
# symmetry, so the flips happen together; two thin layers therefore flip and flip back (DICTO's earlier "alternate top and bottom"):
#   layer 1 A -> M: pentagon cells 5 -> 6, paired-hexagon cells 6 -> 5 (24 scutoids);
#   layer 2 M -> B: pentagon cells 6 -> 5, paired-hexagon cells 5 -> 6 (24 scutoids, the swap back);
#   closing layer B -> RD.
# Planes: A = TI; M = a1·(dP, dHd, k1·dHo); B = a1·a2·(dP, dHd, k2·dHo), k1 past the flip (5-φ)/3, k2 back before it. Score: least
# chunky cell; scutoid height/width (thickness across the cell / width of its outer face), per layer; core share TI / RD. Float.
import itertools, numpy as np, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/scutoid_rd.py').read().rsplit("\nR = []", 1)[0])
def strict(d0, d1, want):   # want: {'P': (inner, outer), 'Ho': (inner, outer)}
    L = sweep_cells(N, d0, d1, G); sw = 0; per = {}; hw = []
    for (g, V), i in zip(L, range(32)):
        if V is None or len(V) < 4: return None
        inn = sum(1 for v in V if abs(N[i] @ v - d0[i]) < 1e-7); out = sum(1 for v in V if abs(N[i] @ v - d1[i]) < 1e-7)
        if g in want and (inn, out) == want[g] and len(V) > inn + out:
            sw += 1; nu = N[i] / np.linalg.norm(N[i]); top = V[np.abs(V @ N[i] - d1[i]) < 1e-7]
            hw.append(((d1[i] - d0[i]) / np.linalg.norm(N[i])) / np.ptp(top - np.outer(top @ nu, nu), axis=0).max())
        per[g] = min(per.get(g, 1), chunk(V))
    return (per, (min(hw), max(hw))) if sw == 24 else None
def planes(a, k): return np.array([dA[i] * (a * k if G[i] == 'Ho' else a) for i in range(32)])
R = []
for a1 in np.linspace(1.04, 1.4, 7):
    for k1 in (flip * 1.01, 1.17, 1.24, 1.32, 1.45):
        dM = planes(a1, k1)
        try: L1 = strict(dA, dM, {'P': (5, 6), 'Ho': (6, 5)})
        except Exception: L1 = None
        if not L1: continue
        for a2 in np.linspace(1.04, 1.5, 8):
            for k2 in (0.95, 1.0, 1.05, 1.1):
                dB = planes(a1 * a2, k2)
                if not (dB > dM + 1e-9).all(): continue
                try: L2 = strict(dM, dB, {'P': (6, 5), 'Ho': (5, 6)})
                except Exception: L2 = None
                if not L2: continue
                for tf in (1.05, 1.15, 1.3):
                    try: b = close(dB, {f'layer1 {g}': v for g, v in L1[0].items()} | {f'layer2 {g}': v for g, v in L2[0].items()}, tf)
                    except Exception: b = None
                    if b: b.update(a1=a1, k1=k1, a2=a2, k2=k2, hw1=L1[1], hw2=L2[1]); R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Two thin scutoid layers (flip, then flip back) in the whole rhombic dodecahedron (float)', f'  bundles with 24 + 24 scutoids: {len(R)}']
for lo, hi in ((0.2, 1), (0.12, 0.2), (0.06, 0.12), (0.0, 0.06)):
    band = [b for b in R if lo <= b['core'] < hi]
    if band:
        bb = band[0]; out.append(f"  core share {lo:.2f}-{hi:.2f}: least chunky {bb['worst']:.3f}; scutoid height/width layer 1 {bb['hw1'][0]:.2f}-{bb['hw1'][1]:.2f}, layer 2 {bb['hw2'][0]:.2f}-{bb['hw2'][1]:.2f} (a1 {bb['a1']:.3f}, k1 {bb['k1']:.3f}, a2 {bb['a2']:.3f}, k2 {bb['k2']}, RD ×{bb['tf']}); kinds {bb['per']}")
out.append('  for comparison, one layer in the whole RD (scutoid-rd.txt): least chunky 0.149 at core 0.20-0.30, 0.167 at 0.12-0.20')
print('\n'.join(out)); open('data/scutoid-two-layers.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-two-layers.json', 'w'))
