# 2D figures for the FUJI family paper (DICTO, 2026-10-14): Odom's construction and the antiprism members. Run on dicto-node.
# DICTO · dictospheres.com
import math, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'paper', 'figures')
phi = (1 + 5 ** .5) / 2
BG, FG, LIL, CY, GO = '#14110d', '#e9e6df', '#c792ea', '#4dd0e1', '#ffc857'
# Odom: unit triangle, each side extended by e at both ends; the six outer points make the flat-ended triangle (sides e, 1 + e)
fig, axs = plt.subplots(1, 3, figsize=(15, 5.2), facecolor=BG)
for ax, e, title in zip(axs, (1 / phi, 1.0, phi), ('e = 1/φ: r = 1/φ²', 'e = 1: r = 1/2 (the space-filler)', 'e = φ: r = 1/φ (FUJI)')):
    A, B, C = (0, 0), (1, 0), (.5, 3 ** .5 / 2); P = []
    for X, Y in ((A, B), (B, C), (C, A)):
        u = (Y[0] - X[0], Y[1] - X[1])
        ax.plot([X[0] - e * u[0], Y[0] + e * u[0]], [X[1] - e * u[1], Y[1] + e * u[1]], color=FG, lw=.8, alpha=.5)
        P += [(X[0] - e * u[0], X[1] - e * u[1]), (Y[0] + e * u[0], Y[1] + e * u[1])]
    c = (.5, 3 ** .5 / 6); P.sort(key=lambda p: math.atan2(p[1] - c[1], p[0] - c[0]))
    ax.fill([p[0] for p in P], [p[1] for p in P], color=LIL, alpha=.55, lw=0)
    ax.plot([p[0] for p in P + P[:1]], [p[1] for p in P + P[:1]], color=LIL, lw=2)
    ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color=GO, alpha=.9)
    ax.set_title(title, color=FG, fontsize=15); ax.set_aspect('equal'); ax.axis('off'); ax.set_facecolor(BG)
fig.text(.5, .02, "Odom's construction: extend each side of the gold triangle by e at both ends; the six ends make a flat-ended triangle with sides e and 1 + e.", color=FG, ha='center', fontsize=12)
fig.text(.99, .005, 'DICTO · dictospheres.com', color='#8a8578', ha='right', fontsize=9)
fig.savefig(os.path.join(OUT, 'fig2-odom.png'), dpi=150, facecolor=BG); plt.close(fig)
# The antiprism theorem: r = 2 cos(pi/n) - 1
fig, ax = plt.subplots(figsize=(11, 5.6), facecolor=BG); ax.set_facecolor(BG)
ns = list(range(3, 13)); rs = [2 * math.cos(math.pi / n) - 1 for n in ns]
xs = [i / 100 for i in range(300, 1301)]; ax.plot(xs, [2 * math.cos(math.pi / x) - 1 for x in xs], color=FG, lw=1, alpha=.4)
ax.scatter(ns, rs, color=[LIL if n == 5 else CY for n in ns], s=[160 if n == 5 else 60 for n in ns], zorder=3)
lab = {3: 'octahedron → tetrahedron (r = 0)', 4: 'square antiprism: √2 − 1', 5: 'pentagonal antiprism (icosahedron): 1/φ, FUJI', 6: 'hexagonal antiprism: √3 − 1'}
for n, t in lab.items(): ax.annotate(t, (n, 2 * math.cos(math.pi / n) - 1), xytext=(14, -6), textcoords='offset points', color=FG, fontsize=11)
ax.axhline(1, color=FG, lw=.6, ls=':', alpha=.6); ax.text(12.9, 1.01, 'flat regular hexagon', color=FG, ha='right', va='bottom', fontsize=10)
ax.set_xlabel('n (the antiprism)', color=FG); ax.set_ylabel('r (the FUJI-family member)', color=FG)
ax.tick_params(colors=FG); [s.set_color('#5a564e') for s in ax.spines.values()]; ax.set_xticks(ns); ax.set_ylim(-.05, 1.08)
ax.set_title('r = 2 cos(π/n) − 1: the member whose base lies flat with the antiprism\'s triangles', color=FG, fontsize=13)
fig.text(.99, .005, 'DICTO · dictospheres.com', color='#8a8578', ha='right', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig3-antiprisms.png'), dpi=150, facecolor=BG); plt.close(fig)
print('ok')
