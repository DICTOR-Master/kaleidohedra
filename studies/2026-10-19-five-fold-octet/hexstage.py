# Stage 3 split through the OG (DICTO's pure hexagonal Cleos, 2026-10-19): ID -> OG -> RT. Float checks: volumes summed against
# each gap, and 400,000 random points tested so that every point of RT minus OG lies in exactly one piece.
import json
from collections import Counter
from scipy.spatial import Delaunay
from frame import *
RT = np.vstack([u5 * t5, u3 * t3]); RO = np.linalg.norm(O, axis=1)
isID = np.linalg.norm(O[:, None] - ID[None], axis=2).min(1) < 1e-9
X = O[(~isID) & (RO < 1.65)]; A = O[RO > 1.65]
res = {'mark': 'DICTO five-fold octet study, hexagonal stage, 2026-10-19 (float)',
       'og_corners_shared_with_id': int(isID.sum()), 'og_other_corners_on_radius_phi': len(X), 'og_apexes': len(A)}
nO, dO = planes(O); sz = [int(np.sum(np.abs(O @ nO[k] - dO[k]) < 1e-7)) for k in range(len(dO))]
hexv = O[np.abs(O @ nO[sz.index(6)] - dO[sz.index(6)]) < 1e-7]
res['og_hexagon_side'] = float(min(np.linalg.norm(p - q) for p, q in itertools.combinations(hexv, 2)))
# ID -> OG: one piece per 5-fold axis (ID pentagon, the 5 nearest extra corners, the OG apex)
low = [hull for hull in [np.vstack([ID[np.argsort(-(ID @ u))[:5]], X[np.argsort(-(X @ u))[:5]], A[np.argmax(A @ u)]]) for u in u5]]
v = [hv(P) for P in low]
res['id_to_og'] = {'pieces': 12, 'sum': sum(v), 'gap': hv(O) - hv(ID), 'one_kind': float(np.ptp(v)) < 1e-12,
                   'note': 'pentagon on the ID, 5 kites + 5 small triangles of the OG hexagons on top; neighbours touch only along edges'}
# OG -> RT: hexagonal Cleos, five-fold caps (dimpled: the OG apex pokes in), 120 tetrahedra
pcs = []
for k in [k for k in range(len(dO)) if sz[k] == 6]: pcs.append(('hexagonal Cleo', np.vstack([O[np.abs(O @ nO[k] - dO[k]) < 1e-7], nO[k] * t3]), None))
for u, L in zip(u5, low): pcs.append(('five-fold cap', np.vstack([ID[np.argsort(-(ID @ u))[:5]], X[np.argsort(-(X @ u))[:5]], u * t5]), L))
for x in X:
    a5 = u5[np.argmax(u5 @ x)] * t5; a3 = u3[np.argmax(u3 @ x)] * t3
    for c in ID[np.argsort(np.linalg.norm(ID - x, axis=1))[:2]]: pcs.append(('tetrahedron', np.array([c, x, a5, a3]), None))
vol = lambda P, L: hv(P) - (hv(L) if L is not None else 0)
kinds = {}
for name, P, L in pcs: kinds.setdefault(name, []).append(vol(P, L))
res['og_to_rt'] = {'pieces': {k: len(w) for k, w in kinds.items()}, 'volumes': {k: w[0] for k, w in kinds.items()},
                   'one_volume_each': {k: float(np.ptp(w)) < 1e-12 for k, w in kinds.items()},
                   'sum': sum(sum(w) for w in kinds.values()), 'gap': hv(RT) - hv(O),
                   'hexagonal_cleo_height': float(t3 - dO[sz.index(6)])}
tO, tR = Delaunay(O), Delaunay(RT); T = [(Delaunay(P), Delaunay(L) if L is not None else None) for _, P, L in pcs]
pts = np.random.default_rng(0).uniform(-1.95, 1.95, (400000, 3)); pts = pts[(tR.find_simplex(pts) >= 0) & (tO.find_simplex(pts) < 0)]
cnt = np.zeros(len(pts), int)
for t, l in T: cnt += (t.find_simplex(pts) >= 0) & ((l.find_simplex(pts) < 0) if l is not None else True)
res['sample_cover'] = {str(k): int(v) for k, v in Counter(cnt).items()}
# five-fold column: ID->OG piece fills the cap's dimple exactly
res['cap_plus_low_convex'] = abs(vol(pcs[20][1], pcs[20][2]) + hv(low[0]) - hv(pcs[20][1])) < 1e-12
# three-fold column: the D' corner is the hexagon's centre, so the Cleo spike meets the hexagonal Cleo at one point
res['d_corner_at_hexagon_centre'] = float(np.min(np.linalg.norm(D - hexv.mean(0), axis=1))) < 1e-12
print(json.dumps(res, indent=1, default=float))
json.dump(res, open('data/hexstage.json', 'w'), indent=1, default=float)
