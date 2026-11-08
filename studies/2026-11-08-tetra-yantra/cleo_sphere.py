"""Twenty yantras on the sphere (DICTO 11-08 'leaning towards Cleos'): the twenty Cleo-Icos (the icosahedron's face pyramids) meet
the sphere in the twenty faces of the spherical icosahedron. In each face's inscribed circle (angular radius 20.9051 deg; adjacent
caps touch) draw the perfect yantra (viewpoint.json V1) by gnomonic projection from the centre, its top pointing at a face corner.
Exact: every line a great circle, every concurrency kept. Orthographic view; only the near hemisphere drawn."""
import json, math, itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
V = json.load(open('golden_family.json'))['GF1']   # the DICTO Yantra (Cleo-Antonius)
f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(V['b']), f(V['w']), f(V['apex'])
phi = (1 + 5 ** .5) / 2
I = [np.array(p, float) for c in [(0, 1, phi), (1, phi, 0), (phi, 0, 1)] for p in itertools.product(*[(x, -x) if x else (0,) for x in c])]
I = [v / np.linalg.norm(v) for v in I]
E = min(np.linalg.norm(I[i] - I[j]) for i, j in itertools.combinations(range(12), 2))
faces = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(I[x] - I[y]) - E) < 1e-9 for x, y in itertools.combinations(t, 2))]
assert len(faces) == 20
c0 = (I[faces[0][0]] + I[faces[0][1]] + I[faces[0][2]]); c0 /= np.linalg.norm(c0)
RHO = math.acos(np.dot(c0, (I[faces[0][0]] + I[faces[0][1]]) / np.linalg.norm(I[faces[0][0]] + I[faces[0][1]])))   # centre to edge midpoint
print(f'inscribed-circle cap: {math.degrees(RHO):.4f} deg')
UP = {i for i in range(1, 10) if a[i] < b[i]}
segs = []
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (0, a[i]); segs += [(L, R, i), (L, A, i), (R, A, i)]
W = H = 1100; img = Image.new('RGB', (W, H), (10, 11, 16)); d = ImageDraw.Draw(img)
GOLD = (232, 194, 90); BLUE = (58, 112, 205); cx = cy = 550; Rpx = 470
tilt = np.array([[1, 0, 0], [0, math.cos(.35), -math.sin(.35)], [0, math.sin(.35), math.cos(.35)]]) @ np.array([[math.cos(.3), 0, math.sin(.3)], [0, 1, 0], [-math.sin(.3), 0, math.cos(.3)]])
d.ellipse([cx - Rpx, cy - Rpx, cx + Rpx, cy + Rpx], outline=(120, 120, 130), width=2)
sc = math.tan(RHO) / 0.5
for t in faces:
    cen = sum(I[k] for k in t); cen /= np.linalg.norm(cen)
    up = I[t[0]] - np.dot(I[t[0]], cen) * cen; up /= np.linalg.norm(up); rt = np.cross(up, cen)
    def P(x, dd): q = cen + (x * sc) * rt + ((0.5 - dd) * sc) * up; q /= np.linalg.norm(q); return tilt @ q
    for p, q, i in segs:
        pts = [P(p[0] + (q[0] - p[0]) * s, p[1] + (q[1] - p[1]) * s) for s in np.linspace(0, 1, 30)]
        for u_, v_ in zip(pts, pts[1:]):
            if u_[2] > 0 and v_[2] > 0: d.line([(cx + Rpx * u_[0], cy - Rpx * u_[1]), (cx + Rpx * v_[0], cy - Rpx * v_[1])], fill=GOLD if i in UP else BLUE, width=1)
    rim = [(lambda q: tilt @ (q / np.linalg.norm(q)))(cen + math.tan(RHO) * (math.cos(s) * rt + math.sin(s) * up)) for s in np.linspace(0, 2 * math.pi, 90)]
    for u_, v_ in zip(rim, rim[1:]):
        if u_[2] > 0 and v_[2] > 0: d.line([(cx + Rpx * u_[0], cy - Rpx * u_[1]), (cx + Rpx * v_[0], cy - Rpx * v_[1])], fill=(170, 170, 180), width=1)
fnt = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 22)
d.text((cx, 40), 'Twenty yantras on the bases of the twenty Cleo-Icos', font=fnt, fill=(230, 230, 235), anchor='mm')
d.text((W - 16, H - 14), 'DICTO · dictospheres.com', font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 16), fill=GOLD, anchor='rs')
img.save('cleo-sphere-yantras-gf1.png')
print('FINAL ok' if len(faces) == 20 and abs(math.degrees(RHO) - 20.9051) < 1e-3 else 'FINAL FAIL')
