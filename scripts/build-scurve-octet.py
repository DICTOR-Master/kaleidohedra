# Builds src/krp-core/src/polyhedra/scurve-octet.js (DICTO 2026-10-20): the S-curved double octet, DICTO's construction set, as
# Polyhedraverse pieces and kits. The octet truss (corners: integer points of even sum; octahedra centred on the odd ones) with
#   - the octahedron's faces alternating dome and hollow (checkerboard), turned on two of the four interleaved cubic lattices of octahedron
#     centres, so every tetrahedron meets 2 domes and 2 hollows (DICTO: "two triangles of each, pivoting and folding");
#   - faces as pillow domes with straight edges, height k L1 L2 L3 (inside the face's cone from the tetrahedron's centre);
#   - then all of space bent, x -> x + E (sin 2 pi y, sin 2 pi z, sin 2 pi x) (DICTO: "a spherical S-curved lattice ... the shapes will
#     change but the relationship should remain"): corners and edge midpoints stay, every edge becomes a shared S-curve, still filling space.
# The bend has period 1, so pieces a lattice step apart are congruent: four shapes (tetrahedron up and down, octahedron in its two turns).
# Studies: kaleidohedra research branch, studies/2026-10-20-double-octet (block filled exactly, float). Usage: python3 scripts/build-scurve-octet.py
import itertools, json, os
import numpy as np
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
T_PLUS = {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}; T_MINUS = {tuple(-x for x in n) for n in T_PLUS}
H_TRI = np.sqrt(2) * np.sqrt(3) / 2; K = 0.98 * 4 * H_TRI * np.tan(np.arctan(1 / np.sqrt(2))); NG = 12; E = 0.07
plus = lambda c: sum(int(x) % 2 for x in c) == 1 and (int(c[0]) % 2 == 1 or int(c[1]) % 2 == 1)
bend = lambda P: P + E * np.stack([np.sin(2 * np.pi * P[:, 1]), np.sin(2 * np.pi * P[:, 2]), np.sin(2 * np.pi * P[:, 0])], 1)
def creases(V, T, deg=40):                           # outline only where the surface folds sharply, not every mesh edge (as Tetoktjiru)
    V = np.asarray(V, float); T = np.asarray(T)
    N = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); N /= np.linalg.norm(N, axis=1)[:, None] + 1e-12; by = {}
    for f, tri in enumerate(T):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])): by.setdefault((min(a, b), max(a, b)), []).append(f)
    return [[int(a), int(b)] for (a, b), fs in by.items() if len(fs) == 2 and N[fs[0]] @ N[fs[1]] < np.cos(np.radians(deg))]
def patch(P, sign, out):
    pts, idx = [], {}
    for i in range(NG + 1):
        for j in range(NG + 1 - i):
            L = np.array([i, j, NG - i - j], float) / NG; idx[(i, j)] = len(pts); pts.append(L @ P + sign * K * L.prod() * out)
    tris = []
    for i in range(NG):
        for j in range(NG - i):
            tris.append([idx[(i, j)], idx[(i + 1, j)], idx[(i, j + 1)]])
            if j + i + 1 < NG: tris.append([idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]])
    return np.array(pts), tris
def mesh(faces):
    V, T, key = [], [], {}
    for P, sign, out in faces:
        pts, tris = patch(np.array(P, float), sign, out); loc = []
        for p in pts:
            k = tuple(np.round(p, 9))
            if k not in key: key[k] = len(V); V.append(p)
            loc.append(key[k])
        for a, b, c in tris:
            n = np.cross(V[loc[b]] - V[loc[a]], V[loc[c]] - V[loc[a]])
            T.append([loc[a], loc[b], loc[c]] if n @ out >= 0 else [loc[a], loc[c], loc[b]])
    return bend(np.array(V, float)), T
def octa(cen):
    cen = np.array(cen, float); D = T_PLUS if plus(cen) else T_MINUS
    return mesh([(np.array([cen + sg[j] * np.eye(3)[j] for j in range(3)]), 1 if tuple(sg) in D else -1, np.array(sg, float) / np.sqrt(3)) for sg in itertools.product((1, -1), repeat=3)])
def tet(V):
    V = np.array(V, float); c = V.mean(0); F = []
    for k in range(4):
        P = V[[i for i in range(4) if i != k]]; ocen = (P.sum(0) - V[k]) / 2; n = np.sign(P.mean(0) - c).astype(int)
        D = T_PLUS if plus(ocen) else T_MINUS; nn = np.cross(P[1] - P[0], P[2] - P[0]); nn /= np.linalg.norm(nn)
        if nn @ (P.mean(0) - c) < 0: nn = -nn
        F.append((P, -1 if tuple(-n) in D else 1, nn))
    return mesh(F)
def tet_at(base):
    base = np.array(base, float); even = int(base.sum()) % 2 == 0
    return ('UP' if even else 'DOWN'), base + np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if even else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)], float)
vol = lambda V, T: abs(sum(np.dot(V[a], np.cross(V[b], V[c])) for a, b, c in T)) / 6
canon, RAW = {}, {}
NAMES = {'SCURVE_TET_UP': 'S-curved double octet tetrahedron (up)', 'SCURVE_TET_DOWN': 'S-curved double octet tetrahedron (down)',
         'SCURVE_OCT_A': 'S-curved double octet octahedron (turn A)', 'SCURVE_OCT_B': 'S-curved double octet octahedron (turn B)'}
def place(pid, V, T):
    """a piece as its shape (centred at its own centre of corners) + a translation; checked: a pure translate of the shape"""
    m = V.mean(0)
    if pid not in canon:
        nm = NAMES.get(pid) or f"S-curved double octet tetrahedron ({pid.split('_')[2].lower()}, cube {pid.split('_')[3]})"
        canon[pid] = V - m; RAW[pid] = {'name': nm, 'vertices': np.round(V - m, 9).tolist(), 'faces': T, 'edges': creases(V - m, T)}
    assert np.abs((V - m) - canon[pid]).max() < 1e-9, (pid, 'not a translate')
    return {'shape': pid, 'position': [round(float(x), 9) for x in m], 'quaternion': [0, 0, 0, 1]}
def octa_entry(c): V, T = octa(c); return place('SCURVE_OCT_A' if plus(c) else 'SCURVE_OCT_B', V, T), vol(V, T)
def tet_entry(b):
    kind, C = tet_at(b); V, T = tet(C); cls = ''.join(str(int(x) % 2) for x in b)              # the dome pattern repeats every 2 cubes
    return place(f'SCURVE_TET_{kind}_{cls}', V, T), vol(V, T)
# kit 1: one octahedron and its eight tetrahedra; kit 2: a block (the 8 tetrahedra of a 2 x 2 x 2 block of cubes and the 13 octahedra round them)
o, vo = octa_entry((1, 0, 0)); kit1 = [o]
for sg in itertools.product((0, 1), repeat=3):
    pass
cen = np.array([1, 0, 0])
for sg in itertools.product((1, -1), repeat=3):
    corner = cen + np.array(sg); far = np.minimum(cen, corner) * 0 + np.array([min(cen[i], corner[i]) for i in range(3)])
    e, _ = tet_entry(tuple(int(x) for x in far)); kit1.append(e)
kit2 = [tet_entry(b)[0] for b in itertools.product((0, 1), repeat=3)]
for c in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 1, 2), (1, 2, 2), (2, 2, 1)]:
    kit2.append(octa_entry(c)[0])
# the eight tetrahedra round the octahedron at (1,0,0) are those of the cubes touching it; check each shares a face with it
assert len(kit1) == 9 and len({tuple(e['position']) for e in kit1}) == 9
KITS = {'sCurveOctet': {'label': 'S-curved double octet · one octahedron + its 8 tetrahedra', 'group': 'sets', 'entries': kit1},
        'sCurveOctet.block': {'label': 'S-curved double octet · a block (8 tetrahedra + 13 octahedra)', 'group': 'sets', 'entries': kit2}}
VOL = {pid: round(vol(np.array(r['vertices']), r['faces']), 9) for pid, r in RAW.items()}
out = f"""// Generated by scripts/build-scurve-octet.py (DICTO 2026-10-20). Do not edit.
// The S-curved double octet, DICTO's construction set: octahedra whose faces alternate dome and hollow, tetrahedra of 2 domes and 2 hollows,
// the whole octet bent so every edge is an S-curve; still filling space, every face shared. Four shapes (tetrahedron up and down,
// octahedron in its two turns), placed by translation.
import {{ specOf }} from './stellaJewel.js';
const RAW = {json.dumps(RAW, separators=(',', ':'))};
export const SCURVE_OCTET_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, {{ ...specOf(id, p.name, p.vertices, p.faces, true, 1), edges: p.edges }}]));
export const SCURVE_OCTET_ADDITION_IDS = Object.keys(SCURVE_OCTET_ADDITIONS);
export const SCURVE_OCTET_KITS = {json.dumps(KITS, separators=(',', ':'))};
export const SCURVE_OCTET_VOLUMES = {json.dumps(VOL)};
"""
open(os.path.join(ROOT, 'src/krp-core/src/polyhedra/scurve-octet.js'), 'w').write(out)
# which of the tetrahedron classes are the same shape (as point sets, after centring)?
ids = sorted(RAW); same = []
for a, b in itertools.combinations(ids, 2):
    A, B = np.array(RAW[a]['vertices']), np.array(RAW[b]['vertices'])
    if len(A) == len(B) and all(np.abs(B - x).sum(1).min() < 1e-7 for x in A): same.append((a, b))
print('identical shapes:', same)
# merge identical shapes: entries of the second use the first's spec (same point set, same centre, so the same position)
for a, b in same:
    if b in RAW and a in RAW:
        for kit in KITS.values():
            for e in kit['entries']:
                if e['shape'] == b: e['shape'] = a
        del RAW[b]
for i, pid in enumerate(sorted(k for k in RAW if k.startswith('SCURVE_TET'))):
    RAW[pid]['name'] = f'S-curved double octet tetrahedron {i + 1}'
VOL = {pid: round(vol(np.array(r['vertices']), r['faces']), 9) for pid, r in RAW.items()}
out = f"""// Generated by scripts/build-scurve-octet.py (DICTO 2026-10-20). Do not edit.
// The S-curved double octet, DICTO's construction set: octahedra whose faces alternate dome and hollow, tetrahedra of 2 domes and 2 hollows,
// the whole octet bent so every edge is an S-curve; still filling space, every face shared. Six shapes (four tetrahedra, the octahedron in
// two turns), placed by translation.
import {{ specOf }} from './stellaJewel.js';
const RAW = {json.dumps(RAW, separators=(',', ':'))};
export const SCURVE_OCTET_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, {{ ...specOf(id, p.name, p.vertices, p.faces, true, 1), edges: p.edges }}]));
export const SCURVE_OCTET_ADDITION_IDS = Object.keys(SCURVE_OCTET_ADDITIONS);
export const SCURVE_OCTET_KITS = {json.dumps(KITS, separators=(',', ':'))};
export const SCURVE_OCTET_VOLUMES = {json.dumps(VOL)};
"""
open(os.path.join(ROOT, 'src/krp-core/src/polyhedra/scurve-octet.js'), 'w').write(out)
print({k: len(v['faces']) for k, v in RAW.items()}, VOL, {k: len(v['entries']) for k, v in KITS.items()}, 'bytes', len(out))
