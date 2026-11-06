# Figure 1 in DICTO's geode / da Vinci style (DICTO 11-06: "the kepler drawing needs the construction lines like our geode style ones"):
# parchment; the octahedron, icosahedron and dodecahedron as sepia skeleton lines in Leonardo's 'vacuus' manner (near lines heavy, hidden
# lines faint and dashed); the cube as pale glass; the tetrahedron solid. Construction: rings at the golden points of the octahedron's edges
# (the icosahedron's corners, Pacioli), crosses at the octahedron's face centres (the cube's corners: the dual cube), dotted rays from the centre.
import math, itertools, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.spatial import ConvexHull
exec(open('../scripts/nest.py').read().split("def inside")[0])
W = 2600; S2 = 2
PARCH = (240, 230, 208); SEPIA = (91, 58, 30)
def rot(ax, ay):
    a, b = math.radians(ax), math.radians(ay)
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]]); return Rx @ Ry
def look(dirv, upv):
    z = np.array(dirv, float); z /= np.linalg.norm(z); u = np.array(upv, float); u = u - (u @ z) * z; u /= np.linalg.norm(u); x = np.cross(u, z)
    return np.array([x, u, z])   # rows: screen x, screen y, toward viewer
import os
VIEW = os.environ.get('VIEW', '3fold')
R = look((1, 1, 1), (0, 0, 1)) if VIEW == '3fold' else look((0.12, 1, 0.22), (0, 0, 1))
sc = 0.34 * W * 1.55
def P(p): q = R @ p; return (W / 2 + q[0] * sc, W * 0.48 - q[1] * sc), q[2]
img = Image.new('RGB', (W, W), PARCH); y, x = np.mgrid[0:W, 0:W]
vig = 1 - 0.10 * (np.hypot(x - W / 2, y - W / 2) / W) ** 2 * 4
img = Image.fromarray(np.clip(np.array(img) * vig[..., None], 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img, 'RGBA')
def faces(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 7)), set()).update(sp)
    return [(np.array(k[:3]), sorted(idx, key=lambda i: math.atan2(*((V[i] - V[list(idx)].mean(0)) @ np.array([np.cross(k[:3], V[list(idx)[0]] - V[list(idx)].mean(0)), V[list(idx)[0]] - V[list(idx)].mean(0)]).T)))) for k, idx in F.items()]
def edges_with_faces(V):
    F = faces(V); E = {}
    for n, idx in F:
        for a, b in zip(idx, idx[1:] + idx[:1]): E.setdefault(tuple(sorted((a, b))), []).append(n)
    return E
view = R.T @ np.array([0, 0, 1.0])
def dashed(p, q, col, w, dash=14):
    L = math.dist(p, q); n = max(1, int(L / dash))
    for k in range(0, n, 2):
        a = k / n; b = min(1, (k + 1) / n); d.line([(p[0] + (q[0] - p[0]) * a, p[1] + (q[1] - p[1]) * a), (p[0] + (q[0] - p[0]) * b, p[1] + (q[1] - p[1]) * b)], fill=col, width=w)
def skeleton(V, w, alpha):
    for (a, b), ns in edges_with_faces(V).items():
        visible = any(n @ view > 0 for n in ns)
        (pa, za), (pb, zb) = P(V[a]), P(V[b])
        if visible: d.line([pa, pb], fill=SEPIA + (alpha,), width=w)
        else: dashed(pa, pb, SEPIA + (int(alpha * 0.35),), max(2, w // 2))
light = R.T @ np.array([-0.4, 0.6, 0.7]); light /= np.linalg.norm(light)
def solid(V, rgb, alpha=255, edge_alpha=220):
    for n, idx in sorted(faces(V), key=lambda f: (R @ V[f[1]].mean(0))[2]):
        if n @ view <= 0: continue
        b = 0.55 + 0.45 * max(0, n @ light); pts = [P(V[i])[0] for i in idx]
        d.polygon(pts, fill=tuple(int(c * b) for c in rgb) + (alpha,)); d.line(pts + [pts[0]], fill=SEPIA + (edge_alpha,), width=3)
# back to front: octahedron and icosahedron skeletons, construction, dodecahedron, cube glass, tetrahedron solid
skeleton(O, 7, 235); skeleton(I, 5, 210)
c0 = P(np.zeros(3))[0]
for p in I:   # golden points on the octahedron's edges (the icosahedron's corners)
    q = P(p)[0]; r = 13; d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], outline=SEPIA + (230,), width=4)
fc = []
for n, idx in faces(O): fc.append(O[idx].mean(0))
for p in fc:  # face centres of the octahedron = corners of the cube
    q = P(p)[0]; r = 15; d.line([(q[0] - r, q[1] - r), (q[0] + r, q[1] + r)], fill=(150, 40, 30, 235), width=4); d.line([(q[0] - r, q[1] + r), (q[0] + r, q[1] - r)], fill=(150, 40, 30, 235), width=4)
    dashed(c0, q, SEPIA + (90,), 2, dash=10)
for p in O: dashed(c0, P(p)[0], SEPIA + (70,), 2, dash=10)
skeleton(D, 4, 170)
solid(C, (150, 190, 140), alpha=90, edge_alpha=150)
solid(T, (190, 82, 54))
img = img.resize((W // S2, W // S2), Image.LANCZOS); d2 = ImageDraw.Draw(img)
try:
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf', 26)
except Exception: F = None
d2.text((W // S2 / 2, W // S2 - 52), "Five in the Octet · the nest in one octahedron", fill=SEPIA, font=F, anchor='mm')
try:
    logo = Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA').resize((70, 70)); logo.putalpha(logo.split()[3].point(lambda a: int(a * 0.5)))
    img.paste(logo, (W // S2 - 100, W // S2 - 100), logo)
except Exception: pass
img.save(os.environ.get('OUT', '../kepler-nest-davinci.png')); print('ok')
