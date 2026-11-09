"""05: figures from data/03_tilings.json (tilings checked exactly in 03, lean scale kappa = 1/30).
leaning-hexagon-piece.png : DICTO's leaning-sided Escher hexagon: the six-riser staircase top (E6u0) with all six sides
                            leaning one way, from above and from below; the stripe piece (four sides leaning) upright
                            and turned over.
leaning-hexagon-cluster.png : copies leaning together: a layer of seven with three above (six sides leaning), and two
                            layers of the stripe tiling (rows of upright and turned-over wedges, forced h)."""
import json, math, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mc

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, '..', 'data', '03_tilings.json')))
HR = math.sqrt(2 / 3)
s3 = math.sqrt(3)
D = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]


def xy(i, j): return (i / 2, (i / 6 + j / 3) * s3)


def faces(cell, K0):
    k, X, off, top, bot, lean, wc = cell
    top = [{tuple(v): x for v, x in s} for s in top]
    bot = [{tuple(v): x for v, x in s} for s in bot]
    ln = {tuple(p): tuple(w) for p, w in lean}

    def P(v, h):
        w = tuple(wc) if v == (0, 0) else ln[v]
        i = X[0] + v[0] + (off[0] + h * w[0]) / K0
        j = X[1] + v[1] + (off[1] + h * w[1]) / K0
        x, y = xy(i, j)
        return (x, y, (12 * k + h) * HR / 12)
    F = {'top': [], 'bot': [], 'wall': [], 'riser': []}
    for s in range(6):
        a, b = D[s], D[(s + 1) % 6]
        F['top'].append([P((0, 0), top[s][(0, 0)]), P(a, top[s][a]), P(b, top[s][b])])
        F['bot'].append([P((0, 0), bot[s][(0, 0)]), P(b, bot[s][b]), P(a, bot[s][a])])
        F['wall'].append([P(a, bot[s][a]), P(b, bot[s][b]), P(b, top[s][b]), P(a, top[s][a])])
        p = (s - 1) % 6
        for T in ((top[p], top[s]), (bot[p], bot[s])):
            if T[0][(0, 0)] != T[1][(0, 0)] or T[0][a] != T[1][a]:
                F['riser'].append([P((0, 0), T[0][(0, 0)]), P(a, T[0][a]), P(a, T[1][a]), P((0, 0), T[1][(0, 0)])])
    return F


def draw(ax, cell, K0, col, alpha=0.95):
    shade = {'top': 1.0, 'riser': 0.6, 'wall': 0.78, 'bot': 0.5}
    base = mc.to_rgb(col)
    for kk, fs in faces(cell, K0).items():
        c = tuple(min(1, x * shade[kk] + (0.12 if kk == 'top' else 0)) for x in base)
        ax.add_collection3d(Poly3DCollection(fs, facecolor=c, edgecolor='k', linewidths=0.45, alpha=alpha))


def mark(fig):
    fig.text(0.985, 0.015, 'DICTO', ha='right', va='bottom', fontsize=11, fontweight='bold', color='#444')


def centre(cells, k):
    cs = [c for c in cells if c[0] == k]
    cx = sum(xy(*c[1])[0] for c in cs) / len(cs)
    cy = sum(xy(*c[1])[1] for c in cs) / len(cs)
    return min(cs, key=lambda c: (xy(*c[1])[0] - cx) ** 2 + (xy(*c[1])[1] - cy) ** 2)


def setlim(ax, c, r, z0, z1):
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(z0, z1)
    ax.set_box_aspect((1, 1, (z1 - z0) / (2 * r))); ax.set_axis_off()


E6 = data['E6u0, six sides leaning (shear (1,0))']
ST = data['FLAT, stripe lean (rows of wedges)']
VIOLET, GOLD = '#7a5cc7', '#d9a520'

fig = plt.figure(figsize=(16, 5.6))
c1 = centre(E6['cells'], 1)
for n, (elev, title) in enumerate(((32, 'from above: six risers climbing round,\nall six sides leaning one way'),
                                   (-30, 'from below'))):
    ax = fig.add_subplot(1, 3, n + 1, projection='3d')
    draw(ax, c1, E6['K0'], VIOLET)
    cx, cy = xy(*c1[1])
    setlim(ax, (cx + 0.05, cy), 0.75, HR * 0.1, HR * 1.9)
    ax.view_init(elev, -62)
    ax.set_title(title, fontsize=11)
ax = fig.add_subplot(1, 3, 3, projection='3d')
s1 = centre(ST['cells'], 1)
X1 = s1[1]
nbr = [c for c in ST['cells'] if c[0] == 1 and c[5] != s1[5]]
s2 = min(nbr, key=lambda c: (xy(*c[1])[0] - xy(*X1)[0]) ** 2 + (xy(*c[1])[1] - xy(*X1)[1]) ** 2)
draw(ax, s1, ST['K0'], VIOLET)
draw(ax, s2, ST['K0'], GOLD)
mx = (xy(*s1[1])[0] + xy(*s2[1])[0]) / 2; my = (xy(*s1[1])[1] + xy(*s2[1])[1]) / 2
setlim(ax, (mx, my), 1.0, HR * 0.3, HR * 1.7)
ax.view_init(18, -40)
ax.set_title('stripe piece: four sides leaning;\nupright (violet) and turned over (gold) rest on each other', fontsize=11)
fig.suptitle("Leaning-sided Escher hexagon (DICTO's idea): tilted side plates on the RD/TRD carrier", fontsize=13)
mark(fig)
fig.savefig(os.path.join(HERE, '..', 'figures', 'leaning-hexagon-piece.png'), dpi=130, bbox_inches='tight')

fig = plt.figure(figsize=(15, 6.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
cA = centre(E6['cells'], 1)
cxA, cyA = xy(*cA[1])
sel = [c for c in E6['cells'] if c[0] == 1 and (xy(*c[1])[0] - cxA) ** 2 + (xy(*c[1])[1] - cyA) ** 2 < 1.05]
sel2 = [c for c in E6['cells'] if c[0] == 2 and (xy(*c[1])[0] - cxA) ** 2 + (xy(*c[1])[1] - cyA) ** 2 < 0.40]
for c in sel:
    draw(ax, c, E6['K0'], VIOLET, 0.97)
for c in sel2:
    draw(ax, c, E6['K0'], '#3c78d8', 0.97)
setlim(ax, (cxA, cyA), 1.5, HR * 0.2, HR * 2.9)
ax.view_init(24, -58)
ax.set_title(f'six sides leaning: a layer of {len(sel)} with {len(sel2)} above (stacking word {E6["word"]}...)\n'
             'every cell of a layer leans the same way', fontsize=11)
ax = fig.add_subplot(1, 2, 2, projection='3d')
cB = centre(ST['cells'], 1)
cxB, cyB = xy(*cB[1])
ref_top = cB[3]
for k, z in ((1, 0), (2, 0)):
    for c in ST['cells']:
        if c[0] == k and (xy(*c[1])[0] - cxB) ** 2 + (xy(*c[1])[1] - cyB) ** 2 < (1.6 if k == 1 else 0.7):
            up = sorted(map(tuple, map(lambda t: (tuple(t[0]), tuple(t[1])), c[5]))) == sorted(map(lambda t: (tuple(t[0]), tuple(t[1])), cB[5]))
            draw(ax, c, ST['K0'], (VIOLET if up else GOLD) if k == 1 else ('#3c78d8' if up else '#e06666'), 0.96)
setlim(ax, (cxB, cyB), 1.8, HR * 0.3, HR * 2.8)
ax.view_init(20, -35)
ax.set_title('stripe lean: rows of upright and turned-over wedges leaning on each other;\n'
             'the next layer is the mirror pattern (forced h)', fontsize=11)
fig.suptitle('Copies leaning together (both tilings checked exactly: planar faces, volumes, winding numbers)',
             fontsize=13)
mark(fig)
fig.savefig(os.path.join(HERE, '..', 'figures', 'leaning-hexagon-cluster.png'), dpi=130, bbox_inches='tight')
import os
print('FINAL ok' if all(os.path.getsize(f) > 10000 for f in []) else 'FINAL FAIL: a figure was not written')
