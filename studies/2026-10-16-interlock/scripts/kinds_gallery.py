# Labelled galleries of the interlock pieces (tiles from shoot_kinds.mjs), DICTO's names: Interlock set 1 (Dharma-Ends) I1·1..I1·12,
# set 2 (Dharma-Middle) I2·1..I2·11, largest first, with shape abbreviation. Each label: name, count, the original layer -> the flipped layer it lies in, corners/faces.
# -> renders/kinds-ends.png, renders/kinds-middle.png
import sys, json, re, collections
from PIL import Image, ImageDraw, ImageFont, ImageChops
src = sys.argv[1]
SH = {'icosahedron': 'I', 'icosidodecahedron': 'ID', 'dodecahedron': 'D', 'truncated icosahedron': 'TI', 'Hecatodihedron': 'H', 'rhombic triacontahedron': 'RT',
      'icosahedron (phi^3)': 'Iφ³', 'dodecahedron (inner)': 'D', 'dual of the Hecatodihedron': 'O', 'pentakis dodecahedron': 'PD', 'dodecahedron (phi^3)': 'Dφ³'}
def short(layer): a, b = layer.split(' -> '); return f'{SH[a]}→{SH[b]}'
txt = open('data/interlock-kinds.txt').read()
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24); bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
SHAPE = {'ends': '12f TBP 7f 7f 12f 7f QPy PPy PPy Tet QPy Tet'.split(), 'middle': '7f 11f 7f HPy 7f 6f Tet QPy Tet Tet Tet'.split()}
for setting, code in (('ends', 'I1·'), ('middle', 'I2·')):
    block = txt.split(f'== {setting} setting')[1].split('== ')[0]
    kinds = re.findall(r'(\d+) x vol .*?= ([0-9.]+)\n\s+in original layer: (.*?) \(\d+\)\n\s+in flipped layer: (.*?) \(turn (-?\d+)\) \(\d+\)\n\s+(\d+) corners, (\d+) faces', block)
    n = len(kinds); cols = 4; rows = (n + cols - 1) // cols; T, H = 420, 110
    img = Image.new('RGB', (cols * T, rows * (T + H) + 50), (244, 241, 234)); d = ImageDraw.Draw(img)
    for i, (cnt, vol, ol, fl, turn, nc, nf) in enumerate(kinds):
        t = Image.open(f'{src}/kind-{setting}-{i}.png').convert('RGB'); bg = Image.new('RGB', t.size, t.getpixel((0, 0)))
        t = t.crop(ImageChops.difference(t, bg).convert('L').point(lambda v: 255 if v > 8 else 0).getbbox())
        f = 0.8 * T / max(t.size); t = t.resize((int(t.width * f), int(t.height * f)), Image.LANCZOS)
        x, y = (i % cols) * T, (i // cols) * (T + H); img.paste(t, (x + (T - t.width) // 2, y + (T - t.height) // 2))
        l1 = f'{code}{i + 1} ({SHAPE[setting][i]})  ×{cnt}'; l2 = f'original {short(ol)} · reversed {short(fl)}'; l3 = f'{nc} corners, {nf} faces · vol {float(vol):.4f}'
        for j, (s, fn) in enumerate(((l1, bold), (l2, font), (l3, font))):
            w = d.textlength(s, font=fn); d.text((x + (T - w) / 2, y + T + 4 + j * 34), s, fill=(42, 34, 24), font=fn)
    s = 'DICTO · dictospheres.com'; d.text((cols * T - d.textlength(s, font=font) - 16, rows * (T + H) + 12), s, fill=(91, 83, 70), font=font)
    img.save(f'renders/kinds-{setting}.png'); print(setting, n)
