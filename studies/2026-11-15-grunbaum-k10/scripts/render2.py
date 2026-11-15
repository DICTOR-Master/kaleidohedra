#!/usr/bin/env python3
"""Figure: the two k = 10 tilers, each from the front and the back (surface rhombi: opaque gold/violet, crisp edges, back faces culled,
painter's order by face depth), plus tiler A with three lattice translates (cells, element colours). DICTO mark.
Usage: render2.py search.json tile.json out.png"""
import sys, os, json, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-13-paradigm-expansion', 'scripts'))
import figlib as F
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
PHI = (1 + 5**0.5)/2
E = np.array([(1, PHI, 0), (-1, PHI, 0), (0, 1, PHI), (0, -1, PHI), (PHI, 0, 1), (-PHI, 0, 1)], float)
S, T, OUT = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
tilers = [r for r in T['results'] if r.get('tiles')]
def surface_panel(ax, faces, col, az, el, title):
    R = F.rot(az, el); polys = []
    pts = np.array([np.array(p, float) @ E for p, a, b, s in faces]); ctr = pts.mean(0) + (E[faces[0][1]]*0)
    allc = []
    for p, a, b, s in faces:
        P0 = np.array(p, float) @ E; Q = np.array([P0, P0 + E[a], P0 + E[a] + E[b], P0 + E[b]]); allc.append(Q)
    ctr = np.vstack(allc).mean(0)
    for (p, a, b, s), Q in zip(faces, allc):
        n = np.cross(E[a], E[b])*s; n /= np.linalg.norm(n)
        if R[2] @ n <= 0: continue
        polys.append((float((R[2] @ (Q - ctr).T).mean()), Q - ctr, n))
    for dep, Q, n in sorted(polys, key=lambda x: x[0]):
        q = (R @ Q.T).T[:, :2]
        ax.add_patch(MPoly(q, closed=True, facecolor=F.shade(col, n), edgecolor=F.INK, lw=1.6, joinstyle='round'))
    F.blank(ax); ax.autoscale_view(); ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.6, 4.6); ax.set_title(title, fontsize=9.5)
fig, axs = plt.subplots(1, 5, figsize=(17, 4.0))
for i, (r, col) in enumerate(zip(tilers, [F.GOLD, F.VIOLET])):
    faces = S['candidates_rank_le_3'][r['index']]['faces']
    surface_panel(axs[2*i], faces, col, 28, 18, f'GET {"AB"[i]}, front')
    surface_panel(axs[2*i + 1], faces, col, 208, -18, f'GET {"AB"[i]}, back')
# tiling patch with cells
A = tilers[0]; R = F.rot(28, 18); sc = F.Scene(R, byobject=True); cells = []
for l, col in zip([[0]*6] + A['basis'], [F.GOLD, F.ELEM['I'], F.ELEM['C'], F.ELEM['T']]):
    for p, t in A['cells']: cells.append(([x + y for x, y in zip(p, l)], t, col))
allV = []
for p, t, col in cells:
    base = np.array(p, float) @ E
    allV.append(np.array([base + sum(s*E[d] for s, d in zip(sub, t)) for sub in itertools.product((0, 1), repeat=3)]))
ctr = np.vstack(allV).mean(0); idx = {sub: i for i, sub in enumerate(itertools.product((0, 1), repeat=3))}
for V, (p, t, col) in zip(allV, cells):
    faces = []
    for k in range(3):
        for v in (0, 1):
            quad = [s for s in itertools.product((0, 1), repeat=3) if s[k] == v]; quad = [quad[0], quad[1], quad[3], quad[2]]
            f = [idx[s] for s in quad]; faces.append((f, np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]])))
    sc.solid(V - ctr, faces=faces, color=col, lw=0.8)
sc.draw(axs[4]); F.blank(axs[4]); axs[4].autoscale_view(); axs[4].set_title('GET A with three lattice translates', fontsize=9.5)
F.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.08, wspace=0.05)
fig.savefig(OUT, dpi=180, facecolor='white'); print('wrote', OUT)
