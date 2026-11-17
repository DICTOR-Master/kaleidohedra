#!/usr/bin/env python3
"""Figure: mixed layer stacks from patch.py outputs (exact patches). Gold = GET A, violet = GET B (as in the 2026-11-15 figure),
teal = Inchbald's dimpled triacontahedron. Surface rhombi, crisp edges, back faces culled, painter's order; layers pulled apart
slightly along the stacking direction so each layer can be seen. DICTO mark.
Usage: fig.py <k10 dir> <inchbald json> <patch1 json> <patch2 json> <out png>"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mixlib import *
sys.path.insert(0, os.path.join(sys.argv[1], '..', '2026-11-13-paradigm-expansion', 'scripts'))
import figlib as FL
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
sol = load_solids(sys.argv[1], sys.argv[2])
EF = np.array([[zfloat(c) for c in e] for e in G.E])
COL = {'A': FL.GOLD, 'B': FL.VIOLET, 'C': FL.TEAL}
B1 = np.array(sol['A']['basis'][0], float) @ EF
def panel(ax, tiles, az, el, gap, title):
    R = FL.rot(az, el); polys = []
    up = B1/np.linalg.norm(B1)
    allP = []
    for T in tiles:
        F = tfaces(sol[T['Y']]['faces'], T['g'], tuple(T['t']))
        for (p, a, b), s in F.items():
            P0 = np.array(p, float) @ EF
            Qd = np.array([P0, P0 + EF[a], P0 + EF[a] + EF[b], P0 + EF[b]]) + gap*T['k']*up
            nrm = np.cross(EF[a], EF[b])*s; nrm /= np.linalg.norm(nrm)
            allP.append(Qd)
            if R[2] @ nrm <= 0: continue
            polys.append((Qd, nrm, COL[T['Y']]))
    ctr = np.vstack(allP).mean(0)
    items = sorted(polys, key=lambda x: float((R[2] @ (x[0] - ctr).T).mean()))
    for Qd, nrm, col in items:
        q = (R @ (Qd - ctr).T).T[:, :2]
        ax.add_patch(MPoly(q, closed=True, facecolor=FL.shade(col, nrm), edgecolor=FL.INK, lw=0.5, joinstyle='round'))
    FL.blank(ax); ax.autoscale_view(); ax.set_aspect('equal'); ax.set_title(title, fontsize=10)
upv = FL.rot(20, 12) @ (B1/np.linalg.norm(B1)); WHERE = 'first layer at the top' if upv[1] < 0 else 'first layer at the bottom'
print('stacking direction on the page', upv[:2], WHERE)
P1 = json.load(open(sys.argv[3])); P2 = json.load(open(sys.argv[4]))
fig, axs = plt.subplots(1, 3, figsize=(17, 6.6), gridspec_kw={'width_ratios': [0.7, 1, 1]})
one = [{'Y': y, 'g': P2['fill'][y][0], 't': P2['fill'][y][1], 'k': 2*i} for i, y in enumerate('ABC') if y in P2['fill']]
panel(axs[0], one, 20, 12, 3.0, 'the three solids, each in the same slab\n(gold GET A, violet GET B, teal Inchbald)')
panel(axs[1], P1['tiles'], 20, 12, 1.2, f'layers stacked in Fibonacci order\n{P1["word"]} ({WHERE})')
panel(axs[2], P2['tiles'], 20, 12, 1.2, f'all three solids, layers in the order\n{P2["word"]} ({WHERE})')
FL.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.04, wspace=0.04)
fig.savefig(sys.argv[5], dpi=170, facecolor='white'); print('wrote', sys.argv[5])
print('FINAL ok' if os.path.getsize(sys.argv[5]) > 10000 else 'FINAL FAIL: empty figure')
