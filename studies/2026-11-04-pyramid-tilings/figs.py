# DICTO 2026-11-04, paper #92: figures (float copies of the exact constructions of tiling_checks.py), matplotlib.
#   python33 figs.py   -> figures/*.png
import itertools, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

GOLD, PURPLE, RED, INK = '#d9a520', '#7b4fa8', '#c0392b', '#333333'
MARK = 'DICTO · dictospheres.com'
R3, R6 = math.sqrt(3), math.sqrt(6)
def real(p): return np.array([p[0] / 2, p[1] * R3 / 6, p[2] * R6 / 3], float)
def P(i, j, k, s): return (2 * i + j + s, 3 * j + s, k)

def build(seq, R):
    tiles = []
    for k in range(len(seq) - 1):
        s0, s1 = seq[k], seq[k + 1]
        up_tets = (s1 - s0) % 3 == 1
        for i in range(-R, R + 1):
            for j in range(-R, R + 1):
                up = (P(i, j, k, s0), P(i + 1, j, k, s0), P(i, j + 1, k, s0))
                dn = (P(i + 1, j, k, s0), P(i, j + 1, k, s0), P(i + 1, j + 1, k, s0))
                for tri, is_up in ((up, True), (dn, False)):
                    g = [sum(p[t] for p in tri) / 3 for t in range(3)]
                    if is_up == up_tets: tiles.append(('T', [real(p) for p in tri] + [real((g[0], g[1], k + 1))]))
                    else: tiles.append(('O', [real(p) for p in tri] + [real((2 * g[0] - p[0], 2 * g[1] - p[1], k + 1)) for p in tri]))
                up1 = (P(i, j, k + 1, s1), P(i + 1, j, k + 1, s1), P(i, j + 1, k + 1, s1))
                dn1 = (P(i + 1, j, k + 1, s1), P(i, j + 1, k + 1, s1), P(i + 1, j + 1, k + 1, s1))
                for tri in (up1, dn1):
                    a0 = sum(p[0] for p in tri) / 3; b0 = sum(p[1] for p in tri) / 3
                    jj = (b0 - s0) / 3; ii = (a0 - jj - s0) / 2
                    if abs(jj - round(jj)) < 1e-9 and abs(ii - round(ii)) < 1e-9:
                        tiles.append(('T', [real(p) for p in tri] + [real((a0, b0, k))]))
    return tiles

def faces(kind, v):
    if kind == 'T': return [list(f) for f in itertools.combinations(v, 3)]
    return [list(f) for f in itertools.combinations(v, 3) if all(abs(np.linalg.norm(p - q) - 1) < 1e-9 for p, q in itertools.combinations(f, 2))]

LIGHT = np.array([0.4, -0.5, 0.75]); LIGHT /= np.linalg.norm(LIGHT)
def shade(col, n, k=0.55):
    c = np.array(matplotlib.colors.to_rgb(col)); f = (1 - k) + k * abs(np.dot(n, LIGHT))
    return tuple(np.clip(c * f, 0, 1))
def draw_solid(ax, kind, v, alpha=0.55, col=None, centre_lines=False, edge=INK, lw=0.7, offset=np.zeros(3)):
    col = col or (GOLD if kind == 'T' else PURPLE)
    v = [p + offset for p in v]
    polys, cols = [], []
    for f in faces(kind, v):
        n = np.cross(f[1] - f[0], f[2] - f[0]); n /= np.linalg.norm(n)
        polys.append(f); cols.append(shade(col, n) + (alpha,))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors=edge, linewidths=lw))
    if centre_lines:
        c = sum(v) / len(v)
        ax.add_collection3d(Line3DCollection([[c, p] for p in v], colors=INK, linewidths=0.5, linestyles=(0, (2, 2))))
def draw_pyramid(ax, apex, base, col, alpha=0.9, offset=np.zeros(3), lw=0.6):
    pts = [apex + offset] + [b + offset for b in base]
    fs = [[pts[1], pts[2], pts[3]], [pts[0], pts[1], pts[2]], [pts[0], pts[2], pts[3]], [pts[0], pts[1], pts[3]]]
    cols = []
    for f in fs:
        n = np.cross(f[1] - f[0], f[2] - f[0]); n /= np.linalg.norm(n); cols.append(shade(col, n) + (alpha,))
    ax.add_collection3d(Poly3DCollection(fs, facecolors=cols, edgecolors=INK, linewidths=lw))
def setup(ax, ctr, r, elev=18, azim=-60):
    ax.set_xlim(ctr[0] - r, ctr[0] + r); ax.set_ylim(ctr[1] - r, ctr[1] + r); ax.set_zlim(ctr[2] - r, ctr[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
def mark(fig):
    fig.text(0.985, 0.015, MARK, ha='right', va='bottom', fontsize=8, color='#777777', family='DejaVu Sans')

# ---------------- Figure 1: the two arrangements round an edge
def edge_tiles(seq, a, b):
    T = build(seq, 3)
    return [t for t in T if any(np.allclose(p, a) for p in t[1]) and any(np.allclose(p, b) for p in t[1])]
fig = plt.figure(figsize=(8.4, 4.0), dpi=220)
for idx, (seq, title) in enumerate((([0, 1, 2], 'straight edge: T O T O (octet)'), ([1, 0, 1], 'twisted edge: T T O O'))):
    a, b = real(P(0, 0, 1, seq[1])), real(P(1, 0, 1, seq[1]))
    ts = edge_tiles(seq, a, b)
    ax = fig.add_subplot(1, 2, idx + 1, projection='3d')
    m = (a + b) / 2
    for kind, v in ts:
        c = sum(v) / len(v); d = c - m; d[0] = 0; d = d / np.linalg.norm(d) * 0.18
        draw_solid(ax, kind, v, alpha=0.62, centre_lines=True, offset=d)
    ax.plot(*np.array([a - (b - a) * 0.6, b + (b - a) * 0.6]).T, color=RED, lw=2.6, zorder=10)
    setup(ax, m, 0.95, elev=8, azim=-8)
    ax.set_title(title, fontsize=10, color=INK, family='DejaVu Sans', pad=-6)
mark(fig)
fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0.02, wspace=0)
fig.savefig('figures/edge-arrangements.png', bbox_inches='tight', pad_inches=0.06); plt.close(fig)

# ---------------- Figure 2: straight and twisted stacks
fig = plt.figure(figsize=(8.4, 4.2), dpi=220)
for idx, (seq, title) in enumerate((([0, 1, 2, 0], 'A B C A: every layer straight (octet, fcc)'), ([0, 1, 0, 1], 'A B A B: every layer twisted (hcp)'))):
    T = build(seq, 4)
    ax = fig.add_subplot(1, 2, idx + 1, projection='3d')
    axis = np.array([0.5, R3 / 6, 0.0])
    sel = [t for t in T if np.linalg.norm((sum(t[1]) / len(t[1]) - axis)[:2]) < 1.05]
    for kind, v in sel:
        k = int(round(min(p[2] for p in v) / (R6 / 3)))
        lift = np.array([0, 0, 0.32 * k])
        draw_solid(ax, kind, v, alpha=0.85, offset=lift, lw=0.5)
    setup(ax, axis + np.array([0, 0, 1.4]), 1.75, elev=14, azim=-75)
    ax.set_title(title, fontsize=9.5, color=INK, family='DejaVu Sans', pad=-4)
mark(fig)
fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0.02, wspace=0)
fig.savefig('figures/layer-stacks.png', bbox_inches='tight', pad_inches=0.06); plt.close(fig)

# ---------------- Figure 3: the cube of 4 T + 4 O pyramids; a slip; a slid column of cubes
S = 1 / math.sqrt(2)
cubev = [np.array(p, float) for p in itertools.product((0, 1), repeat=3)]
def cube_pyramids(origin, parity, e=S):
    ev = [p for p in cubev if int(sum(p)) % 2 == parity]; od = [p for p in cubev if int(sum(p)) % 2 != parity]
    c = np.array([.5, .5, .5]); out = []
    for f in itertools.combinations(ev, 3):
        o = next(q for q in od if all(abs(np.linalg.norm(q - x) - 1) < 1e-9 for x in f))
        out.append(('T', c, f)); out.append(('O', o, f))
    return [(k, origin + e * a, [origin + e * x for x in f]) for k, a, f in out]
fig = plt.figure(figsize=(8.4, 3.3), dpi=220)
ax = fig.add_subplot(1, 3, 1, projection='3d')
ctr = np.array([S / 2] * 3)
for k, a, f in cube_pyramids(np.zeros(3), 0):
    cen = (a + sum(f)) / 4; u = (cen - ctr) / np.linalg.norm(cen - ctr); d = u * (0.32 if k == 'O' else 0.2)
    draw_pyramid(ax, a, f, GOLD if k == 'T' else PURPLE, offset=d)
setup(ax, ctr, 0.72, elev=20, azim=-55)
ax.set_title('cube = 4 T + 4 O', fontsize=9.5, family='DejaVu Sans', color=INK, pad=-4)
# slip: octet slab pair, the upper slab moved along the layer plane
ax = fig.add_subplot(1, 3, 2, projection='3d')
T = build([0, 1, 2], 3)
axis = np.array([0.5, R3 / 6, 0.0])
shift = np.array([0.31, 0.17, 0.0])
for kind, v in T:
    c = sum(v) / len(v)
    if np.linalg.norm((c - axis)[:2]) > 1.25: continue
    up = min(p[2] for p in v) > 0.5
    draw_solid(ax, kind, v, alpha=0.85, lw=0.5, offset=(shift + np.array([0, 0, 0.12])) if up else np.zeros(3))
setup(ax, axis + np.array([0, 0, 0.8]), 1.45, elev=16, azim=-70)
ax.set_title('a slip along a layer plane', fontsize=9.5, family='DejaVu Sans', color=INK, pad=-4)
# a column of cubes slid, each cube cut either way
ax = fig.add_subplot(1, 3, 3, projection='3d')
rng = np.random.default_rng(4)
for i, j, k in itertools.product(range(3), range(2), range(3)):
    dz = 0.37 * S if (i, j) == (1, 0) else 0.0
    if (i, j) == (1, 0) and k == 2: continue
    o = np.array([i * S, j * S, k * S + dz])
    par = int(rng.integers(2))
    for kk, a, f in cube_pyramids(o, par):
        draw_pyramid(ax, a, f, GOLD if kk == 'T' else PURPLE, alpha=0.95, lw=0.35)
setup(ax, np.array([1.5 * S, 1.0 * S, 1.5 * S]), 1.25, elev=22, azim=-62)
ax.set_title('cubes: one column slid', fontsize=9.5, family='DejaVu Sans', color=INK, pad=-4)
mark(fig)
fig.subplots_adjust(left=0, right=1, top=0.93, bottom=0.03, wspace=0)
fig.savefig('figures/beyond-face-to-face.png', bbox_inches='tight', pad_inches=0.06); plt.close(fig)
print('figures written')
