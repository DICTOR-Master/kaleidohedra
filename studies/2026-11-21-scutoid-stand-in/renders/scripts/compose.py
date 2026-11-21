# DICTO · dictospheres.com — compose the resin-solution renders from the shots of scenes.py (renders/<scene>/p<i>.png), in the
# house look of paper #115's fig_compose.py: dark warm ground, bold title, grey subtitle, a line under each panel, swatches, the
# DICTO mark. Kind colours are labels only; violet is the dodecahedron colour (C1's pyramids are dodecahedron centre pyramids).
import os
from PIL import Image, ImageDraw, ImageFont

H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, 'figures')
os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', int(s))
INK, MUTE, BG = (238, 230, 214), (176, 165, 148), (20, 15, 11)
K = 2; PX = 1600; MARK = 'DICTO · dictospheres.com'
KIND = [(214, 180, 106), (156, 116, 72), (127, 147, 168), (201, 158, 149), (143, 138, 128)]


def fit(d, txt, fo, w):
    while d.textlength(txt, font=fo) > w and fo.size > 14 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
    return fo


def ctext(d, x, y, txt, fo, col, w):
    fo = fit(d, txt, fo, w); d.text((x - d.textlength(txt, font=fo) / 2, y), txt, font=fo, fill=col)


def paste(im, path, x, y, cell):
    p = Image.open(path).convert('RGBA'); bb = p.getbbox()
    assert bb and bb[0] > 2 and bb[1] > 2 and bb[2] < PX - 2 and bb[3] < PX - 2, f'{path}: solid touches the shot edge {bb}'
    p = p.resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)


def swatch(d, x, y, col, txt, fo):
    d.rounded_rectangle((x, y + 6 * K, x + 54 * K, y + 26 * K), radius=5 * K, fill=col)
    d.text((x + 66 * K, y), txt, font=fo, fill=INK); return x + 66 * K + d.textlength(txt, font=fo) + 44 * K


def figure(name, title, sub, row, legend, cell=520, gap=40):
    cols = len(row); cell *= K; gap *= K
    W = max(cols * cell + (cols - 1) * gap + 160 * K, 1400 * K)
    Hh = 200 * K + cell + 110 * K + (80 * K if legend else 0) + 80 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    d.text((80 * K, 46 * K), title, font=fit(d, title, f(56 * K, True), W - 160 * K), fill=INK)
    d.text((80 * K, 122 * K), sub, font=fit(d, sub, f(28 * K), W - 160 * K), fill=MUTE)
    y = 200 * K; x0 = (W - (cols * cell + (cols - 1) * gap)) // 2
    for k, (shot, t1, t2) in enumerate(row):
        x = x0 + k * (cell + gap); paste(im, shot, x, y, cell); w = cell + gap - 8 * K
        ctext(d, x + cell / 2, y + cell + 4 * K, t1, f(32 * K, True), INK, w)
        ctext(d, x + cell / 2, y + cell + 48 * K, t2, f(25 * K), MUTE, w)
    y += cell + 110 * K
    if legend:
        x = 80 * K; y += 20 * K; fo = f(27 * K)
        for col, txt in legend: x = swatch(d, x, y, col, txt, fo)
    d.text((W - 80 * K - d.textlength(MARK, font=f(24 * K)), Hh - 56 * K), MARK, font=f(24 * K), fill=MUTE)
    im.save(os.path.join(OUT, name), optimize=True); print(name, im.size)


s = lambda sc, i: os.path.join(R, sc, f'p{i}.png')
VIO = (138, 92, 196); PEARL = (226, 222, 214); GLASS = (120, 128, 132)
KL = [(KIND[i], f'kind {i + 1}') for i in range(5)]
figure('resin-c1.png', 'C1', 'Twelve dodecahedron centre pyramids (violet) on the pentagons; on the right pulled out along their axes',
       [(s('c1', 0), 'C1', '20 hexagons, 60 triangles'), (s('c1', 1), 'pyramids pulled out', 'each along its own 5-fold axis')],
       [(PEARL, 'hexagon faces'), (VIO, 'pyramids')], cell=640)
figure('resin-cell.png', 'One cell: C1 in its mould with 80 resin pieces',
       'bcc lattice at its smallest scale s0; each piece sits on one face of C1 (central division) · left: pulled apart from the centre, mould see-through and enlarged with the pull',
       [(s('cell', 0), 'pulled apart', '80 pieces, 5 kinds'), (s('cell', 1), 'together', 'the mould filled')],
       KL + [(VIO, 'C1 pyramids'), (GLASS, 'mould')], cell=720)
figure('resin-tiling.png', 'Cells together fill space',
       'Six cells of the bcc lattice face to face; the front cell shows C1 inside its see-through mould, the others their resin',
       [(s('tiling', 0), 'six cells', 'bcc translates at s0')], KL + [(VIO, 'C1 pyramids')], cell=900)
SUB = ['on a hexagon · 8 per cell', 'on a hexagon · 12 per cell', 'on a triangle · 24 per cell', 'on a triangle · 24 per cell',
       'on a triangle · 12 per cell']
figure('resin-kinds.png', 'Kinds 1–5', 'One piece of each kind, standing on its face of C1 (outer side up), same scale · colours are labels only',
       [(s('kinds', i), f'kind {i + 1}', SUB[i]) for i in range(5)], [], cell=420, gap=30)
