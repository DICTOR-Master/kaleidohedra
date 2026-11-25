# DICTO · partial Vacuus sheet (26 Nov 2026): one A4 page, renders + solidity chart. With Claude (Anthropic).
# Usage: python sheet.py <out.pdf>   (frames renders/sheet/png/p*.png and captions renders/sheet/sheet.json from sheet_scenes.py)
import os, sys, json
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../renders/sheet/')
caps = json.load(open(R + 'sheet.json'))
W, H, M = 2480, 3508, 90; BG = (250, 248, 244); INK = (30, 28, 24); SUB = (95, 90, 82); GOLD = (150, 110, 20)
S = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(S)
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f1, f2, f3 = ImageFont.truetype(FB, 54), ImageFont.truetype(FB, 32), ImageFont.truetype(FN, 26)
d.text((M, 60), "Building out the Vacuus: excavated solids", font=f1, fill=INK)
d.text((M, 130), "DICTO's idea (26 Nov 2026): grow the Vacuus centre into a core (the solid's dual, scaled); the plates become pit walls.", font=f3, fill=SUB)
d.text((M, 166), "Exact renders. Shell see-through; core inside. t = core size (0 Vacuus, 1 solid). Gold = special size (walls on the core's faces).", font=f3, fill=SUB)
LAB = {'Self-Dual Hexadecahedron #1 (canonical)': 'Self-Dual\nHexadecahedron #1', 'Self-Dual Hexadecahedron #68 (canonical)': 'Self-Dual\nHexadecahedron #68'}
rows = []
for c in caps:
    if not rows or rows[-1][0] != c['solid']: rows.append((c['solid'], []))
    rows[-1][1].append(c)
T = 330; y = 220; k = 0
for solid, cs in rows:
    d.multiline_text((M, y), LAB.get(solid, solid.capitalize()), font=f2, fill=INK, spacing=6); x = M + 560
    for c in cs:
        im = Image.open(R + 'png/p%d.png' % k).convert('RGBA').resize((T, T)); k += 1
        bg = Image.new('RGBA', (T, T), BG + (255,)); bg.alpha_composite(im); S.paste(bg.convert('RGB'), (x, y - 10))
        col = GOLD if c['special'] else SUB
        d.text((x + 20, y + T - 30), 't %.3f · %.1f°%s' % (c['t'], c['wedge'], ' special' if c['special'] else ''), font=f3, fill=col)
        x += T + 40
    d.multiline_text((M, y + (100 if solid in LAB else 60)), {'dodecahedron': 'core: icosahedron\nspecial: 5 − 2√5\n= excavated dodecahedron\n(Wenninger 28)',
                                    'icosahedron': 'core: dodecahedron\nspecial: 3√5 − 6\n= great dodecahedron\n(Poinsot 1809)',
                                    'cube': 'core: octahedron\nno special size', 'cuboctahedron': 'core: rhombic\ndodecahedron\nno special size'}.get(solid, 'core: its own dual\nno special size\n(data: McCooey)'), font=f3, fill=SUB, spacing=8)
    y += T + 40
# chart
G = json.load(open(os.path.join(HERE, '../data-build-out-platonic-cubo.json'))) if os.path.exists(os.path.join(HERE, '../data-build-out-platonic-cubo.json')) else None
MC = json.load(open(os.path.join(HERE, '../data-build-out-mccooey.json')))
fig, ax = plt.subplots(figsize=(11, 4.2), dpi=200)
pal = {'tetrahedron': '#cd3e28', 'cube': '#488e48', 'octahedron': '#c9a634', 'dodecahedron': '#8a5cc4', 'icosahedron': '#3a70cd', 'cuboctahedron': '#555555'}
for s in MC['solids']:
    if 'wedge_curve' in s: a = np.array(s['wedge_curve']); ax.plot(a[:, 0], a[:, 1], color='#bbbbbb', lw=0.5, alpha=0.5)
if G:
    for s in G['solids']: a = np.array(s['wedge_curve']); ax.plot(a[:, 0], a[:, 1], color=pal.get(s['name'], 'k'), lw=2, label=s['name'])
Y = MC['yardstick_deg']['dodecahedron']; ax.axhline(Y, color='#96700f', ls='--', lw=1.2); ax.text(0.01, Y + 1.5, 'as solid as the excavated dodecahedron (41.8°)', color='#96700f', fontsize=9)
ax.set_xlabel('core size t (0 = Vacuus, 1 = solid)'); ax.set_ylabel('thinnest wedge between pits (°)'); ax.set_xlim(0, 1); ax.set_ylim(0, 90)
ax.set_title("Solidity: Platonic solids and the cuboctahedron (colour); McCooey's 162 self-duals (grey; 32 reach the line)", fontsize=10)
ax.legend(fontsize=8, ncol=3, loc='upper left'); fig.tight_layout(); cp = R + 'chart.png'; fig.savefig(cp); plt.close(fig)
C = Image.open(cp).convert('RGB'); C = C.resize((W - 2 * M, int(C.height * (W - 2 * M) / C.width))); S.paste(C, (M, y + 10))
d.text((M, H - 70), 'DICTO · dictospheres.com · with Claude (Anthropic). Self-dual solids and names: David McCooey, Visual Polyhedra.', font=f3, fill=SUB)
S.save(sys.argv[1], 'PDF', resolution=300); print('FINAL ok', sys.argv[1], 'y end', y + 10 + C.height, 'of', H - 90)
