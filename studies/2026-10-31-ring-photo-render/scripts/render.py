# Step 2 of DICTO's "photo-real ring renders" test (2026-10-31): paste the photo cut-outs of his real PET-bottle-cap security
# rings (cutout.py) onto the exact ring triangles of (a) one big triangle (4 rings, flat, top view), (b) a regular tetrahedron
# of 16 rings (edge = 2 ring sides, each face = 4 rings), (c) the HexOct h-tile at lambda = -1/8 (48 rings, exact faces of
# studies/2026-10-31-hexoct-ring-build).
#   placement = affine map of the cut-out's three rounded tips onto points at 0.72 of the model triangle's circumradius;
#               then every pixel is shifted radially so the photographed outline (rounder: the loose rings bulge) becomes
#               45 % of the way to the model's rounded triangle (as the six ties pull a ring flatter), band width kept
#   band      = conical sheet (DICTO): a top-view photo of a conical band shows the wide rim as the outer outline and the
#               narrow rim at the inner edge of the white. So every cut-out pixel gets a height from its distance d to the
#               outer outline: d = 0 -> wide rim, d >= apparent band width -> narrow rim; the two rims sit at +-h/2 along the
#               face normal. The cut-out is a height field, rendered as dense points with a z-buffer (supersampled).
#   flip      = DICTO: the central ring of every 4-ring face is turned over so the slopes cancel. Taken here: corner rings
#               lie wide rim up in the photo, central rings narrow rim up; in the model the photographed side faces out, so
#               corner rings have the wide rim outside, central rings the narrow rim outside. Central positions use central
#               cut-outs, corners corner cut-outs. From inside (through the open centres) a ring shows its other side, so a
#               back-facing corner ring is drawn with a central cut-out and vice versa (mirrored).
#               h-tile faces: the two orientations of ring triangles on a face's grid alternate across every tied side; the
#               minority orientation counts as 'central' (the 4-ring rule extended).
#   shading   = face normal against one light (darker when turned away; faces seen from inside dimmer)
#   ties      = zip-tie patches cut from the photo, folded over the shared side at 0.32 and 0.68 (half on each ring), on top
#   shadow    = all points projected to the ground along the light, blurred twice (contact + soft), plain light ground
# Usage (dicto-big-brother): CUTDIR=~/kres-tmp/ringphoto/derived OUTDIR=~/kres-tmp/ringphoto/derived \
#   TILES_DIR=~/kres-tmp/endless RINGBUILD=~/k-research/studies/2026-10-31-hexoct-ring-build/scripts \
#   ~/geom/bin/python render.py [flat] [tetra] [htile]
import os, sys, json, math
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

CUT = os.path.expanduser(os.environ['CUTDIR']); OUT = os.path.expanduser(os.environ['OUTDIR'])
meta = json.load(open(os.path.join(CUT, 'cutouts.json')))
SIDE = 0.5                                   # ring side in lattice units (double scale: unit triangle = 4 rings)
H_BAND = float(os.environ.get('H_BAND', 0.13)) * SIDE     # band height (assumed 0.13 side, ~4 mm on a ~30 mm side; a top view cannot measure it)
SS = 2                                       # supersampling
GOOD_CORNER = [0, 2, 3, 4, 7, 8, 10, 11]     # cleanest corner-ring cut-outs (5 keeps tatami fringe)
GOOD_CENTRAL = [1, 9]                        # 6 has tatami inside its band
CENTRAL = {m['file'] for m in meta['rings'] if m['central']}
LIGHT = np.array([-0.35, -0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
RM = meta['rings']

def load(f, clean=False):
    a = np.asarray(Image.open(os.path.join(CUT, f)).convert('RGBA')).astype(np.float32) / 255
    if clean:   # kill tatami threads left at the band edge: beige (S > 0.09) and not bright (V < 0.75), then open
        rgb = a[..., :3]; V = rgb.max(-1); S = (V - rgb.min(-1)) / np.maximum(V, 1e-3)
        a[..., 3] *= 1 - np.clip((S - 0.09) / 0.04, 0, 1) * np.clip((0.75 - V) / 0.1, 0, 1)
        yy, xx = np.mgrid[-2:3, -2:3]; keep = ndi.binary_opening(a[..., 3] > 0.5, (yy ** 2 + xx ** 2) <= 5)
        lab, n = ndi.label(keep); keep = lab == 1 + np.argmax(ndi.sum(keep, lab, range(1, n + 1)))
        a[..., 3] = ndi.binary_erosion(keep).astype(np.float32)
    return a

G0 = 0.72          # tips of a cut-out <-> points at 0.72 of the model triangle's circumradius
K_ROUND, INSET = 0.24, 0.012   # corner rounding and inset of the target outline (rounder than mockup.py's 0.16, 0.035)
TIE_AT = 0.32      # ties drawn at 0.32 / 0.68 of a side (built at 1/4, 3/4; there the drawn rings, still partly round,
                   # bow away from the side and a tie would float)
PULL = 0.45        # fraction of the way from the photographed outline to the target (tied rings stay partly round)

def radius_fn(xy, c, nb=720):
    """max radius per angle bin of a point set about c (star-shaped outline), gaps filled, lightly smoothed"""
    d = xy - c; ang = (np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360 * nb / 360).astype(int) % nb
    r = np.zeros(nb); np.maximum.at(r, ang, np.hypot(d[:, 0], d[:, 1]))
    good = r > 0; idx = np.arange(nb)
    r = np.interp(idx, idx[good], r[good], period=nb)
    return ndi.uniform_filter1d(r, 41, mode='wrap')

def target_outline(tips):
    """the model's rounded triangle in texture pixels: sharp triangle c + (tip - c)/G0, inset, corners rounded (K_ROUND)"""
    c = tips.mean(0); V = [c + (t - c) / G0 for t in tips]; a = np.linalg.norm(V[1] - V[0]); r_in = a / (2 * 3 ** .5)
    V = [c + (v - c) * (1 - INSET * a / r_in) for v in V]; pts = []
    for n in range(3):
        A, B, C = V[n - 1], V[n], V[(n + 1) % 3]; p1 = B + (A - B) * K_ROUND; p2 = B + (C - B) * K_ROUND
        if pts: pts += list(np.linspace(pts[-1], p1, 60))[1:]
        for t in np.linspace(0, 1, 40): pts.append((1 - t) ** 2 * p1 + 2 * (1 - t) * t * B + t * t * p2)
    pts += list(np.linspace(pts[-1], pts[0], 60))[1:]
    return np.array(pts)

def points_of(a, U, width=None, tips=None):
    """upsample a cut-out by U and return (tex x, tex y, rgb, height fraction f) of its opaque samples. With tips: each
    sample is shifted radially by (target outline radius - photo outline radius) at its angle, so the photographed ring
    takes the model's rounded-triangle shape (as the ties pull it) while its band width is kept."""
    h, w = a.shape[:2]
    ys, xs = np.mgrid[0:h * U, 0:w * U]; tx = (xs + 0.5) / U - 0.5; ty = (ys + 0.5) / U - 0.5
    al = ndi.map_coordinates(a[..., 3], [ty, tx], order=1) > 0.5
    tx, ty = tx[al], ty[al]
    rgb = np.stack([ndi.map_coordinates(a[..., k], [ty, tx], order=1) for k in range(3)], -1)
    if width is None: return tx, ty, rgb, None
    solid = ndi.binary_fill_holes(a[..., 3] > 0.5); d = ndi.distance_transform_edt(solid)
    f = np.clip(ndi.map_coordinates(d, [ty, tx], order=1) / width, 0, 1)
    if tips is not None:
        c = tips.mean(0); yy, xx = np.nonzero(solid)
        r_ph = radius_fn(np.c_[xx, yy].astype(float), c); r_tg = radius_fn(target_outline(tips), c)
        nb = len(r_ph); dx, dy = tx - c[0], ty - c[1]; rho = np.hypot(dx, dy)
        b = (np.degrees(np.arctan2(dy, dx)) % 360 * nb / 360).astype(int) % nb
        k = (rho + PULL * (r_tg[b] - r_ph[b])) / np.maximum(rho, 1e-6)
        tx, ty = c[0] + dx * k, c[1] + dy * k
    return tx, ty, rgb, f

RAW = {m['file']: load(m['file'], True) for m in RM}
TIES = [load(t['file']) for t in meta['ties']]
_PC = {}
def ring_points(m, U):
    k = (m['file'], U)
    if k not in _PC: _PC[k] = points_of(RAW[m['file']], U, m['width_px'], np.array(m['corners']))
    return _PC[k]
_TC = {}
def tie_points(j, U):
    k = (j, U)
    if k not in _TC: _TC[k] = points_of(TIES[j], U)
    return _TC[k]

class View:
    def __init__(self, elev, azim):
        e, a = math.radians(elev), math.radians(azim)
        self.f = -np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
        self.r = np.cross(self.f, [0, 0, 1.0]); self.r /= np.linalg.norm(self.r); self.u = np.cross(self.r, self.f)
    def setup(self, pts, W, H, pad=0.07):
        P = np.c_[pts @ self.r, pts @ self.u]; lo, hi = P.min(0), P.max(0); self.c = (lo + hi) / 2
        self.s = min(W * (1 - 2 * pad) / (hi[0] - lo[0]), H * (1 - 2 * pad) / (hi[1] - lo[1])) * SS
        self.W, self.H = W * SS, H * SS
    def scr(self, P):
        P = np.atleast_2d(P); return np.c_[(P @ self.r - self.c[0]) * self.s + self.W / 2, self.H / 2 - (P @ self.u - self.c[1]) * self.s]
    def depth(self, P): return np.atleast_2d(P) @ self.f

def tex_to_3d(src, P3):
    """3x3 map: 3D = M @ (x, y, 1), through three correspondences"""
    return np.linalg.solve(np.c_[src, np.ones(3)], np.array(P3)).T

# ---------------- models ----------------
def orient(T, n):
    T = [np.array(p, float) for p in T]
    if np.cross(T[1] - T[0], T[2] - T[0]) @ n > 0: T = [T[0], T[2], T[1]]     # clockwise seen from outside
    return T

def big_triangle(A, B, C, n):
    m = lambda p, q: (p + q) / 2
    ab, bc, ca = m(A, B), m(B, C), m(C, A)
    return [dict(T=orient(t, n), n=n, central=c) for t, c in
            (((A, ab, ca), False), ((ab, B, bc), False), ((ca, bc, C), False), ((ab, bc, ca), True))]

def model_flat():
    A, B, C = np.array([0, 0, 0.]), np.array([1, 0, 0.]), np.array([.5, 3 ** .5 / 2, 0])
    return big_triangle(A, B, C, np.array([0, 0, 1.]))

def model_tetra():
    V = [np.array([0, 0, 0.]), np.array([1, 0, 0.]), np.array([.5, 3 ** .5 / 2, 0]), np.array([.5, 3 ** .5 / 6, (2 / 3) ** .5])]
    cen = np.mean(V, 0); rings = []
    for i, j, k in ((0, 1, 2), (0, 1, 3), (1, 2, 3), (2, 0, 3)):
        n = np.cross(V[j] - V[i], V[k] - V[i]); n /= np.linalg.norm(n)
        if n @ (V[i] - cen) < 0: n = -n
        rings += big_triangle(V[i], V[j], V[k], n)
    return rings

def model_htile():
    sys.path.insert(0, os.path.expanduser(os.environ['TILES_DIR'])); sys.path.insert(0, os.path.expanduser(os.environ['RINGBUILD']))
    import build as B, exactfaces as E
    from tiles import tile
    P = tile('AB', 0, B.LAM)[0]; faces = B.split_edges(E.union_faces([p[3] for p in P])); rings = []
    for f in faces:
        n = B.cnormal(f); Ts = [[B.cart(p) for p in T] for T in B.rings_of(f)]
        c0 = np.mean(Ts[0], 0); u = Ts[0][0] - c0; u /= np.linalg.norm(u)
        cls = [any((p - np.mean(T, 0)) @ u / np.linalg.norm(p - np.mean(T, 0)) > 0.99 for p in T) for T in Ts]
        minority = sum(cls) * 2 < len(cls)
        for T, c in zip(Ts, cls): rings.append(dict(T=orient(T, n), n=n, central=(c == minority)))
    z0 = min(p[2] for r in rings for p in r['T'])
    for r in rings: r['T'] = [p - [0, 0, z0] for p in r['T']]
    return rings

# ---------------- render ----------------
def render(rings, view, W, H, seed=0, name='x'):
    rng = np.random.default_rng(seed)
    allp = np.vstack([np.vstack(r['T']) + r['n'] * s * H_BAND / 2 for r in rings for s in (-1, 1)])
    view.setup(allp, W, H)
    ic = rng.permutation(GOOD_CORNER).tolist(); im = rng.permutation(GOOD_CENTRAL).tolist(); kc = km = 0
    for r in rings:
        if r['central']: r['tex'] = RM[im[km % len(im)]]; km += 1
        else: r['tex'] = RM[ic[kc % len(ic)]]; kc += 1
        r['rot'] = int(rng.integers(3))
        pool = GOOD_CORNER if r['central'] else GOOD_CENTRAL      # its other side looks like the other kind
        r['back'] = RM[pool[int(rng.integers(len(pool)))]]
    P, C = [], []                                  # 3D points, colours
    for r in rings: ring_cloud(r, view, P, C)
    # tie points: 1/4 and 3/4 of every ring side, shared by two rings
    tp = {}
    for idx, r in enumerate(rings):
        T = r['T']
        for k in range(3):
            for s in (TIE_AT, 1 - TIE_AT):
                p = T[k] + (T[(k + 1) % 3] - T[k]) * s; tp.setdefault(tuple(np.round(p, 5)), []).append((idx, T[(k + 1) % 3] - T[k]))
    for j, (p, L) in enumerate(tp.items()):
        if len(L) == 2: tie_cloud(np.array(p), rings[L[0][0]], rings[L[1][0]], L[0][1], j, view, P, C)
    P = np.vstack(P); C = np.vstack(C)
    # z-buffer by sorting: far first, nearest written last
    S = view.scr(P); x = S[:, 0].astype(int); y = S[:, 1].astype(int); d = view.depth(P)
    ok = (x >= 0) & (x < view.W) & (y >= 0) & (y < view.H); o = np.argsort(-d[ok])
    col = np.zeros((view.H, view.W, 3), np.float32); cov = np.zeros((view.H, view.W), np.float32)
    xi, yi = x[ok][o], y[ok][o]; col[yi, xi] = C[ok][o]; cov[yi, xi] = 1
    # close pin-holes left by the splatting (pixels with no sample but covered all around)
    hole = (cov == 0) & (ndi.uniform_filter(cov, 3) > 0.6)
    if hole.any():
        cs = np.stack([ndi.uniform_filter(col[..., k] * cov, 3) for k in range(3)], -1) / np.maximum(ndi.uniform_filter(cov, 3), 1e-6)[..., None]
        col[hole] = cs[hole]; cov[hole] = 1
    # shadow on the ground (z = 0) along the light
    Q = P[::2] - LIGHT[None] * (P[::2, 2:3] / LIGHT[2]); SQ = view.scr(Q)
    qx, qy = SQ[:, 0].astype(int), SQ[:, 1].astype(int); ok = (qx >= 0) & (qx < view.W) & (qy >= 0) & (qy < view.H)
    sh = np.zeros((view.H, view.W), np.float32); sh[qy[ok], qx[ok]] = 1
    sh = ndi.binary_closing(sh > 0, np.ones((3, 3))).astype(np.float32)
    contact = ndi.gaussian_filter(sh, 2.0 * SS); soft = ndi.gaussian_filter(sh, 12 * SS)
    yy = np.linspace(0, 1, view.H)[:, None, None]
    ground = np.array([0.935, 0.928, 0.905])[None, None, :] * (1.02 - 0.06 * yy) * np.ones((1, view.W, 1))
    ground = ground * (1 - 0.28 * contact[..., None] - 0.20 * soft[..., None])
    a = ndi.gaussian_filter(cov, 0.6)[..., None]
    img = col * a + ground * (1 - a)
    out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    out.save(os.path.join(OUT, f'render-{name}.png')); print('saved', name, len(P), 'points', flush=True)
    return out

def anchors(r, g):
    T = r['T']; c = np.mean(T, 0); return [c + (p - c) * g for p in T]

def upsample(view, M, tex_px=1.0):
    """samples per texture pixel so that one texture pixel covers <= 1/1.6 screen pixel"""
    e = np.linalg.norm(M[:, 0]) * view.s; return int(min(8, max(1, math.ceil(e * 1.6))))

def ring_cloud(r, view, P, C):
    front = float(r['n'] @ view.f) < 0
    tm = r['tex'] if front else r['back']
    tips = np.roll(np.array(tm['corners']), r['rot'], 0)
    if not front: tips = tips[[0, 2, 1]]                     # seen from inside: mirrored
    M = tex_to_3d(tips, anchors(r, G0)); U = upsample(view, M)
    tx, ty, rgb, f = ring_points(tm, U)
    n = r['n']; near = (H_BAND / 2) * (1 if front else -1)   # offset (along n) of the rim nearest the viewer
    wide_near = tm['file'] not in CENTRAL                     # corner cut-out: wide rim towards the camera
    z = (near if wide_near else -near) * (1 - 2 * f)          # f = 0 at the wide rim, 1 at the narrow rim
    X = np.c_[tx, ty, np.ones_like(tx)] @ M.T + z[:, None] * n[None]
    nv = n if front else -n; lam = max(0.0, float(nv @ LIGHT))
    shade = (0.66 + 0.42 * lam) if front else (0.50 + 0.22 * lam)
    P.append(X); C.append(np.clip(rgb * shade, 0, 1))

def tie_cloud(p, a, b, e, j, view, P, C):
    tex = TIES[j % len(TIES)]; h, w = tex.shape[:2]
    e = e / np.linalg.norm(e)
    upx = G0 * (SIDE / 3 ** .5) / 99.0 * 0.75               # lattice units per photo pixel (tip radius ~99 px <-> 0.72 R)
    for rr, sgn in ((a, -1), (b, 1)):
        front = float(rr['n'] @ view.f) < 0
        n = rr['n']; off = n * (H_BAND / 2 + 0.006) * (1 if front else -1)
        c = np.mean(rr['T'], 0); u = c - p; u -= (u @ e) * e; u /= np.linalg.norm(u)
        src = np.array([[w / 2, h / 2], [w / 2 + sgn * w / 2, h / 2], [w / 2, 0]])
        dst = [p + off, p + off + u * (w / 2) * upx, p + off + e * (h / 2) * upx]
        M = tex_to_3d(src, dst); U = upsample(view, M)
        tx, ty, rgb, _ = tie_points(j % len(TIES), U)
        half = (tx - w / 2) * sgn >= 0
        X = np.c_[tx[half], ty[half], np.ones(half.sum())] @ M.T
        nv = n if front else -n; lam = max(0.0, float(nv @ LIGHT))
        P.append(X); C.append(np.clip(rgb[half] * ((0.66 + 0.42 * lam) if front else (0.6 + 0.24 * lam)), 0, 1))

if __name__ == '__main__':
    which = sys.argv[1:] or ['flat', 'tetra', 'htile']
    if 'flat' in which: render(model_flat(), View(89.9, -90), 1000, 1000, seed=3, name='flat-top')
    if 'tetra' in which: render(model_tetra(), View(22, -30), 1600, 1300, seed=5, name='tetra')
    if 'htile' in which: render(model_htile(), View(30, -58), 1800, 1350, seed=7, name='htile')
