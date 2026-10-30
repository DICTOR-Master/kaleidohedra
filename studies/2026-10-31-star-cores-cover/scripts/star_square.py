# The STAR CORES square (DICTO 2026-10-31: "star cores cover for book 9x9?! matching current style"): cover for the book "Star Cores",
# after the HexOct, Golden Cycle and Alicia squares. Cyclic Latin square 9 x 9: row i, column j holds position (i+j) mod 9 of STARCORES,
# so STARCORES reads across the top and down the left and every position (solid) comes once in each row and column. Each position is one
# star of the book, a solid with its own face pyramids turned outwards (tips at twice the feet of the face perpendiculars, the doubling
# rule of #78), in the book's order: S Cleo star (icosahedron, #35), T TI Star (#78), A the Star Halo's star, R the GTI's star,
# C the FPD's star, O the Ogdoecontahedron's star, R the TI Star core's star, E the Hecatodihedron's star, S Tweedledum's star.
# Nine solids, nine colours. Letters: the HexOct LED letters (DSEG14 Classic, OFL), white. Usage: star_square.py <dataset solids dir>
import math, os, sys, json, itertools, numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
SOL = sys.argv[1]
WORD = 'STARCORES'; n = 9
M = [[(i + j) % n for j in range(n)] for i in range(n)]
assert all(len(set(r)) == n for r in M) and all(len({M[i][j] for i in range(n)}) == n for j in range(n))
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v): return {tuple(s * x for s, x in zip(ss, v)) for ss in itertools.product((1, -1), repeat=3)}
def orbit(v): return sorted({p for q in signs(v) for p in cyc(q)})
from scipy.spatial import ConvexHull
def hull_faces(V):
    V = np.array(V, float); h = ConvexHull(V); F = {}
    for sm, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
    out = []
    for eq, idx in F.items():
        idx = list(idx); Q = V[idx]; c = Q.mean(0); nn = np.array(eq[:3]); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(nn, a)
        out.append([idx[k] for k in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return V, out
def load(slug):
    m = json.load(open(os.path.join(SOL, slug + '.json')))
    return np.array([[float(x) for x in v['decimal']] for v in m['vertices']]), m['faces']
SOLIDS = [('Cleo star', hull_faces(orbit((0, 1, phi)))),
          ('TI Star', hull_faces(orbit((0, 1, 3 * phi)) + orbit((1, 2 + phi, 2 * phi)) + orbit((phi, 2, phi ** 3)))),
          ('Star Halo', load('dicto-star-halo')), ('GTI', load('dicto-gti')), ('FPD', load('dicto-fpd')),
          ('OG', load('dicto-ogdoecontahedron')), ('TI Star core', load('dicto-ti-star-core')),
          ('Hecatodihedron', load('dicto-hecatodihedron')), ('Tweedledum', load('dicto-tweedledum'))]
if os.environ.get('SET') == 'initials':   # DICTO 10-31: each letter the initial of its shape's name, all from the Star Cores study
    SOLIDS = [('Star Halo', load('dicto-star-halo')), ('TI Star core', load('dicto-ti-star-core')), ('Alice', load('dicto-alice')),
              ('Red King', load('dicto-red-king')), ('Chucky', load('dicto-chucky')), ('OG', load('dicto-ogdoecontahedron')),
              ('Red Knight', load('dicto-red-knight')), ('ED F16', load('dicto-skewed-ed-16')), ('Samson', load('dicto-samson'))]
def star(V, F):
    """the star: each face's pyramid from the centre turned outwards, tip at twice the foot of the perpendicular (#78, t = 2);
    returns triangles (3 x 3 arrays), scaled so the star's farthest point is 1."""
    V = V - V.mean(0); T = []
    for f in F:
        Q = V[f]; nn = np.cross(Q[1] - Q[0], Q[2] - Q[0]); nn /= np.linalg.norm(nn)
        if nn @ Q.mean(0) < 0: nn = -nn; Q = Q[::-1]
        tip = 2 * (nn @ Q[0]) * nn
        for k in range(len(Q)): T.append(np.array([Q[k], Q[(k + 1) % len(Q)], tip]))
    T = np.array(T); return T / np.linalg.norm(T.reshape(-1, 3), axis=1).max()
STARS = []
for name, (V, F) in SOLIDS:
    print(name, len(V), 'corners', len(F), 'faces'); STARS.append(star(np.array(V), F))
def rot(ax, a):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
VIEW = rot((1, 0.55, 0.15), 0.85)   # the squares' general pose
GROUND = (20, 15, 11); EDGE = (40, 26, 12)
TONE = [(217, 165, 33), (138, 92, 196), (43, 179, 163), (205, 62, 40), (196, 198, 208), (58, 112, 205), (64, 160, 84), (226, 124, 44), (206, 96, 150)]
N = 2400; SS = 2; W = N * SS; cell = 0.92 * W / n; sc = 0.47 * cell; x0 = 0.04 * W
light = np.array([-0.4, 0.55, 0.75]); light /= np.linalg.norm(light)
img = Image.new('RGB', (W, W), GROUND); dr = ImageDraw.Draw(img)
for i in range(n):
    for j in range(n):
        k = M[i][j]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        T = STARS[k] @ VIEW.T
        for t in sorted(T, key=lambda t: t[:, 2].mean()):
            nn = np.cross(t[1] - t[0], t[2] - t[0]); nn /= np.linalg.norm(nn)
            if nn @ t.mean(0) < 0: nn = -nn
            if nn[2] <= 1e-9: continue
            b = 0.42 + 0.58 * max(0, nn @ light)
            pts = [(cx + v[0] * sc, cy - v[1] * sc) for v in t]
            dr.polygon(pts, fill=tuple(int(c * b) for c in TONE[k])); dr.line(pts + [pts[0]], fill=EDGE, width=SS)
f = ImageFont.truetype('DSEG14Classic-Regular.ttf', int(0.042 * W))
# DICTO 10-31: "opposite letter colours on stars": each letter in the palette colour opposite its star's (gold/violet, teal/red,
# blue/orange, green/rose), brightened to read on the star; the silver star takes a dark letter with a light rim.
LETTER = [(190, 140, 255), (255, 205, 70), (255, 96, 72), (90, 232, 212), None, (255, 158, 64), (255, 128, 196), (96, 156, 255), (104, 214, 122)]
def carved(ch, col=None):
    box = int(0.09 * W); edge = int(0.0018 * W)
    def lay(t, sw=0):
        m = Image.new('L', (box, box), 0); ImageDraw.Draw(m).text((box / 2, box / 2), t, font=f, fill=255, anchor='mm', stroke_width=sw, stroke_fill=255)
        return np.array(m, float) / 255
    On, Rim, Ghost = lay(ch), lay(ch, edge), lay('~')
    glow = ndimage.gaussian_filter(On, 0.005 * W); glow /= glow.max()
    core = np.array([255, 255, 255.]) if col is None else np.array(col, float); halo = np.array([170, 240, 255.]) if col is None else 0.55 * core + 0.45 * 255
    dark = os.environ.get('LETTERS') == 'opposite' and col is None
    if dark: core = np.array(GROUND, float) * 0.6; halo = np.array([90, 90, 96.])
    rgb = (core * On[..., None] + halo * (1 - On[..., None])) * (On + 0.6 * glow)[..., None] / np.maximum(On + 0.6 * glow, 1e-6)[..., None]
    rim = (Rim - On) > 0.3
    rgb = np.where(rim[..., None], np.array([235, 235, 240.]) if dark else np.array([8, 6, 4.]), rgb)
    rgb = np.where(((Ghost - Rim) > 0.5)[..., None], halo, rgb)
    alpha = np.clip(np.maximum.reduce([On, 1.0 * rim, 0.45 * glow, 0.14 * Ghost]), 0, 1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), Image.fromarray((alpha * 255).astype(np.uint8)), (box, box)
if os.environ.get('LETTERS') == 'opposite': CARVE = {k: carved(WORD[k], LETTER[k]) for k in range(n)}
else: CARVE = {k: carved(WORD[k]) for k in range(n)}
for i in range(n):
    for j in range(n):
        t, m, (bw, bh) = CARVE[M[i][j]]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        img.paste(t, (int(cx - bw / 2), int(cy - bh / 2)), m)
img = img.resize((N, N), Image.LANCZOS); img.save(os.environ.get('OUT', 'star-square.png')); print('ok')
