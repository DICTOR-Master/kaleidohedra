"""05: figures.  escher-hexagon-piece.png: the stepped-hexagon piece (E1: six plates climbing round, one riser,
rise per turn = one layer) from above and below, plus the plate map.  escher-forced-stack.png: the periodic stack the
piece is forced into (from data/04_stack.json, checked exactly in 04)."""
import json, math, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HR = math.sqrt(2 / 3)
D = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
s3 = math.sqrt(3)


def xy(p): return (p[0] / 2, (p[0] / 6 + p[1] / 3) * s3)


def solid_faces(piece, X=(0, 0), zc=0.0):
    """faces of the union of 6 prisms: top plates, bottom plates, outer walls, risers (exposed parts of radial walls)."""
    top, bot = [dict((tuple(v), x) for v, x in s) for s in piece[0]], [dict((tuple(v), x) for v, x in s) for s in piece[1]]
    P = lambda v, z: (xy((X[0] + v[0], X[1] + v[1]))[0], xy((X[0] + v[0], X[1] + v[1]))[1], zc + z * HR / 12)
    F = {'top': [], 'bot': [], 'wall': [], 'riser': []}
    for s in range(6):
        a, b = D[s], D[(s + 1) % 6]
        F['top'].append([P((0, 0), top[s][(0, 0)]), P(a, top[s][a]), P(b, top[s][b])])
        F['bot'].append([P((0, 0), bot[s][(0, 0)]), P(a, bot[s][a]), P(b, bot[s][b])])
        F['wall'].append([P(a, bot[s][a]), P(b, bot[s][b]), P(b, top[s][b]), P(a, top[s][a])])
        p = (s - 1) % 6     # radial edge O -> D_s shared by sectors p and s
        for T in ((top[p], top[s]), (bot[p], bot[s])):
            if T[0][(0, 0)] != T[1][(0, 0)] or T[0][a] != T[1][a]:
                F['riser'].append([P((0, 0), T[0][(0, 0)]), P(a, T[0][a]), P(a, T[1][a]), P((0, 0), T[1][(0, 0)])])
    return F


def draw(ax, piece, X=(0, 0), zc=0.0, col='#7a5cc7', alpha=0.95, edge='k'):
    F = solid_faces(piece, X, zc)
    shade = {'top': 1.0, 'riser': 0.55, 'wall': 0.75, 'bot': 0.45}
    import matplotlib.colors as mc
    base = mc.to_rgb(col)
    for k, fs in F.items():
        c = tuple(min(1, x * shade[k] + (0.15 if k == 'top' else 0)) for x in base)
        ax.add_collection3d(Poly3DCollection(fs, facecolor=c, edgecolor=edge, linewidths=0.5, alpha=alpha))


def mark(fig):
    fig.text(0.985, 0.015, 'DICTO', ha='right', va='bottom', fontsize=11, fontweight='bold', color='#444')


stack = json.load(open('data/04_stack.json'))
piece = stack['piece']

fig = plt.figure(figsize=(15, 5.4))
for n, (elev, azim, title) in enumerate(((38, -60, 'from above: six plates climbing round the axis'),
                                         (-35, -60, 'from below: the matching bottom'))):
    ax = fig.add_subplot(1, 3, n + 1, projection='3d')
    draw(ax, piece)
    ax.set_xlim(-0.6, 0.6); ax.set_ylim(-0.6, 0.6); ax.set_zlim(-0.6, 0.6)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.set_axis_off()
    ax.set_title(title, fontsize=11)
ax = fig.add_subplot(1, 3, 3)
top = [dict((tuple(v), x) for v, x in s) for s in piece[0]]
cm = plt.get_cmap('viridis')
for s in range(6):
    a, b = D[s], D[(s + 1) % 6]
    pts = [xy((0, 0)), xy(a), xy(b)]
    m = sum(top[s].values()) / 3
    ax.fill(*zip(*pts), color=cm((m - 1) / 12), ec='k', lw=1)
    for v, w in (((0, 0), 0.3), (a, 0.78), (b, 0.78)):
        cx = sum(p[0] for p in pts) / 3; cy = sum(p[1] for p in pts) / 3
        px, py = xy(v)
        ax.text(cx + (px - cx) * w, cy + (py - cy) * w, str(top[s][v]), ha='center', va='center', fontsize=9,
                color='w' if m < 7 else 'k')
ax.annotate('', xy=xy((0, 1)), xytext=xy((1, 0)),
            arrowprops=dict(arrowstyle='->', color='crimson', lw=1.5, connectionstyle='arc3,rad=0.45'))
ax.plot(*zip(xy((0, 0)), xy(D[0])), color='crimson', lw=3)
ax.text(*xy((1.15, 0)), 'riser', color='crimson', fontsize=10)
ax.set_aspect('equal'); ax.set_axis_off()
ax.set_title('top heights (units of layer/12): climbs 2 per plate,\nrise 12 = one layer per turn, one riser', fontsize=10)
fig.suptitle('Escher stepped hexagon on the RD/TRD carrier (DICTO proposed; piece E1)', fontsize=13)
mark(fig)
fig.savefig('figures/escher-hexagon-piece.png', dpi=150, bbox_inches='tight')

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
cols = ['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd']
for k, p, c in stack['cells']:
    if k > 3:
        continue
    x, y = xy(p)
    if x * x + y * y > 1.4:
        continue
    draw(ax, c, tuple(p), k * HR, col=cols[k % 5], alpha=0.9, edge='#222')
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_zlim(-0.8, 3.2)
ax.set_box_aspect((1, 1, 1.43)); ax.view_init(18, -55); ax.set_axis_off()
leans = stack['leans']
ax.set_title(f'E1 stack from a cycle of the layer graph (leans {leans[:3]}: h at every interface),\n'
             'three turns of the piece repeat in the plane (period index 3): periodic', fontsize=10)
mark(fig)
fig.savefig('figures/escher-forced-stack.png', dpi=150, bbox_inches='tight')
import os
ok = all(os.path.getsize(f) > 10000 for f in ('figures/escher-hexagon-piece.png', 'figures/escher-forced-stack.png'))
print('FINAL ok' if ok else 'FINAL FAIL: a figure was not written')
