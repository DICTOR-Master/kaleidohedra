#!/usr/bin/env python3
"""Walls of Silence, Figure: the five S5-orbit hulls of the 600-cell (A, -A, C3, B, -B), each in the A4 Coxeter plane,
on a dark ground. Same construction as studies/2026-11-16-queens-construct/scripts/fig_orbits.py (exact face lattice
from qlib.Poly; float only for drawing); label colours as Silent Running Figure 2 (A teal, -A cream, C3 slate, B apricot, -B pink; labels only).
Usage: fig_orbits_dark.py <path to queens-construct/scripts> out.png"""
import sys, os
sys.path.insert(0, sys.argv[1])
from qlib import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = sys.argv[2]; C = Checks()
P5, X, Y = build_600()
known = {vkey(q) for S in (X, Y) for q in S} | {vkey(vneg(q)) for S in (X, Y) for q in S}
C3 = [p for p in P5 if vkey(p) not in known]
C(len(C3) == 20, 'C3 has 20 corners (120 = 20 + 20 + 20 + 30 + 30)')
# Label colours (16 Nov 2026, DICTO: app colours only for the solid they stand for): labels only, no element or solid meaning;
# the same palette in Silent Running and Walls of Silence; chosen apart from the five app solid colours, colour-blind checked.
LABEL = {'teal': (32, 168, 158), 'apricot': (240, 168, 138), 'pink': (240, 150, 192), 'slate': (100, 112, 136), 'cream': (240, 230, 190), 'sky': (120, 200, 240), 'taupe': (176, 150, 140), 'aqua': (110, 230, 226)}
LHEX = {k: '#%02x%02x%02x' % v for k, v in LABEL.items()}
sets = [('A', 'golden truncated 5-cell', X, LHEX['teal']), ('−A', 'mirror image of A', [vneg(x) for x in X], LHEX['cream']),
        ('C3', 'expanded 5-cell (uniform)', C3, LHEX['slate']), ('B', 'golden cantellated 5-cell', Y, LHEX['apricot']),
        ('−B', 'mirror image of B', [vneg(y) for y in Y], LHEX['pink'])]
BG = '#05050a'
k = np.arange(5); U = np.cos(2*np.pi*k/5); Vv = np.sin(2*np.pi*k/5); Wd = np.cos(4*np.pi*k/5)
fig, axs = plt.subplots(1, 5, figsize=(20, 5.6), facecolor=BG)
R = 0
for ax, (nm, sub, S, col) in zip(axs, sets):
    H = Poly([to4(p) for p in S]); F = np.array([flt(to5(p)) for p in H.P])
    C(H.fvec[0] == len(S), f'{nm}: hull has {len(S)} corners, f-vector {H.fvec}')
    x, y, z = F @ U, F @ Vv, F @ Wd; z = (z - z.min())/(np.ptp(z) + 1e-12)
    R = max(R, float(np.max(np.hypot(x, y))))
    for e in sorted(H.edges, key=lambda e: sum(z[list(e)])):
        a, b = tuple(e); d = (z[a] + z[b])/2
        ax.plot([x[a], x[b]], [y[a], y[b]], color=col, lw=1.0 + 0.9*d, alpha=0.35 + 0.6*d, solid_capstyle='round')
    ax.scatter(x, y, s=24, color=col, edgecolor='#f0f0f0', linewidth=0.5, zorder=3)
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(f'{nm}  ({len(S)} corners)\n{sub}\nf = {H.fvec}', fontsize=11, color='#e8e8e8')
for ax in axs:
    ax.set_xlim(-1.12*R, 1.12*R); ax.set_ylim(-1.12*R, 1.12*R)
fig.text(0.5, 0.03, 'The 600-cell\'s 120 corners in five S5-orbits, 20 + 20 + 20 + 30 + 30, each hull in the A4 Coxeter plane (in B and −B some corners fall on the centre). Brighter, thicker edges are nearer.',
         ha='center', fontsize=11, color='#c8c8c8')
fig.text(0.985, 0.03, 'DICTO · dictospheres.com', ha='right', fontsize=10, color='#9a9a9a')
fig.savefig(OUT, dpi=150, bbox_inches='tight', facecolor=BG, pad_inches=0.25); C(os.path.getsize(OUT) > 10000, 'figure written')
C.final()
