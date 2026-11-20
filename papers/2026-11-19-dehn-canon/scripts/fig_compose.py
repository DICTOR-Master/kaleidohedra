# DICTO · dictospheres.com — compose the rendered figures of the Dehn Canon paper from the shots of fig_scenes.py
# (renders/<fig>/p<i>.png) in the house look of paper #43 (studies 2026-10-21-og-turned-out new_solids_compose.py: dark warm
# ground, bold title and grey subtitle inside the image, bold name and grey second line under each solid, the DICTO mark).
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, '..', 'figures')
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', int(s))
INK, MUTE, BG, RULE = (238, 230, 214), (176, 165, 148), (20, 15, 11), (92, 82, 68)
K = 2; PX = 1600
MARK = 'DICTO · dictospheres.com'
LOG = []


def fit(d, txt, fo, w):
    while d.textlength(txt, font=fo) > w and fo.size > 14 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
    return fo


def ctext(d, x, y, txt, fo, col, w):
    fo = fit(d, txt, fo, w); d.text((x - d.textlength(txt, font=fo) / 2, y), txt, font=fo, fill=col); return fo


def paste(im, path, x, y, cell):
    p = Image.open(path).convert('RGBA'); bb = p.getbbox()
    assert bb and bb[0] > 2 and bb[1] > 2 and bb[2] < PX - 2 and bb[3] < PX - 2, f'{path}: solid touches the shot edge {bb}'
    p = p.resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)


def head(d, W, title, sub):
    d.text((80 * K, 46 * K), title, font=f(60 * K, True), fill=INK); d.text((80 * K, 122 * K), sub, font=f(30 * K), fill=MUTE)


def mark(d, W, Hh):
    d.text((W - 80 * K - d.textlength(MARK, font=f(24 * K)), Hh - 56 * K), MARK, font=f(24 * K), fill=MUTE)


def save(im, name):
    im.save(os.path.join(OUT, name), optimize=True); LOG.append(f'{name} {im.size}'); print(name, im.size)


def swatch(d, x, y, col, txt, fo, outline=None):
    d.rounded_rectangle((x, y + 6 * K, x + 54 * K, y + 26 * K), radius=5 * K, fill=col, outline=outline, width=2 * K)
    d.text((x + 66 * K, y), txt, font=fo, fill=INK); return x + 66 * K + d.textlength(txt, font=fo) + 44 * K


# ---------- the canon gallery ----------
def canon():
    L = json.load(open(os.path.join(R, 'canon-labels.json'))); cols, cell, gap = 5, 380 * K, 36 * K
    zero = [i for i, l in enumerate(L) if l['zero']]; non = [i for i, l in enumerate(L) if not l['zero']]
    rowh = cell + 120 * K; bh = 90 * K
    rows = lambda n: (n + cols - 1) // cols
    W = cols * cell + (cols - 1) * gap + 160 * K; top = 200 * K
    Hh = top + 2 * bh + (rows(len(zero)) + rows(len(non))) * rowh + 40 * K + 90 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'The canon', 'Every solid of Table 1, each drawn to fill its frame · under each name its Dehn invariant, for the solid as written in Table 1')
    y = top
    for title, idx in [('Dehn invariant zero', zero), ('Dehn invariant nonzero', non)]:
        d.text((80 * K, y + 18 * K), title, font=f(44 * K, True), fill=INK)
        d.line((80 * K, y + 78 * K, W - 80 * K, y + 78 * K), fill=RULE, width=2 * K); y += bh
        for k, i in enumerate(idx):
            x = 80 * K + (k % cols) * (cell + gap); yy = y + (k // cols) * rowh
            paste(im, f'{R}/canon/p{i}.png', x, yy, cell)
            ctext(d, x + cell / 2, yy + cell + 6 * K, L[i]['title'], f(32 * K, True), INK, cell + gap - 8 * K)
            ctext(d, x + cell / 2, yy + cell + 50 * K, L[i]['sub'], f(25 * K), MUTE, cell + gap - 8 * K)
        y += rows(len(idx)) * rowh + 20 * K
    mark(d, W, Hh); save(im, 'fig-canon-solids.png')


# ---------- Dehn's pair and Hilbert's pair ----------
def pairs():
    L = json.load(open(os.path.join(R, 'pairs-labels.json'))); cell, gap, mid = 560 * K, 30 * K, 110 * K
    W = 4 * cell + 2 * gap + mid + 160 * K; top = 280 * K; Hh = top + cell + 330 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, "Dehn's pair and Hilbert's pair", 'Each edge in the colour of its dihedral angle · left: Theorem 6, right: Theorem 1 (h) and Theorem 6′')
    xs = [80 * K, 80 * K + cell + gap, 80 * K + 2 * cell + gap + mid, 80 * K + 3 * cell + 2 * gap + mid]
    for (a, b), t in [((0, 1), "Dehn's pair: the same volume"), ((2, 3), "Hilbert's pair: the same base, the same height")]:
        x0, x1 = xs[a], xs[b] + cell; d.text(((x0 + x1) / 2 - d.textlength(t, font=f(36 * K, True)) / 2, 196 * K), t, font=f(36 * K, True), fill=INK)
        d.line((x0, 252 * K, x1, 252 * K), fill=RULE, width=2 * K)
    names = [('regular tetrahedron', '6 edges at arccos(1/3) ≈ 70.53° · invariant ≠ 0'), ('cube', '12 edges at π/2 · invariant 0'),
             ('tetrahedron ABCD', '3√2 ⊗ arccos(1/√3) ≠ 0'), ('tetrahedron ABCD′', 'invariant 0')]
    for i, x in enumerate(xs):
        paste(im, f'{R}/pairs/p{i}.png', x, top, cell)
        ctext(d, x + cell / 2, top + cell + 4 * K, names[i][0], f(34 * K, True), INK, cell + gap)
        ctext(d, x + cell / 2, top + cell + 50 * K, names[i][1], f(26 * K), MUTE, cell + gap)
    s = cell / PX
    for i, lab in enumerate(L):
        x0 = xs[2 + i]
        for nm, (px, py) in lab['pts']:
            fo = f(34 * K, True); w = d.textlength(nm, font=fo)
            d.text((x0 + px * s - w / 2, top + py * s - 21 * K), nm, font=fo, fill=INK)
        px, py = lab['height']; t = 'height 1'; fo = f(26 * K, True)
        d.text((x0 + px * s - d.textlength(t, font=fo) / 2, top + py * s - 16 * K), t, font=fo, fill=(243, 226, 176))
    t = 'volume 1/6 each · neither scissors congruent nor equicomplementable'
    ctext(d, (xs[2] + xs[3] + cell) / 2, top + cell + 100 * K, t, f(26 * K, True), INK, 2 * cell + gap)
    t = 'tetrahedron × ∛3 and cube: volume 8 each · not scissors congruent'
    ctext(d, (xs[0] + xs[1] + cell) / 2, top + cell + 100 * K, t, f(26 * K, True), INK, 2 * cell + gap)
    fo = f(26 * K); x = 80 * K; y = Hh - 130 * K
    x = swatch(d, x, y, (242, 234, 214), 'angle not a rational multiple of π (arccos(1/3), arccos(1/√3))', fo)
    x = swatch(d, x, y, (74, 95, 126), 'angle a rational multiple of π (π/2, π/3, π/4)', fo, outline=(239, 230, 210))
    swatch(d, x, y, (243, 226, 176), 'the base ABC, see-through', fo)
    mark(d, W, Hh); save(im, 'fig-pairs.png')


# ---------- the cube ∩ octahedron line ----------
def line():
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    L = json.load(open(os.path.join(R, 'line-labels.json'))); n = len(L); cell, gap = 330 * K, 26 * K
    W = n * cell + (n - 1) * gap + 160 * K; top = 200 * K; ph = 340 * K; Hh = top + cell + 130 * K + ph + 110 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'The cube ∩ octahedron line', '{|xᵢ| ≤ 1, |x| + |y| + |z| ≤ t} at true relative size · Dehn invariant 12√2(2t − 3) ⊗ arccos(1/3), zero only at t = 3/2')
    NAME = {'1': 'octahedron', '3/2': 'truncated octahedron', '8783/5000': 'fair 14-face die'}
    TT = {'1': '1', '9/8': '9/8', '5/4': '5/4', '11/8': '11/8', '3/2': '3/2', '13/8': '13/8', '8783/5000': '1.7566…', '15/8': '15/8'}
    for i, l in enumerate(L):
        x = 80 * K + i * (cell + gap)
        if l['t'] in ('3/2', '8783/5000'):
            d.rounded_rectangle((x - 10 * K, top - 12 * K, x + cell + 10 * K, top + cell + 104 * K), radius=18 * K, outline=RULE, width=3 * K)
        paste(im, f'{R}/line/p{i}.png', x, top, cell)
        c = l['coef']; cs = '0' if c == 0 else (f'{c:+.0f}√2' if abs(c - round(c)) < 1e-9 else f'≈ {c:+.2f}√2').replace('-', '−')
        ctext(d, x + cell / 2, top + cell + 4 * K, 't = ' + TT[l['t']], f(30 * K, True), INK, cell + gap - 6 * K)
        ctext(d, x + cell / 2, top + cell + 46 * K, (NAME[l['t']] + ' · ' if l['t'] in NAME else '') + cs, f(22 * K), MUTE, cell + gap - 6 * K)
    # the small graph: the coefficient 12√2(2t − 3), in units of √2, against t
    fig = plt.figure(figsize=((W - 160 * K) / 200, ph / 200), dpi=200); fig.patch.set_alpha(0)
    ax = fig.add_axes([0.08, 0.3, 0.9, 0.64]); ax.set_facecolor('none')
    t = np.linspace(1, 2, 200); mc = '#b0a594'
    ax.axhline(0, color='#5c5244', lw=2); ax.plot(t, 12 * (2 * t - 3), color='#eee6d6', lw=4)
    tv = [1, 9 / 8, 5 / 4, 11 / 8, 3 / 2, 13 / 8, 1.7565821359, 15 / 8]
    for v in tv: ax.plot(v, 12 * (2 * v - 3), 'o', ms=14, color='#e8c852' if v == 1 else '#cdc3b0', mec='#140f0b')
    ax.plot(2, 12, 'o', ms=14, mfc='#140f0b', mec='#cdc3b0')
    ax.annotate('t = 3/2: 0', (1.5, 0), (1.42, 6.5), color='#eee6d6', fontsize=24, ha='center', arrowprops=dict(arrowstyle='-', color=mc))
    ax.annotate('fair 14-face die', (1.7566, 12 * (2 * 1.7566 - 3)), (1.80, -6), color='#eee6d6', fontsize=24, ha='left', arrowprops=dict(arrowstyle='-', color=mc))
    ax.set_xlim(0.97, 2.03); ax.set_ylim(-14, 14); ax.set_yticks([-12, 0, 12]); ax.set_xticks([1, 1.25, 1.5, 1.75, 2])
    ax.set_xticklabels(['1', '5/4', '3/2', '7/4', '2']); ax.set_yticklabels(['−12√2', '0', '12√2'])
    ax.tick_params(colors=mc, labelsize=22, width=2, length=8)
    for s_ in ax.spines.values(): s_.set_color('#5c5244'); s_.set_linewidth(2)
    ax.set_xlabel('t', color=mc, fontsize=24); ax.set_ylabel('coefficient', color=mc, fontsize=22)
    tmp = os.path.join(R, 'line-graph.png'); fig.savefig(tmp, transparent=True); plt.close(fig)
    g = Image.open(tmp).convert('RGBA'); im.paste(g, (80 * K, top + cell + 120 * K), g)
    mark(d, W, Hh); save(im, 'fig-line.png')


# ---------- CLEO, AXE, FUJI ----------
ACOL = {'α': '#1f1f1f', 'β': '#9a6a2e', 'γ': '#5b6f8a', 'ε': '#a3a3a3', 'π − ε': '#a3a3a3'}
def words():
    L = json.load(open(os.path.join(R, 'words-labels.json'))); cell, gap, cg = 470 * K, 10 * K, 90 * K
    W = 6 * cell + 3 * gap + 2 * cg + 160 * K; top = 330 * K; Hh = top + cell + 210 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'CLEO, AXE and FUJI, every edge by its angle', 'Each word from two opposite sides, so every edge shows · long edges length 1, short edges length g')
    INV = {'CLEO': '3 ⊗ α + 3g ⊗ β', 'AXE': '(1 + g) ⊗ α + 6 ⊗ β', 'FUJI': '(9 − 3g) ⊗ α + (12 − 3g) ⊗ β'}
    s = cell / PX
    for j, nm in enumerate(['CLEO', 'AXE', 'FUJI']):
        x0 = 80 * K + j * (2 * cell + gap + cg)
        ctext(d, x0 + cell + gap / 2, 190 * K, nm, f(40 * K, True), INK, 2 * cell)
        ctext(d, x0 + cell + gap / 2, 244 * K, INV[nm], f(30 * K), MUTE, 2 * cell)
        for k in range(2):
            x = x0 + k * (cell + gap); i = 2 * j + k; paste(im, f'{R}/words/p{i}.png', x, top, cell)
            ctext(d, x + cell / 2, top + cell + 8 * K, ['one side', 'the opposite side'][k], f(24 * K), MUTE, cell)
            for cl, (px, py) in L[i]['edges']:
                fo = f(26 * K, True); w = d.textlength(cl, font=fo); cx, cy = x + px * s, top + py * s
                col = ACOL[cl]; tc = (20, 15, 11) if cl in ('ε', 'π − ε') else (242, 234, 214)
                d.rounded_rectangle((cx - w / 2 - 8 * K, cy - 17 * K, cx + w / 2 + 8 * K, cy + 19 * K), radius=8 * K, fill=col, outline=(239, 230, 210), width=K)
                d.text((cx - w / 2, cy - 15 * K), cl, font=fo, fill=tc)
    fo = f(25 * K); x = 80 * K; y = Hh - 120 * K
    for col, txt in [('#1f1f1f', 'α = arccos(1/√5) ≈ 63.43°'), ('#9a6a2e', 'β ≈ 79.19°'), ('#5b6f8a', 'γ = arccos(√5/3) ≈ 41.81°'),
                     ('#a3a3a3', 'ε ≈ 37.38° and π − ε')]:
        x = swatch(d, x, y, col, txt, fo, outline=(239, 230, 210))
    mark(d, W, Hh); save(im, 'fig-words-3d.png')


# ---------- where CLEO, AXE and FUJI come from ----------
def pieces():
    cell, gap = 600 * K, 30 * K
    W = 4 * cell + 3 * gap + 160 * K; top = 220 * K; Hh = top + cell + 260 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'Where CLEO, AXE and FUJI come from', 'The 63-piece build of the icosahedron of edge φ², and the 20 CLEO inside its dodecahedron [11] · exact corners, put together and pulled apart')
    names = [('icosahedron of edge φ²', 'dodecahedron + 12 J11 + 30 AXE + 20 FUJI'), ('pulled apart', 'AXE in the grooves, FUJI in the corners'),
             ('inside the dodecahedron', 'small icosahedron (edge g) + 20 CLEO'), ('pulled apart', 'each CLEO from a face to a corner')]
    for i in range(4):
        x = 80 * K + i * (cell + gap); paste(im, f'{R}/pieces/p{i}.png', x, top, cell)
        ctext(d, x + cell / 2, top + cell + 4 * K, names[i][0], f(34 * K, True), INK, cell + gap)
        ctext(d, x + cell / 2, top + cell + 50 * K, names[i][1], f(26 * K), MUTE, cell + gap)
    fo = f(26 * K); x = 80 * K; y = Hh - 120 * K
    for col, txt, ol in [((138, 92, 196), 'dodecahedron', None), ((58, 112, 205), 'icosahedron', None), ((77, 208, 225), 'AXE', None),
                         ((199, 146, 234), 'CLEO and FUJI', None), ((60, 56, 48), 'J11, see-through', (207, 198, 180))]:
        x = swatch(d, x, y, col, txt, fo, outline=ol)
    mark(d, W, Hh); save(im, 'fig-pieces.png')


if __name__ == '__main__':
    which = sys.argv[1:] or ['canon', 'pairs', 'line', 'words', 'pieces']
    for w in which: globals()[w]()
    print('FINAL ok')
