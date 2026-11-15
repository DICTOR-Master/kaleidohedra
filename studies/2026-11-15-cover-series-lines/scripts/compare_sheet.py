# Compare sheet: every front cover of THE FIVE ORDERS OF SPACE, old | new (series line), in book order; the Platonic Solids
# cover (the reference, already carrying its line) shown once. Run: python compare_sheet.py PAPERS_DIR OUT.png
# Colour sheet (15 Nov 2026): python compare_sheet.py PAPERS_DIR OUT.png colour -> white series line (v2) | element word in the
# ring's colour (v3), and for the Platonic Solids cover: white | element word coloured | whole line coloured (comparison only).
import os, sys
from PIL import Image, ImageDraw, ImageFont
P, OUT = sys.argv[1], sys.argv[2]; COLOUR = len(sys.argv) > 3 and sys.argv[3] == 'colour'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from series_covers_list import COVERS
H, PAD, LAB = 880, 24, 46
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
cells = []
for rel, book, part, _ in COVERS:
    d_, b_ = os.path.split(os.path.join(P, rel)); new = os.path.join(d_, b_[:-4].replace('-series', '') + '-series-v2.png')
    name = f'Book {book}' + (f', {part}' if part else '')
    if COLOUR:
        v3 = new.replace('-series-v2.png', '-series-v3.png')
        cells.append((name, [('white', new), ('element colour', v3)] if book != 8 else
                      [('white', os.path.join(P, rel)), ('element colour', os.path.join(d_, 'platonic-cover-front-series-v2.png')),
                       ('full colour', os.path.join(HERE, '..', 'platonic-cover-front-series-full.png'))]))
    else:
        cells.append((name, [('old', os.path.join(P, rel)), ('new', new)] if book != 8 else [('reference', os.path.join(P, rel))]))
def thumb(p):
    im = Image.open(p).convert('RGB'); return im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
groups = [(n, [(t, thumb(p)) for t, p in ims]) for n, ims in cells]
PER = 4; rows = [groups[i:i + PER] for i in range(0, len(groups), PER)]
gw = lambda g: sum(im.width for _, im in g[1]) + PAD * (len(g[1]) - 1)
Wsheet = max(sum(gw(g) for g in r) + PAD * 3 * (len(r) + 1) for r in rows)
sheet = Image.new('RGB', (Wsheet, len(rows) * (H + LAB + PAD) + PAD), 'white'); dr = ImageDraw.Draw(sheet)
y = PAD
for r in rows:
    x = PAD * 3
    for n, ims in r:
        for t, im in ims:
            dr.text((x, y), f'{n} · {t}', fill='black', font=F); sheet.paste(im, (x, y + LAB)); x += im.width + PAD
        x += PAD * 2
    y += H + LAB + PAD
sheet.save(OUT); print('FINAL ok', OUT, sheet.size)
