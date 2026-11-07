#!/usr/bin/env python3
"""Figure 2 of paper #100 (Proposition 2.2): the Dehn-zero truncated tetrahedra are T ∩ (w + 2(−T)).
T = {−v_i·x ≤ 1} (corners v_i, edge 2√2); cutter w + 2(−T) = {v_i·x ≤ 2 + v_i·w}; cut fraction c_i = (1 − v_i·w)/4.
Three translations w: the uniform cut (1,1,1,1)/4, the cut (2,1,1,0)/4 and the cut (2,2,0,0)/4, each checked: Σc = 1, volume as predicted."""
import sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
sys.path.insert(0, 'scripts'); import figlib as F

v = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
T = v.copy()
cases = [((1, 1, 1, 1), 'w = 0\ncuts (1, 1, 1, 1)/4: the β-tin piece'),
         ((2, 1, 1, 0), 'w = (−1/2, −1/2, 0)\ncuts (2, 1, 1, 0)/4'),
         ((2, 2, 0, 0), 'w = (−1, 0, 0)\ncuts (2, 2, 0, 0)/4: two cuts meet on an edge')]
R = F.look((-0.2, -1.0, 0.3), up=(0, 0, 1))
fig = plt.figure(figsize=(12.6, 5.2), dpi=170); fig.patch.set_facecolor('white')
for j, (k, label) in enumerate(cases):
    c = np.array(k)/4.0
    w = (1 - 4*c) @ v / 4             # v_i·w = 1 − 4c_i, since Σ v_i v_iᵀ = 4I
    assert np.allclose(v @ w, 1 - 4*c) and abs(c.sum() - 1) < 1e-12
    cutter = -2*v + w
    P = F.hull_from_halfspaces(np.vstack([-v, v]), np.r_[np.ones(4), 2 + v @ w], interior=w*0 + (T.mean(0)*0 + 0.25*w))
    vol = ConvexHull(P).volume; volT = ConvexHull(T).volume
    pred = volT*(1 - (c**3).sum())
    assert abs(vol - pred) < 1e-9, (vol, pred)
    ax = fig.add_axes([j/3 + 0.005, 0.12, 1/3 - 0.01, 0.84]); ax.set_aspect('equal'); ax.axis('off')
    sC = F.Solid(cutter, F.VIOLET, alpha=0.07, glass=True, lw=0.8, edge=F.VIOLET, ealpha=0.9)
    sT = F.Solid(T, F.BLUE, alpha=0.04, glass=True, lw=1.0, edge=F.BLUE, ealpha=0.9)
    sP = F.Solid(P, F.GOLD, lw=1.0, edge='#3a2a08')
    F.draw(ax, [sC, sT, sP], R)
    cx, cy = ((T.mean(0) + 0.5*w) @ R.T)[:2]; h = 3.3   # frame halfway between T and the cutter
    ax.set_xlim(cx - h, cx + h); ax.set_ylim(cy - h, cy + h)
    fig.text(j/3 + 1/6, 0.035, label, ha='center', va='bottom', fontsize=9.5, color='#333')
    print(k, 'w =', np.round(w, 4), 'corners', len(P), 'vol/volT', round(vol/volT, 6), flush=True)
fig.text(0.012, 0.975, 'T (blue)  ∩  w + 2(−T) (violet)  =  a Dehn-zero truncated tetrahedron (gold)', fontsize=10.5, color='#3d3220', va='top', weight='bold')
F.mark(fig)
fig.savefig('figures/fig2-cutter.png', facecolor='white'); print('OK figures/fig2-cutter.png')
