# DICTO 2026-10-21: compose the figure of one new cycle from renders/shots-<X> (scenes of cycles_figs.py) -> figures/. #18 standard,
# dark ground (20, 15, 11). Adapted from og-turned-out/golden_compose.py (rows from the layout; None = empty cell).
# usage: python3 cycles_compose.py A|B|C
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); W_ = sys.argv[1]; S = os.path.join(H, 'renders', f'shots-{W_}'); OUT = os.path.join(H, 'figures')
J = json.load(open(os.path.join(H, 'renders', f'cycles-{W_}-labels.json'))); L = J['labels']
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE, BG = (238, 230, 214), (176, 165, 148), (20, 15, 11)
K = 2; cell, gap = 400 * K, 36 * K; rows = J['layout']; cols = max(len(r) for r in rows)
top = 190 * K; W = cols * cell + (cols - 1) * gap + 160 * K; Hh = top + len(rows) * (cell + 130 * K) + 80 * K
im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
d.text((80 * K, 46 * K), J['title'], font=f(60 * K, True), fill=INK)
fo = f(26 * K)
while d.textlength(J['sub'], font=fo) > W - 160 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
d.text((80 * K, 122 * K), J['sub'], font=fo, fill=MUTE)
for r, row in enumerate(rows):
    for c, i in enumerate(row):
        if i is None: continue
        x = 80 * K + c * (cell + gap); y = top + r * (cell + 130 * K)
        p = Image.open(f'{S}/p{i}.png').convert('RGBA').resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)
        for txt, yy, fo, col in [(L[i]['title'], y + cell + 10 * K, f(30 * K, True), INK), (L[i]['sub'], y + cell + 54 * K, f(22 * K), MUTE)]:
            while d.textlength(txt, font=fo) > cell + gap - 6 * K and fo.size > 12 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
            d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
m = 'DICTO · dictospheres.com'; d.text((W - 80 * K - d.textlength(m, font=f(24 * K)), Hh - 56 * K), m, font=f(24 * K), fill=MUTE)
os.makedirs(OUT, exist_ok=True); im.save(os.path.join(OUT, J['out']), quality=90); print(J['out'], im.size)
