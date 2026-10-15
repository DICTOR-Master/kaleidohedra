# Paper figure (DICTO: "draft the paper from the outline"): the core plane as a cut-and-project picture. Exact plane lattice points
# (height along the five-fold axis, transverse distance t), for |h| < 26 and t < 2.2; the build's silent copies (radius 10) ringed;
# the canonical window [0, L) and the ring-clash window [0, t_c); the fork point at h = 12.81 marked. Positions are exact values
# converted to float for drawing only.
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('scripts/chorus_window_why.py').read().split('out2 = []')[0])
i0 = next(i for i in Pl if wk[i] != -1)
q_ = R72 @ Pf[i0]; j0 = int(np.argmin(np.linalg.norm(Pf - q_, axis=1)))
if np.linalg.norm(Pf[j0] - q_) > 1e-6: q_ = np.linalg.matrix_power(R72, 4) @ Pf[i0]; j0 = int(np.argmin(np.linalg.norm(Pf - q_, axis=1)))
Dx = sub(sites[i0][1], sites[j0][1]); gg = max((dot(n, Dx) / (Q(2) * d) for _, n, d in PO), key=lambda q: q.f())
tc = ((tr[i0] * tr[i0] / dot(w, w)) / (gg * gg)).f() ** .5; Lc = Lw.f() / dot(w, w).f() ** .5; nw = dot(w, w).f() ** .5; nv = vv.f() ** .5
P = []
for p in range(-80, 81):
    for q in range(-80, 81):
        t = (tb1 * Q(p) + tb2 * Q(q)).f() / nw; h = (hb1 * Q(p) + hb2 * Q(q)).f() / nv
        if abs(h) < 26 and -0.3 < t < 2.2: P.append((h, t))
P = np.array(P); Ssil = np.array([(hh[i].f() / nv, tr[i].f() / nw) for i in Pl if silent[i]])
fig, ax = plt.subplots(figsize=(10, 5.0), dpi=200)
ax.axhspan(0, Lc, color='#f3d9a0', zorder=0, label=f'canonical window [0, L), L = {Lc:.4f}')
ax.axhspan(0, tc, color='#e9b949', alpha=0.55, zorder=0, label=f'ring-clash window [0, t$_c$), t$_c$ = {tc:.4f}')
ax.axvspan(-10, 10, color='#000', alpha=0.04, zorder=0)
ax.scatter(P[:, 0], P[:, 1], s=9, c='#2b2620', zorder=2, label='plane lattice points (exact)')
ax.scatter(Ssil[:, 0], Ssil[:, 1], s=60, facecolors='none', edgecolors='#c62828', linewidths=1.3, zorder=3, label='silent in the radius-10 build')
ax.scatter([0], [0], marker='*', s=140, c='#c62828', zorder=4, label='centre copy')
ax.scatter([12.8121], [1.1553], marker='D', s=46, facecolors='none', edgecolors='#7b1fa2', linewidths=1.5, zorder=4, label='the fork, h = 12.81')
inw = P[(P[:, 1] >= -1e-9) & (P[:, 1] < Lc)]
for h in inw[:, 0]: ax.plot([h, h], [-0.42, -0.30], c='#2b2620', lw=1)
ax.axhline(-0.36, c='#2b2620', lw=0.6); ax.text(-25.6, -0.33, 'chain', fontsize=7, va='bottom')
ax.set_xlim(-26, 26); ax.set_ylim(-0.5, 2.2); ax.set_xlabel('height along the five-fold axis'); ax.set_ylabel('distance from the axis, t')
ax.text(0, 2.25, 'grey band: heights inside the radius-10 build', ha='center', va='bottom', fontsize=7, color='#555')
ax.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False); ax.text(25.8, -0.48, 'DICTO · dictospheres.com', ha='right', fontsize=6.5, color='#5b5346')
fig.tight_layout(); fig.savefig('renders/fig-window.png'); print('fig-window written', len(P), 'points;', len(inw), 'chain points shown; t_c', tc, 'L', Lc)
