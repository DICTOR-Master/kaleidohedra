# Mock-up of the two ring-built HexOct tiles at lambda = -1/8 (DICTO 2026-10-31): every face split into its ring triangles
# (exact faces of build.py), each ring drawn as a translucent rounded-triangle band (width 12% of the side, inset so
# neighbouring rings sit side by side), the zip ties as short dark bars across each shared side at 1/4 and 3/4, the optional
# extra tie where the two c-towers touch. Painter's order (rings and ties sorted by depth); rings seen from behind drawn
# lighter, so one sees through the open centres to the rings behind.
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless LOGO=<dicto-logo.png> ~/geom/bin/python mockup.py
#   -> ../out/mockup-c.png, mockup-h.png, mockup-sheet.png
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build as B
import exactfaces as E
from tiles import tile
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
OUT = B.OUT
TINT = {'c': np.array([0.93, 0.80, 0.45]), 'h': np.array([0.55, 0.72, 0.93])}
EDGE = {'c': np.array([0.45, 0.33, 0.08]), 'h': np.array([0.12, 0.28, 0.50])}
INSET, WIDTH, K = 0.035, 0.12, 0.16           # fractions of the ring side

def ring_band(T):
    """T: 3 Cartesian corners. Returns (outer loop, inner loop) as N x 3 arrays."""
    T = [np.array(p) for p in T]; c = np.mean(T, 0)
    a = np.linalg.norm(T[1] - T[0]); r_in = a / (2 * 3 ** .5)
    P = [c + (p - c) * (1 - INSET * a / r_in) for p in T]
    pts = []
    for n in range(3):
        A, Bc, C = P[n - 1], P[n], P[(n + 1) % 3]
        p1 = Bc + (A - Bc) * K; p2 = Bc + (C - Bc) * K
        if pts: pts += list(np.linspace(pts[-1], p1, 6))[1:]
        for t in np.linspace(0, 1, 9):
            pts.append((1 - t) ** 2 * p1 + 2 * (1 - t) * t * Bc + t * t * p2)
    pts += list(np.linspace(pts[-1], pts[0], 6))[1:-1]
    outer = np.array(pts); f = 1 - WIDTH * a / (r_in * (1 - INSET * a / r_in))
    inner = c + (outer - c) * f
    return outer, inner

def model(t, w, L):
    P = tile(w, L, B.LAM)[0]; faces = B.split_edges(E.union_faces([p[3] for p in P]))
    rings, ties = [], {}
    for f in faces:
        n = B.cnormal(f)
        for T in B.rings_of(f):
            X = [B.cart(p) for p in T]; o, i = ring_band(X); c = np.mean(X, 0)
            rings.append(dict(outer=o, inner=i, n=n, c=c))
            for k in range(3):
                for s in (.25, .75):
                    p = X[k] + (X[(k + 1) % 3] - X[k]) * s
                    ties.setdefault(tuple(np.round(p, 6)), []).append((c, n))
    bars = []
    for p, cs in ties.items():
        p = np.array(p); assert len(cs) == 2, 'tie point not shared by two rings'
        a, b = [p + (c - p) / np.linalg.norm(c - p) * 0.07 for c, n in cs]
        bars.append((np.array([a, p, b]), cs[0][1] + cs[1][1]))
    extra = [np.zeros(3)] if t == 'c' else []
    return rings, bars, extra

class View(B.View):
    pass

def draw(ax, t, mdl, view, title=None, lw_tie=1.6):
    rings, bars, extra = mdl; items = []
    for r in rings:
        front = float(r['n'] @ view.f) < 0
        items.append((float(view.proj(r['c'])[0, 2]), 'ring', r, front))
    for b, nb in bars: items.append((float(view.proj(b[1])[0, 2]) - 0.01, 'bar', b, float(nb @ view.f) < 0))
    for e in extra: items.append((float(view.proj(e)[0, 2]) - 0.03, 'extra', e, True))
    items.sort(key=lambda x: -x[0])
    allp = view.proj(np.vstack([r['outer'] for r in rings]))[:, :2]
    tint, edge = TINT[t], EDGE[t]
    for d, kind, obj, front in items:
        if kind == 'ring':
            o = view.proj(obj['outer'])[:, :2]; i = view.proj(obj['inner'])[:, :2][::-1]
            path = Path(np.vstack([o, o[:1], i, i[:1]]), [Path.MOVETO] + [Path.LINETO] * (len(o) - 1) + [Path.CLOSEPOLY]
                        + [Path.MOVETO] + [Path.LINETO] * (len(i) - 1) + [Path.CLOSEPOLY])
            n = obj['n'] if front else -obj['n']
            sh = 0.62 + 0.30 * max(0.0, float(n @ view.L1)) + 0.12 * max(0.0, float(n @ view.L2))
            base = 0.55 * np.ones(3) + 0.45 * tint      # clear plastic, faint tint
            col = np.clip(base * sh + (0.08 if front else 0.18), 0, 1)
            ax.add_patch(PathPatch(path, facecolor=(*col, 0.78 if front else 0.42),
                                   edgecolor=(*(edge if front else 0.5 * edge + 0.5), 1.0 if front else 0.55),
                                   lw=1.1 if front else 0.7, zorder=2, joinstyle='round'))
        elif kind == 'bar':
            q = view.proj(obj)[:, :2]
            ax.plot(q[:, 0], q[:, 1], color='#1a1a1a' if front else '#a8a8a8', lw=lw_tie * (1 if front else 0.6), solid_capstyle='round', zorder=3)
        else:
            q = view.proj(obj)[0, :2]
            ax.plot(*q, marker='o', ms=11, mfc='none', mec='#141414', mew=2.6, zorder=3)
    lo, hi = allp.min(0), allp.max(0); pad = 0.06 * max(hi - lo)
    ax.set_xlim(lo[0] - pad, hi[0] + pad); ax.set_ylim(lo[1] - pad, hi[1] + pad)
    ax.set_aspect('equal'); ax.axis('off')
    if title: ax.set_title(title, fontsize=11, color='#333')

VIEWS = [('three-quarter view', View(22, -58)), ('side view', View(0.5, -90)), ('top view', View(89.5, -90))]
NAMES = {'c': 'c-tile · 60 rings · 180 zip ties', 'h': 'h-tile · 48 rings · 144 zip ties'}

def logo(fig, x=0.93, w=0.06):
    lg = plt.imread(B.LOGO); W, H = fig.get_size_inches()
    la = fig.add_axes([x, 0.012, w, w * W / H]); la.imshow(lg); la.axis('off')

if __name__ == '__main__':
    M = {t: model(t, w, L) for t, w, L in (('c', 'ABC', 1), ('h', 'AB', 0))}
    BG = '#f4f4f2'
    for t in 'ch':
        fig = plt.figure(figsize=(15, 6.2), facecolor=BG)
        for k, (nm, v) in enumerate(VIEWS):
            ax = fig.add_axes([0.01 + k * 0.33, 0.06, 0.32, 0.82]); draw(ax, t, M[t], v, nm, lw_tie=1.3)
        fig.suptitle(f'{NAMES[t]} · HexOct at λ = −1/8 · ring mock-up' + (' · towers touch at one corner (ring = optional tie)' if t == 'c' else ''),
                     fontsize=13, color='#222', y=0.97)
        logo(fig, 0.945, 0.045)
        fig.savefig(os.path.join(OUT, f'mockup-{t}.png'), dpi=160, facecolor=BG); plt.close(fig); print('saved', t, flush=True)
    fig = plt.figure(figsize=(16, 12), facecolor=BG)
    for j, t in enumerate('ch'):
        ax = fig.add_axes([0.01 + j * 0.5, 0.40, 0.48, 0.52]); draw(ax, t, M[t], VIEWS[0][1], NAMES[t])
        for k, (nm, v) in enumerate(VIEWS[1:]):
            ax = fig.add_axes([0.02 + j * 0.5 + k * 0.24, 0.05, 0.22, 0.30]); draw(ax, t, M[t], v, nm, lw_tie=0.9)
    fig.suptitle('HexOct tiles from PET-bottle-cap security rings · λ = −1/8 · each ring a rounded triangle, six zip ties per ring',
                 fontsize=14, color='#222', y=0.975)
    logo(fig, 0.935, 0.055)
    fig.savefig(os.path.join(OUT, 'mockup-sheet.png'), dpi=160, facecolor=BG); plt.close(fig); print('saved sheet')
