# DICTO · dictospheres.com — compose the resin-solution renders from the shots of scenes.py (renders/<scene>/p<i>.png), in the
# house look of paper #115's fig_compose.py: dark warm ground, bold title, grey subtitle, a line under each panel, swatches, the
# DICTO mark. Kind colours are labels only; violet is the dodecahedron colour (the Fullerene Star's pyramids are dodecahedron centre pyramids).
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
    if txt == 'Y vertex':
        d.ellipse((x + 17 * K, y + 6 * K, x + 37 * K, y + 26 * K), fill=col, outline=(90, 80, 66), width=2 * K)
    else: d.rounded_rectangle((x, y + 6 * K, x + 54 * K, y + 26 * K), radius=5 * K, fill=col)
    d.text((x + 66 * K, y), txt, font=fo, fill=INK); return x + 66 * K + d.textlength(txt, font=fo) + 44 * K


def figure(name, title, sub, row, legend, cell=520, gap=40):
    rows = row if isinstance(row[0], list) else [row]
    cols = max(len(r) for r in rows); cell *= K; gap *= K
    W = max(cols * cell + (cols - 1) * gap + 160 * K, 1400 * K)
    if legend:                                      # widen so the swatch row fits
        dd = ImageDraw.Draw(Image.new('RGB', (10, 10))); fo = f(27 * K)
        W = max(W, int(160 * K + sum(110 * K + dd.textlength(txt, font=fo) for _, txt in legend)))
    Hh = 200 * K + len(rows) * (cell + 110 * K) + (80 * K if legend else 0) + 80 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    d.text((80 * K, 46 * K), title, font=fit(d, title, f(56 * K, True), W - 160 * K), fill=INK)
    d.text((80 * K, 122 * K), sub, font=fit(d, sub, f(28 * K), W - 160 * K), fill=MUTE)
    y = 200 * K
    for r in rows:
        x0 = (W - (len(r) * cell + (len(r) - 1) * gap)) // 2
        for k, (shot, t1, t2) in enumerate(r):
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
figure('resin-c1.png', 'Fullerene Star', 'Twelve dodecahedron centre pyramids (violet) on the pentagons of the core; on the right pulled out along their axes',
       [(s('c1', 0), 'Fullerene Star', '20 hexagons, 60 triangles'), (s('c1', 1), 'pyramids pulled out', 'each along its own 5-fold axis')],
       [(PEARL, 'hexagon faces'), (VIO, 'pyramids')], cell=640)
figure('resin-cell.png', 'The Fullerene-Amber Cell: the Fullerene Star in its mould with 80 resin pieces',
       'bcc lattice at its smallest scale s0; each piece sits on one face of the Fullerene Star (central division) · left: pulled apart from the centre, mould see-through and enlarged with the pull',
       [(s('cell', 0), 'pulled apart', '80 pieces, 5 kinds'), (s('cell', 1), 'together', 'the mould filled')],
       KL + [(VIO, 'pyramids'), (GLASS, 'mould')], cell=720)
figure('resin-tiling.png', 'Fullerene-Amber Cells together fill space',
       'Six cells of the bcc lattice face to face; the front cell shows the Fullerene Star inside its see-through mould, the others their resin',
       [(s('tiling', 0), 'six cells', 'bcc translates at s0')], KL + [(VIO, 'pyramids')], cell=900)
SUB = ['on a hexagon · 8 per cell', 'on a hexagon · 12 per cell', 'on a triangle · 24 per cell', 'on a triangle · 24 per cell',
       'on a triangle · 12 per cell']
figure('resin-kinds.png', 'Kinds 1–5', 'One piece of each kind, standing on its face of the Fullerene Star (outer side up), same scale · colours are labels only',
       [(s('kinds', i), f'kind {i + 1}', SUB[i]) for i in range(5)], [], cell=420, gap=30)


# ---- scutoid divisions, bcc mould at 6/5 s0 (scenes2.py) ----
def sh(c, k): return tuple(int(round(x * (1 + k) if k < 0 else x + (255 - x) * k)) for x in c)
FS = 'Fullerene Star'
figure('scutoid-combi-cell.png', 'One Fullerene-Amber Cell cut by the combi method: 80 scutoids',
       f'bcc mould at 6/5 s0, centroid seeds · every piece has a Y vertex · pulled apart from the centre, mould see-through and enlarged with the pull',
       [(s('combi_cell', 0), 'pulled apart', '80 pieces, 5 kinds, 30 Y vertices')], KL + [(VIO, 'pyramids'), (GLASS, 'mould')], cell=900)
NB = ['6 → 3 neighbours · 8 per cell', '6 → 3 neighbours · 12 per cell', '3 → 5 neighbours · 24 per cell', '3 → 5 neighbours · 24 per cell',
      '3 → 5 neighbours · 12 per cell']
figure('scutoid-combi-kinds.png', 'Combi method: kinds 1–5',
       f'One piece of each kind, standing on its face of the {FS}, same scale; top row from above, bottom row from below · dark: {FS} side · light: mould side · white dots: Y vertices',
       [[(s('combi_kinds', i), f'kind {i + 1}', NB[i]) for i in range(5)],
        [(s('combi_kinds', 5 + i), f'kind {i + 1}', 'the same piece from below') for i in range(5)]],
       [(sh(KIND[1], -0.45), f'{FS} side'), (KIND[1], 'walls'), (sh(KIND[1], 0.5), 'mould side'), ((255, 255, 255), 'Y vertex')], cell=420, gap=30)
figure('scutoid-skeleton-kinds.png', 'Exact straight skeleton: the two scutoid kinds',
       f'bcc mould at 6/5 s0, exact in Q(√5, √3) · 12 of kind 2 and 24 of kind 3 per cell · dark: {FS} side · light: mould side · white dot: the Y vertex',
       [(s('skeleton', 0), 'kind 2', '6 → 5 neighbours · from above'), (s('skeleton', 1), 'kind 2', 'from below'),
        (s('skeleton', 2), 'kind 3', '3 → 4 neighbours · from above'), (s('skeleton', 3), 'kind 3', 'from below')],
       [(sh(KIND[1], -0.45), f'{FS} side'), (sh(KIND[1], 0.5), 'mould side'), ((255, 255, 255), 'Y vertex')], cell=560, gap=30)
figure('scutoid-skeleton-hexagons.png', f'The 12 hexagon scutoids round the {FS}',
       'Exact straight skeleton, bcc mould at 6/5 s0 · kind 2 on the 12 hexagons of one orbit; the other 68 pieces left out · white dots: Y vertices',
       [(s('skeleton', 4), 'kind 2 × 12', f'on the {FS}')], [(KIND[1], 'kind 2'), (VIO, 'pyramids'), ((255, 255, 255), 'Y vertex')], cell=900)

# ---- Rollerball (scenes3.py) ----
BLUE = (58, 112, 205); C2N = 'Rollerball'
figure('c2.png', C2N, 'Truncated dodecahedron with a regular icosahedron centre pyramid (blue) on each of its 20 triangles (side edges = the icosahedron circumradius) · right: pyramids pulled out along their 3-fold axes',
       [(s('c2', 0), C2N, '12 decagons, 60 triangles'), (s('c2', 1), 'pyramids pulled out', 'each along its own 3-fold axis')],
       [(PEARL, 'decagon faces'), (BLUE, 'pyramids')], cell=640)
figure('c2-cell.png', 'Rollerball-Amber Cell: the Rollerball in its tightest mould',
       'fcc lattice, rhombic dodecahedron mould at s = 5 + 2√5; each piece sits on one face (central division) · 72 pieces, 4 kinds; colours are labels only',
       [(s('c2cell', 0), 'together', 'the mould filled'), (s('c2cell', 1), 'pulled apart', 'mould see-through, enlarged with the pull')],
       [(KIND[i], f'kind {i + 1}') for i in range(4)] + [(BLUE, 'pyramids'), (GLASS, 'mould')], cell=720)

# ---- Fullerene-Amber Cell completed with scutoids (scenes4.py) ----
figure('fullerene-amber-cell-scutoids.png', 'Fullerene-Amber Cell: 80 scutoids',
       "DICTO's combined method, bcc mould at 6/5 s0 · every piece is a scutoid (5 kinds, 30 Y vertices) · exploded: each piece moved out by 1.7 × its distance from the centre",
       [(s('amber', 0), 'complete', 'the mould filled · outline of the mould'), (s('amber', 1), 'exploded', 'all 80 pieces round the Fullerene Star'),
        (s('amber', 2), 'exploded, cutaway', 'the 25 pieces facing the viewer left out')],
       KL + [(VIO, 'pyramids'), (PEARL, 'Fullerene Star'), ((255, 255, 255), 'Y vertex')], cell=720)
