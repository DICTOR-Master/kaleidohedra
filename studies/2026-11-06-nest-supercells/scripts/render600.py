# Figure: the 600-cell side (DICTO 11-06): 20 tetrahedra round one corner (red edges), each holding a truncated tetrahedron (orange),
# octahedron (yellow), icosahedron (blue), dodecahedron (violet) and a solid cube (green). Element colours of the DICTO square.
import json, math, itertools, numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
d = json.load(open('../nest600.json'))
COL = {'T': (205, 62, 40), 'U': (235, 140, 50), 'O': (232, 200, 82), 'I': (70, 120, 220), 'D': (150, 90, 200), 'C': (72, 160, 72)}
def rx(t): return np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
Rv = rx(-0.9) @ rz(0.3)
def hull_edges(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 5)), set()).update(sp)
    E = set()
    for key, idx in F.items():
        idx = list(idx); n = np.array(key[:3]); c = V[idx].mean(0); u = V[idx[0]] - c; w = np.cross(n, u)
        o = sorted(idx, key=lambda i: math.atan2((V[i] - c) @ w, (V[i] - c) @ u))
        for a, b in zip(o, o[1:] + o[:1]): E.add(tuple(sorted((a, b))))
    return E
items = []
allv = np.vstack([np.array(t) for t in d['tets']]) @ Rv.T
W = 2400; sc = 0.9 * W / np.ptp(allv[:, :2], axis=0).max(); cx, cy = allv[:, 0].mean(), allv[:, 1].mean()
P = lambda p: (W / 2 + (p[0] - cx) * sc, W / 2 - (p[1] - cy) * sc)
light = np.array([-0.4, 0.5, 0.77]); light /= np.linalg.norm(light)
for t, n in zip(d['tets'], d['nests']):
    for name, V, w in (('T', np.array(t), 4), ('U', np.array(n['U']), 2), ('O', np.array(n['O']), 2), ('I', np.array(n['I']), 2), ('D', np.array(n['D']), 2)):
        Vv = V @ Rv.T
        for i, j in hull_edges(V): items.append(((Vv[i, 2] + Vv[j, 2]) / 2, 'e', (Vv[i], Vv[j], COL[name], w)))
    Cv = np.array(n['C']) @ Rv.T; h = ConvexHull(Cv); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 5)), set()).update(sp)
    for key, idx in F.items():
        nrm = np.array(key[:3])
        if nrm[2] <= 0: continue
        idx = list(idx); c = Cv[idx].mean(0); u = Cv[idx[0]] - c; w = np.cross(nrm, u)
        idx.sort(key=lambda i: math.atan2((Cv[i] - c) @ w, (Cv[i] - c) @ u))
        b = 0.35 + 0.65 * max(0, nrm @ light); items.append((Cv[idx][:, 2].mean(), 'f', ([Cv[k] for k in idx], tuple(int(x * b) for x in COL['C']))))
img = Image.new('RGB', (W, W), (20, 15, 11)); dr = ImageDraw.Draw(img)
zs = [z for z, _, _ in items]; z0, z1 = min(zs), max(zs)
for z, kind, dd in sorted(items, key=lambda t: t[0]):
    f = 0.4 + 0.6 * (z - z0) / (z1 - z0)
    if kind == 'e':
        a, b, col, w = dd; dr.line([P(a), P(b)], fill=tuple(int(c * f) for c in col), width=w)
    else:
        pts, col = dd; dr.polygon([P(p) for p in pts], fill=tuple(int(c * (0.6 + 0.4 * f)) for c in col))
img.resize((1200, 1200), Image.LANCZOS).save('../nested-600-corner.png'); print('ok')
