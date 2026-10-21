# DICTO 2026-10-21: cover of the Kyushindo Cores paper, cut from the study figures (#18 standard: dark ground, DICTO mark).
#   python3 cover.py <kres/studies>
import sys, os
from PIL import Image, ImageDraw, ImageFont
S = sys.argv[1]; H = os.path.dirname(os.path.abspath(__file__))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE, BG = (238, 230, 214), (176, 165, 148), (20, 15, 11)
# (figure, crop box in its pixels, title, subtitle)
P = [('2026-10-20-cleo-towers/figures/shells-b.jpg', (2390, 170, 3200, 1100), 'DICTO Cleo Towers', 'shells of 1, 1, 2, 3, 5 beats, half cut away'),
     ('2026-10-20-cleo-towers/figures/polar-b.jpg', (2440, 170, 3250, 1100), 'DICTO Polar Cleo Towers', '5, 3, 2, 1, 1 beats, half cut away'),
     ('2026-10-20-og-spires/figures/og-spires.jpg', (1060, 380, 1980, 1240), 'The OG core', '20 Hex + 60 Deltoid Aktis, drawn out'),
     ('2026-10-20-ott-rays/figures/ott-rays.jpg', (1000, 400, 1860, 1160), 'The OTT core', '8 + 24 + 6 rays, drawn out'),
     ('2026-10-21-og-turned-out/figures/og-turned-out.jpg', (1150, 380, 2080, 1310), 'The OG turned out', 'the 80 Aktis flipped out at 1/φ height')]
cell, gap, side = 760, 40, 120
W = side * 2 + len(P) * cell + (len(P) - 1) * gap; Hh = 300 + cell + 290
im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
d.text((side, 70), 'DICTO Kyushindo Cores', font=f(96, True), fill=INK)
d.text((side, 190), 'Towers and spires round exact cores in Fibonacci beats · DICTO 2026', font=f(46), fill=MUTE)
for k, (fig, box, t, s) in enumerate(P):
    p = Image.open(os.path.join(S, fig)).convert('RGB').crop(box); p.thumbnail((cell, cell), Image.LANCZOS)
    x = side + k * (cell + gap); y = 300
    im.paste(p, (x + (cell - p.width) // 2, y + (cell - p.height) // 2))
    for txt, yy, fo, col in [(t, y + cell + 30, f(50, True), INK), (s, y + cell + 100, f(34), MUTE)]:
        while d.textlength(txt, font=fo) > cell + gap - 10: fo = ImageFont.truetype(fo.path, fo.size - 2)
        d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
m = 'DICTO · dictospheres.com'; d.text((W - side - d.textlength(m, font=f(36)), Hh - 70), m, font=f(36), fill=MUTE)
im.save(os.path.join(H, 'figures', 'cover.jpg'), quality=92); print('cover.jpg', im.size)
