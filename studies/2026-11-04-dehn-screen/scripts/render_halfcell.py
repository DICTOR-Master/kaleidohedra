import math, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
exec(open('scripts/halfcell.py').read().split('print("RD"')[0])
X = half(RD, True)   # the half-cell, hexagon at z = 0, body above
def faces(P):
    h = ConvexHull(P); fs = {}
    for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 6)), set()).update(s)
    out = []
    for k, idx in fs.items():
        n = np.array(k[:3]); idx = list(idx); c = P[idx].mean(0); u = P[idx[0]] - c; w = np.cross(n, u)
        idx.sort(key=lambda i: math.atan2((P[i] - c) @ w, (P[i] - c) @ u)); out.append((P[idx], n))
    return out
def rz(a): return np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
flip = np.diag([1, 1, -1.])
light = np.array([.4, -.5, .8]); light /= np.linalg.norm(light)
ZS = {}
REF = 0.0
def zseam(P): return ZS.get(id(P), 0.0)
ANG = {}
def ang0(P): return ANG.get(id(P), 0.0)
def draw(ax, parts, title, el=38):
    for P, base in parts:
        for V, n in faces(P):
            hexa = len(V) == 6
            onseam = sum(1 for v in V if abs(v[2] - zseam(P)) < 1e-6) >= 2
            if hexa: c = '#cccccc'
            elif onseam:
                cen = V.mean(0) - P.mean(0); k = int(round((((math.degrees(math.atan2(cen[1], cen[0])) + ang0(P) - REF) % 360)) / 60)) % 6
                c = '#d4a020' if k % 2 == 0 else '#7a5fb0'
            else: c = '#4fa3a5'
            col = np.array(matplotlib.colors.to_rgb(c))
            ax.add_collection3d(Poly3DCollection([V], facecolor=np.clip(col*(0.55 + 0.45*max(0, n @ light)), 0, 1), edgecolor='#222', linewidths=1, alpha=0.96))
    r = 0.62; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-.75, .75); ax.set_box_aspect((1, 1, 1.2)); ax.view_init(el, -55); ax.set_axis_off(); ax.set_title(title, fontsize=10)
gap = np.array([0, 0, 0.28])
def piece(P, z, turn=0.0):
    ZS[id(P)] = z; ANG[id(P)] = -turn; return P
U = X + gap; L1 = X @ flip.T - gap; L2 = (X @ flip.T) @ rz(math.pi/3).T - gap; C2 = (X @ flip.T) @ rz(math.pi/3).T; C1 = X @ flip.T
fx = [V for V, n in faces(X) if len(V) != 6 and sum(1 for v in V if abs(v[2]) < 1e-6) >= 2]
cc = fx[0].mean(0) - X.mean(0); REF = math.degrees(math.atan2(cc[1], cc[0])); print('seam faces', len(fx))
for P, z, t in ((X, 0, 0), (U, gap[2], 0), (L1, -gap[2], 0), (L2, -gap[2], 60), (C2, 0, 60), (C1, 0, 0)): piece(P, z, t)
fig = plt.figure(figsize=(15, 5.2), dpi=140)
draw(fig.add_subplot(1, 4, 1, projection='3d'), [(X, '#4fa3a5')], 'the half (seam faces gold / purple)', el=20)
draw(fig.add_subplot(1, 4, 2, projection='3d'), [(U, ''), (L1, '')], 'straight: gold meets gold → TRD (h)')
draw(fig.add_subplot(1, 4, 3, projection='3d'), [(U, ''), (L2, '')], 'twisted 60°: gold meets purple → RD (c)')
draw(fig.add_subplot(1, 4, 4, projection='3d'), [(X, ''), (C2, '')], 'closed: the RD')
fig.suptitle('One half-cell, two-colour seam: put on straight, gold meets gold (TRD, h layer); twist 60°, gold meets purple (RD, c layer)', fontsize=11)
try: m = plt.imread('dicto-mark.png'); a = fig.add_axes([0.92, 0.02, 0.07, 0.1]); a.imshow(m); a.axis('off')
except Exception: pass
fig.savefig('renders/halfcell-joins.png', bbox_inches='tight'); print('ok')
