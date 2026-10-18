# DICTO 2026-10-19: composes the #36 Golden Bodhi Pyrochlore cover (dictospheres.com card) from the shoot_cover.mjs renders
# (piece, six, net from render_cover.html; gbpc from studies/2026-10-16-ocd-pyrochlore render_adapter.html?mode=cell).
# usage: python3 cover_card.py <shots folder> <out.jpg>   (house style as studies/2026-10-16-progenitors/scripts/cleo_figure.py)
import sys
from PIL import Image, ImageDraw, ImageFont
D, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'
f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
BG, INK, MUTE = (244, 241, 234), (43, 38, 32), (109, 101, 86)
W, Hh = 2880, 2160
im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
d.text((90, 70), 'Golden Bodhi Pyrochlore', font=f(84, True), fill=INK)
d.text((92, 182), "The gap of the DICTO Ogdoecontahedron's bcc packing, 22.57% of space, exact in ℚ(√5)", font=f(40), fill=MUTE)
def centred(t, x, y, font, fill):
    d.text((x - d.textlength(t, font=font) / 2, y), t, font=font, fill=fill)
panels = [('piece', "DICTO's Bull-horns OG adaptor", ['the resin between six OGs, one piece', 'one solid, centrally symmetric, with a mirror plane']),
          ('six2', 'Between its six OGs', ['a narrow pair across the slab, a wide ring of four', 'yellow and blue: the two networks (as glass)']),
          ('net', 'The double network, filled', ['three adaptors per OG,', 'nothing left over'])]
S = 880
for i, (k, t, sub) in enumerate(panels):
    x = 90 + i * (S + 25)
    im.paste(Image.open(f'{D}/{k}.png').convert('RGB').resize((S, S), Image.LANCZOS), (x, 290))
    centred(t, x + S / 2, 1200, f(46, True), INK)
    for j, s in enumerate(sub): centred(s, x + S / 2, 1268 + 44 * j, f(32), MUTE)
G = 560
im.paste(Image.open(f'{D}/gbpc.png').convert('RGB').resize((G, G), Image.LANCZOS), (90, 1420))
tx = 90 + G + 60
d.text((tx, 1490), 'The GBPC (Golden Bodhi Pyrochlore Corner)', font=f(46, True), fill=INK)
for j, s in enumerate(['the one adapter every golden fill of the gap needs:',
                       '24 on one cell (lilac), overlapping nothing']): d.text((tx, 1564 + 46 * j), s, font=f(34), fill=MUTE)
d.text((tx, 1730), 'Exact', font=f(40, True), fill=INK)
for j, s in enumerate(['OGs (9225 − 3915√5)/608 ≈ 77.4332% of space,',
                       'adaptors (−8617 + 3915√5)/608 ≈ 22.5668%;',
                       'one adaptor (18728 − 6296√5)/41553 ≈ 0.111898.']): d.text((tx, 1792 + 46 * j), s, font=f(34), fill=MUTE)
t = 'DICTO · dictospheres.com'; d.text((W - 90 - d.textlength(t, font=f(34)), Hh - 90), t, font=f(34), fill=MUTE)
im.resize((1440, 1080), Image.LANCZOS).save(OUT, quality=90); print(OUT)
