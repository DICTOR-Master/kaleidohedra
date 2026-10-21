# DICTO 2026-10-21: compose the surface-pattern figures (#18 standard) -> figures/
#   surface-patterns.jpg: the nine boundary solids, faces coloured by kind (shots of surface_figs.py, renders/surface-shots)
#   ribbons.jpg: the TQH's 30 ribbons, and one ribbon with its two shell-3 towers
#   edge-lines.jpg: the edge network of each boundary solid, lines only (drawn here from surface-lines.json and surface-patterns.json):
#       gold, front lines bright and back lines faint; purple: the edges that point along a symmetry axis (surface_lines.py, (b))
import os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'renders', 'surface-shots'); OUT = os.path.join(H, 'figures')
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', s)
INK, MUTE, BG = (238, 230, 214), (176, 165, 148), (20, 15, 11)
GOLD, PURPLE = (217, 163, 52), (167, 123, 224)
P = json.load(open(os.path.join(H, 'surface-patterns.json')))['solids']; L = json.load(open(os.path.join(H, 'surface-lines.json')))['solids']
NAMES = ['ID', 'RT', 'GTI', 'FPD', 'OG', 'TPH', 'TQH', 'TQP', 'TQHD']
SUB = {'ID': '20 triangles, 12 pentagons', 'RT': '30 rhombi', 'GTI': '12 pentagons, 20 hexagons', 'FPD': '60 triangles', 'OG': '60 kites, 20 hexagons',
       'TPH': '60 + 60 triangles, 12 pentagons', 'TQH': '60 triangles, 60 trapezoids, 20 hexagons', 'TQP': '60 triangles, 30 rhombi, 60 trapezoids, 12 pentagons',
       'TQHD': '60 + 60 triangles, 60 trapezoids, 20 hexagons'}
def sheet(cells, cols, path, title, sub, cell=440, gap=30, K=2):
    cell, gap = cell * K, gap * K; rows = (len(cells) + cols - 1) // cols; top = 190 * K
    W = cols * cell + (cols - 1) * gap + 160 * K; Hh = top + rows * (cell + 120 * K) + 70 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    d.text((80 * K, 46 * K), title, font=f(60 * K, True), fill=INK); d.text((80 * K, 122 * K), sub, font=f(30 * K), fill=MUTE)
    for k, (img, nm, sb) in enumerate(cells):
        x = 80 * K + (k % cols) * (cell + gap); y = top + (k // cols) * (cell + 120 * K)
        p = img.resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)
        for txt, yy, fo, col in [(nm, y + cell + 8 * K, f(32 * K, True), INK), (sb, y + cell + 52 * K, f(22 * K), MUTE)]:
            while d.textlength(txt, font=fo) > cell + gap - 6 * K and fo.size > 12 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
            d.text((x + cell / 2 - d.textlength(txt, font=fo) / 2, yy), txt, font=fo, fill=col)
    m = 'DICTO · dictospheres.com'; d.text((W - 80 * K - d.textlength(m, font=f(24 * K)), Hh - 50 * K), m, font=f(24 * K), fill=MUTE)
    im.save(os.path.join(OUT, path), quality=92); print(path, im.size)
shot = lambda i: Image.open(os.path.join(S, f'p{i}.png')).convert('RGBA')
sheet([(shot(i), nm, SUB[nm]) for i, nm in enumerate(NAMES)], 5, 'surface-patterns.jpg', 'The surfaces of the shells',
      'Every boundary solid, faces coloured by kind: UP stations (top), the OG and its downward solids (bottom) · DICTO 2026')
sheet([(shot(6), 'The TQH', '30 ribbons (coral): trapezoid pairs on the two-fold axes'), (shot(9), 'One ribbon', 'its two shell-3 towers, drawn a little apart')], 2,
      'ribbons.jpg', 'The ribbons', 'The TQH, boundary of the OG turned out at beat 2 · DICTO 2026', cell=520)
# the line drawings, same camera as the renders
ax = np.array([0.62, 0.48, 0.62]); ax /= np.linalg.norm(ax)
def rot(a, t):
    a = a / np.linalg.norm(a); Kx = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(t) * Kx + (1 - np.cos(t)) * Kx @ Kx
cam = rot(np.array([0, 1, 0]), 0.22) @ rot(np.array([1, 0, 0]), 0.30) @ ax
up = np.array([0, 1.0, 0]) - cam[1] * cam; up /= np.linalg.norm(up); rt = np.cross(up, cam)
def lines(nm, n=1200):
    s, l = P[nm], L[nm]; V = np.array(l['corners_float']); assert np.allclose(V, np.array(s['corners_float']))
    V = V / np.linalg.norm(V, axis=1).max(); front = set()
    for fc in s['faces_idx']:
        Q = V[fc]; nn = np.cross(Q[1] - Q[0], Q[2] - Q[0]); nn = nn if nn @ Q[0] > 0 else -nn
        if nn @ cam > 0: front |= {(min(a, b), max(a, b)) for a, b in zip(fc, fc[1:] + fc[:1])}
    hi = {i for fam in l['axis_families'] for i in fam} | {i for b in l['belts'] for i in b}
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pr = lambda p: (n / 2 + p @ rt * n * 0.46, n / 2 - p @ up * n * 0.46)
    order = sorted(range(len(l['edge_list'])), key=lambda i: tuple(l['edge_list'][i]) in front)
    for i in order:
        a, b = l['edge_list'][i]; fr = (min(a, b), max(a, b)) in front; col = PURPLE if i in hi else GOLD
        d.line([pr(V[a]), pr(V[b])], fill=col + ((255,) if fr else (70,)), width=10 if fr else 4)
    return im
LS = {nm: (f"{L[nm]['edges']} edges, {L[nm]['directions']} directions" + (f", {L[nm]['central_belts']} belts" if L[nm]['central_belts'] else '')) for nm in NAMES}
sheet([(lines(nm), nm, LS[nm]) for nm in NAMES], 5, 'edge-lines.jpg', 'The lines of the shells',
      'Edge networks of the boundary solids; purple: edges along a symmetry axis (gold: the rest; faint: behind) · DICTO 2026')
