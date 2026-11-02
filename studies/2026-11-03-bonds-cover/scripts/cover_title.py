# DICTONIC Bonds cover title panel (2026-11-03), copied from the Star Cores one (DICTO 10-31, after the Golden Cycle and HexOct panels,
# DICTO 10-29: "bigger text on the front ... same style letters but no LED breaks"): DSEG14 Classic letters with the gaps between
# segments closed, black outline, soft glow, on the square's dark ground, joined below the square. Title gold, subtitle teal, DICTO red,
# as Star Cores; capitals, with larger initial capitals. Not part of a series: no series line. Each line is shrunk if needed to fit
# 0.92 of the width (the subtitle is longer than Star Cores').
import os, numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
GROUND = (20, 15, 11); GOLD = (217, 165, 33); VIOLET = (180, 138, 224); WHITE = (255, 255, 255); RED = (205, 62, 40); TEAL = (72, 206, 188)
sq = Image.open(os.environ.get('SQUARE', '../bonds-square.png')).convert('RGB'); N = sq.width
def glyph(ch, size, col):
    """One closed LED letter: (rgb, alpha) cropped to its ink, plus padding for glow."""
    f = ImageFont.truetype('DSEG14Classic-Regular.ttf', size); pad = size // 2; w, h = size + 2 * pad, int(size * 1.4) + 2 * pad
    m = Image.new('L', (w, h), 0)
    if ch == '*':   # a diamond (DICTO: a mark either side of DICTO, between title and author), centred on the letter height
        t = Image.new('L', (w, h), 0); ImageDraw.Draw(t).text((pad, pad), 'I', font=f, fill=255); iy = np.where(np.array(t) > 128)[0]
        c, r_ = (pad + size * 0.3, (iy.min() + iy.max()) / 2), size * 0.2
        ImageDraw.Draw(m).polygon([(c[0], c[1] - r_), (c[0] + r_, c[1]), (c[0], c[1] + r_), (c[0] - r_, c[1])], fill=255)
    else:
        ImageDraw.Draw(m).text((pad, pad), ch, font=f, fill=255)
    a = np.array(m) > 128; r = max(2, int(size * (0.1 if ch == 'X' else 0.05))); yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    a = ndimage.binary_closing(np.pad(a, r + 2), structure=xx ** 2 + yy ** 2 <= r * r)[r + 2:-(r + 2), r + 2:-(r + 2)]
    a = ndimage.gaussian_filter(a.astype(float), 0.8)
    e = max(2, size // 28); rim = ndimage.grey_dilation(a, size=(2 * e + 1, 2 * e + 1)); glow = ndimage.gaussian_filter(a, size * 0.06)
    glow /= max(glow.max(), 1e-6); col = np.array(col, float)
    rgb = np.where((rim - a)[..., None] > 0.3, np.array([8, 6, 4.]), col)
    al = np.clip(np.maximum.reduce([a, rim, 0.45 * glow]), 0, 1)
    ys, xs = np.where(a > 0.5); y1 = ys.max()
    if ch == '*': y1 = iy.max()   # sit on the letters' baseline, so the diamond stays centred
    return rgb, al, (ys.min(), y1, xs.min(), xs.max())
def word(text, size, colour_of, big=(), k=1.35):
    """Capitals throughout; letters at the positions in big are larger (initial caps, DICTO 10-29); bottoms on one line."""
    gs = [None if ch == ' ' else glyph(ch, int(size * (k if i in big else 1)), colour_of(ch)) for i, ch in enumerate(text)]
    gap = int(size * 0.18); space = int(size * 0.55)
    widths = [space if g is None else g[2][3] - g[2][2] + 1 for g in gs]
    W_ = sum(widths) + gap * (len(text) - 1) + size; Hh = int(size * k * 1.2) + size
    rgb = np.zeros((Hh, W_, 3)); alpha = np.zeros((Hh, W_)); base = Hh - size // 2; x = size // 2
    for g, wd in zip(gs, widths):
        if g is not None:
            gr, ga, (y0, y1, x0, x1) = g; oy, ox = base - y1, x - x0
            ys, xs = slice(max(0, oy), min(Hh, oy + ga.shape[0])), slice(max(0, ox), min(W_, ox + ga.shape[1]))
            sub_a = ga[ys.start - oy:ys.stop - oy, xs.start - ox:xs.stop - ox]; sub_r = gr[ys.start - oy:ys.stop - oy, xs.start - ox:xs.stop - ox]
            rgb[ys, xs] = rgb[ys, xs] * (1 - sub_a[..., None]) + sub_r * sub_a[..., None]; alpha[ys, xs] = np.maximum(alpha[ys, xs], sub_a)
        x += wd + gap
    ys, xs = np.where(alpha > 0.02); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1]
def paste(canvas, img, cx, y):
    rgb, a = img; h, w = a.shape; x = int(cx - w / 2)
    c = canvas[y:y + h, x:x + w]; canvas[y:y + h, x:x + w] = c * (1 - a[..., None]) + rgb * a[..., None]; return y + h
def fit(text, size, col, big):
    w = word(text, size, lambda ch: col, big=big)
    while w[1].shape[1] > 0.92 * N: size = int(size * 0.97); w = word(text, size, lambda ch: col, big=big)
    print(text, 'size', round(size / N, 4)); return w
big = fit('DICTONIC BONDS', int(N * 0.075), GOLD, tuple(range(14)))   # DICTO 11-03: full capitals, every letter at the large capital size   # lines gold, teal, red (as Star Cores; DICTO red, as the other books)
sub = fit('FROM THE OCTET TO THE RULE OF HALVES', int(N * 0.040), TEAL, (0, 9, 22, 30))   # initials of From, Octet, Rule, Halves
by = word('* DICTO *', int(N * 0.042), lambda ch: RED, big=(0, 2, 3, 4, 5, 6, 8))   # every letter of DICTO is an initial (DICTO)
H = big[1].shape[0] + sub[1].shape[0] + by[1].shape[0] + int(N * 0.16)
panel = np.ones((H, N, 3)) * np.array(GROUND, float)
y = paste(panel, big, N / 2, int(N * 0.02)); y = paste(panel, sub, N / 2, y + int(N * 0.05)); paste(panel, by, N / 2, y + int(N * 0.035))
out = Image.new('RGB', (N, N + H), GROUND); out.paste(sq, (0, 0)); out.paste(Image.fromarray(np.clip(panel, 0, 255).astype(np.uint8)), (0, N))
out.save(os.environ.get('OUT', '../bonds-cover-front.png')); print('ok', out.size)
# the ◆ DICTO ◆ mark alone (transparent), for the back of the KDP cover (DICTO 10-29)
mk = word('* DICTO *', int(N * 0.06), lambda ch: RED, big=(0, 2, 3, 4, 5, 6, 8))   # red on the back too
Image.fromarray(np.dstack([np.clip(mk[0], 0, 255), mk[1] * 255]).astype(np.uint8), 'RGBA').save('../dicto-mark.png')
