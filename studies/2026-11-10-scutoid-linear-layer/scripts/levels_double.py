"""Scutoid linear layer L (DICTO 2026-11-06 / opened 11-10). 2D sketch of the three levels of one layer:
bottom = hexagonal tiling; middle = each hexagon loses one edge (brick pairing of cells: collapsed edges never touch) -> pentagons,
four cells at every collapsed point; top = the points reopen across -> hexagons again with swapped neighbours (the scutoid move).
Edges keep three directions (so prism side faces stay flat trapezoids); vertex positions solved by least squares on a periodic patch."""
import numpy as np, itertools, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import least_squares
NX, NY = 8, 8                                     # cells per row (even), rows (even); periodic
s3 = 3 ** .5
def centre(i, j): return np.array([i + 0.5 * (j % 2), j * s3 / 2])
ang = np.radians([90, 30, -30, -90, -150, 150])    # pointy-top hexagon corners
corner = lambda c, k: c + np.array([np.cos(ang[k]), np.sin(ang[k])]) / s3
# vertex identification on the periodic patch
W, Hh = NX, NY * s3 / 2
def key(p): q = np.array([p[0] % W, p[1] % Hh]); return tuple(np.round(q, 6) % np.array([W, Hh]).round(6))
V = {}; cells = []
for i, j in itertools.product(range(NX), range(NY)):
    c = centre(i, j); ids = []
    for k in range(6):
        kk = key(corner(c, k)); ids.append(V.setdefault(kk, len(V)))
    cells.append(((i, j), ids))
P0 = np.array([np.array(k) for k in sorted(V, key=V.get)])
edges = {}
for (ij, ids) in cells:
    for k in range(6):
        a, b = ids[k], ids[(k + 1) % 6]; edges.setdefault(frozenset((a, b)), []).append((ij, k))
# brick pairing: cell (i, j) with its right neighbour (i+1, j) when i is even (rows shifted alternately so collapsed edges never touch)
def right_edge(i, j):  # shared edge between (i,j) and (i+1,j): corners k=1 (30 deg) and k=2 (-30 deg) of (i,j) -> vertical edge
    ids = cells[i * NY + j][1]; return frozenset((ids[1], ids[2]))
coll = set()
for i, j in itertools.product(range(NX), range(NY)):
    if (i + (j // 2) % 2) % 2 == 0: coll.add(right_edge(i, j))   # double-row brick (11-10 pairing search): hexagons at the top
verts_used = [v for e in coll for v in e]
assert len(verts_used) == len(set(verts_used)), 'collapsed edges touch'
per_cell = [sum(1 for k in range(6) if frozenset((ids[k], ids[(k + 1) % 6])) in coll) for _, ids in cells]
assert all(n == 1 for n in per_cell), 'a cell does not lose exactly one edge'
E = list(edges); dirs = {}
for e in E:
    (ij, k) = edges[e][0]; d = corner(np.zeros(2), (k + 1) % 6) - corner(np.zeros(2), k); dirs[e] = d / np.linalg.norm(d)
# EXACT-STYLE SOLVE (11-10 redo; the first fit drifted): unknown edge LENGTHS with fixed directions; each cell closes (2 linear
# equations); collapsed edges 0; others as near 1/sqrt3 as possible: equality-constrained least squares (KKT, one linear solve).
idx = {e: n for n, e in enumerate(E)}; A = []; 
for (ij, ids) in cells:
    row = np.zeros((2, len(E)))
    for k in range(6):
        e = frozenset((ids[k], ids[(k + 1) % 6])); d = corner(np.zeros(2), (k + 1) % 6) - corner(np.zeros(2), k); d /= np.linalg.norm(d)
        row[:, idx[e]] += d
    A += [row[0], row[1]]
for e in coll:
    r = np.zeros(len(E)); r[idx[e]] = 1; A.append(r)
A = np.array(A); b = np.zeros(len(A)); m = len(E)
K = np.block([[np.eye(m), A.T], [A, np.zeros((len(A), len(A)))]]); rhs = np.concatenate([np.full(m, 1 / s3), b])
sol = np.linalg.lstsq(K, rhs, rcond=None)[0]; L = sol[:m]
others = [L[idx[e]] for e in E if e not in coll]
# LP (11-10): largest possible shortest kept edge, all edges in the three directions, every cell closing, pairs' edges zero
from scipy.optimize import linprog
nE = len(E); keep = [idx[e] for e in E if e not in coll]
c_ = np.zeros(nE + 1); c_[-1] = -1                                     # maximise t
A_ub = np.zeros((len(keep), nE + 1)); 
for r_, k in enumerate(keep): A_ub[r_, k] = -1; A_ub[r_, -1] = 1          # t - l_k <= 0
A_eq = np.hstack([A, np.zeros((len(A), 1))]); b_eq = np.zeros(len(A))
res_ = linprog(c_, A_ub=A_ub, b_ub=np.zeros(len(keep)), A_eq=A_eq, b_eq=b_eq, bounds=[(0, 1)] * nE + [(0, 1)])
print(f'LP: largest possible shortest kept edge = {res_.x[-1]:.6f} (0 means: impossible with flat side faces in three directions)')
print(f'middle level: closure residual {np.abs(A @ L).max():.2e}; shortest kept edge {min(others):.4f}; longest {max(others):.4f}')
# positions: walk edge vectors (lengths x directions) over the periodic patch, starting from vertex 0
adj = {}
for e in E:
    a, b2 = sorted(e); (ij, k) = edges[e][0]; ids = cells[ij[0] * NY + ij[1]][1]
    p, q = ids[k], ids[(k + 1) % 6]; v = dirs[e] * L[idx[e]]
    if np.linalg.norm(P0[q] - P0[p] - dirs[e] / s3) > 1e-6: continue      # edge crosses the wrap-around seam: not walked (11-10 fix)
    adj.setdefault(p, []).append((q, v)); adj.setdefault(q, []).append((p, -v))
mid = {0: np.zeros(2)}; stack = [0]
while stack:
    p = stack.pop()
    for q, v in adj[p]:
        if q not in mid: mid[q] = mid[p] + v; stack.append(q)
fig, ax = plt.subplots(1, 2, figsize=(13, 5.6))
def draw_cells(a, pos, title, hi_edges=set(), dots=False):
    for (ij, ids) in cells:
        if ij[0] in (0, NX - 1) or ij[1] in (0, NY - 1): continue          # skip the wrap-around border cells
        if pos is mid and not all(v in mid for v in ids): continue
        c0 = mid[ids[0]] if pos is mid else corner(centre(*ij), 0)
        pts = [c0]
        for k in range(6):
            e = frozenset((ids[k], ids[(k + 1) % 6])); d = corner(np.zeros(2), (k + 1) % 6) - corner(np.zeros(2), k); d /= np.linalg.norm(d)
            nxt = pts[-1] + d * (L[idx[e]] if pos is mid else 1 / s3)
            a.plot(*np.array([pts[-1], nxt]).T, color='crimson' if e in hi_edges else 'k', lw=2.4 if e in hi_edges else 0.9)
            if dots and e in coll: a.plot(*pts[-1], 'o', color='crimson', ms=5)
            pts.append(nxt)
    a.set_aspect('equal'); a.axis('off'); a.set_title(title, fontsize=11)
    a.text(0.99, 0.01, 'DICTO', transform=a.transAxes, ha='right', fontsize=8, color='0.4')
hexpos = {v: P0[v] for v in range(len(P0))}
# hexagon panel: positions from the regular tiling, but drawn cell by cell from the first corner
for (ij, ids) in cells: pass
draw_cells(ax[0], None, 'bottom: hexagonal prisms\n(red edges shrink to points going up)', coll)
draw_cells(ax[1], mid, 'middle: every cell a pentagon (pentagonal prisms)\n(red dots: four cells meet)', dots=True)
fig.suptitle('Scutoid linear layer L: hexagons to pentagons (double-row pairing: hexagons again at the top)', fontsize=13)
plt.tight_layout(); plt.savefig('l-levels-double-row.png', dpi=130)
ok = all(n == 1 for n in per_cell) and np.abs(A @ L).max() < 1e-9 and min(others) > 1e-6
print('FINAL ok' if ok else 'FINAL FAIL: pentagon level not realised with positive edges')
