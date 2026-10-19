# DICTO 2026-10-20: compose the cover line-up (two rows: solids, fill pieces) -> figures/cover-lineup.jpg
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'cover-shots')
L = json.load(open(os.path.join(H, 'renders', 'lineup-labels.json')))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
BG, INK, MUTE, RULE = (255, 255, 255), (43, 38, 32), (109, 101, 86), (220, 214, 202)
cell, gap, top = 600, 30, 230; W = 4 * cell + 3 * gap + 160; rowh = cell + 120; Hh = top + 2 * rowh + 150
im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
t = 'The OG on the Gyrated Octet'; d.text((80, 70), t, font=f(72, True), fill=INK)
d.text((80, 160), 'The solids and the pieces that fill the rest of space · DICTO 2026', font=f(36), fill=MUTE)
for row, lab in enumerate(('Solids', 'Fill pieces')):
    y0 = top + row * rowh
    d.text((80, y0 + 6), lab.upper(), font=f(24, True), fill=MUTE); d.line((80 + d.textlength(lab.upper(), font=f(24, True)) + 18, y0 + 20, W - 80, y0 + 20), fill=RULE, width=2)
    for k in range(4):
        i = row * 4 + k; p = Image.open(f'{S}/p{i}.png').convert('RGBA'); p = p.resize((cell, cell), Image.LANCZOS)
        x = 80 + k * (cell + gap); im.paste(p, (x, y0 + 30), p)
        nm, sb = L[i]['name'], L[i]['sub']
        for txt, yy, fo, col in [(nm, y0 + cell + 20, f(38, True), INK), (sb, y0 + cell + 70, f(28), MUTE)]:
            while d.textlength(txt, font=fo) > cell and fo.size > 18: fo = f(fo.size - 2, fo == f(38, True))
            d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
m = 'DICTO · dictospheres.com'; d.text((W - 80 - d.textlength(m, font=f(28)), Hh - 70), m, font=f(28), fill=MUTE)
im.save(os.path.join(H, 'figures', 'cover-lineup.jpg'), quality=90); print('cover', im.size)
