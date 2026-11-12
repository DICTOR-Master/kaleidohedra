# cover_render.py (13 Nov 2026; DICTO chose the skins row of #106 Figure 1 as the cover of the Platonic book): the five Platonic
# solids at their one-world sizes, each inside a glass dodecahedral cell of edge 1, in D·I·C·T·O order left to right, element colours
# (DICTO square 10-22), house render standard: solid faces, crisp antialiased edges (3x supersampling), no haze.
# Sizes (#106 Table 1): D edge 1 (its own cell); I edge 1 (sphere-unit, Pacioli's position in the octahedron on the roof ridges);
# C edge phi (Euclid's cube); T edge phi*sqrt2 (on alternate corners of Euclid's cube); O edge phi^2/sqrt2 (corners at the midpoints
# of the six roof ridges). Controls: every solid's edges have their stated length and every corner lies inside the cell (printed).
# Usage: python3 cover_render.py <out.png> [width_px]
import sys, itertools, numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
OUT = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 7200
f = (1 + 5 ** 0.5) / 2
def cyc(p): return [p, (p[1], p[2], p[0]), (p[2], p[0], p[1])]
def signs(p):
    out = set()
    for s in itertools.product([1, -1], repeat=3): out.add(tuple(a * b for a, b in zip(s, p)))
    return list(out)
dod = [np.array(v) for v in signs((f / 2, f / 2, f / 2))] + [np.array(q) for p in signs((0, 0.5, f * f / 2)) for q in cyc(p)]
dod = list({tuple(np.round(v, 12)): v for v in dod}.values())
cube = [np.array(v) for v in signs((f / 2, f / 2, f / 2))]
tet = [v for v in cube if v[0] * v[1] * v[2] > 0]
octa = [np.array(q) for p in [(0, 0, f * f / 2), (0, 0, -f * f / 2)] for q in cyc(p)]
ico = [np.array(q) for p in signs((0, 0.5, f / 2)) for q in cyc(p)]
ico = list({tuple(np.round(v, 12)): v for v in ico}.values())
SOL = [('D', dod, 1.0, (138, 92, 196)), ('I', ico, 1.0, (58, 112, 205)), ('C', cube, f, (72, 142, 72)),
       ('T', tet, f * 2 ** 0.5, (205, 62, 40)), ('O', octa, f * f / 2 ** 0.5, (232, 200, 82))]
def faces(pts):
    P = np.array(pts); h = ConvexHull(P); groups = {}
    for simp, eq in zip(h.simplices, h.equations):
        key = tuple(np.round(eq, 6)); groups.setdefault(key, set()).update(simp)
    out = []
    for key, idx in groups.items():
        n = np.array(key[:3]); idx = list(idx); c = P[idx].mean(0)
        u = P[idx[0]] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((P[i] - c) @ v, (P[i] - c) @ u)); out.append((n, [P[i] for i in idx]))
    return out
ok = True
dmin = lambda pts: min(np.linalg.norm(a - b) for a, b in itertools.combinations(pts, 2))
for name, pts, e, _ in SOL:
    good = abs(dmin(pts) - e) < 1e-9
    inside = all(all(fn[0] @ p <= fn[0] @ fn[1][0] + 1e-5 for fn in faces(dod)) for p in pts)
    print(name, 'corners', len(pts), 'edge', round(dmin(pts), 12), 'expected', round(e, 12), 'inside cell', inside); ok &= good and inside
print('PROGRESS 0.2 geometry checked', flush=True)
def rot(ax, a):
    c, s = np.cos(a), np.sin(a); i, j = [(1, 2), (0, 2), (0, 1)][ax]; R = np.eye(3); R[i, i] = R[j, j] = c; R[i, j] = -s; R[j, i] = s; return R
R = rot(0, np.radians(-18)) @ rot(1, np.radians(24)) @ rot(2, np.radians(8))
SS = 3; cellW = W // 5; H = int(cellW * 1.0); scale = cellW * 0.31
img = Image.new('RGBA', (W * SS, H * SS), (255, 255, 255, 255))
L = np.array([-0.45, 0.65, 0.62]); L /= np.linalg.norm(L)
def shade(n, rgb, lo=0.62):
    k = lo + (1 - lo) * max(0.0, n @ L); return tuple(int(min(255, c * k + 20 * max(0, n @ L) ** 8)) for c in rgb)
def proj(p, cx):
    q = R @ p; return ((cx + q[0] * scale) * SS, (H / 2 - q[1] * scale) * SS), q[2]
EW = max(2, int(cellW / 260)) * SS
for k, (name, pts, e, rgb) in enumerate(SOL):
    cx = cellW * (k + 0.5)
    glass = [] if name == 'D' else faces(dod)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for n, poly in glass:                               # back of the glass cell: faint fill, thin edges
        if (R @ n)[2] < 0: d.polygon([proj(p, cx)[0] for p in poly], fill=(214, 220, 228, 90), outline=(150, 156, 166, 255), width=max(1, EW // 2))
    img = Image.alpha_composite(img, lay); d = ImageDraw.Draw(img)
    for n, poly in faces(pts):                          # the solid, opaque, visible faces only
        if (R @ n)[2] > 0: d.polygon([proj(p, cx)[0] for p in poly], fill=shade(R @ n, rgb) + (255,), outline=(40, 34, 30, 255), width=EW)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for n, poly in glass:                               # front of the glass cell: clear glass, crisp edges
        if (R @ n)[2] > 0: d.polygon([proj(p, cx)[0] for p in poly], fill=(232, 238, 246, 46), outline=(110, 116, 128, 255), width=EW)
    img = Image.alpha_composite(img, lay)
    print(f'PROGRESS {0.2 + 0.15 * (k + 1):.2f} {name} drawn', flush=True)
img = img.convert('RGB').resize((W, H), Image.LANCZOS); img.save(OUT, dpi=(600, 600))
print('saved', OUT, img.size)
print('FINAL ok' if ok else 'FINAL FAIL: a geometry control failed')
