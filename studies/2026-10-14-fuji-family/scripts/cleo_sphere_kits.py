# Polyhedraverse pieces and kits for the CLEO sphere (DICTO, 2026-10-14). Writes src/krp-core/src/polyhedra/cleo-sphere.js:
#   PENTA_CLEO ('Penta-cleo', DICTO's name): one fifth of a pentagonal pocket, a right-angled triangular pyramid with one golden face;
#   CLEO_SPHERE_POCKET: the whole pocket, a tall pentagonal pyramid;
#   kits 'cleoSphere' (20 Cleo + 12 pockets) and 'cleoSphere.allCleo' (20 Cleo + 60 Penta-cleo), from the centre out.
# The sphere is built at the size where its CLEOs are the existing Cleo piece (KIT13_ICOSA13_CLEO), which is reused.
# Checks: every placement congruent to its piece; the kit's volumes add up to the icosidodecahedron. DICTO · dictospheres.com
import itertools, json, math, os, re
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); K = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
phi = (1 + 5 ** .5) / 2
raw = json.loads(re.search(r'const RAW = (\{.*?\});\n', open(os.path.join(K, 'src/krp-core/src/polyhedra/kits13.js')).read(), re.S).group(1))
CLEO = np.array(raw['KIT13_ICOSA13_CLEO']['vertices'], float); CLEO -= CLEO.mean(0)
side = max(np.linalg.norm(a - b) for a, b in itertools.combinations(CLEO, 2))          # Cleo's long (side) edge = the sphere's radius
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
E = [(a, b) for a, b in itertools.combinations(range(12), 2) if abs(np.linalg.norm(ico[a] - ico[b]) - 2) < 1e-9]
V = np.array([(ico[a] + ico[b]) / 2 for a, b in E]); V *= side / np.linalg.norm(V[0])
H = ConvexHull(V); FACES = []
for e in np.unique(np.round(H.equations, 9), axis=0):
    on = np.where(np.abs(V @ e[:3] + e[3]) < 1e-7)[0]; c = V[on].mean(0); a = V[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
    FACES.append([int(i) for i in on[np.argsort(np.arctan2((V[on] - c) @ b, (V[on] - c) @ a))]])
O = np.zeros(3)
def hullfaces(P):
    h = ConvexHull(P); out = []
    for e in np.unique(np.round(h.equations, 9), axis=0):
        on = np.where(np.abs(P @ e[:3] + e[3]) < 1e-7)[0]; c = P[on].mean(0); a = P[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        out.append([int(i) for i in on[np.argsort(np.arctan2((P[on] - c) @ b, (P[on] - c) @ a))]])
    return out
def match(S, P):
    """Rotation R and shift t with P = S @ R.T + t (some vertex order), or None."""
    cS, cP = S.mean(0), P.mean(0); S0, P0 = S - cS, P - cP
    for perm in itertools.permutations(range(len(P))):
        Q = P0[list(perm)]; U, _, Wt = np.linalg.svd(Q.T @ S0); R = U @ np.diag([1, 1, np.sign(np.linalg.det(U @ Wt))]) @ Wt
        if np.abs(S0 @ R.T - Q).max() < 1e-7: return R, cP - cS @ R.T
    return None
def quat(R):
    tr = np.trace(R); m = max(range(4), key=lambda i: [tr, R[0, 0], R[1, 1], R[2, 2]][i])
    if m == 0: w = math.sqrt(1 + tr) / 2; x, y, z = (R[2, 1] - R[1, 2]) / (4 * w), (R[0, 2] - R[2, 0]) / (4 * w), (R[1, 0] - R[0, 1]) / (4 * w)
    elif m == 1: x = math.sqrt(1 + 2 * R[0, 0] - tr) / 2; w, y, z = (R[2, 1] - R[1, 2]) / (4 * x), (R[0, 1] + R[1, 0]) / (4 * x), (R[0, 2] + R[2, 0]) / (4 * x)
    elif m == 2: y = math.sqrt(1 + 2 * R[1, 1] - tr) / 2; w, x, z = (R[0, 2] - R[2, 0]) / (4 * y), (R[0, 1] + R[1, 0]) / (4 * y), (R[1, 2] + R[2, 1]) / (4 * y)
    else: z = math.sqrt(1 + 2 * R[2, 2] - tr) / 2; w, x, y = (R[1, 0] - R[0, 1]) / (4 * z), (R[0, 2] + R[2, 0]) / (4 * z), (R[1, 2] + R[2, 1]) / (4 * z)
    q = np.array([x, y, z, w]); return (q / np.linalg.norm(q)).round(12).tolist()
tris = [f for f in FACES if len(f) == 3]; pens = [f for f in FACES if len(f) == 5]
# canonical pieces (centred): the first pocket and the first fifth of it
P0 = np.vstack([V[pens[0]], O]); POCKET = P0 - P0.mean(0)
f = pens[0]; pc = V[f].mean(0); Q0 = np.array([O, pc, V[f[0]], V[f[1]]]); PENTA = Q0 - Q0.mean(0)
pieces = {'PENTA_CLEO': ('Penta-cleo', PENTA), 'CLEO_SPHERE_POCKET': ('Pentagonal pocket (CLEO sphere)', POCKET)}
def place(shape, S, P):
    m = match(S, P); assert m, shape
    return dict(shape=shape, position=[round(float(x), 12) for x in m[1]], quaternion=quat(m[0]))
cleos = [place('KIT13_ICOSA13_CLEO', CLEO, np.vstack([V[f], O])) for f in tris]
pockets = [place('CLEO_SPHERE_POCKET', POCKET, np.vstack([V[f], O])) for f in pens]
fifths = []
for f in pens:
    c = V[f].mean(0)
    for i in range(5): fifths.append(place('PENTA_CLEO', PENTA, np.array([O, c, V[f[i]], V[f[(i + 1) % 5]]])))
vol = lambda S: ConvexHull(S).volume
v_cleo, v_pocket, v_penta = vol(CLEO), vol(POCKET), vol(PENTA)
checks = dict(scale_radius=side, icosidodecahedron=H.volume, kit_A=20 * v_cleo + 12 * v_pocket, kit_B=20 * v_cleo + 60 * v_penta,
              penta_is_fifth=abs(5 * v_penta - v_pocket) < 1e-12)
print(checks)
assert abs(checks['kit_A'] - H.volume) < 1e-7 and abs(checks['kit_B'] - H.volume) < 1e-7 and checks['penta_is_fifth']
RAW = {k: dict(name=n, vertices=S.round(12).tolist(), faces=hullfaces(S)) for k, (n, S) in pieces.items()}
KITS = {'cleoSphere': dict(label='CLEO sphere · 20 Cleo + 12 pentagonal pockets', group='cleo', entries=cleos[:1] + pockets + cleos[1:]),
        'cleoSphere.allCleo': dict(label='CLEO sphere · 20 Cleo + 60 Penta-cleo', group='cleo', entries=cleos + fifths)}
js = ('// Generated by studies/2026-10-14-fuji-family/scripts/cleo_sphere_kits.py (DICTO 2026-10-14). Do not edit.\n'
      '// The CLEO sphere: 20 Cleo pointing inwards + 12 pentagonal pockets (or 60 Penta-cleo, DICTO\'s name) fill an icosidodecahedron.\n'
      "import { specOf } from './stellaJewel.js';\n"
      f'const RAW = {json.dumps(RAW, separators=(",", ":"))};\n'
      'export const CLEO_SPHERE_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, specOf(id, p.name, p.vertices, p.faces, false, 1)]));\n'
      'export const CLEO_SPHERE_ADDITION_IDS = Object.keys(CLEO_SPHERE_ADDITIONS);\n'
      f'export const CLEO_SPHERE_KITS = {json.dumps(KITS, separators=(",", ":"))};\n')
open(os.path.join(K, 'src/krp-core/src/polyhedra/cleo-sphere.js'), 'w').write(js)
json.dump(checks, open(os.path.join(HERE, '..', 'cleo-sphere-kits-checks.json'), 'w'), indent=1); print(checks)
