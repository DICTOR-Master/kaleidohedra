# Figure 1 of #76: the seven vertex-first shadows, White Queen to Red Queen, from the app (Kaleidohedra, White Queen world, Shadow,
# stage slider; screenshots by Playwright), cropped and labelled.
from PIL import Image, ImageDraw, ImageFont
import os
H = os.path.dirname(os.path.abspath(__file__)) + '/../figures/'
names = ['White Queen\n600-cell', 'truncated\n600-cell', 'rectified\n600-cell', 'bitruncated\n(midpoint)', 'rectified\n120-cell', 'truncated\n120-cell', 'Red Queen\n120-cell']
tiles = [Image.open(f'{H}stage-fig-{k}.png').crop((230, 230, 670, 670)).resize((330, 330)) for k in range(7)]
W, TH = 330 * 4, 330 + 70
im = Image.new('RGB', (W, TH * 2 + 40), tiles[0].getpixel((2, 2))[:3]); d = ImageDraw.Draw(im)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22); fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 30)
except OSError: f = fb = ImageFont.load_default()
for k, t in enumerate(tiles):
    r, c = divmod(k, 4); x = c * 330 + (165 if r else 0); y = r * TH
    im.paste(t, (x, y)); d.multiline_text((x + 165, y + 335), names[k], fill=(232, 228, 216), font=f, anchor='ma', align='center')
d.text((W - 20, TH * 2 + 30), 'DICTO', fill=(212, 175, 55), font=fb, anchor='rb')
im.save(f'{H}stages-shadows.png'); print(im.size)
