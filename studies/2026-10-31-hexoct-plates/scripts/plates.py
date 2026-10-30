# Full-page plates for the book "HexOct: The Hexagonality Law", version 6 (DICTO 2026-10-31: give the shapes room).
# Geometry is the book's own: the HexOct tile engine of #75 (studies/2026-10-29-endless-stack-cell/scripts: tiles.py, render_tiles.py,
# stackings.py, census engine of #53/#57), the HexOct-K counter of studies/2026-10-29-keyed-hexoct/scripts/counter.py, and the
# Rule of Halves pieces of #57 (power cells of the holes of ABAC). Colours as the book's figures: c-tile gold, h-tile blue
# (darker tetrahedral pieces, lighter octahedral halves); single tiles gold tetrahedral pieces, violet octahedral halves;
# Janus pieces hexagonal half blue, cubic half gold.
# Render standard (DICTO, firm): solid shaded faces, crisp dark edges, no haze, antialiased. Done here with an exact z-buffer:
# every visible face is found per pixel (3x supersampled), edges are drawn where the visible face changes, then averaged down.
# Each picture is 180 x 200 mm (one full A4 page inside the book's margins, ~70% of the page) and carries the DICTO mark.
# Usage (dicto-big-brother): ~/geom/bin/python plates.py [name ...]   -> ../out/plate-<name>.png and ../out/facts.txt
import sys, os, math, random, json
import numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
TILES_DIR = os.environ.get('TILES_DIR', os.path.join(HERE, '../../2026-10-29-endless-stack-cell/scripts'))
KEYED_DIR = os.environ.get('KEYED_DIR', os.path.join(HERE, '../../2026-10-29-keyed-hexoct/scripts'))
sys.path.insert(0, TILES_DIR)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from tiles import tile, types, build, corners, half
from engine import Cell
from stackings import POS
LOGO = os.environ.get('LOGO', os.path.join(HERE, '../../../papers/dicto-logo.png'))
OUT = os.path.join(HERE, '../out')
D = (2 / 3) ** 0.5
W_MM, H_MM = 180, 200
PX_PER_MM = 10                       # 1800 x 2000 px, 254 dpi on the page
W, H = W_MM * PX_PER_MM, H_MM * PX_PER_MM
SS = 3                               # supersampling
EDGE = '#1c1c1c'
FACTS = {}

def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * 3 ** 0.5 / 2, float(p[2]) * D])

def hex2rgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])

# ---------- geometry -> faces ----------
def polyfaces(P):
    """Convex body (N x 3) -> list of (ordered polygon, outward unit normal)."""
    h = ConvexHull(P); groups = {}
    for s, eq in zip(h.simplices, h.equations):
        key = tuple(np.round(eq, 6)); groups.setdefault(key, [eq, set()])[1].update(s)
    F = []
    for eq, idx in groups.values():
        Q = P[sorted(idx)]; c = Q.mean(0); n = np.array(eq[:3]); n /= np.linalg.norm(n)
        u = Q[0] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        F.append((Q[np.argsort(np.arctan2((Q - c) @ v, (Q - c) @ u))], n))
    return F

class View:
    def __init__(self, elev, azim):
        e, a = math.radians(elev), math.radians(azim)
        self.f = -np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])   # into the scene
        self.r = np.cross(self.f, [0, 0, 1.0]); self.r /= np.linalg.norm(self.r)
        self.u = np.cross(self.r, self.f)
        L1 = -self.f * 0.55 + self.u * 0.65 - self.r * 0.45; self.L1 = L1 / np.linalg.norm(L1)
        L2 = -self.f * 0.6 + self.r * 0.7 - self.u * 0.2; self.L2 = L2 / np.linalg.norm(L2)
    def proj(self, P): P = np.atleast_2d(P); return np.c_[P @ self.r, P @ self.u, P @ self.f]

def shade(rgb, n, view):
    k = 0.56 + 0.40 * max(0.0, float(n @ view.L1)) + 0.14 * max(0.0, float(n @ view.L2))
    return np.clip(rgb * k, 0, 1)

def render(bodies, view, w, h, scale=None, center=None, pad=0.06, edge_px=2.4):
    """bodies: list of (N x 3 points, hex colour). Returns (RGB float image h x w, mapping fn world->pixel, scale, center)."""
    faces = []
    for P, col in bodies:
        rgb = hex2rgb(col)
        for Q, n in polyfaces(np.asarray(P, float)):
            if n @ view.f < -1e-9: faces.append((Q, shade(rgb, n, view)))
    allp = view.proj(np.vstack([np.asarray(P, float) for P, _ in bodies]))
    lo, hi = allp[:, :2].min(0), allp[:, :2].max(0)
    if center is None: center = (lo + hi) / 2
    if scale is None: scale = min(w * (1 - 2 * pad) / (hi[0] - lo[0]), h * (1 - 2 * pad) / (hi[1] - lo[1]))
    sw, sh = w * SS, h * SS
    def to_px(X):
        X = view.proj(X); return np.c_[(X[:, 0] - center[0]) * scale * SS + sw / 2, sh / 2 - (X[:, 1] - center[1]) * scale * SS, X[:, 2]]
    zb = np.full((sh, sw), np.inf, np.float32); ib = np.full((sh, sw), -1, np.int32)
    for fi, (Q, _) in enumerate(faces):
        T = to_px(Q)
        for k in range(1, len(T) - 1):
            a, b, c = T[0], T[k], T[k + 1]
            x0, x1 = int(max(0, math.floor(min(a[0], b[0], c[0])))), int(min(sw - 1, math.ceil(max(a[0], b[0], c[0]))))
            y0, y1 = int(max(0, math.floor(min(a[1], b[1], c[1])))), int(min(sh - 1, math.ceil(max(a[1], b[1], c[1]))))
            if x1 < x0 or y1 < y0: continue
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(den) < 1e-12: continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l1 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Y - c[1])) / den
            l2 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Y - c[1])) / den
            l3 = 1 - l1 - l2; eps = -1e-6
            m = (l1 >= eps) & (l2 >= eps) & (l3 >= eps)
            if not m.any(): continue
            z = (l1 * a[2] + l2 * b[2] + l3 * c[2]).astype(np.float32)
            zs = zb[y0:y1 + 1, x0:x1 + 1]; ids = ib[y0:y1 + 1, x0:x1 + 1]
            m &= z < zs - 1e-5
            zs[m] = z[m]; ids[m] = fi
    cols = np.vstack([np.ones(3)] + [c for _, c in faces])
    img = cols[ib + 1]
    e = np.zeros((sh, sw), bool)
    e[:, 1:] |= ib[:, 1:] != ib[:, :-1]; e[1:, :] |= ib[1:, :] != ib[:-1, :]
    r = max(1, int(round(edge_px * SS / 2)))
    d = e.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(e, dy, 0), dx, 1)
    img[d] = hex2rgb(EDGE)
    img = img.reshape(h, SS, w, SS, 3).mean((1, 3))
    def world_to_px(X):
        T = to_px(np.atleast_2d(X)); return T[:, 0] / SS, T[:, 1] / SS
    return img, world_to_px, scale, center

def canvas(): return np.ones((H, W, 3))

def save(name, img, labels=(), dots=()):
    """labels: (x_px, y_px, text, dict(kwargs)); dots: (x_px, y_px, radius_px)."""
    fig = plt.figure(figsize=(W / 254, H / 254), dpi=254)
    ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(np.clip(img, 0, 1), interpolation='lanczos'); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    for x, y, rr in dots: ax.add_patch(plt.Circle((x, y), rr, color='black', zorder=5))
    for x, y, t, kw in labels:
        kw = dict(dict(fontsize=11, color='#333', ha='center', va='center', family='DejaVu Sans'), **kw); ax.text(x, y, t, **kw)
    lg = plt.imread(LOGO); lw = 120
    ax.imshow(lg, extent=(W - lw - 20, W - 20, H - 20, H - 20 - lw * lg.shape[0] / lg.shape[1]), zorder=6)
    ax.text(W - lw - 34, H - 20 - lw * lg.shape[0] / lg.shape[1] / 2, 'DICTO · dictospheres.com', ha='right', va='center', fontsize=8, color='#777')
    os.makedirs(OUT, exist_ok=True); fig.savefig(os.path.join(OUT, f'plate-{name}.png'), dpi=254); plt.close(fig); print('saved', name, flush=True)

def paste(dst, src, x, y): dst[y:y + src.shape[0], x:x + src.shape[1]] = src

# ---------- the two tiles ----------
TCOL = {('oct', True): '#8a5cc2', ('oct', False): '#b48ae0', 'tet': '#d9a521'}
def tile_bodies(word, L, lam, gap):
    P, _ = tile(word, L, lam); out = []
    for k, up, s, pts, J in P:
        Q = np.array([cart(p) for p in pts])
        dz = {('oct', True): -1, ('oct', False): 1}.get((k, up), 0) * gap
        if k == 'tet': dz = gap * 0.35 * (1 if s[2] > 0 else -1)
        out.append((Q + [0, 0, dz], TCOL[(k, up)] if k == 'oct' else TCOL['tet']))
    return out

def plate_tile(name, word, L, lam=Fr(1, 10)):
    v = View(16, -58); img = canvas(); dots = []; labels = []
    whole = tile_bodies(word, L, lam, 0.0); apart = tile_bodies(word, L, lam, 0.6)
    bh = H // 2 - 40
    a, fa, sc, cen = render(apart, v, W, bh)                 # common scale: the drawn-apart view is the larger one
    b, fb, _, _ = render(whole, v, W, bh, scale=sc)
    paste(img, b, 0, 30); paste(img, a, 0, 30 + bh + 20)
    for f, y0 in ((fb, 30), (fa, 30 + bh + 20)):
        x, y = f(np.zeros(3)); dots.append((x[0], y[0] + y0, 9))
    labels += [(W / 2, 40, 'whole', {}), (W / 2, 30 + bh + 30, 'drawn apart', {})]
    save(name, img, labels, dots)

# ---------- stackings built from the tiles ----------
SCOL = {'c': ('#d9a521', '#e8c25a'), 'h': ('#3f7fc4', '#7fb0e0')}
CACHE = {}
def tile_cached(word, L, lam):
    k = (word, L % len(word), lam)
    if k not in CACHE: CACHE[k] = tile(word, L % len(word), lam)[0]
    return CACHE[k]

def stack_bodies(word, nlayers, lam, gap, patch=((0, 0), (1, 0), (0, 1), (1, 1))):
    T = types(word); n = len(word); out = []
    for L in range(nlayers):
        P = tile_cached(word, L, lam); ball = POS[word[L % n]]
        for du, dv in patch:
            for k, up, s, pts, J in P:
                Q = np.array([cart((p[0] + ball[0] + du, p[1] + ball[1] + dv, p[2] + L)) for p in pts]) + [0, 0, gap * L]
                out.append((Q, SCOL[T[L % n]][k == 'oct']))
    return out

def plate_stacking(name, word, nlayers, lam=Fr(1, 10)):
    v = View(9, -60); T = types(word); n = len(word); img = canvas(); labels = []
    gap = 0.45 if nlayers <= 9 else 0.3
    half_w = (W - 160) // 2; bh = H - 120
    closed = stack_bodies(word, nlayers, lam, 0.0); apart = stack_bodies(word, nlayers, lam, gap)
    a, fa, sc, cen = render(apart, v, half_w, bh, pad=0.03)
    b, fb, _, _ = render(closed, v, half_w, bh, scale=sc, pad=0.03)
    x_cl, x_ap, y0 = 160, 160 + half_w, 70
    paste(img, b, x_cl, y0); paste(img, a, x_ap, y0)
    labels += [(x_cl + half_w / 2, 40, 'closed', {}), (x_ap + half_w / 2, 40, 'layers drawn apart', {})]
    for L in range(nlayers):
        t = T[L % n]; c = cart((Fr(1, 2) + POS[word[L % n]][0], Fr(1, 2) + POS[word[L % n]][1], L))
        _, y = fb(c)
        labels.append((60, y[0] + y0, f'{word[L % n]}  {t}', dict(fontsize=12, color=SCOL[t][0], weight='bold', family='DejaVu Sans Mono')))
    labels.append((60, 40, 'position\n& type', dict(fontsize=8, color='#777')))
    FACTS[name] = dict(word=word, layers=nlayers, types=''.join(T), n_h=T.count('h'), n=n)
    save(name, img, labels)

# ---------- Rule of Halves pieces (#57), ABAC: layer 0 cubic, layer 1 hexagonal ----------
def piece(word, idx, lam):
    net, spec = build(word); n = len(word)
    c = Cell(net, idx, (lam,), Fr(12)); X = corners(c, lam); site = spec['motif'][idx][1]
    toc = lambda p: cart((p[0], p[1], p[2] * n))
    return c, X, site, toc

def plate_janus(name, lam):
    c, X, site, toc = piece('ABAC', 0, lam)
    top = np.array([toc(p) for p in half(c, X, site[2], True)]); bot = np.array([toc(p) for p in half(c, X, site[2], False)])
    whole = np.array([toc(p) for p in X])
    hv = ConvexHull(whole); FACTS[name] = dict(corners=len(X), volume=hv.volume, faces=sorted(len(Q) for Q, _ in polyfaces(whole)))
    v = View(18, -50); img = canvas(); bh = H // 2 - 40
    g = 0.22 * (whole[:, 2].max() - whole[:, 2].min())
    a, fa, sc, _ = render([(top + [0, 0, g], '#3f7fc4'), (bot - [0, 0, g], '#d9a521')], v, W, bh)
    b, _, _, _ = render([(top, '#3f7fc4'), (bot, '#d9a521')], v, W, bh, scale=sc)
    paste(img, b, 0, 30); paste(img, a, 0, 30 + bh + 20)
    save(name, img, [(W / 2, 40, 'whole', {}), (W / 2, 30 + bh + 30, 'drawn apart at the mid-plane', {})])

def plate_tt(name, lam=Fr(5, 24)):
    c, X, site, toc = piece('ABAC', 2, lam)
    P = np.array([toc(p) for p in X]); hv = ConvexHull(P)
    FACTS[name] = dict(corners=len(X), volume=hv.volume, faces=sorted(len(Q) for Q, _ in polyfaces(P)))
    img = canvas(); bh = H // 2 - 40
    a, _, sc, _ = render([(P, '#d9a521')], View(18, -50), W, bh)
    b, _, _, _ = render([(P, '#d9a521')], View(-18, 130), W, bh, scale=sc)
    paste(img, a, 0, 30); paste(img, b, 0, 30 + bh + 20)
    save(name, img, [(W / 2, 40, 'from above', {}), (W / 2, 30 + bh + 30, 'from below, turned', {})])

# ---------- HexOct-K: the layer that counts (counter.py) ----------
def plate_counter(name):
    sys.path.insert(0, KEYED_DIR); from counter import fillings
    from matplotlib.patches import RegularPolygon
    Wt, Ht = 4, 16; sols = fillings(Wt, Ht); sol = sols[0]
    FACTS[name] = dict(fillings=len(sols))
    fig = plt.figure(figsize=(W / 254, H / 254), dpi=254); ax = fig.add_axes([0.02, 0.04, 0.96, 0.92])
    for v in range(Ht):
        for u in range(Wt):
            b = 0 if v == 0 else sol[(v, u)]; x, y = u + v / 2, v * math.sqrt(3) / 2
            ax.add_patch(RegularPolygon((x, y), 6, radius=0.56, orientation=0, facecolor='#d9a521' if b else '#f3efe4', edgecolor=EDGE, lw=1.3))
            ax.text(x, y, str(b), ha='center', va='center', fontsize=11, color='#222')
        ax.text(Wt - 0.25 + v / 2, v * math.sqrt(3) / 2, f'= {v}', ha='left', va='center', fontsize=11, color='#444')
    ax.text(Wt - 0.45, -0.85, 'carry 1 enters every row', fontsize=9.5, color='#444')
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-0.8, Wt + Ht / 2 + 0.9); ax.set_ylim(-1.2, Ht * math.sqrt(3) / 2 + 0.2)
    lg = plt.imread(LOGO); la = fig.add_axes([1 - 0.075, 0.008, 0.065, 0.065 * W / H]); la.imshow(lg); la.axis('off')
    fig.text(1 - 0.085, 0.008 + 0.0325 * W / H, 'DICTO · dictospheres.com', ha='right', va='center', fontsize=8, color='#777')
    fig.savefig(os.path.join(OUT, f'plate-{name}.png'), dpi=254); plt.close(fig); print('saved', name, flush=True)

def random_word(n, seed):
    rnd = random.Random(seed)
    while True:
        s = [rnd.choice((1, -1)) for _ in range(n)]
        if sum(s) % 3: continue
        pos = [0]
        for x in s[:-1]: pos.append((pos[-1] + x) % 3)
        w = ''.join('ABC'[p] for p in pos)
        if all(w[i] != w[(i + 1) % n] for i in range(n)): return w

PLATES = {
    'c-tile': lambda: plate_tile('c-tile', 'ABC', 1),
    'h-tile': lambda: plate_tile('h-tile', 'AB', 0),
    'hexoct-k': lambda: plate_counter('hexoct-k'),
    '3C': lambda: plate_stacking('3C', 'ABC', 6),
    '2H': lambda: plate_stacking('2H', 'AB', 6),
    '4H': lambda: plate_stacking('4H', 'ABCB', 8),
    '6H': lambda: plate_stacking('6H', 'ABCACB', 6),
    '9R': lambda: plate_stacking('9R', 'ABACACBCB', 9),
    'fibonacci': lambda: plate_stacking('fibonacci', 'ABACBCACBABCACBC', 16),
    'random': lambda: plate_stacking('random', random_word(12, 2026), 12),
    'chucky': lambda: plate_janus('chucky', Fr(-3, 8)),
    'fang': lambda: plate_janus('fang', Fr(5, 24)),
    'tt': lambda: plate_tt('tt'),
}
if __name__ == '__main__':
    for k in (sys.argv[1:] or list(PLATES)): PLATES[k]()
    fp = os.path.join(OUT, 'facts.json'); old = json.load(open(fp)) if os.path.exists(fp) else {}
    old.update(FACTS); json.dump(old, open(fp, 'w'), indent=1, default=str); print(json.dumps(FACTS, default=str))
