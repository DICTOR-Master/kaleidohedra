# DICTO · dictospheres.com — compose the rendered figures of the paper on Grünbaum's zone question at k = 10 from the shots
# of fig_scenes.py (renders/<fig>/p<i>.png), in the house look of paper #43 as carried by the Dehn Canon paper's
# fig_compose.py: dark warm ground, bold title and grey subtitle inside the image, bold name and grey second line under each
# panel, a legend of colour swatches, the DICTO mark. Colours are labels only (captions say so).
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
figure('fig-dimples.png', 'Four flat rhombohedra out of the triacontahedron',
       'Each solid is the rhombic triacontahedron T less four oblate golden rhombohedra, drawn see-through and pulled out of their dimples · the four dimples lie on one inscribed cube',
       [[(s('tri', 0), 'the triacontahedron T', '20 rhombohedra · zones of 10'),
         (s('tri', 1), 'GET A', 'a square face of the cube'),
         (s('tri', 2), 'GET B', 'a cube corner and its three neighbours'),
         (s('tri', 3), 'indented triacontahedron', 'Hall, 2016: alternate cube corners')]],
       [((200, 149, 42), 'GET A', None), ((158, 164, 173), 'GET B', None), ((154, 143, 126), 'indented triacontahedron (Hall; Inchbald)', None),
        ((60, 55, 48), 'removed oblate cell', (239, 233, 220))])
figure('fig-apart.png', 'GET A and GET B: sixteen golden rhombohedra each',
       'Seen from the back (the side opposite to Figure 1), whole and pulled apart from the centre · 10 prolate and 6 oblate rhombohedra, of 16 of the 20 types',
       [[(s('apart', 0), 'GET A', 'from the back'), (s('apart', 1), 'GET A pulled apart', '10 prolate + 6 oblate'),
         (s('apart', 2), 'GET B', 'from the back'), (s('apart', 3), 'GET B pulled apart', '10 prolate + 6 oblate')]],
       [((200, 149, 42), 'GET A, prolate', None), ((236, 217, 160), 'GET A, oblate', None), ((158, 164, 173), 'GET B, prolate', None), ((217, 220, 225), 'GET B, oblate', None)])
AXN = ['(1, φ, 0)', '(−1, φ, 0)', '(0, 1, φ)', '(0, −1, φ)', '(φ, 0, 1)', '(−φ, 0, 1)']
figure('fig-zones.png', 'Every zone has exactly ten faces',
       'For each of the six 5-fold axes (light line), the faces with a side parallel to it form one closed belt of 10 faces (coloured); the other 20 faces see-through',
       [[(s('zones', 6 * i + d), f'zone {d}', f'axis {AXN[d]}') for d in range(6)] for i in (0, 1)],
       [((200, 149, 42), 'GET A, the zone’s 10 faces', None), ((158, 164, 173), 'GET B, the zone’s 10 faces', None), ((60, 55, 48), 'other faces, see-through', (109, 100, 85))],
       cell=330, gap=30, rowhead=['GET A', 'GET B'], fs=0.95)
figure('fig-tiling.png', 'Translates on one lattice fill space',
       'Eight lattice translates (a 2 × 2 × 2 block on three face-neighbour vectors that form a basis of the lattice), together and pulled apart · tones mark the tiles only',
       [[(s('tiling', 0), 'GET A, eight translates', 'face to face'), (s('tiling', 1), 'pulled apart', 'the same eight tiles'),
         (s('tiling', 2), 'GET B, eight translates', 'the same lattice'), (s('tiling', 3), 'pulled apart', 'the same eight tiles')]], [])
