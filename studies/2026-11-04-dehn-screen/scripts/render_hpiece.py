import sys, math, itertools, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
H = math.sqrt(2/3); s3 = math.sqrt(3)
P = np.array([[0,0,0],[0,1/s3,-H/2],[0,1/s3,0],[.5,-1/(2*s3),-H/2],[.5,-1/(2*s3),0],[.5,1/(2*s3),-H],[.5,s3/2,0],[1,0,0],[1,1/s3,-H/2],[1,1/s3,0]])
c = P.mean(0); Q = P - c
# achirality: is the mirror image equal to a rotation of the piece? test reflection planes through the 3-fold axis (z through centroid)
def same(A, B): return all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-9 for a in A)
mir = [th for th in np.linspace(0, math.pi, 361)[:-1] if same(Q @ (np.eye(3) - 2*np.outer(n := np.array([math.cos(th), math.sin(th), 0]), n)).T, Q)]
print('mirror planes through the axis at angles (deg):', [round(math.degrees(t), 1) for t in mir])
h = ConvexHull(Q); faces = {}
for eq, s in zip(h.equations, h.simplices): faces.setdefault(tuple(np.round(eq, 6)), set()).update(s)
polys = []
for k, idx in faces.items():
    idx = list(idx); n = np.array(k[:3]); cc = Q[idx].mean(0); u = Q[idx[0]] - cc; w = np.cross(n, u)
    idx.sort(key=lambda i: math.atan2((Q[i] - cc) @ w, (Q[i] - cc) @ u)); polys.append((Q[idx], n, len(idx)))
col = {3: '#4fa3a5', 4: '#7a5fb0', 6: '#d4a020'}
fig = plt.figure(figsize=(11, 5.6), dpi=150)
for k, (el, az, title) in enumerate(((22, -60, 'from above'), (-18, -60, 'from below'))):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d'); light = np.array([.4, -.5, .8]); light /= np.linalg.norm(light)
    for V, n, m in polys:
        sh = 0.55 + 0.45*max(0, n @ light); base = np.array(matplotlib.colors.to_rgb(col[m]))
        ax.add_collection3d(Poly3DCollection([V], facecolor=np.clip(base*sh, 0, 1), edgecolor='#222', linewidths=1.2, alpha=0.97))
    ax.scatter(*Q.T, s=10, c='k'); ax.set_box_aspect((1, 1, H/1.0*1.2)); r = .7
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-.55, .45); ax.view_init(el, az); ax.set_axis_off(); ax.set_title(title, fontsize=11)
fig.suptitle('HexOct h-piece (λ ≥ 3/8): tiles space with copies of itself — 10 corners · 1 hexagon (gold) · 3 quadrilaterals (purple) · 6 triangles (teal)', fontsize=10)
try:
    m = plt.imread('dicto-mark.png'); a = fig.add_axes([0.9, 0.02, 0.08, 0.1]); a.imshow(m); a.axis('off')
except Exception as e: print('mark', e)
fig.savefig('renders/hexoct-h-piece.png', bbox_inches='tight'); print('saved')
