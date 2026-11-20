# DICTO · dictospheres.com — Figure 2: the two angles at a ridge where a cap meets the 600-cell, against the octet in 3D.
# Each panel is the section by the plane perpendicular to the ridge (4D: a triangle; 3D: an edge). Left: the 600-cell's
# dihedral angle θ600 = 4π/3 − θ5 and the 5-cell cap's θ5 = arccos(1/4) side by side make 4π/3 = 240°, more than a
# straight angle, so the union is not convex there. Right: the octahedron's π − arccos(1/3) and the tetrahedron's
# arccos(1/3) make exactly π, and the faces merge flat. The angles are checked exactly (exact4d.py) before drawing.
# Usage: python3 fig_angles.py   (on a compute host) -> figures/fig-angles.png
import os, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import exact4d as X

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'figures'); os.makedirs(OUT, exist_ok=True)
P = X.six()
c5, c600 = P['5-cell'].cos, P['600-cell'].cos
assert c5 == X.Q5(X.Fr(1, 4)) and c600 == X.Q5(X.Fr(-1, 8), X.Fr(-3, 8))
t5, t600 = math.acos(float(c5)), math.acos(float(c600))
# exact: cos(θ5 + θ600) = −1/2 (sin θ5 sin θ600 = (15 − 3√5)/32 > 0, checked by squares), and θ5 > π/3, θ600 > 5π/6
s5s6_sq = (1 - c5 * c5) * (1 - c600 * c600); prod = X.Q5(X.Fr(15, 32), X.Fr(-3, 32))
assert s5s6_sq == prod * prod and prod.sign() > 0 and c5 * c600 - prod == X.Q5(X.Fr(-1, 2))
assert c5 < X.Q5(X.Fr(1, 2)) and (c600 * c600) > X.Q5(X.Fr(3, 4)) and c600.sign() < 0
assert abs(t5 + t600 - 4 * math.pi / 3) < 1e-14
tt, to = math.acos(1 / 3), math.pi - math.acos(1 / 3)

BG, INK, MUTE = '#140f0b', '#eee6d6', '#b0a594'
NEUTRAL_P, NEUTRAL_C = '#d2c3a0', '#c99a45'          # 600-cell, 5-cell cap: label tones as in Figure 3 (neither is an app solid)
OCT, TET = '#e8c852', '#cd3e28'                      # octahedron yellow, tetrahedron red: the app colours of these solids
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK})
fig, axs = plt.subplots(1, 2, figsize=(10.4, 5.9), facecolor=BG)


def panel(ax, a1, a2, c1, c2, l1, l2, title, sub, total):
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.45, 1.75)
    start = -90 + 0.0                                                      # first face along the downward ray
    d1, d2 = math.degrees(a1), math.degrees(a2)
    ax.add_patch(Wedge((0, 0), 1.0, start, start + d1, fc=c1, ec=BG, lw=1.5, alpha=0.95))
    ax.add_patch(Wedge((0, 0), 1.0, start + d1, start + d1 + d2, fc=c2, ec=BG, lw=1.5, alpha=0.95))
    for ang in (start, start + d1, start + d1 + d2):
        r = math.radians(ang); ax.plot([0, 1.08 * math.cos(r)], [0, 1.08 * math.sin(r)], color=INK, lw=1.6)
    ax.plot([-1.2, 1.2], [0, 0], color=MUTE, lw=1.0, ls=(0, (4, 3)))     # a straight angle through the ridge
    for (a0, d, lab) in ((start, d1, l1), (start + d1, d2, l2)):
        m = math.radians(a0 + d / 2); ax.text(0.6 * math.cos(m), 0.6 * math.sin(m), lab, ha='center', va='center', fontsize=11, color=BG, weight='bold')
    ax.add_patch(Wedge((0, 0), 0.2, start, start + d1 + d2, width=0.035, fc=INK, ec='none'))
    ax.plot(0, 0, 'o', color=INK, ms=6)
    ax.text(-1.32, 1.72, title, fontsize=14, weight='bold', color=INK, va='top')
    ax.text(-1.32, 1.52, sub, fontsize=9.8, color=MUTE, va='top')
    ax.text(0, -1.43, total, fontsize=11.5, color=INK, ha='center', va='bottom')


panel(axs[0], t600, t5, NEUTRAL_P, NEUTRAL_C, f'600-cell\n{math.degrees(t600):.2f}°', f'cap\n{math.degrees(t5):.2f}°',
      'Four dimensions: a cap on the 600-cell', 'section by the plane perpendicular to a triangle\nwhere a capped facet meets an uncapped one',
      'θ₆₀₀ + θ₅ = 4π/3 = 240°: reflex, never convex')
panel(axs[1], to, tt, OCT, TET, f'octahedron\n{math.degrees(to):.2f}°', f'tetrahedron\n{math.degrees(tt):.2f}°',
      'Three dimensions: the octet', 'section by the plane perpendicular to an edge\nwhere a tetrahedron sits on a face of an octahedron',
      '(π − arccos ⅓) + arccos ⅓ = π: the faces merge flat')
fig.text(0.985, 0.02, 'DICTO · dictospheres.com', ha='right', fontsize=9, color=MUTE)
plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.04, wspace=0.04)
fig.savefig(os.path.join(OUT, 'fig-angles.png'), dpi=220, facecolor=BG)
print('fig-angles.png', f'theta5 = {math.degrees(t5):.6f} deg, theta600 = {math.degrees(t600):.6f} deg, sum = {math.degrees(t5 + t600):.6f}')
