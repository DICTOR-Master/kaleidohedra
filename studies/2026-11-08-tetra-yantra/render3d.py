"""The DICTO Yantra in three dimensions (DICTO 11-08): every triangle of the flat yantra becomes a tetrahedron (triangular pyramid)
with its tip on the vertical axis and a level base; spinning, each sweeps a cone, and the flat yantra is exactly the axial section of
the nine nested cones (its 9 mirror pairs of marmas become 9 circles where two cones and one level disc meet). Still, the pyramids
(bases inscribed in the cones' base circles; apex-down ones turned 60 degrees, as in the stella octangula) show from the three
positions on the great circles the yantra narrowed to cos 30 (an affine image: every concurrency kept). Data: golden_family.json GF1 (the DICTO Yantra).
Panels: (1) spinning cones in the sphere, (2) the still tetrahedra, (3) side view of the still tetrahedra at one of the three positions."""
import json, math, itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
K = json.load(open('golden_family.json'))['GF1']   # the DICTO Yantra (Cleo-Antonius)
f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(K['b']), f(K['w']), f(K['apex'])
UP = {i for i in range(1, 10) if a[i] < b[i]}           # apex above base (depth smaller)
z = lambda d: 0.5 - d                                     # height, sphere centre 0
E = math.radians(18)
def proj(p): x, y, h = p; return (x, h * math.cos(E) + y * math.sin(E), -y * math.cos(E) + h * math.sin(E))
W, H = 1800, 860; img = Image.new('RGB', (W, H), (10, 11, 16)); dr = ImageDraw.Draw(img, 'RGBA')
font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 22); small = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 16)
GOLD = (232, 194, 90); BLUE = (58, 112, 205); RED = (205, 62, 40)
def col(i): return GOLD if i in UP else BLUE
def P(cx, cy, sc, q): return (cx + sc * q[0], cy - sc * q[1])
def sphere(cx, cy, sc): dr.ellipse([cx - sc * 0.5, cy - sc * 0.5, cx + sc * 0.5, cy + sc * 0.5], outline=(140, 140, 150), width=2)
# triple points of the flat yantra (for the marma circles)
segs = []
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (0.0, a[i]); segs += [(L, R), (L, A), (R, A)]
def inter(s, t):
    (x1, y1), (x2, y2) = s; (x3, y3), (x4, y4) = t; den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-14: return None
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den; py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    on = lambda p, q: min(p[0], q[0]) - 1e-12 <= px <= max(p[0], q[0]) + 1e-12 and min(p[1], q[1]) - 1e-12 <= py <= max(p[1], q[1]) + 1e-12
    return (round(px, 9), round(py, 9)) if on(*s) and on(*t) else None
cnt = {}
for s, t in itertools.combinations(segs, 2):
    q = inter(s, t)
    if q: cnt.setdefault(q, set()).update({segs.index(s), segs.index(t)})
corn = {(round(x, 9), round(y, 9)) for i in range(1, 10) for (x, y) in [(-w[i], b[i]), (w[i], b[i]), (0, a[i])]}
marmas = sorted({(abs(q[0]), q[1]) for q, s in cnt.items() if len(s) >= 3 and q not in corn and q[0] ** 2 + (q[1] - .5) ** 2 < .25})
TH = np.linspace(0, 2 * math.pi, 181)
def circle3(r, d): return [proj((r * math.cos(t), r * math.sin(t), z(d))) for t in TH]
# panel 1: spinning cones, drawn back to front by depth of base
cx, cy, sc = 300, 400, 560
sphere(cx, cy, sc)
for i in sorted(range(1, 10), key=lambda i: -w[i]):
    ring = circle3(w[i], b[i]); ap = proj((0, 0, z(a[i])))
    pts = [P(cx, cy, sc, q) for q in ring] + [P(cx, cy, sc, ap)]
    hull = []
    for p in sorted(set(pts)):            # convex hull (monotone chain)
        while len(hull) >= 2 and (hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1]) - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0]) <= 0: hull.pop()
        hull.append(p)
    up = hull[:]; hull = []
    for p in sorted(set(pts), reverse=True):
        while len(hull) >= 2 and (hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1]) - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0]) <= 0: hull.pop()
        hull.append(p)
    poly = up[:-1] + hull[:-1]
    c = col(i); dr.polygon(poly, fill=c + (38,), outline=c + (210,))
    dr.line([P(cx, cy, sc, q) for q in ring], fill=c + (160,), width=1)
for (r, d) in marmas: dr.line([P(cx, cy, sc, q) for q in circle3(r, d)], fill=RED + (230,), width=3)
dr.text((cx, 735), 'spinning: nine nested cones', font=font, fill=(230, 230, 235), anchor='mm')
dr.text((cx, 765), f'red: the {len(marmas)} marma circles (two cones and a disc meet)', font=small, fill=(200, 200, 205), anchor='mm')
# panel 2: still tetrahedra
cx = 900
sphere(cx, cy, sc)
def tet(i):
    off = math.pi / 2 if i in UP else math.pi / 2 + math.pi / 3
    base = [(w[i] * math.cos(off + k * 2 * math.pi / 3), w[i] * math.sin(off + k * 2 * math.pi / 3), z(b[i])) for k in range(3)]
    return base, (0, 0, z(a[i]))
for i in sorted(range(1, 10), key=lambda i: -w[i]):
    base, ap = tet(i); c = col(i)
    for p, q in list(itertools.combinations(base, 2)) + [(p, ap) for p in base]:
        dr.line([P(cx, cy, sc, proj(p)), P(cx, cy, sc, proj(q))], fill=c + (230,), width=3 if i in (3, 7) else 2)
dr.text((cx, 735), 'still: the tetrahedra', font=font, fill=(230, 230, 235), anchor='mm')
dr.text((cx, 765), 'great pair: the Cleo-Antonius', font=small, fill=(200, 200, 205), anchor='mm')
# panel 3: side view at one of the three positions (view along a mirror plane): x -> x * cos30 for these pyramids
cx = 1500; s3 = math.sqrt(3) / 2
dr.ellipse([cx - sc * 0.5, cy - sc * 0.5, cx + sc * 0.5, cy + sc * 0.5], outline=(140, 140, 150), width=2)
for i in range(1, 10):
    c = col(i); L, R, A = (-w[i] * s3, z(b[i])), (w[i] * s3, z(b[i])), (0, z(a[i]))
    for p, q in ((L, R), (L, A), (R, A)): dr.line([P(cx, cy, sc, p), P(cx, cy, sc, q)], fill=c + (230,), width=2)
for (r, d) in marmas:
    for sgn in (-1, 1): x, y = P(cx, cy, sc, (sgn * r * s3, z(d))); dr.ellipse([x - 5, y - 5, x + 5, y + 5], fill=RED)
dr.text((cx, 735), 'still, from one of the three positions', font=font, fill=(230, 230, 235), anchor='mm')
dr.text((cx, 765), 'the yantra narrowed to cos 30°: all 18 meetings kept', font=small, fill=(200, 200, 205), anchor='mm')
dr.text((W // 2, 40), 'The DICTO Yantra in three dimensions', font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf', 30), fill=GOLD, anchor='mm')
dr.text((W - 20, H - 16), 'DICTO · dictospheres.com', font=small, fill=GOLD, anchor='rs')
img.save('dicto-yantra-3d-gf1.png')
print('marma circles:', len(marmas))
print('FINAL ok' if len(marmas) == 9 else f'FINAL FAIL: {len(marmas)} marma circles, expected 9')
