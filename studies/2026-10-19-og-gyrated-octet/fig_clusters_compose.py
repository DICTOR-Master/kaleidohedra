# DICTO 2026-10-20: compose Figure 4 (three clusters) -> figures/clusters.jpg
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'cluster-shots')
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE = (43, 38, 32), (109, 101, 86)
labs = [('DBT + Fill set 1 F1', 'gyrated octet'), ('OTT + Fill set 2 F1', 'gyrated octet'), ('OTT + Fill set 2 F2, F3', 'octet')]
cell, gap = 820, 40; W = 3 * cell + 2 * gap + 80; Hh = cell + 190
im = Image.new('RGB', (W, Hh), (255, 255, 255)); d = ImageDraw.Draw(im)
for i, (t, s) in enumerate(labs):
    p = Image.open(f'{S}/p{i}.png').convert('RGBA').resize((cell, cell), Image.LANCZOS); x = 40 + i * (cell + gap); im.paste(p, (x, 10), p)
    for txt, y, fo, col in [(t, cell + 40, f(42, True), INK), (s, cell + 100, f(32), MUTE)]: d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, y), txt, font=fo, fill=col)
m = 'DICTO · dictospheres.com'; d.text((W - 40 - d.textlength(m, font=f(26)), Hh - 40), m, font=f(26), fill=MUTE)
im.save(os.path.join(H, 'figures', 'clusters.jpg'), quality=88); print('clusters', im.size)
