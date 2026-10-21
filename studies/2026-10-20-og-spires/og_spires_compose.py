# DICTO 2026-10-20: compose the OG spires figures from renders/shots (scenes of og_spires_figs.py) -> figures/
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'shots'); OUT = os.path.join(H, 'figures')
L = json.load(open(os.path.join(H, 'renders', 'og-spires-labels.json')))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE, BG = (238, 230, 214), (176, 165, 148), (20, 15, 11)   # the #18 standard: dark ground
K = 2                                             # compose at twice the old size (renders are 1200 px), for sharp print
def sheet(idx, cols, path, title=None, sub=None, cell=520, gap=36, names=None, subs=None, arrows=False):
    cell, gap = cell * K, gap * K
    rows = (len(idx) + cols - 1) // cols; top = (190 if title else 40) * K; W = cols * cell + (cols - 1) * gap + 160 * K; Hh = top + rows * (cell + 130 * K) + 80 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    if title: d.text((80 * K, 46 * K), title, font=f(60 * K, True), fill=INK); d.text((80 * K, 122 * K), sub, font=f(30 * K), fill=MUTE)
    for k, i in enumerate(idx):
        x = 80 * K + (k % cols) * (cell + gap); y = top + (k // cols) * (cell + 130 * K)
        p = Image.open(f'{S}/p{i}.png').convert('RGBA').resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)
        nm = names[k] if names else L[i]['title']; sb = subs[k] if subs else L[i]['sub']
        for txt, yy, fo, col in [(nm, y + cell + 10 * K, f(32 * K, True), INK), (sb, y + cell + 54 * K, f(24 * K), MUTE)]:
            while d.textlength(txt, font=fo) > cell + gap - 6 * K and fo.size > 14 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
            d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
    m = 'DICTO · dictospheres.com'; d.text((W - 80 * K - d.textlength(m, font=f(24 * K)), Hh - 56 * K), m, font=f(24 * K), fill=MUTE)
    im.save(os.path.join(OUT, path), quality=92); print(path, im.size)
# names DICTO's (2026-10-20): Hex Aktis (on the hexagons), Deltoid Aktis (on the kites)
L[1]['title'] = '80 Aktis, drawn out'; L[2]['sub'] = 'the Aktis meet in the middle'
for i, (t, s) in zip((3, 4), [('Hex Aktis', '20 of them, one shape'), ('Deltoid Aktis', '60 of them, one shape')]): L[i]['title'], L[i]['sub'] = t, s
sheet([0, 1, 2, 3, 4], 5, 'og-spires.jpg', 'The DICTO OG core of 80 Aktis', '20 DICTO Hex Aktis (gold) and 60 DICTO Deltoid Aktis (purple), every tip at the centre · DICTO 2026', cell=420)

