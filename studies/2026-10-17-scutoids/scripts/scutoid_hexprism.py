# DICTO 2026-10-17: "maybe the best target outer is a hexagonal prism". Prism axis along the diagonal (1,1,1): its 6 sides are the 6 RD
# directions perpendicular to it (±(1,-1,0), ±(0,1,-1), ±(1,0,-1)), its caps the diagonal-hexagon direction ±(1,1,1). It tiles space
# (hexagonal prism lattice). Width factor fw and height factor fh over the tightest prism around B; fh = 1 means the caps ARE B's two
# axial diagonal hexagons (shared, no cells there). One thick strict scutoid layer as in scutoid_sphericity.py. Score: least
# sphericity over all cells. Float. -> data/scutoid-hexprism.txt
import numpy as np, json
from scipy.spatial import ConvexHull
exec(open('scripts/scutoid_sphericity.py').read().rsplit("\nR = []", 1)[0])
SIDE = np.array([[1, -1, 0], [-1, 1, 0], [0, 1, -1], [0, -1, 1], [1, 0, -1], [-1, 0, 1]], float); CAP = np.array([[1, 1, 1], [-1, -1, -1]], float)
NP = np.vstack([N, SIDE, CAP]); GP = G + ['side'] * 6 + ['cap'] * 2
def close_prism(dB, per, fw, fh):
    VB = corners(N, dB); w = (VB @ SIDE.T).max() * fw; c = (VB @ CAP.T).max() * fh
    PV = []   # prism corners: hexagon in the plane ⊥ (1,1,1) at heights ±c (along unnormalised (1,1,1): n·x = ±c)
    for s in (1, -1):
        H = []
        for k in range(6):
            a = np.pi / 3 * k; e1 = np.array([1, -1, 0]) / np.sqrt(2); e2 = np.array([1, 1, -2]) / np.sqrt(6)
            H.append((np.cos(a) * e1 + np.sin(a) * e2) * (w / np.sqrt(2)) / np.cos(np.pi / 6))
        H = np.array(H)
        # rotate the hexagon so its edges (not corners) face the side normals
        rot = np.pi / 6; H = np.array([np.cos(rot) * h + np.sin(rot) * np.cross(np.ones(3) / np.sqrt(3), h) for h in H])
        PV += list(H + s * np.ones(3) * c / 3)
    PV = np.array(PV)
    if (PV @ SIDE.T).max() > w * 1.0001 or abs((PV @ SIDE.T).max() - w) > 1e-6 * w: return None   # corner construction check
    d0 = np.r_[dB, (VB @ SIDE.T).max(0), (VB @ CAP.T).max(0)]; d1 = np.r_[(PV @ N.T).max(0), np.full(6, w), np.full(2, c)]
    fixed = np.abs(d1 - d0) < 1e-9
    if (d1 < d0 - 1e-9).any(): return None
    per = dict(per)
    for g, V in sweep_cells(NP, d0, d1, GP, skip=list(np.where(fixed)[0])):
        if V is not None and len(V) >= 4: per['close ' + g] = min(per.get('close ' + g, 1), psi(V))
    vP = ConvexHull(PV).volume
    return dict(fw=fw, fh=fh, worst=min(per.values()), per={a: round(b, 3) for a, b in per.items()}, core=ConvexHull(TI).volume / vP, aspect=(2 * c / np.sqrt(3)) / (2 * w / np.sqrt(2)))
R = []
for gP, gHd, gHo in [(1.85, 1.95, 2.10), (2.0, 2.12, 2.28), (1.6, 1.7, 1.85), (2.3, 2.46, 2.64), (1.4, 1.45, 1.6)]:
    for g2 in np.linspace(0.9, 1.1, 3):
        try: L = strict_layer(gP * g2, gHd * g2, gHo * g2) if False else strict_layer(gP, gHd * g2, gHo)
        except Exception: L = None
        if not L: continue
        for fw in (1.05, 1.15, 1.3, 1.45, 1.6):
            for fh in (1.0, 1.1, 1.25, 1.45, 1.7):
                try: b = close_prism(*L, fw, fh)
                except Exception: b = None
                if b: b.update(gP=gP, gHd=gHd * g2, gHo=gHo); R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Hexagonal prism outer (axis along a diagonal), one thick scutoid layer; sphericity (cube 0.806, dodecahedron 0.910) (float)', f'  bundles: {len(R)}']
for b in R[:6]: out.append(f"    least ψ {b['worst']:.3f} (gP {b['gP']:.2f} gHd {b['gHd']:.2f} gHo {b['gHo']:.2f}; prism width ×{b['fw']}, height ×{b['fh']}, height/width {b['aspect']:.2f}, core share {b['core']:.3f}); {b['per']}")
sh = [b for b in R if b['fh'] == 1.0]
if sh: b = sh[0]; out.append(f"  caps shared with B's hexagons: best least ψ {b['worst']:.3f} (width ×{b['fw']}); {b['per']}")
out.append('  for comparison, rhombic dodecahedron outer (scutoid-sphericity.txt): best least ψ 0.578 (RD ×1.6)')
print('\n'.join(out)); open('data/scutoid-hexprism.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-hexprism.json', 'w'))
