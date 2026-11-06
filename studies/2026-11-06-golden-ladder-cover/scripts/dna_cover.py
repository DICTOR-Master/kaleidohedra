# The Golden Ladder cover, DNA version (DICTO 11-06: "solids close to each other forming a DNA strand spiraling up the front cover").
# Two helical strands of golden solids wind up the cover: Icosaxes (gold) on one, Unborn Axes (violet) on the other, half a turn apart;
# each pair is joined by a rung, so the helix is a twisted ladder. Each solid turns a little as it climbs. Painter's order by depth.
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from ladder_cover import Tx, rot, draw_solid, faces_of, GROUND, GOLD, VIOLET, TEAL, BLUE, W, Hc, phi
import ledtext as L
SS = 2; TOP = 2440                                    # height of the picture area above the title panel
cx = W / 2; R = 560; y0, y1 = 2330, 140               # helix radius and vertical span (px)
turns = 1.75; N = 26                                  # solids per strand
VA = Tx(phi); VA /= np.linalg.norm(VA, axis=1).max()
VB = Tx(1 / phi); VB /= np.linalg.norm(VB, axis=1).max()
img = Image.new('RGBA', (W * SS, TOP * SS), GROUND + (255,)); d = ImageDraw.Draw(img)
items = []   # (depth, kind, data)
for k in range(N):
    t = k / (N - 1); y = y0 + (y1 - y0) * t; a = 2 * np.pi * turns * t
    for strand, (V, col, off) in enumerate(((VA, GOLD, 0.0), (VB, VIOLET, np.pi))):
        x = cx + R * np.sin(a + off); z = np.cos(a + off)          # z = +1 nearest the viewer
        s = 118 * (1 + 0.22 * z)                                   # perspective: near solids larger
        items.append((z, 'solid', (V, x, y, s, col, rot(0.35 + 1.3 * t, 0.6 + 2.1 * t + strand, 0.2 * k))))
    if k % 2 == 0:                                                 # a rung between the pair
        xa, xb = cx + R * np.sin(a), cx + R * np.sin(a + np.pi); za, zb = np.cos(a), np.cos(a + np.pi)
        items.append(((za + zb) / 2 - 0.01, 'rung', (xa, xb, y, za, zb)))
for z, kind, data in sorted(items, key=lambda it: it[0]):
    dim = 0.55 + 0.45 * (z + 1) / 2                               # far side dimmer
    if kind == 'rung':
        xa, xb, y, za, zb = data; n = 24
        for i in range(n):
            u0, u1 = i / n, (i + 1) / n; zz = za + (zb - za) * (u0 + u1) / 2; dm = 0.45 + 0.55 * (zz + 1) / 2
            d.line([((xa + (xb - xa) * u0) * SS, y * SS), ((xa + (xb - xa) * u1) * SS, y * SS)],
                   fill=tuple(int(c * dm) for c in (190, 145, 30)) + (255,), width=int(14 * (1 + 0.15 * zz)) * SS)
    else:
        V, x, y, s, col, Rm = data
        draw_solid(d, V, x * SS, y * SS, s * SS, tuple(int(c * dim) for c in col), Rm)
pic = img.resize((W, TOP), Image.LANCZOS).convert('RGB')
Nw = W
big = L.word('THE GOLDEN LADDER', int(Nw * 0.058), lambda ch: GOLD, big=(0, 4, 11))
sub = L.word('GOLDEN CUTS FROM PLATO TO THE EIGHTH DIMENSION', int(Nw * 0.023), lambda ch: TEAL, big=(0, 12, 17, 23, 27, 34))
by = L.word('* DICTO *', int(Nw * 0.040), lambda ch: BLUE, big=(0, 2, 3, 4, 5, 6, 8))
panel = np.ones((Hc - TOP, Nw, 3)) * np.array(GROUND, float)
yy = L.paste(panel, big, Nw / 2, 50); yy = L.paste(panel, sub, Nw / 2, yy + 60); L.paste(panel, by, Nw / 2, yy + 70)
out = Image.new('RGB', (W, Hc), GROUND); out.paste(pic, (0, 0)); out.paste(Image.fromarray(np.clip(panel, 0, 255).astype(np.uint8)), (0, TOP))
out.save('../golden-ladder-cover-DNA.png'); print('FINAL OK')
