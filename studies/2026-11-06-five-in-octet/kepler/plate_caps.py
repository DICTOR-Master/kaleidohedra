# The two new gap pieces of I - D (DICTO 11-06: "can I see a render of caps and wedges"): (a) the pentagonal cap alone, (b) the wedge alone,
# (c) all twelve caps (violet) and thirty wedges (ochre) round the dodecahedron inside the icosahedron (sepia line), opened on one side.
import numpy as np, itertools
from PIL import Image, ImageDraw, ImageFont
from davinci import Plate, look, SEPIA, PARCH
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
I = orbit((0, 1, phi))
F = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(I[i] - I[j]) - 2) < 1e-9 for i, j in itertools.combinations(t, 2))]
D = np.array([I[list(t)].mean(0) for t in F])
caps = []
for a in I:
    near = D[np.argsort(np.linalg.norm(D - a, axis=1))[:5]]; caps.append(np.vstack([near, a]))
wedges = []
for i, j in itertools.combinations(range(12), 2):
    if abs(np.linalg.norm(I[i] - I[j]) - 2) > 1e-9: continue
    m = (I[i] + I[j]) / 2; near = D[np.argsort(np.linalg.norm(D - m, axis=1))[:2]]; wedges.append(np.vstack([I[i], I[j], near]))
CAP = (150, 112, 180); WED = (200, 150, 70); DOD = (176, 150, 200)
def one(piece, rgb, out, cap, dirv, upv):
    c = piece.mean(0); pl = Plate(look(dirv, upv), W=2000, scale=2000 * 0.42 / np.ptp(piece, axis=0).max(), centre=c)
    pl.solid(piece, rgb, w=4); pl.skeleton(piece, 3, 160, hidden=True)
    pl.save(out, cap)
ax = caps[0][-1] - caps[0][:5].mean(0); ax /= np.linalg.norm(ax); side = caps[0][0] - caps[0][:5].mean(0); side /= np.linalg.norm(side)
one(caps[0], CAP, '/tmp/cap.png', 'pentagonal cap (12)', ax * 0.75 + side * 0.66, ax)
w0 = wedges[0]; L = w0[1] - w0[0]; L /= np.linalg.norm(L); out_ = w0.mean(0) / np.linalg.norm(w0.mean(0))
one(w0, WED, '/tmp/wedge.png', 'wedge (30)', out_ * 0.55 + np.cross(L, out_) * 0.75 + L * 0.35, out_)
# one pentagon's worth: the dodecahedron, the cap over its front pentagon, and the five wedges on that pentagon's edges, lifted slightly
cap0 = caps[0]; apex = cap0[-1]; ax5 = apex / np.linalg.norm(apex)
pent = cap0[:5]
mine = [w for w in wedges if sum(np.min(np.linalg.norm(pent - q, axis=1)) < 1e-9 for q in w[2:]) == 2]
side = pent[0] - pent.mean(0); side /= np.linalg.norm(side)
pl = Plate(look(ax5 * 0.86 + side * 0.50, ax5), W=2000, scale=2000 * 0.17, centre=pent.mean(0) * 0.55, cy=0.50)
pl.solid(D, DOD, w=3)
items = [(cap0 + 0.12 * ax5, CAP)] + [(w + 0.10 * (w.mean(0) / np.linalg.norm(w.mean(0))), WED) for w in mine]
for p, col in sorted(items, key=lambda t: pl.z(t[0].mean(0))): pl.solid(p, col, w=3)
pl.save('/tmp/assembled.png', 'one cap and its five wedges on the dodecahedron')
a, b, c = [Image.open(f) for f in ('/tmp/cap.png', '/tmp/wedge.png', '/tmp/assembled.png')]
Wd = a.width + b.width + c.width; H = max(a.height, c.height)
sheet = Image.new('RGB', (Wd, H), PARCH); sheet.paste(a, (0, (H - a.height) // 2)); sheet.paste(b, (a.width, (H - b.height) // 2)); sheet.paste(c, (a.width + b.width, 0))
sheet.save('../plate-caps-wedges.png'); print('ok', sheet.size)
