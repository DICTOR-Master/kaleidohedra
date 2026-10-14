# Golden and silver members (DICTO, 2026-10-14): the n = 4 and n = 5 members of the antiprism theorem, r = 2cos(pi/n) - 1. Each column:
# the member's flat-ended triangle (sides 1 and r), and its antiprism seen down the axis (two n-gons turned by pi/n: a regular 2n-gon
# outline, the octagon for the silver member). DICTO · dictospheres.com
import os, math
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'paper', 'figures')
BG, FG, MUT = '#14110d', '#e9e6df', '#a39d90'; GOLD, SILVER, WIST = '#ffc857', '#c9d3dc', '#c792ea'
def hexagon(r):   # flat-ended triangle: an equilateral triangle of side 1 + 2r with corners cut by r
    s = 1 + 2 * r; T = [np.array([math.cos(a), math.sin(a)]) * s / math.sqrt(3) for a in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3, math.pi / 2 + 4 * math.pi / 3)]
    P = []
    for i in range(3):
        A, B = T[i], T[(i + 1) % 3]; d = (B - A) / s; P += [A + d * r, B - d * r]
    return np.array(P)
fig, axs = plt.subplots(2, 2, figsize=(9, 9), facecolor=BG)
for col, (n, name, colour, rs) in enumerate([(4, 'silver: n = 4, r = √2 − 1 = 1/(1 + √2)', SILVER, math.sqrt(2) - 1), (5, 'golden: n = 5, r = 1/φ (FUJI)', GOLD, (math.sqrt(5) - 1) / 2)]):
    assert abs(rs - (2 * math.cos(math.pi / n) - 1)) < 1e-12
    ax = axs[0, col]; H = hexagon(rs); ax.add_patch(Polygon(H, closed=True, fc=colour, ec=FG, alpha=.9, lw=1.5))
    for i in range(6):
        m = (H[i] + H[(i + 1) % 6]) / 2; L = np.linalg.norm(H[i] - H[(i + 1) % 6]); o = m / np.linalg.norm(m) * 0.13
        ax.text(*(m + o), '1' if abs(L - 1) < 1e-9 else f'{L:.3f}', color=FG, ha='center', va='center', fontsize=10)
    ax.set_title(name, color=FG, fontsize=11)
    ax = axs[1, col]; R = 1 / (2 * math.sin(math.pi / n))
    top = np.array([[R * math.cos(2 * math.pi * k / n), R * math.sin(2 * math.pi * k / n)] for k in range(n)])
    bot = np.array([[R * math.cos(2 * math.pi * k / n + math.pi / n), R * math.sin(2 * math.pi * k / n + math.pi / n)] for k in range(n)])
    out = np.array([top[k // 2] if k % 2 == 0 else bot[k // 2] for k in range(2 * n)])
    ax.add_patch(Polygon(out, closed=True, fc='none', ec=colour, lw=2.5))
    ax.add_patch(Polygon(bot, closed=True, fc=WIST, ec=FG, alpha=.35, lw=1)); ax.add_patch(Polygon(top, closed=True, fc=colour, ec=FG, alpha=.55, lw=1))
    ax.set_title(f'{"square" if n == 4 else "pentagonal"} antiprism down its axis: a regular {"octagon" if n == 4 else "decagon"}', color=FG, fontsize=11)
for ax in axs.flat: ax.set_aspect('equal'); ax.autoscale_view(); ax.margins(0.18); ax.axis('off'); ax.set_facecolor(BG)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', color=MUT, ha='right', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig9-golden-silver.png'), dpi=150, facecolor=BG); print('ok')
