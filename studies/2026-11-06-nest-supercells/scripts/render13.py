# Figure: the nested Dodeca-13 (DICTO 11-06, route c: the 120-cell's 1 + 12): 13 dodecahedra (violet edges), each holding I (blue),
# O (yellow), C (green) and a solid tetrahedron (red); wedges and needles left out so the nests show. Element colours of the DICTO square.
import json, math, itertools, numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
d = json.load(open('../nest13.json'))
COL = {'D': (150, 90, 200), 'I': (70, 120, 220), 'O': (232, 200, 82), 'C': (72, 160, 72), 'T': (205, 62, 40)}
def rx(t): return np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
Rv = rx(-1.05) @ rz(0.37)
def edges(V):
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); e = D_[D_ > 1e-9].min()
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D_[i, j] - e) < 1e-6]
items = []
allv = np.vstack([np.array(V) for V in d['dodecahedra']]) @ Rv.T
W = 2400; sc = 0.9 * W / np.ptp(allv[:, :2], axis=0).max(); cx, cy = allv[:, 0].mean(), allv[:, 1].mean()
P = lambda p: (W / 2 + (p[0] - cx) * sc, W / 2 - (p[1] - cy) * sc)
light = np.array([-0.4, 0.5, 0.77]); light /= np.linalg.norm(light)
for Dv, n in zip(d['dodecahedra'], d['nests']):
    for name, V, w in (('D', np.array(Dv), 4), ('I', np.array(n['I']), 3), ('O', np.array(n['O']), 3), ('C', np.array(n['C']), 3)):
        Vv = V @ Rv.T
        for i, j in edges(V): items.append(((Vv[i, 2] + Vv[j, 2]) / 2, 'e', (Vv[i], Vv[j], COL[name], w)))
    Tv = np.array(n['T']) @ Rv.T; h = ConvexHull(Tv)
    for s, eq in zip(h.simplices, h.equations):
        if eq[2] <= 0: continue
        b = 0.35 + 0.65 * max(0, eq[:3] @ light); items.append((Tv[s][:, 2].mean(), 'f', ([Tv[k] for k in s], tuple(int(c * b) for c in COL['T']))))
img = Image.new('RGB', (W, W), (20, 15, 11)); dr = ImageDraw.Draw(img)
zs = [z for z, _, _ in items]; z0, z1 = min(zs), max(zs)
for z, kind, dd in sorted(items, key=lambda t: t[0]):
    f = 0.45 + 0.55 * (z - z0) / (z1 - z0)
    if kind == 'e':
        a, b, col, w = dd; dr.line([P(a), P(b)], fill=tuple(int(c * f) for c in col), width=w)
    else:
        pts, col = dd; dr.polygon([P(p) for p in pts], fill=tuple(int(c * (0.6 + 0.4 * f)) for c in col))
img.resize((1200, 1200), Image.LANCZOS).save('../nested-dodeca-13.png'); print('ok')
