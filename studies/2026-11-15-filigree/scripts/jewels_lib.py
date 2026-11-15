# jewels_lib.py (15 Nov 2026; split from render_jewels.py) - DICTO · dictospheres.com
# The jewellery figures of the Platonic book's chapter "Filigree": DICTO's image of gold filigree holding stones of different shapes
# close together. Two materials only: stones (the Platonic solids, in their element colours) and one gold (every connector).
# Every piece comes from the checked builders of study 2026-11-14-platonic-hybrid (golden.py exact Q(sqrt5) coordinates,
# hybrid.py cell_pieces / golden_slab, the same pieces its covering tests passed), so each caption's count is the count printed here.
#   ring      (a) the icosahedron of edge 1 in Pacioli's position in its six Admiral Caps (a six-claw setting), on a plain hoop;
#             (b) the same with the eight caps, which close it into the dodecahedron of edge 1; the four upper caps drawn lifted.
#   bracelet  one grid line of the golden tiling (Hart's dodecahedra and Dogstars on alternate cubes of edge phi): D S I S D S I.
#   brooch    a 3 x 3 patch of the middle layer of the golden slab (#106 skins, Space-Fillers Thm 8.3) with its bottom edging
#             (roof plates Z and roofs R, Space-Fillers Prop 8.3) as the flat back; top edging left off so the stones show.
# House render standard: solid faces with a depth buffer, crisp antialiased edges (3x supersampling, hidden edges removed), no haze,
# DICTO mark. Usage: render_jewels.py <outdir> [width_px]  -> PROGRESS lines, COUNT lines, FINAL ok / FINAL FAIL
import sys, os, itertools, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
HYB = os.path.join(HERE, '..', '..', '2026-11-14-platonic-hybrid', 'scripts'); sys.path.insert(0, HYB)
_argv = sys.argv; sys.argv = _argv[:1] + ['pilot']        # hybrid.py reads its own arguments at import
import golden as G, hybrid as H
sys.argv = _argv
from golden import V, Part, PHI, HF, HALF
phi = (1 + 5 ** 0.5) / 2
STONE = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}
GOLD = (214, 168, 66); GOLD_EDGE = (98, 70, 20); STONE_EDGE = (246, 226, 168); GROUND = (22, 17, 13)
GOLDEN = {'A', 'cap', 'S', 'R', 'Z', 'hoop', 'gT', 'gO'}

# ---- faces of a piece = union(pos) minus union(neg) (as render_hybrid.py of the hybrid study)
def hull_faces(Vs):
    Vs = np.asarray(Vs, float); h = ConvexHull(Vs); groups = {}
    for simp, eq in zip(h.simplices, h.equations):
        groups.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
    out = []
    for key, idx in groups.items():
        n = np.array(key[:3]); idx = list(idx); c = Vs[idx].mean(0); u = Vs[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((Vs[i] - c) @ w, (Vs[i] - c) @ u)); out.append((n, key[3], Vs[idx]))
    return out
def piece_faces(pc):
    lab, pos, negs = pc
    PF = [f for p in pos for f in hull_faces([[float(x) for x in v] for v in p.verts])]
    NF = [f for p in negs for f in hull_faces([[float(x) for x in v] for v in p.verts])]
    same = lambda a, b: np.allclose(a[0], b[0], atol=1e-7) and abs(a[1] - b[1]) < 1e-7
    out = [(n, poly) for n, o, poly in PF if not any(same((n, o), (m, q)) for m, q, _ in NF)]
    out += [(-n, poly[::-1]) for n, o, poly in NF if not any(same((n, o), (m, q)) for m, q, _ in PF)]
    if len(pos) > 1:                                   # union of convex parts (Admiral Cap): drop the shared inner faces
        out = [(n, poly) for n, poly in out if not any(np.allclose(n, -m, atol=1e-7) and np.allclose(sorted(map(tuple, np.round(poly, 7))), sorted(map(tuple, np.round(q, 7)))) for m, q in out)]
    return out

def rot(ax, a):
    c, s = np.cos(a), np.sin(a); i, j = [(1, 2), (0, 2), (0, 1)][ax]; R = np.eye(3); R[i, i] = R[j, j] = c; R[i, j] = -s; R[j, i] = s; return R

def render(items, Rm, W, Hmax=None, edges_for=None, pad=0.06):
    """items: (label, normal, polygon, draw_edges). Returns a PIL image (supersampled 3x, reduced)."""
    SS = 3; Wd = W * SS
    allp = np.vstack([p for _, _, p, _ in items]) @ Rm.T
    spanx, spany = np.ptp(allp[:, 0]), np.ptp(allp[:, 1])
    sc = Wd * (1 - 2 * pad) / spanx
    if Hmax and spany * sc / (1 - 2 * pad) > Hmax * SS: sc = Hmax * SS * (1 - 2 * pad) / spany
    Ht = int(spany * sc / (1 - 2 * pad)) + 1
    ox = (Wd - spanx * sc) / 2; oy = (Ht - spany * sc) / 2
    cx0, cy0 = allp[:, 0].min(), allp[:, 1].max()
    def proj(p):
        q = p @ Rm.T; return np.column_stack([ox + (q[:, 0] - cx0) * sc, oy + (cy0 - q[:, 1]) * sc, q[:, 2]])
    img = np.zeros((Ht, Wd, 3)); img[:] = GROUND; zb = np.full((Ht, Wd), -1e9)
    L = np.array([-0.35, 0.55, 0.76]); L /= np.linalg.norm(L); Hh = L + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
    def shade(n, lab):
        nv = Rm @ n; nv = nv if nv[2] >= 0 else -nv; d = max(0.0, nv @ L)
        if lab in GOLDEN: k = 0.38 + 0.52 * d; sp = 0.22 * max(0.0, nv @ Hh) ** 28; base = np.array(GOLD, float)
        else: k = 0.40 + 0.60 * d; sp = 0.22 * max(0.0, nv @ Hh) ** 40; base = np.array(STONE[lab], float)
        return np.clip(base * k + 255 * sp, 0, 255)
    for lab, n, poly, _ in items:
        col = shade(n, lab); s = proj(poly)
        for k in range(1, len(s) - 1):
            (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = s[0], s[k], s[k + 1]
            xa, xb = int(max(0, np.floor(min(x0, x1, x2)))), int(min(Wd - 1, np.ceil(max(x0, x1, x2))))
            ya, yb = int(max(0, np.floor(min(y0, y1, y2)))), int(min(Ht - 1, np.ceil(max(y0, y1, y2))))
            if xb < xa or yb < ya: continue
            X, Y = np.meshgrid(np.arange(xa, xb + 1) + 0.5, np.arange(ya, yb + 1) + 0.5)
            d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(d) < 1e-12: continue
            a = ((y1 - y2) * (X - x2) + (x2 - x1) * (Y - y2)) / d; b = ((y2 - y0) * (X - x2) + (x0 - x2) * (Y - y2)) / d; c = 1 - a - b
            m = (a >= -1e-9) & (b >= -1e-9) & (c >= -1e-9)
            if not m.any(): continue
            z = a * z0 + b * z1 + c * z2 - (2e-3 if lab in GOLDEN else 0.0)   # coincident faces: the stone shows
            sub = zb[ya:yb + 1, xa:xb + 1]; put = m & (z > sub); sub[put] = z[put]; img[ya:yb + 1, xa:xb + 1][put] = col
    # edges: every polygon side of pieces that draw edges, depth-tested with a small offset; gold edges dark, stone edges light
    EPS = 0.02; EW = max(2, int(W / 800)) * SS
    E = {}
    for lab, n, poly, de in items:
        if not de: continue
        for a, b in zip(poly, np.roll(poly, -1, 0)):
            key = tuple(sorted([tuple(np.round(a, 6)), tuple(np.round(b, 6))]))
            if key in E and E[key][0] in GOLDEN and lab not in GOLDEN: E[key] = (lab, a, b)   # a stone edge wins
            E.setdefault(key, (lab, a, b))
    offs = [(dx, dy) for dx in range(-EW // 2, EW // 2 + 1) for dy in range(-EW // 2, EW // 2 + 1) if dx * dx + dy * dy <= (EW / 2) ** 2]
    for golden_pass in (True, False):
        acc = np.zeros((Ht, Wd), bool)
        for lab, a, b in E.values():
            if (lab in GOLDEN) != golden_pass: continue
            s = proj(np.array([a, b])); Ln = np.hypot(*(s[1, :2] - s[0, :2])); nn = max(2, int(Ln * 2))
            t = np.linspace(0, 1, nn)[:, None]; pts = s[0] * (1 - t) + s[1] * t
            xi = np.clip(pts[:, 0].astype(int), 0, Wd - 1); yi = np.clip(pts[:, 1].astype(int), 0, Ht - 1)
            vis = pts[:, 2] >= zb[yi, xi] - EPS
            for dx, dy in offs: acc[np.clip(yi[vis] + dy, 0, Ht - 1), np.clip(xi[vis] + dx, 0, Wd - 1)] = True
        img[acc] = GOLD_EDGE if golden_pass else STONE_EDGE
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).resize((W, max(1, Ht // SS)), Image.LANCZOS)

def items_of(pieces, shift=None):
    out = []
    for pc in pieces:
        d = np.zeros(3) if shift is None else shift(pc)
        for n, poly in piece_faces(pc): out.append((pc[0], n, poly + d, True))
    return out
def hoop(top, R=1.75, wy=0.42, th=0.11, nu=160, nv=16):
    """a plain band: circle of radius R in the x-z plane whose top touches the point top; flat elliptic cross-section"""
    c = np.array(top) - np.array([0, 0, R]); out = []
    U = np.linspace(0, 2 * np.pi, nu + 1); Vv = np.linspace(0, 2 * np.pi, nv + 1)
    def P(u, v):
        rr = R + th * np.cos(v) + th * 0.0; radial = np.array([np.sin(u), 0, np.cos(u)])
        return c + radial * (R + th * np.cos(v) - 0.0) + np.array([0, wy / 2 * np.sin(v), 0]) - radial * th
    for i in range(nu):
        for j in range(nv):
            q = np.array([P(U[i], Vv[j]), P(U[i + 1], Vv[j]), P(U[i + 1], Vv[j + 1]), P(U[i], Vv[j + 1])])
            n = np.cross(q[1] - q[0], q[3] - q[0]); nl = np.linalg.norm(n)
            if nl < 1e-12: continue
            out.append(('hoop', n / nl, q, False))
    return out
def count(pieces): return {l: sum(1 for p in pieces if p[0] == l) for l in sorted(set(p[0] for p in pieces))}
FD = '/usr/share/fonts/truetype/dejavu/'
def finish(im, labels, path):
    d = ImageDraw.Draw(im); Wi = im.size[0]
    f = ImageFont.truetype(FD + 'DejaVuSans.ttf', max(14, Wi // 70))
    for (x, y, t) in labels: d.text((x, y), t, fill=(236, 226, 206), font=f)
    mark = 'DICTO · dictospheres.com'; fm = ImageFont.truetype(FD + 'DejaVuSans.ttf', max(12, Wi // 95))
    d.text((Wi - int(Wi * 0.015), im.size[1] - int(Wi * 0.012)), mark, fill=(200, 160, 72), font=fm, anchor='rd')
    try:
        lg = Image.open(os.path.join(HERE, '..', 'data', 'dicto-logo.png')).convert('RGBA'); hh = int(Wi * 0.035)
        lg = lg.resize((int(lg.size[0] * hh / lg.size[1]), hh), Image.LANCZOS)
        im.paste(lg, (Wi - int(Wi * 0.015) - int(d.textlength(mark, font=fm)) - lg.size[0] - 12, im.size[1] - int(Wi * 0.012) - hh + 4), lg)
    except Exception as ex: print('logo not drawn:', ex)
    im.save(path, dpi=(300, 300)); print('saved', path, im.size, flush=True)
def pad_bottom(im, h):
    out = Image.new('RGB', (im.size[0], im.size[1] + h), GROUND); out.paste(im, (0, 0)); return out

