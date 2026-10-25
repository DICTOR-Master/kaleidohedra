# Figure: (left) one gap seen from the side — layer k on position X, layer k+1 on Y, the octahedral hole over Z at mid-height and the
# two tetrahedral holes over X (near layer k+1) and over Y (near layer k); (right) a stacking column ABAC… with each layer's h/c type
# and which pure piece each hole takes. Drawn in the plane through the three positions (A, B, C one third apart).
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = (2 / 3) ** 0.5; xs = {'A': 0.0, 'B': 1 / 3 ** 0.5, 'C': 2 / 3 ** 0.5}
GOLD, BLUE, GREY, INK = '#c99a2e', '#4a6fc4', '#9aa3ad', '#2b2f36'
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw={'width_ratios': [1.15, 1]})
for ax in (a1, a2): ax.set_aspect('equal'); ax.axis('off')
# left: one gap (X = A, Y = B, Z = C)
for z, pos, lab in ((0, 'A', 'layer k (position X)'), (d, 'B', 'layer k+1 (position Y)')):
    for s in (0, 1):
        a1.add_patch(plt.Circle((xs[pos] + s * 3 ** 0.5, z), 0.5, fc='#e9ecf1', ec=GREY, lw=0.8, alpha=0.55))
        a1.plot(xs[pos] + s * 3 ** 0.5, z, '.', color=GREY)
    a1.text(-0.75, z, lab, va='center', ha='right', fontsize=9, color=INK)
a1.plot([-0.6, 2.4], [d / 2] * 2, ls='--', lw=0.8, color=GREY); a1.text(2.45, d / 2, 'mid-plane', va='center', fontsize=8, color=GREY)
a1.plot(xs['C'], d / 2, 'o', ms=10, color='#7b5cc4'); a1.annotate('octahedral hole over Z,\nheight ½ (on the mid-plane)', (xs['C'], d / 2), (2.45, d + 0.55), fontsize=8, color=INK, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.7))
a1.plot(xs['A'], 3 * d / 4, '^', ms=9, color=GOLD); a1.annotate('tetrahedral hole over X, height ¾:\nnearest layer k+1', (xs['A'], 3 * d / 4), (-2.8, d + 0.6), fontsize=8, color=INK, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.7))
a1.plot(xs['B'], d / 4, 'v', ms=9, color=GOLD); a1.annotate('tetrahedral hole over Y, height ¼:\nnearest layer k', (xs['B'], d / 4), (1.2, -0.85), fontsize=8, color=INK, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.7))
a1.set_xlim(-3.0, 3.6); a1.set_ylim(-1.05, d + 0.95); a1.set_title('One gap between two layers', fontsize=11, color=INK)
# right: a stacking column with h/c
word = 'ABACAB'; n = len(word)
typ = ['h' if word[(k - 1) % n] == word[(k + 1) % n] else 'c' for k in range(n)]
for k, (pos, t) in enumerate(zip(word, typ)):
    y = k * 0.62; col = BLUE if t == 'h' else GOLD
    a2.add_patch(plt.Rectangle((0, y - 0.2), 2.2, 0.4, fc=col, alpha=0.25, ec=col))
    a2.text(0.15, y, f'layer {k}: {pos}', va='center', fontsize=9, color=INK); a2.text(1.75, y, t, va='center', fontsize=11, weight='bold', color=col)
    if k < n - 1:
        a2.text(2.4, y + 0.31, f'octahedral piece: bottom {typ[k]}, top {typ[k + 1]}', va='center', fontsize=7.5, color=INK)
a2.text(0, -0.65, 'h: both neighbours on the same position (hexagonal)\nc: neighbours on different positions (cubic)', fontsize=8, color=INK)
a2.set_xlim(-0.1, 5.2); a2.set_ylim(-1.0, n * 0.62); a2.set_title('A stacking, layer by layer (ABACAB…)', fontsize=11, color=INK)
fig.text(0.985, 0.02, 'DICTO', ha='right', fontsize=9, color='#b8962e')
plt.tight_layout(); plt.savefig('fig1-gap.png', dpi=160)
