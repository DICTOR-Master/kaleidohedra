#!/usr/bin/env python3
"""Inchbald's dimpled rhombic triacontahedron vs the k = 10 solids of study 2026-11-15-grunbaum-k10.
1. Build T, indent four alternating cube-corner 3-valent corners (tetrahedral), compare with candidates 0-2 up to the
   120 symmetries of the six-axis star and translation (exact, in Z^6 face form).
2. Cells: a fine tiling of T by lifting (verified exactly); every fine tiling of T holds the cell at each 3-valent corner,
   so the solid is the other cells. Writes a tile_check.py input.
Usage: inchbald.py <grunbaum-k10 dir> <out dir>"""
import sys, json, itertools, random
import numpy as np
K10, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, K10 + '/scripts')
from zsurf import *
G = Geo(6); n = 6
E = np.array([[zfloat(c) for c in e] for e in G.E])
T = zonotope(G); info, why = analyse(G, T)
pos = lambda v: np.array(v, float) @ E
cen = pos([1]*6) / 2
three = [v for v, fs in info['Vmap'].items() if len(fs) == 3]
print('T: faces', len(T), 'vertices', len(info['Vmap']), '3-valent', len(three))
cube = []
for v in three:
    d = pos(v) - cen; d /= np.abs(d).max()
    if np.allclose(np.abs(d), 1, atol=1e-9): cube.append((v, tuple(np.sign(d).astype(int))))
print('cube-corner 3-valent corners', len(cube))
even = [v for v, s in cube if np.prod(s) > 0]; odd = [v for v, s in cube if np.prod(s) < 0]
def indent_at(S, v):
    """indent the 3-valent corner v itself: the move whose cell has v as a corner and removes v from the surface"""
    inf, _ = analyse(G, S)
    for kind, S2, cell in corner_moves(G, S, inf):
        if kind != 'indent': continue
        inf2, _ = analyse(G, S2)
        if tuple(v) in inf['Vmap'] and tuple(v) not in inf2['Vmap']: return S2, cell
    return None, None
def nsym(S):
    c = canon_t(S); return sum(1 for s in syms if canon_t(apply_sym(G, S, s)) == c)
syms = signed_perms(G)
res = {}
for name, four in (('even', even), ('odd', odd)):
    S = dict(T); removed = []
    for v in four:
        S, cell = indent_at(S, v)
        assert S is not None, 'indent failed'
        removed.append(cell)
    res[name] = (S, removed)
    inf, why = analyse(G, S); print(name, 'faces', len(S), 'analyse', why, 'symmetries', nsym(S), 'removed', removed)
d = json.load(open(K10 + '/data/search6.json'))
cands = [{(tuple(f[0]), f[1], f[2]): f[3] for f in c['faces']} for c in d['candidates_rank_le_3'][:3]]
print('symmetry group', len(syms)); print('candidate symmetries', [nsym(C) for C in cands])
Sinch = res['even'][0]
match = {}
for i, C in enumerate(cands):
    cc = canon_t(C)
    match[i] = any(canon_t(apply_sym(G, Sinch, s)) == cc for s in syms)
print('Inchbald congruent to candidate:', match)
# lifting tiling of T
pairs_ok = None
for trial in range(50):
    h = [random.random() for _ in range(n)]
    W = np.hstack([E, np.array(h)[:, None]])
    for s in (1, -1):
        cells = []
        for t in itertools.combinations(range(n), 3):
            d3 = np.linalg.det(E[list(t)])
            q = [0]*n
            for l in range(n):
                if l in t: continue
                d4 = np.linalg.det(W[list(t) + [l]])
                if np.sign(d4) * np.sign(d3) * s > 0: q[l] = 1
            cells.append((tuple(q), t))
        if from_cells(G, cells) == T and not any(G.relation(a[0], a[1], b[0], b[1]) == 'cross' for a, b in itertools.combinations(cells, 2)):
            pairs_ok = cells; break
    if pairs_ok: break
assert pairs_ok, 'no lifting tiling'
print('T tiling: 20 cells, exact surface and no crossing: ok')
rem = {(tuple(c[0]), tuple(c[1])) for c in res['even'][1]}
tilecells = {(tuple(c[0]), tuple(c[1])) for c in pairs_ok}
print('removed corner cells all in the tiling:', rem <= tilecells)
keep = [c for c in pairs_ok if (tuple(c[0]), tuple(c[1])) not in rem]
print('cells kept', len(keep), 'surface reproduced exactly:', from_cells(G, keep) == Sinch)
types = sorted(''.join(map(str, c[1])) for c in keep)
# shift to the candidate's own position if congruent by pure translation; else write Inchbald's own
cand = next((i for i, m in match.items() if m), None)
basis = d['candidates_rank_le_3'][cand]['test']['basis'] if cand is not None else None
out = {'n': 6, 'note': "Inchbald's tetrahedrally dimpled rhombic triacontahedron (even cube corners), cells from a lifting tiling of T",
       'match': match, 'cell_types': types,
       'candidates_rank_le_3': [{'faces': [[list(f[0]), f[1], f[2], s] for f, s in Sinch.items()], 'cells': [[list(c[0]), list(c[1]), 1] for c in keep]}]}
json.dump(out, open(OUT + '/inchbald.json', 'w'))
print('cell types', types)
print('FINAL ok' if match == {0: False, 1: False, 2: True} else 'FINAL FAIL: Inchbald solid not matched to exactly one candidate')
