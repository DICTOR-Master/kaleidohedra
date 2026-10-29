# The HexOct square (DICTO 2026-10-29): book cover for "HexOct: The Laws of Stacking", after the DICTO square, 6 x 6.
# Letters as a slanted LED display; tiles matching their letter in teal (DICTO). Cyclic Latin square: row i, column j holds letter (i+j) mod 6 of HEXOCT, so HEXOCT reads across the top and down the left,
# every letter once in each row and column. Shapes: H, E, X on the h-tile, O, C, T on the c-tile (the two HexOct tiles of #75,
# at weight 1/10, built exactly by tiles.py). Pieces: tetrahedral gold, octahedral halves violet, as in #75.
import math, os, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
from tiles import tile
WORD = 'HEXOCT'; n6 = 6
M = [[WORD[(i + j) % n6] for j in range(n6)] for i in range(n6)]
assert M[0] == list(WORD) and [r[0] for r in M] == list(WORD)
assert all(len(set(r)) == 6 for r in M) and all(len({M[i][j] for i in range(6)}) == 6 for j in range(6))
SHAPE = {'H': 'h', 'E': 'h', 'X': 'h', 'O': 'c', 'C': 'c', 'T': 'c'}
lam = Fr(1, 10); D3 = (2 / 3) ** 0.5
def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * 3 ** 0.5 / 2, float(p[2]) * D3])
az, el = math.radians(-58), math.radians(14)
d = np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])   # towards the viewer
r = np.array([-math.sin(az), math.cos(az), 0.0]); u = np.cross(d, r)
VIEW = np.array([r, u, d])
def pieces(word, L):
    out = []
    for k, up, s, pts, J in tile(word, L, lam)[0]:
        P = np.array([cart(p) for p in pts]); h = ConvexHull(P); F = {}
        for sm, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
        faces = []
        for eq, idx in F.items():
            Q = P[list(idx)]; c = Q.mean(0); nn = np.array(eq[:3]); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(nn, a)
            faces.append((nn, Q[np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]))
        out.append(('tet' if k == 'tet' else ('octup' if up else 'octdn'), P, faces))
    return out
T = {'c': pieces('ABC', 1), 'h': pieces('AB', 0)}
ext = {}
for s, ps in T.items():
    A = np.vstack([P for _, P, _ in ps]) @ VIEW.T; ext[s] = (A[:, :2].min(0), A[:, :2].max(0))
span = max(float((hi - lo).max()) for lo, hi in ext.values())
GROUND = (20, 15, 11); EDGE = (60, 40, 18)
TONE = {'tet': (217, 165, 33), 'octup': (138, 92, 194), 'octdn': (180, 138, 224)}
MATCH = (43, 179, 163)   # DICTO 10-29: pick out the cells where the tile matches its letter (H on the h-tile, C on the c-tile)
N = 1800; SS = 2; W = N * SS; cell = 0.9 * W / 6; sc = 0.86 * cell / span; x0 = 0.05 * W
light = np.array([-0.4, 0.55, 0.75]); light /= np.linalg.norm(light)
img = Image.new('RGB', (W, W), GROUND); dr = ImageDraw.Draw(img)
for i in range(6):
    for j in range(6):
        s = SHAPE[M[i][j]]; lo, hi = ext[s]; mid = (lo + hi) / 2
        cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        for kind, P, F in sorted(T[s], key=lambda t: (t[1] @ d).mean()):
            for nn, Q in sorted(F, key=lambda f: (f[1] @ d).mean()):
                if nn @ d <= 1e-9: continue
                b = 0.45 + 0.55 * max(0, (nn @ VIEW.T) @ light)
                col = tuple(int(c * b) for c in (MATCH if kind == 'tet' and M[i][j] in 'HC' else TONE[kind]))
                V = Q @ VIEW.T
                pts = [(cx + (v[0] - mid[0]) * sc, cy - (v[1] - mid[1]) * sc) for v in V]
                dr.polygon(pts, fill=col); dr.line(pts + [pts[0]], fill=EDGE, width=2 * SS)
# Letters as an LED display (DICTO 10-29: like his font Timer, DS-Digital and LED Real, "LED style script with stepped parts";
# earlier tries, Trajan, dot-matrix, Righteous and Baumans, dropped): DSEG14 Classic Italic (OFL, keshikan), a slanted
# 14-segment LED face. Lit segments glow cool white over a thin dark edge; unlit segments ('~' lights all 14) show faintly.
f = ImageFont.truetype(os.environ.get('LEDFONT', 'DSEG14Classic-Italic.ttf'), int(0.072 * W))
def carved(ch):
    box = int(0.13 * W); edge = int(0.0022 * W)
    def lay(t, sw=0):
        m = Image.new('L', (box, box), 0); ImageDraw.Draw(m).text((box / 2, box / 2), t, font=f, fill=255, anchor='mm', stroke_width=sw, stroke_fill=255)
        return np.array(m, float) / 255
    On, Rim, Ghost = lay(ch), lay(ch, edge), lay('~')
    glow = ndimage.gaussian_filter(On, 0.006 * W); glow /= glow.max()
    core = np.array([240, 252, 255.]); halo = np.array([140, 230, 255.]); dim = np.array([70, 62, 52.])
    rgb = (core * On[..., None] + halo * (1 - On[..., None])) * (On + 0.6 * glow)[..., None] / np.maximum(On + 0.6 * glow, 1e-6)[..., None]
    rgb = np.where((Rim - On)[..., None] > 0.3, np.array([8, 6, 4.]), rgb)
    rgb = np.where(((Ghost - Rim) > 0.5)[..., None], dim, rgb)
    alpha = np.clip(np.maximum.reduce([Rim, 0.5 * glow, 0.35 * Ghost]), 0, 1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), Image.fromarray((alpha * 255).astype(np.uint8)), (box, box)
CARVE = {ch: carved(ch) for ch in WORD}
for i in range(6):
    for j in range(6):
        t, m, (bw, bh) = CARVE[M[i][j]]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        img.paste(t, (int(cx - bw / 2), int(cy - bh / 2)), m)
img = img.resize((N, N), Image.LANCZOS); img.save(os.environ.get('OUT', 'hexoct-square.png')); print('ok')
