"""Preview sheet (skeletal renders, 24 Nov) and single renders on the dark ground. Usage: python compose.py <shots dir> <renders dir> <sheet.jpg>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
SH, OUT, SHEET = sys.argv[1:4]
BG = (20, 22, 28)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
names = ['octahedron-cardboard-skeleton', 'octahedron-cardboard-skeleton-pulled', 'cube-b1nr-skeleton', 'cube-b1nr-skeleton-pulled',
         'cuboctahedron-b1nr-struts', 'cuboctahedron-b1nr-struts-axis3', 'dodecahedron-b1nr-struts', 'dodecahedron-b1nr-struts-axis5']
caps = ['Cardboard octahedron: three square frames', 'The three square frames pulled apart',
        'B1NR cube: hull + centre struts, empty', 'Its six pyramid frames pulled apart',
        'Cuboctahedron: 12 centre struts, no hull', 'Down a three-fold axis', 'Dodecahedron: 20 centre struts, no hull', 'Down a five-fold axis']
tiles = []
for i, n in enumerate(names):
    fr = Image.open(f'{SH}/p{i}.png').convert('RGBA'); bg = Image.new('RGBA', fr.size, BG + (255,)); im = Image.alpha_composite(bg, fr).convert('RGB')
    im.save(f'{OUT}/{n}.jpg', quality=92); tiles.append(im)
T = 560; rows = [[0, 1], [2, 3], [4, 5], [6, 7]]; heads = ['1  Cardboard octahedron Vacuus', '2  B1NR cube', '3  B1NR cuboctahedron Vacuus (no hull)', '4  B1NR dodecahedron Vacuus (no hull)']
W = 2 * T + 80; H = 140 + len(rows) * (T + 110) + 40
S = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(S)
f1, f2, f3 = ImageFont.truetype(FB, 34), ImageFont.truetype(FB, 24), ImageFont.truetype(FONT, 18)
d.text((40, 40), 'DICTO Vacuus builds: exact skeletal renders', font=f1, fill=(232, 226, 214))
y = 120
for r, row in enumerate(rows):
    d.text((40, y), heads[r], font=f2, fill=(224, 184, 74)); y += 40
    for c, i in enumerate(row):
        x = 40 + c * T; S.paste(tiles[i].resize((T - 20, T - 20), Image.LANCZOS), (x, y)); d.text((x, y + T - 12), caps[i], font=f3, fill=(200, 200, 205))
    y += T + 70
d.text((W - 40, H - 30), 'DICTO · dictospheres.com', font=f3, fill=(224, 184, 74), anchor='rd')
S.save(SHEET, quality=90); print('sheet', S.size); print('FINAL ok')
