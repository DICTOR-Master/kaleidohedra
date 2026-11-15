#!/usr/bin/env python3
"""Exact lattice-tiling check for candidate surfaces (rank-3 face-pair lattices) from k10_search.py output.
1. covolume |det Lambda| = volume, exact in Z[phi];
2. a cell decomposition: the cells tracked along the flip path when they form a genuine set, else exact peeling (zsurf.shell_decompose);
   the decomposition must reproduce the surface exactly;
3. no two cells of P and P + l overlap (exact separating-axis test on the 15 normals, vectorised in integers), for every lattice vector
   l with |l| <= 2R (R = circumradius of P about its corner centroid; the coefficient box comes from the dual basis, so no l is missed).
P tiles by translation with lattice Lambda iff 1 and 3 hold (a packing of density 1 by a closed set is a tiling).
Usage: tile_check.py search.json out.json"""
import sys, json, itertools, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from zsurf import *
t0 = time.time()
src, OUT = sys.argv[1], sys.argv[2]
d = json.load(open(src))
if 'candidates_rank_le_3' not in d:      # gnomon.py output: surfaces only
    d = {'n': 6, 'candidates_rank_le_3': [{'faces': f, 'cells': []} for f in d['rank_le_3_surfaces']]}
n = d['n']; G = Geo(n)
PR = G.pairs
Dx = np.array([[G.D[(x, y, i)][0] for (x, y) in PR] for i in range(n)], dtype=np.int64)   # n x 15
Dy = np.array([[G.D[(x, y, i)][1] for (x, y) in PR] for i in range(n)], dtype=np.int64)
def sign_arr(x, y):
    a, b = 2*x + y, y
    s = np.where((a >= 0) & (b >= 0), np.where((a == 0) & (b == 0), 0, 1), 0)
    s = np.where((a <= 0) & (b <= 0) & ~((a == 0) & (b == 0)), -1, s)
    mixed = ((a > 0) & (b < 0)) | ((a < 0) & (b > 0))
    s = np.where(mixed, np.where(a*a > 5*b*b, np.sign(a), np.sign(b)), s)
    return s
def intervals(cells):
    """lo, hi as (x, y) integer arrays, shape cells x 15"""
    P = np.array([c[0] for c in cells], dtype=np.int64)
    bx, by = P @ Dx, P @ Dy
    lox, loy, hix, hiy = bx.copy(), by.copy(), bx.copy(), by.copy()
    for ci, c in enumerate(cells):
        for dd in c[1]:
            vx, vy = Dx[dd], Dy[dd]; pos = sign_arr(vx, vy) > 0
            hix[ci] += np.where(pos, vx, 0); hiy[ci] += np.where(pos, vy, 0)
            lox[ci] += np.where(pos, 0, vx); loy[ci] += np.where(pos, 0, vy)
    return lox, loy, hix, hiy
def fpos(p): return np.array([sum(p[i]*zfloat(G.E[i][j]) for i in range(n)) for j in range(3)])
res = []
for ci, c in enumerate(d['candidates_rank_le_3']):
    S = {(tuple(f[0]), f[1], f[2]): f[3] for f in c['faces']}
    info, _ = analyse(G, S); lam = face_pair_vectors(G, S, info)
    B = int_rank_basis([list(v) for v in lam.values()])
    det = lattice_det(G, B); det = det if zsign(det) > 0 else zneg(det); vol3 = volume3(G, S)
    r = {'index': ci, 'basis': B, 'det': det, 'vol3': vol3, 'covolume_eq_volume': (3*det[0], 3*det[1]) == vol3}
    cc = {tuple([tuple(x[0]), tuple(x[1])]): x[2] for x in c['cells']}
    tracked = bool(cc) and all(v == 1 for v in cc.values())
    cells = list(cc) if tracked else shell_decompose(G, S, 200000)
    r['decomposition'] = None if cells is None else ('tracked' if tracked else 'peeled')
    if cells is not None and any(G.relation(c1[0], c1[1], c2[0], c2[1]) == 'cross' for c1, c2 in itertools.combinations(cells, 2)):
        r['tiles'] = None; r['why'] = 'decomposition cells overlap (surface not embedded)'; res.append(r); continue
    if cells is None or from_cells(G, cells) != S:
        r['tiles'] = None; r['why'] = 'no exact cell decomposition'; res.append(r); continue
    r['cells'] = [[list(x[0]), list(x[1])] for x in cells]
    r['cell_types'] = sorted(''.join(map(str, x[1])) for x in cells)
    if not r['covolume_eq_volume']: r['tiles'] = False; r['why'] = 'covolume != volume'; res.append(r); continue
    pts = []
    for x in cells:
        for sub in itertools.product((0, 1), repeat=3):
            q = list(x[0])
            for t, dd in zip(sub, x[1]): q[dd] += t
            pts.append(fpos(q))
    pts = np.array(pts); ctr = pts.mean(0); R = np.linalg.norm(pts - ctr, axis=1).max()
    Bf = np.array([fpos(b) for b in B]); dual = np.linalg.inv(Bf).T      # coefficient of x = x . dual_r
    bound = [int(2*R*np.linalg.norm(dual[k])) + 1 for k in range(3)]
    A = intervals(cells); bad = None; tested = 0
    for co in itertools.product(*[range(-b, b + 1) for b in bound]):
        if co == (0, 0, 0): continue
        l = [sum(co[k]*B[k][i] for k in range(3)) for i in range(n)]
        if np.linalg.norm(fpos(l)) > 2*R + 1e-6: continue
        tested += 1
        sh = [(tuple(np.add(x[0], l)), x[1]) for x in cells]; Bi = intervals(sh)
        # cells i (P) vs j (P + l): separated on some axis weakly?
        lox, loy, hix, hiy = A; lx2, ly2, hx2, hy2 = Bi
        g1 = sign_arr(lx2[None, :, :] - hix[:, None, :], ly2[None, :, :] - hiy[:, None, :])   # lo_j - hi_i
        g2 = sign_arr(lox[:, None, :] - hx2[None, :, :], loy[:, None, :] - hy2[None, :, :])   # lo_i - hi_j
        sep = ((g1 >= 0) | (g2 >= 0)).any(axis=2)
        if not sep.all():
            i, j = np.argwhere(~sep)[0]; bad = {'translate': l, 'cell_P': list(map(list, cells[i])), 'cell_translate': list(map(list, sh[j]))}; break
    r['translates_tested'] = tested
    r['tiles'] = bad is None; r['why'] = 'covolume = volume and no overlap with any translate within 2R' if bad is None else f'overlap {bad}'
    res.append(r); print(f'candidate {ci}: tiles={r["tiles"]} translates={tested} {r["why"][:120]} t={time.time()-t0:.0f}s', flush=True)
json.dump({'n': n, 'results': res}, open(OUT, 'w'), indent=0, default=str)
print('RESULT tilers:', sum(1 for r in res if r.get('tiles')), 'of', len(res))
print('FINAL ok' if len(res) == len(d['candidates_rank_le_3']) else 'FINAL FAIL: not every candidate decided or recorded')
