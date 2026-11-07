#!/usr/bin/env python3
"""Figure 4 of paper #100: the Dehn-zero piece (1,1,1,0)/3 and its tiling, two pieces per period.
Construction exactly as scripts/verify_real.py (logged in data/verify-real.log: 0 overlaps of 31138, coverage {1: 4000}):
T = conv{0, b1, b2, b3}, P = cuts c = (1/3, 1/3, 1/3, 0) at V0, V1, V2; partner Q = σ_z(P) + w, w = b1/3;
lattice L = B·diag(1 − c1, 1 − c2, 1 − c3). Re-checked here: volume, and every random point in exactly one copy."""
import sys, itertools, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, Delaunay
sys.path.insert(0, 'scripts'); import figlib as F

B = np.array([(1, 1, 0), (1, 0, 1), (0, 1, 1)], float).T
V = np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], float)
def piece(c):
    pts = [V[i] + c[i]*(V[j] - V[i]) for i in range(4) for j in range(4) if i != j]
    P = np.unique(np.round(pts, 12), axis=0); return P[ConvexHull(P).vertices]
c = [1/3, 1/3, 1/3, 0]; w = np.array([1/3, 1/3, 0])
P = piece(c); Q = P @ np.diag([1., 1., -1.]).T + w
L = B @ np.diag([1 - c[0], 1 - c[1], 1 - c[2]])
assert abs(2*ConvexHull(P).volume - abs(np.linalg.det(L))) < 1e-12
cop = []
for t in itertools.product(range(-5, 6), repeat=3):
    s = L @ np.array(t, float)
    for kind, X in ((0, P), (1, Q)):
        cop.append((kind, X + s))
rng = np.random.default_rng(1); X = rng.uniform(-0.7, 0.7, (6000, 3)); cnt = np.zeros(len(X), int)
for _, y in cop:
    if np.linalg.norm(y.mean(0)) < 3.5: cnt += Delaunay(y).find_simplex(X) >= 0
print('coverage', dict(zip(*np.unique(cnt, return_counts=True))), flush=True)
assert (cnt == 1).all()

c0 = (P.mean(0) + Q.mean(0))/2
R = F.look((0.95, -1.25, 0.75), up=(0, 0, 1))
fig = plt.figure(figsize=(12, 6.4), dpi=170); fig.patch.set_facecolor('white')

# left: the pair, slightly apart
ax = fig.add_axes([0.02, 0.1, 0.33, 0.8]); ax.set_aspect('equal'); ax.axis('off')
gap = 0.18*(Q.mean(0) - P.mean(0))
sP = F.Solid(P - c0 - gap, F.GOLD, lw=1.0, edge='#3a2a08'); sQ = F.Solid(Q - c0 + gap, F.VIOLET, lw=1.0, edge='#24123a')
F.draw(ax, [sP, sQ], R)
def fit(ax, sols, pad=0.08, bottom=0.0):
    A = np.vstack([s.P @ R.T for s in sols]); x0, y0 = A[:, :2].min(0); x1, y1 = A[:, :2].max(0)
    h = max(x1 - x0, y1 - y0)/2 + pad; cx, cy = (x0 + x1)/2, (y0 + y1)/2
    ax.set_xlim(cx - h, cx + h); ax.set_ylim(cy - h - bottom, cy + h); return cx, cy - h - bottom
bx, by = fit(ax, [sP, sQ], bottom=0.25)
ax.text(bx, by + 0.03, 'the piece (gold) and its point-inverse partner (violet)\ncuts (1, 1, 1, 0) at n = 3, one corner uncut',
        ha='center', va='bottom', fontsize=9, color='#333')

# right: a patch, exploded
ax2 = fig.add_axes([0.37, 0.02, 0.6, 0.96]); ax2.set_aspect('equal'); ax2.axis('off')
sol = []
g0 = min((i for i in range(len(cop)) if cop[i][0] == 0), key=lambda i: np.linalg.norm(cop[i][1].mean(0) - c0))
v0 = min((i for i in range(len(cop)) if cop[i][0] == 1), key=lambda i: np.linalg.norm(cop[i][1].mean(0) - cop[g0][1].mean(0)))
near = {0: g0, 1: v0}
for i, (kind, Y) in enumerate(cop):
    d = Y.mean(0) - c0
    if np.linalg.norm(d) > 1.15: continue
    Y2 = Y - c0 + 0.55*d
    if i in near.values():
        sol.append(F.Solid(Y2, F.GOLD if kind == 0 else F.VIOLET, lw=1.0, edge='#2a2030'))
    else:
        sol.append(F.Solid(Y2, F.GOLD if kind == 0 else F.VIOLET, alpha=0.10, glass=True, lw=0.5,
                           edge='#a08a50' if kind == 0 else '#7b5fb0', ealpha=0.65))
print('pieces drawn', len(sol), flush=True)
order = sol
F.draw(ax2, order, R)
bx, by = fit(ax2, sol, bottom=0.15)
ax2.text(bx, by + 0.03, 'a patch of the tiling, pulled apart: two pieces per period, period index N = 8 (Table 2)',
         ha='center', va='bottom', fontsize=9, color='#333')
F.mark(fig)
fig.savefig('figures/fig4-tiling.png', facecolor='white'); print('OK figures/fig4-tiling.png')
