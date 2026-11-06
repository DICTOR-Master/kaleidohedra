# Picture of the football layer: footballs (pentagons dark, hexagons white, as a ball), pentagon-hexagon bridges (gold), on the dark ground.
import numpy as np, math, itertools, sys
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
sys.argv = [sys.argv[0], '0.6']
exec(open('grid_layer.py').read().split('# overlap test')[0])
items = []
N = 2   # sites -N..N
for i, j in itertools.product(range(-N, N + 1), repeat=2):
    Vb, R = ball(i, j); items.append(('ball', Vb))
for i, j in itertools.product(range(-N, N + 1), repeat=2):
    for di, dj, d in ((1, 0, e1), (0, 1, e2)):
        if abs(i + di) > N or abs(j + dj) > N: continue
        k1, f1 = face_toward(i, j, d); k2, f2 = face_toward(i + di, j + dj, -d)
        items.append(('bridge', np.vstack([f1, f2])))
# view: look down the layer normal, tilted
nrm = np.cross(e1, e2); nrm /= np.linalg.norm(nrm)
u = e1 / np.linalg.norm(e1); w = np.cross(nrm, u)
B = np.array([u, w, nrm])                      # layer coordinates
def rx(t): return np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
Rv = rx(-0.75) @ rz(0.35) @ B
GROUND = (20, 15, 11); GOLD = (222, 178, 80); EDGE = (40, 32, 24)
light = np.array([-0.35, 0.45, 0.82]); light /= np.linalg.norm(light)
Wd = 3200; Hd = 2400; img = Image.new('RGB', (Wd, Hd), GROUND); dr = ImageDraw.Draw(img)
allv = np.vstack([P @ Rv.T for _, P in items]); sc = 0.92 * min(Wd / np.ptp(allv[:, 0]), Hd / np.ptp(allv[:, 1]))
cx, cy = (allv[:, 0].max() + allv[:, 0].min()) / 2, (allv[:, 1].max() + allv[:, 1].min()) / 2
Pp = lambda p: (Wd / 2 + (p[0] - cx) * sc, Hd / 2 - (p[1] - cy) * sc)
polys = []
for kind, P in items:
    Q = P @ Rv.T; h = ConvexHull(Q); fs = {}
    for sp, eq in zip(h.simplices, h.equations): fs.setdefault(tuple(np.round(eq, 6)), set()).update(sp)
    for eq, idx in fs.items():
        n = np.array(eq[:3])
        if n[2] <= 1e-9: continue
        idx = list(idx); c = Q[idx].mean(0); a0 = Q[idx[0]] - c; b0 = np.cross(n, a0)
        idx.sort(key=lambda k: math.atan2((Q[k] - c) @ b0, (Q[k] - c) @ a0))
        b = 0.4 + 0.6 * max(0, n @ light)
        if kind == 'ball': base = (40, 40, 46) if len(idx) == 5 else (236, 236, 228)
        else: base = (222, 178, 80)
        polys.append((Q[idx][:, 2].mean() + (0.02 if kind == 'ball' else 0), [Pp(Q[k]) for k in idx], tuple(int(x * b) for x in base)))
for _, pts, col in sorted(polys, key=lambda t: t[0]):
    dr.polygon(pts, fill=col); dr.line(pts + [pts[0]], fill=EDGE, width=3)
img.resize((1600, 1200), Image.LANCZOS).save('../football-layer.png'); print('ok', len(items))
