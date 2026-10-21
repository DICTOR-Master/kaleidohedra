# DICTO 2026-10-21: compose the polar of the OG turned out from renders/polar-shots (scenes of polar_figs.py) -> figures/
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'polar-shots'); OUT = os.path.join(H, 'figures')
L = json.load(open(os.path.join(H, 'renders', 'polar-labels.json')))
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
os.makedirs(OUT, exist_ok=True)
sheet([0, 1, 2, 3, 4], 5, 'polar-turned-out.jpg', 'The polar of the OG turned out', 'Reciprocated: the Hecatodihedron outside, the beats shrinking inward; polar(P(S)) = T(polar S)', cell=420)
