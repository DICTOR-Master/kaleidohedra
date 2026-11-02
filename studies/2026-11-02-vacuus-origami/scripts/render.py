# Pictures of the DICTO Vacuus as modular origami (DICTO proposed 2026-11-02), from fan.py's JSON.
# Left: assembled. Every face's open pyramid is a fan of paper triangles O-v_k-v_(k+1); each triangle is moved off its fin plane by a
# small gap delta towards the inside of its own pyramid, so every fin shows as a DOUBLE WALL (two sheets, back to back) and the two
# sheets show as two lines at the rim (the gap is exaggerated for legibility: delta = 0.8 % of the longest strut).
# Right: exploded, each open pyramid pulled out along its axis (O -> face centroid) by 0.45 R.
# Paper white with subtle shading, crisp dark lines >= 2 px at the final size (render standard), own numpy z-buffer rasteriser
# (as the census renders), 3x supersampled. Usage: render.py <fan json> <logo png> <out png> [elev azim]
import sys, json, math, numpy as np
from PIL import Image
J, LOGO, OUT = sys.argv[1:4]; VIEW = (float(sys.argv[4]), float(sys.argv[5])) if len(sys.argv) > 5 else (22, 28)
SS, PX = 3, 1000; N = SS * PX
BG = np.array([0.925, 0.928, 0.94]); PAPER = np.array([0.985, 0.975, 0.945]); INK = np.array([0.10, 0.10, 0.13])
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
class Canvas:
    def __init__(s, lim, cx=0.0, cy=0.0):
        s.lim, s.cx, s.cy = lim, cx, cy; s.z = np.full((N, N), -np.inf); s.col = np.ones((N, N, 3)) * BG; s.id = np.full((N, N), -1, np.int64)
    def scr(s, W): return np.c_[((W[:, 0] - s.cx) / s.lim + 1) * N / 2, (1 - (W[:, 1] - s.cy) / s.lim) * N / 2, W[:, 2]]
    def tri(s, W, colr, ident):
        P = s.scr(W); x0, y0 = np.floor(P[:, :2].min(0)).astype(int); x1, y1 = np.ceil(P[:, :2].max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, N - 1), min(y1, N - 1)
        if x1 < x0 or y1 < y0: return
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = P
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-12: return
        l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den; l2 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den; l3 = 1 - l1 - l2
        m = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9); Z = l1 * az + l2 * bz + l3 * cz
        zb = s.z[y0:y1 + 1, x0:x1 + 1]; m &= Z > zb
        zb[m] = Z[m]; s.col[y0:y1 + 1, x0:x1 + 1][m] = colr; s.id[y0:y1 + 1, x0:x1 + 1][m] = ident
    def outlines(s, w=2 * SS):
        I = s.id; e = np.zeros_like(I, bool)
        e[:, 1:] |= I[:, 1:] != I[:, :-1]; e[1:, :] |= I[1:, :] != I[:-1, :]
        k = w // 2; E = e.copy()
        for dx in range(-k, k + 1):
            for dy in range(-k, k + 1):
                if dx * dx + dy * dy <= k * k: E |= np.roll(np.roll(e, dx, 0), dy, 1)
        s.col[E] = INK
    def image(s): return Image.fromarray((np.clip(s.col, 0, 1) * 255).astype(np.uint8)).resize((PX, PX), Image.LANCZOS)
r = json.load(open(J)); V = np.array(r['points']); R = r['R']; M = rot(*VIEW); delta = 0.008 * R
def sheets(explode):
    """all paper triangles: (3x3 world points, id); each offset by delta into its own pyramid"""
    out = []
    for fi, f in enumerate(r['faces']):
        cs = f['corners']; m = len(cs); cen = V[cs].mean(0); ax = cen / np.linalg.norm(cen); sh = ax * explode * R
        for k in range(m):
            A, B = V[cs[k]], V[cs[(k + 1) % m]]; n = np.cross(A, B); n /= np.linalg.norm(n)
            if n @ cen < 0: n = -n
            T = np.array([np.zeros(3), A, B]) + n * delta
            T[0] = n * delta * 2.2 + ax * delta * 1.5         # apex pulled in a little so that the walls do not cross at O
            out.append((T + sh, fi * 64 + k))
    return out
def panel(explode):
    S = sheets(explode); allp = np.vstack([t for t, _ in S]) @ M.T
    lo, hi = allp[:, :2].min(0), allp[:, :2].max(0); c = (lo + hi) / 2; lim = 0.53 * max(hi - lo) * 1.04
    C = Canvas(lim, c[0], c[1])
    for T, i in S:
        W = T @ M.T; n = np.cross(W[1] - W[0], W[2] - W[0]); n /= np.linalg.norm(n)
        C.tri(W, PAPER * (0.74 + 0.26 * abs(n @ LIGHT)), i)
    C.outlines(); return C.image()
im = Image.new('RGB', (2 * PX + 40, PX), tuple(int(255 * x) for x in BG)); im.paste(panel(0.0), (0, 0)); im.paste(panel(0.45), (PX + 40, 0))
lg = Image.open(LOGO).convert('RGBA'); h = 70; lg = lg.resize((int(lg.width * h / lg.height), h)); im.paste(lg, (im.width - lg.width - 10, im.height - h - 10), lg)
im.save(OUT, dpi=(300, 300)); print(OUT, 'sheets', len(sheets(0)), flush=True)
