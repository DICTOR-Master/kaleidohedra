"""Preview sheet and single renders on the dark ground. Usage: python compose.py <study dir> <shots dir> <sheet.jpg>"""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
ST, SH, SHEET = sys.argv[1:4]
VD = json.load(open(os.path.join(ST, 'data/verdicts.json')))['verdicts']
BG = (20, 22, 28)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
ORDER = ['RVCMG_V2_TRIANGLE_TO_UHEX', 'RVCMG_V2_SQUARE_TO_UHEX', 'RVCMG_V2_PENTAGON_TO_UHEX', 'RVCMG_V2_GOLDEN_RHOMBUS_TO_UHEX',
         'RVCMG_V2_RD_NATIVE_RHOMBUS_TO_UHEX', 'RVCMG_V2_DI_KITE_TO_UHEX', 'RVCMG_V2_DH_KITE_TO_UHEX', 'RVCMG_V2_REGULAR_HEX_TO_UHEX',
         'RVCMG_TRIANGLE_TO_RDH', 'RVCMG_SQUARE_TO_RDH', 'RVCMG_PENTAGON_TO_RDH', 'RVCMG_GOLDEN_RHOMBUS_TO_RDH',
         'RVCMG_DI_KITE_TO_RDH', 'RVCMG_DH_KITE_TO_RDH', 'RVCMG_REGULAR_HEX_TO_RDH', 'RVCMG_RD_HEMI']
LABEL = ['Triangle', 'Square', 'Pentagon', 'Golden rhombus', 'RD rhombus', 'DI kite', 'DH kite', 'Regular hexagon',
         'Triangle', 'Square', 'Pentagon', 'Golden rhombus', 'DI kite', 'DH kite', 'Regular hexagon', 'RD-Hemi']
def cap(pid):
    """two short lines: the type, then convexity and the merged corners (bent-wall reading)"""
    f = VD[pid]['flat']; b = VD[pid].get('bent', f); t = f"SF {f['n']}-{f['m']}-{f['k']}"; cv = 'convex' if f['convex'] else 'not convex'
    if f['simple']: return [t + ', a frustum', cv + ', simple']
    merged = sum(1 for i, d in enumerate(b['degrees']) if d >= 4)
    if merged == 0: return [t + ', degenerate', cv + '; bent walls: simple']
    return [t + ', degenerate', f'{cv}; {merged} merged corner' + ('s' if merged > 1 else '')]
tiles = []
os.makedirs(os.path.join(ST, 'renders'), exist_ok=True)
for i, pid in enumerate(ORDER):
    fr = Image.open(f'{SH}/p{i}.png').convert('RGBA'); bg = Image.new('RGBA', fr.size, BG + (255,)); im = Image.alpha_composite(bg, fr).convert('RGB')
    im.save(os.path.join(ST, 'renders', pid.lower().replace('_', '-') + '.jpg'), quality=92); tiles.append(im)
T = 420; C = 4; W = C * T + 80
rows = [ORDER[0:4], ORDER[4:8], ORDER[8:12], ORDER[12:16]]
heads = {0: 'Version 2 (17 Sep 2026): regular hexagon end, edge sqrt(2)/2, height 1/4', 2: 'Version 1 (15 Sep 2026): rhombic dodecahedron hexagon end, height sqrt(2)/4'}
H = 120 + 4 * (T + 80) + 2 * 46 + 60
S = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(S)
f1, f2, f3 = ImageFont.truetype(FB, 32), ImageFont.truetype(FB, 22), ImageFont.truetype(FONT, 17)
d.text((40, 36), 'DICTO RVCMG adapter pieces: exact renders, as Scutoid Frusta (preview)', font=f1, fill=(232, 226, 214))
y = 100
for r, row in enumerate(rows):
    if r in heads: d.text((40, y), heads[r], font=f2, fill=(224, 184, 74)); y += 46
    for c, pid in enumerate(row):
        i = ORDER.index(pid); x = 40 + c * T
        S.paste(tiles[i].resize((T - 20, T - 20), Image.LANCZOS), (x, y))
        d.text((x, y + T - 14), LABEL[i], font=f2, fill=(220, 220, 225)); c1, c2 = cap(pid); d.text((x, y + T + 14), c1, font=f3, fill=(190, 190, 198)); d.text((x, y + T + 36), c2, font=f3, fill=(190, 190, 198))
    y += T + 80
d.text((40, H - 34), 'Hexagon end at the bottom (silver), target end on top (cream); gold = merged corner (two hexagon corners in one; a Y-corner merged into the end)', font=f3, fill=(200, 200, 205))
d.text((W - 40, H - 34), 'DICTO · dictospheres.com', font=f3, fill=(224, 184, 74), anchor='ra')
S.save(SHEET, quality=90); print('sheet', S.size); print('FINAL ok')
