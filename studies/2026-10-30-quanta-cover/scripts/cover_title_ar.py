# Arabic Quanta cover (DICTO 11-07: each edition gets a title cover in its own script): the same DICTO square with the Persian title
# کوانتوم‌های فضا, یک مانیفست below (Noto Naskh Arabic, RTL shaping via raqm), and ◆ DICTO ◆ in the series LED letters. Same size as the English cover.
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
src = open('cover_title.py').read(); exec(src.split("big = word(")[0])        # glyph(), word(), paste(), colours, N, sq
eng = Image.open('../quanta-cover-front.png'); Wt, Ht = eng.size
def _glyphs_ok(text, font):   # 11-07: a Latin word in a Persian-only font printed as empty boxes; refuse missing glyphs
    f = ImageFont.truetype(font, 60); g = lambda c: bytes(Image.Image()._new(f.getmask(c)).tobytes()); tofu = g('\U0010FFFD')
    miss = sorted({c for c in text if c not in ' \u200c' and g(c) == tofu})
    assert not miss, f'font {font} has no glyphs for {miss}'
def jtext(text, size, col, font='/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf'):
    _glyphs_ok(text, font); f = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM); b = f.getbbox(text, direction='rtl', language='ar'); w, h = b[2] - b[0] + 20, b[3] - b[1] + 20
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((10 - b[0], 10 - b[1]), text, font=f, fill=255, direction='rtl', language='ar')
    a = np.array(m, float) / 255; rgb = np.ones(a.shape + (3,)) * np.array(col, float)
    ys, xs = np.where(a > 0.02); return rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1], a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
big = jtext('كمّات الفضاء', int(N * 0.066), GOLD)
while big[1].shape[1] > N * 0.92: big = jtext('كمّات الفضاء', int(big[1].shape[0] * 0.95), GOLD)
sub = jtext('بيان', int(N * 0.040), WHITE, '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf')
by = word('* DICTO *', int(N * 0.042), lambda ch: RED, big=(0, 2, 3, 4, 5, 6, 8))
H = Ht - N; panel = np.ones((H, N, 3)) * np.array(GROUND, float)
used = big[1].shape[0] + sub[1].shape[0] + by[1].shape[0]; gap = (H - used) / 4.2
y = paste(panel, big, N / 2, int(gap * 1.1)); y = paste(panel, sub, N / 2, int(y + gap)); paste(panel, by, N / 2, int(y + gap))
out = Image.new('RGB', (N, Ht), GROUND); out.paste(eng.crop((0, 0, N, N)), (0, 0)); out.paste(Image.fromarray(np.clip(panel, 0, 255).astype(np.uint8)), (0, N))
out.save('../quanta-cover-front-ar.png')
print('FINAL ok' if os.path.getsize('../quanta-cover-front-ar.png') > 100000 and out.size == eng.size else 'FINAL FAIL (cover)')
