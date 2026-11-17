#!/usr/bin/env python3
"""Exact finite patches of layer-stacked tilings (evidence for the layer theorem of layers.py).
Plane: ker h with h = (1, 0, -1) in GET's lattice basis b1, b2, b3 (h(b1) = 1, so b1 steps one layer up; ker h = <b2, b1 + b3>).
Layer fillings of one slab (from layers.json, all exact swaps of the layer type 'A, identity image, h = (1, 0, -1)'):
   A: GET A + ker h;   B: GET B + ker h (w = 0);   C: Inchbald's solid in the image C g_C, shifted by w_C, + ker h.
A patch = layers k = 0..K-1, layer k filled by word[k], each with tiles at u2*b2 + u3*(b1 + b3), 0 <= u2, u3 < M, shifted by k*b1.
Checks (exact): (1) no two tiles overlap (mixlib.overlaps: separating axis on cells, exact Q(phi) volumes for Inchbald's solid);
(2) face to face: every face lies on at most two tiles, with opposite sides; every tile of the inner region (layers 1..K-2,
plane box 1..M-2) has all 30 faces matched by a face of another tile of the patch.
Usage: patch.py <k10 dir> <inchbald json> <layers json> <word> <M> <out json>"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
t0 = time.time()
sol = load_solids(sys.argv[1], sys.argv[2]); LY = json.load(open(sys.argv[3])); WORD = sys.argv[4]; M = int(sys.argv[5])
LT = LY['layer_types']; BL = np.array(sol['A']['basis'])
U = next(k for k, L in enumerate(LT) if L['Y'] == 'A' and L['g'] == IDENT and tuple(L['h']) == (1, 0, -1))
fill = {'A': (IDENT, (0,)*6)}
for sw in LY['swaps']:
    for a, b, sg in ((sw['U'], sw['V'], 1), (sw['V'], sw['U'], -1)):
        if a == U and LT[b]['Y'] not in fill:
            fill[LT[b]['Y']] = (LT[b]['g'], tuple(sg*x for x in sw['w']))
        elif a == U and LT[b]['Y'] == 'B' and LT[b]['g'] == IDENT: fill['B'] = (IDENT, tuple(sg*x for x in sw['w']))
print('slab fillings for the plane h = (1, 0, -1):', fill)
assert all(c in fill for c in set(WORD)), 'a letter of the word has no filling of this slab'
b1, b2, b3 = BL
tiles = []
for k, ch in enumerate(WORD):
    g, w = fill[ch]
    for u2 in range(M):
        for u3 in range(M):
            t = tuple(int(x) for x in np.array(w) + k*b1 + u2*b2 + u3*(b1 + b3))
            F, C = place(sol, ch, g, t)
            tiles.append({'Y': ch, 'g': g, 't': t, 'k': k, 'u': (u2, u3), 'F': F, 'C': C})
EF = np.array([[zfloat(c) for c in e] for e in G.E])
for T in tiles:
    P = np.array([np.array(v, float) @ EF for f in T['F'] for v in corners(f, 6)]); T['c'] = P.mean(0); T['R'] = np.linalg.norm(P - T['c'], axis=1).max()
nover = 0; tested = 0
for i, j in itertools.combinations(range(len(tiles)), 2):
    a, b = tiles[i], tiles[j]
    if np.linalg.norm(a['c'] - b['c']) > a['R'] + b['R'] + 1e-6: continue
    tested += 1
    if overlaps(a['C'], b['C']): nover += 1; print('OVERLAP', a['Y'], a['k'], a['u'], b['Y'], b['k'], b['u'])
print('tiles', len(tiles), 'pairs within bounding spheres tested exactly', tested, 'overlapping', nover, f't={time.time()-t0:.0f}s', flush=True)
faces = {}
for i, T in enumerate(tiles):
    for f, s in T['F'].items(): faces.setdefault(f, []).append((i, s))
bad_faces = sum(1 for v in faces.values() if len(v) > 2 or (len(v) == 2 and v[0][1] == v[1][1]))
inner = [i for i, T in enumerate(tiles) if 1 <= T['k'] <= len(WORD) - 2 and all(1 <= x <= M - 2 for x in T['u'])]
inner_ok = sum(1 for i in inner if all(len(faces[f]) == 2 for f in tiles[i]['F']))
print('faces on more than two tiles or with equal sides:', bad_faces, '; inner tiles', len(inner), 'with all 30 faces matched', inner_ok)
json.dump({'word': WORD, 'M': M, 'fill': {k: [v[0], list(v[1])] for k, v in fill.items()},
           'tiles': [{'Y': T['Y'], 'g': T['g'], 't': list(T['t']), 'k': T['k'], 'u': list(T['u'])} for T in tiles],
           'overlaps': nover, 'pairs_tested': tested, 'inner': len(inner), 'inner_matched': inner_ok}, open(sys.argv[6], 'w'))
ok = nover == 0 and bad_faces == 0 and len(inner) > 0 and inner_ok == len(inner)
print('FINAL ok' if ok else 'FINAL FAIL: overlap or unmatched face in the patch')
