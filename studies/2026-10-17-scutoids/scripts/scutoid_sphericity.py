# DICTO 2026-10-17: "short and fat… like a cube or dodecahedron… so I wouldn't end up with a bunch of twigs". Score every cell by
# sphericity ψ = π^(1/3)·(6V)^(2/3) / A (ball 1, dodecahedron 0.910, cube 0.806, regular tetrahedron 0.671; twigs and slabs near 0).
# Step 2 of the agreed plan: ONE thick strict scutoid layer A -> B (12 pentagon cells 5 -> 6, 12 paired-hexagon cells 6 -> 5, each through
# a Y), closed by a rhombic dodecahedron (fcc space-filler). Maximise the least spherical cell over the whole bundle. Float.
# -> data/scutoid-sphericity.txt / .json
import numpy as np, json
from scipy.spatial import ConvexHull
exec(open('scripts/scutoid_rd.py').read().rsplit("\nR = []", 1)[0])
def psi(V):
    h = ConvexHull(V); return np.pi ** (1 / 3) * (6 * h.volume) ** (2 / 3) / h.area
def strict_layer(gP, gHd, gHo):
    dB = np.array([dA[i] * {'P': gP, 'Hd': gHd, 'Ho': gHo}[G[i]] for i in range(32)])
    L = sweep_cells(N, dA, dB, G); sw = 0; per = {}
    for (g, V), i in zip(L, range(32)):
        if V is None or len(V) < 4: return None
        inn = sum(1 for v in V if abs(N[i] @ v - dA[i]) < 1e-7); out = sum(1 for v in V if abs(N[i] @ v - dB[i]) < 1e-7)
        if (g == 'P' and inn == 5 and out == 6 and len(V) > inn + out) or (g == 'Ho' and inn == 6 and out == 5 and len(V) > inn + out): sw += 1
        per['layer ' + g] = min(per.get('layer ' + g, 1), psi(V))
    return (dB, per) if sw == 24 else None
def close_psi(dB, per, tf):
    VB = corners(N, dB); r = (VB @ RDN.T).max() * tf
    RDV = np.array([[s * r, 0, 0] for s in (1, -1)] + [[0, s * r, 0] for s in (1, -1)] + [[0, 0, s * r] for s in (1, -1)] + [[a * r / 2, b * r / 2, c * r / 2] for a in (1, -1) for b in (1, -1) for c in (1, -1)])
    d0 = np.r_[dB, (VB @ RDN.T).max(0)]; d1 = np.r_[(RDV @ N.T).max(0), np.full(12, r)]
    if not (d1 > d0 + 1e-9).all(): return None
    per = dict(per)
    for g, V in sweep_cells(NR, d0, d1, GR):
        if V is not None and len(V) >= 4: per['close ' + g] = min(per.get('close ' + g, 1), psi(V))
    return dict(tf=tf, worst=min(per.values()), per={a: round(b, 3) for a, b in per.items()}, core=ConvexHull(TI).volume / (2 * r ** 3))
R = []
for gP in np.linspace(1.1, 2.6, 11):
    for gHd in np.linspace(1.1, 2.8, 11):
        for gHo in np.linspace(1.2, 3.0, 11):
            try: L = strict_layer(gP, gHd, gHo)
            except Exception: L = None
            if not L: continue
            for tf in (1.03, 1.12, 1.25, 1.45):
                try: b = close_psi(*L, tf)
                except Exception: b = None
                if b: b.update(gP=gP, gHd=gHd, gHo=gHo); R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Sphericity (ball 1, dodecahedron 0.910, cube 0.806, tetrahedron 0.671): one thick scutoid layer, closed by a rhombic dodecahedron (float)',
       f'  bundles with all 24 scutoids: {len(R)}', '  best (least spherical cell of the whole bundle, maximised):']
for b in R[:6]: out.append(f"    least ψ {b['worst']:.3f}  (gP {b['gP']:.2f}, gHd {b['gHd']:.2f}, gHo {b['gHo']:.2f}, RD ×{b['tf']}, core share {b['core']:.3f}); {b['per']}")
lay = max(R, key=lambda b: min(v for k, v in b['per'].items() if k.startswith('layer')))
out.append(f"  most spherical scutoid layer alone: least ψ {min(v for k, v in lay['per'].items() if k.startswith('layer')):.3f} (gP {lay['gP']:.2f}, gHd {lay['gHd']:.2f}, gHo {lay['gHo']:.2f}); whole bundle there {lay['worst']:.3f}; {lay['per']}")
print('\n'.join(out)); open('data/scutoid-sphericity.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-sphericity.json', 'w'))
