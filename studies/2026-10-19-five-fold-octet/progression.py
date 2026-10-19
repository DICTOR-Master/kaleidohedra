# DICTO's five-fold octet (2026-10-19): grow outward from the Cleo star with the same pattern and different solids.
# Float checks only (exact proofs still to do). Frame: icosahedron of edge 1, 5-fold axes on its corners; every solid is built
# in this frame and tested against it (accuracy rule 1). Each stage = the tightest next solid round the last, and the pieces
# between them, with their volumes summed against the gap.
import itertools, json, os, numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__)); PHI = (1 + 5 ** .5) / 2
hv = lambda P: ConvexHull(np.asarray(P)).volume
out = {'mark': 'DICTO five-fold octet study, 2026-10-19 (float)', 'stages': []}
def log(k, v): print(f'{k}: {v}'); out[k] = v

I = np.array([s for a in [(0, 1, PHI), (1, PHI, 0), (PHI, 0, 1)] for s in itertools.product(*[(x, -x) if x else (0,) for x in a])], float) / 2
u5 = I / np.linalg.norm(I, axis=1)[:, None]
D = np.array([I[f].mean(0) for f in ConvexHull(I).simplices]); D *= PHI ** 2 / 3 ** .5 / np.linalg.norm(D[0])   # the Cleo star's D'
u3 = D / np.linalg.norm(D, axis=1)[:, None]
# Known case (rule 3): D' radius phi^2/sqrt3 is the Cleo star's hull in the app (theaetetus-data.js, view cleostar).
app = '/home/dicto/kaleidohedra/src/app/theaetetus-data.js'
if os.path.exists(app):
    s = open(app).read(); V = json.loads(s[s.index('{'):s.rindex('}') + 1])['theaetetus']['views']['cleostar']
    Dapp = np.array([p[1] for p in V if p[0] == 'dprime'][0]); assert abs(np.linalg.norm(Dapp[0]) - np.linalg.norm(D[0])) < 1e-5   # app data has 6 decimals
    assert abs(hv(Dapp) - hv(D)) < 1e-4; log('known_case', "D' matches the app's Cleo star hull (radius and volume)")

# Stage 2: D' -> the tightest icosidodecahedron round it.
E = [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(np.linalg.norm(I[i] - I[j]) - 1) < 1e-9]
ID = np.array([I[i] + I[j] for i, j in E]); ID *= np.linalg.norm(D[0]) / (ID[np.argsort(-(ID @ u3[0]))[:3]].mean(0) @ u3[0])
tri_c = [ID[np.argsort(-(ID @ u))[:3]].mean(0) for u in u3]
assert max(np.linalg.norm(c - d) for c, d in zip(tri_c, D)) < 1e-12           # every D' corner at an ID triangle centre
frusta = [hv(np.vstack([D[np.argsort(-(D @ u))[:5]], ID[np.argsort(-(ID @ u))[:5]]])) for u in u5]
gap2 = hv(ID) - hv(D)
out['stages'].append({'from': "D'", 'to': 'ID', 'pieces': {'five-sided twisted frustum (D pentagon, ID pentagon turned 36 deg, 10 triangles)': 12},
                      'piece_volume': frusta[0], 'sum': sum(frusta), 'gap': gap2, 'one_kind': float(np.ptp(frusta)) < 1e-12})
print('stage D->ID', out['stages'][-1])

# Stage 3: ID -> rhombic triacontahedron with its face planes through the ID corners.
r = np.linalg.norm(ID[0]); n = ID / r; t5 = r / np.max(n @ u5[0]); t3 = r / np.max(n @ u3[0]); RT = np.vstack([u5 * t5, u3 * t3])
P5 = [hv(np.vstack([ID[np.argsort(-(ID @ u))[:5]], u * t5])) for u in u5]; P3 = [hv(np.vstack([ID[np.argsort(-(ID @ u))[:3]], u * t3])) for u in u3]
e = min(np.linalg.norm(a - b) for a, b in itertools.combinations(ID, 2))
EE = [(i, j) for i, j in itertools.combinations(range(30), 2) if abs(np.linalg.norm(ID[i] - ID[j]) - e) < 1e-9]
TV = []
for i, j in EE:
    m = (ID[i] + ID[j]) / 2; a5 = u5[np.argmax(u5 @ m)] * t5; a3 = u3[np.argmax(u3 @ m)] * t3
    TV.append(abs(np.linalg.det(np.array([ID[j] - ID[i], a5 - ID[i], a3 - ID[i]]))) / 6)
gap3 = hv(RT) - hv(ID)
out['stages'].append({'from': 'ID', 'to': 'RT', 'pieces': {'five-sided pyramid': 12, 'three-sided pyramid': 20, 'valley tetrahedron (on each ID edge)': 60},
                      'sum': sum(P5) + sum(P3) + sum(TV), 'gap': gap3, 'tetra_one_kind': float(np.ptp(TV)) < 1e-12})
print('stage ID->RT', out['stages'][-1])

# The five-sided Vajra: Cleo star inward pyramid + frustum + outward pyramid along one 5-fold axis = one convex piece?
ax = u5[0]; df = D[np.argsort(-(D @ ax))[:5]]; ip = ID[np.argsort(-(ID @ ax))[:5]]
parts = [hv(np.vstack([I[0], df])), frusta[0], P5[0]]; whole = hv(np.vstack([I[0], df, ip, ax * t5]))
log('vajra5', {'parts': parts, 'sum': sum(parts), 'hull': whole, 'convex_union': abs(whole - sum(parts)) < 1e-9,
               'inner_tip_r': float(np.linalg.norm(I[0])), 'outer_tip_r': float(t5)})
log('vajra3_note', 'Cleo spike tip and the three-sided pyramid meet only at the D\' corner (a point), so the 3-fold column pinches')

# Pure hexagonal Cleos (DICTO): the tightest OG round the ID puts its regular hexagons in the ID triangle planes.
O = np.array(json.load(open(os.path.join(HERE, 'ocd-vertices.json'))))
R = np.linalg.norm(O, axis=1); far = O[np.abs(R - R.max()) < 1e-7] / R.max()
a = far[0]; b = far[np.argsort(np.linalg.norm(far - a, axis=1))[1]]; x = u5[0]; y = u5[np.argsort(np.linalg.norm(u5 - x, axis=1))[1]]
M = np.array([x, y, np.cross(x, y)]).T @ np.linalg.inv(np.array([a, b, np.cross(a, b)]).T); O = O @ M.T
assert np.allclose(np.sort((O[np.abs(R - R.max()) < 1e-7] / R.max()) @ u5.T, axis=1)[:, -1], 1)   # rule 1: same frame
pl = []
for q in ConvexHull(O).equations:
    if not any(np.allclose(q, w, atol=1e-7) for w in pl): pl.append(q)
pl = np.array(pl); nn = pl[:, :3]; dd = -pl[:, 3]; size = [int(np.sum(np.abs(O @ nn[k] - dd[k]) < 1e-7)) for k in range(len(pl))]
sc = np.max((ID @ nn.T) / dd); hexd = sc * dd[size.index(6)]
log('og_round_id', {'scale_vs_file': float(sc), 'scale_is_3phi_over_2': abs(sc - 3 * PHI / 2) < 1e-9, 'hexagon_plane': float(hexd),
                    'id_triangle_plane': float(np.linalg.norm(D[0])), 'coplanar': abs(hexd - np.linalg.norm(D[0])) < 1e-9,
                    'og_inside_rt': bool(np.max((O * sc) @ n.T) <= r + 1e-9)})
log('radii', {'I': float(np.linalg.norm(I[0])), "D'": float(np.linalg.norm(D[0])), 'ID': float(r), 'RT5': float(t5), 'RT3': float(t3),
              'ID_is_phi': abs(r - PHI) < 1e-12, 'RT5_is_2xI': abs(t5 - 2 * np.linalg.norm(I[0])) < 1e-12, 'RT3_is_sqrt3': abs(t3 - 3 ** .5) < 1e-12})
os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
json.dump(out, open(os.path.join(HERE, 'data', 'progression.json'), 'w'), indent=1, default=float)
