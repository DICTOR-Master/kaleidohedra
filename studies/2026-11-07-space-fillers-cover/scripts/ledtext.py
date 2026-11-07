# LED title letters (hyphen/comma sit on the letter baseline, 11-07), copied from studies/2026-10-29-golden-cover/scripts/cover_title_series.py (series style)
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
def glyph(ch, size, col):
    """One closed LED letter: (rgb, alpha) cropped to its ink, plus padding for glow."""
    f = ImageFont.truetype('DSEG14Classic-Regular.ttf', size); pad = size // 2; w, h = size + 2 * pad, int(size * 1.4) + 2 * pad
    m = Image.new('L', (w, h), 0)
    t = Image.new('L', (w, h), 0); ImageDraw.Draw(t).text((pad, pad), 'I', font=f, fill=255); iy = np.where(np.array(t) > 128)[0]
    if ch == '*':   # a diamond (DICTO: a mark either side of DICTO, between title and author), centred on the letter height
        t = Image.new('L', (w, h), 0); ImageDraw.Draw(t).text((pad, pad), 'I', font=f, fill=255); iy = np.where(np.array(t) > 128)[0]
        c, r_ = (pad + size * 0.3, (iy.min() + iy.max()) / 2), size * 0.2
        ImageDraw.Draw(m).polygon([(c[0], c[1] - r_), (c[0] + r_, c[1]), (c[0], c[1] + r_), (c[0] - r_, c[1])], fill=255)
    elif ch == ',':   # the font's comma is a slanted segment that reads as a slash: a round dot with a short tail instead
        yb, x0, r_ = iy.max(), pad + size * 0.12, size * 0.075
        ImageDraw.Draw(m).ellipse([x0 - r_, yb - 2 * r_, x0 + r_, yb], fill=255)
        ImageDraw.Draw(m).polygon([(x0 + r_ * 0.95, yb - r_), (x0 - r_ * 0.2, yb - r_ * 0.5), (x0 - r_ * 1.3, yb + r_ * 2.0)], fill=255)
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
    if ch in '*-,': y1 = iy.max()   # sit on the letters' baseline, so the diamond stays centred
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
