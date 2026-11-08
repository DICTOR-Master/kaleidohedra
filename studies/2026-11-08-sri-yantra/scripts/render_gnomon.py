"""Picture of the gnomon yantra G1: the yantra, a copy scaled by k inside the bindu's centred incircle, and a magnified view of the
bindu showing the copy (and the next copy, k^2). Mark DICTO · dictospheres.com."""
import json, math
from PIL import Image, ImageDraw, ImageFont
G = json.load(open('figures/gnomon.json'))['G1']; k = float(G['k'])
f = lambda d: {int(i): float(v['a']) for i, v in d.items()}
b, w, a = f(G['b']), f(G['w']), f(G['apex'])
def segs(scale, cx, cy, R):           # depth d in [0,1] -> y; centre (cx, cy), outer radius R * scale
    out = []
    for i in range(1, 10):
        L = (-w[i], b[i]); Rr = (w[i], b[i]); A = (0, a[i])
        for p, q in ((L, Rr), (L, A), (Rr, A)):
            P = lambda t: (cx + 2 * R * scale * t[0], cy + 2 * R * scale * (t[1] - 0.5))
            out.append((P(p), P(q), i))
    return out
W, H = 1700, 900; img = Image.new('RGB', (W, H), (252, 250, 244)); d = ImageDraw.Draw(img)
GOLD = (190, 140, 40); BLUE = (40, 80, 160); RED = (190, 50, 40)
UP = {i for i in range(1, 10) if a[i] < b[i]}
def draw(cx, cy, R, scale, width):
    d.ellipse([cx - R * scale, cy - R * scale, cx + R * scale, cy + R * scale], outline=(60, 60, 60), width=max(1, width - 1))
    for p, q, i in segs(scale, cx, cy, R): d.line([p, q], fill=GOLD if i in UP else BLUE, width=width)
R = 400; cx, cy = 450, 440
draw(cx, cy, R, 1, 2); draw(cx, cy, R, k, 1)
left = img.copy()
# magnified bindu on its own canvas, clipped to a circle, then composed on the right
M = 1.6 * k; cx2, cy2 = 1240, 440; R2 = 400
mag = Image.new('RGB', (W, H), (252, 250, 244)); d = ImageDraw.Draw(mag)
for p, q, i in segs(1, cx2, cy2, R2 / M): d.line([p, q], fill=GOLD if i in UP else BLUE, width=3)
draw(cx2, cy2, R2 / M, k, 2); draw(cx2, cy2, R2 / M, k * k, 1)
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse([cx2 - R2, cy2 - R2, cx2 + R2, cy2 + R2], fill=255)
img = Image.composite(mag, left, mask); d = ImageDraw.Draw(img)
d.ellipse([cx2 - R2, cy2 - R2, cx2 + R2, cy2 + R2], outline=(120, 120, 120), width=2)
d.line([cx + k * R * 1.6, cy, cx2 - R2, cy2], fill=(150, 150, 150), width=1)
fnt = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 20)
d.text((cx, 870), 'the yantra and, in its bindu, the next one (ratio k = 0.0631)', font=fnt, fill=(40, 40, 40), anchor='mm')
d.text((cx2, 870), 'the bindu magnified: the copy, and its own copy', font=fnt, fill=(40, 40, 40), anchor='mm')
d.text((W - 16, 24), 'DICTO · dictospheres.com', font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 16), fill=GOLD, anchor='rm')
img.save('figures/gnomon-yantra.png'); print('FINAL ok' if 0 < k < 0.2 else 'FINAL FAIL: ratio out of range')
