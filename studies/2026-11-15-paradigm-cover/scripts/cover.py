# Front cover of "The Permutohedron Paradigm", exploded version (DICTO 11-15: "a different coloured version of the explodable one ...
# maybe exploded on the cover"). The 4D permutohedron (120 corners = the orderings of 1..5; 30 cells: 10 truncated octahedra = 3D
# permutohedra, 20 hexagonal prisms) in the Schlegel view of paper #105 Figure 1 and the app's perm4 world (eye at 1.18 x the outer
# cell's distance beyond its centre, every corner projected onto that cell's 3-space, radius 1), with the 29 inner cells pulled apart
# from the centre (each cell moved by its centre x PULL, as the app's "Pull apart" slider, here further) and the outer cell as a cage.
# Permutohedra gold, hexagonal prisms pink, on the series ground. Layout, lettering and painting (z-buffer, glossy light, light
# crease edges) copied from the Space-Fillers cover script (studies/2026-11-07-space-fillers-cover/scripts/cover.py); edges here
# shaded by depth. LED lettering: DSEG14 by keshikan (SIL Open Font Licence, DSEG-LICENSE.txt).
# Run from this folder: python cover.py [view ...]  -> ../paradigm-cover-front-exploded[-view].png and ../paradigm-dicto-mark-back.png
import os, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
from PIL import Image
import ledtext as L
# ------------------------------------------------------------------ geometry (exact: orderings of 1..5, a fixed orthonormal frame)
P = np.array(list(itertools.permutations(range(1, 6))), float); NV = len(P)
HB = np.array([[1, -1, 0, 0, 0], [1, 1, -2, 0, 0], [1, 1, 1, -3, 0], [1, 1, 1, 1, -4]], float)   # Helmert frame of x1 + ... + x5 = 0
HB /= np.linalg.norm(HB, axis=1, keepdims=True)
X = (P - 3.0) @ HB.T
assert np.allclose(HB @ HB.T, np.eye(4))
CELLS = []
for k in range(1, 5):
    for S in itertools.combinations(range(5), k):   # the corners whose coordinates on S are the |S| smallest values
        V = [v for v in range(NV) if set(P[v, list(S)].astype(int)) == set(range(1, k + 1))]
        CELLS.append({'S': S, 'kind': 'TO' if k in (1, 4) else 'HP', 'V': V})
assert len(CELLS) == 30 and sum(c['kind'] == 'TO' for c in CELLS) == 10
assert all(len(c['V']) == (24 if c['kind'] == 'TO' else 12) for c in CELLS)
assert all(sum(v in c['V'] for c in CELLS) == 4 for v in range(NV))   # simple: every corner in 4 cells
OUTER = 0                                       # the cell S = {1}: the 3D permutohedron the eye looks through (as the app: first TO)
EYE = 1.18
dot = np.dot
n0 = X[CELLS[OUTER]['V']].mean(0); hf = np.linalg.norm(n0); nh = n0 / hf; eye = nh * hf * EYE
def across(n):                                  # orthonormal basis of the 3-space across n (Gram-Schmidt from the axes, as the app)
    B = []
    for e in np.eye(4):
        v = e - dot(e, n) * n
        for b in B: v = v - dot(v, b) * b
        if np.linalg.norm(v) > 1e-6 and len(B) < 3: B.append(v / np.linalg.norm(v))
    return np.array(B)
BAS = across(nh)
def schlegel(x):
    dx = x - eye; t = (hf - dot(eye, nh)) / dot(dx, nh); return BAS @ (eye + t * dx)
S3 = np.array([schlegel(x) for x in X]); S3 /= np.linalg.norm(S3, axis=1).max()   # radius 1
def faces_of(pts):
    """Convex polytope pts (3D): its faces as ordered corner arrays with outward unit normals (coplanar hull triangles merged)."""
    h = ConvexHull(pts); F = {}
    for simp, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    out = []
    for key, idx in F.items():
        idx = list(idx); q = pts[idx]; nrm = np.array(key[:3]); c = q.mean(0); e1 = q[0] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
        out.append((q[np.argsort(np.arctan2((q - c) @ e2, (q - c) @ e1))], nrm))
    return out
GOLD_TO = np.array([212, 175, 55.])           # the series' gold (#d4af37, the gold pieces of the Space-Fillers cover)
PINK = (199, 125, 171)                        # DICTO 11-15: the pink of the Space-Fillers cover (#c77dab)
PINK_HP = np.array(PINK, float)
def pieces(pull):
    """The 29 inner cells, each moved out by its centre x pull: (faces, rgb, cell index). Checks the face counts."""
    out = []
    for ci, c in enumerate(CELLS):
        if ci == OUTER: continue
        q = S3[c['V']]; F = faces_of(q)
        assert len(F) == (14 if c['kind'] == 'TO' else 8), (ci, len(F))
        sh = q.mean(0) * pull
        out.append(([(f + sh, n) for f, n in F], GOLD_TO if c['kind'] == 'TO' else PINK_HP, ci))
    return out
def min_gap(pull):
    """Smallest gap opened between neighbouring cells: for each shared face (>= 3 common corners), the distance its two copies moved apart."""
    g = np.inf; cen = [S3[c['V']].mean(0) for c in CELLS]
    for a, b in itertools.combinations(range(1, 30), 2):
        if len(set(CELLS[a]['V']) & set(CELLS[b]['V'])) >= 3: g = min(g, np.linalg.norm((cen[a] - cen[b]) * pull))
    return g
# ------------------------------------------------------------------ painting (after the Space-Fillers cover's render)
GROUND = (20, 15, 11); GOLD = (217, 165, 33); TEAL = (40, 165, 150)
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
def render(PC, M, box, SS, cage=None):
    """Z-buffer painting of the pieces PC under the orthographic view M (one scale for x and y: no stretching), fitted to box;
    cage = list of 3D segments drawn as thin gold lines, depth-tested against the solids. Returns rgb, alpha (box size), scale."""
    allv = np.vstack([f[0] for F, _, _ in PC for f in F] + ([np.array(cage).reshape(-1, 3)] if cage is not None else [])) @ M.T
    lo, hi = allv.min(0), allv.max(0); bw, bh = box[2] - box[0], box[3] - box[1]
    s = min(bw / (hi[0] - lo[0]), bh / (hi[1] - lo[1])); ox = box[0] + (bw - s * (hi[0] - lo[0])) / 2; oy = box[1] + (bh - s * (hi[1] - lo[1])) / 2
    to_px = lambda V: np.c_[ox + s * ((V @ M.T)[:, 0] - lo[0]), oy + s * (hi[1] - (V @ M.T)[:, 1])]
    Wb, Hb = int(bw) * SS, int(bh) * SS
    zb = np.full((Hb, Wb), -np.inf, np.float32); ib = np.full((Hb, Wb), -1, np.int32); nrm, cols = [], []
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
            z = zz[0] - (nn[0] * (xx - q[0, 0]) - nn[1] * (yy - q[0, 1])) / nn[2]
            sub = zb[y0:y1, x0:x1]; win = inside & (z > sub)
            sub[win] = z[win]; ib[y0:y1, x0:x1][win] = len(nrm)
            nrm.append(nn); cols.append(col)
    nrm, cols = np.array(nrm), np.array(cols)
    fg = ib >= 0; N = np.zeros((Hb, Wb, 3), np.float32); N[fg] = nrm[ib[fg]]; C = np.zeros((Hb, Wb, 3), np.float32); C[fg] = cols[ib[fg]]
    l = np.array([-0.45, 0.62, 0.64]); l /= np.linalg.norm(l)
    diff = np.clip(N @ l, 0, 1); rim = np.clip(N @ (np.array([0.5, -0.6, 0.3]) / np.linalg.norm([0.5, -0.6, 0.3])), 0, 1)
    yy, xx = np.mgrid[0:Hb, 0:Wb].astype(np.float32)
    Lp = np.stack([(-0.15 * Wb - xx), (yy + 0.6 * Hb), np.full_like(xx, 1.2 * max(Wb, Hb))], -1)
    Lp /= np.linalg.norm(Lp, axis=-1, keepdims=True); Hv = Lp + np.array([0, 0, 1], np.float32); Hv /= np.linalg.norm(Hv, axis=-1, keepdims=True)
    spec = np.clip(np.sum(N * Hv, -1), 0, 1) ** 30
    rgb = C * (0.32 + 0.58 * diff)[..., None] + 255 * (0.24 * spec + 0.05 * rim ** 3)[..., None]
    rgb[~fg] = GROUND
    # light edges: boundaries of the face buffer (creases, cell outlines), ~2 px, shaded by depth (near bright, far dimmer)
    e = np.zeros((Hb, Wb), bool); e[:, :-1] |= ib[:, :-1] != ib[:, 1:]; e[:-1] |= ib[:-1] != ib[1:]
    zf = zb.copy(); zf[~fg] = -np.inf; zmax = ndimage.maximum_filter(zf, size=3)   # an edge takes the depth of its nearer side
    zl, zh = zb[fg].min(), zb[fg].max(); dz = np.clip((zmax - zl) / (zh - zl), 0, 1)
    e = ndimage.binary_dilation(e, iterations=max(1, SS - 1))
    dz = ndimage.maximum_filter(np.where(np.isfinite(dz), dz, 0), size=2 * SS)
    ea = ndimage.gaussian_filter(e.astype(np.float32), SS * 0.35) * (0.45 + 0.47 * dz)
    rgb = rgb * (1 - ea[..., None]) + EDGE * ea[..., None]
    alpha = np.maximum(fg.astype(np.float32), ea)
    if cage is not None:   # the outer cell's edges: thin gold lines, hidden where a solid is in front, dimmer at the back
        ca = np.zeros((Hb, Wb), np.float32); czl, czh = None, None
        segs = [(to_px(np.array(sg_)) - [box[0], box[1]]) * SS for sg_ in cage]; zs = [(np.array(sg_) @ M.T)[:, 2] * s * SS for sg_ in cage]
        zall = np.concatenate(zs); czl, czh = zall.min(), zall.max()
        for q, zz in zip(segs, zs):
            m = int(np.hypot(*(q[1] - q[0]))) * 2 + 2; t = np.linspace(0, 1, m)
            pts = q[0] + t[:, None] * (q[1] - q[0]); zp = zz[0] + t * (zz[1] - zz[0])
            xi, yi = pts[:, 0].astype(int), pts[:, 1].astype(int); ok = (xi >= 0) & (xi < Wb) & (yi >= 0) & (yi < Hb)
            xi, yi, zp = xi[ok], yi[ok], zp[ok]; vis = zp > zb[yi, xi]
            ca[yi[vis], xi[vis]] = np.maximum(ca[yi[vis], xi[vis]], 0.6 + 0.4 * (zp[vis] - czl) / (czh - czl))
        ca = ndimage.grey_dilation(ca, size=(2 * SS, 2 * SS)); ca = ndimage.gaussian_filter(ca, SS * 0.35)
        rgb = rgb * (1 - ca[..., None]) + np.array(GOLD, float) * ca[..., None]; alpha = np.maximum(alpha, ca)
    rgb = np.clip(rgb, 0, 255).astype(np.uint8); a8 = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    rgb = np.array(Image.fromarray(rgb).resize((int(bw), int(bh)), Image.LANCZOS), float)
    al = np.array(Image.fromarray(a8).resize((int(bw), int(bh)), Image.LANCZOS), float) / 255
    return rgb, np.clip(al, 0, 1), s
def put(canvas, rgb, al, x, y):
    h_, w_ = al.shape; c = canvas[y:y + h_, x:x + w_]; canvas[y:y + h_, x:x + w_] = c * (1 - al[..., None]) + rgb * al[..., None]
def title_panel(canvas, top):
    N = W; sz = int(N * 0.064)
    t1 = L.word('THE PERMUTOHEDRON', sz, lambda ch: GOLD, big=(0, 4))
    t2 = L.word('PARADIGM', sz, lambda ch: GOLD, big=(0,))
    sub = L.word('EVERY POSSIBLE ORDER', int(N * 0.03), lambda ch: TEAL, big=(0, 6, 15))
    by = L.word('* DICTO *', int(N * 0.040), lambda ch: PINK, big=(0, 2, 3, 4, 5, 6, 8))
    assert t1[1].shape[1] < W - 160, ('title too wide', t1[1].shape)
    y = L.paste(canvas, t1, N / 2, top); y = L.paste(canvas, t2, N / 2, y + 40); y = L.paste(canvas, sub, N / 2, y + 75)
    return L.paste(canvas, by, N / 2, y + 85)
PULL = float(os.environ.get('PULL', 2.4))   # the app's slider at full is 0.9; the cover pulls further
VIEWS = {   # orthographic view directions in the Schlegel 3-space (all: the picture's symmetry axes or between)
    'tilt': lambda: rot(np.radians(float(os.environ.get('TA', 24))), 0, 0) @ rot(0, np.radians(float(os.environ.get('TB', 33))), 0) @ look(np.mean([S3[v] for v in CELLS[29 - 0]['V']], 0) + 1e-9 if False else (0, 0, 1.0), (0, 1.0, 0)),
}
def seed_dirs():
    """Directions of the centre cell's face centres (the cell opposite the outer one): hexagons (3-fold) and squares (2-fold)."""
    seed = next(i for i, c in enumerate(CELLS) if c['kind'] == 'TO' and not set(c['S']) & set(CELLS[OUTER]['S']) and len(c['S']) == 4)
    F = faces_of(S3[CELLS[seed]['V']]); return [n for f, n in F if len(f) == 6], [n for f, n in F if len(f) == 4]
def view_matrix(name):
    hexn, sqn = seed_dirs()
    if name == 'hex': return look(hexn[0], up=sqn[0] - (sqn[0] @ hexn[0]) * hexn[0])
    if name == 'sq': return look(sqn[0], up=hexn[0] - (hexn[0] @ sqn[0]) * sqn[0])
    if name == 'vert':   # along a corner of the centre cell (where two hexagons and a square meet): between the ring cells
        seed = next(i for i, c in enumerate(CELLS) if c['kind'] == 'TO' and not set(c['S']) & set(CELLS[OUTER]['S']) and len(c['S']) == 4)
        d = S3[CELLS[seed]['V'][int(os.environ.get('VI', 0))]] - S3[CELLS[seed]['V']].mean(0); d /= np.linalg.norm(d)
        u = sqn[0] - (sqn[0] @ d) * d
        return rot(np.radians(float(os.environ.get('TA', 0))), np.radians(float(os.environ.get('TB', 0))), np.radians(float(os.environ.get('RZ', 0)))) @ look(d, up=u)
    if name == 'tilt':   # the hexagon view (3-fold axis), tipped so the cells behind the centre come out from behind it
        return rot(np.radians(float(os.environ.get('TA', 22))), np.radians(float(os.environ.get('TB', 14))), 0) @ view_matrix('hex')
    if name == 'oblique':   # between a hexagon and a square direction, turned a little: no cell hides behind another
        d = hexn[0] * float(os.environ.get('WH', 1.0)) + sqn[0] * float(os.environ.get('WS', 0.45)); d /= np.linalg.norm(d)
        up = sqn[0] - (sqn[0] @ d) * d; return rot(0, 0, np.radians(float(os.environ.get('RZ', 0)))) @ look(d, up=up)
    raise KeyError(name)
def make(view, SS, out):
    M = view_matrix(view); PC = pieces(PULL)
    cage = None
    if os.environ.get('CAGE', '1') == '1':   # the outer cell, scaled to wrap the pulled-apart cells (as it wraps them closed)
        h0 = ConvexHull(S3[CELLS[OUTER]['V']]); allp = np.vstack([f for F_, _, _ in PC for f, _ in F_])
        fac = max(1.0, np.max((allp @ h0.equations[:, :3].T) / -h0.equations[:, 3])) * 1.04   # just wraps every pulled cell
        q = S3[CELLS[OUTER]['V']] * fac; F = faces_of(q); segs = {}
        for f, n in F:
            for a, b in zip(f, np.roll(f, -1, axis=0)): segs.setdefault(tuple(sorted((tuple(np.round(a, 9)), tuple(np.round(b, 9))))), []).append((M @ n)[2])
        assert len(segs) == 36 and all(len(v) == 2 for v in segs.values()), len(segs)
        # only its outline and back edges: the shell stands behind the cells as a frame, never across them
        cage = [np.array(sg_) for sg_, nz in segs.items() if min(nz) < 0]
    can = np.ones((Hc, W, 3)) * np.array(GROUND, float)
    TOP = 2200
    bx0, bx1, bh = 180, W - 180, 2060
    rgb, al, s = render(PC, M, (bx0, 0, bx1, bh), SS, cage)
    ys, xs_ = np.where(al > 0.01); y0, y1 = ys.min(), ys.max() + 1; rgb, al = rgb[y0:y1], al[y0:y1]
    top = int((TOP - (y1 - y0)) / 2) + 30; assert top >= 60, ('picture too tall', top)
    put(can, rgb, al, bx0, top)
    title_panel(can, TOP + 40)
    Image.fromarray(np.clip(can, 0, 255).astype(np.uint8)).save(out)
    print(view, 'pull', PULL, 'cells', len(PC), 'picture', int(np.ptp(xs_)) + 1, 'x', y1 - y0, 'px; scale', round(s, 2), 'px/unit (x and y alike)',
          '; smallest gap between neighbours', round(min_gap(PULL) * s, 1), 'px', '; saved', out, flush=True)
if __name__ == '__main__':
    args = sys.argv[1:] or ['vert']; SS = int(os.environ.get('SS', 3))
    print('corners', NV, 'cells', len(CELLS), '(TO', sum(c['kind'] == 'TO' for c in CELLS), ', HP', sum(c['kind'] == 'HP' for c in CELLS), ')', flush=True)
    outs = []
    for i, v in enumerate(args):
        out = '../paradigm-cover-front-exploded.png' if len(args) == 1 and os.environ.get('FINAL') == '1' else f'../pilot-{v}-p{PULL}{os.environ.get("TAG", "")}.png'
        make(v, SS, out); outs.append(out); print(f'PROGRESS {(i + 1) / len(args):.2f} {v}', flush=True)
    mk = L.word('* DICTO *', int(W * 0.06), lambda ch: PINK, big=(0, 2, 3, 4, 5, 6, 8))   # the back-cover mark, as Space-Fillers
    Image.fromarray(np.dstack([np.clip(mk[0], 0, 255), mk[1] * 255]).astype(np.uint8), 'RGBA').save('../paradigm-dicto-mark-back.png')
    ok = all(Image.open(o).size == (W, Hc) for o in outs)
    print('FINAL ok' if ok else 'FINAL FAIL (cover missing or wrong size)')
