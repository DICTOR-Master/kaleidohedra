# Composes the Cleo star figure (paper Progenitors) from the render_cleo.html shots (shoot_cleo.mjs -> a folder of PNGs):
# usage: python3 scripts/cleo_figure.py <shots folder> <out.jpg>
import sys
from PIL import Image, ImageDraw, ImageFont
D, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'
f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
BG, INK, MUTE = (244, 241, 234), (43, 38, 32), (109, 101, 86)
W, Hh = 2460, 1560
im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
d.text((40, 30), 'The Cleo star build in the golden cycle', font=f(46, True), fill=INK)
d.text((40, 92), "I (20 Cleo-Icos) ⊂ Cleo star ⊂ D′ = (2/3)·D ⊂ ID ⊂ O ⊂ rTI ⊂ TI ⊂ H ⊂ hull ⊂ RT ⊂ M ⊂ I·φ³   (exact in ℚ(√5))", font=f(26), fill=MUTE)
panels = [('exploded', 'The build, pulled apart', ['20 Cleo-Icos (wisteria) · 20 Cleo spikes (cyan)', '12 inward pyramids (gold) · 30 valley tetrahedra (green)']),
          ('assembled', 'Assembled: 82 pieces fill D′', ["the spike tips are the corners of D′; pyramids and valleys", 'as glass, inside glass D′ and glass ID']),
          ('cycle', 'In the cycle', ['a slice removed: the build at the centre', 'of the outer shells'])]
for i, (k, t, sub) in enumerate(panels):
    p = Image.open(f'{D}/{k}.png').convert('RGB').resize((720, 720)); x = 40 + i * 800
    im.paste(p, (x, 150))
    tw = d.textlength(t, font=f(30, True)); d.text((x + 360 - tw / 2, 885), t, font=f(30, True), fill=INK)
    for j, s in enumerate(sub):
        sw = d.textlength(s, font=f(21)); d.text((x + 360 - sw / 2, 928 + 28 * j), s, font=f(21), fill=MUTE)
d.text((40, 1020), 'The twelve stations at true scale', font=f(30, True), fill=INK)
names = ['I', 'star', 'Dp', 'ID', 'O', 'rTI', 'TI', 'H', 'hull', 'RT', 'M', 'Ip3']; labels = ['I', 'Cleo star', 'D′', 'ID', 'O', 'rTI', 'TI', 'H', 'hull', 'RT', 'M', 'I·φ³']
for i, (n, l) in enumerate(zip(names, labels)):
    p = Image.open(f'{D}/one-{n}.png').convert('RGB').resize((196, 196)); x = 40 + i * 200
    im.paste(p, (x, 1080)); lw = d.textlength(l, font=f(24, True)); d.text((x + 98 - lw / 2, 1286), l, font=f(24, True), fill=INK)
d.text((40, 1370), "Exact: the 20 Cleo-Icos, 20 spikes, 12 inward pyramids and 30 valley tetrahedra (one shape) fill D′ with remainder 0; volumes: core and spikes", font=f(22), fill=MUTE)
d.text((40, 1402), "−5/12 + 5√5/12 each set, pyramids 5/9 − √5/27 in all, valleys 25/18 − 5√5/18 in all; D′ = 10/9 + 14√5/27.", font=f(22), fill=MUTE)
d.text((W - 300, Hh - 50), 'DICTO · dictospheres.com', font=f(22), fill=MUTE)
im.save(OUT, quality=88); print(OUT, im.size)
