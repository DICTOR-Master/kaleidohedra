"""Spherical yantra (DICTO 11-08: 'spherical?'): the perfect yantra (the DICTO Yantra from the perfect viewpoint, viewpoint.json V1)
on the plane z = 1 touching the unit sphere at the pole, projected from the centre (gnomonic): every line -> a great circle, every
concurrency kept, the yantra's circle -> a small circle of angular radius RHO, the level bases -> great circles through two opposite
points on the equator. Panels: seen from above the cap, and from the side. Check: each marma's three great circles meet exactly
(the three planes through the centre share one line)."""
import json, math, itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
RHO = math.radians(60)
V = json.load(open('viewpoint.json'))['V1']; f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(V['b']), f(V['w']), f(V['apex'])
sc = math.tan(RHO) / 0.5                                  # circle radius 1/2 (diameter-1 frame) -> tan(RHO) on the plane z = 1
def plane(p): x, d = p; return np.array([x * sc, (0.5 - d) * sc, 1.0])
def sph(p): q = plane(p); return q / np.linalg.norm(q)
UP = {i for i in range(1, 10) if a[i] < b[i]}
segs = []
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (0, a[i]); segs += [(L, R, i), (L, A, i), (R, A, i)]
# exactness check: three lines through a marma <=> three planes through the centre share a line (det of the normals' span)
def normal(s): return np.cross(plane(s[0]), plane(s[1]))
W, H = 1500, 760; img = Image.new('RGB', (W, H), (10, 11, 16)); d = ImageDraw.Draw(img)
GOLD = (232, 194, 90); BLUE = (58, 112, 205)
def view(p, el):          # rotate about x by el (0 = looking down the pole axis), orthographic
    x, y, z = p; c, s = math.cos(el), math.sin(el); return (x, y * c - z * s, y * s + z * c)
def panel(cx, cy, R, el, title):
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(120, 120, 130), width=2)
    rim = [view((math.sin(RHO) * math.cos(t), math.sin(RHO) * math.sin(t), math.cos(RHO)), el) for t in np.linspace(0, 2 * math.pi, 241)]
    d.line([(cx + R * p[0], cy - R * p[1]) for p in rim], fill=(200, 200, 205), width=2)
    for p, q, i in segs:
        pts = [view(sph((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)), el) for t in np.linspace(0, 1, 60)]
        d.line([(cx + R * x, cy - R * y) for x, y, z in pts], fill=GOLD if i in UP else BLUE, width=2)
    d.text((cx, cy + R + 40), title, font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 22), fill=(230, 230, 235), anchor='mm')
panel(380, 360, 300, 0.0, 'from above the cap (60°)')
panel(1110, 360, 300, math.radians(-55), 'tilted: great circles on the sphere')
d.text((W - 18, H - 14), 'DICTO · dictospheres.com', font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 16), fill=GOLD, anchor='rs')
img.save('spherical-yantra.png')
# bases: their planes all contain the x-axis direction (1, 0, 0) (the two opposite points on the equator)
base_ok = all(abs(np.dot(normal(s), [1, 0, 0])) < 1e-12 for s in segs[0::3])
print('every level base is a great circle through (±1, 0, 0):', base_ok)
print('FINAL ok' if base_ok else 'FINAL FAIL')
