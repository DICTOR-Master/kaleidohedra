# DICTO 2026-10-19: composes the octet paper's figures from the clean renders (shoot_clean.mjs) -> ../figures/*.jpg
# usage: python3 make_figs.py <renders folder>
import sys, os
from PIL import Image, ImageDraw, ImageFont
D = sys.argv[1]; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures'); os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'
f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
BG, INK, MUTE = (244, 241, 234), (43, 38, 32), (109, 101, 86)
figs = {
  'golden-key': [('p1set', 'The set', 'keyed octahedron, tetrahedron L/R'), ('p1round', 'Round one octahedron', '8 dented tetrahedra'), ('p1net', 'Network', 'the octet truss filled')],
  'stars': [('stars', 'Facing five-fold stars', 'seen down the five-fold axis'), ('penrose', 'The Penrose link', 'thick rhombus + two φ-smaller ones')],
  'penrose-core': [('p2set', 'The set', 'notched octahedron, middle piece, tetrahedron L/R'), ('p2round', 'Round one octahedron', '12 middle pieces, 8 tetrahedra'), ('k3', 'Keyless, three Penrose cores', 'DICTO\'s choice')],
  'envelope': [('p3two', 'Two shapes', 'envelope (OG inside) + grown piece L/R'), ('p4two', 'Envelope + adaptor half', 'the adaptor opens in two halves'), ('p4inside', 'One piece', 'rhombic dodecahedra, envelopes inside (glass)')],
  'glue': [('p4envW', 'Envelope + W', 'W round an octet vertex'), ('p4ocdWset', 'OG + W with OG imprints', 'two shapes, no mirror pair'), ('p4starWset', 'OG + W on the Penrose star', 'two shapes, no mirror pair')],
  'keyed-w': [('kWone', 'Keyed W', 'one kite key per flat face'), ('kWpair', 'Bump meets dent', 'neighbours pulled apart'), ('kWring', '12 round one OG', 'none can slide out')],
  'chamber': [('p4chamber', 'Chamber, cut open', 'envelopes exposed outside and inside')],
}
for name, panels in figs.items():
    n = len(panels); S = 900; gap = 40; W = n * S + (n - 1) * gap + 80; H = S + 190
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    for i, (k, t, sub) in enumerate(panels):
        p = Image.open(f'{D}/{k}.png').convert('RGB'); p.thumbnail((S, S), Image.LANCZOS)
        x = 40 + i * (S + gap); im.paste(p, (x + (S - p.width) // 2, 20 + (S - p.height) // 2))
        for txt, y, fo, col in [(t, S + 50, f(44, True), INK), (sub, S + 112, f(34), MUTE)]:
            d.text((x + S / 2 - d.textlength(txt, font=fo) / 2, y), txt, font=fo, fill=col)
    m = 'DICTO · dictospheres.com'; d.text((W - 40 - d.textlength(m, font=f(26)), H - 40), m, font=f(26), fill=MUTE)
    im.save(f'{OUT}/{name}.jpg', quality=88); print(name, im.size)
