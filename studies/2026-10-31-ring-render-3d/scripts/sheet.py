# Photo / render pairs for the three views of the bipyramid, DICTO mark on each render, "photo © DICTO" note.
# The output contains DICTO's photos: write it only outside the repository.
# Usage: ~/geom/bin/python sheet.py photodir renderdir logo out.png [title-suffix]
#    or: ~/geom/bin/python sheet.py mark render.png logo out.png
import sys, os
from PIL import Image, ImageDraw, ImageFont
if sys.argv[1] == 'mark':                       # sheet.py mark render.png logo out.png : DICTO mark on a single render
    im = Image.open(sys.argv[2]).convert('RGB'); lg = Image.open(sys.argv[3]).convert('RGBA')
    k = int(im.width * 0.11); lg = lg.resize((k, int(k * lg.height / lg.width)), Image.LANCZOS)
    im.paste(lg, (im.width - k - im.width // 40, im.height - lg.height - im.width // 40), lg); im.save(sys.argv[4]); sys.exit()
pd, rd, logo, out = sys.argv[1:5]; sfx = sys.argv[5] if len(sys.argv) > 5 else ''
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = lambda s, b=False: ImageFont.truetype(FB if b else F, s)
w, h = 600, 800; g = 24; top = 120; BG = (243, 241, 235)
W = 6 * w + 5 * g + 2 * 40 - 3 * g + 3 * 50; H = top + h + 110
sheet = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(sheet)
d.text((40, 24), 'Ring bipyramid: photo beside 3D render' + sfx, font=font(42, True), fill=(30, 30, 30))
d.text((40, 76), "24 PET-bottle-cap security rings, 72 zip ties; render: true 3D bands (Blender Cycles), camera fitted to each photo",
       font=font(24), fill=(80, 80, 80))
lg = Image.open(logo).convert('RGBA'); lg = lg.resize((90, int(90 * lg.height / lg.width)), Image.LANCZOS)
x = 40
for i in (1, 2, 3):
    ph = Image.open(os.path.join(pd, f'2026-10-31-double-pyramid-{i}.jpg')).convert('RGB').resize((w, h), Image.LANCZOS)
    rn = Image.open(os.path.join(rd, f'render-{i}.png')).convert('RGB').resize((w, h), Image.LANCZOS)
    rn.paste(lg, (w - lg.width - 14, h - lg.height - 14), lg)
    sheet.paste(ph, (x, top)); sheet.paste(rn, (x + w + g // 2, top))
    d.text((x, top + h + 10), f'photo {i}', font=font(24, True), fill=(40, 40, 40))
    d.text((x + w + g // 2, top + h + 10), f'render {i}', font=font(24, True), fill=(40, 40, 40))
    x += 2 * w + g // 2 + 50
d.text((40, H - 46), 'photo © DICTO · render: 3D model of DICTO\'s ring build · 2026-10-31 · not for publication', font=font(22),
       fill=(110, 110, 110))
sheet.save(out); print(out, sheet.size)
