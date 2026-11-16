# Renders of the non-heart Vacuus of the golden solids A and B ("Silent Running: Twisted Silence"), redone 16 Nov 2026 after
# DICTO's critique of the first set ("they look all the same except color"): the slices were uniform clear crystals, the
# projection hid the differences, and in the plates figure every fin overlapped from one centre.
# Input: data/vacuus-exact.json from scripts/vacuus_exact.py (exact Q(sqrt5) analysis; float coordinates for drawing only).
#   (a) RENDER-non-heart-vacuus-{A,B}-slices.png: one slice per kind of plate, every face coloured by its KIND (triangle,
#       rectangle, rhombus, trapezoid, pentagon, hexagon, heptagon; Kaleidohedra app face-kind palette, extended with element
#       colours), in one standard pose: the plate's own two-face flat at the bottom (gold rim, dashed where hidden), the camera
#       at the same height and turn for every slice, and ONE scale for all slices of both solids (both solids have circumradius
#       2.288 in these coordinates). Under each slice a face-count strip.
#   (b) RENDER-non-heart-vacuus-{A,B}-plates.png: one plate of each kind ALONE (the cone from the centre of the solid over the
#       plate's two-face, drawn in the plate's own 3-space, exact proportions, same pose and scale), next to a small locator:
#       the whole solid as a depth-shaded wire view (projection along the 5-cell axis through coordinate 5), with that one
#       two-face filled and its spokes to the centre drawn.
# Painting: hidden edges first (dim, depth-shaded), then faces back to front, nearly opaque (alpha 0.93), then front edges crisp
# on top (the 2D form of polygon offset); 3x supersampling, edges >= 1.6 px after downsampling; no haze; orthographic, one
# scale for x and y; every model asserted inside its frame margin.
# Run from the study folder: python scripts/render_vacuus.py [--pilot]  ; ends "FINAL ok" or "FINAL FAIL".
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
PILOT = '--pilot' in sys.argv
SS = 2 if PILOT else 3; SIZE = 520 if PILOT else 900
GROUND = (5, 5, 10); EDGE = np.array([240, 234, 216.]); GOLD = (222, 178, 80); CRYSTAL = np.array([150, 170, 190.])
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
# face kinds: app palette (krp-core faceKinds.js: triangle, square, rhombus, hexagon), trapezoid and pentagon from the element
# colours (Wind, Fire), heptagon the app's orange (world-chains.js)
KINDS = ['triangle', 'rectangle', 'rhombus', 'trapezoid', 'pentagon', 'hexagon', 'heptagon']
KCOL = {'triangle': (0x47, 0xcc, 0x24), 'rectangle': (0x3f, 0xa9, 0xf5), 'rhombus': (0xff, 0x5f, 0xa2), 'trapezoid': (232, 200, 82),
        'pentagon': (205, 62, 40), 'hexagon': (0xa7, 0x7b, 0xff), 'heptagon': (0xff, 0x9a, 0x52)}
PLURAL = {'triangle': 'triangles', 'rectangle': 'rectangles', 'rhombus': 'rhombi', 'trapezoid': 'trapezoids', 'pentagon': 'pentagons',
          'hexagon': 'hexagons', 'heptagon': 'heptagons'}
fails = []
def check(ok, msg):
    if not ok: print('CHECK FAIL ' + msg, flush=True); fails.append(msg)
def font(px): return ImageFont.truetype(FONT, px)
def kind_of(name):
    for k in ('triangle', 'rectangle', 'square', 'rhombus', 'trapezoid', 'pentagon', 'heptagon', 'hexagon'):
        if k in name: return 'rectangle' if k == 'square' else k
    raise ValueError(name)
def look(d, up):
    z = np.array(d, float); z /= np.linalg.norm(z); up = np.array(up, float); x = np.cross(up, z); x /= np.linalg.norm(x); y = np.cross(z, x)
    return np.array([x, y, z])
class Canvas:
    """Supersampled canvas; ONE scale k (model units -> px) for x and y; model centred on `centre`; asserted inside the margin."""
    def __init__(s, P3, M, k_px, centre, size=SIZE, margin=0.04):
        s.M, s.size, s.W = M, size, size * SS; Q = P3 @ M.T
        s.k = k_px * SS; s.c = centre; s.zl, s.zh = Q[:, 2].min(), Q[:, 2].max()
        s.img = np.zeros((s.W, s.W, 3), np.float32); s.img[:] = GROUND
        px = s.px(P3); m = margin * s.W
        check(px.min() >= m - 1 and px.max() <= s.W - m + 1, 'model inside its frame margin')
    def px(s, P): Q = np.atleast_2d(P) @ s.M.T; return np.c_[s.W / 2 + s.k * (Q[:, 0] - s.c[0]), s.W / 2 - s.k * (Q[:, 1] - s.c[1])]
    def depth(s, P): return float(((np.atleast_2d(P) @ s.M.T)[:, 2].mean() - s.zl) / (s.zh - s.zl + 1e-12))   # 0 far .. 1 near
    def _blend(s, draw_fn, col, alpha):
        L = Image.new('L', (s.W, s.W), 0); draw_fn(ImageDraw.Draw(L))
        a = np.asarray(L, np.float32) / 255 * alpha; ys, xs = np.nonzero(a)
        if len(ys) == 0: return
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; aa = a[y0:y1, x0:x1, None]
        s.img[y0:y1, x0:x1] = s.img[y0:y1, x0:x1] * (1 - aa) + np.array(col, np.float32) * aa
    def poly(s, P, col, alpha): q = [tuple(p) for p in s.px(P)]; s._blend(lambda d: d.polygon(q, fill=255), col, alpha)
    def line(s, a, b, col, w_px, alpha=1.0, dash=None):
        q = s.px(np.array([a, b])); w = max(1, int(round(w_px * SS))); segs = [(q[0], q[1])]
        if dash:
            L = np.linalg.norm(q[1] - q[0]); n = max(1, int(L / (dash * SS * 2)))
            segs = [(q[0] + (q[1] - q[0]) * (2 * i) / (2 * n), q[0] + (q[1] - q[0]) * (2 * i + 1) / (2 * n)) for i in range(n)]
        def f(d):
            for a_, b_ in segs:
                d.line([tuple(a_), tuple(b_)], fill=255, width=w); r = w / 2
                for x, y in (a_, b_): d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        s._blend(f, col, alpha)
    def dot(s, P, col, r_px):
        x, y = s.px(P)[0]; r = r_px * SS; s._blend(lambda d: d.ellipse([x - r, y - r, x + r, y + r], fill=255), col, 1.0)
    def image(s): return Image.fromarray(np.clip(s.img, 0, 255).astype(np.uint8)).resize((s.size, s.size), Image.LANCZOS)
def shade(col, t): return tuple(float(c) for c in np.array(GROUND) + (np.array(col, float) - GROUND) * (0.40 + 0.60 * t))
# ------------------------------------------------------------------ the standard pose
CAM = look([np.cos(np.radians(-58)), np.sin(np.radians(-58)), np.tan(np.radians(24))], [0, 0, 1])   # 24 deg above, fixed turn
LIGHT = np.array([-0.35, 0.45, 0.82]); LIGHT /= np.linalg.norm(LIGHT)
def pose(sl):
    """rotate the slice (plate coordinates, centre of the solid at 0) so that its ridge face lies flat at the bottom: ridge plane z = 0,
    the slice above it, the ridge's centroid on the vertical axis. Returns posed corners, the posed centre of the solid, the ridge."""
    X = np.array(sl['X3']); ridge = [f for f in sl['faces'] if f['ridge']][0]['cycle']; R = X[ridge]
    n = np.cross(R[1] - R[0], R[2] - R[0]); n /= np.linalg.norm(n)
    if n @ (X.mean(0) - R.mean(0)) < 0: n = -n          # n points into the slice
    a = np.cross(n, [1, 0, 0]); a = a if np.linalg.norm(a) > 1e-6 else np.cross(n, [0, 1, 0]); a /= np.linalg.norm(a); b = np.cross(n, a)
    T = np.array([a, b, n]); Y = (X - R.mean(0)) @ T.T; C0 = (np.zeros(3) - R.mean(0)) @ T.T
    check(np.allclose(Y[ridge][:, 2], 0) and Y[:, 2].min() > -1e-9, 'pose: ridge flat at z = 0, slice above it')
    check(np.allclose(np.linalg.norm(Y - Y[0], axis=1), np.linalg.norm(X - X[0], axis=1)), 'pose is a rigid motion')
    return Y, C0, ridge
def nrm(Y, cyc, inside):
    P = Y[cyc]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
    return n if n @ (P.mean(0) - inside) > 0 else -n
def solid_panel(Y, faces, edges, ridge, cols, k_px, centre, extra=None, glass=False):
    cv = Canvas(Y if extra is None else np.vstack([Y, extra]), CAM, k_px, centre)
    inside = Y.mean(0)
    front = lambda cyc: (CAM @ nrm(Y, cyc, inside))[2] > 0
    if glass:   # the cone: its two-face (base) seen through clear sides, so the kind colour shows
        for cyc, col in sorted(zip(faces, cols), key=lambda t: cv.depth(Y[t[0]])):
            cv.poly(Y[cyc], col, 0.92 if cyc == ridge else 0.22)
        for i, j in edges: cv.line(Y[i], Y[j], shade(EDGE, 0.45 + 0.55 * cv.depth(Y[[i, j]])), 2.0)
        for t in range(len(ridge)): cv.line(Y[ridge[t]], Y[ridge[(t + 1) % len(ridge)]], GOLD, 2.6)
        return cv
    for i, j in sorted(edges, key=lambda e: cv.depth(Y[list(e)])):            # hidden edges, dim and depth-shaded
        cv.line(Y[i], Y[j], shade(EDGE, 0.15 + 0.35 * cv.depth(Y[[i, j]])), 1.3)
    for cyc, col in sorted(zip(faces, cols), key=lambda t: cv.depth(Y[t[0]])):
        if front(cyc):
            lit = 0.64 + 0.36 * max(0.0, nrm(Y, cyc, inside) @ LIGHT)
            cv.poly(Y[cyc], tuple(np.array(col) * lit), 0.93)
    for i, j in edges:                                                          # front edges crisp on top
        if any(front(c) and i in c and j in c for c in faces): cv.line(Y[i], Y[j], shade(EDGE, 0.55 + 0.45 * cv.depth(Y[[i, j]])), 2.0)
    vis = front(ridge)
    for t in range(len(ridge)):
        a, b = Y[ridge[t]], Y[ridge[(t + 1) % len(ridge)]]; cv.line(a, b, GOLD, 2.6, dash=None if vis else 5)
    return cv
# ------------------------------------------------------------------ locator: the whole solid as a wire view
def solid_basis():
    A = np.array([[1, -1, 0, 0, 0], [0, 1, -1, 0, 0], [0, 0, 1, -1, 0]], float); Q, _ = np.linalg.qr(A.T); return Q.T
def locator(sol, ridge_idx, col, views):
    V = np.array(sol['V']) - np.array(sol['centre']); P = V @ solid_basis().T; P /= np.linalg.norm(P, axis=1).max()
    def seen(v):   # how open the two-face lies in this view: its smallest singular value on screen
        Mv = look(v, [0, 0, 1]); W = (P[ridge_idx] - P[ridge_idx].mean(0)) @ Mv[:2].T; return np.linalg.svd(W, compute_uv=False)[-1]
    view = max(views, key=seen); check(seen(view) > 0.05, 'locator: the two-face is seen open, not edge-on')
    M = look(view, [0, 0, 1]); k = SIZE * 0.42 / np.abs(P @ M.T)[:, :2].max()
    cv = Canvas(np.vstack([P, np.zeros((1, 3))]), M, k, np.zeros(3))
    for i, j in sorted(sol['edges'], key=lambda e: cv.depth(P[list(e)])):
        cv.line(P[i], P[j], shade(EDGE, 0.20 + 0.55 * cv.depth(P[[i, j]])), 1.6)
    W = V[ridge_idx] - V[ridge_idx].mean(0); U = np.linalg.svd(W)[2]; cyc = [ridge_idx[t] for t in np.argsort(np.arctan2(W @ U[1], W @ U[0]))]
    for t in cyc: cv.line(np.zeros(3), P[t], shade(GOLD, 0.8), 1.6, dash=4)
    cv.poly(P[cyc], col, 0.92)
    for t in range(len(cyc)): cv.line(P[cyc[t]], P[cyc[(t + 1) % len(cyc)]], GOLD, 2.6)
    cv.dot(np.zeros(3), (250, 248, 240), 5)
    return cv.image()
# ------------------------------------------------------------------ the face-count strip and the sheet
def counts_of(sl):
    c = {}
    for f in sl['faces']: k = kind_of(f['name']); c[k] = c.get(k, 0) + 1
    return [(k, c[k]) for k in KINDS if k in c]
def strip_text(cnt): return ' · '.join(f'{n} {PLURAL[k] if n > 1 else k}' for k, n in cnt)
def draw_strip(d, x, y, cnt, f, fs):
    for k, n in cnt:
        sw = int(22 * fs); d.rectangle([x, y + int(4 * fs), x + sw, y + int(4 * fs) + sw], fill=KCOL[k]); x += sw + int(8 * fs)
        t = f'{n} {PLURAL[k] if n > 1 else k}'; d.text((x, y), t, font=f, fill=(225, 220, 205)); x += d.textlength(t, font=f) + int(22 * fs)
    return x
def sheet(rows, title, legend, out, P, cols):
    """rows: list of panels (img, caption lines, strip counts or None); cols panels per row."""
    f = P / 900; pad = int(40 * f); top = int(150 * f); capl = int(36 * f)
    ft, fc, fs_ = font(int(36 * f)), font(int(25 * f)), font(int(23 * f))
    nl = max(len(r[1]) + (1 if r[2] else 0) for r in rows); cap = int(16 * f) + nl * capl
    nrow = (len(rows) + cols - 1) // cols; Wd = cols * P + (cols + 1) * pad
    Hd = top + nrow * (P + cap + pad) + int(56 * f) * len(legend) + int(70 * f)
    im = Image.new('RGB', (Wd, Hd), GROUND); d = ImageDraw.Draw(im)
    for i, line in enumerate(title):
        fn = ft if i == 0 else fc
        check(d.textlength(line, font=fn) < Wd - 2 * pad, f'title fits: {line}'); d.text((pad, int(20 * f) + i * int(44 * f)), line, font=fn, fill=(236, 230, 214) if i == 0 else (196, 192, 182))
    for i, (img, caps, cnt) in enumerate(rows):
        r, c = divmod(i, cols); x = pad + c * (P + pad); y = top + r * (P + cap + pad); im.paste(img, (x, y)); yy = y + P + int(10 * f)
        for li, t in enumerate(caps):
            check(d.textlength(t, font=fc) < P - 4, f'caption fits: {t}'); d.text((x + 6, yy), t, font=fc, fill=(232, 226, 210) if li == 0 else (186, 182, 172)); yy += capl
        if cnt:
            xe = draw_strip(d, x + 6, yy, cnt, fs_, f); check(xe < x + P + pad * 0.5, f'face-count strip fits: {strip_text(cnt)}')
    y = top + nrow * (P + cap + pad)
    for item in legend:
        if isinstance(item, str): d.text((pad, y), item, font=fc, fill=(205, 200, 188)); check(d.textlength(item, font=fc) < Wd - 2 * pad, 'legend line fits')
        else:
            x = pad
            for k in item:
                sw = int(26 * f); d.rectangle([x, y + int(3 * f), x + sw, y + int(3 * f) + sw], fill=KCOL[k] if k in KCOL else GOLD); x += sw + int(10 * f)
                t = k if k in KCOL else 'gold rim: the plate\'s own two-face (at the bottom; dashed where hidden)'; d.text((x, y), t, font=fc, fill=(220, 214, 200)); x += d.textlength(t, font=fc) + int(30 * f)
            check(x < Wd, 'legend fits')
        y += int(56 * f)
    mk = 'DICTO · dictospheres.com'; d.text((Wd - pad - d.textlength(mk, font=fs_), Hd - int(46 * f)), mk, font=fs_, fill=(150, 150, 150))
    im.save(out); return im
# ------------------------------------------------------------------ main
if __name__ == '__main__':
    js = json.load(open('data/vacuus-exact.json'))
    SOL = {'A': ('A: perms of (φ², φ², φ², φ, 0)', '(φ², φ², φ², φ, 0)'), 'B': ('B: perms of (φ², φ², 1, 1, 0)', '(φ², φ², 1, 1, 0)')}
    CELLWORD = {'tetrahedron': 'tetrahedron', 'truncated tetrahedron': 'golden truncated tetrahedron', 'octahedron': 'octahedron',
                'triangular prism': 'golden prism', 'cuboctahedron': 'golden cuboctahedron'}
    NAMES = {'equilateral triangle': 'triangle', 'equiangular hexagon': 'hexagon', 'rectangle': 'rectangle'}
    posed = {(t, i): pose(o['slice']) for t, (key, _s) in SOL.items() for i, o in enumerate(js[key]['orbits'])}
    def frame(Y, C0):   # projected extent of slice + centre: its middle and half-size
        Q = np.vstack([Y, C0[None]]) @ CAM.T; lo, hi = Q[:, :2].min(0), Q[:, :2].max(0); return np.r_[(lo + hi) / 2, 0], (hi - lo).max() / 2
    ext = max(frame(Y, C0)[1] for (Y, C0, _r) in posed.values())
    K_PX = SIZE * 0.44 / ext            # ONE scale for every slice and plate of both solids
    print(f'one scale for all panels: {K_PX:.2f} px per unit (largest half-extent {ext:.3f})', flush=True)
    os.makedirs('figures', exist_ok=True); made = []
    for tag, (key, seed) in SOL.items():
        sol = js[key]; orbs = sol['orbits']; slices, plates = [], []
        LOCVIEW = [[0.25, 1, 0.62], [1, 0.55, 0.42], [-0.6, 0.9, 0.5], [0.9, -0.3, 0.55]]   # the view that opens the two-face most
        for oi, o in enumerate(orbs):
            sl = o['slice']; Y, C0, ridge = posed[(tag, oi)]; ctr = frame(Y, C0)[0]
            faces = [f['cycle'] for f in sl['faces']]; cols = [KCOL[kind_of(f['name'])] for f in sl['faces']]
            cnt = counts_of(sl); check(sum(n for _k, n in cnt) == sl['counts'][2], f'{tag}{oi + 1}: face-count strip adds up to {sl["counts"][2]} faces')
            cv = solid_panel(Y, faces, sl['edges'], ridge, cols, K_PX, ctr, extra=C0[None])
            for k, org in enumerate(sl['origin']):
                if org[0] == 'vertex': cv.dot(Y[k], (250, 248, 240), 3.2)
            rf = [f for f in sl['faces'] if f['ridge']][0]
            rw = o['ridge_shape'].split(',')[0]; rw = NAMES.get(rw, rw)
            side = o['ridge_shape'].split('side')[-1].strip() if ' side ' in o['ridge_shape'] else o['ridge_shape'].split('sides')[-1].replace(' in turn', '').strip()
            between = ' | '.join(CELLWORD[c] for c in rf['cellnames']) if len(rf['cellnames']) == 2 else f'two {CELLWORD[rf["cellnames"][0]]}s'
            nv, ne, nf = sl['counts']; name = f'{tag}{oi + 1}'
            slices.append((cv.image(), [f'{name}: {o["n_plates"]} plates on the {rw}s ({side})', f'slice: {nv} corners, {ne} edges, {nf} faces'], cnt))
            # the plate alone: the cone from the centre over the ridge, in the plate's own 3-space
            P = np.vstack([Y[ridge], C0[None]]); m = len(ridge); cyc = list(range(m))
            cfaces = [cyc] + [[t, (t + 1) % m, m] for t in range(m)]
            ccols = [KCOL[kind_of(rf['name'])]] + [tuple(CRYSTAL)] * m
            cedges = [(t, (t + 1) % m) for t in range(m)] + [(t, m) for t in range(m)]
            Qc = P @ CAM.T; cc = np.r_[(Qc[:, :2].min(0) + Qc[:, :2].max(0)) / 2, 0]
            cv2 = solid_panel(P, cfaces, cedges, cyc, ccols, K_PX, cc, glass=True)
            cv2.dot(C0, (250, 248, 240), 5.0)
            check(abs(C0[2]) > 0.1, f'{name}: the centre lies off the ridge plane')
            plates.append((cv2.image(), [f'{name}: one plate alone ({o["n_plates"]} like it)', f'cone from the centre (white) over the {rw}'], None))
            plates.append((locator(sol, o['ridge_vertices'], KCOL[kind_of(rf['name'])], LOCVIEW), [f'where {name} sits in solid {tag}', f'between {between}'], None))
            print(f'PROGRESS {(list(SOL).index(tag) + (oi + 1) / len(orbs)) / 2:.2f} {name}: {strip_text(cnt)}', flush=True)
        present = [k for k in KINDS if any(k == kind_of(f['name']) for o in orbs for f in o['slice']['faces'])]
        sfx = '-pilot' if PILOT else ''
        t1 = [f'Solid {tag}, perms of {seed}: one slice per kind of plate',
              f'{len(sol["V"])} corners, {len(sol["ridges"])} two-faces on {sol["n_plates"]} central plates; {len(orbs)} kinds under its {sol["group_order"]} symmetries.',
              'Every slice in the same pose and at the same scale; the plate\'s own two-face lies flat at the bottom.']
        leg = ['Faces coloured by kind. White dots: corners of the solid; other corners are where the plate cuts an edge.', present, ['gold']]
        out = f'figures/RENDER-non-heart-vacuus-{tag}-slices{sfx}.png'; sheet(slices, t1, leg, out, SIZE, 2); made.append(out)
        t2 = [f'Solid {tag}, perms of {seed}: one central plate of each kind, alone',
              'Left: the plate as the cone from the centre over its two-face, in the plate\'s own space (true shape; pose and scale as the slices).',
              'Right: the whole solid as a wire view along a 5-cell axis, that two-face filled, its spokes to the centre dashed.']
        leg2 = ['One two-face per plate: no centre of symmetry, so no plate carries an opposite pair (the non-heart kind).',
                [k for k in KINDS if any(k == kind_of(f['name']) for o in orbs for f in o['slice']['faces'] if f['ridge'])], ['gold']]
        out = f'figures/RENDER-non-heart-vacuus-{tag}-plates{sfx}.png'; sheet(plates, t2, leg2, out, SIZE, 2); made.append(out)
    ok = all(os.path.exists(m) for m in made) and not fails
    print(f'{len(fails)} checks failed', flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
