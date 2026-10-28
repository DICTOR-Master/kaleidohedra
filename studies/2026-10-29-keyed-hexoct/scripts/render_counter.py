# Figure: the HexOct-K layer that counts (counter.py), drawn on the layer's own lattice (60-degree axes u, v).
# Each tile is a hexagon at its ball; gold = bit 1, pale = bit 0; row v spells v in binary (most significant bit at u = 0).
import math, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from counter import fillings
W, H = 4, 16
sol = fillings(W, H)[0]
fig, ax = plt.subplots(figsize=(7.2, 8.6))
for v in range(H):
    for u in range(W):
        b = 0 if v == 0 else sol[(v, u)]
        x, y = u + v / 2, v * math.sqrt(3) / 2
        ax.add_patch(RegularPolygon((x, y), 6, radius=0.56, orientation=0, facecolor='#d9a521' if b else '#f3efe4',
                                    edgecolor='#555', lw=0.8))
        ax.text(x, y, str(b), ha='center', va='center', fontsize=9, color='#222')
    ax.text(W - 0.2 + v / 2, v * math.sqrt(3) / 2, f'= {v}', ha='left', va='center', fontsize=9, color='#444')
ax.annotate('carry 1 enters every row', xy=(W - 0.45 + 0.0, -0.75), fontsize=8.5, color='#444')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-0.8, W + H / 2 + 0.8); ax.set_ylim(-1.1, H * math.sqrt(3) / 2 + 0.3)
ax.text(-0.7, H * math.sqrt(3) / 2 + 0.1, 'DICTO · HexOct-K layer: 4 keyed tiles, one filling, rows count 0 to 15', fontsize=9, color='#333')
plt.savefig('../out/counter.png', dpi=200, bbox_inches='tight')
print('written')
