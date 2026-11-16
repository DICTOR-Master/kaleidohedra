# Vacuus figures that look like Vacuus: slotted central sheets (16 Nov 2026, after DICTO: "better vacuus figures but they don't
# appear as vacuus in the figures"; plan approved 16 Nov). DICTO's physical Vacuus solids are flat plates slotted together through
# the centre (his cardboard octahedron: 3 squares with half-lap slots). These figures draw the Vacuus that way.
#   RENDER-vacuus-key.png         3D key: heart (octahedron, 3 full square sheets) | non-heart (tetrahedron, 6 fins, one per edge)
#   RENDER-vacuus-A-sheets.png    solid A cut by a 3D hyperplane through its centre: every 4D fin (cone over a 2-face) becomes a
#   RENDER-vacuus-B-sheets.png    flat triangle (centre, p, q); two sections each: symmetric (across the 5-cell axis) and generic
#   RENDER-vacuus-three-kinds.png heart (600-cell) | inherited heart (a diminished 600-cell) | non-heart (A), the same method
# Camera and colours as scripts/render_vacuus.py (DICTO 16 Nov: "keep the view angles and colours"): its standard camera CAM
# (24 degrees above, fixed turn) for the 3D key and the 600-cell family; its locator view along the 5-cell axis (basis
# solid_basis, first locator view) for A and B; its app colours (triangle green, rectangle blue, rhombus pink, hexagon lavender).
# Painting: sheets see-through (order-independent: every pixel composites its sheets back to front by exact depth), two-sided
# light, then the outline of the solid's own section (faint), then slot lines (where two sheets cross, bright), crisp >= 1.5 px.
# Run from the study folder: python scripts/render_sheets.py [--pilot] ; ends "FINAL ok" or "FINAL FAIL".
import os, sys, json, time, itertools
from fractions import Fraction as Fr
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import render_vacuus as RV  # noqa: E402  (camera, palette, canvas)
from sheets_lib import *  # noqa: E402,F401,F403
PILOT = RV.PILOT; SS = RV.SS; P = 520 if PILOT else 900
t0 = time.time(); fails = RV.fails; check = RV.check
GROUND = RV.GROUND; K = RV.KCOL
LOCVIEW0 = [0.25, 1, 0.62]                     # render_vacuus.py: first locator view (5-cell axis projection)
VIEW_A = RV.look(LOCVIEW0, [0, 0, 1])
SLOT = np.array([252, 246, 228.]); RIM = np.array([200, 196, 186.])
STATUS_COL = {'through': K['rectangle'], 'shared': K['rhombus'], 'single': K['triangle']}
LIGHT = RV.LIGHT
NCHK = {'exact': 0}


# ------------------------------------------------------------------ renderer
def render(tris, rims, slots, M, k_px, centre, dots=(), alpha=0.40, size=P, faint=(), dashed=()):
    """tris: [(3x3 float corners, colour)]; rims, slots: [(a, b)] 3D segments; one scale; returns a PIL image."""
    allP = np.vstack([t[0] for t in tris] + [np.zeros((1, 3))])
    cv = RV.Canvas(allP, M, k_px, centre, size=size, margin=0.05)
    W = cv.W; img = cv.img
    S = [(cv.px(t[0]), (t[0] @ M.T)[:, 2], t[1], t[0]) for t in tris]
    TA = np.array([t[2] if len(t) > 2 else alpha for t in tris], np.float32)
    shade = []
    for (_xy, _z, col, T) in S:
        n = np.cross(T[1] - T[0], T[2] - T[0]); n /= np.linalg.norm(n) + 1e-15
        shade.append(np.array(col, np.float32) * (0.62 + 0.38 * abs(n @ LIGHT)))
    zl, zh = cv.zl, cv.zh
    dep = lambda a, b: float(((np.array([a, b]) @ M.T)[:, 2].mean() - zl) / (zh - zl + 1e-12))
    for a, b in faint: cv.line(a, b, tuple(GROUND + (RIM - GROUND) * (0.22 + 0.18 * dep(a, b))), 1.5)   # under the sheets
    TS = 96
    for ty in range(0, W, TS):
        for tx in range(0, W, TS):
            ys, xs = np.mgrid[ty:min(ty + TS, W), tx:min(tx + TS, W)] + 0.5
            Ds, Is = [], []
            for i, (xy, z, col, T) in enumerate(S):
                if xy[:, 0].max() < tx or xy[:, 0].min() > tx + TS or xy[:, 1].max() < ty or xy[:, 1].min() > ty + TS: continue
                (x0, y0), (x1, y1), (x2, y2) = xy
                den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
                if abs(den) < 1e-9: continue
                l0 = ((y1 - y2) * (xs - x2) + (x2 - x1) * (ys - y2)) / den
                l1 = ((y2 - y0) * (xs - x2) + (x0 - x2) * (ys - y2)) / den
                l2 = 1 - l0 - l1
                m = (l0 >= -1e-9) & (l1 >= -1e-9) & (l2 >= -1e-9)
                if not m.any(): continue
                Ds.append(np.where(m, l0 * z[0] + l1 * z[1] + l2 * z[2], np.inf)); Is.append(i)
            if not Ds: continue
            D = np.array(Ds); order = np.argsort(-D, axis=0)      # far (low z) first after reversing below
            tile = img[ty:ty + TS, tx:tx + TS]
            Dsorted = np.take_along_axis(D, order, 0)
            for layer in range(len(Ds) - 1, -1, -1):            # from the farthest (smallest z) to the nearest
                idx = order[layer]; dz = Dsorted[layer]; ok = np.isfinite(dz)
                if not ok.any(): continue
                cols = np.array([shade[Is[j]] for j in range(len(Is))])[idx]
                a = (TA[np.array(Is)][idx] * ok)[..., None]
                tile[:] = tile * (1 - a) + cols * a
    zl, zh = cv.zl, cv.zh
    dep = lambda a, b: float(((np.array([a, b]) @ M.T)[:, 2].mean() - zl) / (zh - zl + 1e-12))
    for a, b, col in dashed: cv.line(a, b, tuple(0.35 * np.array(col) + 0.65 * np.array([235, 232, 222.])), 1.6, dash=4)
    for a, b in rims: cv.line(a, b, tuple(GROUND + (RIM - GROUND) * (0.45 + 0.45 * dep(a, b))), 1.6)
    for a, b in slots: cv.line(a, b, tuple(GROUND + (SLOT - GROUND) * (0.62 + 0.38 * dep(a, b))), 2.3)
    for p, col, r in dots: cv.dot(p, col, r)
    return cv.image()


def slot_segments(tris3, plates):
    """where two sheets of different plates cross: each piece is a triangle (0, a, b) with its corner at the centre, so two pieces
    meet along a segment from the centre in the direction of the line common to their planes; returned merged per direction."""
    N = []
    for a, b in tris3:
        n = np.cross(a, b); N.append(n / np.linalg.norm(n))
    best = {}
    for i in range(len(tris3)):
        for j in range(i + 1, len(tris3)):
            if plates[i] == plates[j]: continue
            d = np.cross(N[i], N[j]); nd = np.linalg.norm(d)
            if nd < 1e-9: continue
            d /= nd
            for sg in (1, -1):
                ext = []
                for (a, b) in (tris3[i], tris3[j]):
                    G = np.array([[a @ a, a @ b], [a @ b, b @ b]]); al, be = np.linalg.solve(G, [sg * d @ a, sg * d @ b])
                    if al < -1e-7 or be < -1e-7: ext.append(None); break
                    ext.append(1 / (al + be))
                if None in ext: continue
                L_ = min(ext); kk = tuple(np.round(sg * d, 5))
                best[kk] = max(best.get(kk, 0), L_)
    return [(np.zeros(3), np.array(kk) * L_) for kk, L_ in best.items()]


# ------------------------------------------------------------------ figure sheet (layout as render_vacuus.sheet)
def compose(panels, title, legend, out, cols):
    f = P / 900; pad = int(40 * f); top = int(30 * f) + len(title) * int(44 * f) + int(20 * f); capl = int(36 * f)
    ft, fc, fs_ = RV.font(int(36 * f)), RV.font(int(25 * f)), RV.font(int(23 * f))
    nl = max(len(p[1]) for p in panels); cap = int(16 * f) + nl * capl
    nrow = (len(panels) + cols - 1) // cols; Wd = cols * P + (cols + 1) * pad
    Hd = top + nrow * (P + cap + pad) + int(52 * f) * len(legend) + int(70 * f)
    im = Image.new('RGB', (Wd, Hd), GROUND); d = ImageDraw.Draw(im)
    for i, line in enumerate(title):
        fn = ft if i == 0 else fc
        check(d.textlength(line, font=fn) < Wd - 2 * pad, f'title fits: {line}')
        d.text((pad, int(20 * f) + i * int(44 * f)), line, font=fn, fill=(236, 230, 214) if i == 0 else (196, 192, 182))
    for i, (img, caps) in enumerate(panels):
        r, c = divmod(i, cols); x = pad + c * (P + pad); y = top + r * (P + cap + pad); im.paste(img, (x, y)); yy = y + P + int(10 * f)
        for li, t in enumerate(caps):
            check(d.textlength(t, font=fc) < P + pad * 0.6, f'caption fits: {t}')
            d.text((x + 6, yy), t, font=fc, fill=(232, 226, 210) if li == 0 else (186, 182, 172)); yy += capl
    y = top + nrow * (P + cap + pad)
    for item in legend:
        if isinstance(item, str):
            d.text((pad, y), item, font=fc, fill=(205, 200, 188)); check(d.textlength(item, font=fc) < Wd - 2 * pad, f'legend fits: {item}')
        else:
            x = pad
            for col, t in item:
                sw = int(26 * f)
                if col == 'slot': d.line([x, y + int(16 * f), x + sw, y + int(16 * f)], fill=tuple(int(v) for v in SLOT), width=max(2, int(3 * f)))
                elif col == 'dash':
                    for xx in range(int(x), int(x) + sw, int(10 * f)): d.line([xx, y + int(16 * f), xx + int(5 * f), y + int(16 * f)], fill=(200, 200, 200), width=max(2, int(2 * f)))
                elif col == 'rim': d.line([x, y + int(16 * f), x + sw, y + int(16 * f)], fill=tuple(int(v) for v in RIM), width=max(2, int(2 * f)))
                else: d.rectangle([x, y + int(3 * f), x + sw, y + int(3 * f) + sw], fill=col)
                x += sw + int(10 * f); d.text((x, y), t, font=fc, fill=(220, 214, 200)); x += d.textlength(t, font=fc) + int(30 * f)
            check(x < Wd, 'legend row fits')
        y += int(52 * f)
    mk = 'DICTO · dictospheres.com'; d.text((Wd - pad - d.textlength(mk, font=fs_), Hd - int(46 * f)), mk, font=fs_, fill=(150, 150, 150))
    im.save(out); return im


def fit(points, M, frac=0.40):
    Q = np.vstack(points) @ M.T; lo, hi = Q[:, :2].min(0), Q[:, :2].max(0)
    return np.r_[(lo + hi) / 2, 0], P * frac / ((hi - lo).max() / 2)


# ------------------------------------------------------------------ 1. the 3D key
def key3d():
    out = []
    # octahedron: corners +-e_i; an edge e_i e_j spans with the centre the plane x_k = 0, which holds 4 edges -> 3 full squares
    O = [tuple(s if t == i else 0 for t in range(3)) for i in range(3) for s in (1, -1)]
    Oe = [(a, b) for a, b in itertools.combinations(range(6), 2) if sum(x * y for x, y in zip(O[a], O[b])) == 0]
    planes = {}
    for a, b in Oe:
        n = tuple(np.cross(O[a], O[b]).tolist()); g = max(abs(x) for x in n); n = tuple(x // g for x in n)
        n = n if next(x for x in n if x) > 0 else tuple(-x for x in n); planes.setdefault(n, []).append((a, b))
    check(len(Oe) == 12 and len(planes) == 3 and all(len(v) == 4 for v in planes.values()), 'octahedron: 12 edges on 3 planes, 4 each')
    for n, es in planes.items():
        for a, b in es: check(np.dot(n, O[a]) == 0 and np.dot(n, O[b]) == 0, 'octahedron edge on its plane (exact)')
    # tetrahedron: corners (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1); fin = triangle (centre, edge)
    T = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    Te = list(itertools.combinations(range(4), 2))
    tn = {}
    for a, b in Te:
        n = tuple(np.cross(T[a], T[b]).tolist()); g = max(abs(x) for x in n); n = tuple(x // g for x in n)
        n = n if next(x for x in n if x) > 0 else tuple(-x for x in n)
        on = [e for e in Te if np.dot(n, T[e[0]]) == 0 and np.dot(n, T[e[1]]) == 0]
        check(on == [(a, b)], f'tetrahedron: the plane through the centre and edge {a}{b} holds that edge only (exact)')
        tn[(a, b)] = n
    check(len(set(tn.values())) == 6, 'tetrahedron: 6 distinct fin planes, no two coplanar (exact)')
    # each fin plane is a mirror: it contains the edge and the midpoint of the opposite edge, normal = the opposite edge direction
    for (a, b), n in tn.items():
        c, d = [i for i in range(4) if i not in (a, b)]; dv = np.subtract(T[c], T[d]); check(np.allclose(np.cross(n, dv), 0), 'fin normal = opposite edge')
    s3 = 1 / np.sqrt(3)
    # the tetrahedron turned (a rigid turn: 315 degrees about z after 30 about x) so that every fin is seen open under CAM
    ca, sa, cb, sb = np.cos(np.radians(315)), np.sin(np.radians(315)), np.cos(np.radians(30)), np.sin(np.radians(30))
    TR = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]]) @ np.array([[1, 0, 0], [0, cb, -sb], [0, sb, cb]])
    Of = [np.array(v, float) for v in O]; Tf = [TR @ np.array(v, float) * s3 for v in T]   # both of circumradius 1
    M = RV.CAM
    ctr, kp = fit(Of + Tf, M, 0.40)
    tris = []
    sq_col = K['rectangle']
    for n, es in planes.items():
        for a, b in es: tris.append((np.array([np.zeros(3), Of[a], Of[b]]), sq_col))
    rims = [(Of[a], Of[b]) for a, b in Oe]
    slots = [(Of[i], Of[i + 1]) for i in (0, 2, 4)]               # the three axes: where the squares slot together
    im1 = render(tris, rims, slots, M, kp, ctr, dots=[(np.zeros(3), (250, 248, 240), 4.5)])
    tris = [(np.array([np.zeros(3), Tf[a], Tf[b]]), K['triangle']) for a, b in Te]
    rims = [(Tf[a], Tf[b]) for a, b in Te]
    slots = [(np.zeros(3), Tf[i]) for i in range(4)]              # three fins meet along each centre-corner line
    im2 = render(tris, rims, slots, M, kp, ctr, dots=[(np.zeros(3), (250, 248, 240), 4.5)])
    compose([(im1, ['heart: the octahedron', '3 full square sheets, slotted at the centre']),
             (im2, ['non-heart: the regular tetrahedron', '6 fins, centre to one edge each'])],
            ['The Vacuus as slotted sheets: a key', 'Each plate is the plane through the centre and an edge. Same camera and scale for both (the tetrahedron turned to open its fins).'],
            [[(sq_col, 'a sheet through the centre (an edge and its opposite on one plate)')],
             [(K['triangle'], 'a fin: one edge on its plate, no two fins on one plane')],
             [('slot', 'slot line: where sheets cross or meet'), ('rim', 'outline of the solid')]],
            f'figures/RENDER-vacuus-key{SFX}.png', 2)
    print(f'PROGRESS 0.15 key ({time.time() - t0:.1f}s)', flush=True)


# ------------------------------------------------------------------ the golden solids A and B, from the exact study data
JS = json.load(open('data/vacuus-exact.json'))
PHI2 = PHI + ONE
VALS = [(0.0, ZERO), (1.0, ONE), (float(PHI), PHI), (float(PHI2), PHI2)]


def exact_of(x):
    v = min(VALS, key=lambda t: abs(t[0] - x)); assert abs(v[0] - x) < 1e-9; return v[1]


def golden(label):
    s = JS[label]; X5 = [[exact_of(x) for x in v] for v in s['V']]
    Y = [tuple(v[i] - v[4] for i in range(4)) for v in X5]          # exact linear chart of the sum-constant 4-space
    kind = {}
    for oi, o in enumerate(s['orbits']):
        for R in o['all_plates_ridges']: kind[frozenset(R)] = oi
    return s, X5, Y, kind


def to5(y):   # exact: the point of the centred 5D space (coordinate sum 0) with chart y
    x5 = -sum(y, ZERO) * Q5(Fr(1, 5)); return [yi + x5 for yi in y] + [x5]


def ab_section(label, u5, B):
    s, X5, Y, kind = golden(label)
    ridges = [frozenset(R) for R in s['ridges']]
    pcs, n = section(Y, s['edges'], ridges, tuple(Q5(x) for x in u5[:4])); NCHK['exact'] += n
    for pc in pcs:   # the same checks in the 5D coordinates of the study: on H (u . x = 0) and in the centred 4-space
        for x in (to5(pc['p']), to5(pc['q'])):
            check(sum((Q5(a) * b for a, b in zip(u5, x)), ZERO).iszero() and sum(x, ZERO).iszero(), 'piece corner on H in 5D (exact)')
            NCHK['exact'] += 2
    rpp = {}
    for R in ridges: kk = key(plate_normal(Y, R)); rpp[kk] = rpp.get(kk, 0) + 1
    check(all(v == 1 for v in rpp.values()) and len(rpp) == s['n_plates'], f'{label[0]}: one 2-face per plate, {s["n_plates"]} plates')
    cl = classify(pcs, rpp); check(all(c == 'single' for c in cl), f'{label[0]}: every piece of the section is a single fin')
    f3 = lambda y: np.array([float(t) for t in to5(y)]) @ B.T
    tris3 = [(f3(pc['p']), f3(pc['q'])) for pc in pcs]
    # metric check: the drawing keeps lengths (B is orthonormal and spans H)
    for pc, (a, b) in zip(pcs[:5], tris3[:5]):
        d5 = np.array([float(t) for t in to5(pc['p'])]) - np.array([float(t) for t in to5(pc['q'])])
        check(abs(np.linalg.norm(d5) - np.linalg.norm(a - b)) < 1e-9, 'drawing keeps lengths')
    return pcs, tris3, [kind[pc['ridge']] for pc in pcs], [pc['plate'] for pc in pcs], cl


def h_basis(u5):
    one = np.ones(5) / np.sqrt(5); u = np.array(u5, float); u /= np.linalg.norm(u)
    return ortho_basis(RV.solid_basis(), [one, u])


KIND_COL = {'A': [K['triangle'], K['hexagon']],
            'B': [K['triangle'], (196, 226, 64), K['rectangle'], (52, 200, 160)]}
KIND_WORD = {'A': ['A1: the 20 triangle plates', 'A2: the 10 hexagon plates'],
             'B': ['B1: triangles (octahedron | prism)', 'B2: triangles (cuboctahedron | octahedron)',
                   'B3: the 30 rectangle plates', 'B4: triangles (two cuboctahedra)']}
SECTIONS = [('symmetric', (1, 1, 1, 1, -4), 'across the 5-cell axis through coordinate 5'),
            ('generic', (3, -1, 7, -2, -7), 'a generic hyperplane, normal (3, -1, 7, -2, -7)')]


def ab_figure(tag):
    label = [k for k in JS if k.startswith(tag + ':')][0]; seed = label.split('of ')[1]
    built = []
    for nm, u5, words in SECTIONS:
        assert sum(u5) == 0
        B = h_basis(u5); pcs, tris3, kinds, plates, cl = ab_section(label, u5, B)
        built.append((nm, words, pcs, tris3, kinds, plates))
    ctr0, kp = fit([np.vstack([a, b]) for b_ in built for (a, b) in b_[3]], VIEW_A, 0.42)
    panels = []
    for nm, words, pcs, tris3, kinds, plates in built:
        tris = [(np.array([np.zeros(3), a, b]), KIND_COL[tag][kd]) for (a, b), kd in zip(tris3, kinds)]
        rims = [(a, b) for a, b in tris3]
        slots = slot_segments(tris3, plates)
        ctr, _ = fit([np.vstack([a, b]) for a, b in tris3], VIEW_A)
        im = render(tris, rims, slots, VIEW_A, kp, ctr, dots=[(np.zeros(3), (250, 248, 240), 4.5)])
        cnt = [kinds.count(i) for i in range(len(KIND_COL[tag]))]
        panels.append((im, [f'{nm} section: {words}', f'{len(pcs)} fins on {len(set(plates))} plates: ' + ', '.join(f'{c} {tag}{i + 1}' for i, c in enumerate(cnt) if c)]))
        print(f'PROGRESS {tag} {nm}: {len(pcs)} fins, {len(slots)} slot lines ({time.time() - t0:.1f}s)', flush=True)
    sol = JS[label]
    compose(panels, [f'Solid {tag}, perms of {seed}: its Vacuus as slotted sheets',
                     f'A 3D cut through the centre of the 4D solid. Each of its {sol["n_plates"]} plates is a 4D fin (centre to one two-face);',
                     'the cut turns every fin it meets into one flat triangular sheet. Both cuts at one scale; view as the locator views.'],
            [[(KIND_COL[tag][i], w) for i, w in enumerate(KIND_WORD[tag][:2])]] + ([[(KIND_COL[tag][i], w) for i, w in enumerate(KIND_WORD[tag][2:], 2)]] if tag == 'B' else []) +
            ['Every sheet is single: one fin per plate, none passes through the centre (the non-heart kind).',
             [('slot', 'slot line: where fins meet or cross'), ('rim', "outline of the solid's own 3D section")]],
            f'figures/RENDER-vacuus-{tag}-sheets{SFX}.png', 2)


def pick_spread(cand, pl, t3, k=3, must_slot=True):
    """k plates whose sheets are as near perpendicular to each other as possible (then the most triangles)."""
    nrm = {}
    for p, (a, b) in zip(pl, t3):
        if p in cand and p not in nrm: n = np.cross(a, b); nrm[p] = n / np.linalg.norm(n)
    size = {p: pl.count(p) for p in cand}
    tri_of = {p: [t for t, q in zip(t3, pl) if q == p] for p in cand}
    def slotted(x, y):   # total slot length between two sheets (0 when their common line runs through gaps)
        segs = slot_segments(tri_of[x] + tri_of[y], [x] * len(tri_of[x]) + [y] * len(tri_of[y]))
        return sum(np.linalg.norm(b_) for _a, b_ in segs)
    cache = {}
    def sl(x, y):
        if (x, y) not in cache: cache[(x, y)] = slotted(x, y)
        return cache[(x, y)]
    trip = [c for c in itertools.combinations(sorted(cand), k) if max(abs(nrm[x] @ nrm[y]) for x, y in itertools.combinations(c, 2)) < 0.6
            and abs(np.linalg.det(np.array([nrm[x] for x in c]))) > 0.4]
    trip = trip or list(itertools.combinations(sorted(cand), k))
    area = {p: sum(np.linalg.norm(np.cross(a, b)) / 2 for a, b in tri_of[p]) for p in cand}
    # first: every pair slots (heart family); then the largest sheets, so the eye reads them as sheets
    best = min(trip, key=lambda c: (-sum(sl(x, y) > 1e-6 for x, y in itertools.combinations(c, 2)) if must_slot else 0,
                                    -round(sum(area[x] for x in c), 6)))
    if must_slot: check(all(sl(x, y) > 1e-6 for x, y in itertools.combinations(best, 2)), 'the three solid sheets slot pairwise')
    return set(best)


def frame_of(hl, pl, t3):
    """rotation taking the normals of the three chosen sheets (Gram-Schmidt, in order) to the coordinate axes."""
    N = []
    for p in sorted(hl):
        a, b = t3[pl.index(p)]; n = np.cross(a, b); N.append(n / np.linalg.norm(n))
    Rm = ortho_basis(N, [])
    if np.linalg.det(Rm) < 0: Rm[2] = -Rm[2]
    print('  chosen sheets: |cos| between normals', [round(abs(N[i] @ N[j]), 3) for i, j in itertools.combinations(range(3), 2)], flush=True)
    return Rm


def highlight_panel(t3, pl, cl, hl, M, kp, ctr):
    """the highlighted plates' sheets solid with their slot lines and their own edges; every other sheet a faint ghost."""
    tris, rims, faint = [], [], []
    for (a, b), p, c in zip(t3, pl, cl):
        tris.append((np.array([np.zeros(3), a, b]), STATUS_COL[c], 0.55 if p in hl else 0.045))
        (rims if p in hl else faint).append((a, b))
    for p in hl:   # sheet boundary along a spoke: a corner used by one triangle of this sheet only
        cnt = {}
        for (a, b), q in zip(t3, pl):
            if q == p:
                for x in (a, b): kx = tuple(np.round(x, 7)); cnt[kx] = cnt.get(kx, 0) + 1
        rims += [(np.zeros(3), np.array(kx)) for kx, n in cnt.items() if n == 1]
    dashed = []
    for p in hl:   # the plate's whole cut: the plane of its sheet across the solid's 3D section (convex polygon)
        a0, b0 = t3[pl.index(p)]; n = np.cross(a0, b0); n /= np.linalg.norm(n); pts = []
        for a, b in t3:
            sa, sb = n @ a, n @ b
            if abs(sa) < 1e-9: pts.append(a)
            if abs(sb) < 1e-9: pts.append(b)
            if sa * sb < -1e-18: pts.append(a + (b - a) * sa / (sa - sb))
        pts = np.unique(np.round(np.array(pts), 7), axis=0); e1 = a0 / np.linalg.norm(a0); e2 = np.cross(n, e1)
        pts = pts[np.argsort(np.arctan2(pts @ e2, pts @ e1))]
        col = STATUS_COL[cl[pl.index(p)]]
        dashed += [(pts[t], pts[(t + 1) % len(pts)], col) for t in range(len(pts))]
    idx = [i for i, p in enumerate(pl) if p in hl]
    slots = slot_segments([t3[i] for i in idx], [pl[i] for i in idx]); print(f'  {len(slots)} slot lines among the solid sheets', flush=True)
    return render(tris, rims, slots, M, kp, ctr, dots=[(np.zeros(3), (250, 248, 240), 4.5)], faint=faint, dashed=dashed)


# ------------------------------------------------------------------ 3. the three kinds
def three_kinds():
    V6 = L.V600; E6 = [tuple(e) for e in L.ST600['E']]; T6 = [frozenset(t) for t in L.ST600['T']]
    u = L.C600[0]                                    # across a cell centre (a cross wall of the Queens: not itself a plate)
    uf = fl(u); uf /= np.linalg.norm(uf)
    B4 = ortho_basis(np.eye(4), [uf])
    # inherited heart: remove an independent set of corners lying on one side of the cut (so the cut shows the loss)
    w = B4[0] @ np.eye(4)   # a direction inside H
    adj = {i: set() for i in range(len(V6))}
    for a, b in E6: adj[a].add(b); adj[b].add(a)
    order = sorted(range(len(V6)), key=lambda i: -fl(V6[i]) @ w)
    rem = []
    for i in order:
        if fl(V6[i]) @ w <= 0.5: break
        if not (adj[i] & set(rem)): rem.append(i)
    keep = [i for i in range(len(V6)) if i not in rem]
    VD = [V6[i] for i in keep]
    fac, rid, _ = L.lattice(np.array([fl(v) for v in VD]))
    ED = set()
    for r in rid: ED |= L.polygon_edges(np.array([fl(v) for v in VD]), r)
    check(len(VD) - len(ED) + len(rid) - len(fac) == 0, 'diminished 600-cell: Euler in 4D')
    ks = {key(v) for v in VD}; csym = all(key(neg(v)) in ks for v in VD)
    check(not csym, 'diminished 600-cell: not centrally symmetric')
    out = []
    for name, V, E, R in (('600-cell', V6, E6, T6), ('diminished', VD, sorted(ED), [frozenset(r) for r in rid])):
        rpp = {}
        for r in R: kk = key(plate_normal(V, r)); rpp[kk] = rpp.get(kk, 0) + 1
        pcs, n = section(V, E, R, u); NCHK['exact'] += n
        cl = classify(pcs, rpp)
        hist = {}
        for v in rpp.values(): hist[v] = hist.get(v, 0) + 1
        print(f'  {name}: {len(V)} corners, {len(R)} two-faces, {len(rpp)} plates, two-faces per plate {dict(sorted(hist.items()))}; '
              f'cut: {len(pcs)} pieces ' + str({k: cl.count(k) for k in ('through', 'shared', 'single')}), flush=True)
        out.append((name, V, R, rpp, pcs, cl))
    check(all(c == 'through' for c in out[0][5]), '600-cell: every piece has its opposite on its plate (heart)')
    check(any(c == 'shared' for c in out[1][5]) and any(c == 'through' for c in out[1][5]), 'diminished: both through and one-sided shared pieces')
    check(min(out[1][3].values()) >= 2, 'diminished: every plate carries two or more two-faces (inherited heart)')
    # A: symmetric section, in its own view
    labA = [k for k in JS if k.startswith('A:')][0]
    BA = h_basis((1, 1, 1, 1, -4)); pcsA, trisA, kindsA, platesA, clA = ab_section(labA, (1, 1, 1, 1, -4), BA)
    M = RV.CAM
    f3 = lambda x: fl(x) @ B4.T
    panels = []
    allp = [np.vstack([f3(pc['p']), f3(pc['q'])]) for pc in out[0][4]]
    ctr, kp = fit(allp, M, 0.42)
    words = {'600-cell': ['heart: the 600-cell', 'full sheets through the centre'],
             'diminished': [f'inherited heart: 600-cell less {len(rem)} corners', 'shared sheets, some one-sided'],
             'A': ['non-heart: solid A', 'single fins, one side of the centre']}
    # scale from the circumradius (any turn of the cut stays inside it): the 600-cell family at one scale, the centre in the middle
    rA = max(np.linalg.norm(np.array(v) - np.array(JS[labA]['centre'])) for v in JS[labA]['V'])
    runs = [(name, [(f3(pc['p']), f3(pc['q'])) for pc in pcs], [pc['plate'] for pc in pcs], cl, P * 0.43 / 2.0, np.zeros(3)) for name, V, R, rpp, pcs, cl in out]
    runs.append(('A', trisA, platesA, clA, P * 0.43 / rA, np.zeros(3)))
    for name, t3, pl, cl, kp_, ctr_ in runs:
        cand = sorted({p for p, c in zip(pl, cl) if (c == 'shared' if name == 'diminished' else True)})
        hl = pick_spread(cand, pl, t3, must_slot=(name != 'A'))
        # turn the cut (a rotation inside H, lengths kept) so the three solid sheets stand like the key's three squares
        Rm = frame_of(hl, pl, t3); t3 = [(Rm @ a, Rm @ b) for a, b in t3]
        check(np.allclose(Rm @ Rm.T, np.eye(3)) and np.linalg.det(Rm) > 0, 'turn inside H is a rotation')
        im = highlight_panel(t3, pl, cl, hl, M, kp_, ctr_)
        nsh = len(set(pl)); kinds_hl = sorted({c for p, c in zip(pl, cl) if p in hl})
        unit = 'fins' if name == 'A' else 'sheets'
        panels.append((im, words[name] + [f'{nsh} {unit} ({len(t3)} triangles); 3 shown solid']))
        print(f'PROGRESS three-kinds {name}: highlighted plates carry {kinds_hl} ({time.time() - t0:.1f}s)', flush=True)
    compose(panels, ['The three kinds of Vacuus, cut in 3D through the centre',
                     'Each 4D plate meets the cut in one flat sheet. Three large sheets solid (at least 53° apart), the rest faint.',
                     'Left, middle: one cut across a cell centre, one scale. Right: solid A across its 5-cell axis. Camera as the key.'],
            [[(STATUS_COL['through'], 'sheet through the centre (its opposite on the same plate)')],
             [(STATUS_COL['shared'], 'on a shared plate, opposite missing'), (STATUS_COL['single'], 'single fin')],
             [('slot', 'slot line'), ('dash', "the plate's whole cut (dashed)"), ('rim', "outline of the solid's 3D section")]],
            f'figures/RENDER-vacuus-three-kinds{SFX}.png', 3)
    return rem


if __name__ == '__main__':
    SFX = '-pilot' if PILOT else ''
    os.makedirs('figures', exist_ok=True)
    try:
        key3d()
        for tag in ('A', 'B'): ab_figure(tag)
        rem = three_kinds()
        print(f'diminished: removed corners {rem}', flush=True)
    except AssertionError as e:
        check(False, f'exact assertion: {e}')
    print(f'{NCHK["exact"]} exact corner checks passed; {len(fails)} checks failed; {time.time() - t0:.1f}s', flush=True)
    made = [f'figures/RENDER-vacuus-{n}{SFX}.png' for n in ('key', 'A-sheets', 'B-sheets', 'three-kinds')]
    print('FINAL ok' if not fails and all(os.path.exists(m) for m in made) else 'FINAL FAIL', flush=True)
