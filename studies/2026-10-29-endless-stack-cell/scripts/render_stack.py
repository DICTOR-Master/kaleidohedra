# Stacked layer tiles (HexOct, DICTO's name 2026-10-29; was Endless Stack Cell): five consecutive layers of a mixed stacking, each layer a 2x2 patch of
# its tile, coloured by type (c gold, h blue); left closed, right with the layers drawn apart so the interlocking spikes show.
import sys, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tiles import tile, types
from render_tiles import faces, cart
from stackings import POS
lam = Fr(sys.argv[1]) if len(sys.argv) > 1 else Fr(1, 10)
word = 'ABCBCACB'; T = types(word); Ls = range(1, 6)
COL = {'c': ['#d9a521', '#e8c25a'], 'h': ['#3f7fc4', '#7fb0e0']}
fig = plt.figure(figsize=(13, 9), facecolor='white')
for col, gap in enumerate((0.0, 0.55)):
    ax = fig.add_subplot(1, 2, col + 1, projection='3d'); ax.set_proj_type('ortho'); allp = []
    for L in Ls:
        P, _ = tile(word, L, lam); ball = POS[word[L]]
        for du, dv in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            for k, up, s, pts, J in P:
                Q = np.array([cart((p[0] + ball[0] + du, p[1] + ball[1] + dv, p[2] + L)) for p in pts]) + [0, 0, gap * L]
                allp.append(Q)
                ax.add_collection3d(Poly3DCollection(faces(Q), facecolor=COL[T[L]][k == 'oct'], edgecolor='#222', linewidth=0.35, alpha=0.9))
    A = np.vstack(allp); c = A.mean(0); r = (A.max(0) - A.min(0)).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=8, azim=-60); ax.set_axis_off()
    ax.set_title('closed' if not gap else 'layers drawn apart', fontsize=11)
fig.suptitle('HexOct (DICTO): five layers of ' + word + ', types ' + ' '.join(T[L] for L in Ls) + ' (bottom to top)', fontsize=12)
fig.text(0.5, 0.03, f'λ = {lam}. Each layer is a 2×2 patch of its tile: gold = c-tile, blue = h-tile (darker: tetrahedral pieces, lighter: octahedral halves). '
         'Any tile sits on any tile; the tetrahedral spikes key each layer into the next.', ha='center', fontsize=9, wrap=True)
fig.text(0.98, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=8, color='#777')
plt.subplots_adjust(left=0, right=1, top=0.93, bottom=0.07, wspace=0)
plt.savefig('../stack_' + str(lam).replace('/', '_').replace('-', 'm') + '.png', dpi=130); print('saved', [T[L] for L in Ls])
