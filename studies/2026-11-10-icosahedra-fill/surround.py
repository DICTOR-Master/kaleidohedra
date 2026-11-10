"""Icosahedra-fill, step 2 pilot (DICTO 10 Nov 2026). Can the rhombic hexecontahedron star (20 prolate golden rhombohedra round a
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
RMAX = float(sys.argv[1]); MAXN = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
nodes = [0]; T0 = time.time()
def exposed(tiles):
    cnt = {}
    for t in tiles:
        for f in t['faces']: cnt[f] = cnt.get(f, 0) + 1
    return [f for f, n in cnt.items() if n == 1]
def solve(tiles):
    nodes[0] += 1
    if nodes[0] > MAXN: raise TimeoutError
    ex = [f for f in exposed(tiles) if np.linalg.norm(centre(f)) <= RMAX]
    if not ex: return tiles
    f = min(ex, key=lambda f: np.linalg.norm(centre(f)))
    for t in candidates(f, tiles):
        if any(overlap(t, s) for s in tiles): continue
        r = solve(tiles + [t])
        if r: return r
    return None
try:
    res = solve(start)
    print(f'RMAX {RMAX}: ' + (f'SURROUNDED with {len(res) - 20} extra prolate tiles' if res else 'IMPOSSIBLE (search exhausted)') + f'; nodes {nodes[0]}; {time.time()-T0:.0f} s')
    if res:
        import json
        json.dump({'rmax': RMAX, 'tiles': [{'p': list(t['p']), 'span': [list(x) for x in t['span']]} for t in res],
                   'axes_float': E.tolist()}, open(f'witness-{RMAX}.json', 'w'))
    sound = res is None or (len(res) >= 20 and not any(overlap(x, y) for x, y in itertools.combinations(res, 2)))
    print('FINAL ok' if sound else 'FINAL FAIL: witness has overlapping tiles')
except TimeoutError:
    print(f'RMAX {RMAX}: undecided after {MAXN} nodes ({time.time()-T0:.0f} s)'); print('FINAL TIMEOUT: search undecided')
