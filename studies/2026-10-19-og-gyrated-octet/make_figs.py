# DICTO 2026-10-20: the gyrated-octet paper's figures from renders/shots (shoot.mjs) -> figures/*.jpg
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'renders', 'shots'); OUT = os.path.join(H, 'figures'); os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
BG, INK, MUTE = (255, 255, 255), (43, 38, 32), (109, 101, 86)
figs = {'twins': [('00', 'Twin OGs', 'across a shared face'), ('01', 'The gyrated octet', 'three layers, A B A')],
        'kit': [('02', 'One kit for every stacking', 'OG, caps L/R, twin cap, tetrahedron, bipyramid'), ('05', 'Mirror middle piece', 'between an OG and its twin')],
        'family': [('03', 'Twin OCD Stellas', 'meeting on the whole triangle'), ('04', 'Twin DBTs', 'pole to pole across a twin layer')]}
for name, panels in figs.items():
    n = len(panels); S = 900; gap = 40; W = n * S + (n - 1) * gap + 80; Hh = S + 190
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    for i, (k, t, sub) in enumerate(panels):
        p = Image.open(f'{D}/{k}.png').convert('RGB'); w, h = p.size; p = p.crop((6, int(h * .04), w - 6, int(h * .95))); p.thumbnail((S, S), Image.LANCZOS)
        x = 40 + i * (S + gap); im.paste(p, (x + (S - p.width) // 2, 20 + (S - p.height) // 2))
        for txt, y, fo, col in [(t, S + 50, f(44, True), INK), (sub, S + 112, f(34), MUTE)]:
            d.text((x + S / 2 - d.textlength(txt, font=fo) / 2, y), txt, font=fo, fill=col)
    m = 'DICTO · dictospheres.com'; d.text((W - 40 - d.textlength(m, font=f(26)), Hh - 40), m, font=f(26), fill=MUTE)
    im.save(f'{OUT}/{name}.jpg', quality=88); print(name, im.size)
