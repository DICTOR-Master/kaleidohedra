# DICTO 2026-10-19: the two 2D panels (facing five-fold stars; the Penrose link) drawn from the exact-derived data of
# studies/2026-10-18-ocd-octet (step4-stars.json, step13-penrose.json), seen down the five-fold axis -> <out>/stars.png, penrose.png
import sys, json, math, os
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1]; H = os.path.dirname(os.path.abspath(__file__)); DD = os.path.join(H, '..', '..', '..', 'studies', '2026-10-18-ocd-octet', 'data')
st = json.load(open(f'{DD}/step4-stars.json')); pe = json.load(open(f'{DD}/step13-penrose.json'))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
BG, INK = (244, 241, 234), (43, 38, 32); GOLD, BLUE, RED, PURP = (226, 182, 82), (122, 170, 232), (214, 84, 60), (150, 104, 190)
SS = 3; N = 1000 * SS; sc = N / 1.2; cx = -0.175
P = lambda p: (N / 2 + (p[0] - cx) * sc, N / 2 - p[1] * sc)
def panel(name, link):
    im = Image.new('RGB', (N, N), BG); d = ImageDraw.Draw(im, 'RGBA')
    for ks, col in [(st['kites1'], GOLD), (st['kites2'], BLUE)]:
        for k in ks: d.polygon([P(q) for q in k], fill=col + ((110,) if link else (215,)), outline=(40, 34, 28, 255), width=2 * SS)
    c1, c2 = st['c1'], st['c2']
    if not link:
        r = math.dist(c1, c2) * sc; x, y = P(c1)
        for a in range(0, 360, 6): d.arc([x - r, y - r, x + r, y + r], a, a + 3, fill=(90, 84, 74, 255), width=2 * SS)
        d.line([P(c1), P(c2)], fill=(40, 34, 28, 255), width=3 * SS)
        m = P(((c1[0] + c2[0]) / 2, 0.02)); t = '0.3505'; d.text((m[0] - d.textlength(t, font=f(30 * SS)) / 2, m[1] - 40 * SS), t, font=f(30 * SS), fill=INK)
    else:
        for k, col in [('flank1', PURP), ('flank2', PURP), ('central', RED)]:
            d.polygon([P(q) for q in pe['patch'][k]], fill=col + (225,), outline=(30, 24, 20, 255), width=3 * SS)
        m = P((-0.1752, 0)); t = '72°'; d.text((m[0] + 70 * SS, m[1] - 18 * SS), t, font=f(30 * SS, True), fill=(255, 255, 255))
    for c, lab, dx in [(c1, 'c1', 18), (c2, 'c2', -60)]:
        x, y = P(c); d.ellipse([x - 9 * SS, y - 9 * SS, x + 9 * SS, y + 9 * SS], fill=INK); d.text((x + dx * SS, y + 14 * SS), lab, font=f(30 * SS), fill=INK)
    im.resize((1000, 1000), Image.LANCZOS).save(f'{OUT}/{name}.png'); print(name)
panel('stars', False); panel('penrose', True)
