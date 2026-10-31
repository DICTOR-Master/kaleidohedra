# Ring nets (DICTO 2026-10-31): the HexOct pieces as nets of rounded triangles, one PET-bottle-cap security ring each, tied at
# six points (two per side, at 1/4 and 3/4 of the side). Pieces: tetrahedron (4 rings), octahedron (8), and the close-packed
# layer as a hexagon of 6 rings. Shared edges: matching tie points join the two rings (shown as small dots, same colour per edge).
# Usage: ~/geom/bin/python ring_nets.py <out png> <logo png>
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
OUT, LOGO = sys.argv[1:3]
s3 = 3 ** .5
def tri(i, j, up):
    """triangle of the triangular lattice: lattice coords (i, j), pointing up or down; unit side"""
    a = np.array([i + j / 2, j * s3 / 2])
    return [a, a + [1, 0], a + [.5, s3 / 2]] if up else [a + [1, 0], a + [1.5, s3 / 2], a + [.5, s3 / 2]]
def rounded(P, k=0.16):
    """the ring pulled into a rounded triangle: straight sides between the tie zones, rounded corners (radius ~ k of the side)"""
    P = [np.array(p) for p in P]; verts, codes = [], []
    for n in range(3):
        a, b, c = P[n - 1], P[n], P[(n + 1) % 3]
        p1 = b + (a - b) * k; p2 = b + (c - b) * k
        verts += [p1, b, p2] if not verts else [p1, b, p2]
        codes += ([Path.MOVETO] if not codes else [Path.LINETO]) + [Path.CURVE3, Path.CURVE3]
    verts.append(verts[0]); codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)
def ties(P, inset=0.06):
    c = np.mean(P, 0); out = []
    for n in range(3):
        a, b = P[n], P[(n + 1) % 3]
        for t in (.25, .75):
            p = a + (b - a) * t; out.append(p + (c - p) * inset)
    return out
NETS = [('Tetrahedron · 4 rings', [(0, 0, 1), (1, 0, 1), (0, 1, 1), (0, 0, 0)], '#2bb3a3'),
        ('Octahedron · 8 rings', [(0, 0, 1), (0, 0, 0), (1, 0, 1), (1, 0, 0), (2, 0, 1), (2, 0, 0), (0, 1, 1), (2, -1, 0)], '#8e5bd6'),
        ('Close-packed layer · hexagon of 6 rings', [(0, 0, 1), (-1, 0, 1), (-1, 0, 0), (0, -1, 1), (0, -1, 0), (-1, -1, 0)], '#d4af37')]
fig, axs = plt.subplots(1, 3, figsize=(12, 4.6), gridspec_kw=dict(wspace=0.08))
for ax, (title, cells, col) in zip(axs, NETS):
    allp = []
    for i, j, up in cells:
        P = [np.array(p, float) for p in tri(i, j, up)]; allp += P
        ax.add_patch(PathPatch(rounded(P), facecolor=matplotlib.colors.to_rgba(col, 0.28), edgecolor='#1d1d24', lw=2.2))
        for t in ties(P): ax.plot(*t, 'o', ms=4.2, color='#1d1d24')
    A = np.array(allp); pad = 0.25
    ax.set_xlim(A[:, 0].min() - pad, A[:, 0].max() + pad); ax.set_ylim(A[:, 1].min() - pad, A[:, 1].max() + pad)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=11)
fig.text(0.5, 0.04, 'One security ring per triangle, tied at six points (dots: two per side, at a quarter and three quarters).\n'
         'Where two rings meet along a side, tie their facing dots together; fold along the shared sides to close the piece.',
         ha='center', fontsize=9)
la = fig.add_axes([0.935, 0.02, 0.05, 0.05 * 12 / 4.6]); la.imshow(plt.imread(LOGO)); la.axis('off')
fig.savefig(OUT, dpi=220, facecolor='white'); print('ok')
