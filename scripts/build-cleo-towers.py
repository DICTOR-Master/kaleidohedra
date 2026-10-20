# Builds src/krp-core/src/polyhedra/cleo-towers.js (DICTO 2026-10-20): Polyhedraverse pieces and kits for two of DICTO's centre cores,
# beside the CLEO sphere (cleo-sphere.js):
#   Cleo Towers: round the CLEO sphere, shells of the tallest towers in 1, 1, 2, 3, 5 beats of the Universal PiTet rule
#     T(S) = {x : v.x <= v.v for every corner v of S}; each shell cut into towers, one over each face of its inner solid (exact study:
#     kaleidohedra research branch, studies/2026-10-20-cleo-towers);
#   the OG core of 80 spires: the DICTO Ogdoecontahedron as 20 DICTO Hex Aktis + 60 DICTO Deltoid Aktis (DICTO's names), every apex at
#     the centre (studies/2026-10-20-og-spires).
# Frame and size: the CLEO sphere kit's (its icosidodecahedron has circumradius 1, cleoSphere entries reused); the OG is scaled to
# circumradius 1 too. Float here; every piece is placed by an exact symmetry of its solid and checked congruent; volumes checked.
#   the polar Cleo Towers: reciprocated about the GTI's circumsphere (beat k -> 5 - k): an RT core 1/c^2 of 30 rhombic rays, then shells of
#     5, 3, 2, 1, 1 beats (studies/2026-10-20-cleo-towers/polar_exact.py);
#   the DICTO OTT core of 38 rays: 8 Cleo-Icos (the octahedral rays are exactly Cleo-Icos), 24 triangle rays, 6 rhombic rays
#     (studies/2026-10-20-ott-rays).
# Usage: python3 scripts/build-cleo-towers.py <step1-ocd-exact.json (the OG, exact)> <cut8-exact.json (the OTT, exact)>
import sys, os, re, json, itertools, math
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
PHI = (1 + 5 ** .5) / 2
cs = open(os.path.join(ROOT, 'src/krp-core/src/polyhedra/cleo-sphere.js')).read()
KITS_CS = json.loads(re.search(r'export const CLEO_SPHERE_KITS = (\{.*?\});\n', cs, re.S).group(1))
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * PHI), (s[0], s[1] * PHI, 0), (s[1] * PHI, 0, s[0])]], float)
E = [(a, b) for a, b in itertools.combinations(range(12), 2) if abs(np.linalg.norm(ico[a] - ico[b]) - 2) < 1e-9]
ID = np.array([(ico[a] + ico[b]) / 2 for a, b in E]); ID /= np.linalg.norm(ID[0])          # the CLEO sphere's icosidodecahedron, radius 1
def faces_of(P):
    h = ConvexHull(P); out, seen = [], set()
    for e in h.equations:                                         # one face per plane (hull triangles of a face share it; merge by corners)
        on = np.where(np.abs(P @ e[:3] + e[3]) < 1e-7)[0]
        if frozenset(on.tolist()) in seen: continue
        seen.add(frozenset(on.tolist())); c = P[on].mean(0); a = P[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        out.append((e, [int(i) for i in on[np.argsort(np.arctan2((P[on] - c) @ b, (P[on] - c) @ a))]]))
    return out
def corners(H, inside):
    X = HalfspaceIntersection(np.array(H, float), inside).intersections; out = []
    for x in X:                                                   # merge near-duplicates (several planes through one corner)
        if not any(np.abs(x - y).max() < 1e-7 for y in out): out.append(x)
    return np.array(out)
def T(P): return corners(np.c_[P, -(P * P).sum(1)], np.zeros(3))
# the 60 rotations of the frame (generated, then checked to fix the icosidodecahedron)
def rot(axis, ang):
    a = np.array(axis, float) / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K
G = [np.eye(3)]; gens = [rot((0, 1, PHI), 2 * math.pi / 5), np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float), np.diag([-1.0, -1, 1])]
while True:
    new = [g @ h for g in G for h in gens]; added = False
    for m in new:
        if not any(np.allclose(m, g, atol=1e-9) for g in G): G.append(m); added = True
    if not added: break
key = lambda P: frozenset(tuple(np.round(p, 7)) for p in P)
assert len(G) == 60 and all(key(ID @ g.T) == key(ID) for g in G), len(G)
# boundaries: 12 beats of T, the later turns as exact scaled copies (one turn = x 10/phi^4)
S = [ID]
for _ in range(4): S.append(T(S[-1]))
c = 10 / PHI ** 4; assert key(S[4]) == key(ID * c)
for k in range(5, 13): S.append(S[k - 4] * c)
beat = lambda j: S[j % 4] * c ** (j // 4)
beats = [1, 1, 2, 3, 5]; edges = [0]
for b in beats: edges.append(edges[-1] + b)
def towers(inner, outer):
    Hout = [e for e, _ in faces_of(outer)]
    for e, f in faces_of(inner):
        F = inner[f]; H = list(Hout) + [np.r_[-e[:3], -e[3]]]
        for a, b in zip(F, np.roll(F, -1, 0)):
            m = np.cross(a, b)
            if m @ F.mean(0) > 0: m = -m                        # wall through the centre and the edge; the face's cone on its inner side
            H.append(np.r_[m, 0.0])
        yield len(f), F, corners(H, F.mean(0) + e[:3] * 1e-3)
pieces, entries_by_kit = {}, {}
vol = lambda P: ConvexHull(P).volume
def piece_faces(P):
    return [f for _, f in faces_of(P)]
SIDES = {3: 'TRI', 4: 'RHOMB', 5: 'PENT', 6: 'HEX'}
SIDES_NAME = {3: 'a triangle', 4: 'a rhombus', 5: 'a pentagon', 6: 'a hexagon'}
def quat(R):
    tr = np.trace(R); m = max(range(4), key=lambda i: [tr, R[0, 0], R[1, 1], R[2, 2]][i])
    if m == 0: w = math.sqrt(1 + tr) / 2; x, y, z = (R[2, 1] - R[1, 2]) / (4 * w), (R[0, 2] - R[2, 0]) / (4 * w), (R[1, 0] - R[0, 1]) / (4 * w)
    elif m == 1: x = math.sqrt(1 + 2 * R[0, 0] - tr) / 2; w, y, z = (R[2, 1] - R[1, 2]) / (4 * x), (R[0, 1] + R[1, 0]) / (4 * x), (R[0, 2] + R[2, 0]) / (4 * x)
    elif m == 2: y = math.sqrt(1 + 2 * R[1, 1] - tr) / 2; w, x, z = (R[0, 2] - R[2, 0]) / (4 * y), (R[0, 1] + R[1, 0]) / (4 * y), (R[1, 2] + R[2, 1]) / (4 * y)
    else: z = math.sqrt(1 + 2 * R[2, 2] - tr) / 2; w, x, y = (R[1, 0] - R[0, 1]) / (4 * z), (R[0, 2] + R[2, 0]) / (4 * z), (R[1, 2] + R[2, 1]) / (4 * z)
    q = np.array([x, y, z, w]); return (q / np.linalg.norm(q)).round(12).tolist()
tower_entries = []
for k, (a, b) in enumerate(zip(edges, edges[1:])):
    canon = {}
    for n, F, P in towers(S[a], S[b]):
        pid = f'CLEO_TOWER_{k + 1}_{SIDES[n]}'
        if pid not in canon:
            m0 = P.mean(0); canon[pid] = (P, m0)
            pieces[pid] = (f'Cleo Tower, shell {k + 1} ({beats[k]} beat{"s" if beats[k] > 1 else ""}), on {SIDES_NAME[n]}', P - m0)
        P0, m0 = canon[pid]
        same = lambda A, B: len(A) == len(B) and all(np.abs(B - x).sum(1).min() < 1e-6 for x in A)
        g = next((g for g in G if same(P0 @ g.T, P)), None); assert g is not None, (pid, 'not congruent')
        tower_entries.append((k, dict(shape=pid, position=[round(float(x), 12) for x in g @ m0], quaternion=quat(g))))
# the polar Cleo Towers (beats -7 | -2 | 1 | 3 | 4 | 5); the core: the RT 1/c^2 as 30 rhombic rays
pbounds = [-7, -2, 1, 3, 4, 5]; pbeats = [5, 3, 2, 1, 1]; polar_entries = []
for k, (a, b) in enumerate(zip(pbounds, pbounds[1:])):
    canon = {}
    for n, F, P in towers(beat(a), beat(b)):
        pid = f'POLAR_TOWER_{k + 1}_{SIDES[n]}'
        if pid not in canon:
            m0 = P.mean(0); canon[pid] = (P, m0)
            pieces[pid] = (f'Polar Cleo Tower, shell {k + 1} ({pbeats[k]} beat{"s" if pbeats[k] > 1 else ""}), on {SIDES_NAME[n]}', P - m0)
        P0, m0 = canon[pid]
        same = lambda A, B: len(A) == len(B) and all(np.abs(B - x).sum(1).min() < 1e-6 for x in A)
        g = next((g for g in G if same(P0 @ g.T, P)), None); assert g is not None, (pid, 'not congruent')
        polar_entries.append(dict(shape=pid, position=[round(float(x), 12) for x in g @ m0], quaternion=quat(g)))
pcore = beat(-7); core_rays = []
for e, f in faces_of(pcore):
    P = np.vstack([pcore[f], np.zeros(3)])
    if 'POLAR_CORE_RAY' not in pieces: pieces['POLAR_CORE_RAY'] = ('Rhombic ray (polar Cleo Towers core)', P - P.mean(0))
    core_rays.append(P)
core = KITS_CS['cleoSphere']['entries']
vID = vol(ID); vOut = vol(S[12])
tvol = sum(vol(pieces[e['shape']][1]) for _, e in tower_entries)
assert abs(vID + tvol - vOut) < 1e-6, (vID + tvol, vOut)
upto3 = [e for k, e in tower_entries if k < 3]; vOut3 = vol(S[edges[3]])
assert abs(vID + sum(vol(pieces[e['shape']][1]) for e in upto3) - vOut3) < 1e-6
# the OG core of 80 spires
D = json.load(open(sys.argv[1]))
qf = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
OG = np.array([[qf(x) for x in p] for p in D['V']]); OG /= np.linalg.norm(OG, axis=1).max()
def pyr_place(Pc, P):
    """rotation R, shift t with P = Pc @ R.T + t, matching apex to apex and the base in cyclic order (either way round)"""
    n = len(P) - 1
    for sh in range(n):
        for dr in (1, -1):
            idx = [(sh + dr * j) % n for j in range(n)] + [n]; Q = P[idx]
            A, B = Pc - Pc.mean(0), Q - Q.mean(0); U, _, Wt = np.linalg.svd(B.T @ A); R = U @ np.diag([1, 1, np.sign(np.linalg.det(U @ Wt))]) @ Wt
            if np.abs(A @ R.T - B).max() < 1e-7: return R, Q.mean(0) - Pc.mean(0) @ R.T
    return None
aktis_entries = []; canonA = {}
for e, f in faces_of(OG):
    P = np.vstack([OG[f], np.zeros(3)]); pid = 'HEX_AKTIS' if len(f) == 6 else 'DELTOID_AKTIS'
    if pid not in canonA:
        canonA[pid] = P - P.mean(0); pieces[pid] = ('DICTO Hex Aktis' if len(f) == 6 else 'DICTO Deltoid Aktis', canonA[pid])
    m = pyr_place(canonA[pid], P); assert m, pid
    aktis_entries.append(dict(shape=pid, position=[round(float(x), 12) for x in m[1]], quaternion=quat(m[0])))
assert sum(1 for e in aktis_entries if e['shape'] == 'HEX_AKTIS') == 20 and len(aktis_entries) == 80
assert abs(sum(vol(pieces[e['shape']][1]) for e in aktis_entries) - vol(OG)) < 1e-9
pc_entries = []
for P in core_rays:
    m = pyr_place(pieces['POLAR_CORE_RAY'][1], P); assert m, 'polar core ray'
    pc_entries.append(dict(shape='POLAR_CORE_RAY', position=[round(float(x), 12) for x in m[1]], quaternion=quat(m[0])))
vpol = vol(beat(5)); assert abs(sum(vol(pieces[e['shape']][1]) for e in pc_entries + polar_entries) - vpol) < 1e-6
# the DICTO OTT core of 38 rays (radius 1)
D2 = json.load(open(sys.argv[2]))
OTT = np.array([[qf(x) for x in p] for p in D2['V']]); OTT /= np.linalg.norm(OTT, axis=1).max()
ott_entries = []
for e, f in faces_of(OTT):
    P = np.vstack([OTT[f], np.zeros(3)]); m = None
    for pid in [k for k in pieces if k.startswith('OTT_')]:
        if len(pieces[pid][1]) == len(P): m = pyr_place(pieces[pid][1], P)
        if m: break
    if not m:
        m_ = P[:-1].mean(0); octa_ = len(f) == 3 and abs(abs(m_[0]) - abs(m_[1])) < 1e-9 and abs(abs(m_[1]) - abs(m_[2])) < 1e-9
        pid = 'OTT_CLEO_ICOS' if octa_ else ('OTT_TRIANGLE_RAY' if len(f) == 3 else 'OTT_RHOMBIC_RAY')
        pieces[pid] = ({'OTT_CLEO_ICOS': 'Cleo-Icos (DICTO OTT octahedral ray)', 'OTT_TRIANGLE_RAY': 'DICTO OTT triangle ray', 'OTT_RHOMBIC_RAY': 'DICTO OTT rhombic ray'}[pid], P - P.mean(0))
        m = pyr_place(pieces[pid][1], P)
    ott_entries.append(dict(shape=pid, position=[round(float(x), 12) for x in m[1]], quaternion=quat(m[0])))
from collections import Counter as _C
assert _C(e['shape'] for e in ott_entries) == {'OTT_CLEO_ICOS': 8, 'OTT_TRIANGLE_RAY': 24, 'OTT_RHOMBIC_RAY': 6}, _C(e['shape'] for e in ott_entries)
assert abs(sum(vol(pieces[e['shape']][1]) for e in ott_entries) - vol(OTT)) < 1e-9
RAW = {pid: {'name': nm, 'vertices': np.round(P, 12).tolist(), 'faces': piece_faces(P)} for pid, (nm, P) in pieces.items()}
KITS = {
    'cleoTowers.three': {'label': 'Cleo Towers · CLEO sphere + 3 shells (1, 1, 2 beats)', 'group': 'cleo', 'entries': core + upto3},
    'cleoTowers': {'label': 'Cleo Towers · CLEO sphere + 5 shells (1, 1, 2, 3, 5 beats)', 'group': 'cleo', 'entries': core + [e for _, e in tower_entries]},
    'ogAktis': {'label': 'OG core · 20 Hex Aktis + 60 Deltoid Aktis', 'group': 'cleo', 'entries': aktis_entries},
    'polarTowers': {'label': 'Polar Cleo Towers · RT core + 5 shells (5, 3, 2, 1, 1 beats)', 'group': 'cleo', 'entries': pc_entries + polar_entries},
    'ottRays': {'label': 'OTT core · 8 Cleo-Icos + 24 triangle rays + 6 rhombic rays', 'group': 'cleo', 'entries': ott_entries},
}
out = f"""// Generated by scripts/build-cleo-towers.py (DICTO 2026-10-20). Do not edit.
// Cleo Towers: shells of the tallest towers round the CLEO sphere in 1, 1, 2, 3, 5 beats of the Universal PiTet rule; and the OG core of
// 80 spires: the DICTO Ogdoecontahedron as 20 DICTO Hex Aktis + 60 DICTO Deltoid Aktis, every apex at the centre (DICTO's ideas and names);
// the polar Cleo Towers (beat k -> 5 - k about the GTI's circumsphere); and the DICTO OTT core of 38 rays (8 of them Cleo-Icos).
import {{ specOf }} from './stellaJewel.js';
const RAW = {json.dumps(RAW, separators=(',', ':'))};
export const CLEO_TOWERS_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, specOf(id, p.name, p.vertices, p.faces, false, 1)]));
export const CLEO_TOWERS_ADDITION_IDS = Object.keys(CLEO_TOWERS_ADDITIONS);
export const CLEO_TOWERS_KITS = {json.dumps(KITS, separators=(',', ':'))};
// Volumes (radius-1 frame) for the tests: CLEO sphere {vID:.12f}; with 3 shells {vOut3:.12f}; with 5 shells {vOut:.12f}; the OG {vol(OG):.12f}.
export const CLEO_TOWERS_VOLUMES = {json.dumps(dict(core=round(vID, 12), three=round(vOut3, 12), five=round(vOut, 12), og=round(vol(OG), 12), polar=round(vpol, 12), ott=round(vol(OTT), 12)))};
"""
open(os.path.join(ROOT, 'src/krp-core/src/polyhedra/cleo-towers.js'), 'w').write(out)
print('pieces', {k: len(v['faces']) for k, v in RAW.items()}); print({k: len(v['entries']) for k, v in KITS.items()}, 'bytes', len(out))
