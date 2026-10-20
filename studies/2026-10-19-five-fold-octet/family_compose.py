# DICTO 2026-10-20: compose the OG family figures from renders/family-shots (shots.mjs) -> figures/
#   family-grid.jpg  the nine solids, 3 x 3, the OG in the centre, true relative size (cover)
#   breaks.jpg       where the nesting breaks, up and down
#   shells.jpg       the six shells that fill exactly, up (top row) and down (bottom row)
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'family-shots'); OUT = os.path.join(H, 'figures'); os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE, RULE = (43, 38, 32), (109, 101, 86), (220, 214, 202)
def sheet(cells, cols, path, title=None, sub=None, cell=560, gap=40):
    rows = (len(cells) + cols - 1) // cols; top = 200 if title else 40; W = cols * cell + (cols - 1) * gap + 160; Hh = top + rows * (cell + 130) + 90
    im = Image.new('RGB', (W, Hh), 'white'); d = ImageDraw.Draw(im)
    if title: d.text((80, 50), title, font=f(64, True), fill=INK); d.text((80, 130), sub, font=f(32), fill=MUTE)
    for k, (i, name, line2) in enumerate(cells):
        x = 80 + (k % cols) * (cell + gap); y = top + (k // cols) * (cell + 130)
        p = Image.open(f'{S}/p{i}.png').convert('RGBA').resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)
        for txt, yy, fo, col in [(name, y + cell + 12, f(34, True), INK), (line2, y + cell + 58, f(26), MUTE)]:
            while d.textlength(txt, font=fo) > cell + gap - 6 and fo.size > 16: fo = ImageFont.truetype(fo.path, fo.size - 2)
            d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
    m = 'DICTO · dictospheres.com'; d.text((W - 80 - d.textlength(m, font=f(26)), Hh - 60), m, font=f(26), fill=MUTE)
    im.save(os.path.join(OUT, path), quality=90); print(path, im.size)
grid = [(0, 'DICTO TQHD', '162 corners · down 4'), (1, 'DICTO TQP', '140 corners · down 3'), (2, 'DICTO TQH', '132 corners · down 2'),
        (3, 'DICTO TPH', '80 corners · down 1'), (4, 'DICTO OG', 'Ogdoecontahedron · 102 corners'), (5, 'DICTO KRE', '92 corners · up 1'),
        (6, 'DICTO PHE', '180 corners · up 2'), (7, 'DICTO TPP', '212 corners · up 3'), (8, 'DICTO DPHP', '270 corners · up 4')]
sheet(grid, 3, 'family-grid.jpg', 'The OG Family, Both Ways', 'Four steps down and four up from the Ogdoecontahedron · true relative size · DICTO 2026')
sheet([(9, 'DICTO TPP in DICTO DPHP', '60 corners poke out, by up to 0.0185'), (10, 'DICTO TQP in DICTO TQH', '60 corners poke out, by up to 0.0058')], 2, 'breaks.jpg')
sheet([(11, 'OG → KRE', '60 + 20 pieces'), (12, 'KRE → PHE', '90 pieces'), (13, 'PHE → TPP', '12 + 80 pieces'),
       (14, 'TPH → OG', '120 + 12 pieces'), (15, 'TQH → TPH', '60 + 60 + 20 pieces'), (16, 'TQHD → TQP', '120 + 60 + 20 pieces')], 3, 'shells.jpg')
