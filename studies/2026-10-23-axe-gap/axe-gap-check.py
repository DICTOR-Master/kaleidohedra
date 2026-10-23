# The AXE gap of the simple cubic icosahedron lattice (DICTO 2026-10-23). Checks, and writes data/:
#   - Unborn (DICTO's name; Koca et al. 2015's pseudoicosahedron, x = 1/tau) exact, centred, faces outward;
#   - the 6 AXE of one cell (Mosseri-Sadoc t6, krp-core KIT13_ICOSA13_AXE), each congruent to the kit AXE by corner matching;
#   - the 8 Tricaps (t3) of one icosahedron, each inside it and inside its void dodecahedron;
#   - volumes per cell in exact Q(sqrt5) arithmetic: icosahedron + Unborn + 6 AXE = Lotus Jewel + 8 Tricaps + Unborn + 6 AXE = phi^3;
#   - point tests (200 000 random points of one cell): every point in exactly one piece, for the three readings
#     (1) icosahedra + Unborn + AXE, (2) Lotus Jewels + void dodecahedra + AXE, (3) Lotus Jewels + Tricaps + Unborn + AXE;
#   - the app's Lotus Jewel (octet-data's clawed icosahedron) = icosahedron minus its 8 Tricaps, by a winding-number test.
# Scale: icosahedron edge 1 (krp-core POLYHEDRA scale); lattice spacing phi; the icosahedron at the origin, its void
# dodecahedron (edge 1/phi, EKP orientation) at (phi/2)(1,1,1). Usage (repo root): python3 studies/2026-10-23-axe-gap/axe-gap-check.py
import itertools, json, re
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull

OUT = 'studies/2026-10-23-axe-gap/data/'
PHI = (1 + 5 ** 0.5) / 2; h = PHI / 2
fails = []
def check(label, ok):
    print(('OK   ' if ok else 'FAIL ') + label)
    if not ok: fails.append(label)

# ---- exact arithmetic in Q(sqrt5): (a, b) = a + b sqrt5 ----
class Q5:
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __eq__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s.a == o.a and s.b == o.b
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s): return f'{s.a} + {s.b}√5'
V_ICO = Q5(Fr(15, 12), Fr(5, 12))          # 5(3 + sqrt5)/12
V_UNBORN = Q5(Fr(3, 12), Fr(7, 12))        # (3 + 7 sqrt5)/12
V_DODECA = Q5(Fr(5, 4), Fr(1, 4))          # (5 + sqrt5)/4, edge 1/phi
V_TRICAP = Q5(Fr(3, 24), Fr(-1, 24))       # (3 - sqrt5)/24
V_AXE = Q5(Fr(1, 12))                       # 1/12
V_JEWEL = Q5(Fr(1, 4), Fr(3, 4))           # (1 + 3 sqrt5)/4
PHI3 = Q5(2, 1)                             # phi^3 = 2 + sqrt5

# ---- the pieces ----
ico = np.array([p for s1 in (1, -1) for s2 in (1, -1) for p in [(0, s1 * .5, s2 * h), (s1 * .5, s2 * h, 0), (s2 * h, 0, s1 * .5)]])
cyc = lambda p: [p, (p[2], p[0], p[1]), (p[1], p[2], p[0])]
U0 = np.array([q for s1 in (1, -1) for s2 in (1, -1) for q in cyc((s1 * h, s2 / (2 * PHI), 0))])   # Unborn, centred (cyclic (±phi/2, ±1/(2phi), 0))
C = np.array([h, h, h])
U = U0 + C
cube = np.array([C + np.array([a, b, c]) for a in (-.5, .5) for b in (-.5, .5) for c in (-.5, .5)])
D = np.vstack([U, cube])                     # the void dodecahedron
axe = np.array([(-.5, h, 0), (.5, h, 0), (0, h + .5 / PHI, h), (0, h - .5 / PHI, h)])
H_STUDY = np.array(json.load(open('studies/2026-10-10-icosa-networks-2/data/sc-star-H-unit.json'))['vertices'])
key = lambda P: sorted(tuple(np.round(p, 6)) for p in P)
check('Unborn = the study\'s H (sc-star-H-unit.json), same 12 vertices', key(U) == key(H_STUDY))

def hull_faces(P):
    """Outward triangles of a convex hull (coplanar triangles kept apart: every face here is a triangle)."""
    hl = ConvexHull(P); c = P.mean(0); out = []
    for s, eq in zip(hl.simplices, hl.equations):
        a, b, cc = P[s]; n = np.cross(b - a, cc - a)
        out.append([int(x) for x in (s if n @ (a - c) > 0 else s[::-1])])
    return out, hl
UF, uh = hull_faces(U0)
d = lambda a, b: float(np.linalg.norm(a - b))
edges = sorted({tuple(sorted((f[i], f[(i + 1) % 3]))) for f in UF for i in range(3)})
lens = sorted(round(d(U0[a], U0[b]), 6) for a, b in edges)
eq_faces = sum(all(abs(d(U0[f[i]], U0[f[(i + 1) % 3]]) - 1) < 1e-9 for i in range(3)) for f in UF)
check(f'Unborn: 12 vertices, {len(UF)} faces (want 20), {len(edges)} edges (want 30): {lens.count(round(1 / PHI, 6))} of 1/phi (want 6), {lens.count(1.0)} of 1 (want 24); {eq_faces} equilateral faces (want 8), {len(UF) - eq_faces} isosceles (1/phi, 1, 1) (want 12)',
      len(UF) == 20 and len(edges) == 30 and lens.count(round(1 / PHI, 6)) == 6 and lens.count(1.0) == 24 and eq_faces == 8)
check(f'Unborn volume {uh.volume:.9f} = (3 + 7√5)/12 = {float(V_UNBORN):.9f}', abs(uh.volume - float(V_UNBORN)) < 1e-9)
dh = ConvexHull(D)
check(f'void dodecahedron: 20 vertices on the hull ({len(dh.vertices)}), volume {dh.volume:.9f} = (5 + √5)/4', len(dh.vertices) == 20 and abs(dh.volume - float(V_DODECA)) < 1e-9)

# The 6 AXE of a cell: the images of one AXE under the pyritohedral group m-3 about the icosahedron's centre (cyclic
# permutations x sign changes), each moved by a lattice vector so its centroid lies in [0, phi)^3.
ops = [(perm, np.array(sg)) for perm in [(0, 1, 2), (1, 2, 0), (2, 0, 1)] for sg in itertools.product((1, -1), repeat=3)]
axes = {}
for perm, sg in ops:
    V = axe[:, perm] * sg; c = V.mean(0); t = np.floor(c / PHI + 1e-9) * PHI; V = V - t
    k = tuple(np.round(V.mean(0), 6))
    if k not in axes: axes[k] = V
AX = list(axes.values())
check(f'distinct AXE per cell: {len(AX)} (want 6)', len(AX) == 6)
kit = re.search(r'"KIT13_ICOSA13_AXE":\{"name":"AXE","vertices":(\[\[.*?\]\])', open('src/krp-core/src/polyhedra/kits13.js').read())
KIT = np.array(json.loads(kit.group(1)))
def congruent(P, Q):
    """Corner matching: some ordering of P's corners has the same pairwise distances as Q's."""
    dq = np.array([[d(a, b) for b in Q] for a in Q])
    return any(np.allclose(np.array([[d(P[i], P[j]) for j in p] for i in p]), dq, atol=1e-6) for p in itertools.permutations(range(len(P))))
vol = lambda P: abs(np.linalg.det(np.array([P[1] - P[0], P[2] - P[0], P[3] - P[0]]))) / 6
check('each AXE congruent to krp-core KIT13_ICOSA13_AXE (corner matching), volume 1/12: ' + ', '.join(f'{vol(V):.9f}' for V in AX),
      all(congruent(V, KIT) and abs(vol(V) - 1 / 12) < 1e-12 for V in AX))
# Where each AXE sits: its long edge (1) is the edge two neighbouring icosahedra share, its short edge (1/phi) an edge two Unborns share.
def edge_ok(V):
    pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    lng = [p for p in pairs if abs(d(V[p[0]], V[p[1]]) - 1) < 1e-9]; sht = [p for p in pairs if abs(d(V[p[0]], V[p[1]]) - 1 / PHI) < 1e-9]
    if len(lng) != 5 or len(sht) != 1: return False
    i, j = sht[0]; o = [k for k in range(4) if k not in (i, j)]
    # the edge opposite the short one: on two icosahedra a lattice step apart
    on_ico = lambda p: [tuple(t) for t in itertools.product(range(-1, 3), repeat=3) if any(np.allclose(p, q + np.array(t) * PHI, atol=1e-9) for q in ico)]
    shared_ico = set(on_ico(V[o[0]])) & set(on_ico(V[o[1]]))
    on_un = lambda p: [tuple(t) for t in itertools.product(range(-2, 3), repeat=3) if any(np.allclose(p, q + np.array(t) * PHI, atol=1e-9) for q in U)]
    shared_un = set(on_un(V[i])) & set(on_un(V[j]))
    return len(shared_ico) == 2 and len(shared_un) == 2
check('each AXE: its opposite-to-short edge is shared by 2 icosahedra, its 1/phi edge by 2 Unborns', all(edge_ok(V) for V in AX))
# The face each AXE straddles: centroid on a cell face (one coordinate 0), and that face's two AXE.
face_axis = [int(np.argmin(np.abs(V.mean(0)))) for V in AX]
check(f'AXE centroids on the cell faces: axes {sorted(face_axis)} (two per face)', sorted(face_axis) == [0, 0, 1, 1, 2, 2] and all(abs(V.mean(0)[a]) < 1e-9 for V, a in zip(AX, face_axis)))

# The 8 Tricaps of the icosahedron at the origin: its corner face towards a void (direction s) and the void dodecahedron's cube corner s/(2phi).
TRI = []
for s in itertools.product((1, -1), repeat=3):
    s = np.array(s); base = ico[np.argsort(-(ico @ s))[:3]]
    TRI.append(np.vstack([s / (2 * PHI), base]))
tc = ConvexHull(TRI[0]).volume
inside = lambda P, hull: (P @ hull.equations[:, :3].T + hull.equations[:, 3] <= 1e-9).all()
ih = ConvexHull(ico)
tri_d = [T + 0 for T in TRI]
check(f'Tricap volume {tc:.9f} = (3 − √5)/24; each inside the icosahedron and inside its void dodecahedron; congruent to each other',
      abs(tc - float(V_TRICAP)) < 1e-12 and all(inside(T, ih) for T in TRI)
      and all(inside(T, ConvexHull(D + (np.sign(T[0]) - 1) * h)) for T in TRI) and all(congruent(T, TRI[0]) for T in TRI))

# ---- exact volumes per cell ----
s1 = V_ICO + V_UNBORN + 6 * V_AXE; s2 = V_JEWEL + V_DODECA + 6 * V_AXE; s3 = V_JEWEL + 8 * V_TRICAP + V_UNBORN + 6 * V_AXE
check(f'exact: icosahedron = Lotus Jewel + 8 Tricaps ({V_JEWEL + 8 * V_TRICAP}), dodecahedron = Unborn + 8 Tricaps ({V_UNBORN + 8 * V_TRICAP})',
      V_JEWEL + 8 * V_TRICAP == V_ICO and V_UNBORN + 8 * V_TRICAP == V_DODECA)
check(f'exact per cell: ico + Unborn + 6 AXE = {s1}; Jewel + dodeca + 6 AXE = {s2}; Jewel + 8 Tricap + Unborn + 6 AXE = {s3}; phi^3 = {PHI3}', s1 == PHI3 and s2 == PHI3 and s3 == PHI3)
check(f'numeric: ico {float(V_ICO):.9f} + Unborn {float(V_UNBORN):.9f} + 6 AXE 0.5 = {float(s1):.9f} = phi^3 {PHI ** 3:.9f}', abs(float(s1) - PHI ** 3) < 1e-12)

# ---- point tests ----
rng = np.random.default_rng(1); P = rng.random((200000, 3)) * PHI
shifts = [np.array(t) * PHI for t in itertools.product(range(-1, 2), repeat=3)]
def count_in(V):
    E = ConvexHull(V).equations
    return (P @ E[:, :3].T + E[:, 3] <= 1e-12).all(1)
inI = np.zeros(len(P), int); inU = np.zeros(len(P), int); inD = np.zeros(len(P), int); inA = np.zeros(len(P), int); inT = np.zeros(len(P), int)
for o in shifts:
    inI += count_in(ico + o); inU += count_in(U + o); inD += count_in(D + o)
    for V in AX: inA += count_in(V + o)
    for T in TRI: inT += count_in(T + o)
inJ = inI - inT  # in an icosahedron and in none of its Tricaps (each Tricap lies in its icosahedron)
for name, tot, share in [('(1) icosahedra + Unborn + AXE', inI + inU + inA, {'ico': inI, 'Unborn': inU, 'AXE': inA}),
                         ('(2) Lotus Jewels + void dodecahedra + AXE', inJ + inD + inA, {'Jewel': inJ, 'dodeca': inD, 'AXE': inA}),
                         ('(3) Lotus Jewels + Tricaps + Unborn + AXE', inJ + inT + inU + inA, {'Jewel': inJ, 'Tricap': inT, 'Unborn': inU, 'AXE': inA})]:
    print('     ', name, 'shares', {k: round(float(v.mean()), 5) for k, v in share.items()})
    check(f'{name}: {len(P)} points, {(tot == 0).sum()} in no piece, {(tot > 1).sum()} in more than one', (tot == 0).sum() == 0 and (tot > 1).sum() == 0)
print('      exact shares: ico %.5f Unborn %.5f AXE %.5f Jewel %.5f Tricaps %.5f dodeca %.5f' % tuple(float(v) / PHI ** 3 for v in (V_ICO, V_UNBORN, 6 * V_AXE, V_JEWEL, 8 * V_TRICAP, V_DODECA)))

# The app's Lotus Jewel (the clawed icosahedron) is exactly the icosahedron minus its 8 Tricaps: winding numbers of its mesh.
J = json.load(open('studies/2026-10-10-icosa-networks-3/data/clawed-icosahedron-unit.json'))
JV, JF = np.array(J['vertices']), J['faces']
JV = JV - (JV.max(0) + JV.min(0)) / 2
Q = rng.random((40000, 3)) * 2 - 1
w = np.zeros(len(Q))
for f in JF:
    for i in range(1, len(f) - 1):
        a, b, c = (JV[f[0]] - Q), (JV[f[i]] - Q), (JV[f[i + 1]] - Q)
        la, lb, lc = (np.linalg.norm(x, axis=1) for x in (a, b, c))
        num = np.einsum('ij,ij->i', a, np.cross(b, c))
        den = la * lb * lc + np.einsum('ij,ij->i', a, b) * lc + np.einsum('ij,ij->i', b, c) * la + np.einsum('ij,ij->i', c, a) * lb
        w += 2 * np.arctan2(num, den)
w /= 4 * np.pi
inMesh = np.abs(w - 1) < 1e-6
inTheory = (Q @ ih.equations[:, :3].T + ih.equations[:, 3] <= 1e-12).all(1) & ~np.any([(Q @ ConvexHull(T).equations[:, :3].T + ConvexHull(T).equations[:, 3] <= 1e-12).all(1) for T in TRI], axis=0)
check(f'Lotus Jewel mesh (clawed-icosahedron-unit.json) = icosahedron minus 8 Tricaps: {len(Q)} points, {(inMesh != inTheory).sum()} disagree; volume {J["volume"]} = (1 + 3√5)/4',
      (inMesh != inTheory).sum() == 0 and abs(J['volume'] - float(V_JEWEL)) < 1e-8)

# ---- mixed networks (DICTO 2026-10-23): each Tricap given to its icosahedron or its dodecahedron ----
# Every Tricap is exactly icosahedron ∩ dodecahedron and no two overlap, so any assignment should tile. Tested here per point, cell by
# cell (a point's cell c = floor(P/phi): its own void dodecahedron, the 8 icosahedra on its corners, the AXE of the 27 cells round it):
# random assignments, and the app's patterns (world-octet.js mixedWhole): a cell whose block (floor(c / block)) is marked keeps its
# dodecahedron whole (all 8 Tricaps), the rest go to the icosahedra; Swap marks lattice points instead (whole icosahedra there).
mod = np.mod
def pyro_set(B):
    B = np.asarray(B)
    return np.any([((mod(B - np.array(o), 8) % 4 == 0).all(-1) & ((mod(B - np.array(o), 8).sum(-1) // 4) % 2 == 0))
                   for o in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]], axis=0)
PATTERNS = {'layers': lambda B: mod(B[..., 2], 2) == 0, 'rods': lambda B: mod(B[..., 0] + B[..., 1], 2) == 0,
            'checker': lambda B: mod(B.sum(-1), 2) == 0, 'pyrochlore': pyro_set}
check('pyrochlore set: 16 per 8^3 block', pyro_set(np.array(list(itertools.product(range(8), repeat=3)))).sum() == 16)
EI, ED = ConvexHull(ico).equations, ConvexHull(D - C).equations
EA = [ConvexHull(V).equations for V in AX]
ins = lambda Q, E: (Q @ E[:, :3].T + E[:, 3] <= 1e-12).all(1)
N = 200000; Pm = rng.random((N, 3)) * 6 * PHI - 3 * PHI   # 6 x 6 x 6 cells round the origin
cell = np.floor(Pm / PHI).astype(int); L = Pm - cell * PHI
inDc = ins(L - C, ED)
corners = [np.array(k) for k in itertools.product((0, 1), repeat=3)]
inIk = [ins(L - k * PHI, EI) for k in corners]
inAx = sum(ins(L - np.array(t) * PHI, E) for E in EA for t in itertools.product((-1, 0, 1), repeat=3))
def mixed_test(to_dodeca):
    """to_dodeca(cell, corner): bool arrays, does the Tricap shared by this cell's dodecahedron and the icosahedron on that corner go to the dodecahedron."""
    tot = inAx.copy()
    tric_to_d = np.zeros(N, bool); tric_to_i = np.zeros(N, bool); ico_any = np.zeros(N, bool)
    for k, m in zip(corners, inIk):
        t = m & inDc; g = to_dodeca(cell, k)
        tric_to_d |= t & g; tric_to_i |= t & ~g; ico_any |= m
    ico_piece = ico_any & ~tric_to_d; dod_piece = inDc & ~tric_to_i
    tot = tot + ico_piece + dod_piece
    return (tot == 0).sum(), (tot > 1).sum()
rand = np.random.default_rng(5)
for trial in range(2):
    salt = rand.integers(1 << 30)
    def to_d(c, k, salt=salt):  # a fixed random choice per Tricap (its cell and corner)
        hsh = (c[:, 0] * 73856093 ^ c[:, 1] * 19349663 ^ c[:, 2] * 83492791 ^ (k @ [1, 2, 4]) * 2654435761 ^ salt) & 0xffffffff
        return (hsh * 2654435761 & 0xffffffff) >> 31 == 1
    u, o = mixed_test(to_d)
    check(f'mixed, random Tricap assignment {trial + 1}: {N} points, {u} in no piece, {o} in more than one', u == 0 and o == 0)
for name, whole in PATTERNS.items():
    for block in (1, 2, 3):
        for swap in (False, True):
            fl = lambda X: np.floor_divide(X, block)
            if not swap: rule = lambda c, k: whole(fl(c))                 # the cell's dodecahedron whole: its Tricaps go to it
            else: rule = lambda c, k: ~whole(fl(c + k))                    # the corner's icosahedron whole: its Tricaps go to it
            u, o = mixed_test(rule)
            check(f'mixed {name}, block {block}{", swapped" if swap else ""}: {u} in no piece, {o} in more than one', u == 0 and o == 0)

# ---- data ----
r9 = lambda A: np.round(np.asarray(A, float), 9).tolist()
credit = 'DICTO (design study, 2026-10-23)'
un = {'credit': credit + "; Unborn is DICTO's name; the solid is Koca, Koca, Al-Mukhaini & Al-Qanobi 2015's pseudoicosahedron (x = 1/tau)",
      'name': 'Unborn: the void dodecahedron of the simple cubic icosahedron lattice minus its 8 Tricaps; cyclic (±phi/2, ±1/(2phi), 0)',
      'volume': round(uh.volume, 9), 'exactVolume': '(3 + 7√5)/12',
      'checks': ['convex', 'faces outward', '8 equilateral (1) + 12 isosceles (1/phi, 1, 1)', '30 edges: 6 of 1/phi, 24 of 1', 'equals sc-star-H'],
      'vertices': r9(U0), 'faces': UF}
parts = [{'role': 'ico', 'vertices': r9(ico), 'faces': hull_faces(ico)[0]}, {'role': 'unborn', 'vertices': r9(U), 'faces': hull_faces(U)[0]}]
parts += [{'role': 'tricap', 'direction': [int(x) for x in np.sign(T[0])], 'vertices': r9(T), 'faces': hull_faces(T)[0]} for T in TRI]
parts += [{'role': 'axe', 'faceAxis': a, 'vertices': r9(V), 'faces': hull_faces(V)[0]} for V, a in sorted(zip(AX, face_axis), key=lambda x: (x[1], x[0].mean(0).tolist()))]
cell = {'credit': credit, 'name': "One cell of the simple cubic icosahedron lattice (spacing phi) as Lotus Jewel + 8 Tricaps + Unborn + 6 AXE: the icosahedron at the origin "
        "(role ico = Lotus Jewel + its 8 Tricaps), its Tricaps by direction, the Unborn at (phi/2)(1,1,1), and the cell's 6 AXE, two on each of the cell faces x = 0, y = 0, z = 0 (faceAxis)",
        'exactVolume': 'phi^3 = 2 + √5 (ico + Unborn + 6 × 1/12)',
        'checks': ['point tests: 0 uncovered, 0 covered twice (three readings)', 'AXE congruent to KIT13_ICOSA13_AXE', 'Tricaps inside icosahedron and dodecahedron'],
        'parts': parts}
for name, data in [('unborn', un), ('axe-cell-parts', cell)]:
    json.dump({**data, 'scale': 'icosahedron edge 1 (krp-core POLYHEDRA scale)'}, open(f'{OUT}{name}-unit.json', 'w'), separators=(',', ':'))
    raw = json.loads(json.dumps(data))
    for p in raw.get('parts', [raw]): p['vertices'] = r9(np.array(p['vertices']) / h)
    if 'volume' in raw: raw['volume'] = round(raw['volume'] / h ** 3, 9)
    json.dump({**raw, 'scale': 'unit / (phi/2): the EKP / Sunstar raw frame'}, open(f'{OUT}{name}-raw.json', 'w'), separators=(',', ':'))
print(f'{len(fails)} failures.' if fails else 'All checks passed (0 failures).')
raise SystemExit(1 if fails else 0)
