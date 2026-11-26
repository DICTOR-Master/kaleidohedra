# Vacuus-Solids paper: figures from the exact renders of study 2026-11-25-partial-vacuus (26 Nov 2026). With Claude (Anthropic).
# fig1-family.jpg: dodecahedron, icosahedron, cube, cuboctahedron at three core sizes (frames p0-p11 of renders/sheet);
# fig2-special.jpg: the twelve special sizes with their cores (renders/special); fig3-solidity.png: the solidity chart.
import os, json, shutil
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, '../../../studies/2026-11-25-partial-vacuus/renders')
F = os.path.join(HERE, '../figures'); FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def grid(frames, cols, labels, out, T=420):
    rows = (len(frames) + cols - 1) // cols; W = Image.new('RGB', (cols * T, rows * (T + 40)), 'white'); d = ImageDraw.Draw(W); f = ImageFont.truetype(FN, 22)
    for k, (fr, lab) in enumerate(zip(frames, labels)):
        im = Image.open(fr).convert('RGBA').resize((T, T)); bg = Image.new('RGBA', (T, T), (255, 255, 255, 255)); bg.alpha_composite(im)
        x, y = (k % cols) * T, (k // cols) * (T + 40); W.paste(bg.convert('RGB'), (x, y)); d.text((x + 12, y + T + 6), lab, font=f, fill=(40, 36, 30))
    W.save(out, quality=90)
cap = json.load(open(os.path.join(S, 'sheet/sheet.json')))
grid([os.path.join(S, 'sheet/png/p%d.png' % k) for k in range(12)], 3,
     ['%s, t = %.3f%s' % (c['solid'], c['t'], ' (special)' if c['special'] else '') for c in cap[:12]], os.path.join(F, 'fig1-family.jpg'))
sp = json.load(open(os.path.join(S, 'special/special.json')))
grid([os.path.join(S, 'special/png/p%d.png' % k) for k in range(12)], 4, ['%s / %s' % (c['P'], c['Q']) for c in sp], os.path.join(F, 'fig2-special.jpg'), T=360)
shutil.copy(os.path.join(S, 'sheet/chart.png'), os.path.join(F, 'fig3-solidity.png'))
print('FINAL ok')
