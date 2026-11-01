# Plates of the DICTO Vacuus: two views side by side per solid (DICTO 2026-11-02: "possibly struts is enough, or both as views").
#   SHEETS: the fins (triangle O-A-B for every edge AB), solid, coloured by congruence class, crisp dark outlines; translucent ghost of
#           the solid (faces tinted, edges grey).
#   STRUTS: the frame: one rod from the centre O to every corner (the lines where fins meet), coloured by length class, nodes as balls;
#           the solid's own edges as thin rods (the fins' outer edges), translucent ghost faces.
# Own z-buffer rasteriser (numpy), orthographic, 3x supersampled then downsampled: hidden surfaces correct, edges >= 2 px at the final
# size (render standard: solid, crisp >= 1.5 px edges). Usage: render.py <shapes dir> <out dir> <logo png> <slug> [<slug> ...]
import sys, os, json, math, numpy as np
from PIL import Image
SH, OUT, LOGO = sys.argv[1:4]; SLUGS = sys.argv[4:]
SS, PX = 3, 1000; N = SS * PX
PAL = ['#d4af37', '#8e5bd6', '#2bb3a3', '#e07b39', '#4a7fd4', '#c94a5a', '#c4a6ee', '#7fbf4d', '#8a8f9c', '#e3c86a', '#5bc0de', '#b36bb3']
def rgb(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float) / 255
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
class Canvas:
    def __init__(s, lim):
        s.lim = lim; s.z = np.full((N, N), -np.inf); s.col = np.ones((N, N, 3)); s.id = np.full((N, N), -1, np.int32)
    def scr(s, W): return np.c_[(W[:, 0] / s.lim + 1) * N / 2, (1 - W[:, 1] / s.lim) * N / 2, W[:, 2]]
    def tri(s, W, colr, ident, zoff=0.0):
        P = s.scr(W); x0, y0 = np.floor(P[:, :2].min(0)).astype(int); x1, y1 = np.ceil(P[:, :2].max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, N - 1), min(y1, N - 1)
        if x1 < x0 or y1 < y0: return
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = P
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-12: return
        l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den; l2 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den; l3 = 1 - l1 - l2
        m = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9); Z = l1 * az + l2 * bz + l3 * cz + zoff
        zb = s.z[y0:y1 + 1, x0:x1 + 1]; m &= Z > zb
        zb[m] = Z[m]; s.col[y0:y1 + 1, x0:x1 + 1][m] = colr; s.id[y0:y1 + 1, x0:x1 + 1][m] = ident
    def rod(s, a, b, r, colr, ident):
        """screen-space tube a-b (view coords), radius r (world units): cylinder shading, dark rim, depth with bulge"""
        A, B = s.scr(a[None])[0], s.scr(b[None])[0]; rp = r / s.lim * N / 2
        x0, y0 = np.floor(np.minimum(A[:2], B[:2]) - rp - 2).astype(int); x1, y1 = np.ceil(np.maximum(A[:2], B[:2]) + rp + 2).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, N - 1), min(y1, N - 1)
        if x1 < x0 or y1 < y0: return
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
        d = B[:2] - A[:2]; L2 = d @ d
        t = np.clip(((X - A[0]) * d[0] + (Y - A[1]) * d[1]) / max(L2, 1e-12), 0, 1)
        px, py = A[0] + t * d[0] - X, A[1] + t * d[1] - Y; q = np.sqrt(px * px + py * py) / rp
        m = q <= 1; Z = A[2] + t * (B[2] - A[2]) + np.sqrt(np.clip(1 - q * q, 0, 1)) * r
        zb = s.z[y0:y1 + 1, x0:x1 + 1]; m &= Z > zb
        sh = 0.55 + 0.45 * np.sqrt(np.clip(1 - q * q, 0, 1)); C = colr[None, None, :] * sh[..., None]
        C[q > 0.78] = np.array([0.11, 0.11, 0.14])
        zb[m] = Z[m]; s.col[y0:y1 + 1, x0:x1 + 1][m] = C[m]; s.id[y0:y1 + 1, x0:x1 + 1][m] = ident
    def ball(s, c, r, colr, ident): s.rod(c, c + 1e-9, r, colr, ident)
    def outlines(s, w=2 * SS):
        """dark lines where the id changes (fin boundaries, silhouettes), w subpixels wide"""
        I = s.id; e = np.zeros_like(I, bool)
        e[:, 1:] |= I[:, 1:] != I[:, :-1]; e[1:, :] |= I[1:, :] != I[:-1, :]
        e &= True; k = w // 2; E = e.copy()
        for dx in range(-k, k + 1):
            for dy in range(-k, k + 1):
                if dx * dx + dy * dy <= k * k: E |= np.roll(np.roll(e, dx, 0), dy, 1)
        s.col[E] = np.array([0.11, 0.11, 0.14])
    def ghost(s, W, F, NF, alpha=0.10):
        """translucent faces of the solid over the image where in front of the opaque content"""
        tint = np.array([0.62, 0.68, 0.80]); acc = np.zeros((N, N))
        for f, n in zip(F, NF):
            for k in range(1, len(f) - 1):
                Q = s.scr(W[[f[0], f[k], f[k + 1]]]); x0, y0 = np.floor(Q[:, :2].min(0)).astype(int); x1, y1 = np.ceil(Q[:, :2].max(0)).astype(int)
                x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, N - 1), min(y1, N - 1)
                if x1 < x0 or y1 < y0: continue
                X, Y = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
                (ax, ay, az), (bx, by, bz), (cx, cy, cz) = Q; den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
                if abs(den) < 1e-12: continue
                l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den; l2 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den; l3 = 1 - l1 - l2
                m = (l1 >= 0) & (l2 >= 0) & (l3 >= 0); Z = l1 * az + l2 * bz + l3 * cz
                m &= Z > s.z[y0:y1 + 1, x0:x1 + 1] - 1e-9
                acc[y0:y1 + 1, x0:x1 + 1][m] += 1
        a = 1 - (1 - alpha) ** acc; s.col = s.col * (1 - a[..., None]) + tint * a[..., None]
    def ghost_edges(s, W, edges, r):
        for a, b in edges:
            A, B = s.scr(W[[a, b]]); n = int(np.linalg.norm(B[:2] - A[:2]) / 0.7) + 2; rp = r / s.lim * N / 2
            T = np.linspace(0, 1, n); Pt = A[None] + T[:, None] * (B - A)[None]
            for x, y, z in Pt:
                xi, yi = int(x), int(y); k = int(math.ceil(rp))
                ys, xs = slice(max(yi - k, 0), min(yi + k + 1, N)), slice(max(xi - k, 0), min(xi + k + 1, N))
                front = s.z[ys, xs] <= z + 1e-9
                s.col[ys, xs][front] = s.col[ys, xs][front] * 0.35 + np.array([0.30, 0.34, 0.44]) * 0.65
    def image(s):
        im = (np.clip(s.col, 0, 1) * 255).astype(np.uint8)
        return Image.fromarray(im).resize((PX, PX), Image.LANCZOS)
def shade(c, n):
    n = n / np.linalg.norm(n); return c * (0.48 + 0.52 * abs(n @ LIGHT)) + 0.04
def plate(slug, view=(20, 24)):
    r = json.load(open(os.path.join(SH, slug + '.json'))); V = np.array(r['points']); F = r['faces']; M = rot(*view); W = V @ M.T
    lim = 1.06 * np.sqrt(r['R2']); fins = r['fin_list']
    # congruence class index per fin
    keys = {}; cls = []
    for c in r['classes']: keys.setdefault((round(c['OA2'], 8), round(c['OB2'], 8), round(c['AB2'], 8)), len(keys))
    for f in fins:
        k = (round(f['OA2'] / r['R2'], 8), round(f['OB2'] / r['R2'], 8), round(f['AB2'] / r['R2'], 8))
        cls.append(keys.setdefault(k, len(keys)))
    NF = []
    for f in F:
        n = np.zeros(3)
        for k in range(len(f)): n += np.cross(W[f[k]], W[f[(k + 1) % len(f)]])
        NF.append(n)
    edges = [f['edge'] for f in fins]
    # SHEETS
    A = Canvas(lim); O = np.zeros(3)
    for i, f in enumerate(fins):
        a, b = f['edge']; T = np.array([O, W[a], W[b]]); n = np.cross(T[1], T[2])
        A.tri(T, shade(rgb(PAL[cls[i] % len(PAL)]), n), i)
    A.outlines(); A.ghost(W, F, NF, 0.10)
    # STRUTS
    B = Canvas(lim); R = math.sqrt(r['R2']); rr = R * min(0.022, max(0.007, 0.075 / math.sqrt(len(V))))
    sk = {}; scl = [sk.setdefault(round(float(p @ p) / r['R2'], 8), len(sk)) for p in V]
    order = sorted(sk, reverse=True); scl = [order.index(round(float(p @ p) / r['R2'], 8)) for p in V]
    for i in range(len(V)): B.rod(O, W[i], rr, rgb(PAL[scl[i] % len(PAL)]), i)
    for j, (a, b) in enumerate(edges): B.rod(W[a], W[b], rr * 0.55, np.array([0.72, 0.74, 0.80]), len(V) + j)
    for i in range(len(V)): B.ball(W[i], rr * 1.5, np.array([0.85, 0.85, 0.88]), len(V) + len(edges) + i)
    B.ball(O, rr * 2.2, np.array([0.20, 0.20, 0.25]), 10 ** 6)
    B.ghost(W, F, NF, 0.07)
    im = Image.new('RGB', (2 * PX + 40, PX), 'white'); im.paste(A.image(), (0, 0)); im.paste(B.image(), (PX + 40, 0))
    lg = Image.open(LOGO).convert('RGBA'); h = 70; lg = lg.resize((int(lg.width * h / lg.height), h)); im.paste(lg, (im.width - lg.width - 8, im.height - h - 8), lg)
    im.save(os.path.join(OUT, slug.replace('.json', '') + '.png'), dpi=(300, 300))
    print(slug, 'fin classes', len(keys), 'strut classes', len(sk), flush=True)
    return dict(slug=slug, fin_colours=[PAL[i % len(PAL)] for i in range(len(keys))], strut_colours=[PAL[i % len(PAL)] for i in range(len(sk))])
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for s in SLUGS:
        info = plate(s); json.dump(info, open(os.path.join(OUT, s + '.colours.json'), 'w'))
