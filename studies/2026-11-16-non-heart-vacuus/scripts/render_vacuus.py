# Renders of the non-heart Vacuus of the golden solids A and B ("Silent Running: Twisted Silence", DICTO 16 Nov 2026).
# Input: data/vacuus-exact.json from scripts/vacuus_exact.py (exact Q(sqrt5) analysis; float coordinates for drawing only).
#   (a) RENDER-non-heart-vacuus-{A,B}-slices.png: one slice per plate orbit (the solid cut by one central plate) as a see-through
#       crystal polyhedron; the plate's own ridge filled in the orbit colour with a gold rim; white dots = corners of the solid,
#       the other corners are where the plate crosses an edge of the solid.
#   (b) RENDER-non-heart-vacuus-{A,B}-plates.png: the solid projected to 3D along one 5-cell axis (keeps the tetrahedral part of the
#       symmetry), edges as a depth-shaded wire cage; for each orbit, every plate of that orbit drawn as a translucent fin = the cone from
#       the centre over its ridge.
# Painting: back faces first, then front faces, then edges on top (the 2D form of polygon offset); 3x supersampling, edges >= 1.6 px
# after downsampling, depth-shaded (near bright, far dim), no haze; orthographic, one scale for x and y; every model asserted inside
# its frame margin. Sheet layout and DICTO mark as studies/2026-11-15-golden-a4-candidate/scripts/silent_render.py.
# Run from the study folder: python scripts/render_vacuus.py [--pilot]  ; ends "FINAL ok".
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
PILOT = '--pilot' in sys.argv
SS = 2 if PILOT else 3; SIZE = 560 if PILOT else 1100
GROUND = (21, 25, 33); EDGE = np.array([240, 234, 216.]); GOLD = (232, 190, 70); CRYSTAL = np.array([170, 200, 225.])
EL = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(px): return ImageFont.truetype(FONT, px)
def look(d, up):
    z = np.array(d, float); z /= np.linalg.norm(z); up = np.array(up, float); x = np.cross(up, z); x /= np.linalg.norm(x); y = np.cross(z, x)
    return np.array([x, y, z])
def rot(axis, deg):
    a = np.array(axis, float); a /= np.linalg.norm(a); t = np.radians(deg); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
class Canvas:
    """Supersampled float canvas; every model point is mapped with ONE scale for x and y (aspect kept), asserted inside the margin."""
    def __init__(s, P3, M, size=SIZE, margin=0.07):
        s.M, s.size, s.W = M, size, size * SS
        Q = P3 @ M.T; lo, hi = Q.min(0), Q.max(0); inner = s.W * (1 - 2 * margin)
        s.k = inner / max(hi[0] - lo[0], hi[1] - lo[1]); s.lo, s.hi = lo, hi
        s.ox = (s.W - s.k * (hi[0] - lo[0])) / 2; s.oy = (s.W - s.k * (hi[1] - lo[1])) / 2
        s.zl, s.zh = lo[2], hi[2]; s.img = np.zeros((s.W, s.W, 3), np.float32); s.img[:] = GROUND
        px = s.px(P3); m = margin * s.W * 0.999
        assert px[:, 0].min() >= m - 1 and px[:, 0].max() <= s.W - m + 1 and px[:, 1].min() >= m - 1 and px[:, 1].max() <= s.W - m + 1, 'model outside frame'
    def px(s, P): Q = np.atleast_2d(P) @ s.M.T; return np.c_[s.ox + s.k * (Q[:, 0] - s.lo[0]), s.oy + s.k * (s.hi[1] - Q[:, 1])]
    def depth(s, P): return float(((np.atleast_2d(P) @ s.M.T)[:, 2].mean() - s.zl) / (s.zh - s.zl + 1e-12))   # 0 far .. 1 near
    def _blend(s, draw_fn, col, alpha):
        L = Image.new('L', (s.W, s.W), 0); draw_fn(ImageDraw.Draw(L))
        a = np.asarray(L, np.float32) / 255 * alpha; ys, xs = np.nonzero(a)
        if len(ys) == 0: return
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; aa = a[y0:y1, x0:x1, None]
        s.img[y0:y1, x0:x1] = s.img[y0:y1, x0:x1] * (1 - aa) + np.array(col, np.float32) * aa
    def poly(s, P, col, alpha): q = [tuple(p) for p in s.px(P)]; s._blend(lambda d: d.polygon(q, fill=255), col, alpha)
    def line(s, a, b, col, w_px, alpha=1.0):
        q = s.px(np.array([a, b])); w = max(1, int(round(w_px * SS)))
        def f(d):
            d.line([tuple(q[0]), tuple(q[1])], fill=255, width=w)
            r = w / 2; [d.ellipse([x - r, y - r, x + r, y + r], fill=255) for x, y in q]   # round caps
        s._blend(f, col, alpha)
    def dot(s, P, col, r_px):
        x, y = s.px(P)[0]; r = r_px * SS; s._blend(lambda d: d.ellipse([x - r, y - r, x + r, y + r], fill=255), col, 1.0)
    def image(s): return Image.fromarray(np.clip(s.img, 0, 255).astype(np.uint8)).resize((s.size, s.size), Image.LANCZOS)
def shade(col, t): return tuple(float(c) for c in np.array(GROUND) + (np.array(col, float) - GROUND) * (0.42 + 0.58 * t))
# ------------------------------------------------------------------ (a) a slice as a crystal
def crystal(sl, colr, view):
    X = np.array(sl['X3']); X = X - X.mean(0); X /= np.linalg.norm(X, axis=1).max()
    faces = [f['cycle'] for f in sl['faces']]; ridge = [f for f in sl['faces'] if f['ridge']][0]['cycle']
    rn = X[ridge].mean(0)                                    # the ridge face's outward direction (the slice is centred at its mean)
    M = look(view(rn), [0, 0, 1] if abs(rn[2]) < 0.9 else [1, 0, 0])
    cv = Canvas(X, M); l = np.array([-0.4, 0.55, 0.73]); l /= np.linalg.norm(l)
    def nrm(cyc):
        P = X[cyc]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        return n if n @ (P.mean(0)) > 0 else -n
    front = lambda cyc: (M @ nrm(cyc))[2] > 0
    order = sorted(faces, key=lambda c: cv.depth(X[c]))
    for cyc in order:   # back faces
        if not front(cyc): cv.poly(X[cyc], colr if cyc == ridge else tuple(CRYSTAL * 0.8), 0.80 if cyc == ridge else 0.10)
    E = sorted(sl['edges'], key=lambda e: cv.depth(X[list(e)]))
    for i, j in E:      # all edges, depth-shaded (the far ones show through the crystal)
        cv.line(X[i], X[j], shade(EDGE, cv.depth(X[[i, j]])), 1.7)
    for cyc in order:   # front faces: a light glassy tint, lit
        if front(cyc):
            n = M @ nrm(cyc); lit = 0.55 + 0.45 * max(0.0, n @ l)
            if cyc == ridge: cv.poly(X[cyc], colr, 0.80)
            else: cv.poly(X[cyc], tuple(CRYSTAL * lit), 0.16)
    for i, j in E:      # front edges again on top of the front faces (crisp)
        on_front = any(front(c) and i in c and j in c for c in faces)
        if on_front: cv.line(X[i], X[j], shade(EDGE, cv.depth(X[[i, j]])), 2.0)
    for t in range(len(ridge)): cv.line(X[ridge[t]], X[ridge[(t + 1) % len(ridge)]], GOLD, 2.8)
    for k, o in enumerate(sl['origin']):
        if o[0] == 'vertex': cv.dot(X[k], (250, 248, 240), 3.4)
    return cv.image()
# ------------------------------------------------------------------ (b) plates as fins over the solid
FINVIEW = [float(t) for t in os.environ.get('FINVIEW', '1,0.55,0.42').split(',')]
def solid_basis():
    # orthonormal basis of {x : x5 = 0, x1 + .. + x4 = 0}: projection along the 5-cell axis through coordinate 5 (tetrahedral symmetry)
    A = np.array([[1, -1, 0, 0, 0], [0, 1, -1, 0, 0], [0, 0, 1, -1, 0]], float); Q, _ = np.linalg.qr(A.T); return Q.T
def fins(sol, orb, colr):
    V = np.array(sol['V']) - np.array(sol['centre']); P = V @ solid_basis().T; P /= np.linalg.norm(P, axis=1).max()
    M = look(FINVIEW, [0, 0, 1])
    cv = Canvas(np.vstack([P, np.zeros((1, 3))]), M)
    tris = []
    for R in orb['all_plates_ridges']:
        Q = P[R]; m = Q.mean(0); U = np.linalg.svd(np.array(V)[R] - np.array(V)[R].mean(0))[2]   # order the ridge in its own 4D plane
        W = (np.array(V)[R] - np.array(V)[R].mean(0)); ang = np.arctan2(W @ U[1], W @ U[0]); cyc = [R[k] for k in np.argsort(ang)]
        for t in range(len(cyc)): tris.append(np.array([np.zeros(3), P[cyc[t]], P[cyc[(t + 1) % len(cyc)]]]))
    E = sorted(sol['edges'], key=lambda e: cv.depth(P[list(e)]))
    for i, j in E:
        t = cv.depth(P[[i, j]])
        if t < 0.5: cv.line(P[i], P[j], shade(EDGE, 0.6 * t), 1.6)
    for T in sorted(tris, key=lambda T: cv.depth(T)):
        t = cv.depth(T); cv.poly(T, shade(colr, 0.55 + 0.45 * t), 0.14 * min(1.0, 20 / len(orb['all_plates_ridges'])))
    spokes = sorted({k for R in orb['all_plates_ridges'] for k in R}, key=lambda k: cv.depth(np.array([np.zeros(3), P[k]])))
    for k in spokes: cv.line(np.zeros(3), P[k], shade(colr, 0.35 + 0.45 * cv.depth(np.array([np.zeros(3), P[k]]))), 1.6, 0.8)
    for R in orb['all_plates_ridges']:   # each ridge's rim in the orbit colour
        W = np.array(V)[R] - np.array(V)[R].mean(0); U = np.linalg.svd(W)[2]; cyc = [R[k] for k in np.argsort(np.arctan2(W @ U[1], W @ U[0]))]
        for t in range(len(cyc)):
            a, b = P[cyc[t]], P[cyc[(t + 1) % len(cyc)]]; cv.line(a, b, shade(colr, 0.5 + 0.5 * cv.depth(np.array([a, b]))), 2.0)
    for i, j in E:
        t = cv.depth(P[[i, j]])
        if t >= 0.5: cv.line(P[i], P[j], shade(EDGE, 0.8 * t), 1.8)
    cv.dot(np.zeros(3), (250, 248, 240), 4.5)
    return cv.image()
# ------------------------------------------------------------------ sheet: a grid of panels, two caption lines each, DICTO mark
def sheet(panels, title, legend, out, cols):
    P = panels[0][0].size[0]; f = P / 1100; pad = int(46 * f); top = int(150 * f); cap = int((20 + 38 * max(len(p[1]) for p in panels)) * f)
    ft, fc, fl, fm = font(int(40 * f)), font(int(27 * f)), font(int(27 * f)), font(int(24 * f))
    rows = (len(panels) + cols - 1) // cols
    Wd = cols * P + (cols + 1) * pad; lh = int(42 * f)
    Hd = top + rows * (P + cap + pad) + len(legend) * lh + int(80 * f)
    im = Image.new('RGB', (Wd, Hd), GROUND); d = ImageDraw.Draw(im)
    for k, line in enumerate(title): d.text((pad, int(26 * f) + k * int(52 * f)), line, font=ft if k == 0 else fc, fill=(236, 230, 214) if k == 0 else (200, 196, 186))
    for k, (p, caps, sw) in enumerate(panels):
        r, cc = divmod(k, cols); x = pad + cc * (P + pad); y = top + r * (P + cap + pad); im.paste(p, (x, y))
        for li, c in enumerate(caps):
            assert d.textlength(c, font=fc) < P - 10, ('caption too long', c)
            tw = d.textlength(c, font=fc) + (int(36 * f) if li == 0 else 0); x0 = x + (P - tw) / 2; yy = y + P + int(10 * f) + li * int(38 * f)
            if li == 0: d.rectangle([x0, yy + int(3 * f), x0 + int(24 * f), yy + int(27 * f)], fill=sw); x0 += int(36 * f)
            d.text((x0, yy), c, font=fc, fill=(220, 214, 200) if li == 0 else (190, 186, 176))
    y = top + rows * (P + cap + pad)
    for line in legend:
        assert d.textlength(line, font=fl) < Wd - 2 * pad, ('legend too long', line); d.text((pad, y), line, font=fl, fill=(205, 200, 188)); y += lh
    mk = 'DICTO · dictospheres.com'; d.text((Wd - pad - d.textlength(mk, font=fm), Hd - int(48 * f)), mk, font=fm, fill=(150, 150, 150))
    im.save(out); return im
# ------------------------------------------------------------------ main
if __name__ == '__main__':
    js = json.load(open('data/vacuus-exact.json'))
    SOL = {'A': ('A: perms of (φ², φ², φ², φ, 0)', '(φ², φ², φ², φ, 0)', ['T', 'I']),
           'B': ('B: perms of (φ², φ², 1, 1, 0)', '(φ², φ², 1, 1, 0)', ['O', 'C', 'I', 'D'])}
    CELLWORD = {'tetrahedron': 'tetrahedron', 'truncated tetrahedron': 'golden truncated tetrahedron', 'octahedron': 'octahedron',
                'triangular prism': 'golden prism', 'cuboctahedron': 'golden cuboctahedron'}
    NAMES = {'equilateral triangle': 'triangle', 'equiangular hexagon': 'hexagon', 'rectangle': 'rectangle'}
    os.makedirs('figures', exist_ok=True); made = []
    VIEW = lambda rn: rot(np.cross(rn, [0.3, 0.2, 0.93]) if np.linalg.norm(np.cross(rn, [0.3, 0.2, 0.93])) > 1e-3 else [1, 0, 0], 52) @ rn
    for si, (tag, (key, seed, cols)) in enumerate(SOL.items()):
        sol = js[key]; orbs = sol['orbits']; slices, finp = [], []
        FINVIEW = {'A': [0.25, 1, 0.62], 'B': [1, 0.55, 0.42]}[tag]   # camera per solid (pilot of four views, 16 Nov)
        for oi, o in enumerate(orbs):
            sl = o['slice']; colr = EL[cols[oi]]
            rf = [f for f in sl['faces'] if f['ridge']][0]
            ridge_word = o['ridge_shape'].split(',')[0]; ridge_word = NAMES.get(ridge_word, ridge_word)
            side = o['ridge_shape'].split('side')[-1].strip() if ' side ' in o['ridge_shape'] else o['ridge_shape'].split('sides')[-1].replace(' in turn', '').strip()
            between = ' | '.join(CELLWORD[c] for c in rf['cellnames']) if len(rf['cellnames']) == 2 else f'two {CELLWORD[rf["cellnames"][0]]}s'
            c1 = f'{o["n_plates"]} plates on the {ridge_word}s ({side})'
            nv, ne, nf = sl['counts']
            c2 = f'between {between}'; c3 = f'slice: {nv} corners, {ne} edges, {nf} faces'
            img = crystal(sl, colr, VIEW); slices.append((img, [c1, c2, c3], colr))
            finp.append((fins(sol, o, colr), [c1, c2], colr))
            print(f'PROGRESS {(si + (oi + 1) / len(orbs)) / 2:.2f} {tag} orbit {oi + 1}', flush=True)
        if PILOT:
            for k, (img, *_r) in enumerate(slices): img.save(f'figures/pilot-{tag}-slice{k + 1}.png')
            for k, (img, *_r) in enumerate(finp): img.save(f'figures/pilot-{tag}-fins{k + 1}.png')
            made += [f'figures/pilot-{tag}-slice1.png']; continue
        nr = sum(o['n_plates'] for o in orbs)
        ncol = 2
        t1 = [f'Solid {tag}, perms of {seed}: the non-heart Vacuus, one slice per kind of plate',
              f'{len(sol["V"])} corners, {len(sol["ridges"])} two-faces on {sol["n_plates"]} central plates, one two-face per plate; '
              f'{len(orbs)} kinds of plate under the {sol["group_order"]} symmetries']
        leg = ['Each panel: the solid cut by one central plate (the hyperplane through the centre and one two-face), seen as a clear crystal.',
               'Filled with a gold rim: the plate\'s own two-face. White dots: corners of the solid; the other corners are where the plate cuts an edge.']
        sheet(slices, t1, leg, f'figures/RENDER-non-heart-vacuus-{tag}-slices.png', ncol); made.append(f'figures/RENDER-non-heart-vacuus-{tag}-slices.png')
        t2 = [f'Solid {tag}, perms of {seed}: the {sol["n_plates"]} central plates, by kind',
              f'Each plate drawn as the cone from the centre (white dot) over its two-face, rimmed in the orbit colour; the solid as a wire cage']
        leg2 = ['Projection to 3D along the direction of one coordinate axis of the 5-cell (keeps the 24 symmetries of the tetrahedron).',
                'One two-face per plate: the solid has no centre of symmetry, so no plate carries an opposite pair. This is the non-heart kind of Vacuus.']
        sheet(finp, t2, leg2, f'figures/RENDER-non-heart-vacuus-{tag}-plates.png', ncol); made.append(f'figures/RENDER-non-heart-vacuus-{tag}-plates.png')
    ok = all(os.path.exists(m) for m in made)
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
