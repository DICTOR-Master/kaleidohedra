# Figure for #47 Theorem 2 (DICTO 11-06: "couldnt see any figures for threeway combi"): cubes (green) in a flat slab below; above it,
# one layer of the octet cut along its triangle planes: tetrahedra (red) and octahedra (yellow), no connector. The octet layer is
# lifted a little so the flat seam shows. Style and colours as #47's seam figure (element colours of the DICTO square, gold edges).
import math, numpy as np, itertools, sys
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull, cKDTree
h = math.sqrt(2 / 3); a1 = np.array([1., 0, 0]); a2 = np.array([.5, math.sqrt(3) / 2, 0]); shift = [np.zeros(3), (a1 + a2) / 3, 2 * (a1 + a2) / 3]
R = 5
def layer(k): return [i * a1 + j * a2 + shift[k % 3] + np.array([0, 0, k * h]) for i in range(-R, R + 1) for j in range(-R, R + 1)]
def octet_layer(k):
    lo, hi = layer(k), layer(k + 1); P = np.array(lo + hi); nlo = len(lo)
    adj = {i: set() for i in range(len(P))}
    for i, j in cKDTree(P).query_pairs(1 + 1e-6):
        if abs(np.linalg.norm(P[i] - P[j]) - 1) < 1e-6: adj[i].add(j); adj[j].add(i)
    out = set()
    for i in range(len(P)):
        for j, k2, l in itertools.combinations(sorted(x for x in adj[i] if x > i), 3):
            if k2 in adj[j] and l in adj[j] and l in adj[k2] and min(i, j, k2, l) < nlo <= max(i, j, k2, l): out.add(('T', (i, j, k2, l)))
    for i in range(nlo):
        for j, k2 in itertools.combinations(sorted(x for x in adj[i] if x < nlo), 2):
            if k2 not in adj[j]: continue
            tri = (i, j, k2); c = P[list(tri)].mean(0)
            up = [x for x in range(nlo, len(P)) if sum(x in adj[y] for y in tri) == 2 and np.linalg.norm(P[x, :2] - c[:2]) < 0.6]
            if len(up) == 3: out.add(('O', tuple(sorted(tri + tuple(up)))))
    return [(k, P[list(q)]) for k, q in out]
LIFT = 0.28; BOX = 1.75
sel = []
for k, V in octet_layer(0):
    c = V.mean(0)
    if max(abs(c[0]), abs(c[1])) < BOX: sel.append((k, V + [0, 0, LIFT]))
SAND = len(sys.argv) > 2 and sys.argv[2] == 'sandwich'
for i, j in itertools.product(range(-2, 2), repeat=2):
    V = np.array([[i + a, j + b, -1 + c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], float)
    sel.append(('C', V))
    if SAND and i < 1 and j < 1: sel.append(('C', V + [0, 0, 1 + h + 2 * LIFT + 0.55]))   # cube slab above, lifted further
def rot(ax, a):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
Rv = rot((1, 0, 0), -1.18 if len(sys.argv) > 2 else -1.05) @ rot((0, 0, 1), 0.45)
COL = {'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}
GROUND = (20, 15, 11); GOLD = (222, 178, 80)
light = np.array([-0.4, 0.5, 0.77]); light /= np.linalg.norm(light)
N = 1600; SS = 2; W = N * SS; img = Image.new('RGB', (W, int(W * 0.82)), GROUND); d = ImageDraw.Draw(img)
allv = np.vstack([V @ Rv.T for _, V in sel]); sc = 0.9 * min(W / np.ptp(allv[:, 0]), img.height / np.ptp(allv[:, 1]))
cx = (allv[:, 0].max() + allv[:, 0].min()) / 2; cy = (allv[:, 1].max() + allv[:, 1].min()) / 2
P = lambda p: (W / 2 + (p[0] - cx) * sc, img.height / 2 - (p[1] - cy) * sc)
items = []
for k, V in sel:
    Vv = V @ Rv.T; hh = ConvexHull(Vv); faces = {}
    for simp, eq in zip(hh.simplices, hh.equations): faces.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    items.append((Vv[:, 2].max() + Vv[:, 2].mean(), k, Vv, faces))
for _, k, Vv, faces in sorted(items, key=lambda t: t[0]):
    for eq, idx in faces.items():
        n = np.array(eq[:3])
        if n[2] <= 1e-9: continue
        idx = list(idx); c = Vv[idx].mean(0); u = Vv[idx[0]] - c; w = np.cross(n, u)
        idx.sort(key=lambda i: math.atan2((Vv[i] - c) @ w, (Vv[i] - c) @ u))
        b = 0.35 + 0.65 * max(0, n @ light); col = tuple(int(x * b) for x in COL[k])
        pts = [P(Vv[i]) for i in idx]; d.polygon(pts, fill=col); d.line(pts + [pts[0]], fill=GOLD, width=2 * SS)
out = sys.argv[1] if len(sys.argv) > 1 else 'seam-cto-plain.png'
img.resize((N, int(N * 0.82)), Image.LANCZOS).save(out); print('ok', len(sel), out)
