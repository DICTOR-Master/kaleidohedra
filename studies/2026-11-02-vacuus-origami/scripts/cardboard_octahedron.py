# Cardboard Vacuus of the octahedron (DICTO's slot-together build, 2026): the 12 fins lie in the three coordinate planes and
# close into three squares (half-diagonal a). Glue-free exact scheme (no flexing): square A (plane z = 0) and square B
# (plane x = 0) cross by a half-lap along the y-axis; square C (plane y = 0) is cut in two along the x-axis, and each half
# slides onto B by a half-lap along the z-axis and rests on A. Board thickness t, slot width t + clearance.
# Page 1: cut sheet at 1:1 (A4). Page 2: assembly in three steps. Usage: cardboard_octahedron.py <out.pdf> [edge mm] [t mm] [clearance mm]
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

out = sys.argv[1]; s = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
t = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5; cl = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
a = s / 2 ** .5; w = t + cl                                  # half-diagonal; slot width
R = np.array([[1, -1], [1, 1]]) / 2 ** .5      # every piece turned 45 deg on the sheet: squares upright
A4 = (210 / 25.4, 297 / 25.4); INK, SLOT, GUIDE = '#1d1d24', '#c0392b', '#9aa3b5'

def slot(ax, x0, y0, x1, y1, cx, cy):
    """slot of width w from (x0,y0) to (x1,y1), piece placed at (cx,cy); drawn as a closed outline (cut on the red line)"""
    d = np.array([x1 - x0, y1 - y0]); d /= np.linalg.norm(d); n = np.array([-d[1], d[0]]) * w / 2
    P = np.array([[x0, y0] + n, [x1, y1] + n, [x1, y1] - n, [x0, y0] - n]) @ R.T + [cx, cy]
    ax.fill(P[:, 0], P[:, 1], color=SLOT, alpha=0.25, lw=0); ax.plot(*np.vstack([P, P[:1]]).T, color=SLOT, lw=0.6)

def square(ax, cx, cy, label):
    """square with corners on the axes at distance a (drawn as a diamond: its diagonals are the two axes it carries)"""
    P = np.array([[a, 0], [0, a], [-a, 0], [0, -a], [a, 0]]) @ R.T + [cx, cy]; ax.plot(P[:, 0], P[:, 1], color=INK, lw=0.8)
    for L in (np.array([[-a, 0], [a, 0]]), np.array([[0, -a], [0, a]])):
        G = L @ R.T + [cx, cy]; ax.plot(G[:, 0], G[:, 1], color=GUIDE, lw=0.4, ls=(0, (3, 3)))
    ax.text(cx, cy - s / 2 - 5, label, ha='center', va='top', fontsize=8)

with PdfPages(out) as pdf:
    # ---- page 1: cut sheet, 1 mm = 1 mm on A4 ----
    fig = plt.figure(figsize=A4); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 210); ax.set_ylim(0, 297); ax.axis('off')
    ax.text(105, 285, 'DICTO Vacuus: the octahedron in cardboard (cut sheet, print at 100 %)', ha='center', fontsize=10, weight='bold')
    ax.text(105, 279, f'edge {s:.0f} mm, board {t:.1f} mm, slot width {w:.1f} mm. Black: cut. Red: cut out the slot. Grey dashes: guide lines only.',
            ha='center', fontsize=7)
    # A: horizontal diagonal = x-axis, vertical = y-axis; slot along y from the +y corner to the centre
    cA = (55, 215); square(ax, *cA, 'A  (plane z = 0): one slot, corner to centre'); slot(ax, 0, a, 0, 0, *cA)
    # B: horizontal diagonal = y-axis, vertical = z-axis; slot along y from the -y corner to the centre (meets A's slot),
    #    slots along z from both corners to half-way (for the two halves of C)
    cB = (155, 215); square(ax, *cB, 'B  (plane x = 0): three slots'); slot(ax, -a, 0, 0, 0, *cB)
    slot(ax, 0, a, 0, a / 2, *cB); slot(ax, 0, -a, 0, -a / 2, *cB)
    # C halves: triangles with the x-axis as base (trimmed by t/2 where they rest on A), apex on the z-axis;
    #           slot along z from the base up to half-way
    for k, (cx, cy) in enumerate(((55, 115), (155, 115))):
        P = np.array([[-a, t / 2], [a, t / 2], [0, a], [-a, t / 2]]) @ R.T + [cx, cy]; ax.plot(P[:, 0], P[:, 1], color=INK, lw=0.8)
        slot(ax, 0, t / 2, 0, a / 2, cx, cy)
        ax.text(cx, cy - s / 2 - 5, f'C{k + 1}  (half of plane y = 0): one slot, base to half-way', ha='center', va='top', fontsize=8)
    # scale check bar
    ax.plot([20, 120], [30, 30], color=INK, lw=1); ax.plot([20, 20], [28, 32], color=INK, lw=1); ax.plot([120, 120], [28, 32], color=INK, lw=1)
    ax.text(70, 33, '100 mm: measure after printing', ha='center', fontsize=7)
    ax.text(105, 14, 'DICTO · dictospheres.com · from paper #87 DICTO Vacuus Solids', ha='center', fontsize=6.5, color='#555')
    pdf.savefig(fig); plt.close(fig)

    # ---- page 2: assembly ----
    sqA = [[a, 0, 0], [0, a, 0], [-a, 0, 0], [0, -a, 0]]; sqB = [[0, a, 0], [0, 0, a], [0, -a, 0], [0, 0, -a]]
    hC1 = [[a, 0, t / 2], [0, 0, a], [-a, 0, t / 2]]; hC2 = [[a, 0, -t / 2], [0, 0, -a], [-a, 0, -t / 2]]
    steps = [([sqA, sqB], ['#d4af37', '#8e5bd6'], '1. Push the slot of A into the slot of B along the y-axis\n   until the two centres meet: a cross.'),
             ([sqA, sqB, hC1], ['#d4af37', '#8e5bd6', '#2bb3a3'], '2. Slide half C1 down onto B (slot into slot)\n   until its base rests on A.'),
             ([sqA, sqB, hC1, hC2], ['#d4af37', '#8e5bd6', '#2bb3a3', '#2bb3a3'], '3. Slide half C2 up from below the same way.\n   Three squares, twelve fins: the octahedron\'s Vacuus.')]
    fig = plt.figure(figsize=A4); fig.text(0.5, 0.96, 'Assembly', ha='center', fontsize=11, weight='bold')
    for i, (polys, cols, txt) in enumerate(steps):
        ax = fig.add_axes([0.08, 0.66 - 0.3 * i, 0.4, 0.28], projection='3d')
        ax.add_collection3d(Poly3DCollection([np.array(p) for p in polys], facecolors=cols, edgecolors=INK, linewidths=0.6, alpha=0.85))
        ax.set_xlim(-a, a); ax.set_ylim(-a, a); ax.set_zlim(-a, a); ax.set_box_aspect((1, 1, 1)); ax.view_init(20, 30); ax.axis('off')
        fig.text(0.52, 0.80 - 0.3 * i, txt, fontsize=9, va='center')
    fig.text(0.5, 0.04, 'DICTO · dictospheres.com · DICTO\'s own first build used three whole squares and let the board flex at the centre.',
             ha='center', fontsize=6.5, color='#555')
    pdf.savefig(fig); plt.close(fig)
print('written', out, 'edge', s, 'a', round(a, 2), 'slot', w)
