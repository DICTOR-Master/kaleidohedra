# DICTO 2026-10-21: compose the figures of paper #44 from renders/shots (aristotle_figs.py + jewel-shots.mjs) -> figures/
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'shots'); OUT = os.path.join(H, 'figures'); os.makedirs(OUT, exist_ok=True)
L = json.load(open(os.path.join(H, 'renders', 'aristotle-labels.json')))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE, BG = (238, 230, 214), (176, 165, 148), (20, 15, 11)   # the #18 standard: dark ground
K = 2
def sheet(idx, cols, path, title, sub, cw, ch, gap=40):
    cw, ch, gap = cw * K, ch * K, gap * K
    rows = (len(idx) + cols - 1) // cols; top = 190 * K; W = cols * cw + (cols - 1) * gap + 160 * K; Hh = top + rows * (ch + 130 * K) + 70 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    d.text((80 * K, 46 * K), title, font=f(60 * K, True), fill=INK); d.text((80 * K, 122 * K), sub, font=f(30 * K), fill=MUTE)
    for k, i in enumerate(idx):
        x = 80 * K + (k % cols) * (cw + gap); y = top + (k // cols) * (ch + 130 * K)
        p = Image.open(f'{S}/p{i}.png').convert('RGBA'); p = p.crop(p.getbbox()); sc = min(cw / p.width, ch / p.height); p = p.resize((round(p.width * sc), round(p.height * sc)), Image.LANCZOS)   # fill the cell (may enlarge)
        im.paste(p, (x + (cw - p.width) // 2, y + (ch - p.height) // 2), p)
        for txt, yy, fo, col in [(L[i]['title'], y + ch + 14 * K, f(32 * K, True), INK), (L[i]['sub'], y + ch + 58 * K, f(24 * K), MUTE)]:
            while d.textlength(txt, font=fo) > cw + gap - 6 * K and fo.size > 14 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
            d.text((x + cw / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
    m = 'DICTO · dictospheres.com'; d.text((W - 80 * K - d.textlength(m, font=f(24 * K)), Hh - 52 * K), m, font=f(24 * K), fill=MUTE)
    im.save(os.path.join(OUT, path), quality=92); print(path, im.size)
sheet([0, 1, 2, 3, 4], 5, 'face-pyramids.jpg', 'The five face pyramids', 'Each Platonic solid cut from its centre: the cone over one face (gold), in its solid (glass)', 400, 400)
sheet([5, 6, 7, 8], 1, 'rhombohedra.jpg', 'Two rhombohedra, each cut in three', 'The octet\'s 60° rhombohedron (above) and the prolate golden rhombohedron (below)', 1640, 420, gap=20)
