# Radial strip (DICTO, 2026-10-16): the up-down toggle at a glance (matplotlib; run with ~/plotenv/bin/python on dicto-node).
# Radius on a log scale. Top row: the original Spheres of Dharma, each station a dot at the geometric mean of its face distance d
# and corner radius R, with a thin line from d to R; repeated by phi^3. Bottom row: its polar image in the toggle sphere; station
# X goes to rho^2/R .. rho^2/d. Dashed: the mirror spheres rho * phi^(3k/2). Grey links join each station to its image. Black:
# stations the two cycles share. Input data/radial-strip-stations.json (from polar.py, d and R per station).
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.ticker
p = (1 + 5 ** .5) / 2
ST = json.load(open('data/radial-strip-stations.json'))
dual = {'I': 'D', 'ID': 'RT', 'D': 'I', 'TI': 'PD', 'H': 'O', 'RT': 'ID'}
warm = {'I': '#d4a017', 'ID': '#ef8a3c', 'D': '#d9534f', 'TI': '#e07fb4', 'H': '#a974d6', 'RT': '#8d6e63'}
cool = {'D': '#00838f', 'RT': '#1e88e5', 'I': '#3949ab', 'PD': '#26a69a', 'O': '#7e57c2', 'ID': '#5c6bc0'}
r0, r1 = 0.22, 8.5
fig, axes = plt.subplots(2, 1, figsize=(13, 7.4), facecolor='#f4f1ea')
for ax, (title, r2) in zip(axes, [('Ends shared: toggle sphere ρ = φ/2 (ρ² = φ²/4)', p * p / 4), ('Middle shared: toggle sphere ρ = φ√3/2 (ρ² = 3φ²/4)', 3 * p * p / 4)]):
    ax.set_facecolor('#f4f1ea'); ax.set_xscale('log'); ax.set_xlim(r0, r1); ax.set_ylim(-0.75, 1.75)
    rho = r2 ** .5
    for k in range(-8, 9):
        m = rho * p ** (1.5 * k)
        if r0 < m < r1: ax.axvline(m, color='#9a7a1c', ls='--', lw=1, zorder=0)
    orig = [(n, d * p ** (3 * k), R * p ** (3 * k)) for k in range(-3, 4) for n, d, R in ST]
    flip = [(dual[n], r2 / R, r2 / d) for n, d, R in orig]
    same = lambda a, b, L: any(abs(a - c) < 1e-6 and abs(b - e) < 1e-6 for _, c, e in L)
    for (n, d, R), (fn, a, b) in zip(orig, flip):
        g1, g2 = np.sqrt(d * R), np.sqrt(a * b)
        if r0 < g1 < r1 and r0 < g2 < r1: ax.plot([g1, g2], [0.92, 0.08], color='#c9bfae', lw=0.7, zorder=1)
    for row, L, other, pal, y in [('yours', orig, flip, warm, 1.0), ('flipped', flip, orig, cool, 0.0)]:
        vis = sorted([t for t in L if r0 < np.sqrt(t[1] * t[2]) < r1], key=lambda t: t[1] * t[2])
        for i, (n, a, b) in enumerate(vis):
            sh = same(a, b, other); c = '#1d1a16' if sh else pal[n]; g = np.sqrt(a * b)
            ax.plot([a, b], [y, y], color=c, lw=2.2, alpha=0.55, solid_capstyle='butt', zorder=2)
            ax.plot([g], [y], 'o', color=c, ms=8 if sh else 6, zorder=3)
            tier = (0.22 + 0.2 * (i % 3)) * (1 if y > 0.5 else -1)
            ax.text(g, y + tier, n, ha='center', va='center', fontsize=10, color=c, fontweight='bold' if sh else 'normal')
    ax.set_yticks([0, 1]); ax.set_yticklabels(['flipped', 'yours']); ax.tick_params(axis='y', length=0)
    ax.set_xticks([0.25, 0.5, 1, 2, 4, 8]); ax.set_xticklabels(['0.25', '0.5', '1', '2', '4', '8']); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
    ax.set_title(title + '; mirror spheres dashed, every φ^(3/2)', loc='left', fontsize=12, fontweight='bold', color='#2b2620')
fig.text(0.01, 0.034, 'Radius on a log scale · dot = geometric mean of face distance and corner radius, line = their range · '
         'H = Hecatodihedron, O = Ogdoecontahedron, PD = pentakis dodecahedron · black = shared by both cycles', ha='left', fontsize=8.5, color='#5b5346')
fig.text(0.99, 0.008, 'DICTO · dictospheres.com', ha='right', fontsize=9, fontweight='bold', color='#5b5346')
fig.tight_layout(rect=(0, 0.055, 1, 1)); fig.savefig('renders/radial-strip.png', dpi=160, facecolor='#f4f1ea'); fig.savefig('renders/radial-strip.svg', facecolor='#f4f1ea')
print('written')
