# Figure: Kepler's nest in one octahedron of the octet (DICTO 11-06 "a lattice of five shapes, the Platonic solids").
# Element colours of the DICTO square: D violet, I blue, C green, T red, O yellow. Outer solids as edges (glowing lines), the tetrahedron solid.
import numpy as np, math, itertools
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
exec(open('nest.py').read().split("def inside")[0])
COL = {'O': (232, 200, 82), 'I': (70, 120, 220), 'D': (150, 90, 200), 'C': (72, 160, 72), 'T': (205, 62, 40)}
def rx(t): return np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
Rv = rx(-1.15) @ rz(0.42)
W = 2400; img = Image.new('RGB', (W, W), (20, 15, 11)); dr = ImageDraw.Draw(img); sc = W * 0.62
P = lambda p: (W / 2 + p[0] * sc, W / 2 - p[1] * sc)
def edge_list(V):
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); m = D_[D_ > 1e-9].min()
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D_[i, j] - m) < 1e-6]
# tetrahedron solid (back faces first)
Tv = T @ Rv.T; h = ConvexHull(Tv); light = np.array([-0.4, 0.5, 0.77]); light /= np.linalg.norm(light)
faces = sorted(zip(h.simplices, h.equations), key=lambda t: Tv[t[0]][:, 2].mean())
items = []
for name, V, w in (('O', O, 7), ('I', I, 6), ('D', D, 5), ('C', C, 6)):
    Vv = V @ Rv.T
    for i, j in edge_list(V): items.append(((Vv[i, 2] + Vv[j, 2]) / 2, 'e', (Vv[i], Vv[j], COL[name], w)))
for s, eq in faces:
    b = 0.35 + 0.65 * max(0, eq[:3] @ light); items.append((Tv[s][:, 2].mean(), 'f', ([Tv[k] for k in s], tuple(int(c * b) for c in COL['T']))))
for z, kind, d in sorted(items, key=lambda t: t[0]):
    if kind == 'e':
        a, b, col, w = d; fade = 0.55 + 0.45 * (z + 0.75) / 1.5
        dr.line([P(a), P(b)], fill=tuple(int(c * min(1, fade)) for c in col), width=w)
    else:
        pts, col = d; dr.polygon([P(p) for p in pts], fill=col)
img.resize((1200, 1200), Image.LANCZOS).save('../five-nest.png'); print('ok')
