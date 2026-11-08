"""The frame of the tetrahedral Sri Yantra (DICTO 11-08: 'the stella octangula is the rhombs'): the regular stella octangula
(up tetrahedron T and down tetrahedron T*) in its circumsphere, with the 3-fold axis vertical. Two views: down the axis, and from
the side. Exact corners: T = cube corners with xyz > 0, T* = the others, rotated so (1,1,1) points up. Checks the side view."""
import itertools, math
from PIL import Image, ImageDraw, ImageFont
s3 = math.sqrt(3)
T = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]; Ts = [tuple(-c for c in p) for p in T]
# rotation taking (1,1,1)/sqrt3 to z
import numpy as np
z = np.array([1,1,1]) / s3; x = np.array([1,-1,0]) / math.sqrt(2); y = np.cross(z, x)
Rm = np.vstack([x, y, z])
def rot(p): return Rm @ np.array(p, float)
def edges(P): return [(P[i], P[j]) for i, j in itertools.combinations(range(4), 2)]
W = 1400; H = 760; img = Image.new('RGB', (W, H), (10, 11, 16)); d = ImageDraw.Draw(img)
GOLD = (232, 194, 90); RED = (205, 62, 40); BLUE = (58, 112, 205)
f = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 22)
def panel(cx, cy, sc, proj, title):
    d.ellipse([cx - sc * s3, cy - sc * s3, cx + sc * s3, cy + sc * s3], outline=(120, 120, 130), width=2)
    for P, col in ((T, RED), (Ts, BLUE)):
        for a, b in edges([rot(p) for p in P]):
            A, B = proj(a), proj(b)
            d.line([cx + sc * A[0], cy - sc * A[1], cx + sc * B[0], cy - sc * B[1]], fill=col, width=4)
    d.text((cx, cy + sc * s3 + 34), title, font=f, fill=(230, 230, 235), anchor='mm')
panel(360, 350, 165, lambda p: (p[0], p[1]), 'down the axis: the hexagram')
panel(1040, 350, 165, lambda p: (p[0], p[2]), 'from the side: the upright rhombus')
d.text((W - 20, H - 18), 'DICTO · dictospheres.com', font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 16), fill=GOLD, anchor='rs')
img.save('stella-frame.png')
# check: side view outline = the projected apexes (top/bottom) and widest points form a rhombus
top = max(rot(p)[2] for p in T); bot = min(rot(p)[2] for p in Ts)
ok = abs(top - s3) < 1e-12 and abs(bot + s3) < 1e-12
print('apex heights', round(top, 6), round(bot, 6), '(= ± circumradius √3)')
print('FINAL ok' if ok else 'FINAL FAIL: apexes not on the sphere at the axis')
