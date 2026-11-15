# Front cover of "The Platonic Solids" (Book Eight of The Five Orders of Space), series style (DICTO 15 Nov 2026: a new cover
# "matching protocols", the house style of his other book covers). The five Platonic solids as stones in their element colours, each
# seated in its gold setting of #106 (Table 1) and the book's Chapter 10 (Filigree, Table 10.2), so that stone and setting together
# are exactly the dodecahedron of edge 1: D bare (the stone is the cell), I in six Admiral Caps + eight caps, C in Euclid's six roofs,
# T in four corner tetrahedra + six roofs, O (edge phi^2/sqrt2) in eight caps. Every jewel fills the same cell, so all five are drawn
# at one scale. The front half of each setting is left off so the stone shows (as Chapter 10's figures leave the upper caps off).
# Exact pieces from the checked builders of study 2026-11-14-platonic-hybrid (golden.py, Q(sqrt5)) through the filigree study's
# piece_faces (studies/2026-11-15-filigree/scripts/jewels_lib.py); exact checks (volumes, gold shares, edges, containment) run first.
# Layout, lettering and painting (z-buffer, glossy light, light crease edges shaded by depth) copied from the Permutohedron Paradigm
# cover script (studies/2026-11-15-paradigm-cover/scripts/cover.py, itself after the Space-Fillers cover); series line above the
# title as on The Golden Cycle and Star Cores. LED lettering: DSEG14 by keshikan (SIL Open Font Licence, DSEG-LICENSE.txt).
# Run from this folder: python cover.py [view ...]  -> ../platonic-cover-front-series.png (FINAL=1) and ../platonic-dicto-mark-back.png
import os, sys, itertools
import numpy as np
from scipy import ndimage
from PIL import Image
import ledtext as L
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-filigree', 'scripts'))
import jewels_lib as J                                   # imports golden.py and hybrid.py of the hybrid study
G, H = J.G, J.H
from golden import V, Part, PHI, Q5
FAIL = []
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
# ------------------------------------------------------------------ the five jewels (exact, Q(sqrt5)), cell centred at the origin
R5 = Q5(0, 1); TWO = Q5(2)
EVEN = [v for v in G.CUBE if sum(1 for x in v if x < 0) % 2 == 0]       # the tetrahedron of edge phi sqrt2 on alternate cube corners
ODD = [v for v in G.CUBE if v not in EVEN]
d2 = lambda a, b: G.dot(G.sub(a, b), G.sub(a, b))
def corner_tet(c): return [c] + [v for v in G.CUBE if d2(v, c) == PHI * PHI]   # a cube corner and its three neighbours (legs phi)
ROOFS = [('R', [Part(G.ROOFS[k])], []) for k in sorted(G.ROOFS)]
JEWELS = {   # stone label -> (stone corners, gold pieces as (label, positive parts, negative parts))
    'D': (G.DOD, []),
    'I': (G.ICO, [p for p in H.cell_pieces(V(0, 0, 0), 'I') if p[0] != 'I']),
    'C': (G.CUBE, ROOFS),
    'T': (EVEN, [('gT', [Part(corner_tet(c))], []) for c in ODD] + ROOFS),
    'O': (G.OCT, [('cap', [Part(vs)], []) for s, vs in G.caps8()]),
}
EDGE2 = {'D': Q5(1), 'I': Q5(1), 'C': PHI * PHI, 'T': 2 * PHI * PHI, 'O': PHI * PHI * PHI * PHI / 2}
SHARE = {'D': Q5(0), 'I': (11 - 3 * R5) / 6, 'C': 1 / R5, 'T': (10 + R5) / 15, 'O': (25 - 3 * R5) / 30}   # Table 10.2
COUNT = {'D': {}, 'I': {'A': 6, 'cap': 8}, 'C': {'R': 6}, 'T': {'gT': 4, 'R': 6}, 'O': {'cap': 8}}
def checks():
    vD = G.volume(G.DOD); X('cell: the dodecahedron of edge 1 has volume (15 + 7 sqrt5)/4', vD == (15 + 7 * R5) / 4, vD)
    PD = G.planes_from_vertices(G.DOD)
    for k, (st, gold) in JEWELS.items():
        e = min(d2(a, b) for a, b in itertools.combinations(st, 2))
        X(f'{k}: stone edge squared {EDGE2[k]}', e == EDGE2[k], e)
        vg = sum((G.volume(p.verts) for pc in gold for p in pc[1]), Q5())
        X(f'{k}: stone + setting = the cell exactly (volumes)', G.volume(st) + vg == vD)
        X(f'{k}: gold share of the cell = Table 10.2', vg == SHARE[k] * vD, vg / vD)
        X(f'{k}: every corner of stone and setting inside the cell',
          all(G.dot(n, v) <= c for n, c in PD for v in list(st) + [v for pc in gold for p in pc[1] for v in p.verts]))
        X(f'{k}: piece counts {COUNT[k]}', J.count(gold) == COUNT[k], J.count(gold))
    X('T: the four corner tetrahedra have legs phi (cube edges)', all(sorted(d2(t[0], v) for v in t[1:]) == [PHI * PHI] * 3 for t in map(corner_tet, ODD)))
# ------------------------------------------------------------------ painting (after the Paradigm cover's render)
GROUND = (20, 15, 11); GOLD = (217, 165, 33); TEAL = (40, 165, 150); WHITE = (255, 255, 255)
PINK = (199, 125, 171)                                   # DICTO 11-15: the pink of the Space-Fillers cover (#c77dab)
GOLD_P = np.array([float(x) for x in os.environ.get('GOLDP', '204,152,44').split(',')])   # one gold for every piece of every setting:
# the series' gold (#d4af37) deepened a little, so the yellow octahedron (element colour, fixed) stays distinct from its setting
GOLD_EDGE = np.array([98, 70, 20.])                      # gold edges dark, stone edges light (as Chapter 10's figures, jewels_lib.py)
STONE = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}   # element colours
hexrgb = lambda s: np.array([int(s[i:i + 2], 16) for i in (1, 3, 5)], float)
EDGE = hexrgb('#f0ead8')
W, Hc = 2400, 3394
def rot(a, b, c):
    Rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    Ry = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    Rz = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx
def look(d, up=(0, 0, 1.0)):
    """Orthographic view from direction d (towards the viewer), the given up: rows = screen x, y, z."""
    z = np.array(d, float); z /= np.linalg.norm(z); x = np.cross(up, z)
    if np.linalg.norm(x) < 1e-6: x = np.cross((0, 1.0, 0), z)
    x /= np.linalg.norm(x); y = np.cross(z, x); return np.array([x, y, z])
fl = lambda vs: np.array([[float(x) for x in v] for v in vs])
def pieces(k, M):
    """(faces, rgb, gold?) of jewel k under view M: the stone and the setting pieces whose centre lies behind the cell's centre."""
    st, gold = JEWELS[k]; out = [([(poly, n) for n, poly in J.piece_faces((k, [Part(st)], []))], np.array(STONE[k], float), False)]
    kept = [pc for pc in gold if (M @ np.mean([fl(p.verts).mean(0) for p in pc[1]], 0))[2] <= 0]
    for pc in kept: out.append(([(poly, n) for n, poly in J.piece_faces(pc)], GOLD_P, True))
    return out, len(kept)
def render(PC, M, box, s, SS):
    """Z-buffer painting of the pieces PC under the orthographic view M at the fixed scale s (px per unit, x and y alike), the cell's
    centre at the middle of box. Faces of one piece in one plane share an id (no false creases); gold sits a hair behind a stone
    face it touches. Returns rgb, alpha (box size)."""
    bw, bh = box[2] - box[0], box[3] - box[1]; Wb, Hb = int(bw) * SS, int(bh) * SS
    to_px = lambda V_: np.c_[Wb / 2 + s * SS * (V_ @ M.T)[:, 0], Hb / 2 - s * SS * (V_ @ M.T)[:, 1]]
    zb = np.full((Hb, Wb), -np.inf, np.float32); ib = np.full((Hb, Wb), -1, np.int32); nrm, cols, gid, gfl = [], [], [], []; groups = {}
    for pi, (F, col, isg) in enumerate(PC):
        for pts, nv in F:
            nn = M @ nv
            if nn[2] <= 1e-9: continue
            q = to_px(pts); zz = (pts @ M.T)[:, 2] * s * SS - (0.6 if isg else 0.0)
            x0, x1 = max(0, int(q[:, 0].min())), min(Wb, int(np.ceil(q[:, 0].max())) + 1)
            y0, y1 = max(0, int(q[:, 1].min())), min(Hb, int(np.ceil(q[:, 1].max())) + 1)
            if x1 <= x0 or y1 <= y0: continue
            yy, xx = np.mgrid[y0:y1, x0:x1] + 0.5; inside = np.ones(xx.shape, bool)
            area = np.sum(q[:, 0] * np.roll(q[:, 1], -1) - np.roll(q[:, 0], -1) * q[:, 1]); sg = np.sign(area)
            for a, b in zip(q, np.roll(q, -1, axis=0)):
                inside &= sg * ((b[0] - a[0]) * (yy - a[1]) - (b[1] - a[1]) * (xx - a[0])) >= 0
            z = zz[0] - (nn[0] * (xx - q[0, 0]) - nn[1] * (yy - q[0, 1])) / nn[2]
            sub = zb[y0:y1, x0:x1]; win = inside & (z > sub)
            sub[win] = z[win]; ib[y0:y1, x0:x1][win] = len(nrm)
            key = (pi, tuple(np.round(nv, 6)), round(float(nv @ pts[0]), 6)); gid.append(groups.setdefault(key, len(groups)))
            nrm.append(nn); cols.append(col); gfl.append(isg)
    nrm, cols, gid = np.array(nrm), np.array(cols), np.array(gid)
    fg = ib >= 0; N = np.zeros((Hb, Wb, 3), np.float32); N[fg] = nrm[ib[fg]]; C = np.zeros((Hb, Wb, 3), np.float32); C[fg] = cols[ib[fg]]
    l = np.array([-0.45, 0.62, 0.64]); l /= np.linalg.norm(l)
    diff = np.clip(N @ l, 0, 1); rim = np.clip(N @ (np.array([0.5, -0.6, 0.3]) / np.linalg.norm([0.5, -0.6, 0.3])), 0, 1)
    yy, xx = np.mgrid[0:Hb, 0:Wb].astype(np.float32)
    Lp = np.stack([(-0.15 * Wb - xx), (yy + 0.6 * Hb), np.full_like(xx, 1.2 * max(Wb, Hb))], -1)
    Lp /= np.linalg.norm(Lp, axis=-1, keepdims=True); Hv = Lp + np.array([0, 0, 1], np.float32); Hv /= np.linalg.norm(Hv, axis=-1, keepdims=True)
    spec = np.clip(np.sum(N * Hv, -1), 0, 1) ** 30
    rgb = C * (0.32 + 0.58 * diff)[..., None] + 255 * (0.24 * spec + 0.05 * rim ** 3)[..., None]
    rgb[~fg] = GROUND
    # light edges: boundaries between faces (creases, piece outlines), ~2 px, shaded by depth (near bright, far dimmer)
    G_ = np.where(fg, gid[np.maximum(ib, 0)], -1)
    e = np.zeros((Hb, Wb), bool); e[:, :-1] |= G_[:, :-1] != G_[:, 1:]; e[:-1] |= G_[:-1] != G_[1:]
    zf = zb.copy(); zf[~fg] = -np.inf; zmax = ndimage.maximum_filter(zf, size=3)
    zl, zh = zb[fg].min(), zb[fg].max(); dz = np.clip((zmax - zl) / (zh - zl), 0, 1)
    e = ndimage.binary_dilation(e, iterations=max(1, SS - 1))
    dz = ndimage.maximum_filter(np.where(np.isfinite(dz), dz, 0), size=2 * SS)
    ea = ndimage.gaussian_filter(e.astype(np.float32), SS * 0.35) * (0.45 + 0.47 * dz)
    isg = np.zeros((Hb, Wb), bool); gl = np.array(gfl); isg[fg] = gl[ib[fg]]
    near_stone = ndimage.maximum_filter((fg & ~isg).astype(np.uint8), size=2 * SS + 1) > 0   # a stone's outline stays light
    ecol = np.where(near_stone[..., None], EDGE, GOLD_EDGE)
    rgb = rgb * (1 - ea[..., None]) + ecol * ea[..., None]
    alpha = np.maximum(fg.astype(np.float32), ea)
    rgb = np.clip(rgb, 0, 255).astype(np.uint8); a8 = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    rgb = np.array(Image.fromarray(rgb).resize((int(bw), int(bh)), Image.LANCZOS), float)
    al = np.array(Image.fromarray(a8).resize((int(bw), int(bh)), Image.LANCZOS), float) / 255
    return rgb, np.clip(al, 0, 1)
def put(canvas, rgb, al, x, y):
    h_, w_ = al.shape; c = canvas[y:y + h_, x:x + w_]; canvas[y:y + h_, x:x + w_] = c * (1 - al[..., None]) + rgb * al[..., None]
def caps_of(text):
    """LED word from DICTO's wording: capitals throughout, the letters capital in his text drawn larger (initial caps)."""
    return text.upper(), tuple(i for i, ch in enumerate(text) if ch.isupper() and (i == 0 or text[i - 1] == ' '))
def fit(text, size, col, maxw):
    t, big = caps_of(text)
    while True:
        w_ = L.word(t, size, lambda ch: col, big=big)
        if w_[1].shape[1] <= maxw: return w_, size
        size = int(size * 0.96)
SERIES = 'Book Eight · Wind 風 · The Five Orders of Space'   # front.html's series line, as it stands
TITLE = 'The Platonic Solids'
SUB = 'Inside the Five, Filling Space & Where They Live'   # front.html: "Inside the five, the five filling space, and where the five live"
def title_panel(canvas, top):
    N = W
    ser, s1 = fit(SERIES, int(N * 0.030), WHITE, W - 360)
    t1, s2 = fit(TITLE, int(N * 0.064), GOLD, W - 160)
    sub, s3 = fit(SUB, int(N * 0.0225), TEAL, W - 200)
    by = L.word('* DICTO *', int(N * 0.040), lambda ch: PINK, big=(0, 2, 3, 4, 5, 6, 8))
    print('lettering sizes: series', s1, 'title', s2, 'subtitle', s3, flush=True)
    y = L.paste(canvas, ser, N / 2, top); y = L.paste(canvas, t1, N / 2, y + 60); y = L.paste(canvas, sub, N / 2, y + 75)
    return L.paste(canvas, by, N / 2, y + 85)
VIEW = lambda: look(np.array([float(x) for x in os.environ.get('DIR', '0.62,-0.55,0.56').split(',')]), (0, 0, 1.0)) @ np.eye(3)
ORDER = ['D', 'I', 'C', 'T', 'O']            # DICTO order: top row D I, bottom row C T O (left to right, top to bottom)
def make(SS, out):
    M = rot(0, 0, np.radians(float(os.environ.get('RZ', 0)))) @ VIEW()
    can = np.ones((Hc, W, 3)) * np.array(GROUND, float)
    TOP = 2200
    w = int(os.environ.get('CELL', 740)); g = int(os.environ.get('GAP', 30))      # one jewel's box; all five at one scale
    rD = np.abs(fl(G.DOD) @ M.T)[:, :2].max(); s = (w / 2 - 6) / rD                # the cell's outline fills the box
    sp = w + g; dy = int(np.sqrt(sp ** 2 - (sp / 2) ** 2))                         # top row nested between the bottom row
    hgt = dy + w; y0 = int((TOP - hgt) / 2) + 20
    pos = {'D': (W / 2 - sp / 2, y0), 'I': (W / 2 + sp / 2, y0), 'C': (W / 2 - sp, y0 + dy), 'T': (W / 2, y0 + dy), 'O': (W / 2 + sp, y0 + dy)}
    for k in ORDER:
        PC, nk = pieces(k, M); cx, cy = pos[k]
        rgb, al = render(PC, M, (0, 0, w, w), s, SS)
        put(can, rgb, al, int(cx - w / 2), int(cy)); print(f'jewel {k}: stone + {nk} gold pieces drawn of {len(JEWELS[k][1])}', flush=True)
    assert y0 >= 60 and pos['O'][0] + w / 2 <= W - 40, 'picture outside the block'
    title_panel(can, TOP + 40)
    Image.fromarray(np.clip(can, 0, 255).astype(np.uint8)).save(out)
    print('scale', round(s, 2), 'px/unit (x and y alike); cell box', w, 'px; saved', out, flush=True)
if __name__ == '__main__':
    checks(); print('PROGRESS 0.20 checks', flush=True)
    SS = int(os.environ.get('SS', 3)); out = '../platonic-cover-front-series.png' if os.environ.get('FINAL') == '1' else f'../pilot{os.environ.get("TAG", "")}.png'
    make(SS, out); print('PROGRESS 0.90 cover', flush=True)
    mk = L.word('* DICTO *', int(W * 0.06), lambda ch: PINK, big=(0, 2, 3, 4, 5, 6, 8))   # the back-cover mark, as Space-Fillers
    Image.fromarray(np.dstack([np.clip(mk[0], 0, 255), mk[1] * 255]).astype(np.uint8), 'RGBA').save('../platonic-dicto-mark-back.png')
    ok = Image.open(out).size == (W, Hc) and not FAIL
    print('FINAL ok' if ok else 'FINAL FAIL: ' + '; '.join(FAIL or ['cover missing or wrong size']))
