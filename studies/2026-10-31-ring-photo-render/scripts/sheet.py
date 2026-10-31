# Comparison sheet for the photo-real ring render test (2026-10-31): DICTO's photo of one real big triangle beside the render
# of the same 4-ring face, then the 16-ring tetrahedron and the 48-ring h-tile; DICTO mark in the bottom-right corner.
# Usage (dicto-big-brother): PHOTO=... CUTDIR=... OUTDIR=... LOGO=~/kres-tmp/dicto-logo.png ~/geom/bin/python sheet.py
import os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
P = lambda k: os.path.expanduser(os.environ[k])
OUT = P('OUTDIR'); meta = json.load(open(os.path.join(P('CUTDIR'), 'cutouts.json')))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = lambda s, b=False: ImageFont.truetype(FB if b else F, s)
BG = (243, 241, 235); W, H = 2400, 1950
sheet = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(sheet)
d.text((40, 28), 'Photo-real ring renders: first test', font=font(46, True), fill=(30, 30, 30))
d.text((40, 88), "DICTO's PET-bottle-cap security rings, cut out of his photo and placed on the exact ring triangles "
       "(ring side 1/2, unit triangle = 4 rings)", font=font(25), fill=(70, 70, 70))
# (a) photo crop of the first big triangle (rings of cluster 1 = the four rings nearest the top-left)
ph = Image.open(P('PHOTO')).convert('RGB')
C = sorted(meta['rings'], key=lambda m: m['photo_centre'][1])[:4]
c = np.mean([m['photo_centre'] for m in C], 0); R = 230
crop = ph.crop((int(c[0] - R), int(c[1] - R), int(c[0] + R), int(c[1] + R))).resize((700, 700), Image.LANCZOS)
y0 = 150
sheet.paste(crop, (40, y0 + 40)); fl = Image.open(os.path.join(OUT, 'render-flat-top.png')); m = fl.width // 9
sheet.paste(fl.crop((m, m, fl.width - m, fl.height - m)).resize((700, 700), Image.LANCZOS), (760, y0 + 40))
d.text((40, y0), '(a) photo: one real big triangle (4 rings, tied)', font=font(26, True), fill=(40, 40, 40))
d.text((760, y0), '(a) render: the same face, top view', font=font(26, True), fill=(40, 40, 40))
t = Image.open(os.path.join(OUT, 'render-tetra.png')); t = t.resize((900, int(900 * t.height / t.width)), Image.LANCZOS)
sheet.paste(t, (1480, y0 + 40)); d.text((1480, y0), '(b) tetrahedron, 16 rings (4 faces x 4)', font=font(26, True), fill=(40, 40, 40))
y1 = 940
h = Image.open(os.path.join(OUT, 'render-htile.png')); h = h.resize((1300, int(1300 * h.height / h.width)), Image.LANCZOS)
sheet.paste(h, (40, y1 + 40)); d.text((40, y1), '(c) HexOct h-tile at λ = −1/8, 48 rings, 144 ties (three-quarter view)', font=font(26, True), fill=(40, 40, 40))
notes = [
    ('Method', True),
    ('12 rings cut out of one top-view photo (white vs tatami,', False),
    ('split at the open centres); each pasted on its ring', False),
    ('triangle by its three tips, pulled 45 % towards the', False),
    ('model outline; band = conical height field; central', False),
    ('ring of each 4-ring face turned over (DICTO);', False),
    ('ties cut from the photo, folded over shared sides;', False),
    ('lit by face angle, ground shadow.', False),
    ('Photo: central rings look slightly larger and more', False),
    ('triangular than corner rings (tied on all 3 sides).', False),
    ('', False),
    ('What still looks fake', True),
    ('- rings seen edge-on: the band wall is a stretched', False),
    ('  top view (streaky), its height is assumed (0.13 side)', False),
    ('- the inside of every ring is the same top-view photo', False),
    ('- ties are flat decals, not straps around two bands', False),
    ('- no translucency, no bounce light, one light only', False),
    ('', False),
    ('Photos that would fix it', True),
    ('- one ring standing on edge, side view, both ways up', False),
    ('- one ring from below (other side) next to from above', False),
    ('- two tied rings close up from the side (a real tie)', False),
    ('- a ring at 45 degrees; all on a plain white sheet', False),
]
y = y1 + 60
for s, b in notes:
    d.text((1450, y), s, font=font(26 if b else 23, b), fill=(30, 30, 30) if b else (60, 60, 60)); y += 38 if b else 33
lg = Image.open(P('LOGO')).convert('RGBA'); lg = lg.resize((130, int(130 * lg.height / lg.width)), Image.LANCZOS)
sheet.paste(lg, (W - 170, H - 40 - lg.height), lg)
d.text((1450, H - 50), 'Test render, not for publication · ring photo © DICTO · 2026-10-31', font=font(21), fill=(110, 110, 110))
for x0, y0_, w_, h_ in ((40, y0 + 40, 700, 700), (760, y0 + 40, 700, 700), (1480, y0 + 40, t.width, t.height), (40, y1 + 40, h.width, h.height)):
    d.rectangle([x0 - 1, y0_ - 1, x0 + w_, y0_ + h_], outline=(205, 202, 194))
sheet.save(os.path.join(OUT, 'ring-photo-test.png')); print('sheet saved', sheet.size)
