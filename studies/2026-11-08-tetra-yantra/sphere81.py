"""The 81-triangle spherical yantra (DICTO 11-08: 'a four times bigger one with four triangles for every one'): the twenty Cleo
faces (spherical icosahedron) each split into four by their side midpoints (geodesic frequency 2): 80 triangles (20 central
equilateral, 60 corner ones in fives round the 12 icosahedron corners); with the bindu at the centre, 81. Each triangle carries the
DICTO Yantra (golden_family.json GF1, the Cleo-Antonius yantra) in its inscribed circle, drawn by gnomonic projection (every line a
great circle, every meeting exact); corner yantras point to their icosahedron corner (a five-petalled flower at each). Counts checked."""
import json, math, itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
Y = json.load(open('golden_family.json'))['GF1']; f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(Y['b']), f(Y['w']), f(Y['apex'])
UP = {i for i in range(1, 10) if a[i] < b[i]}
segs = []
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (0, a[i]); segs += [(L, R, i), (L, A, i), (R, A, i)]
phi = (1 + 5 ** .5) / 2
I = [np.array(p, float) for c in [(0, 1, phi), (1, phi, 0), (phi, 0, 1)] for p in itertools.product(*[(x, -x) if x else (0,) for x in c])]
I = [v / np.linalg.norm(v) for v in I]; E = min(np.linalg.norm(I[i] - I[j]) for i, j in itertools.combinations(range(12), 2))
faces = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(I[x] - I[y]) - E) < 1e-9 for x, y in itertools.combinations(t, 2))]
nz = lambda v: v / np.linalg.norm(v)
tris = []   # (vertices, pointing vertex)
for t in faces:
    A, B, C = (I[k] for k in t); ab, bc, ca = nz(A + B), nz(B + C), nz(C + A)
    tris += [((A, ab, ca), A), ((B, bc, ab), B), ((C, ca, bc), C), ((ab, bc, ca), ab)]
assert len(tris) == 80
V = {tuple(np.round(p, 9)) for tr, _ in tris for p in tr}; Ed = {tuple(sorted((tuple(np.round(p, 9)), tuple(np.round(q, 9))))) for tr, _ in tris for p, q in itertools.combinations(tr, 2)}
print('triangles', len(tris), 'corners', len(V), 'edges', len(Ed), 'Euler', len(V) - len(Ed) + len(tris), '+ bindu = 81 triangles and centre:', len(tris) + 1)
def incircle(tr):
    A, B, C = tr; la, lb, lc = (math.acos(np.clip(np.dot(q, r), -1, 1)) for q, r in ((B, C), (C, A), (A, B)))
    cen = nz(la * A + lb * B + lc * C)
    rad = min(math.asin(abs(np.dot(cen, nz(np.cross(q, r))))) for q, r in ((A, B), (B, C), (C, A)))
    return cen, rad
W = H = 1200; img = Image.new('RGB', (W, H), (10, 11, 16)); d = ImageDraw.Draw(img)
GOLD = (232, 194, 90); BLUE = (58, 112, 205); cx = cy = 600; Rpx = 520
tilt = np.array([[1, 0, 0], [0, math.cos(.35), -math.sin(.35)], [0, math.sin(.35), math.cos(.35)]]) @ np.array([[math.cos(.3), 0, math.sin(.3)], [0, 1, 0], [-math.sin(.3), 0, math.cos(.3)]])
d.ellipse([cx - Rpx, cy - Rpx, cx + Rpx, cy + Rpx], outline=(110, 110, 120), width=2)
def line3(pts, col, wd):
    for p, q in zip(pts, pts[1:]):
        p, q = tilt @ p, tilt @ q
        if p[2] > 0 and q[2] > 0: d.line([(cx + Rpx * p[0], cy - Rpx * p[1]), (cx + Rpx * q[0], cy - Rpx * q[1])], fill=col, width=wd)
for tr, point in tris:
    for p, q in itertools.combinations(tr, 2): line3([nz(p + (q - p) * s) for s in np.linspace(0, 1, 20)], (95, 95, 105), 1)
    cen, rad = incircle(tr); up = point - np.dot(point, cen) * cen; up = nz(up); rt = np.cross(up, cen); sc = math.tan(rad) / 0.5
    P = lambda x, dd: nz(cen + (x * sc) * rt + ((0.5 - dd) * sc) * up)
    for p, q, i in segs: line3([P(p[0] + (q[0] - p[0]) * s, p[1] + (q[1] - p[1]) * s) for s in np.linspace(0, 1, 14)], GOLD if i in UP else BLUE, 1)
fnt = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 22)
d.text((cx, 34), '81: eighty DICTO Yantras on the twice-split Cleo sphere, the bindu at the centre', font=fnt, fill=(230, 230, 235), anchor='mm')
d.text((W - 16, H - 14), 'DICTO · dictospheres.com', font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 16), fill=GOLD, anchor='rs')
img.save('sphere81.png')
print('FINAL ok' if len(tris) == 80 and len(V) - len(Ed) + len(tris) == 2 else 'FINAL FAIL')
