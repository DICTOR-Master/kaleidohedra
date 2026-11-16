# Figures for DICTO's shadows test (16 Nov 2026): one sheet per Queen.
# Input: data/shadows.json from scripts/shadows.py (exact Q(sqrt5) analysis; float 3D coordinates for drawing only).
# Main panel: the main shadow (White Queen corner-first, Red Queen cell-first): the shadow's hull as a faint depth-shaded cage, every
# surviving wall as a translucent disc through the centre (mirrors blue = I water, cross walls red = T fire, element colours of the DICTO
# square), and the possible-Vacuus layer outlines: innermost a solid lit core, the others see-through crystal shells with crisp edges.
# Side panels: the mirror planes alone and the cross-wall planes alone, with the same outlines.
# Painting: far halves of the discs, then the shapes (back faces, edges, front faces, front edges on top: the 2D form of polygon offset),
# then the near halves of the discs; 3x supersampling, edges >= 1.6 px after downsampling, depth-shaded, no haze; orthographic, one
# scale for x and y; every model asserted inside its frame margin. Canvas and sheet layout follow
# studies/2026-11-16-non-heart-vacuus/scripts/render_vacuus.py (same project). DICTO mark bottom right.
# Run from the study folder: python scripts/render_shadows.py [--pilot] ; ends "FINAL ok".
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
PILOT = '--pilot' in sys.argv
SS = 2 if PILOT else 3
GROUND = (21, 25, 33); EDGE = np.array([240, 234, 216.]); GOLD = (232, 190, 70); CRYSTAL = np.array([170, 200, 225.])
EL = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}
WALLCOL = {'mirror': EL['I'], 'cross': EL['T']}
SHAPECOL = [GOLD, (236, 232, 220), (120, 210, 200), (232, 150, 90)]
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(px): return ImageFont.truetype(FONT, px)
def look(d, up):
    z = np.array(d, float); z /= np.linalg.norm(z); up = np.array(up, float); x = np.cross(up, z); x /= np.linalg.norm(x); y = np.cross(z, x)
    return np.array([x, y, z])
def rot(axis, deg):
    a = np.array(axis, float); a /= np.linalg.norm(a); t = np.radians(deg); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
class Canvas:
    def __init__(s, P3, M, size, margin=0.06):
        s.M, s.size, s.W = M, size, size * SS
        Q = P3 @ M.T; lo, hi = Q.min(0), Q.max(0); inner = s.W * (1 - 2 * margin)
        s.k = inner / max(hi[0] - lo[0], hi[1] - lo[1]); s.lo, s.hi = lo, hi
        s.ox = (s.W - s.k * (hi[0] - lo[0])) / 2; s.oy = (s.W - s.k * (hi[1] - lo[1])) / 2
        s.zl, s.zh = lo[2], hi[2]; s.img = np.zeros((s.W, s.W, 3), np.float32); s.img[:] = GROUND
        px = s.px(P3); m = margin * s.W * 0.999
        assert px[:, 0].min() >= m - 1 and px[:, 0].max() <= s.W - m + 1 and px[:, 1].min() >= m - 1 and px[:, 1].max() <= s.W - m + 1, 'model outside frame'
    def px(s, P): Q = np.atleast_2d(P) @ s.M.T; return np.c_[s.ox + s.k * (Q[:, 0] - s.lo[0]), s.oy + s.k * (s.hi[1] - Q[:, 1])]
    def depth(s, P): return float(((np.atleast_2d(P) @ s.M.T)[:, 2].mean() - s.zl) / (s.zh - s.zl + 1e-12))
    def _blend(s, draw_fn, col, alpha):
        L = Image.new('L', (s.W, s.W), 0); draw_fn(ImageDraw.Draw(L))
        a = np.asarray(L, np.float32) / 255 * alpha; ys, xs = np.nonzero(a)
        if len(ys) == 0: return
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; aa = a[y0:y1, x0:x1, None]
        s.img[y0:y1, x0:x1] = s.img[y0:y1, x0:x1] * (1 - aa) + np.array(col, np.float32) * aa
    def _blend_box(s, q, pad, draw_fn, col, alpha):
        # draw on a mask only as large as the primitive's bounding box (speed; same pixels as a full-size mask)
        x0 = max(0, int(np.floor(q[:, 0].min() - pad))); y0 = max(0, int(np.floor(q[:, 1].min() - pad)))
        x1 = min(s.W, int(np.ceil(q[:, 0].max() + pad)) + 1); y1 = min(s.W, int(np.ceil(q[:, 1].max() + pad)) + 1)
        if x1 <= x0 or y1 <= y0: return
        L = Image.new('L', (x1 - x0, y1 - y0), 0); draw_fn(ImageDraw.Draw(L), x0, y0)
        a = np.asarray(L, np.float32)[:, :, None] / 255 * alpha
        s.img[y0:y1, x0:x1] = s.img[y0:y1, x0:x1] * (1 - a) + np.array(col, np.float32) * a
    def poly(s, P, col, alpha):
        q = s.px(P); s._blend_box(q, 2, lambda d, x0, y0: d.polygon([(x - x0, y - y0) for x, y in q], fill=255), col, alpha)
    def line(s, a, b, col, w_px, alpha=1.0):
        q = s.px(np.array([a, b])); w = max(1, int(round(w_px * SS)))
        def f(d, x0, y0):
            d.line([(q[0][0] - x0, q[0][1] - y0), (q[1][0] - x0, q[1][1] - y0)], fill=255, width=w)
            r = w / 2; [d.ellipse([x - x0 - r, y - y0 - r, x - x0 + r, y - y0 + r], fill=255) for x, y in q]
        s._blend_box(q, w + 2, f, col, alpha)
    def image(s): return Image.fromarray(np.clip(s.img, 0, 255).astype(np.uint8)).resize((s.size, s.size), Image.LANCZOS)
def shade(col, t): return tuple(float(c) for c in np.array(GROUND) + (np.array(col, float) - GROUND) * (0.42 + 0.58 * t))

def disc(n, rho, k=120):
    n = np.array(n, float); n /= np.linalg.norm(n); u = np.cross(n, [0.31, 0.57, 0.76]); u /= np.linalg.norm(u); v = np.cross(n, u)
    t = np.linspace(0, 2 * np.pi, k, endpoint=False); return rho * (np.cos(t)[:, None] * u + np.sin(t)[:, None] * v)
def half(D, M, near):
    z = D @ M[2]; keep = z >= 0 if near else z <= 0
    idx = np.nonzero(keep)[0]
    if len(idx) < 3: return None
    # rotate so the kept arc is contiguous, then close through the centre line
    roll = np.argmax(~keep) if not keep.all() else 0
    Dr = np.roll(D, -roll, 0); kr = np.roll(keep, -roll)
    arc = Dr[kr]
    return np.vstack([arc, [0, 0, 0]]) if len(arc) else None

def draw_shape(cv, X, faces, edges, col, solid, M, l):
    cen = X.mean(0)
    def nrm(cyc):
        P = X[cyc]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        return n if n @ (P.mean(0) - cen) > 0 else -n
    front = lambda cyc: (M @ nrm(cyc))[2] > 0
    order = sorted(faces, key=lambda c: cv.depth(X[c]))
    for cyc in order:
        if not front(cyc) and not solid: cv.poly(X[cyc], tuple(CRYSTAL * 0.8), 0.07)
    if not solid:
        for i, j in sorted(edges, key=lambda e: cv.depth(X[list(e)])):
            cv.line(X[i], X[j], shade(col, 0.5 * cv.depth(X[[i, j]])), 1.6)
    for cyc in order:
        if front(cyc):
            n = M @ nrm(cyc); lit = 0.45 + 0.55 * max(0.0, n @ l)
            if solid: cv.poly(X[cyc], tuple(np.array(col, float) * lit), 0.97)
            else: cv.poly(X[cyc], tuple(CRYSTAL * lit), 0.10)
    for i, j in edges:
        if any(front(c) and i in c and j in c for c in faces):
            cv.line(X[i], X[j], shade(col if not solid else (40, 34, 20), 0.5 + 0.5 * cv.depth(X[[i, j]])) if not solid else (60, 50, 30), 2.2 if not solid else 1.7)

def panel(sh, shapes, kinds, size, M):
    hull = sh['hull']; HX = np.array(hull['X3']); rho = 1.08 * np.linalg.norm(HX, axis=1).max()
    walls = [w for w in sh['wall_normals_3d'] if w['kind'] in kinds]
    allpts = np.vstack([HX] + [disc(w['n'], rho, 48) for w in walls])
    cv = Canvas(allpts, M, size); l = np.array([-0.4, 0.55, 0.73]); l /= np.linalg.norm(l)
    na = {'mirror': 0.06, 'cross': 0.03}
    single = len(kinds) == 1
    for w in walls:                                          # far halves
        D = disc(w['n'], rho); H = half(D, M, False)
        if H is not None: cv.poly(H, WALLCOL[w['kind']], na[w['kind']] * (1.6 if single else 1.0))
        for a, b in zip(D, np.roll(D, -1, 0)):
            if (a @ M[2]) <= 0: cv.line(a, b, shade(WALLCOL[w['kind']], 0.5), 1.0, 0.35)
    for i, j in hull['edge_list']:                           # hull cage, far edges dim
        cv.line(HX[i], HX[j], shade(EDGE, 0.25 + 0.35 * cv.depth(HX[[i, j]])), 1.0, 0.55)
    for k, s in reversed(list(enumerate(shapes))):           # outer shells first, solid core last
        draw_shape(cv, np.array(s['X3']), s['face_list'], s['edge_list'], SHAPECOL[k % len(SHAPECOL)], k == 0, M, l)
    for w in walls:                                          # near halves on top
        D = disc(w['n'], rho); H = half(D, M, True)
        if H is not None: cv.poly(H, WALLCOL[w['kind']], 0.5 * na[w['kind']] * (1.6 if single else 1.0))
        for a, b in zip(D, np.roll(D, -1, 0)):
            if (a @ M[2]) > 0: cv.line(a, b, shade(WALLCOL[w['kind']], 0.95), 1.5, 0.75)
    return cv.image()

def sheet(main, sides, title, legend, out):
    P = main.size[0]; p2 = sides[0][0].size[0]; f = P / 1100; pad = int(40 * f); top = int(150 * f)
    ft, fc, fm = font(int(38 * f)), font(int(25 * f)), font(int(23 * f)); lh = int(38 * f)
    Wd = P + p2 + 3 * pad; Hd = top + P + len(legend) * lh + int(110 * f)
    im = Image.new('RGB', (Wd, Hd), GROUND); d = ImageDraw.Draw(im)
    for k, line in enumerate(title):
        assert d.textlength(line, font=ft if k == 0 else fc) < Wd - 2 * pad, ('title too long', line)
        d.text((pad, int(24 * f) + k * int(48 * f)), line, font=ft if k == 0 else fc, fill=(236, 230, 214) if k == 0 else (200, 196, 186))
    im.paste(main, (pad, top))
    y = top
    for img, cap, sw in sides:
        assert y + p2 + int(40 * f) <= top + P, 'side panels overrun'
        im.paste(img, (2 * pad + P, y)); yy = y + p2 + int(6 * f)
        assert d.textlength(cap, font=fc) < p2 - 30, ('caption too long', cap)
        d.rectangle([2 * pad + P, yy + int(4 * f), 2 * pad + P + int(22 * f), yy + int(26 * f)], fill=sw)
        d.text((2 * pad + P + int(32 * f), yy), cap, font=fc, fill=(220, 214, 200)); y += p2 + int(60 * f)
    y = top + P + int(20 * f)
    for line in legend:
        assert d.textlength(line, font=fc) < Wd - 2 * pad, ('legend too long', line); d.text((pad, y), line, font=fc, fill=(205, 200, 188)); y += lh
    mk = 'DICTO · dictospheres.com'; d.text((Wd - pad - d.textlength(mk, font=fm), Hd - int(46 * f)), mk, font=fm, fill=(150, 150, 150))
    im.save(out); return im

def vacuus_shapes(sh):
    out, seen = [], []
    for L in sh['layers']:
        if L['verdict_O'] != 'possible Vacuus' or L['rank'] != 3: continue
        X = np.array(L['X3']); key = sorted(map(tuple, np.round(X, 6)))
        if key in seen: continue
        seen.append(key); out.append(L)
    return sorted(out, key=lambda L: np.linalg.norm(np.array(L['X3']), axis=1).max())

if __name__ == '__main__':
    js = json.load(open('data/shadows.json')); os.makedirs('figures', exist_ok=True); made = []
    SH = {(s['queen'], s['type']): s for s in js['shadows']}
    jobs = [('600', 'V', 'white', 'The White Queen (600-cell), corner-first shadow'),
            ('120', 'V', 'red', 'The Red Queen (120-cell), cell-first shadow')]
    size = 620 if PILOT else 1100; s2 = int((size - 120 * size / 1100) / 2)
    for qn, typ, tag, ttl in jobs:
        sh = SH[(qn, typ)]; shapes = vacuus_shapes(sh)
        if not shapes: print('no Vacuus shapes for', qn, typ); continue
        # view: an outer corner direction of the hull turned 24 deg about a mirror normal -> discs show as ellipses
        m0 = np.array([w['n'] for w in sh['wall_normals_3d'] if w['kind'] == 'mirror'][0])
        v0 = np.array(shapes[0]['X3'][0]); v0 = v0 / np.linalg.norm(v0)
        ax = np.cross(v0, m0); ax = ax if np.linalg.norm(ax) > 1e-6 else np.cross(v0, [1, 0.3, 0.1])
        vd = rot(ax, 9) @ rot(m0, 5) @ v0; up = m0 - (m0 @ vd) * vd
        M = look(vd, up)
        main = panel(sh, shapes, ('mirror', 'cross'), size, M)
        pm = panel(sh, shapes, ('mirror',), s2, M); pc = panel(sh, shapes, ('cross',), s2, M)
        W = sh['walls']
        names = [L['name'].split(' (')[0] for L in shapes]
        title = [ttl, f"{W['mirror'] + W['cross']} walls contain the view and stay flat: {W['mirror']} mirrors (blue) + {W['cross']} cross walls (red)"]
        legend = ['Possible Vacuus outlines (every edge fin from the shadow\'s centre lies in a kept wall), inside out:',
                  '   ' + ', '.join(names) + ' (innermost solid gold, the others see-through shells).',
                  'Faint cage: the shadow\'s hull. Each disc is a central plane of the shadow, the trace of a wall of the 600-cell.']
        out = f'figures/RENDER-queens-shadows-{tag}.png'
        sheet(main, [(pm, f"{W['mirror']} mirror planes", WALLCOL['mirror']), (pc, f"{W['cross']} cross-wall planes", WALLCOL['cross'])], title, legend, out)
        made.append(out); print('wrote', out, 'shapes', names)
    print('FINAL ok' if len(made) == 2 else 'FINAL FAIL')
