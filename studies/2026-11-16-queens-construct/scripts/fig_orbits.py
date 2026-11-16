#!/usr/bin/env python3
"""Figure: the five S5-orbit hulls of the 600-cell side by side (A, -A, C3 hull, B, -B), each drawn in the A4 Coxeter plane
(the plane where the 5-cycle of S5 acts as a rotation by 72 degrees). Edges from the exact face lattice (qlib.Poly).
Element colours (D violet, I blue, C green, T red, O yellow, in D-I-C-T-O order). Usage: fig_orbits.py out.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = sys.argv[1]; C = Checks()
P5, X, Y = build_600(); Pk = {vkey(p): i for i, p in enumerate(P5)}
known = {vkey(q) for S in (X, Y) for q in S} | {vkey(vneg(q)) for S in (X, Y) for q in S}
C3 = [p for p in P5 if vkey(p) not in known]
sets = [('A', 'C1: golden truncated 5-cell', X), ('−A', 'C2: its mirror image', [vneg(x) for x in X]),
        ('C3', 'C3: expanded 5-cell (uniform)', C3), ('B', 'C4: golden cantellated 5-cell', Y), ('−B', 'C5: its mirror image', [vneg(y) for y in Y])]
COL = ['#8a5cc4', '#3a70cd', '#488e48', '#cd3e28', '#e8c852']
k = np.arange(5); U = np.cos(2*np.pi*k/5); Vv = np.sin(2*np.pi*k/5); Wd = np.cos(4*np.pi*k/5)
fig, axs = plt.subplots(1, 5, figsize=(20, 5.2), facecolor='white')
for ax, (nm, sub, S), col in zip(axs, sets, COL):
    H = Poly([to4(p) for p in S]); F = np.array([flt(to5(p)) for p in H.P])
    C(H.fvec[0] == len(S), f'{nm}: hull has {len(S)} corners, f-vector {H.fvec}')
    x, y, z = F @ U, F @ Vv, F @ Wd; z = (z - z.min())/(np.ptp(z) + 1e-12)
    for e in sorted(H.edges, key=lambda e: sum(z[list(e)])):
        a, b = tuple(e); d = (z[a] + z[b])/2
        ax.plot([x[a], x[b]], [y[a], y[b]], color=col, lw=1.4, alpha=0.85, solid_capstyle='round')
    ax.scatter(x, y, s=22, color=col, edgecolor='#222222', linewidth=0.5, zorder=3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(f'{nm}  ({len(S)} corners)\n{sub}\nf = {H.fvec}', fontsize=11)
fig.text(0.5, 0.02, 'The 600-cell\'s 120 corners split into five S5-orbits: 20 + 20 + 20 + 30 + 30. Each hull drawn in the A4 Coxeter plane (5-fold view; in B and −B several corners fall on the centre).',
         ha='center', fontsize=11, color='#333333')
fig.text(0.985, 0.02, 'DICTO · dictospheres.com', ha='right', fontsize=10, color='#555555')
fig.savefig(OUT, dpi=150, bbox_inches='tight'); C(os.path.getsize(OUT) > 10000, 'figure written')
C.final()
