# DICTO 2026-10-20: compose the DICTO Jewel figures from renders/shots (scenes of jewel_figs.py) -> figures/
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'shots'); OUT = os.path.join(H, 'figures')
L = json.load(open(os.path.join(H, 'renders', 'jewel-labels.json')))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE = (43, 38, 32), (109, 101, 86)
def sheet(idx, cols, path, title=None, sub=None, cell=520, gap=36, names=None, subs=None, arrows=False):
    rows = (len(idx) + cols - 1) // cols; top = 190 if title else 40; W = cols * cell + (cols - 1) * gap + 160; Hh = top + rows * (cell + 130) + 80
    im = Image.new('RGB', (W, Hh), 'white'); d = ImageDraw.Draw(im)
    if title: d.text((80, 46), title, font=f(60, True), fill=INK); d.text((80, 122), sub, font=f(30), fill=MUTE)
    for k, i in enumerate(idx):
        x = 80 + (k % cols) * (cell + gap); y = top + (k // cols) * (cell + 130)
        p = Image.open(f'{S}/p{i}.png').convert('RGBA').resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)
        nm = names[k] if names else L[i]['title']; sb = subs[k] if subs else L[i]['sub']
        for txt, yy, fo, col in [(nm, y + cell + 10, f(32, True), INK), (sb, y + cell + 54, f(24), MUTE)]:
            while d.textlength(txt, font=fo) > cell + gap - 6 and fo.size > 14: fo = ImageFont.truetype(fo.path, fo.size - 2)
            d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
        if arrows and k % cols < cols - 1 and k < len(idx) - 1:
            ax = x + cell + gap / 2; ay = y + cell / 2; d.text((ax - d.textlength('T', font=f(34, True)) / 2, ay - 60), 'T', font=f(34, True), fill=MUTE)
            d.text((ax - d.textlength('→', font=f(44)) / 2, ay - 22), '→', font=f(44), fill=MUTE)
    m = 'DICTO · dictospheres.com'; d.text((W - 80 - d.textlength(m, font=f(24)), Hh - 56), m, font=f(24), fill=MUTE)
    im.save(os.path.join(OUT, path), quality=90); print(path, im.size)
sheet([0, 6, 7], 3, 'cover.jpg', 'The DICTO Jewel', 'The Jewel, the Jewel Cube and the Jewel Cube Key, which fill space 5 : 3 · DICTO 2026')
sheet([1, 2], 2, 'lattice.jpg')
sheet([3, 4, 5], 3, 'clusters.jpg')
sheet([8], 1, 'cube-key.jpg', cell=760)
