# DICTO 2026-10-17 asked about halving the truncated octahedron or squashing it. Reasoned answer: neither moves the axis conflict (B's
# paired-hexagon flip reaches 3φ·k·s along the axes; T's squares sit at 2t with t fixed by the diagonal hexagons: fit needs k < 1.079, the
# flip needs k > 1.127). A Th-symmetric lattice space-filler is the cube, the RD or the TO (Voronoi cells of the three cubic lattices);
# the RD reaches furthest along the axes (its 4-valent corners). Test: strict scutoid layer A -> B (12 pentagon cells 5 -> 6, 12
# paired-hexagon cells 6 -> 5, each through a Y), then a closing layer B -> RD over the 32 cage planes and the 12 RD planes; the RD is the
# smallest around B times a looseness tf. Score: least chunky cell; compactness: core share (TI / RD volume). Float.
import itertools, numpy as np, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/scutoid_squares.py').read().split("R = []")[0])
RDN = np.array([[a, b, 0] for a in (1, -1) for b in (1, -1)] + [[a, 0, b] for a in (1, -1) for b in (1, -1)] + [[0, a, b] for a in (1, -1) for b in (1, -1)], float)
NR = np.vstack([N, RDN]); GR = G + ['RD'] * 12
def layer(gP, gHd, gHo):
    dB = np.array([dA[i] * {'P': gP, 'Hd': gHd, 'Ho': gHo}[G[i]] for i in range(32)])
    L = sweep_cells(N, dA, dB, G); sw = 0; per = {}
    for (g, V), i in zip(L, range(32)):
        if V is None or len(V) < 4: return None
        inn = sum(1 for v in V if abs(N[i] @ v - dA[i]) < 1e-7); out = sum(1 for v in V if abs(N[i] @ v - dB[i]) < 1e-7)
        if (g == 'P' and inn == 5 and out == 6 and len(V) > inn + out) or (g == 'Ho' and inn == 6 and out == 5 and len(V) > inn + out): sw += 1
        per[f'layer {g}'] = min(per.get(f'layer {g}', 1), chunk(V))
    return (dB, per) if sw == 24 else None
def close(dB, per, tf):
    VB = corners(N, dB); r = (VB @ RDN.T).max() * tf
    RDV = np.array([[s * r, 0, 0] for s in (1, -1)] + [[0, s * r, 0] for s in (1, -1)] + [[0, 0, s * r] for s in (1, -1)] + [[a * r / 2, b * r / 2, c * r / 2] for a in (1, -1) for b in (1, -1) for c in (1, -1)])
    d0 = np.r_[dB, (VB @ RDN.T).max(0)]; d1 = np.r_[(RDV @ N.T).max(0), np.full(12, r)]
    if not (d1 > d0 + 1e-9).all(): return None
    per = dict(per)
    for g, V in sweep_cells(NR, d0, d1, GR):
        if V is None or len(V) < 4: continue
        per[f'close {g}'] = min(per.get(f'close {g}', 1), chunk(V))
    return dict(r=r, tf=tf, worst=min(per.values()), per={a: round(b, 3) for a, b in per.items()}, core=ConvexHull(TI).volume / (2 * r ** 3))
R = []
for gP in np.linspace(1.05, 2.2, 10):
    for gHd in np.linspace(1.05, 2.6, 10):
        for gHo in np.linspace(1.05, 2.6, 10):
            try: L = layer(gP, gHd, gHo)
            except Exception: L = None
            if not L: continue
            for tf in (1.02, 1.1, 1.2, 1.35):
                try: b = close(*L, tf)
                except Exception: b = None
                if b: b.update(gP=gP, gHd=gHd, gHo=gHo); R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Strict scutoid bundles closed by a rhombic dodecahedron (float)', f'  bundles: {len(R)}']
for lo, hi in ((0.30, 1), (0.2, 0.3), (0.12, 0.2), (0.0, 0.12)):
    band = [b for b in R if lo <= b['core'] < hi]
    if band: bb = band[0]; out.append(f"  core share {lo:.2f}-{hi:.2f}: worst cell {bb['worst']:.3f} (gP {bb['gP']:.3f}, gHd {bb['gHd']:.3f}, gHo {bb['gHo']:.3f}, RD ×{bb['tf']}); kinds {bb['per']}")
out.append('  for comparison, truncated octahedron (scutoid-shared-hex.txt): best worst cell 0.043 (core 0.00-0.12), 0.009 (core 0.12-0.20)')
print('\n'.join(out)); open('data/scutoid-rd.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-rd.json', 'w'))
