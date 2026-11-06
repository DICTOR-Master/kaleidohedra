"""Classical (Kepler-like) renderer for nested solids (DICTO 11-06: "more classical, more 3D feeling, more Kepleresque rather than 80s
album covers"). Parchment ground with a soft vignette; perspective; each solid shaded by a soft light; outer shells as tinted glass
(back faces first, then inner solids, then front faces), fine dark engraved edges, a faint drop shadow. Painter order for nested convex
shells: all back faces outer -> inner, the innermost solid, then front faces inner -> outer."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.spatial import ConvexHull
PARCH = np.array([241, 232, 210]); INK = (58, 44, 30)
def ground(W, H):
    y, x = np.mgrid[0:H, 0:W]; r = np.hypot((x - W / 2) / W, (y - H / 2) / H)
    tone = 1 - 0.18 * np.clip(r * 1.6, 0, 1) ** 2
    rng = np.random.default_rng(3); noise = rng.normal(0, 3, (H, W, 1))
    img = np.clip(PARCH * tone[..., None] + noise, 0, 255).astype(np.uint8); return Image.fromarray(img).convert('RGBA')
def faces(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 6)), set()).update(sp)
    out = []
    for k, idx in F.items():
        idx = list(idx); n = np.array(k[:3]); c = V[idx].mean(0); u = V[idx[0]] - c; w = np.cross(n, u)
        out.append((n, sorted(idx, key=lambda i: math.atan2((V[i] - c) @ w, (V[i] - c) @ u))))
    return out
def render(solids, out, R, W=2400, H=2400, dist=9.0, scale=None, light=(-0.45, 0.55, 0.70), shadow=True, cut=None):
    """solids: list of (vertices, rgb, alpha) from OUTER to INNER (alpha 1 = opaque). R: 3x3 view rotation."""
    L = np.array(light) / np.linalg.norm(light); eye = np.array([0, 0, dist])
    allV = np.vstack([x[0] for x in solids]) @ R.T
    def proj(P):
        z = dist - P[:, 2]; return P[:, :2] / z[:, None] * dist
    pp = proj(allV); s = scale or 0.80 * min(W, H) / np.ptp(pp, axis=0).max(); c0 = (pp.max(0) + pp.min(0)) / 2
    def to_px(P): q = (proj(P) - c0) * s; return [(W / 2 + x, H / 2 - y) for x, y in q]
    base = ground(W, H)
    if shadow:   # soft shadow of the outer solid on the ground
        sh = Image.new('L', (W, H), 0); d = ImageDraw.Draw(sh)
        V0 = np.array(solids[0][0]) @ R.T; hull = ConvexHull(proj(V0)); pts = to_px(V0[hull.vertices])
        pts = [(x + 0.04 * W, y + 0.05 * H) for x, y in pts]; d.polygon(pts, fill=70)
        sh = sh.filter(ImageFilter.GaussianBlur(W / 60)); dark = Image.new('RGBA', (W, H), (60, 40, 20, 255)); base = Image.composite(dark, base, sh)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    def draw_faces(V, rgb, alpha, which, cutaway=False, thr=0.25):
        nonlocal layer
        Vr = V @ R.T; ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        fs = faces(Vr)
        fs = sorted(fs, key=lambda f: Vr[f[1]][:, 2].mean())
        for n, idx in fs:
            cen = Vr[idx].mean(0); facing = (eye - cen) @ n > 0
            if (which == 'back' and facing) or (which == 'front' and not facing): continue
            if cutaway and cut is not None and which == 'front' and (cen @ cut[0]) > thr * np.linalg.norm(cen): continue
            b = 0.62 + 0.42 * max(0.0, n @ L) if facing else 0.72 + 0.20 * max(0.0, -n @ L)
            col = tuple(int(min(255, c * b)) for c in rgb)
            a = int(255 * (alpha if facing else min(1.0, alpha * 0.8)))
            d.polygon(to_px(Vr[idx]), fill=col + (a,))
            d.line(to_px(Vr[idx]) + [to_px(Vr[idx])[0]], fill=INK + (int(230 if facing else 110),), width=max(2, W // 700))
        layer = Image.alpha_composite(layer, ov)
    solids = [(x[0], x[1], x[2], (x[3] if len(x) > 3 else True)) for x in solids]
    for V, rgb, a, _ in solids[:-1]: draw_faces(V, rgb, a, 'back')
    V, rgb, a, _ = solids[-1]; draw_faces(V, rgb, 1.0, 'back'); draw_faces(V, rgb, 1.0, 'front')
    k = len(solids) - 1
    for j, (V, rgb, a, iscut) in reversed(list(enumerate(solids[:-1]))):
        thr = cut[1] + (cut[2] if cut is not None and len(cut) > 2 else 0.12) * j if cut is not None else 0
        draw_faces(V, rgb, a, 'front', cutaway=iscut, thr=thr)
    img = Image.alpha_composite(base, layer).convert('RGB')
    img.resize((W // 2, H // 2), Image.LANCZOS).save(out)
def view(ax_deg=-62, az_deg=28):
    a, b = math.radians(ax_deg), math.radians(az_deg)
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Rz = np.array([[math.cos(b), -math.sin(b), 0], [math.sin(b), math.cos(b), 0], [0, 0, 1]])
    return Rx @ Rz
