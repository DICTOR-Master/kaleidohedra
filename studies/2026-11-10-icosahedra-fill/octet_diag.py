"""[octet_stars.py, from surround.py] Icosahedra-fill, step 4 (DICTO 10 Nov 2026: 'test the stars on the octet'):
stars at the fcc points x(i,j,k), i+j+k even, cube axes = icosahedron 2-fold axes (octet 3-folds = icosahedron 3-folds); x = (2m + 2n phi)
in units of the unnormalised axis length; fill between the stars with prolate tiles only, near the origin star first.
usage: python octet_diag.py m n [maxnodes]
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
# DIAGNOSTIC: star faces inside the fill radius that NO prolate tile can cover without hitting a star (ignores fill tiles)
cnt = {}
for t in stars:
    for f in t['faces']: cnt[f] = cnt.get(f, 0) + 1
ex = [f for f, n in cnt.items() if n == 1 and np.linalg.norm(centre(f)) <= RMAX]
dead = [f for f in ex if not any(not any(ov(t, s) for s in stars) for t in candidates(f, stars))]
print(f'exposed star faces within radius {RMAX:.3f}: {len(ex)}; uncoverable: {len(dead)}')
if dead: print('  nearest uncoverable face at radius', round(min(np.linalg.norm(centre(f)) for f in dead), 4))
print('FINAL ok' if len(ex) > 0 else 'FINAL FAIL: no exposed faces (setup error)')
