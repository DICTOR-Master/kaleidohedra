"""Cover of The Permutohedron Paradigm: the square (cover_svg.py + cover_shot.mjs) and a title panel in the house style of DICTO's book
covers (studies/2026-10-31-star-cores-cover/scripts/cover_title_series.py: closed LED letters with a dark rim, gold title, red DICTO
between diamonds, on the dark ground). Usage: python cover_title.py square.png out.png"""
import sys, os, numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FONT = os.path.join(HERE, 'DSEG14Classic-Regular.ttf')
GROUND = (20, 15, 11); GOLD = (217, 165, 33); RED = (205, 62, 40); WHITE = (255, 255, 255)
sq = Image.open(sys.argv[1]).convert('RGB'); N = sq.width
def glyph(ch, size, col):
    f = ImageFont.truetype(FONT, size); pad = size // 2; w, h = size + 2 * pad, int(size * 1.4) + 2 * pad
    m = Image.new('L', (w, h), 0)
    if ch == '*':
        t = Image.new('L', (w, h), 0); ImageDraw.Draw(t).text((pad, pad), 'I', font=f, fill=255); iy = np.where(np.array(t) > 128)[0]
        c, r_ = (pad + size * 0.3, (iy.min() + iy.max()) / 2), size * 0.2
        ImageDraw.Draw(m).polygon([(c[0], c[1] - r_), (c[0] + r_, c[1]), (c[0], c[1] + r_), (c[0] - r_, c[1])], fill=255)
    else: ImageDraw.Draw(m).text((pad, pad), ch, font=f, fill=255)
    a = np.array(m) > 128; r = max(2, int(size * 0.05)); yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    a = ndimage.binary_closing(np.pad(a, r + 2), structure=xx ** 2 + yy ** 2 <= r * r)[r + 2:-(r + 2), r + 2:-(r + 2)]
    a = ndimage.gaussian_filter(a.astype(float), 0.8)
    e = max(2, size // 28); rim = ndimage.grey_dilation(a, size=(2 * e + 1, 2 * e + 1)); glow = ndimage.gaussian_filter(a, size * 0.06)
    glow /= max(glow.max(), 1e-6); col = np.array(col, float)
    rgb = np.where((rim - a)[..., None] > 0.3, np.array([8, 6, 4.]), col)
    al = np.clip(np.maximum.reduce([a, rim, 0.45 * glow]), 0, 1)
    ys, xs = np.where(a > 0.5); y1 = iy.max() if ch == '*' else ys.max()
    return rgb, al, (ys.min(), y1, xs.min(), xs.max())
def word(text, size, col, big=(), k=1.35):
    gs = [None if ch == ' ' else glyph(ch, int(size * (k if i in big else 1)), col) for i, ch in enumerate(text)]
    gap = int(size * 0.18); space = int(size * 0.55)
    widths = [space if g is None else g[2][3] - g[2][2] + 1 for g in gs]
    W_ = sum(widths) + gap * (len(text) - 1) + size; Hh = int(size * k * 1.2) + size
    rgb = np.zeros((Hh, W_, 3)); alpha = np.zeros((Hh, W_)); base = Hh - size // 2; x = size // 2
    for g, wd in zip(gs, widths):
        if g is not None:
            gr, ga, (y0, y1, x0, x1) = g; oy, ox = base - y1, x - x0
            ys, xs = slice(max(0, oy), min(Hh, oy + ga.shape[0])), slice(max(0, ox), min(W_, ox + ga.shape[1]))
            sa = ga[ys.start - oy:ys.stop - oy, xs.start - ox:xs.stop - ox]; sr = gr[ys.start - oy:ys.stop - oy, xs.start - ox:xs.stop - ox]
            rgb[ys, xs] = rgb[ys, xs] * (1 - sa[..., None]) + sr * sa[..., None]; alpha[ys, xs] = np.maximum(alpha[ys, xs], sa)
        x += wd + gap
    ys, xs = np.where(alpha > 0.02); return rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1], alpha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def paste(canvas, img, cx, y):
    rgb, a = img; h, w = a.shape; x = int(cx - w / 2)
    c = canvas[y:y + h, x:x + w]; canvas[y:y + h, x:x + w] = c * (1 - a[..., None]) + rgb * a[..., None]; return y + h
t1 = word('THE PERMUTOHEDRON', int(N * 0.05), GOLD, big=(0, 4)); t2 = word('PARADIGM', int(N * 0.05), GOLD, big=(0,))
by = word('* DICTO *', int(N * 0.042), RED, big=(0, 2, 3, 4, 5, 6, 8))
H = t1[1].shape[0] + t2[1].shape[0] + by[1].shape[0] + int(N * 0.17)
panel = np.ones((H, N, 3)) * np.array(GROUND, float)
y = paste(panel, t1, N / 2, int(N * 0.035)); y = paste(panel, t2, N / 2, y + int(N * 0.025)); paste(panel, by, N / 2, y + int(N * 0.045))
out = Image.new('RGB', (N, N + H), GROUND); out.paste(sq, (0, 0)); out.paste(Image.fromarray(np.clip(panel, 0, 255).astype(np.uint8)), (0, N))
out.save(sys.argv[2]); print('wrote', sys.argv[2], out.size)
