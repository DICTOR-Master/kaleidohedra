# The GOLDEN square (DICTO 2026-10-29: "do the cover in HexOct style"): cover for the book "The Golden Cycle", after the HexOct
# square. Cyclic Latin square: row i, column j holds letter (i+j) mod 6 of GOLDEN, so GOLDEN reads across the top and down the
# left, every letter once in each row and column. Each letter is one station of the inside-out golden cycle (Spheres of Dharma
# turned inside out, #32, chapter 6 of the book), in order: G dodecahedron, O icosidodecahedron, L DICTO Ogdoecontahedron,
# D pentakis dodecahedron (polar of the truncated icosahedron), E icosahedron, N rhombic triacontahedron; then the dodecahedron
# again, phi^3 larger. Six different solids, six colours (DICTO 10-29: no repeated solid or colour; "a different cycle of six").
# All drawn at one circumradius, one pose. Letters: the HexOct LED letters (DSEG14 Classic, OFL), white.
import math, os, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
WORD = 'GOLDEN'; n6 = 6
M = [[WORD[(i + j) % n6] for j in range(n6)] for i in range(n6)]
assert M[0] == list(WORD) and [r[0] for r in M] == list(WORD)
assert all(len(set(r)) == 6 for r in M) and all(len({M[i][j] for i in range(6)}) == 6 for j in range(6))
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v): return {tuple(s * x for s, x in zip(ss, v)) for ss in itertools.product((1, -1), repeat=3)}
def orbit(v): return sorted({p for q in signs(v) for p in cyc(q)})
ICO = orbit((0, 1, phi)); DOD = orbit((1, 1, 1)) + orbit((0, 1 / phi, phi))
IDO = orbit((0, 0, phi)) + orbit((0.5, phi / 2, phi * phi / 2))
TIC = orbit((0, 1, 3 * phi)) + orbit((1, 2 + phi, 2 * phi)) + orbit((phi, 2, phi ** 3))
def polar(V):   # the dual of a convex solid: one corner per face plane, n/d
    h = ConvexHull(np.array(V, float)); P = {}
    for eq in h.equations: P.setdefault(tuple(np.round(eq, 6)), eq)
    return [tuple(-e[:3] / e[3]) for e in P.values()]
RTC = polar(IDO)
import json
OG = [tuple(v) for v in json.load(open('og-geometry.json'))['v']]   # = papers/ogdoecontahedron/data/hstar-render.json
SOLID = {'G': DOD, 'O': IDO, 'L': OG, 'D': polar(TIC), 'E': ICO, 'N': RTC}
COUNT = {'G': 12, 'O': 32, 'L': 80, 'D': 60, 'E': 20, 'N': 30}   # faces, as a check
def faces(V):
    V = np.array(V, float); V = V / np.linalg.norm(V, axis=1).max(); h = ConvexHull(V); F = {}
    for sm, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
    out = []
    for eq, idx in F.items():
        Q = V[list(idx)]; c = Q.mean(0); nn = np.array(eq[:3]); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(nn, a)
        out.append((nn, Q[np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]))
    return out
FACES = {k: faces(v) for k, v in SOLID.items()}
assert all(len(FACES[k]) == COUNT[k] for k in WORD), {k: len(FACES[k]) for k in WORD}
def rot(ax, a):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
VIEW = rot((1, 0.55, 0.15), 0.85)   # the DICTO square's general pose: every solid shows several faces
d = VIEW.T @ np.array([0, 0, 1.0])
GROUND = (20, 15, 11); EDGE = (60, 40, 18)
TONE = {'G': (138, 92, 196), 'O': (43, 179, 163), 'L': (205, 62, 40), 'D': (196, 198, 208), 'E': (58, 112, 205), 'N': (217, 165, 33)}
N = 1800; SS = 2; W = N * SS; cell = 0.9 * W / 6; sc = 0.42 * cell; x0 = 0.05 * W
light = np.array([-0.4, 0.55, 0.75]); light /= np.linalg.norm(light)
img = Image.new('RGB', (W, W), GROUND); dr = ImageDraw.Draw(img)
for i in range(6):
    for j in range(6):
        k = M[i][j]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        for nn, Q in sorted(FACES[k], key=lambda f: (f[1] @ d).mean()):
            if nn @ d <= 1e-9: continue
            b = 0.45 + 0.55 * max(0, (VIEW @ nn) @ light)
            col = tuple(int(c * b) for c in TONE[k]); V = Q @ VIEW.T
            pts = [(cx + v[0] * sc, cy - v[1] * sc) for v in V]
            dr.polygon(pts, fill=col); dr.line(pts + [pts[0]], fill=EDGE, width=2 * SS)
f = ImageFont.truetype(os.environ.get('LEDFONT', 'DSEG14Classic-Regular.ttf'), int(0.06 * W))
def carved(ch):
    box = int(0.13 * W); edge = int(0.0022 * W)
    def lay(t, sw=0):
        m = Image.new('L', (box, box), 0); ImageDraw.Draw(m).text((box / 2, box / 2), t, font=f, fill=255, anchor='mm', stroke_width=sw, stroke_fill=255)
        return np.array(m, float) / 255
    On, Rim, Ghost = lay(ch), lay(ch, edge), lay('~')
    glow = ndimage.gaussian_filter(On, 0.006 * W); glow /= glow.max()
    core = np.array([255, 255, 255.]); halo = np.array([170, 240, 255.])   # full brightness, glow kept soft (DICTO: "not too bright though"); dim = np.array([70, 62, 52.])
    # DICTO: H and C, the letters on their own tile (teal), in the pieces' colourway: H yellow (gold), C purple (violet)
    rgb = (core * On[..., None] + halo * (1 - On[..., None])) * (On + 0.6 * glow)[..., None] / np.maximum(On + 0.6 * glow, 1e-6)[..., None]
    # dark edges at full strength (DICTO, final: "back to the stronger black outline"); unlit segments a faint veil
    rim = (Rim - On) > 0.3
    rgb = np.where(rim[..., None], np.array([8, 6, 4.]), rgb)
    rgb = np.where(((Ghost - Rim) > 0.5)[..., None], halo, rgb)
    alpha = np.clip(np.maximum.reduce([On, 1.0 * rim, 0.45 * glow, 0.14 * Ghost]), 0, 1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), Image.fromarray((alpha * 255).astype(np.uint8)), (box, box)
CARVE = {ch: carved(ch) for ch in WORD}
for i in range(6):
    for j in range(6):
        t, m, (bw, bh) = CARVE[M[i][j]]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        img.paste(t, (int(cx - bw / 2), int(cy - bh / 2)), m)
img = img.resize((N, N), Image.LANCZOS); img.save(os.environ.get('OUT', 'golden-square.png')); print('ok')
