# DICTO · dictospheres.com — compose Figures 1 and 3 of the paper on the Dehn–Hadwiger invariant in four dimensions from the
# shots of fig_scenes.py (renders/<fig>/p<i>.png), with the figure() of the Grünbaum k = 10 paper's fig_compose.py (house look
# of paper #43): dark warm ground, bold title and grey subtitle inside the image, bold name and grey second line under each
# panel, a legend of colour swatches, the DICTO mark.
import os
from PIL import Image, ImageDraw, ImageFont

H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, '..', 'figures')
os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', int(s))
INK, MUTE, BG, RULE = (238, 230, 214), (176, 165, 148), (20, 15, 11), (92, 82, 68)
K = 2; PX = 1600; MARK = 'DICTO · dictospheres.com'


def fit(d, txt, fo, w):
    while d.textlength(txt, font=fo) > w and fo.size > 14 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
    return fo


def ctext(d, x, y, txt, fo, col, w):
    fo = fit(d, txt, fo, w); d.text((x - d.textlength(txt, font=fo) / 2, y), txt, font=fo, fill=col)


def paste(im, path, x, y, cell):
    p = Image.open(path).convert('RGBA'); bb = p.getbbox()
    assert bb and bb[0] > 2 and bb[1] > 2 and bb[2] < PX - 2 and bb[3] < PX - 2, f'{path}: solid touches the shot edge {bb}'
    p = p.resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)


def swatch(d, x, y, col, txt, fo, outline=None):
    d.rounded_rectangle((x, y + 6 * K, x + 54 * K, y + 26 * K), radius=5 * K, fill=col, outline=outline, width=2 * K)
    d.text((x + 66 * K, y), txt, font=fo, fill=INK); return x + 66 * K + d.textlength(txt, font=fo) + 44 * K


def figure(name, title, sub, rows, legend, cell=420, gap=40, rowhead=None, fs=1.0):
    """rows: lists of (shot, name, second line); rowhead: optional bold heading above each row"""
    cols = max(len(r) for r in rows); cell *= K; gap *= K
    W = cols * cell + (cols - 1) * gap + 160 * K
    rowh = cell + int(110 * fs) * K + (70 * K if rowhead else 0)
    Hh = 200 * K + len(rows) * rowh + (80 * K if legend else 0) + 80 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    d.text((80 * K, 46 * K), title, font=fit(d, title, f(60 * K, True), W - 160 * K), fill=INK)
    d.text((80 * K, 122 * K), sub, font=fit(d, sub, f(30 * K), W - 160 * K), fill=MUTE)
    y = 200 * K
    for ri, r in enumerate(rows):
        if rowhead:
            d.text((80 * K, y + 6 * K), rowhead[ri], font=f(42 * K, True), fill=INK)
            d.line((80 * K, y + 60 * K, W - 80 * K, y + 60 * K), fill=RULE, width=2 * K); y += 70 * K
        x0 = 80 * K + (cols - len(r)) * (cell + gap) // 2
        for k, (shot, t1, t2) in enumerate(r):
            x = x0 + k * (cell + gap); paste(im, shot, x, y, cell); w = cell + gap - 8 * K
            ctext(d, x + cell / 2, y + cell + 4 * K, t1, f(32 * fs * K, True), INK, w)
            ctext(d, x + cell / 2, y + cell + (4 + 44 * fs) * K, t2, f(25 * fs * K), MUTE, w)
        y += cell + int(110 * fs) * K
    if legend:
        x = 80 * K; y += 20 * K; fo = f(27 * K)
        for col, txt, ol in legend: x = swatch(d, x, y, col, txt, fo, ol)
    d.text((W - 80 * K - d.textlength(MARK, font=f(24 * K)), Hh - 56 * K), MARK, font=f(24 * K), fill=MUTE)
    im.save(os.path.join(OUT, name), optimize=True); print(name, im.size)


s = lambda fig, i: os.path.join(R, fig, f'p{i}.png')
# six.html scenes in exact4d.ORDER: 0 120-cell, 1 600-cell, 2 tesseract, 3 5-cell, 4 16-cell, 5 24-cell
figure('fig-six.png', 'The six regular 4-polytopes and their Dehn–Hadwiger invariants',
       'Perspective projections from a point on the axis of one facet · every edge drawn, light near the eye, dark far · one facet solid in the colour of its solid',
       [[(s('six', 0), '120-cell', '120 dodecahedra · 144° = 4π/5'), (s('six', 2), 'tesseract', '8 cubes · 90° = π/2'),
         (s('six', 4), '16-cell', '16 tetrahedra · 120° = 2π/3'), (s('six', 5), '24-cell', '24 octahedra · 120° = 2π/3')],
        [(s('six', 1), '600-cell', '600 tetrahedra · 164.48° = 4π/3 − arccos ¼'), (s('six', 3), '5-cell', '5 tetrahedra · 75.52° = arccos ¼')]],
       [((138, 92, 196), 'dodecahedron', None), ((72, 142, 72), 'cube', None), ((205, 62, 40), 'tetrahedron', None), ((232, 200, 82), 'octahedron', None)],
       cell=400, rowhead=['Invariant zero: every dihedral angle a rational multiple of π', 'Invariant nonzero: the angle is not a rational multiple of π'])
figure('fig-caps.png', 'One 600-cell and 120 regular 5-cells: invariant zero',
       'The caps of one orbit of left multiplication · 120 caps of the same edge, one on each capped facet · colours are labels only',
       [[(s('caps', 0), 'at one corner', '4 of the 20 facets capped, using its 12 edges once'),
         (s('caps', 1), 'the whole solid', '600-cell + 120 caps, star-shaped, not convex'),
         (s('caps', 2), 'the 120 tips', 'a 600-cell of radius √2 round the 600-cell')]],
       [((210, 195, 160), '600-cell (edges)', None), ((154, 116, 72), 'capped facets', None), ((201, 154, 69), 'cap edges and tips', None), ((138, 155, 179), 'the tips’ 600-cell', None)],
       cell=460)
