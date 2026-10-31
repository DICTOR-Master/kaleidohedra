# The two bottle nodes as clock faces (DICTO 31 Oct 2026): every cap drawn as a true circle with the numbers 1-12; 12 o'clock points
# to the top of the node (the 3-fold axis). Tie points at the clock positions of the face's edge midpoints, each labelled with the cap it
# ties to. Caps: T1-T3 top, W1-W6 waist, B1-B3 bottom. Usage: ~/geom/bin/python clocks.py <out png> <logo png>
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.spatial import HalfspaceIntersection
OUT, LOGO = sys.argv[1:3]; s3 = 3 ** .5
NAMES = [f'W{i+1}' for i in range(6)] + ['T1', 'T2', 'T3', 'B1', 'B2', 'B3']
def ties(dn):
    inpl = [np.array([np.cos(t), np.sin(t), 0]) for t in np.radians(range(0, 360, 60))]
    up = [np.array([np.cos(t) / s3, np.sin(t) / s3, (2 / 3) ** .5]) for t in np.radians([30, 150, 270])]
    down = [np.array([np.cos(t) / s3, np.sin(t) / s3, -(2 / 3) ** .5]) for t in np.radians(dn)]
    N = inpl + up + down
    P = np.unique(np.round(HalfspaceIntersection(np.array([np.r_[n, -.5] for n in N]), np.zeros(3)).intersections, 9), axis=0)
    out = []
    for i, n in enumerate(N):
        F = np.array([p for p in P if abs(p @ n - .5) < 1e-7]); c = F.mean(0)
        u = np.array([0, 0, 1.]) - n[2] * n; u /= np.linalg.norm(u); r = np.cross(u, n)   # 12 o'clock = towards the top
        F = F[np.argsort(np.arctan2((F - c) @ r, (F - c) @ u))]; t = []
        for a, b in zip(F, np.roll(F, -1, 0)):
            m = (a + b) / 2 - c; clock = (np.degrees(np.arctan2(m @ r, m @ u)) % 360) / 30
            nb = [j for j, mm in enumerate(N) if j != i and abs(a @ mm - .5) < 1e-7 and abs(b @ mm - .5) < 1e-7][0]
            t.append((clock, NAMES[nb]))
        out.append((NAMES[i], t))
    return dict(out)
def layout(T):
    L = {f'W{i+1}': (i * 2.15, 1.0) for i in range(6)}
    for k in ('T1', 'T2', 'T3', 'B1', 'B2', 'B3'):
        ws = [L[n][0] for c, n in T[k] if n[0] == 'W']
        xs = sorted(ws)
        x = (xs[0] + xs[-1]) / 2 if xs[-1] - xs[0] < 5 else (xs[-1] + 2.15 * 6 + xs[0]) / 2 % (2.15 * 6)
        L[k] = (x, 2.45 if k[0] == 'T' else -0.45)
    return L
def panel(ax, T, square, title):
    for name, (x, y) in layout(T).items():
        x = x + (.0 if name[0] == 'W' else -.0); R = .45
        waist = name[0] == 'W'
        ax.add_patch(Circle((x, y), R, fc='#e8f0fa' if waist else '#fbf1d8', ec='#3f7fc4' if waist else '#b8962e', lw=2))
        ax.text(x, y, name, ha='center', va='center', fontsize=11, weight='bold', color='#1d1d24')
        for clock, nb in T[name]:
            a = np.radians(90 - 30 * clock); px, py = x + R * np.cos(a), y + R * np.sin(a)
            sq = square and waist
            ax.plot(px, py, 's' if sq else 'o', ms=8, color='#c8102e' if sq else '#111', mec='white', mew=.8, zorder=5)
            ax.text(x + (R + .27) * np.cos(a), y + (R + .27) * np.sin(a), f'{(round(clock) % 12) or 12}' + f'\n→{nb}', ha='center', va='center', fontsize=9, color='#c8102e' if sq else '#111')
    ax.set_title(title, fontsize=11, loc='left'); ax.set_xlim(-1.1, 13.4); ax.set_ylim(-1.3, 3.3); ax.set_aspect('equal'); ax.axis('off')
fig, axs = plt.subplots(2, 1, figsize=(14, 12))
panel(axs[0], ties([90, 210, 330]), False, 'RD node, c layers (the octet): top caps T, waist caps W, bottom caps B')
panel(axs[1], ties([30, 150, 270]), True, 'Turned node (trapezo-rhombic dodecahedron), h layers (gyrated octet)')
fig.text(.5, .03, "On every cap 12 o'clock points to the top of the node. Each tie point shows its clock hour and the cap it ties to (→).\n"
         "Waist caps W1–W6 go round the middle in order; T1–T3 sit above, B1–B3 below. Only the waist caps change: red squares at 3, 6, 9 and 12.", ha='center', fontsize=9)
la = fig.add_axes([.9, .005, .08, .08 * 10 / 11]); la.imshow(plt.imread(LOGO)); la.axis('off')
fig.savefig(OUT, dpi=200, facecolor='white'); print('ok')
for nm, dn in (('RD', [90, 210, 330]), ('TRD', [30, 150, 270])):
    print(nm, {k: [(round(c, 1), n) for c, n in v] for k, v in ties(dn).items()})
