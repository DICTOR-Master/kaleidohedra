"""The 4D scutoid as a 3D build, readable: (1-3) plan views of the vertical cut at λ below / at / above the wall -1/8: every hole's
polygon; the centre octahedral cell gold, the two tetrahedral cells that reach it at the wall bright green, the new contact red;
(4) the three columns in 3D (λ upwards): the new shared face starts at the wall as a wedge, the scutoid's Y one dimension up."""
import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Polygon
d = json.load(open('build3d.json')); cols = d['cols']; ci = d['centre']; gain = set(d['gained']); Z = 22.0
def section(c, lv):
    """polygon of column c at height lv: intersect its edges with the plane λ = lv"""
    W = np.array(c['V']); pts = []
    for f in c['F']:
        P = W[f]
        for a in range(len(P)):
            for b in range(a + 1, len(P)):
                za, zb = P[a, 2] - lv, P[b, 2] - lv
                if abs(za) < 1e-12: pts.append(P[a, :2])
                elif za * zb < 0: t = za / (za - zb); pts.append(P[a, :2] + t * (P[b, :2] - P[a, :2]))
    if len(pts) < 3: return None
    Q = np.unique(np.round(np.array(pts), 9), axis=0); cen = Q.mean(0); Q = Q[np.argsort(np.arctan2(Q[:, 1] - cen[1], Q[:, 0] - cen[0]))]
    return Q
def colour(c): return '#e2b43c' if c['i'] == ci else ('#26b86a' if c['i'] in gain else ('#8fb0ea' if c['kind'] == 'oct' else '#b9e2c8'))
fig = plt.figure(figsize=(16, 5.6), dpi=150)
for k, (lv, ttl) in enumerate(((-0.14, 'λ = −0.140: below the wall'), (d['wall'], 'λ = −0.125: the wall'), (-0.11, 'λ = −0.110: above the wall'))):
    ax = fig.add_subplot(1, 4, k + 1)
    for c in cols:
        Q = section(c, lv)
        if Q is None: continue
        ax.add_patch(Polygon(Q, closed=True, facecolor=colour(c), edgecolor='#222', lw=0.6))
    cg = section([c for c in cols if c['i'] == ci][0], lv)
    for c in cols:
        if c['i'] not in gain: continue
        Q = section(c, lv)
        if Q is None: continue
        shared = [q for q in Q if np.min(np.linalg.norm(cg - q, axis=1)) < 1e-7]
        if len(shared) >= 2: ax.plot(*np.array(shared[:2]).T, color='#d02020', lw=2.6)
        elif len(shared) == 1: ax.plot(*shared[0], 'o', color='#d02020', ms=5)
    cc = cg.mean(0); ax.set_xlim(cc[0] - 0.9, cc[0] + 0.9); ax.set_ylim(cc[1] - 0.75, cc[1] + 0.75); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(ttl, family='serif', fontsize=11)
ax = fig.add_subplot(1, 4, 4, projection='3d')
def faces3(c):
    W = np.array(c['V']); W = np.c_[W[:, 0], W[:, 1], (W[:, 2] - d['la']) * Z]; out = []
    for f in c['F']:
        P = W[f]; cen = P.mean(0); nr = np.cross(P[1] - P[0], P[2] - P[0])
        if np.linalg.norm(nr) < 1e-12: continue
        nr /= np.linalg.norm(nr); e1 = P[0] - cen; e1 /= np.linalg.norm(e1); e2 = np.cross(nr, e1); out.append(P[np.argsort(np.arctan2((P - cen) @ e2, (P - cen) @ e1))])
    return out
for c in cols:
    if c['i'] == ci or c['i'] in gain: ax.add_collection3d(Poly3DCollection(faces3(c), facecolor=colour(c), edgecolor='#1d1d1d', linewidths=0.5, alpha=0.85))
zw = (d['wall'] - d['la']) * Z; cg = np.array([c for c in cols if c['i'] == ci][0]['V'])[:, :2].mean(0)
ax.add_collection3d(Poly3DCollection([[(cg[0] - .7, cg[1] - .6, zw), (cg[0] + .7, cg[1] - .6, zw), (cg[0] + .7, cg[1] + .6, zw), (cg[0] - .7, cg[1] + .6, zw)]], facecolor='#d04040', alpha=0.12, edgecolor='#d04040', lw=0.6))
ax.set_xlim(cg[0] - .7, cg[0] + .7); ax.set_ylim(cg[1] - .6, cg[1] + .6); ax.set_zlim(0, (d['lb'] - d['la']) * Z); ax.set_box_aspect((1.4, 1.2, (d['lb'] - d['la']) * Z))
ax.view_init(elev=12, azim=-70); ax.set_axis_off(); ax.set_title('the three columns, λ upwards\n(red sheet: the wall)', family='serif', fontsize=11)
fig.suptitle('The 4D scutoid as a 3D build — a vertical cut through the stacking (ACABC, s = 1/5): every hole is a polygon; stacked upwards through\n'
             'λ (the 4th dimension) each becomes a flat-faced column. At the wall the gold cell gains two green neighbours (red: the new contact).', family='serif', fontsize=11.5)
fig.text(0.995, 0.01, 'DICTO', ha='right', fontsize=8, color='#888')
plt.subplots_adjust(left=0.01, right=0.99, top=0.82, bottom=0.03, wspace=0.05); plt.savefig('build3d.png'); print('FINAL ok')
