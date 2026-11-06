# Figure: UNITY with nests (DICTO 11-06): icosidodecahedron (white-gold edges) with 12 icosahedra (J11 + cap, blue edges) on its pentagons,
# each icosahedron holding a dodecahedron (violet), octahedron (yellow), cube (green) and a solid tetrahedron (red).
import json, math, itertools, numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
d = json.load(open('../unity-nests.json'))
COL = {'ID': (236, 214, 160), 'I': (70, 120, 220), 'D': (150, 90, 200), 'O': (232, 200, 82), 'C': (72, 160, 72), 'T': (205, 62, 40)}
def rx(t): return np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
Rv = rx(-1.0) @ rz(0.33)
def edges(V):
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); e = D_[D_ > 1e-9].min()
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D_[i, j] - e) < 1e-6]
items = []
allv = np.vstack([np.array(I) for I in d['icos']]) @ Rv.T
W = 2400; sc = 0.9 * W / np.ptp(allv[:, :2], axis=0).max(); cx, cy = allv[:, 0].mean(), allv[:, 1].mean()
P = lambda p: (W / 2 + (p[0] - cx) * sc, W / 2 - (p[1] - cy) * sc)
light = np.array([-0.4, 0.5, 0.77]); light /= np.linalg.norm(light)
def add_edges(V, col, w):
    Vv = V @ Rv.T
    for i, j in edges(V): items.append(((Vv[i, 2] + Vv[j, 2]) / 2, 'e', (Vv[i], Vv[j], col, w)))
add_edges(np.array(d['ID']), COL['ID'], 5)
for I, n in zip(d['icos'], d['nests']):
    add_edges(np.array(I), COL['I'], 3)
    for k in ('D', 'O', 'C'): add_edges(np.array(n[k]), COL[k], 2)
    Tv = np.array(n['T']) @ Rv.T; h = ConvexHull(Tv)
    for s, eq in zip(h.simplices, h.equations):
        if eq[2] <= 0: continue
        b = 0.35 + 0.65 * max(0, eq[:3] @ light); items.append((Tv[s][:, 2].mean(), 'f', ([Tv[k] for k in s], tuple(int(c * b) for c in COL['T']))))
img = Image.new('RGB', (W, W), (20, 15, 11)); dr = ImageDraw.Draw(img)
zs = [z for z, _, _ in items]; z0, z1 = min(zs), max(zs)
for z, kind, dd in sorted(items, key=lambda t: t[0]):
    f = 0.4 + 0.6 * (z - z0) / (z1 - z0)
    if kind == 'e':
        a, b, col, w = dd; dr.line([P(a), P(b)], fill=tuple(int(c * f) for c in col), width=w)
    else:
        pts, col = dd; dr.polygon([P(p) for p in pts], fill=tuple(int(c * (0.6 + 0.4 * f)) for c in col))
img.resize((1200, 1200), Image.LANCZOS).save('../unity-nests.png'); print('ok')
