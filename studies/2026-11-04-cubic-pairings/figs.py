# DICTO 2026-11-04, paper #93: figures (float copies of the exact constructions of pairing_checks.py), matplotlib.
#   ~/geom/bin/python figs.py   -> figures/*.png
import itertools, math, random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

GOLD, PURPLE, TEAL, RED, INK = '#d9a520', '#7b4fa8', '#3a9c9c', '#c0392b', '#333333'
MARK = 'DICTO · dictospheres.com'
PHI = (1 + 5 ** 0.5) / 2
LIGHT = np.array([0.4, -0.5, 0.75]); LIGHT /= np.linalg.norm(LIGHT)

def polytope(planes):
    planes = [(np.array(n, float), float(d)) for n, d in planes]
    V = []
    for (n1, d1), (n2, d2), (n3, d3) in itertools.combinations(planes, 3):
        A = np.array([n1, n2, n3])
        if abs(np.linalg.det(A)) < 1e-9: continue
        x = np.linalg.solve(A, [d1, d2, d3])
        if all(n @ x <= d + 1e-9 for n, d in planes) and not any(np.allclose(x, y) for y in V): V.append(x)
    F = []
    for n, d in planes:
        f = [v for v in V if abs(n @ v - d) < 1e-9]
        if len(f) < 3: continue
        c = sum(f) / len(f); u = f[0] - c; w = np.cross(n, u)
        f.sort(key=lambda p: math.atan2((p - c) @ w, (p - c) @ u)); F.append((n / np.linalg.norm(n), f))
    return F
def hull(pts):
    pts = [np.array(p, float) for p in pts]; pl = []
    for a, b, c in itertools.combinations(pts, 3):
        n = np.cross(b - a, c - a)
        if np.linalg.norm(n) < 1e-9: continue
        s = [n @ (p - a) for p in pts]
        if all(x <= 1e-9 for x in s): pl.append((n, n @ a))
        elif all(x >= -1e-9 for x in s): pl.append((-n, -n @ a))
    return polytope(pl)
def shade(col, n, k=0.55):
    c = np.array(matplotlib.colors.to_rgb(col)); f = (1 - k) + k * abs(np.dot(n, LIGHT))
    return tuple(np.clip(c * f, 0, 1))
def draw(ax, F, col, off=np.zeros(3), alpha=0.9, lw=0.6):
    ax.add_collection3d(Poly3DCollection([[p + off for p in f] for n, f in F],
                                         facecolors=[shade(col, n) + (alpha,) for n, f in F], edgecolors=INK, linewidths=lw))
def setup(ax, ctr, r, elev=18, azim=-60):
    ax.set_xlim(ctr[0] - r, ctr[0] + r); ax.set_ylim(ctr[1] - r, ctr[1] + r); ax.set_zlim(ctr[2] - r, ctr[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
def mark(fig):
    fig.text(0.985, 0.015, MARK, ha='right', va='bottom', fontsize=8, color='#777777', family='DejaVu Sans')
def cell(m, c=(0, 0, 0)):
    c = np.array(c, float); pl = []
    for i in range(3):
        for s in (1, -1):
            n = np.zeros(3); n[i] = s; pl.append((n, s * c[i] + 1))
    for s in itertools.product((1, -1), repeat=3):
        pl.append((np.array(s, float), m + np.array(s) @ c))
    return polytope(pl)

# ---------------- Figure 1: five pairs of the CsCl walk, each P (gold) with its Q (purple) across the shared face
pairs = [(3 - PHI, 'μ = 3 − φ: Unborn Axes\n+ Icosaxes'), (1.5, 'μ = 3/2: Kelvin\n(self-paired)'), (2.0, 'μ = 2: cuboctahedron\n+ octahedron'),
         (1 + 2 ** 0.5, 'μ = 1 + √2: truncated\ncube + octahedron'), (4 + 1.5 * 2 ** 0.5 - 5 ** 0.5 - 10 ** 0.5 / 2, 'μ ≈ 2.304: Greater Golden\nCut Cube + octahedron')]
fig = plt.figure(figsize=(10.0, 2.9), dpi=220)
for k, (m, title) in enumerate(pairs):
    ax = fig.add_subplot(1, 5, k + 1, projection='3d')
    gap = np.array([1, 1, 1.0]) * 0.22
    draw(ax, cell(m), GOLD, -gap / 2)
    draw(ax, cell(3 - m, (1, 1, 1)), PURPLE, gap / 2)
    setup(ax, np.array([0.5, 0.5, 0.5]), 1.55, elev=16, azim=-58)
    ax.set_title(title, fontsize=8.2, color=INK, family='DejaVu Sans', pad=-2)
mark(fig)
fig.subplots_adjust(left=0, right=1, top=0.92, bottom=0.03, wspace=0)
fig.savefig('figures/cscl-walk.png', bbox_inches='tight', pad_inches=0.06); plt.close(fig)

# ---------------- Figure 2: the bipyramid B on a face of the cube lattice and its three cuts
sq = [np.array(p, float) for p in [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]]
U, D = np.array([.5, .5, .5]), np.array([.5, .5, -.5])
fig = plt.figure(figsize=(10.0, 2.9), dpi=220)
panels = [('B: the two cube pyramids\nacross a face of the cube lattice', [(hull(sq + [U, D]), TEAL, np.zeros(3))]),
          ('equator: two cube pyramids C6', [(hull(sq + [U]), GOLD, np.array([0, 0, .2])), (hull(sq + [D]), GOLD, np.array([0, 0, -.2]))]),
          ('one diagonal: two RD pyramids R12\n(apexes at the even corners)', [(hull([sq[0], sq[1], sq[3], U, D]), PURPLE, np.array([-.18, -.18, 0])),
                                                                         (hull([sq[2], sq[1], sq[3], U, D]), PURPLE, np.array([.18, .18, 0]))]),
          ('the other diagonal: two R12\n(apexes at the odd corners)', [(hull([sq[1], sq[0], sq[2], U, D]), PURPLE, np.array([.3, -.3, 0])),
                                                                     (hull([sq[3], sq[0], sq[2], U, D]), PURPLE, np.array([-.3, .3, 0]))])]
for k, (title, items) in enumerate(panels):
    ax = fig.add_subplot(1, 4, k + 1, projection='3d')
    for F, col, off in items: draw(ax, F, col, off, alpha=0.85)
    setup(ax, np.array([.5, .5, 0]), 0.85, elev=22, azim=-62 if k < 3 else -20)
    ax.set_title(title, fontsize=8.2, color=INK, family='DejaVu Sans', pad=-2)
mark(fig)
fig.subplots_adjust(left=0, right=1, top=0.92, bottom=0.03, wspace=0)
fig.savefig('figures/bipyramid-cuts.png', bbox_inches='tight', pad_inches=0.06); plt.close(fig)

# ---------------- Figure 3: round one corner v of the cube lattice, the 12 squares at v; left all cut through v (a whole
# rhombic dodecahedron of 12 R12, drawn apart), right a random choice (gold: apex at v; purple: apex at a neighbour)
def squares_at(v):
    out = []
    for ax_ in range(3):
        e1, e2 = (ax_ + 1) % 3, (ax_ + 2) % 3
        for s1, s2 in itertools.product((1, -1), repeat=2):
            a = np.zeros(3); a[e1] = s1; b = np.zeros(3); b[e2] = s2
            c = v + (a + b) / 2; n = np.zeros(3); n[ax_] = .5
            out.append((v, v + a, v + a + b, v + b, c + n, c - n))
    return out
v = np.zeros(3)
rng = random.Random(7)
fig = plt.figure(figsize=(8.4, 4.0), dpi=220)
for k, (title, choose) in enumerate((('all 12 cut through v: a whole rhombic dodecahedron', lambda: True),
                                     ('a random choice: gold R12 have their apex at v,\npurple ones at the far corner of the square', lambda: rng.random() < 0.5))):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d')
    for (p0, p1, p2, p3, up, dn) in squares_at(v):
        c = (p0 + p2) / 2; off = (c - v) * 0.45
        if choose(): draw(ax, hull([p0, p1, p3, up, dn]), GOLD, off, alpha=0.88)
        else: draw(ax, hull([p2, p1, p3, up, dn]), PURPLE, off, alpha=0.88)
    setup(ax, v, 1.35, elev=18, azim=-55)
    ax.set_title(title, fontsize=8.6, color=INK, family='DejaVu Sans', pad=-4)
mark(fig)
fig.subplots_adjust(left=0, right=1, top=0.93, bottom=0.02, wspace=0)
fig.savefig('figures/corner-choices.png', bbox_inches='tight', pad_inches=0.06); plt.close(fig)
print('figures written')
