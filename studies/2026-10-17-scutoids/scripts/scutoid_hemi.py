# DICTO 2026-10-17: "we were cutting the hemi-RD before building the scutoids", "so they can be shorter and fatter". The hemi-RD is
# cut first; the whole core truncated icosahedron A sits inside it, raised to height h above the flat square base; the scutoid layer
# A -> B (strict swap: 12 pentagon cells 5 -> 6, 12 paired-hexagon cells 6 -> 5, each through a Y) grows in it with the base as a fixed
# wall; a closing layer B -> hemi-RD fills the rest (cage planes, the 8 upper RD planes, the base fixed). Measures: least chunky cell,
# the scutoids' own shape (height = layer thickness across the cell, width = across its outer face), core share = TI / hemi-RD (r³).
# Float search over h, the three growths and the hemi-RD looseness. -> data/scutoid-hemi.txt
import itertools, numpy as np, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/scutoid_rd.py').read().rsplit("\nR = []", 1)[0])
UP = np.array([n for n in RDN if n[2] >= 0], float)   # 4 sides (z = 0 normals) + 4 upper
BASE = np.array([[0, 0, -1.]])
def run(h, gP, gHd, gHo, tf):
    c = np.array([0, 0, -h]); dA_ = dA.copy()   # core frame (the cell builder starts from the core centre)
    dB_ = np.array([dA[i] * {'P': gP, 'Hd': gHd, 'Ho': gHo}[G[i]] for i in range(32)])
    NL = np.vstack([N, BASE]); GL = G + ['base']
    L = sweep_cells(NL, np.r_[dA_, h], np.r_[dB_, h], GL)
    sw = 0; per = {}; shape = []
    for (g, V), i in zip(L, range(32)):
        if V is None or len(V) < 4: return None
        inn = sum(1 for v in V if abs(N[i] @ v - dA_[i]) < 1e-7); out = sum(1 for v in V if abs(N[i] @ v - dB_[i]) < 1e-7)
        if (g == 'P' and inn == 5 and out == 6 and len(V) > inn + out) or (g == 'Ho' and inn == 6 and out == 5 and len(V) > inn + out):
            sw += 1; nu = N[i] / np.linalg.norm(N[i]); top = V[np.abs(V @ N[i] - dB_[i]) < 1e-7]
            shape.append(((dB_[i] - dA_[i]) / np.linalg.norm(N[i])) / np.ptp(top - np.outer(top @ nu, nu), axis=0).max())
        per[f'layer {g}'] = min(per.get(f'layer {g}', 1), chunk(V))
    if sw < 24: return None
    VB = corners(NL, np.r_[dB_, h]); r = max(((VB - c) @ UP.T).max(), 0) * tf
    HV = np.array([[s * r, 0, 0] for s in (1, -1)] + [[0, s * r, 0] for s in (1, -1)] + [[0, 0, r]] + [[a * r / 2, b * r / 2, r / 2] for a in (1, -1) for b in (1, -1)]) + c
    NC = np.vstack([N, UP, BASE]); GC = G + ['RD'] * 8 + ['base']
    d0 = np.r_[dB_, (VB @ UP.T).max(0), h]; d1 = np.r_[(HV @ N.T).max(0), r + UP @ c, h]
    mv = d1 - d0; ok = np.r_[np.ones(40, bool), False]
    if not (mv[ok] > 1e-9).all(): return None
    for g, V in sweep_cells(NC, d0, d1, GC):
        if V is not None and len(V) >= 4: per[f'close {g}'] = min(per.get(f'close {g}', 1), chunk(V))
    return dict(h=h, gP=gP, gHd=gHd, gHo=gHo, tf=tf, worst=min(per.values()), per={a: round(b, 3) for a, b in per.items()},
                core=ConvexHull(TI).volume / r ** 3, scut_h_over_w=(min(shape), max(shape)))
zA = TI[:, 2].max()
R = []
for hf in (1.02, 1.15, 1.3, 1.45, 1.6):
    for gP in np.linspace(1.05, 1.8, 6):
        for gHd in np.linspace(1.05, 2.0, 6):
            for gHo in np.linspace(1.15, 2.2, 6):
                for tf in (1.05, 1.15, 1.3):
                    try: b = run(zA * hf, gP, gHd, gHo, tf)
                    except Exception: b = None
                    if b: R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Hemi-RD cut first, whole core raised inside, scutoids grown against the flat base (float)', f'  bundles with all 24 scutoids: {len(R)}']
for lo, hi in ((0.2, 1), (0.12, 0.2), (0.06, 0.12), (0.0, 0.06)):
    band = [b for b in R if lo <= b['core'] < hi]
    if band:
        bb = band[0]; out.append(f"  core share {lo:.2f}-{hi:.2f}: least chunky {bb['worst']:.3f}; scutoid height/width {bb['scut_h_over_w'][0]:.2f}-{bb['scut_h_over_w'][1]:.2f} (h {bb['h']:.2f}, gP {bb['gP']:.2f}, gHd {bb['gHd']:.2f}, gHo {bb['gHo']:.2f}, ×{bb['tf']}); kinds {bb['per']}")
out.append('  for comparison: whole RD best 0.149 at core 0.20-0.30 (×2 r³ volume), 0.167 at 0.12-0.20; halved after 0.156')
print('\n'.join(out)); open('data/scutoid-hemi.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-hemi.json', 'w'))
