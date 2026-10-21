# DICTO 2026-10-21 ("feels like some figures are missing for solids and patterns"): three more pattern figures, drawn in 2D with the
# same camera as edge-lines.jpg (surface_compose.py): (1) the surfaces of the new solids D5-D11 (front faces filled by kind, lines on top);
# (2) the surfaces of the polar Hecatodihedron sequence (polar S0-S4); (3) the axis rhythm: what each 2-, 3- and 5-fold axis passes
# through on the true hull of each solid, beats 0-11 (axis-words.log, axis-hull.json). Float on exact points.
#   usage: python3 more_patterns.py <studies/2026-10-19-five-fold-octet>
import os, sys, json, pickle, numpy as np
from scipy.spatial import ConvexHull
from PIL import Image, ImageDraw
sys.path.insert(0, sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'surface_compose.py')).read()
exec(src[src.index('import os, json'):src.index('shot = lambda')])                  # fonts, colours, sheet()
exec(src[src.index('# the line drawings'):src.index('def lines(')])                   # the same camera
KC = {3: (217, 163, 52), 4: (107, 63, 160), 5: (154, 120, 200), 6: (138, 90, 36), 10: (240, 212, 138)}
def faces(P):
    H = ConvexHull(P); G = {}
    for s_, e in zip(H.simplices, H.equations): G.setdefault(tuple(np.round(e, 8)), set()).update(s_)
    out = []
    for ids in G.values():
        ids = list(ids); c = P[ids].mean(0); nn = c / np.linalg.norm(c); u = P[ids[0]] - c; u /= np.linalg.norm(u); w = np.cross(nn, u)
        ids.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); out.append(ids)
    return out
def surface(P, n=1200):
    P = P / np.linalg.norm(P, axis=1).max(); F = faces(P); im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pr = lambda p: (n / 2 + p @ rt * n * 0.46, n / 2 - p @ up * n * 0.46)
    front = []
    for fc in F:
        Q = P[fc]; nn = np.cross(Q[1] - Q[0], Q[2] - Q[0]); nn = nn if nn @ Q.mean(0) > 0 else -nn
        if nn @ cam > 0: front.append((Q.mean(0) @ cam, fc, nn / np.linalg.norm(nn)))
    for _, fc, nn in sorted(front):
        shade = 0.55 + 0.45 * max(0, nn @ cam); col = tuple(int(c * shade) for c in KC.get(len(fc), (200, 200, 200)))
        d.polygon([pr(P[i]) for i in fc], fill=col + (255,), outline=(30, 22, 15, 255))
    return im, len(F)
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb'))
NM = {5: 'DICTO TQP-252', 6: 'DICTO TQ-320', 7: 'DICTO TQP-402', 8: 'DICTO TQ-500', 9: 'DICTO TQD-732', 10: 'DICTO TQHD-662', 11: 'DICTO TQP-672'}
cells = []
for k in range(5, 12):
    P = np.array([[x.f() for x in v] for v in D[k]]); P = P[sorted(set(ConvexHull(P).vertices))]; im, nf = surface(P)
    cells.append((im, NM[k], f'beat {k}: {len(P)} corners, {nf} faces'))
sheet(cells, 4, 'new-solids-surfaces.jpg', 'The surfaces of the new solids',
      'Beats 5-11, same view as Figure 9 · triangles gold, four-sided purple, pentagons lilac, hexagons bronze, decagons pale · DICTO 2026')
PL = json.load(open(os.path.join(HERE, 'polar-turned.json')))['boundaries_float']; cells = []
for i, k in enumerate(['polar S0', 'polar S1', 'polar S2', 'polar S3', 'polar S4']):
    P = np.array(PL[k], float); P = P[sorted(set(ConvexHull(P).vertices))]; im, nf = surface(P)
    cells.append((im, 'the Hecatodihedron (scaled)' if i == 0 else f'polar beat {i}', f'{len(P)} corners, {nf} faces'))
sheet(cells, 5, 'polar-surfaces.jpg', 'The surfaces of the polar sequence',
      'The Hecatodihedron and its UP family shrinking inward (the polar of the OG turned out), same view · DICTO 2026')
# the axis rhythm
W_ = {}
for line in open(os.path.join(HERE, 'axis-words.log')):
    t = line.split()
    if len(t) > 8 and t[1].isdigit() or (t and t[0] in ('OG', 'TPH', 'TQH', 'TQP', 'TQHD')):
        nm = t[0] if t[0] in ('OG', 'TPH', 'TQH', 'TQP', 'TQHD') else f'{t[0]} {t[1]}'
        try: W_[nm] = {'5': t[t.index('5-fold:') + 1], '3': t[t.index('3-fold:') + 1], '2': t[t.index('2-fold:') + 1]}
        except ValueError: pass
HU = json.load(open(os.path.join(HERE, 'axis-hull.json')))
for nm, v in HU.items(): W_[nm] = {'5': v['word']['5-fold'], '3': v['word']['3-fold'], '2': v['word']['2-fold']}
order = ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'] + [f'down {k}' for k in range(5, 10)]
order = [o for o in order if o in W_]
K = 2; cw, ch = 150 * K, 120 * K; left = 260 * K; top = 220 * K; Wd = left + cw * len(order) + 80 * K; Hd = top + ch * 3 + 140 * K
im = Image.new('RGB', (Wd, Hd), BG); d = ImageDraw.Draw(im)
d.text((80 * K, 46 * K), 'The axis rhythm', font=f(60 * K, True), fill=INK)
d.text((80 * K, 122 * K), 'What each symmetry axis passes through on each solid (true hull): dot = corner, bar = edge, disc = face · DICTO 2026', font=f(26 * K), fill=MUTE)
for j, o in enumerate(order):
    lab = {'down 5': 'TQP-252', 'down 6': 'TQ-320', 'down 7': 'TQP-402', 'down 8': 'TQ-500', 'down 9': 'TQD-732'}.get(o, o); x = left + j * cw + cw / 2
    d.text((x - d.textlength(lab, font=f(24 * K)) / 2, top - 50 * K), lab, font=f(24 * K), fill=INK)
for r, (ax_, nm) in enumerate([('2', 'two-fold'), ('3', 'three-fold'), ('5', 'five-fold')]):
    y = top + r * ch + ch / 2; d.text((80 * K, y - 16 * K), nm, font=f(30 * K, True), fill=INK)
    for j, o in enumerate(order):
        x = left + j * cw + cw / 2; w = W_[o][ax_]; c = GOLD if w == 'corner' else PURPLE if w == 'edge' else (240, 212, 138)
        if w == 'corner': d.ellipse([x - 14 * K, y - 14 * K, x + 14 * K, y + 14 * K], fill=c)
        elif w == 'edge': d.rectangle([x - 40 * K, y - 8 * K, x + 40 * K, y + 8 * K], fill=c)
        else: d.ellipse([x - 40 * K, y - 40 * K, x + 40 * K, y + 40 * K], outline=c, width=8 * K)
m = 'DICTO · dictospheres.com'; d.text((Wd - 80 * K - d.textlength(m, font=f(24 * K)), Hd - 50 * K), m, font=f(24 * K), fill=MUTE)
im.save(os.path.join(OUT, 'axis-rhythm.jpg'), quality=92); print('axis-rhythm.jpg', im.size, order)
