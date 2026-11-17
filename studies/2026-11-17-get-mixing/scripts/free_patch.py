#!/usr/bin/env python3
"""Exact patch checks for the decorated-lattice theorems (decorated_lattice.py, decorated_sft.py).
Mode 'AB': GET A and GET B (identity images) at the points of their common lattice L, constant on each line t + Z v,
v = -b1 + b2 - b3, the line choices drawn at random (seeded), independently.
Mode 'A2': GET A alone in two placements, A (identity, offset 0) and A' (image g40, offset (0,0,0,1,1,0)), constant on each plane
c3 = const (lattice coordinates), the plane choices at random.
Checks (exact): no two tiles overlap; every face lies on at most two tiles with opposite sides; every tile with all lattice
coordinates in 2..n-3 has all 30 faces matched (face to face).
Control: one switch put into a line (mode AB: A at c, B at c - v, the pair the exact table allows) or into a plane (mode A2:
A at c, A' at c + b1) must create an overlap or an unmatched inner face: the local rule, not the pair table alone, decides.
Usage: free_patch.py <k10 dir> <inchbald json> <n> <seed> <out json> <AB|A2>"""
import sys, json, time, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
t0 = time.time()
sol = load_solids(sys.argv[1], sys.argv[2]); n = int(sys.argv[3]); random.seed(int(sys.argv[4]))
MODE = sys.argv[6] if len(sys.argv) > 6 else 'AB'
SHAPE = {'A': ('A', IDENT, (0,)*6), 'B': ('B', IDENT, (0,)*6), "A'": ('A', 40, (0, 0, 0, 1, 1, 0))}
BL = np.array(sol['A']['basis']); EF = np.array([[zfloat(c) for c in e] for e in G.E])
def build(assign):
    tiles = []
    for c, Y in assign.items():
        Yn, g, w = SHAPE[Y]; t = tuple(int(x) for x in np.array(c) @ BL + np.array(w)); F, C = place(sol, Yn, g, t)
        P = np.array([np.array(v, float) @ EF for f in F for v in corners(f, 6)])
        tiles.append({'c': c, 'Y': Y, 't': t, 'F': F, 'C': C, 'ctr': P.mean(0), 'R': np.linalg.norm(P - P.mean(0), axis=1).max()})
    return tiles
def check(tiles, stop_first=False):
    nover = 0; tested = 0
    for i, j in itertools.combinations(range(len(tiles)), 2):
        a, b = tiles[i], tiles[j]
        if np.linalg.norm(a['ctr'] - b['ctr']) > a['R'] + b['R'] + 1e-6: continue
        tested += 1
        if overlaps(a['C'], b['C']):
            nover += 1
            if stop_first: break
    faces = {}
    for i, T in enumerate(tiles):
        for f, s in T['F'].items(): faces.setdefault(f, []).append((i, s))
    bad = sum(1 for v in faces.values() if len(v) > 2 or (len(v) == 2 and v[0][1] == v[1][1]))
    inner = [T for T in tiles if all(2 <= x <= n - 3 for x in T['c'])]
    matched = sum(1 for T in inner if all(len(faces[f]) == 2 for f in T['F']))
    return nover, tested, bad, len(inner), matched
pts = list(itertools.product(range(n), repeat=3))
if MODE == 'AB':
    s = {}
    for c in pts:
        l = (c[0] + c[1], c[2] + c[1])                   # the line of c in direction v = (-1, 1, -1)
        if l not in s: s[l] = random.choice('AB')
    assign = {c: s[(c[0] + c[1], c[2] + c[1])] for c in pts}
else:
    s = {k: random.choice(['A', "A'"]) for k in range(n)}
    assign = {c: s[c[2]] for c in pts}
tiles = build(assign)
nover, tested, bad, ninner, matched = check(tiles)
nA = sum(1 for v in assign.values() if v == 'A')
print('mode', MODE, 'counts', {k: sum(1 for v in assign.values() if v == k) for k in set(assign.values())})
print(f'patch {n}^3: pairs tested exactly {tested}, overlapping {nover}; bad faces {bad}; inner tiles {ninner}, all faces matched {matched}  t={time.time()-t0:.0f}s', flush=True)
# control: one switch
c0 = (n//2, n//2, n//2)
if MODE == 'AB':
    c1 = (c0[0] + 1, c0[1] - 1, c0[2] + 1)                                   # c0 - v
    bad_assign = {c: assign[c] for c in pts}; l0 = (c0[0] + c0[1], c0[2] + c0[1])
    for c in pts:                                                             # the line of c0: A at height >= c0's, B below
        if (c[0] + c[1], c[2] + c[1]) == l0: bad_assign[c] = 'A' if c[1] >= c0[1] else 'B'
else:
    bad_assign = {c: ('A' if c[2] == c0[2] and c[0] <= c0[0] else ("A'" if c[2] == c0[2] else assign[c])) for c in pts}
nov2, _, bad2, ni2, m2 = check(build(bad_assign))
control = nov2 > 0 or bad2 > 0 or m2 < ni2
print(f'control (one switch): overlaps {nov2}, bad faces {bad2}, inner tiles fully matched {m2} of {ni2}; switch detected: {control}')
json.dump({'mode': MODE, 'n': n, 'seed': int(sys.argv[4]), 'rule_parameters': {str(k): v for k, v in s.items()},
           'assign': {str(k): v for k, v in assign.items()}, 'overlaps': nover, 'pairs_tested': tested, 'bad_faces': bad,
           'inner': ninner, 'inner_matched': matched, 'control_switch_detected': control}, open(sys.argv[5], 'w'))
ok = nover == 0 and bad == 0 and ninner > 0 and matched == ninner and control and len(set(assign.values())) == 2
print('FINAL ok' if ok else 'FINAL FAIL: overlap, unmatched face, one shape only, or switch not detected')
