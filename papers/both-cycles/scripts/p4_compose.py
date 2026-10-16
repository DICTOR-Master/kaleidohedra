# Compose the P4 three.js shots (shoot_p4.mjs on dicto-node -> /tmp/p4) into the paper figures: hero, peel, kit (+ locators).
# Counts, shapes and layers are read from data/interlock-kinds.txt and the S1 table (Tables 1-3), never typed in.
#   python3 scripts/p4_compose.py <shots dir> <view>  -> renders/p4-hero.png, p4-peel.png, p4-kit-ends.png, p4-kit-middle.png
import sys, re, collections, json
from PIL import Image, ImageDraw, ImageFont, ImageChops
src, view = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else 'A')
BG = (244, 241, 234); INK = (43, 38, 32); MUTE = (91, 83, 70)
F = lambda n, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', n)
def bbox(im, pad=12):
    bg = Image.new('RGB', im.size, im.getpixel((2, 2))); b = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 8 else 0).getbbox()
    return (max(b[0] - pad, 0), max(b[1] - pad, 0), min(b[2] + pad, im.width), min(b[3] + pad, im.height))
def ctext(d, x, y, s, f, fill=INK): d.text((x - d.textlength(s, font=f) / 2, y), s, font=f, fill=fill)
def tag(img, d): s = 'DICTO · dictospheres.com'; d.text((img.width - d.textlength(s, font=F(22)) - 18, img.height - 34), s, font=F(22), fill=MUTE)
TXT = open('data/interlock-kinds.txt').read()
def kinds(s):
    block = TXT.split(f'== {s} setting')[1].split('== ')[0]
    return re.findall(r'(\d+) x vol .*?\n\s+in original layer: (.*?) \(\d+\)\n.*?\n\s+(\d+) corners, (\d+) faces', block)
SHAPE = {'ends': '12f TBP 7f 7f 12f 7f QPy PPy PPy Tet QPy Tet'.split(), 'middle': '7f 11f 7f HPy 7f 6f Tet QPy Tet Tet Tet'.split()}
LAY = ['I → ID', 'ID → D', 'D → TI', 'TI → H', 'H → RT', 'RT → I·φ³']
SH = {'icosahedron': 'I', 'icosidodecahedron': 'ID', 'dodecahedron': 'D', 'truncated icosahedron': 'TI', 'Hecatodihedron': 'H', 'rhombic triacontahedron': 'RT', 'icosahedron (phi^3)': 'I·φ³'}
cnt = {s: collections.Counter(p['o'][0] for p in json.load(open(f'data/interlock-{s}.json'))['pieces']) for s in ('ends', 'middle')}
NS = {'ends': ('Ends setting', 'shares I and D', 536, '1 (Dharma-Ends)'), 'middle': ('Middle setting', 'shares ID and RT', 502, '2 (Dharma-Middle)')}

# hero: the two settings side by side, a slice removed
H = [Image.open(f'{src}/hero-{s}-{view}.png').convert('RGB') for s in ('ends', 'middle')]
H = [im.crop(bbox(im, 30)) for im in H]; h = max(im.height for im in H); w = sum(im.width for im in H) + 120
img = Image.new('RGB', (w, h + 190), BG); d = ImageDraw.Draw(img); x = 40
for im, s in zip(H, ('ends', 'middle')):
    img.paste(im, (x, 120)); t, sub, n, _ = NS[s]
    ctext(d, x + im.width / 2, 22, t, F(40, True)); ctext(d, x + im.width / 2, 74, f'{sub} · {n} pieces per turn', F(28), MUTE); x += im.width + 40
tag(img, d); img.save('renders/p4-hero.png'); print('hero', img.size)

# peel: each original layer alone, both settings
T = 380; img = Image.new('RGB', (230 + 6 * T, 120 + 2 * (T + 110) + 40), BG); d = ImageDraw.Draw(img)
for j, l in enumerate(LAY): ctext(d, 230 + j * T + T / 2, 30, l, F(30, True))
for i, s in enumerate(('ends', 'middle')):
    y0 = 100 + i * (T + 110); d.text((20, y0 + T / 2 - 40), NS[s][0].split()[0], font=F(32, True), fill=INK); d.text((20, y0 + T / 2 + 4), NS[s][1], font=F(22), fill=MUTE)
    for l in range(6):
        im = Image.open(f'{src}/layer-{s}-{l}.png').convert('RGB'); im = im.crop(bbox(im, 16)); f = (T - 30) / max(im.size)
        im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS); x0 = 230 + l * T
        img.paste(im, (int(x0 + (T - im.width) / 2), int(y0 + (T - im.height) / 2)))
        n = cnt[s][l]; whole = {'ends': [20, 20, 12, 20, 72, 30], 'middle': [20, 20, 12, 20, 72, 30]}[s][l] == n
        ctext(d, x0 + T / 2, y0 + T + 8, f'{n} pieces' + (' (whole)' if whole else ''), F(28, True) if whole else F(28), INK if whole else MUTE)
tag(img, d); img.save('renders/p4-peel.png'); print('peel', img.size)

# kit: one piece of each kind at one common scale (all tiles shot at the same half-width), with a locator
SCALE_PX = 700 / (2 * 2.0)                                     # pixels per unit in the kind shots (px 700, h 2.0)
for s in ('ends', 'middle'):
    K = kinds(s); n = len(K); cols = 4; rows = (n + cols - 1) // cols; TW, TH = 520, 570; crop = (90, 110, 610, 570)
    img = Image.new('RGB', (cols * TW, 120 + rows * TH + 80), BG); d = ImageDraw.Draw(img)
    d.text((24, 20), f'DICTO Interlock set {NS[s][3]}: {n} kinds, {NS[s][2]} pieces per turn', font=F(34, True), fill=INK)
    d.text((24, 66), 'One piece of each kind, all at one scale, outward direction up. Small view: where that kind sits.', font=F(24), fill=MUTE)
    for i, (c, ol, nc, nf) in enumerate(K):
        x0, y0 = (i % cols) * TW, 120 + (i // cols) * TH
        im = Image.open(f'{src}/kind-{s}-{i + 1}.png').convert('RGB').crop(crop); img.paste(im, (x0, y0))
        lo = Image.open(f'{src}/loc-{s}-{i + 1}.png').convert('RGB'); lo = lo.crop(bbox(lo, 6)); lo.thumbnail((150, 150), Image.LANCZOS)
        img.paste(lo, (x0 + TW - lo.width - 10, y0 + 6)); d.rectangle((x0 + TW - lo.width - 11, y0 + 5, x0 + TW - 9, y0 + 7 + lo.height), outline=(200, 191, 172))
        ctext(d, x0 + TW / 2, y0 + 468, f'I{1 if s == "ends" else 2}·{i + 1} ({SHAPE[s][i]})  ×{c}', F(30, True))
        a, b = ol.split(' -> '); ctext(d, x0 + TW / 2, y0 + 508, f'{SH[a]} → {SH[b]} · {nc} corners, {nf} faces', F(22), MUTE)
    yb = 120 + rows * TH + 30; L = int(SCALE_PX * 0.5); d.line((24, yb, 24 + L, yb), fill=INK, width=4)
    for xx in (24, 24 + L): d.line((xx, yb - 9, xx, yb + 9), fill=INK, width=3)
    d.text((34 + L, yb - 15), '0.5 (I has corner radius 0.588)', font=F(22), fill=MUTE)
    tag(img, d); img.save(f'renders/p4-kit-{s}.png'); print('kit', s, img.size)

# x-ray: Figure 2 (DICTO: "use an actual x-ray cut through, as in the app"), from render_p4_xray.html via shoot_p4_xray.mjs
import os
if os.path.exists(f'{src}/xray-ends.png'):
    X = [Image.open(f'{src}/xray-{s}.png').convert('RGB') for s in ('ends', 'middle')]
    X = [im.crop(bbox(im, 24)) for im in X]; h = max(im.height for im in X); w = sum(im.width for im in X) + 120
    img = Image.new('RGB', (w, h + 190), BG); d = ImageDraw.Draw(img); x = 40
    for im, s, rr in zip(X, ('ends', 'middle'), ('ρ² = φ²/4', 'ρ² = 3φ²/4')):
        img.paste(im, (x, 130)); t, sub, n, _ = NS[s]
        ctext(d, x + im.width / 2, 22, f'{t}, {rr}', F(40, True)); ctext(d, x + im.width / 2, 76, sub, F(28), MUTE); x += im.width + 40
    tag(img, d); img.save('renders/p4-xray.png'); print('xray', img.size)

# slice: Figure 2 final (DICTO: "same type as the hero pictures, sliced clean through the middle like the X-ray slice in the app, front on
# like tree rings"), from render_p4.html?mode=slice via shoot_p4_slice.mjs; labels at the anchors the page reports
if os.path.exists(f'{src}/slice-ends.png'):
    panels = []
    for s in ('ends', 'middle'):
        im = Image.open(f'{src}/slice-{s}.png').convert('RGB'); A = json.load(open(f'{src}/slice-{s}.json')); d = ImageDraw.Draw(im)
        for j, L in enumerate(sorted(A['labels'], key=lambda L: L['r'])):
            tx, ty = 1400 - 250, 120 + 70 * j; d.line((L['x'], L['y'], tx - 8, ty + 16), fill=INK, width=3); d.ellipse((L['x'] - 6, L['y'] - 6, L['x'] + 6, L['y'] + 6), fill=INK)
            d.text((tx, ty), f'shared {L["name"]}', font=F(32, True), fill=INK)
        r = A['rho']; tx, ty = 1400 - 420, 1400 - 90; d.line((r['x'], r['y'], tx + 60, ty), fill=(150, 120, 30), width=3)
        d.text((tx, ty), 'sphere of reciprocation', font=F(30), fill=(120, 95, 20))
        panels.append(im.crop(bbox(im, 20)))
    h = max(im.height for im in panels); w = sum(im.width for im in panels) + 120
    img = Image.new('RGB', (w, h + 170), BG); d = ImageDraw.Draw(img); x = 40
    for im, s, rr in zip(panels, ('ends', 'middle'), ('ρ² = φ²/4', 'ρ² = 3φ²/4')):
        img.paste(im, (x, 130)); t, sub, n, _ = NS[s]
        ctext(d, x + im.width / 2, 22, f'{t}, {rr}', F(40, True)); ctext(d, x + im.width / 2, 76, sub, F(28), MUTE); x += im.width + 40
    tag(img, d); img.save('renders/p4-slice.png'); print('slice', img.size)
