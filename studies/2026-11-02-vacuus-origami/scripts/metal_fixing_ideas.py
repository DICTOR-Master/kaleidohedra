# Fixing ideas for a metal octahedron Vacuus (DICTO's four-piece slot-together build), no welds, no bolts, no plinth.
# One A4 page, four panels: (1) gravity lock: standing on three corners; (2) flat feet; (3) drop-lock slot; (4) slot lining.
# Usage: metal_fixing_ideas.py <out.pdf>
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

INK, GOLD, VIOLET, TEAL, RED, GREY = '#1d1d24', '#d4af37', '#8e5bd6', '#2bb3a3', '#c0392b', '#9aa3b5'
a = 1.0; foot = 0.2                                          # half-diagonal; length cut off each ground corner
def frame():                                                  # rotate so the face with corners -x, -y, -z is the floor
    n = -np.ones(3) / 3 ** .5; z = -n; x = np.cross([0, 0, 1.0], z); x = x / np.linalg.norm(x) if np.linalg.norm(x) > 1e-9 else np.array([1.0, 0, 0])
    y = np.cross(z, x); return np.array([x, y, z])
Rm = frame()
sq = {'A': [[a, 0, 0], [0, a, 0], [-a, 0, 0], [0, -a, 0]], 'B': [[0, a, 0], [0, 0, a], [0, -a, 0], [0, 0, -a]],
      'C1': [[a, 0, 0], [0, 0, a], [-a, 0, 0]], 'C2': [[a, 0, 0], [0, 0, -a], [-a, 0, 0]]}
cols = {'A': GOLD, 'B': VIOLET, 'C1': TEAL, 'C2': TEAL}

def feet(P, ground):
    """cut each ground corner back to a short flat: replace corner v by two points 'foot' along its two edges"""
    out = []
    for i, v in enumerate(P):
        if tuple(np.round(v, 6)) in ground:
            u, w = P[i - 1], P[(i + 1) % len(P)]
            out += [v + foot * (u - v) / np.linalg.norm(u - v), v + foot * (w - v) / np.linalg.norm(w - v)]
        else: out.append(v)
    return np.array(out)

def draw3d(ax, flat):
    ground = {(-a, 0, 0), (0, -a, 0), (0, 0, -a)}
    polys = []
    for k, P in sq.items():
        P = np.array(P, float)
        if flat: P = feet(P, ground)
        polys.append((P @ Rm.T, cols[k]))
    zmin = min(P[:, 2].min() for P, _ in polys)
    ax.add_collection3d(Poly3DCollection([P - [0, 0, zmin] for P, _ in polys], facecolors=[c for _, c in polys], edgecolors=INK, linewidths=0.6, alpha=0.9))
    g = 1.0; ax.add_collection3d(Poly3DCollection([np.array([[-g, -g, 0], [g, -g, 0], [g, g, 0], [-g, g, 0]])], facecolors='#eeeeee', edgecolors='none', alpha=0.6))
    ax.set_xlim(-0.9, 0.9); ax.set_ylim(-0.9, 0.9); ax.set_zlim(0, 1.8); ax.set_box_aspect((1, 1, 1)); ax.view_init(8, 35); ax.axis('off')

fig = plt.figure(figsize=(210 / 25.4, 297 / 25.4))
fig.text(0.5, 0.965, 'Metal Vacuus: holding together by shape alone', ha='center', fontsize=12, weight='bold')
fig.text(0.5, 0.945, "DICTO's four pieces, slid together as in cardboard: no welds, no bolts, no plinth", ha='center', fontsize=8.5)

ax = fig.add_axes([0.02, 0.56, 0.48, 0.36], projection='3d'); draw3d(ax, False)
fig.text(0.06, 0.55, '1. Gravity lock', fontsize=10, weight='bold')
fig.text(0.06, 0.475, 'Stand it on three corners (one face of the\noctahedron down). Every piece can leave only\nthe way it slid in: for each piece that way runs\ninto the floor or uphill. Its own weight holds it.', fontsize=7.5, va='bottom')

ax = fig.add_axes([0.50, 0.56, 0.48, 0.36], projection='3d'); draw3d(ax, True)
fig.text(0.54, 0.55, '2. Flat feet', fontsize=10, weight='bold')
fig.text(0.54, 0.475, 'Cut the three ground corners back to short\nflats (part of the outline, nothing added).\nThe piece stands on three small feet instead\nof three points: steadier, kinder to floors.', fontsize=7.5, va='bottom')

# 3. drop-in tabs (side view): a half of C slides down onto B; its tab drops through a tab slot in A
ax = fig.add_axes([0.06, 0.13, 0.40, 0.30]); ax.set_aspect('equal'); ax.axis('off')
ax.fill([-4, 4, 4, -4], [-0.5, -0.5, 0.5, 0.5], color='#e8e8ee', ec=INK, lw=0.8)                       # A, edge-on
ax.fill([1.4, 2.6, 2.6, 1.4], [-0.5, -0.5, 0.5, 0.5], color='white', ec=TEAL, lw=1.0)                   # tab slot in A
ax.fill([-3, 3, 0], [0.75, 0.75, 3.6], color='#d8d8e0', ec=INK, lw=0.8)                                  # half of C above
ax.fill([1.5, 2.5, 2.5, 1.5], [-0.9, -0.9, 0.75, 0.75], color=TEAL, ec=INK, lw=0.6)                      # its tab, dropped in
ax.annotate('', xy=(0, 1.2), xytext=(0, 3.0), arrowprops=dict(arrowstyle='->', color=RED, lw=1))
ax.text(0.3, 2.2, 'slides down\nalong B', fontsize=7, color=RED); ax.text(2.8, -0.9, 'tab through A', fontsize=7, color=TEAL)
ax.set_xlim(-4.5, 5.5); ax.set_ylim(-1.5, 4)
fig.text(0.06, 0.115, '3. Drop-in tabs', fontsize=10, weight='bold')
fig.text(0.06, 0.04, 'Each half of the cut square carries two short\ntabs that drop through slots in A as it slides\nonto B. Nothing can shift sideways; a half\ncomes out only by lifting it straight back.', fontsize=7.5, va='bottom')

# 4. slot lining, cross-section
ax = fig.add_axes([0.54, 0.13, 0.40, 0.30]); ax.set_aspect('equal'); ax.axis('off')
ax.fill([-3, 3, 3, -3], [-0.5, -0.5, 0.5, 0.5], color='#e8e8ee', ec=INK, lw=0.8)              # plate A seen edge-on
ax.fill([-0.5, 0.5, 0.5, -0.5], [-3, -3, 3, 3], color='#d8d8e0', ec=INK, lw=0.8)              # plate B through it
for sgn in (-1, 1): ax.fill([sgn * 0.5, sgn * 0.68, sgn * 0.68, sgn * 0.5], [-0.5, -0.5, 0.5, 0.5], color=TEAL, ec='none')
ax.text(0.9, 0.9, 'felt or rubber\nlining (0.2-0.5 mm)', fontsize=7, color=TEAL); ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5)
fig.text(0.54, 0.115, '4. Slot lining', fontsize=10, weight='bold')
fig.text(0.54, 0.04, 'Metal does not grip like cardboard. A thin\nlining in each slot takes up the cutting\nclearance: no rattle, a snug slide, and the\nfinish is not scratched.', fontsize=7.5, va='bottom')
fig.text(0.5, 0.012, 'DICTO · dictospheres.com · sketch of ideas, not an engineering drawing', ha='center', fontsize=6.5, color='#555')
fig.savefig(sys.argv[1]); print('written', sys.argv[1])
