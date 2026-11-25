"""Preview sheets for the slot schemes (25 Nov 2026). Sheet 1: DICTO's construction (scheme (a)), diagonal (octahedral) form and axial
(cubic) form side by side, whole and pulled apart, pieces labelled as on his templates (A, B, C1, C2). Sheet 2: the other schemes pulled
apart, both forms. Usage: python compose.py <shots dir> <scenes.json> <renders dir> <sheet prefix>"""
import sys, json
from PIL import Image, ImageDraw, ImageFont
SH, SJ, OUT, PRE = sys.argv[1:5]
meta = json.load(open(SJ))
BG = (20, 22, 28); GOLD = (224, 184, 74); TXT = (232, 226, 214); SUB = (200, 200, 205); RED = (232, 120, 104); GRN = (140, 200, 140)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f1, f2, f3, fl, fs = [ImageFont.truetype(p, s) for p, s in ((FB, 34), (FB, 22), (FONT, 18), (FB, 26), (FB, 19))]
FORM = {'octahedron': 'Diagonal (octahedral) form', 'cube': 'Axial (cubic) form: the Resonus squares'}
def tile(i, T, labels=True, small=False):
    m = meta[i]; fr = Image.open(f'{SH}/p{i}.png').convert('RGBA'); bg = Image.new('RGBA', fr.size, BG + (255,))
    im = Image.alpha_composite(bg, fr).convert('RGB'); im.save(f"{OUT}/{m['cut']}-{m['scheme']}-{m['view']}.jpg", quality=92)
    im = im.resize((T, T), Image.LANCZOS)
    if labels and m.get('labels'):
        d = ImageDraw.Draw(im); k = T / fr.size[0]
        for nm, x, y in m['labels']: d.text((x * k, y * k - (30 if small else 0)), nm, font=fs if small else fl, fill=(250, 246, 236), anchor='mm', stroke_width=3, stroke_fill=(40, 30, 20))
    return im
idx = {(m['cut'], m['scheme'], m['view']): i for i, m in enumerate(meta)}
# sheet 1
T = 600; Wd = 2 * T + 120; Ht = 170 + 2 * (T + 20) + 170
S = Image.new('RGB', (Wd, Ht), BG); d = ImageDraw.Draw(S)
d.text((40, 30), "DICTO's three-plane card models: four pieces", font=f1, fill=TXT)
d.text((40, 80), 'A: one slot, edge to centre. B: a slot from the other edge to the centre and two short edge slots.', font=f3, fill=SUB)
d.text((40, 104), 'C1, C2: the third square cut in two along the line where it meets A; one short slot each. Top: assembled. Bottom: pulled apart.', font=f3, fill=SUB)
for c, cut in enumerate(('octahedron', 'cube')):
    x = 40 + c * (T + 40); d.text((x, 140), FORM[cut], font=f2, fill=GOLD)
    for r, v in enumerate(('whole', 'pulled')): S.paste(tile(idx[(cut, 'a', v)], T), (x, 175 + r * (T + 20)))
y = 175 + 2 * (T + 20) + 10
d.text((40, y), 'PROVED POSSIBLE (both forms): A and B slide together on their centre slots; C1 and C2 slide onto B from either side,', font=f3, fill=GRN)
d.text((40, y + 26), 'their slots meeting B\'s short edge slots, straight edges against A. Pieces 80 mm across, slots 1.5 mm, as on the templates.', font=f3, fill=SUB)
d.text((40, y + 52), 'Three whole cards can never be put together by sliding (README, Theorem 1): one card must be cut.', font=f3, fill=SUB)
d.text((Wd - 40, Ht - 26), 'DICTO · dictospheres.com', font=f3, fill=GOLD, anchor='rd')
S.save(f'{PRE}1-dicto-construction.png', optimize=True); print('sheet 1', S.size)
# sheet 2
HOW = {'W': ['Three whole cards (any slots):', 'PROVED IMPOSSIBLE, no card can leave first'],
       'b': ['C in four quarters, no slots in C:', 'PROVED POSSIBLE, quarters drop into the corners'],
       'c': ['A closed centre slot in A:', 'PROVED IMPOSSIBLE, A and B lock']}
T = 470; Wd = 3 * T + 100; Ht = 150 + 2 * (T + 46) + 120
S = Image.new('RGB', (Wd, Ht), BG); d = ImageDraw.Draw(S)
d.text((40, 30), 'Other ways to slot three perpendicular cards, pulled apart', font=f1, fill=TXT)
d.text((40, 80), 'Rows: diagonal (octahedral) form, axial (cubic) form. Same outcome for both forms, scheme by scheme (exhaustive search, README).', font=f3, fill=SUB)
for c, key in enumerate(('W', 'b', 'c')):
    x = 40 + c * (T + 10)
    for r, cut in enumerate(('octahedron', 'cube')):
        yy = 120 + r * (T + 46); d.text((x, yy), FORM[cut].split(':')[0], font=f3, fill=GOLD)
        S.paste(tile(idx[(cut, key, 'pulled')], T - 10, small=True), (x, yy + 26))
    oc = meta[idx[('octahedron', key, 'pulled')]]['outcome']
    for l, line in enumerate(HOW[key]): d.text((x, 120 + 2 * (T + 46) + 26 * l), line, font=f3, fill=(GRN if oc == 'POSSIBLE' else RED) if l else SUB)
for i, m in enumerate(meta):                      # every frame also as its own jpg
    if m['view'] == 'whole' and m['scheme'] != 'a': tile(i, 800, False)
d.text((Wd - 40, Ht - 26), 'DICTO · dictospheres.com', font=f3, fill=GOLD, anchor='rd')
S.save(f'{PRE}2-other-schemes.png', optimize=True); print('sheet 2', S.size)
import os
ok = all(os.path.getsize(f'{PRE}{n}.png') > 0 for n in ('1-dicto-construction', '2-other-schemes')) and len(idx) == 16
print('FINAL ok' if ok else 'FINAL FAIL: a sheet missing or not 16 frames')
