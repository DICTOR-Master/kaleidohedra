# Figure 3: the canon. Left: the solids proved to have Dehn invariant zero; right: those proved nonzero, in their two angle families.
# Every line is a non-congruence proved in Lean (studies 2026-11-19-lean-dehn-6, -7 and -8). Node colours: the app colour of the solid
# it stands for (Platonic solids in the element colours; AXE cyan, CLEO and FUJI lilac); other solids and the boxes neutral.
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

D, I, C, T, O = '#8a5cc4', '#3a70cd', '#488e48', '#cd3e28', '#e8c852'
AXE, LIL, NEU, INK, BOX = '#4dd0e1', '#c792ea', '#e6e1d6', '#1f1f1f', '#f4f1ea'
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=220)

def box(x, y, w, h, title):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.12', fc=BOX, ec='#8c8475', lw=1.2))
    ax.text(x + w / 2, y + h - 0.22, title, ha='center', va='top', fontsize=10.5, fontweight='bold')

def node(x, y, label, col, w=1.75, sub=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.24), w, 0.48, boxstyle='round,pad=0.02,rounding_size=0.1', fc=col, ec=INK, lw=0.9, zorder=4))
    dark = col in (D, I, C, T)
    ax.text(x, y + (0.06 if sub else 0), label, ha='center', va='center', fontsize=9, color='white' if dark else INK, zorder=5)
    if sub: ax.text(x, y - 0.12, sub, ha='center', va='center', fontsize=7, color='white' if dark else '#444', zorder=5)

# zero
box(0.1, 0.2, 3.3, 6.0, 'Dehn invariant zero')
zero = [('cube', C, None), ('rhombic dodecahedron', NEU, None), ('cube ∩ rhombic dodecahedron', NEU, 'every cut; fair 18-face die'),
        ('truncated octahedron', NEU, 'cube ∩ octahedron, t = 3/2'), ('rhombic triacontahedron', NEU, 'and every solid on 2-fold normals'),
        ('golden rhombohedron, prolate', NEU, None), ('golden rhombohedron, oblate', NEU, None)]
for k, (l, c, s) in enumerate(zero): node(1.75, 5.35 - 0.72 * k, l, c, w=2.9, sub=s)

# nonzero, alpha-beta family: complete graph on five
box(4.3, 0.2, 4.4, 6.0, 'nonzero, over α and β')
cx, cy, R = 6.5, 3.0, 1.6
ab = [('dodecahedron', D), ('icosahedron', I), ('CLEO', LIL), ('AXE', AXE), ('FUJI', LIL)]
pos = [(cx + R * np.sin(2 * np.pi * k / 5), cy + R * np.cos(2 * np.pi * k / 5)) for k in range(5)]
for i in range(5):
    for j in range(i + 1, 5):
        ax.plot(*zip(pos[i], pos[j]), color='#3d3d3d', lw=1.3, zorder=2)
for (l, c), (x, y) in zip(ab, pos): node(x, y, l, c, w=1.4)
ax.text(cx, 0.42, 'all 10 pairs proved', ha='center', fontsize=8.5, color='#3d3d3d')

# nonzero, arccos(1/3) family: tetrahedron-octahedron, low cuts-tetrahedron, high cuts-octahedron (opposite signs only)
box(9.4, 0.2, 2.55, 6.0, 'nonzero, over\narccos(1/3)')
X = 10.45
tp, lo, hi, op = (X, 4.75), (X, 3.55), (X, 2.35), (X, 1.15)
ax.plot([X, X], [tp[1], lo[1]], color='#3d3d3d', lw=1.3, zorder=2)
ax.plot([X, X], [hi[1], op[1]], color='#3d3d3d', lw=1.3, zorder=2)
ax.plot([X + 0.8, 11.65, 11.65, X + 0.8], [tp[1], tp[1], op[1], op[1]], color='#3d3d3d', lw=1.3, zorder=2)
node(*tp, 'tetrahedron', T, w=1.6, sub='+12√2 ⊗ arccos(1/3)')
node(*lo, 'cube ∩ octahedron', NEU, w=1.6, sub='1 < t < 3/2: sign −')
node(*hi, 'cube ∩ octahedron', NEU, w=1.6, sub='3/2 < t < 2: sign +')
node(*op, 'octahedron', O, w=1.6, sub='−12√2 ⊗ arccos(1/3)')
ax.text(X - 0.08, 1.78, 'fair 14-face die:\nt ≈ 1.757', ha='right', fontsize=7, color='#444')
ax.text(10.675, 0.42, 'pairs of opposite sign', ha='center', fontsize=8.5, color='#3d3d3d')

# zero vs nonzero
ax.add_patch(FancyArrowPatch((3.45, 6.45), (11.9, 6.45), arrowstyle='<->', mutation_scale=14, lw=1.4, color=INK,
                             connectionstyle='arc3,rad=0'))
ax.text(7.7, 6.6, 'no similar copy of a nonzero solid is scissors congruent to a similar copy of a zero solid',
        ha='center', fontsize=9)
# across the two nonzero families: all 15 pairs proved (study 8)
ax.add_patch(FancyArrowPatch((8.75, 3.0), (9.35, 3.0), arrowstyle='<->', mutation_scale=12, lw=1.4, color=INK))
ax.text(9.05, 3.15, 'all 15\npairs', ha='center', va='bottom', fontsize=7.5, color='#3d3d3d', linespacing=1.0)
ax.set_xlim(0, 12); ax.set_ylim(0, 6.9); ax.set_aspect('equal'); ax.axis('off')
plt.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
plt.savefig('../figures/fig-canon.png', facecolor='white')
print('FINAL ok')
