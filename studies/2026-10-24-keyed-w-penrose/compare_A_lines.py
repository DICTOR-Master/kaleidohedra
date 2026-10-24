# DICTO 10-24 ("do you know what you are doing?"): picture A's rhombs on face 1 (faint) with the free band (white) and the ridge lines that
# actually survive in 3D (dark), so the 2D pattern and the 3D keys can be compared directly.
import json, math, cmath, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon
H = os.path.dirname(os.path.abspath(__file__)); G = json.load(open(os.path.join(H, 'keyed-W-geometry.json'))); Lj = json.load(open(os.path.join(H, 'penrose-W-lines.json')))
tri = np.array(G['face1_triangle_uv']); Sh = np.array(G['shadow_uv']); phi = (1 + 5 ** .5) / 2; L = Lj['rhomb_edge']
allowed = Polygon(tri).buffer(-0.035, join_style=2).difference(Polygon(Sh).buffer(0.025, join_style=2))
def subdivide(tris):
    out = []
    for c, a, b, cc in tris:
        if c == 0: p = a + (b - a) / phi; out += [(0, cc, p, b), (1, p, cc, a)]
        else: q = b + (a - b) / phi; r = b + (cc - b) / phi; out += [(1, r, cc, a), (1, q, r, b), (0, r, q, a)]
    return out
LEV = 7; tris = []
for i in range(10):
    b = cmath.rect(L * phi ** LEV, (2 * i - 1) * math.pi / 10); c = cmath.rect(L * phi ** LEV, (2 * i + 1) * math.pi / 10)
    if i % 2 == 0: b, c = c, b
    tris.append((0, 0j, b, c))
for _ in range(LEV): tris = subdivide(tris)
S, PAD = 900, 60; lo, hi = tri.min(0) - .05, tri.max(0) + .05; sc = (S - 2 * PAD) / max(hi - lo)
P = lambda p: (PAD + (p[0] - lo[0]) * sc, S - PAD - (p[1] - lo[1]) * sc)
im = Image.new('RGB', (S, S + 60), (246, 244, 239)); d = ImageDraw.Draw(im, 'RGBA')
d.polygon([P(q) for q in tri], fill=(255, 255, 255))
d.polygon([P(q) for q in Sh], fill=(157, 183, 220, 160))
for g in (getattr(allowed, 'geoms', None) or [allowed]): d.polygon([P(q) for q in g.exterior.coords], fill=(255, 236, 190))
for c, a, b, cc in tris:
    for p, q in ((a, b), (a, cc)): d.line([P((p.real, p.imag)), P((q.real, q.imag))], fill=(150, 130, 90, 110), width=1)
for l in Lj['lines_face1_uv']: d.line([P(l[0]), P(l[1])], fill=(120, 60, 10), width=7)
d.line([P(q) for q in list(tri) + [tri[0]]], fill=(31, 36, 48), width=3)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
d.text((PAD, 12), 'One face of W: picture A\'s rhombs (thin) and the 3D ridge lines (thick)', font=F, fill=(31, 36, 48))
d.text((PAD, S + 6), 'blue = the OG socket\'s shadow (keys must stay clear); pale yellow = the free band (34% of the face); thick = what survives', font=f, fill=(90, 90, 90))
d.text((S - 85, S + 30), 'DICTO', font=F, fill=(150, 150, 150)); im.save('/home/dicto/Documents/papers-to-read/keyed-w-face-compare.png'); print('saved')
