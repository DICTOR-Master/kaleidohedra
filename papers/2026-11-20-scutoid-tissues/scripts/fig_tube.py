# Figure 4: one cell of the 120-cell as a cell tube in space-time, swept in two generic directions.
# Exact geometry: the 120-cell by Wythoff's construction (the routine of studies/2026-11-15-tissue-null-models/scripts/sweeps.py)
# and Qhull. Asserted here: 600 corners, 1200 edges, 120 cells of 20 corners; in each direction the whole sweep has corner indices
# (1, 116, 366, 116, 1) (#104 Theorem 2); the chosen cell has exactly one lowest corner (index 1, its birth) and one highest
# (index 3, its death); its section gains one side at each corner with one of its own edges below and loses one at each corner
# with two below, starting and ending as a triangle; every drawn section is a convex polygon.
# Writes the checks and the drawing data (the cell's corners, edges, walls, events and sections in each direction) to OUT.json;
# fig_scenes.py renders Figure 4 from it.   Usage: python3 fig_tube.py OUT.json        (run on a compute host)
import sys, json
import numpy as np
from scipy.spatial import ConvexHull, cKDTree

OUT_JSON = sys.argv[1]
CHECKS = []


def check(name, ok, info=''):
    CHECKS.append([name, bool(ok), str(info)])
    print(('PASS ' if ok else 'FAIL ') + name + ' ' + str(info), flush=True)


def wythoff(m, ring):
    k = len(ring)
    G = np.array([[1.0 if i == j else -np.cos(np.pi / m[i][j]) for j in range(k)] for i in range(k)])
    Rt = np.linalg.cholesky(G)
    x = np.linalg.solve(Rt, np.array([1.0 if r else 0.0 for r in ring]))
    pts = {tuple(np.round(x, 6)): x}
    front = [x]
    while front:
        nf = []
        for p in front:
            for r in Rt:
                q = p - 2 * (r @ p) * r
                key = tuple(np.round(q, 6))
                if key not in pts:
                    pts[key] = q; nf.append(q)
        front = nf
    return np.array(list(pts.values()))


m = [[1, 5, 2, 2], [5, 1, 3, 2], [2, 3, 1, 3], [2, 2, 3, 1]]
V = wythoff(m, (1, 0, 0, 0))
V = V / np.linalg.norm(V, axis=1).max()
check('120-cell: 600 corners', len(V) == 600, len(V))
hull = ConvexHull(V)
eq = np.round(hull.equations, 6)
uniq, fac = np.unique(eq, axis=0, return_inverse=True)
fac = fac.ravel()
cells = {}
for s, f in zip(hull.simplices, fac):
    cells.setdefault(int(f), set()).update(int(v) for v in s)
check('120 cells of 20 corners', len(cells) == 120 and all(len(c) == 20 for c in cells.values()))
normal = {f: uniq[f][:4] / np.linalg.norm(uniq[f][:4]) for f in cells}
tree = cKDTree(V)
d, _ = tree.query(V, k=2)
dmin = d[:, 1].min()
E = sorted(tree.query_pairs(dmin * (1 + 1e-6)))
nbr = {i: [] for i in range(len(V))}
for a, b in E:
    nbr[a].append(b); nbr[b].append(a)
check('1200 edges, four at every corner', len(E) == 1200 and all(len(n) == 4 for n in nbr.values()), len(E))

rng = np.random.default_rng(20261120)
U = []
for _ in range(2):
    u = rng.normal(size=4); U.append(u / np.linalg.norm(u))


def census(u):
    h = V @ u
    gap = min(abs(h[a] - h[b]) for a, b in E)
    idx = np.array([sum(h[j] < h[i] for j in nbr[i]) for i in range(len(V))])
    return h, idx, [int((idx == k).sum()) for k in range(5)], gap


for k, u in enumerate(U):
    h, idx, hist, gap = census(u)
    check('direction %d: corner indices (1, 116, 366, 116, 1)' % (k + 1), hist == [1, 116, 366, 116, 1], hist)
    check('direction %d generic: no edge level' % (k + 1), gap > 1e-6, gap)

# the cell: the one whose centre is most nearly at right angles to both directions (it lives in the middle of both sweeps)
cent = {f: V[sorted(c)].mean(0) for f, c in cells.items()}
C = min(cells, key=lambda f: abs(cent[f] @ U[0]) / np.linalg.norm(cent[f]) + abs(cent[f] @ U[1]) / np.linalg.norm(cent[f]))
CV = sorted(cells[C])
CE = [(a, b) for a, b in E if a in cells[C] and b in cells[C]]
check('the cell has 30 edges, three of them at each corner', len(CE) == 30 and all(sum(v in e for e in CE) == 3 for v in CV))
# its 12 walls: corners shared with each neighbouring cell
walls = []
for f, c in cells.items():
    if f != C and len(c & cells[C]) == 5:
        walls.append(sorted(c & cells[C]))
check('12 pentagonal walls', len(walls) == 12)

# local coordinates in the cell's hyperplane
n = normal[C]
B = np.linalg.svd(np.outer(n, n))[0][:, 1:]    # orthonormal basis of the hyperplane


def frame(u):
    t = u - (u @ n) * n; t /= np.linalg.norm(t)
    a = B[:, 0] - (B[:, 0] @ t) * t; a /= np.linalg.norm(a)
    b = B[:, 1] - (B[:, 1] @ t) * t - (B[:, 1] @ a) * a
    if np.linalg.norm(b) < 1e-6:
        b = B[:, 2] - (B[:, 2] @ t) * t - (B[:, 2] @ a) * a
    b /= np.linalg.norm(b)
    return a, b, t


def classify(u):
    h = V @ u
    ev = {}
    for v in CV:
        own = [w for w in nbr[v] if w in cells[C]]
        out = [w for w in nbr[v] if w not in cells[C]]
        j = sum(h[w] < h[v] for w in own)
        i = j + sum(h[w] < h[v] for w in out)
        if j == 0: kind = 'birth'
        elif j == 3: kind = 'death'
        else: kind = {1: 'neighbour born', 2: 'swap', 3: 'neighbour dies'}[i]
        ev[v] = (kind, i, j)
    return h, ev


def section(h, level):
    pts = []
    for a, b in CE:
        if (h[a] - level) * (h[b] - level) < 0:
            s = (level - h[a]) / (h[b] - h[a]); pts.append(V[a] + s * (V[b] - V[a]))
    return np.array(pts)


def convex_order(P, a, b):
    c = P.mean(0)
    ang = np.arctan2((P - c) @ b, (P - c) @ a)
    return P[np.argsort(ang)]


RC = max(np.linalg.norm(V[v] - cent[C]) for v in CV)
SC = 0.6 / RC     # drawing scale: the cell's circumradius becomes 0.6
RES = {'cell_corners': 20, 'cell_walls': 12, 'directions': []}
FR = (0.1, 0.3, 0.5, 0.7, 0.9)       # the drawn sections, as fractions of the cell's life
for k, u in enumerate(U):
    h, ev = classify(u)
    kinds = [ev[v][0] for v in CV]
    check('direction %d: one birth corner (index 1) and one death corner (index 3)' % (k + 1),
          kinds.count('birth') == 1 and kinds.count('death') == 1 and
          all(ev[v][1] == 1 for v in CV if ev[v][0] == 'birth') and all(ev[v][1] == 3 for v in CV if ev[v][0] == 'death'))
    order = sorted(CV, key=lambda v: h[v])
    check('direction %d: birth lowest, death highest' % (k + 1), ev[order[0]][0] == 'birth' and ev[order[-1]][0] == 'death')
    a, b, t = frame(u)
    sides, seq, pred, ok_conv = 3, [], [], True
    for v0, v1 in zip(order[:-1], order[1:]):
        if v0 != order[0]:
            sides += 1 if ev[v0][2] == 1 else -1
        P = section(h, 0.5 * (h[v0] + h[v1]))
        Q = np.c_[(P - cent[C]) @ a, (P - cent[C]) @ b]
        ok_conv &= len(ConvexHull(Q).vertices) == len(Q)
        seq.append(len(P)); pred.append(sides)
    check('direction %d: section sides follow the corners (+1 at one own edge below, -1 at two)' % (k + 1),
          seq == pred and seq[0] == 3 and seq[-1] == 3 and len(seq) == 19, seq)
    check('direction %d: every section a convex polygon' % (k + 1), ok_conv)
    cnt = {kk: kinds.count(kk) for kk in ('birth', 'swap', 'neighbour born', 'neighbour dies', 'death')}
    h0, h1 = h[order[0]], h[order[-1]]
    levels = [h0 + f * (h1 - h0) for f in FR]
    check('direction %d: drawn sections avoid the corner levels' % (k + 1), min(abs(l - h[v]) for l in levels for v in CV) > 1e-6)
    # the drawing data (rendered by fig_scenes.py): the cell in its own 3-space, time along the third axis, circumradius 0.6
    loc = lambda p: (SC * np.array([(p - cent[C]) @ a, (p - cent[C]) @ b, (p - cent[C]) @ t])).round(6).tolist()
    secs = []
    for l in levels:
        P = section(h, l); Q = np.c_[(P - cent[C]) @ a, (P - cent[C]) @ b]; c2 = Q.mean(0)
        P = P[np.argsort(np.arctan2(Q[:, 1] - c2[1], Q[:, 0] - c2[0]))]
        secs.append([loc(p) for p in P])
    RES['directions'].append({'counts': cnt, 'sides': seq, 'corners': [loc(V[v]) for v in CV], 'kind': kinds,
                              'edges': [[CV.index(x), CV.index(y)] for x, y in CE], 'walls': [[CV.index(v) for v in w] for w in walls],
                              'order': [CV.index(v) for v in order], 'time': [float((h[v] - h0) / (h1 - h0)) for v in order],
                              'sections': secs, 'levels': list(FR)})
    print('DIR', k + 1, cnt, seq, flush=True)
check('cell circumradius / edge = sqrt(3)(1 + sqrt5)/4 (regular dodecahedron)', abs(RC / dmin - 3 ** 0.5 * (1 + 5 ** 0.5) / 4) < 1e-9, RC / dmin)
RES['checks'] = CHECKS
json.dump(RES, open(OUT_JSON, 'w'), indent=1)
nf = sum(not c[1] for c in CHECKS)
print('%d checks, %d failed' % (len(CHECKS), nf))
print('FINAL ok' if nf == 0 else 'FINAL FAIL')
sys.exit(1 if nf else 0)
