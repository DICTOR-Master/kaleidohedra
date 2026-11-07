#!/usr/bin/env python3
"""Figure 3 of paper #100 (Theorem 2.4, Table 2): the thirteen Dehn-zero integer truncated tetrahedra that tile,
each drawn in T(n) = n·conv{0, b1, b2, b3} with the octet planes (x ± y ± z = even) traced on its faces,
so the octahedra and tetrahedra of edge 1 it is built from show. Cell counts are checked against Table 2
(octahedra C(m+1,3) per T(m) minus the corners'; tetrahedra = 2 × octahedra when Σk = n, Proposition 2.3)."""
import sys, numpy as np
from math import comb
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
sys.path.insert(0, 'scripts'); import figlib as F

V = np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], float)
rows = [[(2, (1, 1, 0, 0), 2), (3, (2, 1, 0, 0), 6), (3, (1, 1, 1, 0), 8), (8, (5, 3, 0, 0), 120)],
        [(4, (3, 1, 0, 0), 12), (4, (2, 2, 0, 0), 16), (4, (2, 1, 1, 0), 18), (4, (1, 1, 1, 1), 20)],
        [(5, (4, 1, 0, 0), 20), (5, (3, 2, 0, 0), 30), (5, (3, 1, 1, 0), 32), (5, (2, 2, 1, 0), 36), (5, (2, 1, 1, 1), 38)]]
fam = [(1, -1, -1), (-1, 1, -1), (-1, -1, 1), (1, 1, 1)]
R = F.look((1.0, -1.35, 0.85), up=(0, 0, 1))
fig = plt.figure(figsize=(12, 8.6), dpi=170); fig.patch.set_facecolor('white')
for r, row in enumerate(rows):
    for j, (n, k, N) in enumerate(row):
        Vn = n*V
        kc = [0]*4
        for i, corner in enumerate((2, 0, 1, 3)): kc[corner] = k[i]   # largest cuts on the corners nearest the viewer
        pts = [Vn[i] + (kc[i]/n)*(Vn[q] - Vn[i]) for i in range(4) for q in range(4) if i != q]
        P = np.unique(np.round(pts, 12), axis=0); P = P[ConvexHull(P).vertices]
        O = comb(n + 1, 3) - sum(comb(m + 1, 3) for m in k)
        Tt = comb(n + 2, 3) + comb(n, 3) - sum(comb(m + 2, 3) + comb(m, 3) for m in k)
        assert Tt == 2*O and N == 2*O, (n, k, O, Tt, N)
        assert abs(ConvexHull(P).volume - (O*4 + Tt)/3) < 1e-9   # fcc unit: octahedron 4/3, tetrahedron 1/3
        off = (5 - len(row))/2
        ax = fig.add_axes([(j + off)/5 + 0.004, 1 - (r + 1)/3 + 0.075, 1/5 - 0.008, 1/3 - 0.085]); ax.set_aspect('equal'); ax.axis('off')
        s = F.Solid(P/n, F.GOLD, lw=0.9, edge='#3a2a08')
        F.draw(ax, [s], R)
        F.wire(ax, V, R, color=F.BLUE, lw=0.5, alpha=0.45, z=-1e9)
        F.face_grid(ax, s, R, fam, [2*m/n for m in range(-2*n, 2*n + 1)], '#5a4210', lw=0.5, alpha=0.75)
        A = (V @ R.T)[:, :2]; (x0, y0), (x1, y1) = A.min(0), A.max(0); cx = (x0 + x1)/2; h = 0.80
        ax.set_xlim(cx - h, cx + h); ax.set_ylim(y1 + 0.05 - 2*h*0.93, y1 + 0.05)
        fig.text((j + off)/5 + 0.1, 1 - (r + 1)/3 + 0.022, f'({k[0]}, {k[1]}, {k[2]}, {k[3]})  ·  n = {n}\n{O} octahedr{"on" if O == 1 else "a"}, {Tt} tetrahedra  ·  N = {N}',
                 ha='center', va='bottom', fontsize=8.6, color='#333', linespacing=1.3)
F.mark(fig)
fig.savefig('figures/fig3-thirteen.png', facecolor='white'); print('OK figures/fig3-thirteen.png')
