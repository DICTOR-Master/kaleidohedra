# DICTO 2026-10-17: "half a rhombic dodecahedron". The RD bundle cut by the square plane z = 0 (a mirror of the bundle's Th symmetry):
# two mirror-image half bundles, each in a hemi-RD (a space-filler). Cells on the mirror are split into mirror halves; the rest are kept.
# Compares the least chunky cell, whole vs half, for the best RD bundles of scutoid-rd.json. Float. -> data/scutoid-rd-half.txt
import json, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/scutoid_rd.py').read().rsplit("\nR = []", 1)[0])
def cells_of(gP, gHd, gHo, tf):
    dB, _ = layer(gP, gHd, gHo); VB = corners(N, dB); r = (VB @ RDN.T).max() * tf
    RDV = np.array([[s * r, 0, 0] for s in (1, -1)] + [[0, s * r, 0] for s in (1, -1)] + [[0, 0, s * r] for s in (1, -1)] + [[a * r / 2, b * r / 2, c * r / 2] for a in (1, -1) for b in (1, -1) for c in (1, -1)])
    L = sweep_cells(N, dA, dB, G)
    C = sweep_cells(NR, np.r_[dB, (VB @ RDN.T).max(0)], np.r_[(RDV @ N.T).max(0), np.full(12, r)], GR)
    return [('layer ' + g, V) for g, V in L if V is not None] + [('close ' + g, V) for g, V in C if V is not None and len(V) >= 4]
def half(V):
    if V[:, 2].min() >= -1e-9: return V, False
    if V[:, 2].max() <= 1e-9: return None, False
    eq = ConvexHull(V).equations; hs = np.vstack([eq, [0, 0, -1, 0]])
    x0 = V.mean(0); x0[2] = max(V[:, 2].max() * 0.3, 1e-4) if V[:, 2].max() > 0 else 1e-4
    W = HalfspaceIntersection(hs, x0).intersections; return np.unique(np.round(W, 9), axis=0), True
out = ['DICTO · dictospheres.com', 'Half rhombic dodecahedron: the RD scutoid bundle cut on its square mirror plane z = 0 (float)']
best = sorted(json.load(open('data/scutoid-rd.json')), key=lambda b: -b['core'] * min(b['worst'], 0.2))[:5]
for b in best:
    cs = cells_of(b['gP'], b['gHd'], b['gHo'], b['tf']); whole = min(chunk(V) for _, V in cs); per = {}; nsplit = 0
    for g, V in cs:
        H, sp = half(V)
        if H is None: continue
        nsplit += sp; per[g + (' (halved)' if sp else '')] = min(per.get(g + (' (halved)' if sp else ''), 1), chunk(H))
    out.append(f"  gP {b['gP']:.3f} gHd {b['gHd']:.3f} gHo {b['gHo']:.3f} RD ×{b['tf']}: core {b['core']:.3f}; least chunky whole {whole:.3f} -> half {min(per.values()):.3f}; cells split {nsplit}")
    out.append('     ' + ', '.join(f'{k} {v:.3f}' for k, v in sorted(per.items())))
print('\n'.join(out)); open('data/scutoid-rd-half.txt', 'w').write('\n'.join(out) + '\n')
