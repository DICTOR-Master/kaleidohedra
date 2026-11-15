# flat_karma_render.py (15 Nov 2026; DICTO: "fig 6.7 too big for fig frame again" -> every figure checked for models cut by the frame):
# #106 Figure 3 / Platonic book ch 9 "the flat Karma layer", re-rendered so the whole model sits inside the frame on a plain ground.
# Scene (exact, from studies/2026-11-10-di-bridge/octet_on_cleo.py): world 1 (cubic grid phi, dodecahedra of edge 1 on alternating
# cubes); the plane n.x = phi/(2 sqrt3), n = (1,1,1)/sqrt3. The violet dodecahedron centred at (0,-phi,-phi) has its top corner
# A = (phi/2)(1,-1,-1); the CLEO = apex A + base of the three dodecahedron corners one edge from A inside the Dogstar cube centred
# at (phi,0,0) (base edges 1/phi, in the plane); the octahedron (edge phi/sqrt2, axis-parallel) with its bottom face centred on the
# CLEO base, and Pacioli's icosahedron in it (edge 1/phi, mirror form cyclic(0, +-phi, +-1)/(2 phi)), its face on the CLEO base.
# Controls (printed): base edges, plane level, icosahedron edge, face-to-face distance 0, every corner inside the frame with margin.
# Render standard: solid faces, crisp antialiased edges (3x supersampling), no haze; plain white ground; DICTO mark.
# Usage: python3 flat_karma_render.py <out.png> [width_px]
import sys, itertools, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
OUT = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
f = (1 + 5 ** 0.5) / 2
def cyc(p): return [tuple(p), (p[2], p[0], p[1]), (p[1], p[2], p[0])]
def signs(p): return list({tuple(a * b for a, b in zip(s, p)) for s in itertools.product([1, -1], repeat=3)})
def uniq(pts): return [np.array(v) for v in {tuple(np.round(v, 12)): v for v in pts}.values()]
DOD = uniq([np.array(v) for v in signs((f / 2, f / 2, f / 2))] + [np.array(q) for p in signs((0, 0.5, f * f / 2)) for q in cyc(p)])
n = np.ones(3) / 3 ** .5; c = f / (2 * 3 ** .5); h = f / 2
ok = True
Dc = np.array([0., -f, -f]); dod = [Dc + v for v in DOD]
A = f / 2 * np.array([1., -1, -1]); cub = np.array([f, 0., 0])
ok &= any(np.linalg.norm(v - A) < 1e-9 for v in dod) and abs(max(v @ n for v in dod) - A @ n) < 1e-9
grid = uniq([v + f * np.array(p) for p in itertools.product(range(-1, 3), repeat=3) if sum(p) % 2 == 0 for v in DOD])
base = [v for v in grid if abs(np.linalg.norm(v - A) - 1) < 1e-9 and np.all(np.abs(v - cub) <= h + 1e-9)]
be = [np.linalg.norm(p - q) for p, q in itertools.combinations(base, 2)]
ok &= len(base) == 3 and all(abs(x - 1 / f) < 1e-9 for x in be) and all(abs(v @ n - c) < 1e-9 for v in base)
print('CLEO base corners', len(base), 'edges', np.round(be, 9), 'levels', np.round([v @ n for v in base], 9), 'plane', round(c, 9))
cleo = [A] + base
B = sum(base) / 3; O = B + f / 6 * np.ones(3)
octa = [O + s * h * e for e in np.eye(3) for s in (1, -1)]
ico = uniq([O + np.array(w) * np.array(sg) / (2 * f) for w in cyc((0, f, 1)) for sg in itertools.product((1, -1), repeat=3)])
ied = min(np.linalg.norm(p - q) for p, q in itertools.combinations(ico, 2))
d = max(min(np.linalg.norm(q - b) for q in ico) for b in base)
ok &= len(ico) == 12 and abs(ied - 1 / f) < 1e-9 and d < 1e-9
print('icosahedron corners', len(ico), 'edge', round(ied, 9), '| face-to-face: max distance CLEO base corner -> icosahedron corner', f'{d:.1e}')
def faces(pts):
    P = np.array(pts); hl = ConvexHull(P); groups = {}
    for simp, eq in zip(hl.simplices, hl.equations): groups.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    out = []
    for key, idx in groups.items():
        nn = np.array(key[:3]); idx = list(idx); cc = P[idx].mean(0); u = P[idx[0]] - cc; u /= np.linalg.norm(u); v = np.cross(nn, u)
        idx.sort(key=lambda i: np.arctan2((P[i] - cc) @ v, (P[i] - cc) @ u)); out.append((nn, [P[i] for i in idx]))
    return out
# view: n straight up on the page, looking slightly down onto the stack
up = n; side = np.cross(np.array([0., 0, 1]), up); side /= np.linalg.norm(side); fwd = np.cross(up, side)
def rot(axis, a):
    axis = axis / np.linalg.norm(axis); K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
M = rot(up, np.radians(20)); side, fwd = M @ side, M @ fwd
T = rot(side, np.radians(-30)); up2, fwd2 = T @ up, T @ fwd             # tilt: camera above, looking down 30 degrees
R = np.array([side, up2, -fwd2])                                         # rows: screen x, screen y, depth toward viewer
allp = np.array([R @ p for p in dod + cleo + octa + ico])
x0, x1 = allp[:, 0].min(), allp[:, 0].max(); y0, y1 = allp[:, 1].min(), allp[:, 1].max()
MARG = 0.08
scale = W * (1 - 2 * MARG) / (x1 - x0); H = int((y1 - y0) * scale + 2 * MARG * W)
SS = 3; cx = W / 2 - (x0 + x1) / 2 * scale; cy = H / 2 + (y0 + y1) / 2 * scale
def proj(p): q = R @ p; return ((cx + q[0] * scale) * SS, (cy - q[1] * scale) * SS)
inside = all(MARG * W * 0.99 <= (cx + q[0] * scale) <= W - MARG * W * 0.99 and MARG * W * 0.99 <= (cy - q[1] * scale) <= H - MARG * W * 0.99 for q in allp)
ok &= inside; print('every corner inside the frame with', int(MARG * 100), '% margin:', inside, '| size', W, 'x', H)
img = Image.new('RGBA', (W * SS, H * SS), (255, 255, 255, 255))
L = np.array([-0.35, 0.8, 0.5]); L /= np.linalg.norm(L)
def shade(nv, rgb, lo=0.6): k = lo + (1 - lo) * max(0.0, nv @ L); return tuple(int(min(255, cc * k + 20 * max(0, nv @ L) ** 8)) for cc in rgb)
EW = max(2, W // 400) * SS; EDGE = (40, 34, 30, 255)
def solid(img, pts, rgb):
    dd = ImageDraw.Draw(img)
    for nv, poly in faces(pts):
        if (R @ nv)[2] > 0: dd.polygon([proj(p) for p in poly], fill=shade(R @ nv, rgb) + (255,), outline=EDGE, width=EW)
    return img
def glass(img, pts, front):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    for nv, poly in faces(pts):
        if ((R @ nv)[2] > 0) == front:
            dd.polygon([proj(p) for p in poly], fill=(232, 200, 82, 40 if front else 60), outline=(150, 128, 50, 255), width=max(1, EW // (1 if front else 2)))
    return Image.alpha_composite(img, lay)
img = solid(img, dod, (138, 92, 196))          # D violet (element colours)
img = solid(img, cleo, (196, 120, 92))         # CLEO
img = glass(img, octa, False)                  # octahedron (O yellow) as glass: back
img = solid(img, ico, (58, 112, 205))          # I blue
img = glass(img, octa, True)                   # octahedron: front
img = img.convert('RGB').resize((W, H), Image.LANCZOS)
dd = ImageDraw.Draw(img)
try: font = ImageFont.truetype('DejaVuSans.ttf', max(12, W // 70))
except Exception: font = ImageFont.load_default()
txt = 'DICTO · dictospheres.com'; tw = dd.textlength(txt, font=font)
dd.text((W - tw - W * 0.015, H - W * 0.015 - font.size), txt, fill=(150, 130, 60), font=font)
img.save(OUT, dpi=(300, 300)); print('saved', OUT, img.size)
print('FINAL ok' if ok else 'FINAL FAIL: a geometry or frame control failed')
