# DICTO 2026-10-20: compose the OG polytypes figures from renders/shots (scenes of polytype_figs.py) -> figures/
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'shots'); OUT = os.path.join(H, 'figures'); os.makedirs(OUT, exist_ok=True)
L = json.load(open(os.path.join(H, 'renders', 'stacks-labels.json')))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE = (43, 38, 32), (109, 101, 86)
def sheet(idx, path, title=None, sub=None, names=None, subs=None, cell=560, gap=30):
    cols = len(idx); top = 190 if title else 40; W = cols * cell + (cols - 1) * gap + 160; Hh = top + cell + 210
    im = Image.new('RGB', (W, Hh), 'white'); d = ImageDraw.Draw(im)
    if title: d.text((80, 46), title, font=f(60, True), fill=INK); d.text((80, 122), sub, font=f(30), fill=MUTE)
    for k, i in enumerate(idx):
        x = 80 + k * (cell + gap); y = top
        p = Image.open(f'{S}/p{i}.png').convert('RGBA').resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)
        for txt, yy, fo, col in [(names[k] if names else L[i]['title'], y + cell + 14, f(34, True), INK), (subs[k] if subs else L[i]['sub'], y + cell + 62, f(26), MUTE)]:
            while d.textlength(txt, font=fo) > cell + gap - 6 and fo.size > 14: fo = ImageFont.truetype(fo.path, fo.size - 2)
            d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
    m = 'DICTO · dictospheres.com'; d.text((W - 80 - d.textlength(m, font=f(24)), Hh - 56), m, font=f(24), fill=MUTE)
    im.save(os.path.join(OUT, path), quality=90); print(path, im.size)
sheet([0, 1, 2, 3], 'stacks.jpg', 'The OG on Every Stacking', 'OGs gold, mirror twins blue (each the OG turned 60°), twin layers faint red · side view, stacking axis upright · DICTO 2026',
      names=['3C · the octet', '2H · the gyrated octet', '6H', 'Fibonacci'], subs=['c c c c c c  ·  A B C A B C', 'h h h h h h  ·  A B A B', 'h c c h c c  ·  A B C A C B', 'c h c c h c …  ·  never repeats'])
sheet([4, 5, 6, 7], 'fit.jpg', names=['the OTT', 'the DBT', 'the golden envelope', 'the golden envelope'],
      subs=['on the Fibonacci stacking', 'on the Fibonacci stacking', 'across a c layer: no overlap', 'across an h layer: the tips overlap (red)'])
