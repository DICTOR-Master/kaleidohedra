# Japanese DICTOnary cover (DICTO 11-07: "any japanese language version gets a katakana cover"): the golden DICTO square of the
# English cover, with a Japanese title panel: katakana ディクトナリー・オブ・アトムズ (dictionary → ディクショナリー, long mark kept),
# the Japanese title DICTO 原子辞典 ― 空間の量子 II, and ◆ DICTO ◆ in the series LED letters. Same size as the English cover.
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
exec(open('cover_title.py').read().split("big = fit(")[0])          # word(), paste(), colours, N, sq
eng = Image.open('../dictonary-cover-front-golden.png'); Wt, Ht = eng.size
def jtext(text, size, col, font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'):
    f = ImageFont.truetype(font, size, index=0); b = f.getbbox(text); w, h = b[2] - b[0] + 20, b[3] - b[1] + 20
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((10 - b[0], 10 - b[1]), text, font=f, fill=255)
    a = np.array(m, float) / 255; rgb = np.ones(a.shape + (3,)) * np.array(col, float)
    ys, xs = np.where(a > 0.02); return rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1], a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
T = 'ディクトナリー・オブ・アトムズ'; s = int(N * 0.066); big = jtext(T, s, GOLD)
while big[1].shape[1] > N * 0.92: s = int(s * 0.96); big = jtext(T, s, GOLD)
sub = jtext('DICTO 原子辞典 ― 空間の量子 II', int(N * 0.036), WHITE, '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc')
by = word('* DICTO *', int(N * 0.042), lambda ch: RED, big=(0, 2, 3, 4, 5, 6, 8))
H = Ht - N; panel = np.ones((H, N, 3)) * np.array(GROUND, float)
used = big[1].shape[0] + sub[1].shape[0] + by[1].shape[0]; gap = (H - used) / 4.2
y = paste(panel, big, N / 2, int(gap * 1.1)); y = paste(panel, sub, N / 2, int(y + gap)); paste(panel, by, N / 2, int(y + gap))
out = Image.new('RGB', (N, Ht), GROUND); out.paste(eng.crop((0, 0, N, N)), (0, 0)); out.paste(Image.fromarray(np.clip(panel, 0, 255).astype(np.uint8)), (0, N))
out.save('../dictonary-cover-front-golden-ja.png')
print('FINAL ok' if os.path.getsize('../dictonary-cover-front-golden-ja.png') > 100000 and out.size == eng.size else 'FINAL FAIL (cover)')
