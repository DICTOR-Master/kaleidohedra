# Front cover of "Space-Fillers and Lattice Moves" (cover design by DICTO, 11-07): a Fibonacci rock salt, with the Fibonacci
# word in LED letters as its basis (c cubic blue, h hexagonal gold), and the series title panel (as The Golden Ladder).
# Geometry and colours exactly as the Fibonacci tower (HexOct Figure 7.1; studies/2026-10-28-fibonacci-stackings/tower69.py):
# rock salt (power cells, ball weight lam = 1/3) on the 16-layer Fibonacci approximant ABACBCACBABCACBC; ball piece of every
# layer and octahedral piece of every gap, each drawn at offsets 0, a1, a2. Painted here by a z-buffer (supersampled, glossy).
# A: stack runs left to right, one LED letter under each layer.  B: the stack stands as a tower, the word as its foundation line.
import os, sys, itertools
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy import ndimage
from PIL import Image
import ledtext as L
# ------------------------------------------------------------------ geometry (verbatim from tower69.py)
POS = {'A': (0, 0), 'B': (1 / 3, 1 / 3), 'C': (2 / 3, 2 / 3)}
LAM = 1 / 3; WORD = 'ABACBCACBABCACBC'
a1 = np.array([1.0, 0, 0]); a2 = np.array([0.5, np.sqrt(3) / 2, 0]); h = np.sqrt(2 / 3)
n = len(WORD); cz = n * h
def types(w): return ['h' if w[k - 1] == w[(k + 1) % len(w)] else 'c' for k in range(len(w))]
T = types(WORD)
S = []
for k in range(n):
    X, Y = WORD[k], WORD[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
    for role, P, f, w in (('S', X, 0, LAM), ('C', X, .75, 0), ('O', Z, .5, LAM), ('Y', Y, .25, 0)):
        u, v = POS[P]; S.append((role, k, u * a1 + v * a2 + np.array([0, 0, (k + f) * h]), w))
def cell(i):
    p, wp = S[i][2], S[i][3]; H = []
    for j, (r, k, q, w) in enumerate(S):
        for da, db, dc in itertools.product(range(-2, 3), range(-2, 3), (-1, 0, 1)):
            qq = q + da * a1 + db * a2 + np.array([0, 0, dc * cz])
            if j == i and da == db == dc == 0: continue
            if np.linalg.norm(qq - p) > 2.2: continue
            H.append(np.r_[2 * (qq - p), -(qq @ qq - p @ p - w + wp)])
    hs = HalfspaceIntersection(np.array(H), p); return hs.intersections, ConvexHull(hs.intersections)
COL = {('S', 'c'): '#5b9bd5', ('S', 'h'): '#d4af37', ('O', 'cc'): '#9ec3e6', ('O', 'ch'): '#c77dab', ('O', 'hc'): '#a8507f'}
hexrgb = lambda s: np.array([int(s[i:i + 2], 16) for i in (1, 3, 5)], float)
EDGE = hexrgb('#f0ead8'); BLUE_C = hexrgb(COL[('S', 'c')]); GOLD_H = hexrgb(COL[('S', 'h')])
AX = np.array([0.5, np.sqrt(3) / 6, 0])   # the rod's axis: through the B sites (the centre of A, B, C)
UH = np.array([[np.cos(t), np.sin(t)] for t in np.radians([30, 90, 150])])
hexd = lambda d: np.abs(UH @ d[:2]).max()   # hexagonal distance (apothem): the rod is a hexagonal prism of whole pieces
def pieces(R):
    """Every drawn piece, all lattice copies whose centre lies within R of the axis (a hexagonal rod of the crystal): (faces as ordered vertex arrays, outward normals, rgb, layer k)."""
    out = []
    for i, (role, k, p, w) in enumerate(S):
        if role not in ('S', 'O'): continue
        P0, hull = cell(i); kind = T[k] if role == 'S' else T[k] + T[(k + 1) % n]
        faces = {}
        for simp, eq in zip(hull.simplices, hull.equations): faces.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
        for i_, j_ in itertools.product(range(-int(2 * R) - 3, int(2 * R) + 4), repeat=2):
            shift = i_ * a1 + j_ * a2; c = P0.mean(0) + shift
            if hexd(c - AX) > R: continue
            P = P0 + shift; F = []
            for key, idx in faces.items():
                idx = list(idx); pts = P[idx]; nrm = np.array(key[:3]); ctr = pts.mean(0)
                e1 = pts[0] - ctr; e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
                F.append((pts[np.argsort(np.arctan2((pts - ctr) @ e2, (pts - ctr) @ e1))], nrm))
            out.append((F, hexrgb(COL[(role, kind)]), k))
    return out
# ------------------------------------------------------------------ painting
GROUND = (20, 15, 11); GOLD = (217, 165, 33); TEAL = (40, 165, 150); BLUE = (55, 115, 205); PINK = (199, 125, 171)   # DICTO 11-15: exactly the pink of the C/H design's octahedra (#c77dab)
W, Hc = 2400, 3394
def rot(a, b, c):
    Rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    Ry = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    Rz = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx
def render(PC, M, box, SS, letters=None):
    """Z-buffer painting of the pieces PC under the linear view M (world -> screen x right, y up, z towards the viewer),
    scaled to fit box = (x0, y0, x1, y1) of the cover; returns rgb, alpha (cover size of the box) and the map world -> pixel."""
    allv = np.vstack([f[0] for F, _, _ in PC for f in F]) @ M.T
    lo, hi = allv.min(0), allv.max(0); bw, bh = box[2] - box[0], box[3] - box[1]
    s = min(bw / (hi[0] - lo[0]), bh / (hi[1] - lo[1])); ox = box[0] + (bw - s * (hi[0] - lo[0])) / 2; oy = box[1] + (bh - s * (hi[1] - lo[1])) / 2
    to_px = lambda V: np.c_[ox + s * ((V @ M.T)[:, 0] - lo[0]), oy + s * (hi[1] - (V @ M.T)[:, 1])]
    Wb, Hb = int(bw) * SS, int(bh) * SS
    zb = np.full((Hb, Wb), -np.inf, np.float32); ib = np.full((Hb, Wb), -1, np.int32); nrm, cols, pid, rec = [], [], [], []
    for pi, (F, col, k) in enumerate(PC):
        for pts, nv in F:
            nn = M @ nv
            if nn[2] <= 1e-9: continue
            q = (to_px(pts) - [box[0], box[1]]) * SS; zz = (pts @ M.T)[:, 2] * s * SS
            x0, x1 = max(0, int(q[:, 0].min())), min(Wb, int(np.ceil(q[:, 0].max())) + 1)
            y0, y1 = max(0, int(q[:, 1].min())), min(Hb, int(np.ceil(q[:, 1].max())) + 1)
            if x1 <= x0 or y1 <= y0: continue
            yy, xx = np.mgrid[y0:y1, x0:x1] + 0.5; inside = np.ones(xx.shape, bool)
            area = np.sum(q[:, 0] * np.roll(q[:, 1], -1) - np.roll(q[:, 0], -1) * q[:, 1]); sg = np.sign(area)
            for a, b in zip(q, np.roll(q, -1, axis=0)):
                inside &= sg * ((b[0] - a[0]) * (yy - a[1]) - (b[1] - a[1]) * (xx - a[0])) >= 0
            # depth plane in pixel coords (screen y down): z = z0 - (nx (x - x0) - ny (y - y0)) / nz
            z = zz[0] - (nn[0] * (xx - q[0, 0]) - nn[1] * (yy - q[0, 1])) / nn[2]
            sub = zb[y0:y1, x0:x1]; win = inside & (z > sub)
            sub[win] = z[win]; ib[y0:y1, x0:x1][win] = len(nrm)
            nrm.append(nn); cols.append(col); pid.append(pi); rec.append((q, zz, nn, (x0, x1, y0, y1)))
    nrm, cols, pid = np.array(nrm), np.array(cols), np.array(pid)
    # glossy shading: key light from upper left front, a point-light highlight, faint rim from below right
    fg = ib >= 0; N = np.zeros((Hb, Wb, 3), np.float32); N[fg] = nrm[ib[fg]]; C = np.zeros((Hb, Wb, 3), np.float32); C[fg] = cols[ib[fg]]
    l = np.array([-0.45, 0.62, 0.64]); l /= np.linalg.norm(l)
    diff = np.clip(N @ l, 0, 1); rim = np.clip(N @ (np.array([0.5, -0.6, 0.3]) / np.linalg.norm([0.5, -0.6, 0.3])), 0, 1)
    yy, xx = np.mgrid[0:Hb, 0:Wb].astype(np.float32)
    Lp = np.stack([(-0.15 * Wb - xx), (yy + 0.6 * Hb), np.full_like(xx, 1.2 * max(Wb, Hb))], -1)   # pixel -> light (y up)
    Lp /= np.linalg.norm(Lp, axis=-1, keepdims=True); Hv = Lp + np.array([0, 0, 1], np.float32); Hv /= np.linalg.norm(Hv, axis=-1, keepdims=True)
    spec = np.clip(np.sum(N * Hv, -1), 0, 1) ** 30
    rgb = C * (0.32 + 0.58 * diff)[..., None] + 255 * (0.24 * spec + 0.05 * rim ** 3)[..., None]
    rgb[~fg] = GROUND
    if letters: paint_letters(rgb, zb, ib, rec, pid, PC, M, SS, letters)
    # light edges: boundaries of the face buffer (creases, piece seams and the silhouette), widened to ~2 px
    e = np.zeros((Hb, Wb), bool); e[:, :-1] |= ib[:, :-1] != ib[:, 1:]; e[:-1] |= ib[:-1] != ib[1:]
    e = ndimage.binary_dilation(e, iterations=max(1, SS - 1))
    ea = ndimage.gaussian_filter(e.astype(np.float32), SS * 0.35) * 0.92
    rgb = rgb * (1 - ea[..., None]) + EDGE * ea[..., None]
    alpha = np.maximum(fg.astype(np.float32), ea)
    rgb = np.clip(rgb, 0, 255).astype(np.uint8); a8 = (alpha * 255).astype(np.uint8)
    rgb = np.array(Image.fromarray(rgb).resize((int(bw), int(bh)), Image.LANCZOS), float)
    al = np.array(Image.fromarray(a8).resize((int(bw), int(bh)), Image.LANCZOS), float) / 255
    return rgb, np.clip(al, 0, 1), to_px
def glyph_masks(ch, size=320):
    """LED letter (DSEG14, closed as in ledtext.glyph) as ink and outline masks, cropped to the ink plus the outline."""
    from PIL import ImageDraw, ImageFont
    f = ImageFont.truetype('DSEG14Classic-Regular.ttf', size); pad = size // 2
    m = Image.new('L', (size + 2 * pad, int(size * 1.4) + 2 * pad), 0); ImageDraw.Draw(m).text((pad, pad), ch, font=f, fill=255)
    a = np.array(m) > 128; r = max(2, int(size * 0.05)); yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    a = ndimage.binary_closing(np.pad(a, r + 2), structure=xx ** 2 + yy ** 2 <= r * r)[r + 2:-(r + 2), r + 2:-(r + 2)]
    e = max(3, size // 16); ys, xs = np.where(a); a = a[ys.min() - e:ys.max() + e + 1, xs.min() - e:xs.max() + e + 1]
    yy, xx = np.mgrid[-e:e + 1, -e:e + 1]; o = ndimage.binary_dilation(a, structure=xx ** 2 + yy ** 2 <= e * e) & ~a
    return ndimage.gaussian_filter(a.astype(np.float32), 1.0), ndimage.gaussian_filter(o.astype(np.float32), 1.0)
GLYPHS = {}
INK = {'C': np.array([255, 205, 70.]), 'H': np.array([110, 160, 255.])}   # reciprocal colours (DICTO 11-03 rule): C in bright gold, H in bright blue
OUTLINE = np.array([0, 0, 0.])   # black rim round the glyph
def paint_letters(rgb, zb, ib, rec, pid, PC, M, SS, letters):
    """The layer's letter on every visible face of every lettered piece: upright along the stacking axis, as large as fits the face."""
    ax = M @ np.array([0, 0, 1.0]); n_done = 0
    l = np.array([-0.45, 0.62, 0.64]); l /= np.linalg.norm(l)
    best = {}   # one face per piece (DICTO 11-07: "natural places, not fake"): its face most turned to the viewer, if visible
    for fid, (q, zz, nn, bb) in enumerate(rec):
        if letters(PC[pid[fid]]) is None: continue
        area = abs(np.sum(q[:, 0] * np.roll(q[:, 1], -1) - np.roll(q[:, 0], -1) * q[:, 1])) / 2
        if (ib[bb[2]:bb[3], bb[0]:bb[1]] == fid).sum() < 0.6 * area: continue   # mostly hidden by pieces in front
        sc = nn[2] / np.linalg.norm(nn) * area ** 0.5
        if sc > best.get(pid[fid], (-1, None))[0]: best[pid[fid]] = (sc, fid)
    for _, fid in best.values():
        q, zz, nn, (x0, x1, y0, y1) = rec[fid]; ch = letters(PC[pid[fid]])
        if nn[2] < 0.22: continue
        n_ = nn / np.linalg.norm(nn); up = ax - (ax @ n_) * n_
        if np.linalg.norm(up) < 0.35: up = np.array([0, 1.0, 0]) - n_[1] * n_
        up /= np.linalg.norm(up); rt = np.cross(up, n_)
        Q = np.c_[q[:, 0], -q[:, 1], zz]; c = Q.mean(0); U = np.c_[(Q - c) @ rt, (Q - c) @ up]
        if ch not in GLYPHS: GLYPHS[ch] = glyph_masks(ch)
        ink, out = GLYPHS[ch]; gh, gw = ink.shape; w, h = gw / gh, 1.0
        sg = np.sign(np.sum(U[:, 0] * np.roll(U[:, 1], -1) - np.roll(U[:, 0], -1) * U[:, 1])); t = np.inf
        for a, b in zip(U, np.roll(U, -1, axis=0)):
            m = sg * np.array([-(b[1] - a[1]), b[0] - a[0]])
            for cx, cy in ((w / 2, h / 2), (-w / 2, h / 2), (w / 2, -h / 2), (-w / 2, -h / 2)):
                mc = m @ (cx, cy)
                if mc < 0: t = min(t, (m @ a) / mc)
        t *= 0.78
        if not np.isfinite(t) or t * nn[2] < 15 * SS: continue   # too small or too slanted to read: leave the face plain
        sub = ib[y0:y1, x0:x1] == fid
        if not sub.any(): continue
        yy, xx = np.nonzero(sub); P = np.c_[xx + x0 + 0.5, -(yy + y0 + 0.5), zb[y0:y1, x0:x1][sub]] - c
        u, v = P @ rt, P @ up; gx = (u / (t * w) + 0.5) * (gw - 1); gy = (0.5 - v / t) * (gh - 1)
        ai = ndimage.map_coordinates(ink, [gy, gx], order=1, cval=0); ao = ndimage.map_coordinates(out, [gy, gx], order=1, cval=0)
        px = rgb[y0:y1, x0:x1][sub]; px = px * (1 - 0.95 * ao[:, None]) + OUTLINE * 0.95 * ao[:, None]
        shade = 0.42 + 0.58 * max(0.0, (nn / np.linalg.norm(nn)) @ l)   # the glyph is lit like its face (darker on faces turned away)
        px = px * (1 - 0.95 * ai[:, None]) + INK[ch] * shade * 0.95 * ai[:, None]; rgb[y0:y1, x0:x1][sub] = px; n_done += 1
    print('letters painted on', n_done, 'faces', flush=True)
def put(canvas, rgb, al, x, y):
    h_, w_ = al.shape; c = canvas[y:y + h_, x:x + w_]; canvas[y:y + h_, x:x + w_] = c * (1 - al[..., None]) + rgb * al[..., None]
def title_panel(canvas, top):
    N = W; sz = int(N * 0.064)
    t1 = L.word('SPACE-FILLERS', sz, lambda ch: GOLD, big=(0, 6))
    t2 = L.word('& LATTICE MOVES', sz, lambda ch: GOLD, big=(0, 2, 10))   # DICTO 11-15: '&' as on all covers
    sub = L.word('PIECES THAT FILL SPACE ALONE, TOGETHER & HELD', int(N * 0.0225), lambda ch: TEAL, big=(0, 12, 17, 23, 30, 41))
    by = L.word('* DICTO *', int(N * 0.040), lambda ch: PINK, big=(0, 2, 3, 4, 5, 6, 8))   # DICTO 11-15: DICTO in pink, back cover too
    y = L.paste(canvas, t1, N / 2, top); y = L.paste(canvas, t2, N / 2, y + 40); y = L.paste(canvas, sub, N / 2, y + 75)
    return L.paste(canvas, by, N / 2, y + 85)
VIEW = {   # version: (rod apothem, view, picture box (x0, x1, max height))
    'A': (2.6, lambda: rot(np.radians(-26), 0, 0) @ rot(0, np.radians(-14), 0) @ np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float), (90, W - 90, 1700)),
    'B': (2.05, lambda: rot(np.radians(20), 0, 0) @ rot(0, np.radians(30), 0) @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float), (300, W - 300, 1780)),
    'C': (float(os.environ.get('CR', 8.0)), lambda: rot(np.radians(float(os.environ.get('CA', 13))), 0, 0) @ rot(0, np.radians(30), 0) @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float), (180, W - 180, 2060)),
}   # A: stacking axis to the right (as tower69); B: stacking axis up (in-plane x right)
def make(version, SS=3):
    R, Mf, (bx0, bx1, bh) = VIEW[version]; M = Mf(); PC = pieces(R); can = np.ones((Hc, W, 3)) * np.array(GROUND, float)
    TOP = 2200   # picture area (65 %)
    letters = None
    if version == 'C':   # the fat pillar: hidden inner pieces dropped (speed only); every ball piece carries its layer's letter
        cen = lambda F: np.vstack([f[0] for f in F]).mean(0)
        PC = [p for p in PC if hexd(cen(p[0]) - AX) > R - 1.8 or p[2] >= n - 3]
        letters = lambda p: T[p[2]].upper() if tuple(p[1]) in (tuple(BLUE_C), tuple(GOLD_H)) else None
    rgb, al, to_px = render(PC, M, (bx0, 0, bx1, bh), SS, letters)
    ys, xs_ = np.where(al > 0.01); y0, y1 = ys.min(), ys.max() + 1; rgb, al = rgb[y0:y1], al[y0:y1]
    # the basis: the layer-type word, one LED letter per layer, in the order of the layers shown
    lsz = 108 if version == 'A' else 104
    if version == 'A':   # under its layer: the x where the layer's plane meets the front of the rod (the side facing the viewer)
        v = M.T @ np.array([0, 0, 1.0]); v[2] = 0; v *= R / np.linalg.norm(v)
        xs = np.array([to_px(AX[None] + v + [[0, 0, k * h]])[0, 0] for k in range(n)])
        ball = lambda col: tuple(col) in (tuple(BLUE_C), tuple(GOLD_H))   # nudge the even row onto the front balls of each layer
        off = []
        for k in range(n):
            B = np.array([np.vstack([f[0] for f in F]).mean(0) for F, col, kk in PC if kk == k and ball(col)]); d = (B @ M.T)[:, 2]
            off.append(to_px(B[d > np.percentile(d, 70)])[:, 0].mean() - xs[k])
        xs = xs + np.mean(off)
    else:                # the foundation line under the standing tower, first layer (the bottom one) on the left
        xs = list(W / 2 + (np.arange(n) - 7.5) * 116)
    print(version, 'picture', al.shape[1] if False else int(np.ptp(xs_)) + 1, 'x', y1 - y0, 'px', flush=True)
    gs = [L.word(T[k].upper(), lsz, lambda ch: BLUE_C if ch == 'C' else GOLD_H) for k in range(n)]
    if version == 'C': gs = []   # DICTO 11-07: no word underneath ("those that know know"); the letters live on the pieces
    gap = 70 if gs else 0; wh = max([g[1].shape[0] for g in gs] + [0]); group = (y1 - y0) + gap + wh
    top = int((TOP - group) / 2) + (50 if gs else 30); assert top >= 60, ('picture too tall', top)
    put(can, rgb, al, bx0, top)
    for g, x in zip(gs, xs): L.paste(can, g, x, top + (y1 - y0) + gap + (wh - g[1].shape[0]))
    title_panel(can, TOP + 40)
    fn = f'../space-fillers-cover-{version}.png'; Image.fromarray(np.clip(can, 0, 255).astype(np.uint8)).save(fn); print('saved', fn, 'rod pieces', len(PC), flush=True)
if __name__ == '__main__':
    vs = sys.argv[1:] or ['A', 'B', 'C']
    print('layer word', ''.join(T), 'from', WORD, flush=True)
    for v in vs: make(v)
    # the ◆ DICTO ◆ mark alone (transparent), for the back cover, in the same pink as the front (DICTO 11-15: "back cover same")
    mk = L.word('* DICTO *', int(W * 0.06), lambda ch: PINK, big=(0, 2, 3, 4, 5, 6, 8))
    Image.fromarray(np.dstack([np.clip(mk[0], 0, 255), mk[1] * 255]).astype(np.uint8), 'RGBA').save('../space-fillers-dicto-mark-back.png'); print('saved back mark', flush=True)
    ok = all(os.path.exists(f'../space-fillers-cover-{v}.png') and Image.open(f'../space-fillers-cover-{v}.png').size == (W, Hc) for v in vs)
    print('FINAL ok' if ok else 'FINAL FAIL (cover missing or wrong size)')
