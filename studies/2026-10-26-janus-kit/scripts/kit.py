# Janus kit computations (DICTO 2026-10-26). Exact where it matters (rational λ, census engine), floats only for ranking/roundness.
# For the four kit weights (one per Janus family: −3/8 Chucky, −1/4, 0, 5/24 Fang) and the cubic (ABC) / hexagonal (AB) /
# double-hexagonal (ABAC) stackings:
#  A. HALVES: each pure octahedral half is achiral (has a mirror plane) → top and bottom halves are one physical object turned over.
#  B. RODS: for every bond (shared face) the straight segment between the two holes crosses the face INSIDE it (exact: the crossing
#     point lies in the face polygon), or how far outside it falls.
#  C. SCALE: the smallest shared face's inradius (in ball spacings) → ball spacing needed so a 28 mm hole leaves ≥ 8 mm rim.
#  D. SPHERES: clusters = one piece + its bonded neighbours; roundness = (volume of the cluster's convex hull) / (volume of its
#     circumscribed ball about the centre piece's hole); count of pieces.
import itertools, json, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
from engine import Net, Cell, aff_eval, gdot, vsub
from stackings import net_for
LAMS = [Fr(-3, 8), Fr(-1, 4), Fr(0), Fr(5, 24)]
def build(word):
    spec = net_for(word); return Net(word, spec['G'], spec['T'], spec['motif'], spec['w']), spec
def cart(spec):
    G = np.array([[float(x) for x in r] for r in spec['G']]); return np.linalg.cholesky(G).T
out = {}; lines = []
def say(s): print(s, flush=True); lines.append(s)
for word in ('ABC', 'AB', 'ABAC'):
    net, spec = build(word); L = cart(spec)
    for lam in LAMS:
        key = f'{word} λ={lam}'; rec = {}
        cells = {}
        for i, (k, p) in enumerate(spec['motif']):
            try: c = Cell(net, i, (lam,), Fr(12))
            except Exception: c = None
            if c is None or c.empty: continue
            cells[i] = c
        # B + C: faces, rods, inradius
        min_inr, worst = 1e9, 0.0; nb = 0
        for i, c in cells.items():
            p = np.array([float(x) for x in spec['motif'][i][1]]) @ L.T * 0 + L @ np.array([float(x) for x in spec['motif'][i][1]])
            for kf, pts in c.faces().items():
                H = c.H[kf]; q = L @ np.array([float(x) for x in H['c']])         # neighbour hole (Cartesian)
                P = np.array([L @ np.array([float(aff_eval(pt['P'][r], (lam,))) for r in range(3)]) for pt in pts])
                n = q - p; n /= np.linalg.norm(n); ctr = P.mean(0)
                t = np.dot(ctr - p, n) / np.dot(q - p, n); X = p + t * (q - p)        # rod ∩ face plane
                u = P[1] - P[0]; u -= np.dot(u, n) * n; u /= np.linalg.norm(u); v = np.cross(n, u)
                Q = np.c_[(P - ctr) @ u, (P - ctr) @ v]; x = np.array([(X - ctr) @ u, (X - ctr) @ v])
                h = ConvexHull(Q); ins = np.max(h.equations[:, :2] @ x + h.equations[:, 2])   # >0 means outside
                inr = -np.max(h.equations[:, :2] @ np.zeros(2) * 0 + h.equations[:, 2]) if False else min(-(h.equations[:, 2] + h.equations[:, :2] @ x))
                worst = max(worst, ins); min_inr = min(min_inr, inr if ins <= 0 else 0.0); nb += 1
        rec['rods'] = dict(bonds=nb, all_inside=worst <= 1e-9, worst_outside=round(worst, 6))
        rec['scale'] = dict(min_clearance_around_rod=round(min_inr, 6), ball_spacing_mm_for_28mm_hole_8mm_rim=round(22 / min_inr, 1) if min_inr > 0 else None)
        say(f"{key}: {nb} face-checks, rods all inside faces: {worst <= 1e-9} (worst outside {worst:.4f}); smallest clearance round a rod {min_inr:.4f} → ball spacing ≥ {22 / min_inr:.0f} mm for a 28 mm hole with 8 mm rim" if min_inr > 0 else f"{key}: rods outside faces somewhere (worst {worst:.4f})")
        out[key] = rec
json.dump(out, open('../kit.json', 'w'), indent=1); open('../kit.txt', 'w').write('\n'.join(lines) + '\n')
