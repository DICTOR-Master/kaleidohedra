# render_twin_discs.py, DICTO 11 Nov 2026 ("render the twin hull vacuus with the discs"). Uses the #87 census renderer (own z-buffer,
# orthographic, 3x supersampled, edges >= 2 px: render standard) from studies/2026-11-02-dicto-vacuus/scripts/render.py.
# Panel A: the twin hull's Vacuus, 300 fins; the 60 fins of the six decagonal discs (36 deg each) in gold, the other fins in muted
# colours by apex class; translucent ghost of the twin hull. Panel B: the six discs alone inside the ghost. View along a generic
# direction so all six discs show. Usage: render_twin_discs.py <five-fold-octet dir> <render.py> <logo> <out.png>
import sys, os, numpy as np
D, RENDER, LOGO, OUTP = sys.argv[1:5]
sys.argv = ['x', '.', '.', LOGO]
exec(open(RENDER).read().split('def plate(')[0])                         # Canvas, rgb, shade, rot, PAL, SS, PX, N
sys.path.insert(0, D); cwd = os.getcwd(); os.chdir(D); exec(open('exact_upward.py').read().split("def kinds(S)")[0]); os.chdir(cwd)
from scipy.spatial import ConvexHull
S5 = 5 ** .5
T = np.array([[float(x.a) - float(x.b) * S5 for x in v] for v in OG])  # the 102 twin points
h = ConvexHull(T); F = [list(s) for s in h.simplices]                    # 200 triangles (simplicial, checked in twin_vacuus.py)
assert len(F) == 200, len(F)
E = sorted({(min(a, b), max(a, b)) for f in F for a, b in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2]))}); assert len(E) == 300
apex = np.array([np.degrees(np.arccos(np.clip(T[a] @ T[b] / (np.linalg.norm(T[a]) * np.linalg.norm(T[b])), -1, 1))) for a, b in E])
disc = np.abs(apex - 36.0) < 1e-6; assert disc.sum() == 60, disc.sum()
# group the disc fins into the six discs by plane normal
nrm = []
for (a, b) in E:
    n = np.cross(T[a], T[b]); n /= np.linalg.norm(n); n *= np.sign(n[np.argmax(np.abs(n) > 1e-9)]); nrm.append(n)
nrm = np.array(nrm); keys = {}
for i in np.where(disc)[0]: keys.setdefault(tuple(np.round(nrm[i], 6)), []).append(i)
assert len(keys) == 6 and all(len(v) == 10 for v in keys.values()), [len(v) for v in keys.values()]
cls_levels = sorted(set(np.round(apex[~disc], 4)))
MUTE = ['#8e5bd6', '#2bb3a3', '#c4a6ee']
GOLD = rgb('#d4af37'); DISC_COLS = ['#d4af37', '#8e5bd6', '#2bb3a3', '#e07b39', '#4a7fd4', '#c94a5a']   # six distinct discs (11-11: golds blurred)
M = rot(22, 31); W = T @ M.T; lim = 1.08 * np.linalg.norm(T, axis=1).max(); O = np.zeros(3)
NF = []
for f in F:
    n = np.zeros(3)
    for k in range(3): n += np.cross(W[f[k]], W[f[(k + 1) % 3]])
    NF.append(n)
A = Canvas(lim)
for i, (a, b) in enumerate(E):
    tri = np.array([O, W[a], W[b]]); n = np.cross(tri[1], tri[2])
    if disc[i]: col = GOLD
    else: col = np.array([0.78, 0.78, 0.82]) * (0.85 + 0.05 * cls_levels.index(round(apex[i], 4)))
    A.tri(tri, shade(col, n), i)
A.outlines(); A.ghost(W, F, NF, 0.08)
B = Canvas(lim)
for d, ids in enumerate(keys.values()):
    for i in ids:
        a, b = E[i]; tri = np.array([O, W[a], W[b]]); B.tri(tri, shade(rgb(DISC_COLS[d]), np.cross(tri[1], tri[2])), i)
B.outlines(); B.ghost(W, F, NF, 0.10)
from PIL import Image, ImageDraw, ImageFont
im = Image.new('RGB', (2 * PX + 40, PX + 90), 'white'); im.paste(A.image(), (0, 90)); im.paste(B.image(), (PX + 40, 90))
dr = ImageDraw.Draw(im)
try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
except Exception: fnt = fs = ImageFont.load_default()
dr.text((24, 14), 'The twin OG: Vacuus of the twin hull', fill=(30, 30, 40), font=fnt)
dr.text((24, 52), '300 fins (centre to every edge); the 60 disc fins (36°) in gold', fill=(80, 80, 90), font=fs)
dr.text((PX + 64, 52), 'the six decagonal discs alone, one per five-fold axis', fill=(80, 80, 90), font=fs)
lg = Image.open(LOGO).convert('RGBA'); hh = 70; lg = lg.resize((int(lg.width * hh / lg.height), hh)); im.paste(lg, (im.width - lg.width - 8, im.height - hh - 8), lg)
dr.text((24, im.height - 34), 'DICTO · dictospheres.com · twin = √5 → −√5 on the exact OG', fill=(120, 110, 90), font=fs)
im.save(OUTP, dpi=(300, 300)); print('six discs of ten 36-degree fins; FINAL ok')
