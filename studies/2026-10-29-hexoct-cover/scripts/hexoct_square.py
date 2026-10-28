# The HexOct square (DICTO 2026-10-29): book cover for "HexOct: The Laws of Stacking", after the DICTO square, 6 x 6.
# Cyclic Latin square: row i, column j holds letter (i+j) mod 6 of HEXOCT, so HEXOCT reads across the top and down the left,
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
                col = tuple(int(c * b) for c in TONE[kind])
                V = Q @ VIEW.T
                pts = [(cx + (v[0] - mid[0]) * sc, cy - (v[1] - mid[1]) * sc) for v in V]
                dr.polygon(pts, fill=col); dr.line(pts + [pts[0]], fill=EDGE, width=2 * SS)
# Trajan-style initials V-cut and gilded with platinum leaf, as in the DICTO square
f = ImageFont.truetype('Cinzel.ttf', int(0.074 * W)); f.set_variation_by_name('Bold')
Lc = np.array([-0.55, 0.6, 0.58]); Lc /= np.linalg.norm(Lc)
def carved(ch):
    box = int(0.12 * W); m = Image.new('L', (box, box), 0); ImageDraw.Draw(m).text((box / 2, box / 2), ch, font=f, fill=255, anchor='mm')
    Mk = np.array(m) / 255.0; ins = Mk > 0.5
    dist = ndimage.gaussian_filter(ndimage.distance_transform_edt(ins), 0.8); gy, gx = np.gradient(dist); k = 1.6
    nrm = np.dstack([gx * k, -gy * k, np.ones_like(dist)]); nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
    lamb = np.clip(nrm @ Lc, 0, 1); h = np.clip(nrm @ (Lc + [0, 0, 1.0]) / np.linalg.norm(Lc + [0, 0, 1.0]), 0, 1) ** 40
    dark = np.array([70, 74, 82.]); lite = np.array([226, 229, 235.]); rgb = dark + (lite - dark) * lamb[..., None] ** 1.3
    rgb = rgb + (255 - rgb) * h[..., None] * 0.8
    sh = ndimage.shift(ins.astype(float), (-2 * SS * 0.6, 2 * SS * 0.6), order=1); rgb *= (1 - 0.35 * np.clip(ins - sh, 0, 1))[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), Image.fromarray((ndimage.gaussian_filter(Mk, 0.6) * 255).astype(np.uint8)), box
CARVE = {ch: carved(ch) for ch in WORD}
for i in range(6):
    for j in range(6):
        t, m, box = CARVE[M[i][j]]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        img.paste(t, (int(cx - box / 2), int(cy - box / 2)), m)
img = img.resize((N, N), Image.LANCZOS); img.save('hexoct-square.png'); print('ok')
