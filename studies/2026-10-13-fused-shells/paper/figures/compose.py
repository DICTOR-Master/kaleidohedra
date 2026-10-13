# Compose the paper's figure plates from the study's renders (renders/*.png, 900 px, the catalogue's look).
# Run on dicto-node: python compose.py <renders dir> <out dir>. Output: fig1..fig6 as JPEG (modest size). DICTO · dictospheres.com
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageChops
R, OUT = sys.argv[1], sys.argv[2]
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f_lab = ImageFont.truetype(FONT, 30); f_mark = ImageFont.truetype(FONT, 22)
PLATES = {
    'fig1-karma-route': (['karma-step0%d.png' % i for i in range(1, 7)], 3, True),
    'fig2-dharma-route': (['dharma-step%02d.png' % i for i in range(1, 12)], 4, True),
    'fig3-bodhi-route': (['bodhi-step0%d.png' % i for i in range(1, 7)], 3, True),
    'fig4-named-inbetweens': (['karma-step02.png', 'karma-step03.png', 'bodhi-step02.png', 'dharma-step07.png', 'dharma-step10.png', 'dharma-step02.png'], 3, False),
    'fig5-samsara-stages': (['app-karma-step2-step%02d.png' % i for i in range(1, 12)], 4, True),
    'fig6-convex-partials': (['dharma-stage%03d.png' % i for i in (62, 38, 29, 84, 31, 85, 86, 88, 83, 89, 69, 76)], 4, False),
}

def bbox(im):
    bg = Image.new(im.mode, im.size, (0, 0, 0))
    return ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 12 else 0).getbbox()

for name, (files, cols, common) in PLATES.items():
    ims = [Image.open(os.path.join(R, f)).convert('RGB') for f in files]
    boxes = [bbox(im) for im in ims]
    if common:  # one crop for all panels, so sizes stay comparable through the growth
        x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes); x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
        boxes = [(x0, y0, x1, y1)] * len(ims)
    tiles = []
    for im, b in zip(ims, boxes):
        x0, y0, x1, y1 = b; s = max(x1 - x0, y1 - y0) + 40; cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        crop = im.crop((cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2)).resize((420, 420), Image.LANCZOS)
        tiles.append(crop)
    rows = (len(tiles) + cols - 1) // cols
    W, H = cols * 420 + (cols + 1) * 10, rows * 420 + (rows + 1) * 10 + 40
    P = Image.new('RGB', (W, H), (0, 0, 0)); D = ImageDraw.Draw(P)
    for k, t in enumerate(tiles):
        x = 10 + (k % cols) * 430; y = 10 + (k // cols) * 430
        P.paste(t, (x, y)); D.text((x + 10, y + 6), '(%s)' % chr(97 + k), fill=(235, 235, 235), font=f_lab)
    D.text((W - 10, H - 12), 'DICTO · dictospheres.com', fill=(200, 200, 200), font=f_mark, anchor='rs')
    P.save(os.path.join(OUT, name + '.jpg'), quality=86, optimize=True)
    print(name, P.size)
