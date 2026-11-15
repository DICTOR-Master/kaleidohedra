#!/usr/bin/env python3
"""byzone-deep: breadth-first search over class C(n) surfaces (n axes among the six 5-fold axes; one zone per direction, every zone
k = 2(n-1) faces, every two zones crossing twice) reached from the zonotope by exact corner flips (indent / bulge at 3-valent corners;
flips keep the face count n(n-1) and every zone size). Canonical forms up to translation and the signed-permutation symmetries.
For every state: Grunbaum's non-coplanar rule (no two edge-adjacent faces in one plane), the face-pair vectors lambda_ab, their rank.
Rank <= 3 -> lattice from the lambdas (exact Z-basis), volume = |det| exactly in Z[phi], then exact cell-overlap test with the cell
set tracked along the flip path (when the tracked set is a genuine decomposition). Usage: k10_search.py n depth out.json [maxstates]."""
import sys, json, time, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from zsurf import *
t0 = time.time()
n, DEPTH, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
MAXST = int(sys.argv[4]) if len(sys.argv) > 4 else 10**7
NOTILE = len(sys.argv) > 5 and sys.argv[5] == 'notile'
G = Geo(n); syms = signed_perms(G)
print(f'n={n} k={G.k} symmetries={len(syms)}', flush=True)

def zonotope_cells(G):
    n = G.n; cells = {((0,)*n, (0, 1, 2))}
    for top in range(3, n):
        for i, j in itertools.combinations(range(top), 2):
            sg = zsign(G.D[(i, j, top)])
            off = [0]*n
            for q in range(top):
                if q not in (i, j) and sg*zsign(G.D[(i, j, q)]) > 0: off[q] = 1
            cells.add((tuple(off), (i, j, top)))
    return cells

def cells_overlap(G, c1, c2): return G.relation(c1[0], c1[1], c2[0], c2[1]) == 'cross'

def tiling_test(G, S, lam, cellcount):
    rows = [list(v) for v in lam.values()]
    B = int_rank_basis(rows)
    if len(B) != 3: return {'tiles': False, 'why': f'lambda lattice rank {len(B)}'}
    det = lattice_det(G, B); vol3 = volume3(G, S)
    if zsign(det) < 0: det = zneg(det)
    if (3*det[0], 3*det[1]) != vol3: return {'tiles': False, 'why': 'covolume != volume', 'basis': B, 'det': det, 'vol3': vol3}
    cells = list(cellcount) if all(c == 1 for c in cellcount.values()) else shell_decompose(G, S)
    if cells is None: return {'tiles': None, 'why': 'covolume = volume; no cell decomposition found, overlap undecided', 'basis': B}
    if from_cells(G, cells) != S: return {'tiles': None, 'why': 'decomposition does not reproduce the surface', 'basis': B}
    def fpos(p): return [sum(p[i]*zfloat(G.E[i][j]) for i in range(n)) for j in range(3)]
    pts = []
    for c in cells:
        for sub in itertools.product((0, 1), repeat=3):
            q = list(c[0])
            for t, d in zip(sub, c[1]): q[d] += t
            pts.append(fpos(q))
    ctr = [sum(p[j] for p in pts)/len(pts) for j in range(3)]
    R = max(sum((p[j] - ctr[j])**2 for j in range(3))**0.5 for p in pts)
    Bf = [fpos(b) for b in B]                     # rows: lattice vectors in R^3
    a, b, c = Bf
    def cross(u, v): return [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]]
    dt = sum(x*y for x, y in zip(a, cross(b, c)))
    dual = [cross(b, c), cross(c, a), cross(a, b)]          # coefficient r of x is (x . dual_r)/dt
    bound = [int(2*R*sum(x*x for x in d)**0.5/abs(dt)) + 1 for d in dual]   # rigorous: |coef| <= |x||dual|/|dt| with |x| <= 2R
    for co in itertools.product(*[range(-bd, bd + 1) for bd in bound]):
        if co == (0, 0, 0): continue
        l = tuple(sum(co[r]*B[r][i] for r in range(3)) for i in range(n))
        lf = fpos(l)
        if sum(x*x for x in lf)**0.5 > 2*R + 1e-6: continue
        for c1 in cells:
            c1s = (vadd(c1[0], l), c1[1])
            for c2 in cells:
                if cells_overlap(G, c1s, c2): return {'tiles': False, 'why': f'overlap with translate {l}', 'basis': B}
    return {'tiles': True, 'why': 'covolume = volume and no overlap with any translate within twice the circumradius', 'basis': B}

start = zonotope(G); cc0 = {c: 1 for c in zonotope_cells(G)}
assert from_cells(G, list(cc0)) == start, 'zonotope cells and surface disagree'
level = {canon(G, start, syms): (start, cc0)}; seen = set(level)
stats = []; cands = []; examples = []; rank_hist = {}; total = 0
for depth in range(DEPTH + 1):
    good = noncop = 0; nxt = {}
    for key, (S, cc) in level.items():
        info, why = analyse(G, S)
        if info is None or not in_class(G, info) or coplanar_overlap(G, S, info): continue
        good += 1; total += 1
        lam = face_pair_vectors(G, S, info)
        rk = rank_Q([list(v) for v in lam.values()]) if lam else -1
        rank_hist[rk] = rank_hist.get(rk, 0) + 1
        if info['coplanar_adjacent'] == 0:
            noncop += 1
            if len(examples) < 60: examples.append({'depth': depth, 'faces': [[list(f[0]), f[1], f[2], s] for f, s in S.items()], 'rank': rk})
        if lam and rk <= 3:
            res = {'tiles': None, 'why': 'not tested (notile run)'} if NOTILE else tiling_test(G, S, lam, cc)
            cands.append({'depth': depth, 'rank': rk, 'coplanar_adjacent': info['coplanar_adjacent'], 'test': {k: (str(v) if k in ('det', 'vol3') else v) for k, v in res.items()},
                          'faces': [[list(f[0]), f[1], f[2], s] for f, s in S.items()], 'cells': [[list(c[0]), list(c[1]), m] for c, m in cc.items()]})
        if depth < DEPTH:
            for kind, T, cell in corner_moves(G, S, info):
                kk = canon(G, T, syms)
                if kk in seen: continue
                seen.add(kk)
                cc2 = dict(cc); cc2[cell] = cc2.get(cell, 0) + (-1 if kind == 'indent' else 1)
                if cc2[cell] == 0: del cc2[cell]
                nxt[kk] = (T, cc2)
                if len(seen) > MAXST: break
    tilers = sum(1 for c in cands if c['test']['tiles'])
    stats.append({'depth': depth, 'states': len(level), 'in_class': good, 'non_coplanar': noncop, 'rank_le_3_so_far': len(cands), 'tilers_so_far': tilers})
    print(f'PROGRESS {(depth+1)/(DEPTH+1):.3f} depth={depth} states={len(level)} in_class={good} noncoplanar={noncop} rank<=3={len(cands)} tilers={tilers} t={time.time()-t0:.0f}s', flush=True)
    level = nxt
    if not level or len(seen) > MAXST: break
out = {'n': n, 'k': G.k, 'depth': DEPTH, 'symmetries': len(syms), 'levels': stats, 'rank_histogram': rank_hist, 'candidates_rank_le_3': cands[:200],
       'n_candidates': len(cands), 'n_tilers': sum(1 for c in cands if c['test']['tiles']), 'examples_noncoplanar': examples, 'states_total': total,
       'capped': len(seen) > MAXST, 'seconds': round(time.time() - t0)}
json.dump(out, open(OUT, 'w'), indent=0)
print(f'RESULT n={n} k={G.k} states={total} rank_hist={rank_hist} rank<=3={len(cands)} tilers={out["n_tilers"]} capped={out["capped"]}')
ok = (n != 5 or out['n_tilers'] >= 1) and (stats[0]['tilers_so_far'] == 0 or n < 5)
print('CONTROLS', 'n=5 needs a tiler (Grunbaum D1/D2):' if n == 5 else '', out['n_tilers'] if n == 5 else '', '| zonotope at depth 0 does not tile (n>=5):', stats[0]['tilers_so_far'] == 0)
print('FINAL ok' if ok else 'FINAL FAIL: control failed')
