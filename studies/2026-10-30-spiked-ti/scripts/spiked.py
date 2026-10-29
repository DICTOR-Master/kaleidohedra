# Spiked TI (DICTO, 2026-10-30): a new golden cycle beginning with a spiked core. TI (TI, station 7 of DICTO's
# twelve-station golden cycle, #54) with its 32 face pyramids (study 2026-10-30-ti-pyramids) turned outwards: each pyramid
# reflected in its own face, tip at twice the face centre, as the Cleo star does to the icosahedron. Exact in Q(sqrt5) via sympy.
# Checks: volume = 2 TI; the hull of the spiked TI (faces, kinds); its place among the twelve stations (inside / outside,
# corners or tips on faces); similarity of the hull to every station up to golden scale. -> data/spiked.json
import json, itertools, math
import numpy as np, sympy as sp
from scipy.spatial import ConvexHull
r5 = sp.sqrt(5); phi = (1 + r5) / 2
raw = json.load(open('data/stations-exact.json'))
ST = {k: [[sp.Rational(a) + sp.Rational(b) * r5 for a, b in v] for v in V] for k, V in raw.items()}
NUM = {k: np.array([[float(x) for x in v] for v in V]) for k, V in ST.items()}
ORDER = ['I', 'D′', 'ID', 'OG', 'rTI', 'TI', 'H', 'jtI', 'RT', 'M', 'I·φ³']

def planes(P):
    h = ConvexHull(P); out = {}
    for eq in h.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = [i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8]
    return out
def face_kinds(P):
    c = {}
    for ids in planes(P).values(): c[len(ids)] = c.get(len(ids), 0) + 1
    return dict(sorted(c.items()))

TI = ST['TI']; P = NUM['TI']
tips = []
for ids in planes(P).values():
    c = [sum((TI[i][k] for i in ids), sp.Integer(0)) / len(ids) for k in range(3)]
    tips.append(([sp.nsimplify(sp.radsimp(2 * x)) for x in c], len(ids)))
T = np.array([[float(x) for x in t] for t, _ in tips])
out = {'TI faces': face_kinds(P), 'tips': len(tips)}
r = {n: sorted({round(float(sp.sqrt(sum(x * x for x in t))), 9) for t, m in tips if m == n}) for n in (5, 6)}
out['tip distances (pentagon, hexagon)'] = r
volTI = ConvexHull(P).volume
# spiked volume: TI + each pyramid again = 2 TI (each outward pyramid is the mirror of an inward one)
out['volume TI'] = volTI; out['volume spiked'] = 2 * volTI
# hull of the spiked TI: tips + TI corners
A = np.vstack([P, T]); hA = ConvexHull(A)
on_hull = set(hA.vertices)
out['hull corners: TI corners on hull'] = sum(1 for i in on_hull if i < len(P))
out['hull corners: tips on hull'] = sum(1 for i in on_hull if i >= len(P))
HP = A[sorted(on_hull)]
out['hull faces by corners'] = face_kinds(HP); out['hull volume / TI'] = ConvexHull(HP).volume / volTI
# radii of the hull's face planes, to name it
d = sorted({round(-eq[3], 7) for eq in ConvexHull(HP).equations}); out['hull face distances'] = d
# the hull's similarity to a station up to golden scale: compare sorted corner radii ratios and face kinds
def signature(Q):
    rr = np.linalg.norm(Q, axis=1); return (face_kinds(Q), sorted(set(np.round(rr / rr.max(), 6))))
sigH = signature(HP); sims = []
for k in ORDER:
    if signature(NUM[k]) == sigH:
        s = np.linalg.norm(NUM[k], axis=1).max() / np.linalg.norm(HP, axis=1).max(); sims.append((k, s, math.log(s) / math.log(float(phi))))
out['hull similar to stations (name, scale, log_phi scale)'] = sims
# nesting: is the spiked TI inside each station, and the station inside its hull? tips on station faces?
def inside(Q, R):   # all of Q inside hull R (tolerance)
    h = ConvexHull(R); return bool(np.all(Q @ h.equations[:, :3].T + h.equations[:, 3] <= 1e-9))
def touching(Q, R):
    h = ConvexHull(R); dd = Q @ h.equations[:, :3].T + h.equations[:, 3]
    return int(np.sum(np.any(np.abs(dd) < 1e-9, axis=1)))
nest = []
for k in ORDER:
    R = NUM[k]
    nest.append(dict(station=k, spiked_inside_station=inside(A, R), station_inside_spiked_hull=inside(R, HP),
                     tips_on_station_faces=touching(T, R), station_corners_on_hull_faces=touching(R, HP),
                     station_radius=float(np.linalg.norm(R, axis=1).max())))
out['nesting'] = nest
out['spiked hull radius'] = float(np.linalg.norm(HP, axis=1).max())
json.dump(out, open('data/spiked.json', 'w'), indent=1, ensure_ascii=False, default=str)
print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
