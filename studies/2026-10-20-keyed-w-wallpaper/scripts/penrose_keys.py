# Keyed W, Penrose reading (DICTO 10-24, restated): the keys on W's flat faces form a Penrose pattern at the OG's own edge length,
# centred on the socket (OG centre A) and running unbroken across the join into the neighbouring W (the two faces opened like a book
# about the edge A-E). A = Penrose rhombs (P3), B = kites and darts (P2). Robinson-triangle subdivision; 2D pictures for DICTO's pick.
import json, math, os, cmath, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, '..', 'data', 'step1-ocd-exact.json')))
num = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
V = np.array([[num(c) for c in v] for v in D['V']]); F = D['faces']; R = num(D['R']) if isinstance(D['R'], str) else 2 * (1 + 5 ** .5) / 6
u = np.array([0, 1, 0.]); w = np.array([1, 0, 1.]) / 2 ** .5; n = np.array([1, 0, -1.]) / 2 ** .5
A, E, T = np.zeros(3), np.array([0, R, 0]), np.array([R / 2, R / 2, R / 2])
tri = np.array([[x @ u, x @ w] for x in (A, E, T)]); tri2 = tri * np.array([1, -1])         # this W's face and the neighbour's, opened about A-E
cr = []
for f in F:
    for i in range(len(f)):
        a, b = V[f[i]], V[f[(i + 1) % len(f)]]; ha, hb = a @ n, b @ n
        if ha * hb < 0: x = a + ha / (ha - hb) * (b - a); cr.append([x @ u, x @ w])
cr = np.unique(np.round(np.array(cr), 9), axis=0); c0 = cr.mean(0); cr = cr[np.argsort(np.arctan2(cr[:, 1] - c0[1], cr[:, 0] - c0[0]))]
EDGE = float(np.sqrt(min(num(s) if isinstance(s, str) else s for s in [0]) or 0)) if False else None
# OG edge lengths from the faces (kite long side = hexagon side)
el = sorted({round(float(np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]])), 6) for f in F for i in range(len(f))})
L = max(float(np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]])) for f in F if len(f) == 6 for i in range(6)); phi = (1 + 5 ** .5) / 2   # the OG edge = hexagon side = kite long side
print('face triangle', tri.round(4).tolist(), '| socket rim corners', len(cr), '| OG edges', el, '-> Penrose edge', L)
def subdivide(tris, kind):
    out = []
    for c, a, b, cc in tris:
        if kind == 'P3':
            if c == 0: p = a + (b - a) / phi; out += [(0, cc, p, b), (1, p, cc, a)]
            else:
                q = b + (a - b) / phi; r = b + (cc - b) / phi
                out += [(1, r, cc, a), (1, q, r, b), (0, r, q, a)]
        else:   # P2 kites and darts (Robinson half-kites c=0, half-darts c=1)
            if c == 0:
                q = a + (b - a) / phi; r = b + (cc - b) / phi
                out += [(1, r, q, b), (0, q, a, r), (0, cc, a, r)]
            else:
                p = cc + (a - cc) / phi; out += [(1, b, p, a), (0, p, cc, b)]
    return out
def tiling(kind, levels=7, radius=1.6):
    tris = []
    for i in range(10):     # a sun (P2) / wheel (P3) of 10 triangles round the origin
        b = cmath.rect(radius, (2 * i - 1) * math.pi / 10); c = cmath.rect(radius, (2 * i + 1) * math.pi / 10)
        if i % 2 == 0: b, c = c, b
        tris.append((0, 0j, b, c))
    for _ in range(levels): tris = subdivide(tris, kind)
    return tris
def merge_pairs(tris):      # draw each Robinson triangle; the long dividing edges are left undrawn so the pairs read as rhombs/kites/darts
    return tris
S = 900; PAD = 60
pts = np.vstack([tri, tri2]); lo, hi = pts.min(0), pts.max(0); sc = (S - 2 * PAD) / max(hi - lo)
P = lambda z: (PAD + (z.real - lo[0]) * sc, S - PAD - (z.imag - lo[1]) * sc) if isinstance(z, complex) else (PAD + (z[0] - lo[0]) * sc, S - PAD - (z[1] - lo[1]) * sc)
def inside_tri(z, T3):
    x, y = z.real, z.imag; s = []
    for i in range(3):
        (x1, y1), (x2, y2) = T3[i], T3[(i + 1) % 3]; s.append((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1))
    return all(v >= 0 for v in s) or all(v <= 0 for v in s)
def in_poly(z, poly):
    x, y = z.real, z.imag; c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
F1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26); F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
def draw(kind, title, sub, path, levels, scale):
    radius = L * scale * phi ** levels; tris = tiling(kind, levels, radius)
    im = Image.new('RGB', (S, S + 70), (246, 244, 239)); d = ImageDraw.Draw(im, 'RGBA')
    layer = Image.new('RGBA', (S, S + 70), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
    gold = {0: (217, 169, 60, 255), 1: (239, 208, 138, 255)}
    for c, a, b, cc in tris:
        poly = [P(a), P(b), P(cc)]; dl.polygon(poly, fill=gold[c])
        dl.line([P(a), P(b)], fill=(43, 52, 69, 255), width=2); dl.line([P(cc), P(a)], fill=(43, 52, 69, 255), width=2)
    mask = Image.new('L', (S, S + 70), 0); dm = ImageDraw.Draw(mask)
    for T3 in (tri, tri2): dm.polygon([P(q) for q in T3], fill=255)
    for poly in (cr, cr * np.array([1, -1])): dm.polygon([P(q) for q in poly], fill=0)     # keys only on the flat face, not in the socket
    im.paste(layer, (0, 0), Image.fromarray((np.array(mask) * (np.array(layer)[:, :, 3] > 0)).astype('uint8')))
    for poly in (cr, cr * np.array([1, -1])):
        clip = Image.new('L', (S, S + 70), 0); ImageDraw.Draw(clip).polygon([P(q) for q in poly], fill=255)
        tm = Image.new('L', (S, S + 70), 0); [ImageDraw.Draw(tm).polygon([P(q) for q in T3], fill=255) for T3 in (tri, tri2)]
        blue = Image.new('RGBA', (S, S + 70), (157, 183, 220, 255)); im.paste(blue, (0, 0), Image.fromarray((np.array(clip) & np.array(tm)).astype('uint8')))
    for T3 in (tri, tri2): d.line([P(q) for q in list(T3) + [T3[0]]], fill=(31, 36, 48), width=3)
    d.line([P(tri[0]), P(tri[1])], fill=(200, 60, 60), width=3)
    d.text((PAD, 14), title, font=F1, fill=(31, 36, 48)); d.text((PAD, 48), sub, font=F2, fill=(107, 114, 128))
    d.text((PAD, S + 10), 'blue = the OG socket; red = the join: this W above, its neighbour below (opened like a book)', font=F2, fill=(107, 114, 128))
    d.text((S - 90, S + 38), 'DICTO', font=F1, fill=(150, 150, 150)); im.save(path); print('saved', path)
OUT = os.path.join(HERE, '..', 'renders')
draw('P3', 'A: Penrose rhombs', 'fat and thin rhombs, edge = OG edge / φ, centred on the socket, one pattern across the join', os.path.join(OUT, 'keyed-w-penrose-A.png'), 7, 1 / phi)
draw('P2', 'B: Penrose kites and darts', 'kites and darts, long edge = OG edge / φ, centred on the socket, one pattern across the join', os.path.join(OUT, 'keyed-w-penrose-B.png'), 7, 1 / phi)
