# Compose the paper's piece gallery (Figure 4) from the tiles of shoot_pieces.mjs: one piece of each layer, faithful nest (a-f)
# and the tight nest's two new end pieces (g, h). Each tile at its own scale. Writes renders/polar-pieces-gallery.png.
import sys
from PIL import Image, ImageDraw, ImageFont
src = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
tiles = [('0', '(a) D → ID: column, ×12'), ('1', '(b) ID → O: cap, ×12'), ('2', '(c) O → PD: pyramid, ×20'), ('3', '(d) PD → I: wedge, ×60'),
         ('4', '(e) I → RT: pyramid, ×20'), ('5', '(f) RT → D·φ³: roof, ×30'), ('t0', '(g) tight D → ID, ×12'), ('t5', '(h) tight RT → D, ×30')]
T, H = 500, 80
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32); mark = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
img = Image.new('RGB', (4 * T, 2 * (T + H) + 40), (244, 241, 234)); d = ImageDraw.Draw(img)
for i, (k, lab) in enumerate(tiles):
    x, y = (i % 4) * T, (i // 4) * (T + H)
    t = Image.open(f'{src}/piece-{k}.png').convert('RGB')   # crop to the piece, then fit it centred in the tile
    bg = Image.new('RGB', t.size, t.getpixel((0, 0))); from PIL import ImageChops
    bx = ImageChops.difference(t, bg).convert('L').point(lambda v: 255 if v > 8 else 0).getbbox(); t = t.crop(bx)
    f = 0.86 * T / max(t.size); t = t.resize((int(t.width * f), int(t.height * f)), Image.LANCZOS)
    img.paste(t, (x + (T - t.width) // 2, y + (T - t.height) // 2))
    w = d.textlength(lab, font=font); d.text((x + (T - w) / 2, y + T + 8), lab, fill=(42, 34, 24), font=font)
s = 'DICTO · dictospheres.com'; d.text((4 * T - d.textlength(s, font=mark) - 14, 2 * (T + H) + 2), s, fill=(91, 83, 70), font=mark)
img.save('renders/polar-pieces-gallery.png'); print('renders/polar-pieces-gallery.png')
