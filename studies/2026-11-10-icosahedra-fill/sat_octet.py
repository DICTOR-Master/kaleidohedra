"""[octet_stars.py, from surround.py] Icosahedra-fill, step 4 (DICTO 10 Nov 2026: 'test the stars on the octet'):
stars at the fcc points x(i,j,k), i+j+k even, cube axes = icosahedron 2-fold axes (octet 3-folds = icosahedron 3-folds); x = (2m + 2n phi)
in units of the unnormalised axis length; fill between the stars with prolate tiles only, near the origin star first.
usage: python octet_stars.py m n [maxnodes]
Original: Icosahedra-fill, step 2 pilot (DICTO 10 Nov 2026). Can the rhombic hexecontahedron star (20 prolate golden rhombohedra round a
point; its 20 inner Cleo-Icos form an icosahedron) be surrounded by PROLATE golden rhombohedra alone? Tiles: parallelepipeds spanned by
the three corner vectors of an icosahedron face (prolate), placed with corners in the module Z<e_1..e_6> (integer 6-vectors, exact
keys). Search: repeatedly take the exposed face nearest the centre within radius RMAX, try every prolate tile having that face on the
outside, reject interior overlaps (separating axes), backtrack. Result: 'surrounded to radius RMAX' with a witness, or 'impossible to
radius RMAX' (exhausted). usage: python surround.py RMAX [maxnodes]"""
import sys, itertools, time
import numpy as np
phi = (1 + 5 ** .5) / 2
V12 = []
for s1, s2 in itertools.product((1, -1), repeat=2):
    for v in ((0, s1, s2 * phi), (s1, s2 * phi, 0), (s2 * phi, 0, s1)): V12.append(np.array(v) / np.linalg.norm(v))
AX = V12[::2] if False else None
# 6 axes e_i (one of each antipodal pair) and their integer representation
axes = []
for v in V12:
    if not any(np.allclose(v, -a) or np.allclose(v, a) for a in axes): axes.append(v)
E = np.array(axes)                       # 6 x 3
def vec(iv): return np.array(iv) @ E     # integer 6-vector -> point
def unit(i, s):
    z = [0] * 6; z[i] = s; return tuple(z)
DIRS = [unit(i, s) for i in range(6) for s in (1, -1)]
faces_ico = [t for t in itertools.combinations(range(12), 3) if all(abs(V12[a] @ V12[b] - 1 / 5 ** .5) < 1e-9 for a, b in itertools.combinations(t, 2))]
assert len(faces_ico) == 20
def to_dir(v):
    for d in DIRS:
        if np.allclose(vec(d), v): return d
TRIPLES = [tuple(to_dir(V12[k]) for k in f) for f in faces_ico]          # prolate spanning triples (integer)
add = lambda p, q: tuple(x + y for x, y in zip(p, q))
def tile(p, a, b, c):
    vs = [p, add(p, a), add(p, b), add(p, c), add(add(p, a), b), add(add(p, a), c), add(add(p, b), c), add(add(add(p, a), b), c)]
    fs = []
    for (u, w), base in (((a, b), [p, add(p, c)]), ((a, c), [p, add(p, b)]), ((b, c), [p, add(p, a)])):
        for q in base: fs.append(frozenset([q, add(q, u), add(q, w), add(add(q, u), w)]))
    return {'p': p, 'span': (a, b, c), 'faces': fs, 'pts': np.array([vec(x) for x in vs])}
def axes_of(t):
    a, b, c = (vec(x) for x in t['span'])
    return [np.cross(a, b), np.cross(a, c), np.cross(b, c)], [a, b, c]
def overlap(t1, t2, eps=1e-7):
    n1, e1 = axes_of(t1); n2, e2 = axes_of(t2)
    for ax in n1 + n2 + [np.cross(x, y) for x in e1 for y in e2]:
        nn = np.linalg.norm(ax)
        if nn < 1e-9: continue
        ax = ax / nn; p1 = t1['pts'] @ ax; p2 = t2['pts'] @ ax
        if p1.max() <= p2.min() + eps or p2.max() <= p1.min() + eps: return False
    return True
start = [tile((0,) * 6, *tr) for tr in TRIPLES]
for x, y in itertools.combinations(start, 2): assert not overlap(x, y), 'star overlaps itself'
def centre(f): return np.mean([vec(q) for q in f], axis=0)
def candidates(face, tiles):
    q = sorted(face)                            # build spans from the face
    pts = [vec(x) for x in face]; c = centre(face)
    out = []
    for tr in TRIPLES:
        for p0 in face:
            for perm in itertools.permutations(tr):
                a, b, w = perm
                for sw in (1,):
                    t = tile(p0, a, b, w)
                    if face in t['faces']:
                        out.append(t)
                t2 = tile(add(p0, tuple(-x for x in w)), a, b, w)
                if face in t2['faces']: out.append(t2)
    uniq = {}
    for t in out: uniq[(t['p'], frozenset(t['span']))] = t
    return list(uniq.values())
m_, n_ = int(sys.argv[1]), int(sys.argv[2]); MAXN = int(sys.argv[3]) if len(sys.argv) > 3 else 300000
# integer 6-vectors along the cube axes: e_i + e_j or e_i - e_j parallel to a coordinate axis, length 2/s0 or 2 phi/s0
s0 = (1 + phi ** 2) ** .5
def axis_vec(k, length):
    for i, j in itertools.combinations(range(6), 2):
        for sg in (1, -1):
            v = E[i] + sg * E[j]; t = np.zeros(3); t[k] = length
            if np.allclose(v, t):
                z = [0] * 6; z[i] = 1; z[j] = sg; return tuple(z)
    raise ValueError
X = []
for k in range(3):
    a1 = axis_vec(k, 2 / s0); a2 = axis_vec(k, 2 * phi / s0)
    X.append(tuple(m_ * p + n_ * q for p, q in zip(a1, a2)))
x = np.linalg.norm(vec(X[0])); d_nn = x * 2 ** .5
pts = []
for i, j, k in itertools.product(range(-3, 4), repeat=3):
    if (i + j + k) % 2 == 0 and (i, j, k) != (0, 0, 0):
        P = tuple(i * X[0][q] + j * X[1][q] + k * X[2][q] for q in range(6))
        if np.linalg.norm(vec(P)) <= 2 * d_nn + 1e-9: pts.append(P)
def bbox(t): return t['pts'].min(0), t['pts'].max(0)
def ov(t, s):
    a, b = bbox(t); c, d = bbox(s)
    if np.any(b < c + 1e-9) or np.any(d < a + 1e-9): return False
    return overlap(t, s)
stars = list(start)
clash = False
for P in pts:
    for tr in TRIPLES:
        t = tile(P, *tr)
        if any(ov(t, s) for s in start): clash = True
        stars.append(t)
RMAX = d_nn
# only stars that can touch the fill region matter (fill reaches at most RMAX + longest tile diagonal ~ 2.4)
stars = list(start) + [t for t in stars[20:] if np.linalg.norm(t['pts'], axis=1).min() <= RMAX + 2.5]
print(f'octet m={m_} n={n_}: x {x:.4f}, star spacing {d_nn:.4f}, {len(pts)} neighbour stars; stars overlap: {clash}', flush=True)
if clash:
    print('FINAL ok: spacing too small (stars overlap)' if clash else 'FINAL FAIL'); sys.exit()
import os
if os.environ.get('RMAX_OVERRIDE'): RMAX = float(os.environ['RMAX_OVERRIDE']); print('RMAX override', RMAX)
TAG = 'octet'
# SAT FORM (DICTO 10 Nov 2026): decide outright whether the region between the stars, within radius RMAX of the origin star's
# centre, can be filled face to face by prolate rhombohedra (= Cleo-Icos + Antonius + Cleo-Icos). Candidates: every prolate tile
# reachable by face adjacency from the star faces (tile centre within RMAX + 1.5), not overlapping a star. Clauses: each exposed star
# face within RMAX is covered; every face of a chosen tile with centre within RMAX is a star face or shared with another chosen tile;
# overlapping candidates exclude each other. SAT -> witness (exact check by verify_exact.py); UNSAT -> no filling (under face to face).
from scipy.spatial import cKDTree
from pysat.solvers import Cadical153
T0 = time.time()
cnt = {}
for t in stars:
    for f in t['faces']: cnt[f] = cnt.get(f, 0) + 1
starface = {f for f, n in cnt.items()}
cands = {}; queue = [f for f, n in cnt.items() if n == 1 and np.linalg.norm(centre(f)) <= RMAX]; seen = set(queue)
starC = np.array([t['pts'].mean(0) for t in stars]); stree = cKDTree(starC)
# WINDOW (11-10 stage check: candidate list grew without end, the golden grid is dense): corners must lie within a bounded window in
# the hidden (Galois-conjugate) directions, as in cut-and-project tilings. W = largest hidden norm among star corners + WMARGIN.
# UNSAT is then 'no filling inside this window'; widen WMARGIN to extend.
_phi = (1 + 5 ** .5) / 2; _U = np.round(E * (1 + _phi ** 2) ** .5, 9)
_C = np.where(np.isclose(np.abs(_U), _phi), np.sign(_U) * (-1 / _phi), _U)
def hid(z): return np.linalg.norm(np.array(z) @ _C)
WMARGIN = float(os.environ.get('WMARGIN', '0.5'))
_starcorners = {q for t in stars for f in t['faces'] for q in f}
W = max(hid(q) for q in _starcorners) + WMARGIN
print(f'hidden window W = {W:.3f} (star max + {WMARGIN})', flush=True)
def in_window(t): return all(hid(q) <= W + 1e-9 for f in t['faces'] for q in f)
def clear_of_stars(t):
    c = t['pts'].mean(0)
    return not any(ov(t, stars[i]) for i in stree.query_ball_point(c, 2.5))
while queue:
    f = queue.pop()
    for t in candidates(f, []):
        key = (t['p'], frozenset(t['span']))
        if key in cands or np.linalg.norm(t['pts'].mean(0)) > RMAX + 1.5 or not in_window(t) or not clear_of_stars(t): continue
        cands[key] = t
        for g in t['faces']:
            if g not in seen and g not in starface and np.linalg.norm(centre(g)) <= RMAX: seen.add(g); queue.append(g)
    if len(cands) % 5000 == 0 and cands: print(f'  heartbeat candidates {len(cands)} queue {len(queue)} {time.time()-T0:.0f} s', flush=True)
C = list(cands.values()); n = len(C)
print(f'candidates {n} ({time.time()-T0:.0f} s)', flush=True)
byface = {}
for i, t in enumerate(C):
    for g in t['faces']: byface.setdefault(g, []).append(i)
S = Cadical153(); ncl = 0
for f, k in cnt.items():
    if k == 1 and np.linalg.norm(centre(f)) <= RMAX:
        lits = [i + 1 for i in byface.get(f, [])]
        if not lits: print('star face with no candidate: UNSAT at once'); 
        S.add_clause(lits); ncl += 1
for i, t in enumerate(C):
    for g in t['faces']:
        if g in starface or np.linalg.norm(centre(g)) > RMAX: continue
        S.add_clause([-(i + 1)] + [j + 1 for j in byface[g] if j != i]); ncl += 1
cen = np.array([t['pts'].mean(0) for t in C]); tree = cKDTree(cen); npairs = 0
for i, j in tree.query_pairs(2.45):
    if ov(C[i], C[j]): S.add_clause([-(i + 1), -(j + 1)]); npairs += 1
print(f'clauses: cover/match {ncl}, overlap pairs {npairs} ({time.time()-T0:.0f} s); solving', flush=True)
ok = S.solve()
print(f'{TAG} m={m_} n={n_} spacing {d_nn:.4f}: ' + ('SAT: a filling exists' if ok else 'UNSAT: no face-to-face filling with prolate rhombohedra') + f' ({time.time()-T0:.0f} s)')
if ok:
    import json
    model = set(l for l in S.get_model() if l > 0); used = [C[i] for i in range(n) if i + 1 in model]
    json.dump({'rmax': RMAX, 'tiles': [{'p': list(t['p']), 'span': [list(x) for x in t['span']]} for t in stars + used], 'axes_float': E.tolist()},
              open(f'sat-witness-{TAG}-{m_}-{n_}.json', 'w'))
    print(f'witness: {len(used)} fill tiles + {len(stars)} star tiles')
sound = (not ok) or not any(ov(x, y) for x, y in itertools.combinations([C[i] for i in range(n) if i + 1 in model], 2))
print('FINAL ok' if sound else 'FINAL FAIL: witness overlaps')
