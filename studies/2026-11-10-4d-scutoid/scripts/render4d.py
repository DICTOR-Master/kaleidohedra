"""Film strip of a 4D scutoid (DICTO 10 Nov "show me the 4D scutoid render"): word ACABC, hole 3 (octahedral), s = 1/5; its 3D slices at
five λ across the wall -5s/8 = -1/8. Faces coloured by the neighbour across them: gold = octahedral holes two layers away (they shrink
and vanish at the wall), blue = octahedral holes one layer away, green = tetrahedral holes."""
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import HalfspaceIntersection, ConvexHull
import scutoid4d as S
A, c0, V, used, labels = S.cell4d('ACABC', 3)
def slice_faces(lv):
    A3 = A.copy(); A3[:, 4] = A[:, 4] + A[:, 3] * lv; A3 = A3[:-2][:, [0, 1, 2, 4]]
    p3, _ = S.inner(A3); hs = HalfspaceIntersection(A3, p3); W = np.unique(np.round(hs.intersections, 9), axis=0)
    faces = []
    for k in range(len(A3)):
        on = np.where(np.abs(W @ A3[k, :3] + A3[k, 3]) < 1e-7)[0]
        if len(on) < 3: continue
        P = W[on]; c = P.mean(0); nrm = A3[k, :3] / np.linalg.norm(A3[k, :3]); e1 = P[0] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
        P = P[np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))]
        area = 0.5 * np.linalg.norm(sum(np.cross(P[t], P[(t + 1) % len(P)]) for t in range(len(P))))
        if area > 1e-9: faces.append((P, labels[k]))
    return W, faces
lams = [-0.155, -0.14, -0.125, -0.11, -0.06]
COL = lambda lab: '#e2b43c' if lab[0] == 'oct' and abs(lab[1]) >= 2 else ('#4f7fd6' if lab[0] == 'oct' else '#4fae7a')
fig = plt.figure(figsize=(16, 4.6), dpi=150); allW = np.vstack([slice_faces(l)[0] for l in lams]); cen = allW.mean(0); R = np.abs(allW - cen).max() * 0.82
for t, lv in enumerate(lams):
    W, faces = slice_faces(lv); ax = fig.add_subplot(1, len(lams), t + 1, projection='3d')
    for P, lab in faces:
        ax.add_collection3d(Poly3DCollection([P], facecolor=COL(lab), edgecolor='#222', linewidths=0.5, alpha=0.92))
    for a, f in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), range(3)): a(cen[f] - R, cen[f] + R)
    ax.view_init(elev=14, azim=35); ax.set_box_aspect((1, 1, 1)); ax.set_axis_off()
    gold = sum(1 for P, lab in faces if lab[0] == 'oct' and abs(lab[1]) >= 2)
    ttl = f'λ = {lv:+.3f}' + ('  (the wall)' if abs(lv + 0.125) < 1e-9 else '')
    ax.set_title(f'{ttl}\n{len(faces)} faces, {gold} gold', fontsize=10, family='serif')
fig.suptitle('A 4D scutoid: one octahedral hole\'s cell (stacking ACABC, s = 1/5) sliced at five values of λ, the 4th dimension',
             family='serif', fontsize=12.5)
fig.text(0.5, 0.025, 'gold: faces towards octahedral holes two layers away (they end at the wall λ = −5s/8 = −1/8)   ·   blue: octahedral holes one layer away   ·   green: tetrahedral holes',
         ha='center', family='serif', fontsize=9, color='#333')
fig.text(0.995, 0.01, 'DICTO', ha='right', fontsize=8, color='#888')
plt.subplots_adjust(left=0.0, right=1.0, top=0.84, bottom=0.07, wspace=0.0); plt.savefig('scutoid4d-strip.png'); print('FINAL ok')
