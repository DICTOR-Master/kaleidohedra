# Star Cores book: move the DICTO mark of each card picture from its own bottom strip to the free top-right corner and trim the strip,
# so that picture and data fit one page. Usage: card_trim.py <png>...
import sys, numpy as np
from PIL import Image
for fn in sys.argv[1:]:
    im = Image.open(fn).convert('RGB'); a = np.asarray(im); H, W = a.shape[:2]; nw = (a < 245).any(2)
    y0, x0 = int(H * 0.82), W - 230
    ys, xs = np.nonzero(nw[y0:, x0:])
    if len(ys) == 0: print('no mark', fn); continue
    box = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1); mark = im.crop(box)
    body = nw[:, :x0 - 10]; last = np.nonzero(body.any(1))[0].max()
    top_free = not nw[:mark.height + 10, W - mark.width - 10:].any()
    out = im.crop((0, 0, W, last + 12)).copy()
    if top_free: out.paste(mark, (W - mark.width - 4, 4))
    else: out = im.crop((0, 0, W, max(last + 12, box[3] + 4)))
    out.convert('P', palette=Image.ADAPTIVE, colors=256).save(fn); print(fn, H, '->', out.height, 'mark top' if top_free else 'mark kept')
