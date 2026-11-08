"""Make DICTO stand out on the straightened Takasegawa flyer: gentle levels on the whole sheet, then a dark plate with a
gold border, a gold pin and a bold gold DICTO over the original small label (pin at 642,890 in flat.png), and a glow ring.
Everything else on the organisers' flyer is left as printed. Usage: highlight.py flat.png out.png"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
im = Image.open(sys.argv[1]).convert('RGB')
im = ImageOps.autocontrast(im, cutoff=0.5); im = ImageEnhance.Color(im).enhance(1.08)
GOLD = (232, 194, 90); PX, PY = 642, 890
# glow ring round the pin
glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
g.ellipse([PX - 34, PY - 34, PX + 34, PY + 34], outline=GOLD + (255,), width=8)
glow = glow.filter(ImageFilter.GaussianBlur(5)); im.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(im)
# plate over the original label
x0, y0, x1, y1 = 622, 862, 880, 918
d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=(18, 16, 14), outline=GOLD, width=4)
# pin: gold teardrop
d.ellipse([PX - 13, PY - 17, PX + 13, PY + 9], fill=GOLD); d.polygon([(PX - 11, PY - 1), (PX + 11, PY - 1), (PX, PY + 20)], fill=GOLD)
d.ellipse([PX - 5, PY - 9, PX + 5, PY + 1], fill=(18, 16, 14))
f = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf', 38)
d.text((694, PY), 'DICTO', font=f, fill=GOLD, anchor='lm')
# outer ring on the river beside the pin
d.ellipse([PX - 40, PY - 40, PX + 40, PY + 40], outline=GOLD, width=4)
im.save(sys.argv[2], quality=92); print('saved', sys.argv[2])
