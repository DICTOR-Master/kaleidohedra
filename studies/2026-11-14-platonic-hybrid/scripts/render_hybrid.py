# render_hybrid.py (14 Nov 2026) - DICTO · dictospheres.com
# Figure: the hybrid golden slab, drawn apart in two tiers. Middle tier: on alternate cubes of edge phi, dodecahedra of edge 1
# (violet) and icosahedra of edge 1 (blue) in their glass skins (6 Admiral Caps + 8 caps, together the same dodecahedral
# cell); Dogstars (pale violet glass) in the other cubes. Top tier, lifted: the edging of one face (lifted), plates Z (gold glass, a
# phi x phi x 1/2 plate with a roof-shaped hollow underneath) over every cell, and over every Dogstar a roof R (amber) hanging
# point-down into its hollow, then Z + R making a full plate. The bottom face is the same turned over (not drawn).
# House render standard: solid faces with a depth buffer (no painter's errors), crisp antialiased edges (3x supersampling,
# hidden edges removed), element colours (DICTO square), the DICTO mark. Pieces come from the checked builder (hybrid.py).
# Usage: render_hybrid.py <out.png> [width_px]   -> PROGRESS lines, FINAL ok / FINAL FAIL
import sys, os, itertools, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 2400
sys.argv = sys.argv[:1]                                # hybrid.py reads its own arguments at import
import golden as G, hybrid as H
phi = (1 + 5 ** 0.5) / 2
CELLS = {(0, 0): 'D', (2, 0): 'I', (1, 1): 'I', (3, 1): 'D', (0, 2): 'I', (2, 2): 'D', (4, 0): 'D', (4, 2): 'I', (1, -1): 'D', (3, -1): 'I'}
NI, NJ = range(0, 5), range(0, 3)
kinds = lambda i, j, k=0: CELLS.get((i, j), 'D')
LIFT = 3.2                                            # the edging tier is drawn lifted by this much
P = H.golden_slab('RZ', R=5, kinds=kinds)
def col_of(pc):
    c = np.mean([[float(x) for x in v] for p in pc[1] for v in p.verts], 0)
    if pc[0] in ('A', 'cap'):                          # skin pieces reach past the cube: assign to the nearest cell centre
        i, j = min(((i, j) for i in range(-6, 7) for j in range(-6, 7) if (i + j) % 2 == 0),
                   key=lambda t: (c[0] - t[0] * phi) ** 2 + (c[1] - t[1] * phi) ** 2); return i, j, c[2]
    return int(round(c[0] / phi)), int(round(c[1] / phi)), c[2]
keep = []
for pc in P:
    i, j, zc = col_of(pc)
    if i not in NI or j not in NJ: continue
    lab = pc[0]
    if lab in ('Z',) and zc < 0: continue              # bottom edging not drawn
    if lab == 'R' and zc < float(phi) / 2: continue
    keep.append(pc)
print('pieces drawn', len(keep), {l: sum(1 for p in keep if p[0] == l) for l in sorted(set(p[0] for p in keep))}, flush=True)
# ---- faces of a piece = union(pos) minus union(neg); pos/neg convex. Coplanar pos/neg faces with the same outward normal cancel.
def hull_faces(V):
    V = np.asarray(V, float); h = ConvexHull(V); groups = {}
    for simp, eq in zip(h.simplices, h.equations):
        groups.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
    out = []
    for key, idx in groups.items():
        n = np.array(key[:3]); idx = list(idx); c = V[idx].mean(0); u = V[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((V[i] - c) @ w, (V[i] - c) @ u)); out.append((n, key[3], V[idx]))
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
STYLE = {  # label: (rgb, alpha, edge rgb, edge width factor)
    'D': ((138, 92, 196), 1.0), 'I': ((58, 112, 205), 1.0), 'R': ((214, 146, 64), 1.0),
    'S': ((176, 150, 214), 0.20), 'A': ((150, 190, 235), 0.10), 'cap': ((150, 190, 235), 0.10), 'Z': ((236, 204, 120), 0.30)}
GOLD = (222, 178, 80); GROUND = (20, 15, 11)
# ---- view
def rot(ax, a):
    c, s = np.cos(a), np.sin(a); i, j = [(1, 2), (0, 2), (0, 1)][ax]; R = np.eye(3); R[i, i] = R[j, j] = c; R[i, j] = -s; R[j, i] = s; return R
Rm = rot(0, np.radians(-58)) @ rot(2, np.radians(-28))
L = np.array([-0.35, 0.55, 0.76]); L /= np.linalg.norm(L)
items = []
for pc in keep:
    lift = LIFT if pc[0] in ('Z', 'R') else 0.0
    for n, poly in piece_faces(pc):
        items.append((pc[0], n, poly + np.array([0, 0, lift])))
allp = np.vstack([p for _, _, p in items]) @ Rm.T
SS = 3; Wd = W * SS; pad = 0.05
spanx, spany = np.ptp(allp[:, 0]), np.ptp(allp[:, 1])
sc = Wd * (1 - 2 * pad) / spanx; Ht = int(spany * sc / (1 - 2 * pad)) + int(0.07 * Wd)
cx0, cy0 = allp[:, 0].min(), allp[:, 1].max()
def proj(p):
    q = p @ Rm.T; return np.column_stack([Wd * pad + (q[:, 0] - cx0) * sc, Wd * pad * 0.6 + (cy0 - q[:, 1]) * sc, q[:, 2]])
img = np.zeros((Ht, Wd, 3)); img[:] = GROUND; zb = np.full((Ht, Wd), -1e9)
def raster(tri, cb):
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
    xa, xb = int(max(0, np.floor(min(x0, x1, x2)))), int(min(Wd - 1, np.ceil(max(x0, x1, x2))))
    ya, yb = int(max(0, np.floor(min(y0, y1, y2)))), int(min(Ht - 1, np.ceil(max(y0, y1, y2))))
    if xb < xa or yb < ya: return
    X, Y = np.meshgrid(np.arange(xa, xb + 1) + 0.5, np.arange(ya, yb + 1) + 0.5)
    d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(d) < 1e-12: return
    a = ((y1 - y2) * (X - x2) + (x2 - x1) * (Y - y2)) / d; b = ((y2 - y0) * (X - x2) + (x0 - x2) * (Y - y2)) / d; c = 1 - a - b
    m = (a >= -1e-9) & (b >= -1e-9) & (c >= -1e-9)
    if not m.any(): return
    z = a * z0 + b * z1 + c * z2; cb(ya, xa, m, z)
def shade(n, rgb):
    nv = Rm @ n; nv = nv if nv[2] >= 0 else -nv
    k = 0.42 + 0.58 * max(0.0, nv @ L) + 0.10 * max(0.0, nv @ L) ** 12
    return np.array([min(255, c * k) for c in rgb])
# opaque pass
opaque = [it for it in items if STYLE[it[0]][1] >= 1]; glass = [it for it in items if STYLE[it[0]][1] < 1]
for lab, n, poly in opaque:
    col = shade(n, STYLE[lab][0]); s = proj(poly)
    for k in range(1, len(s) - 1):
        def cb(ya, xa, m, z):
            sub = zb[ya:ya + m.shape[0], xa:xa + m.shape[1]]; put = m & (z > sub)
            sub[put] = z[put]; img[ya:ya + m.shape[0], xa:xa + m.shape[1]][put] = col
        raster((s[0], s[k], s[k + 1]), cb)
print('PROGRESS 0.40 opaque faces', flush=True)
# edges (feature edges of every drawn face), depth-tested against the opaque buffer with a small polygon offset
EPS = 0.03 * sc / sc * 1.0; EW = max(2, int(W / 700)) * SS
def edge_list(sel):
    E = {}
    for lab, n, poly in sel:
        for a, b in zip(poly, np.roll(poly, -1, 0)):
            key = tuple(sorted([tuple(np.round(a, 6)), tuple(np.round(b, 6))]))
            E.setdefault(key, (lab, a, b))
    return list(E.values())
def draw_edges(E, rgb, width, alpha, zref):
    offs = [(dx, dy) for dx in range(-width // 2, width // 2 + 1) for dy in range(-width // 2, width // 2 + 1) if dx * dx + dy * dy <= (width / 2) ** 2]
    acc = np.zeros((Ht, Wd), bool)
    for lab, a, b in E:
        s = proj(np.array([a, b])); L_ = np.hypot(*(s[1, :2] - s[0, :2])); n = max(2, int(L_ * 2))
        t = np.linspace(0, 1, n)[:, None]; pts = s[0] * (1 - t) + s[1] * t
        xi = np.clip(pts[:, 0].astype(int), 0, Wd - 1); yi = np.clip(pts[:, 1].astype(int), 0, Ht - 1)
        vis = pts[:, 2] >= zref[yi, xi] - EPS
        for dx, dy in offs:
            acc[np.clip(yi[vis] + dy, 0, Ht - 1), np.clip(xi[vis] + dx, 0, Wd - 1)] = True
    img[acc] = img[acc] * (1 - alpha) + np.array(rgb) * alpha
draw_edges(edge_list(opaque), GOLD, EW, 1.0, zb)
print('PROGRESS 0.55 opaque edges', flush=True)
# glass pass: back to front, only in front of the opaque buffer
gl = sorted(glass, key=lambda it: (it[2] @ Rm.T)[:, 2].mean())
for lab, n, poly in gl:
    rgb, al = STYLE[lab]; col = shade(n, rgb); s = proj(poly)
    for k in range(1, len(s) - 1):
        def cb(ya, xa, m, z):
            sub = zb[ya:ya + m.shape[0], xa:xa + m.shape[1]]; put = m & (z > sub)
            blk = img[ya:ya + m.shape[0], xa:xa + m.shape[1]]; blk[put] = blk[put] * (1 - al) + col * al
        raster((s[0], s[k], s[k + 1]), cb)
print('PROGRESS 0.75 glass faces', flush=True)
for lab in ('A', 'cap', 'S', 'Z'):
    E = edge_list([it for it in glass if it[0] == lab])
    rgb = {'A': (170, 200, 240), 'cap': (170, 200, 240), 'S': (196, 176, 226), 'Z': GOLD}[lab]
    draw_edges(E, rgb, max(2, EW * 2 // 3), {'A': 0.35, 'cap': 0.35, 'S': 0.45, 'Z': 0.9}[lab], zb)
print('PROGRESS 0.85 glass edges', flush=True)
im = Image.fromarray(img.clip(0, 255).astype(np.uint8)).resize((W, Ht // SS), Image.LANCZOS)
d = ImageDraw.Draw(im); FD = '/usr/share/fonts/truetype/dejavu/'
f = ImageFont.truetype(FD + 'DejaVuSans.ttf', max(12, W // 95)); fb = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', max(12, W // 95))
leg = [('D', (138, 92, 196), 'dodecahedron'), ('I', (58, 112, 205), 'icosahedron in its skin'), ('S', (176, 150, 214), 'Dogstar'),
       ('R', (214, 146, 64), 'roof R'), ('Z', (236, 204, 120), 'plate Z')]
x = int(W * 0.03); y = im.size[1] - int(W * 0.045); sw = int(W * 0.014)
for _, rgb, txt in leg:
    d.rectangle([x, y, x + sw, y + sw], fill=rgb, outline=GOLD); d.text((x + sw + 8, y + sw / 2), txt, fill=(236, 226, 206), font=f, anchor='lm')
    x += sw + 20 + int(d.textlength(txt, font=f)) + int(W * 0.02)
mark = 'DICTO · dictospheres.com'; d.text((W - int(W * 0.015), im.size[1] - int(W * 0.012)), mark, fill=(200, 160, 72), font=f, anchor='rd')
try:
    lg = Image.open(os.path.join(HERE, '..', 'data', 'dicto-logo.png')).convert('RGBA'); hh = int(W * 0.035)
    lg = lg.resize((int(lg.size[0] * hh / lg.size[1]), hh), Image.LANCZOS)
    im.paste(lg, (W - int(W * 0.015) - int(d.textlength(mark, font=f)) - lg.size[0] - 12, im.size[1] - int(W * 0.012) - hh + 4), lg)
except Exception as ex: print('logo not drawn:', ex)
im.save(OUT, dpi=(300, 300)); print('saved', OUT, im.size)
# controls: every drawn piece is one the covering test checked (same builder); faces found for each; both cell kinds present
ok = all(len(piece_faces(pc)) > 0 for pc in keep) and {'D', 'I', 'S', 'R', 'Z'} <= {p[0] for p in keep}
print('FINAL ok' if ok else 'FINAL FAIL: a piece without faces or a kind missing')
