# Vacuus-Solids paper: figures from the exact renders of study 2026-11-25-partial-vacuus (26 Nov 2026). With Claude (Anthropic).
# fig1-family.jpg: dodecahedron, icosahedron, cube, cuboctahedron at three core sizes (frames p0-p11 of renders/sheet);
# fig2-special.jpg: the eleven special sizes with their cores (renders/special); fig3-solidity.png: the solidity chart.
import os, json, shutil
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, '../../../studies/2026-11-25-partial-vacuus/renders')
F = os.path.join(HERE, '../figures'); FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
INSET_LAB = None   # per panel: 'core' where Q is the real core (hull of the pit tips), else 'Q'
def _inset(W, d, insets, k, x, y, T):
    # the core alone, enlarged, top right of the cell, in a thin frame, labelled "core"
    if not insets: return
    S2 = int(T * 0.36); im = Image.open(insets[k]).convert('RGBA').resize((S2, S2)); bg = Image.new('RGBA', (S2, S2), (255, 255, 255, 255)); bg.alpha_composite(im)
    X, Y = x + T - S2 - 6, y + 6; W.paste(bg.convert('RGB'), (X, Y)); d.rectangle([X, Y, X + S2, Y + S2], outline=(170, 162, 150), width=1)
    d.text((X + 6, Y + 4), INSET_LAB[k] if INSET_LAB else 'core', font=ImageFont.truetype(FN, 16), fill=(110, 104, 95))
def grid(frames, cols, labels, out, T=420, LH=40, insets=None):
    rows = (len(frames) + cols - 1) // cols; W = Image.new('RGB', (cols * T, rows * (T + LH)), 'white'); d = ImageDraw.Draw(W); f = ImageFont.truetype(FN, 22)
    for k, (fr, lab) in enumerate(zip(frames, labels)):
        im = Image.open(fr).convert('RGBA').resize((T, T)); bg = Image.new('RGBA', (T, T), (255, 255, 255, 255)); bg.alpha_composite(im)
        x, y = (k % cols) * T, (k // cols) * (T + LH); W.paste(bg.convert('RGB'), (x, y)); _inset(W, d, insets, k, x, y, T); d.multiline_text((x + 12, y + T + 6), lab, font=f, fill=(40, 36, 30), spacing=6)
    W.save(out, quality=90)
cap = json.load(open(os.path.join(S, 'sheet/sheet.json')))
grid([os.path.join(S, 'sheet/png/p%d.png' % k) for k in range(12)], 3,
     ['%s, t = %.3f%s' % (c['solid'], c['t'], ' (special)' if c['special'] else '') for c in cap[:12]], os.path.join(F, 'fig1-family.jpg'))
sp = json.load(open(os.path.join(S, 'special/special.json')))
# fig 2 (redone 26 Nov, DICTO): the eleven exact special sizes in fig 1's style, three columns, three-line labels
CLOSED = {'5 - 2*sqrt(5)': '5 − 2√5', '10/11 - 3*sqrt(5)/11': '(10 − 3√5)/11', 'sqrt(5)/3': '√5/3', '-6 + 3*sqrt(5)': '3√5 − 6',
          '-9/11 + 6*sqrt(5)/11': '(6√5 − 9)/11', '30/11 - 9*sqrt(5)/11': '(30 − 9√5)/11', '3 - sqrt(5)': '3 − √5',
          '42/19 - 11*sqrt(5)/19': '(42 − 11√5)/19', '9 - 6*sqrt(2)': '9 − 6√2', '12/11 - 3*sqrt(5)/11': '(12 − 3√5)/11',
          '3 - 6*sqrt(5)/5': '3 − 6√5/5'}
# 27 Nov (DICTO: is it sound to draw these cores?): drawn inside only where the pits reach Q (core_or_planes.py)
LINE2 = {'core': 'core: %s\n(pit tips = its corners)', 'touch': 'Q: %s\n(meets the pits at its corners)',
         'planes': 'Q: %s\n(shares the wall planes only)'}
INSET_LAB = ['core' if c['kind'] == 'core' else 'Q' for c in sp]
grid([os.path.join(S, 'special/png/p%d.png' % k) for k in range(len(sp))], 3,
     ['%s\n%s\ns = %s' % (c['P'], LINE2[c['kind']] % c['Q'], CLOSED[c['s']]) for c in sp],
     os.path.join(F, 'fig2-special.jpg'), T=420, LH=132, insets=[os.path.join(S, 'special/png/p%d.png' % (k + len(sp))) for k in range(len(sp))])
shutil.copy(os.path.join(S, 'sheet/chart.png'), os.path.join(F, 'fig3-solidity.png'))
print('FINAL ok')
