# s6_plate.py -- overview plate: the nine regular solids (5 Platonic, 4 Kepler-Poinsot), each with its doubled star (t = 2, gold
# solid, violet spikes) inside its Star Halo (grey edges), and the flag-line curves t_min*(mu) of the four Kepler-Poinsot solids against
# the dodecahedron's (the turn theorem). DICTO mark. Study 2026-11-09-regular-stars-census.
# Usage: ~/geom/bin/python -u s6_plate.py <flags.json> <s4_starturn.json> <logo png> <out png>
import sys, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial import ConvexHull
from regstar import *
FL, ST, LOGO, OUT = sys.argv[1:5]
fl = {r['symbol']: r for r in json.load(open(FL)) if r['d'] == 3}; st = {r['symbol']: r for r in json.load(open(ST))}
order = ['{5,3}', '{3,5}', '{4,3}', '{3,3}', '{3,4}', '{5/2,5}', '{5,5/2}', '{5/2,3}', '{3,5/2}']
fig = plt.figure(figsize=(15, 17), facecolor='white')
for i, sym in enumerate(order):
    r = fl[sym]; ms = [vp(m) for m in r['mirrors']]; q = [flv(vp(x)) for x in r['q']]; Ms = [refl_mat(m) for m in ms]
    G = group_float(Ms); R = np.linalg.norm(q[0])
    poly = [q[0]]
    while True:
        nxt = Ms[1] @ (Ms[0] @ poly[-1])
        if np.abs(nxt - poly[0]).max() < 1e-9: break
        poly.append(nxt)
    faces = []
    for g in G:
        c = g @ q[2]
        if not any(np.abs(c - f[0]).max() < 1e-9 for f in faces): faces.append((c, [g @ p for p in poly]))
    t = 2.0; tips = np.array([t * c for c, _ in faces])
    ax = fig.add_subplot(4, 3, i + 1, projection='3d'); ax.set_proj_type('ortho'); ax.view_init(elev=18, azim=32)
    polys = [np.array(P) / R for c, P in faces]
    ax.add_collection3d(Poly3DCollection(polys, facecolor=(0.93, 0.74, 0.25, 0.85 if r['density'] == 1 else 0.55), edgecolor=(0.35, 0.25, 0.05, 1), linewidths=0.6))
    spikes = [np.array([t * c, P[k], P[(k + 1) % len(P)]]) / R for c, P in faces for k in range(len(P))]
    ax.add_collection3d(Poly3DCollection(spikes, facecolor=(0.55, 0.35, 0.80, 0.30), edgecolor=(0.40, 0.20, 0.60, 0.6), linewidths=0.3))
    H = ConvexHull(tips); E = set()
    for sm in H.simplices:
        for a, b in ((0, 1), (1, 2), (0, 2)): E.add(tuple(sorted((sm[a], sm[b]))))
    # keep only true edges of the hull (not facet diagonals): edges whose two adjacent facets are not coplanar
    segs = []
    eqs = H.equations
    for a, b in E:
        adj = [k for k, sm in enumerate(H.simplices) if a in sm and b in sm]
        if len(adj) == 2 and np.abs(eqs[adj[0]] - eqs[adj[1]]).max() < 1e-7: continue
        segs.append([tips[a] / R, tips[b] / R])
    ax.add_collection3d(Line3DCollection(segs, colors=(0.45, 0.45, 0.45, 0.9), linewidths=0.8))
    m = max(1.0, np.abs(tips / R).max()) * 0.9
    ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_zlim(-m, m); ax.set_box_aspect((1, 1, 1)); ax.set_axis_off()
    s = st[sym]['scan']
    ax.set_title(f"{r['name']}  {sym}\ndensity {r['density']},  g = (R/h)² = {r['g_float']:.4f}", fontsize=11)
axc = fig.add_subplot(4, 1, 4)
cols = {'{5,3}': '#555555', '{5/2,5}': '#2b7bb9', '{5,5/2}': '#7fb3dd', '{5/2,3}': '#c0392b', '{3,5/2}': '#e59866'}
for sym, cl in cols.items():
    s = st[sym]; cur = np.array(s['curve']); hR = s['hR_f']
    ls = '-' if sym in ('{5,3}', '{5/2,5}', '{5/2,3}') else '--'
    axc.plot(np.log(cur[:, 0] / hR), cur[:, 1], ls, color=cl, lw=2, label=f"{s['name']} {sym}")
    axc.plot(np.log(cur[:, 0] / hR), cur[:, 2], ':', color=cl, lw=1)
axc.axvline(0, color='k', lw=0.6); axc.text(0.02, 1.05, 'the turn  μ = hR', fontsize=10)
axc.set_xlabel('log(μ / hR) along the flag line  (ends: the solid and its reciprocal)'); axc.set_ylabel('t_min*(μ)')
axc.set_title('The turn for stars: symmetric under μ ↦ h²R²/μ for every solid; largest at the turn only for the convex ones (dotted: within one flag, where the turn theorem holds for all)', fontsize=10)
axc.legend(fontsize=9, loc='center', ncol=1); axc.grid(alpha=0.3)
fig.suptitle('The regular solids and their doubled stars (t = 2) in their Star Halos', fontsize=16, y=0.995)
try:
    logo = plt.imread(LOGO); la = fig.add_axes([0.86, 0.955, 0.12, 0.04]); la.imshow(logo); la.axis('off')
except Exception as e:
    fig.text(0.97, 0.985, 'DICTO', ha='right', fontsize=14, weight='bold')
fig.text(0.99, 0.003, 'DICTO · dictospheres.com', ha='right', fontsize=9, color='#444')
fig.tight_layout(rect=(0, 0.01, 1, 0.985)); fig.savefig(OUT, dpi=110)
import os
print('FINAL ok' if os.path.getsize(OUT) > 10000 else 'FINAL FAIL: plate not written')
