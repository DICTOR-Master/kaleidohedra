# DICTO · dictospheres.com — Figures 1 and 2 of the Dehn packets paper in the 3D card style (shots of scenes6.py: renders/ring, renders/screen; ring.json).
import os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from render3d import project
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, 'figures'); os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', int(s))
INK, MUTE, BG, RED = (238, 230, 214), (176, 165, 148), (20, 15, 11), (211, 58, 44)
MARK = 'DICTO · dictospheres.com'
def tw(d, t, fo): return d.textlength(t, font=fo)
def ctext(d, x, y, t, fo, col): d.text((x - tw(d, t, fo) / 2, y), t, font=fo, fill=col)
def hexc(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def paste(im, path, x, y, size):
    p = Image.open(path).convert('RGBA'); p = p.resize((size, size), Image.LANCZOS); im.paste(p, (x, y), p)
# ================= Figure 1: the ring =================
J = json.load(open(os.path.join(R, 'ring.json'))); E = J['E']; DIR = np.array(J['dir']); W_, H_ = 2400, 1840
im = Image.new('RGB', (W_, H_), BG); d = ImageDraw.Draw(im)
d.text((80, 44), 'One edge, one and a half turns', font=f(70, True), fill=INK)
d.text((80, 132), 'Lead 1 of Theorem 4: the angles of the pieces at one edge, wedge by wedge · beyond 360° they overlap (ghosted, red)', font=f(30), fill=MUTE)
cell = 1290; x0, y0 = 90, 180; paste(im, os.path.join(R, 'ring', 'p0.png'), x0, y0, cell)
COL = {'pyramid base': (122, 80, 180), 'TI pentagon–hexagon': (189, 184, 170), 'TI hexagon–hexagon': (139, 135, 124)}
for k, nm, a, d0, d1 in J['wedges']:
    mid = (d0 + d1) / 2; over = mid >= 360 or (d0 >= 360)
    rr = 1.30 if (mid % 360) >= 0 else 1.3
    m = (d0 + d1) / 2
    t = math.radians(m % 360); P = np.array([[rr * math.cos(t), rr * math.sin(t), 0.0]])
    px, py = project(P, DIR, E)[0]; px = x0 + px * cell / 1600; py = y0 + py * cell / 1600
    txt = f'{k}  {a:.2f}°'
    fo = f(36, True); w = tw(d, txt, fo)
    d.rounded_rectangle((px - w / 2 - 12, py - 24, px + w / 2 + 12, py + 24), radius=10, fill=(20, 15, 11), outline=RED if m > 360 else (90, 80, 66), width=3)
    d.text((px - w / 2, py - 22), txt, font=fo, fill=INK)
# right: wheel inset
cx, cy, rad = 1830, 560, 250
d.text((1480, 205), 'What one turn can take', font=f(40, True), fill=INK)
d.text((1480, 258), 'The first three wedges fill 339.09°; 20.91° remain.', font=f(30), fill=MUTE)
cum = 0.0
for k, nm, a, d0, d1 in J['wedges'][:3]:
    d.pieslice((cx - rad, cy - rad + 40, cx + rad, cy + rad + 40), -d1, -d0, fill=COL[nm], outline=(43, 38, 30), width=3)
d.pieslice((cx - rad, cy - rad + 40, cx + rad, cy + rad + 40), -360, -(360 - J['gap']) - 0, fill=(20, 15, 11), outline=RED, width=4)
d.text((cx - 70, cy + 40 - 14), '', font=f(30), fill=INK)
d.text((cx + rad + 20, cy + 40 - 18), f'{J["gap"]:.2f}°', font=f(36, True), fill=RED)
d.text((cx + rad + 20, cy + 40 + 24), 'left at 360°', font=f(28), fill=MUTE)
d.text((1480, 880), 'but the next pieces bring 200.91°:', font=f(32), fill=INK)
d.text((1480, 930), '142.62° + 58.28°, and so 180° too many.', font=f(32), fill=INK)
# bottom: the strip 0..540
sx0, sx1, sy = 100, 2300, 1590; sc = (sx1 - sx0) / 540.0
d.text((100, 1400), 'The ring as a strip, 0° to 540°', font=f(38, True), fill=INK)
for k, nm, a, d0, d1 in J['wedges']:
    d.rectangle((sx0 + d0 * sc, sy - 60, sx0 + d1 * sc, sy + 20), fill=COL[nm], outline=(43, 38, 30), width=3)
    ctext(d, sx0 + (d0 + d1) / 2 * sc, sy - 48, f'{a:.2f}°', f(34, True), (20, 15, 11) if nm != 'pyramid base' else (240, 232, 255))
d.rectangle((sx0 + 360 * sc, sy - 60, sx1, sy + 20), outline=RED, width=5)
d.line((sx0 + 360 * sc, sy - 100, sx0 + 360 * sc, sy + 50), fill=RED, width=6)
d.text((sx0 + 360 * sc - 190, sy - 150), 'one full turn, 360°', font=f(32, True), fill=RED)
d.text((sx0 + 360 * sc + 14, sy + 38), '180° beyond: the ring cannot close', font=f(32), fill=RED)
d.text((sx0, sy + 38), '0°', font=f(30), fill=MUTE); d.text((sx1 - 78, sy + 38), '540°', font=f(30), fill=MUTE)
# legend
lx, ly = 100, 1720
for col, txt in [(COL['pyramid base'], 'pyramid base angle'), (COL['TI pentagon–hexagon'], 'truncated icosahedron: pentagon–hexagon'), (COL['TI hexagon–hexagon'], 'truncated icosahedron: hexagon–hexagon')]:
    d.rounded_rectangle((lx, ly + 6, lx + 54, ly + 32), radius=6, fill=col); d.text((lx + 66, ly), txt, font=f(30), fill=INK); lx += 66 + tw(d, txt, f(30)) + 50
d.text((W_ - 80 - tw(d, MARK, f(26)), H_ - 60), MARK, font=f(26), fill=MUTE)
im.save(os.path.join(OUT, 'fig-ring-3d.png'), optimize=True); print('fig1', im.size)
# ================= Figure 2: the screen =================
CL = [('zero', 3, 'packet zero', 'no partner needed', (214, 180, 106), ['cube', 'rhombic dodecahedron', 'rhombic triacontahedron']),
      ('one', 10, 'one helper', 'one piece cancels the packet', (127, 147, 168), ['tetrahedron', 'octahedron', 'dodecahedron']),
      ('two', 17, 'two helpers', 'a pair cancels, no single piece', (156, 116, 72), ['truncated tetrahedron', 'rhombicuboctahedron', 'icosidodecahedron']),
      ('none', 17, 'none in the library', 'no one or two pieces cancel', (201, 158, 149), ['triakis tetrahedron', 'triakis octahedron', 'deltoidal icositetrahedron'])]
assert sum(c[1] for c in CL) == 47
W2, H2 = 2400, 1800; im = Image.new('RGB', (W2, H2), BG); d = ImageDraw.Draw(im)
d.text((80, 44), 'The 47 centre pyramids, sorted by what cancels them', font=f(66, True), fill=INK)
d.text((80, 130), 'Proposition 6 · three examples of each class, drawn from the exact solids, not to scale', font=f(29), fill=MUTE)
colw = (W2 - 160) // 4; i = 0
for cl, n, t1, t2, col, names in CL:
    x = 80 + CL.index((cl, n, t1, t2, col, names)) * colw
    d.rounded_rectangle((x, 200, x + colw - 30, H2 - 130), radius=22, outline=(70, 62, 50), width=3)
    d.text((x + 30, 215), str(n), font=f(190, True), fill=col)
    d.text((x + 30, 430), t1, font=f(44, True), fill=INK); d.text((x + 30, 486), t2, font=f(30), fill=MUTE)
    d.rectangle((x + 30, 540, x + 30 + int((colw - 90) * n / 17), 560), fill=col)
    for j, nm in enumerate(names):
        paste(im, os.path.join(R, 'screen', f'p{i}.png'), x + (colw - 30 - 260) // 2, 575 + j * 355, 260); i += 1
        ctext(d, x + (colw - 30) / 2, 575 + j * 355 + 258, nm, f(32), INK)
d.text((W2 - 80 - tw(d, MARK, f(26)), H2 - 70), MARK, font=f(26), fill=MUTE)
im.save(os.path.join(OUT, 'fig-screen-3d.png'), optimize=True); print('fig2', im.size)
