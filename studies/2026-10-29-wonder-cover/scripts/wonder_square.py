# The WONDER square (DICTO 2026-10-29): cover for "Alicia in Wonderland: The Red & White Queens", in the series style of the
# HexOct and GOLDEN squares. Cyclic Latin square of WONDER (six different letters). One shape of the book per letter:
# W the White Queen (600-cell) and R the Red Queen (120-cell), each as its vertex-first shadow (outline of the 4D solid
# projected along a corner); O Alicia (W48, Boole Stott's cell-first middle slice), N Alice (W49), D Humpty Dumpty (the
# 48-corner egg), E the White Rabbit (W51): exact slices from the dataset (DICTO Solids v5). One circumradius, one pose.
# Letters: the series LED letters (DSEG14 Classic, OFL), white.
import math, os, itertools, json, numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
WORD = 'WONDER'; n6 = 6
M = [[WORD[(i + j) % n6] for j in range(n6)] for i in range(n6)]
assert M[0] == list(WORD) and [r[0] for r in M] == list(WORD)
assert all(len(set(r)) == 6 for r in M) and all(len({M[i][j] for i in range(6)}) == 6 for j in range(6))
phi = (1 + 5 ** .5) / 2
def evenperms(v):
    out = set()
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0: out.add(tuple(v[k] for k in p))
    return out
def signs(v): return {tuple(s * x for s, x in zip(ss, v)) for ss in itertools.product((1, -1), repeat=len(v))}
C600 = set()   # the 120 corners of the 600-cell (circumradius 1)
for i in range(4):
    for s in (1, -1): C600.add(tuple(s if k == i else 0 for k in range(4)))
C600 |= signs((.5, .5, .5, .5))
for q in signs((phi / 2, .5, 1 / (2 * phi), 0)): C600 |= evenperms(q)
C600 = np.array(sorted(C600)); assert len(C600) == 120
cells = ConvexHull(C600).simplices; assert len(cells) == 600
C120 = C600[cells].mean(1)                 # the 120-cell's 600 corners: the 600-cell's cell centres (DICTO's Red Queen from the White)
def shadow(V4): return [tuple(v[:3]) for v in V4]   # along the corner (0,0,0,1): vertex-first shadow
def slice_(name): return [tuple(float(x) for x in v['decimal']) for v in json.load(open(f'solids/dicto-{name}.json'))['vertices']]
SOLID = {'W': shadow(C600), 'O': slice_('alicia'), 'N': slice_('alice'), 'D': slice_('humpty-dumpty'), 'E': slice_('white-rabbit'), 'R': shadow(C120)}
COUNT = {}
def faces(V):
    V = np.array(V, float); V = V / np.linalg.norm(V, axis=1).max(); h = ConvexHull(V); F = {}
    for sm, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
    out = []
    for eq, idx in F.items():
        Q = V[list(idx)]; c = Q.mean(0); nn = np.array(eq[:3]); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(nn, a)
        out.append((nn, Q[np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]))
    return out
FACES = {k: faces(v) for k, v in SOLID.items()}
print({k: len(FACES[k]) for k in WORD})
def rot(ax, a):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
VIEW = rot((1, 0.55, 0.15), 0.85)   # the DICTO square's general pose: every solid shows several faces
d = VIEW.T @ np.array([0, 0, 1.0])
GROUND = (20, 15, 11); EDGE = (60, 40, 18)
TONE = {'W': (226, 228, 236), 'O': (217, 165, 33), 'N': (58, 112, 205), 'D': (43, 179, 163), 'E': (180, 138, 224), 'R': (205, 62, 40)}   # White Queen white, Alicia gold, Alice blue, Humpty teal, White Rabbit lilac, Red Queen red
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
    box = int(0.13 * W); edge = int(0.0042 * W)   # DICTO 10-29: black letter outlines over the spheres, stronger than on the flat-faced covers
    def lay(t, sw=0):
        m = Image.new('L', (box, box), 0); ImageDraw.Draw(m).text((box / 2, box / 2), t, font=f, fill=255, anchor='mm', stroke_width=sw, stroke_fill=255)
        return np.array(m, float) / 255
    On, Rim, Ghost = lay(ch), lay(ch, edge), lay('~')
    glow = ndimage.gaussian_filter(On, 0.006 * W); glow /= glow.max()
    core = np.array([255, 255, 255.]); halo = np.array([170, 240, 255.])   # full brightness, glow kept soft (DICTO: "not too bright though"); dim = np.array([70, 62, 52.])
    if ch == 'W': core = np.array([205, 62, 40.]); halo = core   # DICTO 10-29: the W letters red, tiles unchanged
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
img = img.resize((N, N), Image.LANCZOS); img.save(os.environ.get('OUT', 'wonder-square.png')); print('ok')
