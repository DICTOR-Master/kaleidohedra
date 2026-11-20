# Figure 1: one cell of the 120-cell as a cell tube in space-time, swept in two generic directions.
# Exact geometry: the 120-cell by Wythoff's construction (the routine of studies/2026-11-15-tissue-null-models/scripts/sweeps.py)
# and Qhull. Asserted here: 600 corners, 1200 edges, 120 cells of 20 corners; in each direction the whole sweep has corner indices
# (1, 116, 366, 116, 1) (#104 Theorem 2); the chosen cell has exactly one lowest corner (index 1, its birth) and one highest
# (index 3, its death); its section gains one side at each corner with one of its own edges below and loses one at each corner
# with two below, starting and ending as a triangle; every drawn section is a convex polygon.
# Usage: python3 fig_tube.py OUT.png OUT.json        (run on a compute host)
import sys, json
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

OUT_PNG, OUT_JSON = sys.argv[1], sys.argv[2]
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
VIOLET = '#8a5cc4'; GROUND = '#14100d'; SAND = '#d9c7a3'; WHITE = '#f2efe6'; GREY = '#8c8c8c'; TEXT = '#efe9dc'; SUB = '#b9b0a0'
fig = plt.figure(figsize=(13, 9.4), dpi=220, facecolor=GROUND)
fig.text(0.05, 0.945, 'One cell, swept in two directions', color=TEXT, fontsize=24, fontweight='bold')
fig.text(0.05, 0.905, 'A dodecahedral cell of the 120-cell as a tube in space-time: born at its lowest corner, '
         'dead at its highest, its section changing at every corner between', color=SUB, fontsize=11.5)
fig.text(0.95, 0.955, 'DICTO · dictospheres.com', color=SUB, fontsize=11, ha='right')
FR = (0.1, 0.3, 0.5, 0.7, 0.9)       # the drawn sections, as fractions of the cell's life
def marker(ax, s, kind, big=1.0, **kw):
    if kind in ('birth', 'death'):
        ax.plot(*s, marker='^' if kind == 'birth' else 'v', ms=15 * big, color=WHITE, mec=GROUND, mew=1.2, zorder=10, **kw)
    elif kind == 'swap':
        ax.plot(*s, marker='D', ms=8.5 * big, color=SAND, mec=GROUND, mew=1.0, zorder=10, **kw)
    else:
        ax.plot(*s, marker='o', ms=8 * big, color=GROUND, mec=GREY, mew=1.8, zorder=10, **kw)
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
    RES['directions'].append({'counts': cnt, 'sides': seq})
    print('DIR', k + 1, cnt, seq, flush=True)
    h0, h1 = h[order[0]], h[order[-1]]
    levels = [h0 + f * (h1 - h0) for f in FR]
    check('direction %d: drawn sections avoid the corner levels' % (k + 1), min(abs(l - h[v]) for l in levels for v in CV) > 1e-6)

    # drawing: orthographic, time up, camera turned about time and tilted down
    X = {v: SC * np.array([(V[v] - cent[C]) @ a, (V[v] - cent[C]) @ b, (V[v] - cent[C]) @ t]) for v in CV}
    az, el = np.radians(28 + 40 * k), np.radians(10)
    def proj(p):
        x = p[0] * np.cos(az) - p[1] * np.sin(az)
        dpt = p[0] * np.sin(az) + p[1] * np.cos(az)
        return np.array([x, p[2] * np.cos(el) + dpt * np.sin(el)])
    view = np.array([np.sin(az) * np.cos(el), np.cos(az) * np.cos(el), -np.sin(el)])
    ax = fig.add_axes([0.02 + 0.49 * k, 0.30, 0.47, 0.55]); ax.set_facecolor(GROUND); ax.set_aspect('equal'); ax.axis('off')
    light = np.array([-0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    polys = []
    for w in walls:
        P = np.array([X[v] for v in w]); c = P.mean(0)
        nn = np.cross(P[1] - P[0], P[2] - P[0]); nn /= np.linalg.norm(nn)
        if nn @ c < 0: nn = -nn
        e1 = (P[0] - c) / np.linalg.norm(P[0] - c)
        P = convex_order(P, e1, np.cross(nn, e1))
        polys.append((nn @ view < 0, P, nn))
    def draw_face(P, nn, front):
        S = np.array([proj(p) for p in P])
        shade = 0.45 + 0.55 * max(0.0, nn @ light)
        rgb = np.clip(np.array(matplotlib.colors.to_rgb(VIOLET)) * shade, 0, 1)
        ax.add_patch(Polygon(S, closed=True, facecolor=rgb, alpha=0.16 if front else 0.42, edgecolor='none', zorder=6 if front else 2))
    for front, P, nn in polys:
        if not front: draw_face(P, nn, front)
    for x, y in CE:
        fr = any(front and min(np.linalg.norm(P - X[x], axis=1)) < 1e-9 and min(np.linalg.norm(P - X[y], axis=1)) < 1e-9 for front, P, nn in polys)
        S = np.array([proj(X[x]), proj(X[y])])
        ax.plot(S[:, 0], S[:, 1], color='#d8c8f0' if fr else '#7a6498', lw=2.0 if fr else 1.1, zorder=7 if fr else 3, solid_capstyle='round')
    for l in levels:
        P = section(h, l)
        P3 = SC * np.array([[(p - cent[C]) @ a, (p - cent[C]) @ b, (p - cent[C]) @ t] for p in P])
        P3 = convex_order(P3, np.array([1.0, 0, 0]), np.array([0, 1.0, 0]))
        S = np.array([proj(p) for p in P3])
        ax.add_patch(Polygon(S, closed=True, facecolor=SAND, alpha=0.30, edgecolor=SAND, lw=1.6, zorder=5))
        ax.plot([S[:, 0].max() + 0.02, 0.74], [S[:, 1].mean()] * 2, color='#5a5246', lw=0.8, zorder=1)
        ax.text(0.76, S[:, 1].mean(), '%d sides' % len(P), color=SAND, fontsize=9.5, va='center', ha='left', zorder=11)
    for front, P, nn in polys:
        if front: draw_face(P, nn, front)
    for v in sorted(CV, key=lambda v: ev[v][0] in ('birth', 'death')):   # birth and death drawn last, on top
        marker(ax, proj(X[v]), ev[v][0])
    ax.annotate('', xy=(-0.98, 0.5), xytext=(-0.98, -0.5), arrowprops=dict(arrowstyle='->', color=SUB, lw=1.4))
    ax.text(-1.03, 0, 'time = direction %d' % (k + 1), color=SUB, fontsize=10.5, rotation=90, va='center', ha='right')
    ax.set_xlim(-1.2, 1.15); ax.set_ylim(-0.78, 0.78)
    # the life of the section: sides against time, with the corners where it changes
    bx = fig.add_axes([0.09 + 0.49 * k, 0.11, 0.37, 0.17]); bx.set_facecolor(GROUND)
    T = [(h[v] - h0) / (h1 - h0) for v in order]
    xs, ys = [], []
    for i in range(19):
        xs += [T[i], T[i + 1]]; ys += [seq[i], seq[i]]
    bx.plot(xs, ys, color=SAND, lw=2.0)
    for f in FR:
        bx.axvline(f, color='#5a5246', lw=0.9, ls='--', zorder=0)
    for v, x in sorted(zip(order, T), key=lambda q: ev[q[0]][0] in ('birth', 'death')):
        marker(bx, (x, 1.6), ev[v][0], big=0.62, clip_on=False)
    bx.set_ylim(1.0, 10.2); bx.set_xlim(-0.02, 1.02); bx.set_yticks([3, 5, 7, 9])
    bx.tick_params(colors=SUB, labelsize=9); bx.set_xticks([])
    for sp in bx.spines.values(): sp.set_color('#5a5246')
    bx.set_ylabel('sides', color=SUB, fontsize=10)
    bx.set_xlabel('time, from birth to death', color=SUB, fontsize=10)
    c = cnt
    fig.text(0.275 + 0.49 * k, 0.035, 'direction %d: 1 birth, %d swaps, %d neighbours born, %d dying, 1 death'
             % (k + 1, c['swap'], c['neighbour born'], c['neighbour dies']), color=TEXT, fontsize=11, ha='center')
# legend
lx = 0.06
for mk, col, mec, lab in (('^', WHITE, GROUND, 'birth (lowest corner)'), ('D', SAND, GROUND, 'swap'),
                          ('o', GROUND, GREY, 'a neighbour born or dying'), ('v', WHITE, GROUND, 'death (highest corner)')):
    fig.lines.append(matplotlib.lines.Line2D([lx], [0.865], marker=mk, ms=10, color=col, mec=mec, mew=1.5, transform=fig.transFigure))
    fig.text(lx + 0.012, 0.865, lab, color=SUB, fontsize=10.5, va='center'); lx += 0.22
check('cell circumradius / edge = sqrt(3)(1 + sqrt5)/4 (regular dodecahedron)', abs(RC / dmin - 3 ** 0.5 * (1 + 5 ** 0.5) / 4) < 1e-9, RC / dmin)
fig.savefig(OUT_PNG, facecolor=GROUND)
RES['checks'] = CHECKS
json.dump(RES, open(OUT_JSON, 'w'), indent=1)
nf = sum(not c[1] for c in CHECKS)
print('%d checks, %d failed' % (len(CHECKS), nf))
print('FINAL ok' if nf == 0 else 'FINAL FAIL')
sys.exit(1 if nf else 0)
