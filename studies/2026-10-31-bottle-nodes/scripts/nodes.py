# DICTO's bottle-strut nodes (31 Oct 2026): the RD node (c layers, octet) and the turned node = trapezo-rhombic dodecahedron (h layers,
# gyrated octet). Each face = one cap; tie points at the midpoints of the face's edges (DICTO's clock positions, 12 = towards the top).
# Usage: ~/geom/bin/python nodes.py <out png> <logo png>
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from scipy.spatial import HalfspaceIntersection
OUT, LOGO = sys.argv[1:3]; s3 = 3 ** .5
def node(dn):
    inpl = [np.array([np.cos(t), np.sin(t), 0]) for t in np.radians(range(0, 360, 60))]
    up = [np.array([np.cos(t) / s3, np.sin(t) / s3, (2 / 3) ** .5]) for t in np.radians([30, 150, 270])]
    down = [np.array([np.cos(t) / s3, np.sin(t) / s3, -(2 / 3) ** .5]) for t in np.radians(dn)]
    N = inpl + up + down
    P = HalfspaceIntersection(np.array([np.r_[n, -.5] for n in N]), np.zeros(3)).intersections
    P = np.unique(np.round(P, 9), axis=0); faces = []
    for i, n in enumerate(N):
        F = np.array([p for p in P if abs(p @ n - .5) < 1e-7]); c = F.mean(0)
        z = np.array([0, 0, 1.]); u = z - (z @ n) * n
        if np.linalg.norm(u) < 1e-6: u = np.array([1, 0, 0.]) - n[0] * n
        u /= np.linalg.norm(u); r = np.cross(u, n)
        F = F[np.argsort(np.arctan2((F - c) @ r, (F - c) @ u))]
        faces.append((n, F, c, 'waist' if i < 6 else ('top' if i < 9 else 'bottom')))
    return faces
def view(el, az):
    a, e = np.radians(az), np.radians(el)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
COL = {'waist': '#3f7fc4', 'top': '#d9a521', 'bottom': '#d9a521'}
def draw(ax, faces, M, square_waist):
    L = np.array([-.4, .5, .77]); L /= np.linalg.norm(L)
    vis = sorted([f for f in faces if (M @ f[0])[2] > 1e-6], key=lambda f: (M @ f[2])[2])
    for n, F, c, kind in vis:
        W = F @ M.T; k = .55 + .45 * max(0, (M @ n) @ L)
        col = np.array(matplotlib.colors.to_rgb(COL[kind])) * k + (1 - k) * .1
        ax.add_patch(Polygon(W[:, :2], closed=True, fc=col, ec='#1d1d24', lw=1.6, zorder=2))
        # the cap: the largest circle inside the face (drawn as a projected ring)
        rr = min(np.linalg.norm(np.cross(b - a, c - a)) / np.linalg.norm(b - a) for a, b in zip(F, np.roll(F, -1, 0)))
        u = F[0] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        t = np.linspace(0, 2 * np.pi, 80); ring = c + .82 * rr * (np.outer(np.cos(t), u) + np.outer(np.sin(t), v))
        ax.plot(*(ring @ M.T)[:, :2].T, color='white', lw=1.2, alpha=.85, zorder=3)
        for a, b in zip(F, np.roll(F, -1, 0)):
            m = c + .82 * rr * ((a + b) / 2 - c) / np.linalg.norm((a + b) / 2 - c); W2 = M @ m
            sq = square_waist and kind == 'waist'
            ax.plot(W2[0], W2[1], 's' if sq else 'o', ms=7, color='#c8102e' if sq else '#111', mec='white', mew=.8, zorder=4)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05)
fig, axs = plt.subplots(2, 2, figsize=(10, 10.6))
for row, (dn, title, sq) in enumerate((([90, 210, 330], 'RD node: c layers (the octet)', False), ([30, 150, 270], 'Turned node (trapezo-rhombic dodecahedron): h layers (gyrated octet)', True))):
    f = node(dn)
    draw(axs[row, 0], f, view(4, 0), sq); draw(axs[row, 1], f, view(38, 18), sq)
    axs[row, 0].set_title(title + '\nside view', fontsize=11, loc='left'); axs[row, 1].set_title('\nthree-quarter view', fontsize=11)
fig.text(.5, .045, 'Each face is one cap. Gold: the 3 top and 3 bottom caps (ties at about 2, 4, 8 and 10 o\'clock, the same in both nodes). Blue: the 6 waist caps.\n'
         'RD node waist caps: ties at 12, 6 and 4 & 10 (or 2 & 8 on alternate caps), black dots.  Turned node waist caps: ties at 12, 3, 6 and 9, red squares.\n'
         'To turn an RD node into an h node: cut across the waist and turn the top half 60°.', ha='center', fontsize=9)
la = fig.add_axes([.9, .005, .08, .08 * 10 / 10.6]); la.imshow(plt.imread(LOGO)); la.axis('off')
fig.savefig(OUT, dpi=200, facecolor='white'); print('ok')
