# Figure 2: the angle at an edge read from the solid alone (Lean study 2, Dehn2Local.lean, wedgeAngle), and why a cut keeps it
# (wedgeAngle_split, wedgeAngle_mem_ratPi_of_line). Diagram only; colours are labels (neutral palette).
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge, Circle

SOLID, CONE, CONE2, INK = '#d9c7a3', '#5b6f8a', '#9aaac0', '#1f1f1f'
fig, axs = plt.subplots(1, 4, figsize=(13, 3.9), dpi=220)

# (a) an edge of a solid, the plane across the edge at a point x, and the cone of directions that stay in the solid
ax = axs[0]
def P(x, y, z): return np.array([x + 0.42 * y, z + 0.30 * y])      # oblique projection
th = np.radians(70)
f1 = [P(0, 0, -1.2), P(0, 0, 1.2), P(1.6, 0, 1.2), P(1.6, 0, -1.2)]                       # face 1: the half-plane y = 0, x > 0
d2 = np.array([np.cos(th), np.sin(th)])
f2 = [P(0, 0, -1.2), P(0, 0, 1.2), P(*(1.6 * d2), 1.2), P(*(1.6 * d2), -1.2)]             # face 2 through the edge (the z axis)
ax.add_patch(Polygon(f1, fc=SOLID, ec=INK, lw=1.0, alpha=0.8))
ax.add_patch(Polygon(f2, fc=SOLID, ec=INK, lw=1.0, alpha=0.55))
t = np.linspace(0, th, 40)
ax.add_patch(Polygon([P(0, 0, 0)] + [P(0.75 * np.cos(a), 0.75 * np.sin(a), 0) for a in t], fc=CONE, ec='none', alpha=0.9))
c = np.linspace(0, 2 * np.pi, 120)
ax.plot(*np.array([P(0.75 * np.cos(a), 0.75 * np.sin(a), 0) for a in c]).T, color=INK, lw=0.8, ls=(0, (2, 2)))
ax.plot(*np.array([P(0, 0, -1.5), P(0, 0, 1.5)]).T, color=INK, lw=2.4)
ax.plot(*P(0, 0, 0), 'o', color=INK, ms=4)
ax.text(*(P(0, 0, 0) + [-0.18, -0.05]), 'x', fontsize=11, ha='right')
ax.text(*(P(0, 0, 1.5) + [0.05, 0.05]), 'edge', fontsize=9)
ax.text(-0.85, -1.70, 'dashed: unit disc across the edge at x', fontsize=8.5)
ax.set_title('(a) the cone of directions at x', fontsize=10)

# (b) the disc in its plane: the angle is 2π × (shaded area) / (area of the disc)
ax = axs[1]
ax.add_patch(Circle((0, 0), 1, fc='white', ec=INK, lw=1.0, ls=(0, (2, 2))))
ax.add_patch(Wedge((0, 0), 1, 0, 70, fc=CONE, ec=INK, lw=1.0))
ax.text(0.33, 0.20, 'θ', color='white', fontsize=13, ha='center', va='center')
ax.text(0, -1.33, 'θ = 2π · area / π\n(sector of angle θ has area θ/2)', fontsize=8.5, ha='center')
ax.set_title('(b) angle = share of the disc', fontsize=10)

# (c) a plane through the edge cuts the cone in two; the two angles add up
ax = axs[2]
ax.add_patch(Circle((0, 0), 1, fc='white', ec=INK, lw=1.0, ls=(0, (2, 2))))
ax.add_patch(Wedge((0, 0), 1, 0, 30, fc=CONE, ec=INK, lw=1.0))
ax.add_patch(Wedge((0, 0), 1, 30, 70, fc=CONE2, ec=INK, lw=1.0))
ax.plot([-1.15 * np.cos(np.radians(30)), 1.15 * np.cos(np.radians(30))], [-1.15 * np.sin(np.radians(30)), 1.15 * np.sin(np.radians(30))], color=INK, lw=1.6)
ax.text(0.55, 0.14, 'θ₁', fontsize=11, ha='center'); ax.text(0.30, 0.55, 'θ₂', fontsize=11, ha='center')
ax.text(0, -1.33, 'θ = θ₁ + θ₂\n(cutting plane through the edge)', fontsize=8.5, ha='center')
ax.set_title('(c) a cut through an edge', fontsize=10)

# (d) a cut across a face makes a new edge: the two new angles make a straight angle, π, which is 0 modulo rational multiples of π
ax = axs[3]
ax.add_patch(Circle((0, 0), 1, fc='white', ec=INK, lw=1.0, ls=(0, (2, 2))))
ax.add_patch(Wedge((0, 0), 1, 0, 115, fc=CONE, ec=INK, lw=1.0))
ax.add_patch(Wedge((0, 0), 1, 115, 180, fc=CONE2, ec=INK, lw=1.0))
ax.plot([-1.15, 1.15], [0, 0], color=INK, lw=2.0)
ax.plot([0, 1.15 * np.cos(np.radians(115))], [0, 1.15 * np.sin(np.radians(115))], color=INK, lw=1.6)
ax.text(0.30, 0.40, 'θ₁', fontsize=11, ha='center', color='white'); ax.text(-0.62, 0.22, 'θ₂', fontsize=11, ha='center')
ax.text(0, -1.33, 'θ₁ + θ₂ = π ≡ 0\n(new edge on a face of the solid)', fontsize=8.5, ha='center')
ax.set_title('(d) a cut across a face', fontsize=10)

for ax in axs:
    ax.set_aspect('equal'); ax.axis('off')
axs[0].set_xlim(-0.9, 2.5); axs[0].set_ylim(-1.75, 1.95)
for ax in axs[1:]:
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.75, 1.35)
plt.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.02, wspace=0.08)
plt.savefig('../figures/fig-wedge.png', facecolor='white')
print('FINAL ok')
