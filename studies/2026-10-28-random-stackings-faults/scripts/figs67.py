# Figures of #67. Fig 1: the six classical stacking faults as strips of layers (cubic / hexagonal by Jagodzinski's rule).
# Fig 2: the diamond / ice framework (#60's pyrochlore run: balls and diamond atoms of weight lam, holes 0) at lam = 1/16:
# volume per layer of the ball pieces against the hexagonality, exact line, with measured stacking-disordered ice marked
# (cubicity 73.3%, Malkin et al. 2015; 78%, Amaya et al. 2017) and the pure stackings.
import os
from fractions import Fraction as F
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures'); os.makedirs(OUT, exist_ok=True)
BG, INK, MUTED, C_C, C_H = 'white', '#1a1a1a', '#666666', '#3f7cb8', '#a9862a'
def types(w, pad=4): return ''.join('h' if w[k - 1] == w[k + 1] else 'c' for k in range(pad, len(w) - pad))
FAULTS = [('cubic crystal, perfect', 'ABCABCABCABCABCABC'), ('twin boundary', 'ABCABCABCBACBACBAC'),
          ('intrinsic fault', 'ABCABCABCBCABCABCA'), ('extrinsic fault', 'ABCABCABCBABCABCAB'),
          ('hexagonal crystal, perfect', 'ABABABABABABABABAB'), ('growth fault I1', 'ABABABABCBCBCBCBCB'),
          ('deformation fault I2', 'ABABABABCACACACACA'), ('extrinsic fault E', 'ABABABABCABABABABA')]
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200); ax.set_axis_off()
for r, (name, w) in enumerate(FAULTS):
    y = len(FAULTS) - r - (0.6 if r >= 4 else 0)
    t = types(w); full = w[4:len(w) - 4]
    for k, (ch, letter) in enumerate(zip(t, full)):
        ax.add_patch(plt.Rectangle((k, y), 0.92, 0.8, color=C_C if ch == 'c' else C_H, ec='white', lw=2))
        ax.text(k + 0.46, y + 0.4, letter, ha='center', va='center', color='white', fontsize=9, weight='bold')
    base = t.count('h') if r < 4 else t.count('c')
    ax.text(-0.4, y + 0.4, name, ha='right', va='center', color=INK, fontsize=10)
    ax.text(len(t) + 0.4, y + 0.4, f"{t.count('h')} h", ha='left', va='center', color=MUTED, fontsize=9)
ax.add_patch(plt.Rectangle((0, -0.9), 0.92, 0.6, color=C_C)); ax.text(1.2, -0.6, 'cubic layer (c)', va='center', fontsize=9, color=INK)
ax.add_patch(plt.Rectangle((5.5, -0.9), 0.92, 0.6, color=C_H)); ax.text(6.7, -0.6, 'hexagonal layer (h)', va='center', fontsize=9, color=INK)
ax.set_xlim(-8, 13); ax.set_ylim(-1.2, 9)
fig.text(0.98, 0.02, 'DICTO', color='#b8962e', fontsize=12, ha='right', family='serif', weight='bold')
fig.savefig(os.path.join(OUT, 'faults.png'), bbox_inches='tight', facecolor=BG); plt.close(fig)
lam = F(1, 16)
cc = -(80 * lam**3 - 27 * lam - 6) / 24
hh = -(4928 * lam**3 + 720 * lam**2 - 1908 * lam - 405) / 1536
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=200)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.set_axisbelow(True); ax.grid(axis='y', color='#e5e5e5')
ax.plot([0, 1], [float(cc), float(hh)], color=C_H, lw=2)
pts = [('cubic stacking (3C)', F(0), (8, 8)), ('ice I$_{sd}$, 78% cubic', F(22, 100), (10, -14)), ('ice I$_{sd}$, 73.3% cubic', F(267, 1000), (-40, 12)),
       ('a random stacking, h = 1/2', F(1, 2), (8, 8)), ('hexagonal stacking (2H)', F(1), (-150, 6))]
for name, h, off in pts:
    y = cc + h * (hh - cc)
    ax.scatter([float(h)], [float(y)], s=60, color=C_H, edgecolor='white', linewidth=1.5, zorder=3)
    ax.annotate(name, (float(h), float(y)), xytext=off, textcoords='offset points', fontsize=9, color=INK)
ax.set_xlabel('hexagonality h (share of hexagonal layers)', fontsize=10, color=INK)
ax.set_ylabel('ball piece volume per layer', fontsize=10, color=INK)
ax.set_title('Diamond / ice framework (balls and diamond atoms, weight λ = 1/16): exact straight line in h', fontsize=10, loc='left', color=INK)
ax.tick_params(colors=MUTED, labelsize=9)
fig.text(0.98, 0.01, 'DICTO', color='#b8962e', fontsize=12, ha='right', family='serif', weight='bold')
fig.savefig(os.path.join(OUT, 'ice-line.png'), bbox_inches='tight', facecolor=BG); plt.close(fig)
print('ok', float(cc), float(hh))
