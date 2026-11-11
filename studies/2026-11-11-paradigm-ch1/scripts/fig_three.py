"""Chapter 1 figure: the six orders of three values as a hexagon, for equal gaps (regular), gaps 1:2 (the DICTO 1:2's hexagon) and
gaps 1:tau (the golden cut). Corners labelled by their orders, sides coloured by the exchange (first pair blue, second pair red)."""
import itertools, sys, math
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
tau = (1 + 5 ** .5) / 2
cases = [('equal gaps: the regular hexagon', (1, 2, 3), ('1', '2', '3')), ('gaps 1 : 2: the DICTO 1:2\'s hexagon', (1, 2, 4), ('1', '2', '4')),
         ('gaps 1 : τ: the golden cut', (0, 1, 1 + tau), ('a', 'b', 'c'))]
B = np.array([[1, -1, 0], [1, 1, -2]]) / np.array([[2 ** .5], [6 ** .5]])   # orthonormal basis of x + y + z = 0
fig, axs = plt.subplots(1, 3, figsize=(13, 4.6), dpi=220)
for ax, (title, vals, names) in zip(axs, cases):
    m = sum(vals) / 3; lab = dict(zip(vals, names))
    cyc = [list(vals)]; cur = list(vals)
    for k in range(6):
        lo, hi = (vals[0], vals[1]) if k % 2 == 0 else (vals[1], vals[2])
        cur = [hi if x == lo else lo if x == hi else x for x in cur]; cyc.append(cur[:])
    P = [B @ (np.array(p) - m) for p in cyc]
    ax.fill([p[0] for p in P[:6]], [p[1] for p in P[:6]], color='#f3e9c6', zorder=0)
    for k in range(6):
        ax.plot([P[k][0], P[k + 1][0]], [P[k][1], P[k + 1][1]], color='#2f6fb3' if k % 2 == 0 else '#c0392b', lw=3, solid_capstyle='round')
    c = np.mean(P[:6], axis=0)
    for k in range(6):
        d = P[k] - c; d = d / np.linalg.norm(d)
        ax.text(*(P[k] + 0.32 * d), ''.join(lab[x] for x in cyc[k]), ha='center', va='center', fontsize=11, fontweight='bold')
        ax.plot(*P[k], 'o', color='#222', ms=4)
    ax.set_title(title, fontsize=11); ax.set_aspect('equal'); ax.axis('off')
    r = max(np.linalg.norm(p - c) for p in P) + 0.6; ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r)
axs[0].plot([], [], color='#2f6fb3', lw=3, label='exchange of the two smallest values'); axs[0].plot([], [], color='#c0392b', lw=3, label='exchange of the two largest values')
fig.legend(loc='lower center', ncol=2, frameon=False, fontsize=9)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
fig.savefig(sys.argv[1], bbox_inches='tight')
import os; print('FINAL ok' if os.path.getsize(sys.argv[1]) > 30000 else 'FINAL FAIL')
