# Figure 3, plate style: the diffraction ladder as engraved sepia plates on parchment (2/1, 3/2, 8/5, quasilattice).
import numpy as np
from PIL import Image, ImageDraw, ImageFont
P = '/home/dicto/k-research/studies/2026-11-06-approximant-ladder/'
names = [('diffraction-2-1.npy', '2/1 · ten-fold 0.974'), ('diffraction-3-2.npy', '3/2 · 0.994'), ('diffraction-8-5.npy', '8/5 · 0.997'), ('diffraction-golden.npy', 'quasilattice · 0.998')]
PARCH = np.array([240, 230, 208.]); SEP = np.array([91, 58, 30.])
tiles = []
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf', 22)
except Exception: F = None
for f, lab in names:
    I = np.load(P + f); L = np.log10(I + 1e-4); L = (L - np.percentile(L, 55)) / (L.max() - np.percentile(L, 55)); L = np.clip(L, 0, 1) ** 1.4
    rgb = (PARCH * (1 - L[..., None]) + SEP * L[..., None]).astype(np.uint8)
    im = Image.fromarray(rgb).resize((440, 440), Image.LANCZOS); d = ImageDraw.Draw(im)
    d.ellipse([4, 4, 436, 436], outline=tuple(int(c) for c in SEP), width=2)
    tiles.append((im, lab))
W = Image.new('RGB', (4 * 460 + 20, 520), tuple(int(c) for c in PARCH)); d = ImageDraw.Draw(W)
for k, (t, lab) in enumerate(tiles):
    mask = Image.new('L', (440, 440), 0); ImageDraw.Draw(mask).ellipse([0, 0, 440, 440], fill=255)
    W.paste(t, (20 + k * 460, 20), mask); d.text((20 + k * 460 + 220, 488), lab, fill=tuple(int(c) for c in SEP), font=F, anchor='mm')
W.save('/home/dicto/k-research/studies/2026-11-06-five-in-octet/plate-diffraction.png'); print('ok')
