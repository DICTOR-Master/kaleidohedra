# The Golden Ladder cover (DICTO 11-06 "yes make the ladder cover"): a ladder whose rungs are golden shapes climbing the dimensions,
# 2D truncated triangle (ratio phi) -> 3D Icosaxes + Unborn Axes -> 4D 120-cell (Chapter 5) -> 8D E8 as two 600-cells (Coxeter plane,
# Chapter 9), with the series title panel (LED letters, as Dictonic Bonds / The Golden Cycle). Two versions: A series colours, B all gold.
import numpy as np, itertools, sys
from PIL import Image, ImageDraw, ImageFilter
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
import ledtext as L
phi = (1 + 5 ** 0.5) / 2
GROUND = (20, 15, 11); GOLD = (217, 165, 33); VIOLET = (150, 105, 205); TEAL = (40, 165, 150); BLUE = (55, 115, 205); LILAC = (180, 138, 224)
W, Hc = 2400, 3394; SS = 2   # A4 (DICTO 11-06: cover centred, like the other books)
   # supersampling for the shapes
# ------------------------------------------------------------------ geometry
def rot(a, b, c):
    Rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    Ry = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    Rz = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx
def faces_of(V):
    h = ConvexHull(V); groups = {}
    for s, eq in zip(h.simplices, h.equations):
        k = tuple(np.round(eq, 5)); groups.setdefault(k, [eq, set()])[1].update(s)
    out = []
    for eq, idx in groups.values():
        idx = list(idx); n = eq[:3]; c = V[idx].mean(0)
        u = V[idx[0]] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        ang = [np.arctan2((V[i] - c) @ v, (V[i] - c) @ u) for i in idx]
        out.append(([idx[i] for i in np.argsort(ang)], n))
    return out
def Tx(x):   # semi-uniform truncated octahedron: hull of all permutations of (+-(1+x), +-x, 0)  (Koca et al.; #48, #88)
    P = set()
    for p in itertools.permutations((1 + x, x, 0)):
        for s in itertools.product((1, -1), repeat=3): P.add(tuple(a * b for a, b in zip(p, s)))
    return np.array(sorted(P), float)
def cell600():
    V = [p for i in range(4) for s in (1, -1) for p in [tuple(s if j == i else 0 for j in range(4))]]
    V += list(itertools.product((0.5, -0.5), repeat=4))
    base = (phi / 2, 0.5, 1 / (2 * phi), 0.0)
    even = [p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
    for p in even:
        for s in itertools.product((1, -1), repeat=3):
            q = [0.0] * 4; vals = [base[0] * s[0], base[1] * s[1], base[2] * s[2], 0.0]
            for k in range(4): q[p[k]] = vals[k]
            V.append(tuple(q))
    V = np.unique(np.round(np.array(V, float), 9), axis=0); assert len(V) == 120, len(V)
    D = np.linalg.norm(V[:, None] - V[None], axis=2); e = D[D > 1e-9].min()
    E = [(i, j) for i in range(120) for j in range(i + 1, 120) if abs(D[i, j] - e) < 1e-6]; assert len(E) == 720
    return V, E
def cell120():
    V, E = cell600(); nb = {i: set() for i in range(120)}
    for i, j in E: nb[i].add(j); nb[j].add(i)
    tets = set()
    for i, j in E:
        for k in nb[i] & nb[j]:
            for l in nb[i] & nb[j] & nb[k]: tets.add(tuple(sorted((i, j, k, l))))
    tets = sorted(tets); assert len(tets) == 600, len(tets)
    C = np.array([V[list(t)].mean(0) for t in tets]); C /= np.linalg.norm(C, axis=1)[:, None]
    face = {}
    for n, t in enumerate(tets):
        for f in itertools.combinations(t, 3): face.setdefault(f, []).append(n)
    E2 = [tuple(v) for v in face.values() if len(v) == 2]; assert len(E2) == 1200, len(E2)
    return C, E2
def coxeter_plane(R):
    """H4 Coxeter plane from the roots R (the 600-cell's 120 vertices): simple roots = extreme rays of the positive cone."""
    g = np.array([1, 0.31, 0.17, 0.07]); P = R[R @ g > 0]
    simple = []
    for k, r in enumerate(P):
        others = np.delete(P, k, axis=0)
        res = linprog(np.zeros(len(others)), A_eq=others.T, b_eq=r, bounds=(0, None), method='highs')
        if not res.success: simple.append(r)
    S = np.array(simple); assert len(S) == 4, len(S)
    C = np.eye(4)
    for a in S: C = C @ (np.eye(4) - 2 * np.outer(a, a) / (a @ a))
    w, v = np.linalg.eig(C); k = np.argmin(abs(w - np.exp(2j * np.pi / 30)))
    x = v[:, k].real; y = v[:, k].imag; x /= np.linalg.norm(x); y -= (y @ x) * x; y /= np.linalg.norm(y)
    return x, y
# ------------------------------------------------------------------ painting
def shade(col, n, light=np.array([-0.45, 0.65, 0.62])):
    light = light / np.linalg.norm(light); k = 0.42 + 0.58 * max(0.0, n @ light)
    return tuple(int(min(255, c * k + 18 * max(0, n @ light) ** 8)) for c in col)
def draw_solid(dr, V, cx, cy, s, col, R):
    P = V @ R.T; F = faces_of(V)
    for idx, n in sorted(F, key=lambda f: (P[f[0]] @ np.array([0, 0, 1])).mean()):
        nn = R @ n
        if nn[2] <= 0: continue
        pts = [(cx + s * P[i][0], cy - s * P[i][1]) for i in idx]
        dr.polygon(pts, fill=shade(col, nn)); dr.line(pts + [pts[0]], fill=(10, 8, 6), width=max(2, int(s * 0.022)), joint='curve')
def draw_wire(img, X2, E, depth, cx, cy, s, col, width, alpha_range=(0.18, 0.95)):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    z = (depth - depth.min()) / (np.ptp(depth) + 1e-9)
    for i, j in sorted(E, key=lambda e: z[e[0]] + z[e[1]]):
        a = alpha_range[0] + (alpha_range[1] - alpha_range[0]) * (z[i] + z[j]) / 2
        d.line([(cx + s * X2[i][0], cy - s * X2[i][1]), (cx + s * X2[j][0], cy - s * X2[j][1])], fill=col + (int(255 * a),), width=width)
    img.alpha_composite(lay)
def glow_layer(img, mask_draw_fn, col, radius):
    m = Image.new('L', img.size, 0); mask_draw_fn(ImageDraw.Draw(m)); g = m.filter(ImageFilter.GaussianBlur(radius))
    img.alpha_composite(Image.merge('RGBA', [Image.new('L', img.size, c) for c in col] + [g.point(lambda v: int(v * 0.55))]))
def make(version):
    mono = version == 'B'
    C2, C3a, C3b, C4, C8a, C8b = ((GOLD,) * 6) if mono else (GOLD, GOLD, VIOLET, VIOLET, GOLD, TEAL)
    LADH = 2500; img = Image.new('RGBA', (W * SS, LADH * SS), GROUND + (255,))
    xl, xr = 330 * SS, (W - 330) * SS; rungs = [2440, 1930, 1440, 860]   # DICTO 11-06: much more space for the top rung (8D)   # 2D (bottom) ... 8D (top), centre y
    rail = lambda d: [d.line([(x, 160 * SS), (x, (LADH - 20) * SS)], fill=255, width=26 * SS) for x in (xl, xr)]
    glow_layer(img, rail, GOLD, 22 * SS)
    d = ImageDraw.Draw(img)
    for x in (xl, xr): d.line([(x, 160 * SS), (x, (LADH - 20) * SS)], fill=GOLD + (255,), width=22 * SS)
    for y in rungs:
        d.line([(xl, y * SS), (xr, y * SS)], fill=(150, 112, 22, 255), width=18 * SS)
    # 2D: truncated triangle, long/short = phi (Chapter 3, #88), lying on its rung, seen slightly from above
    a, b = phi, 1.0; Lt = a + 2 * b; T = [np.array([np.cos(t), np.sin(t)]) * Lt / 3 ** 0.5 for t in np.radians([90, 210, 330])]
    hexv = []
    for i in range(3):
        p, q = T[i], T[(i + 1) % 3]; u = (q - p) / Lt; hexv += [p + u * b, q - u * b]
    hexv = np.array(hexv); V2 = np.c_[hexv, np.zeros(6)]; V2 = np.r_[V2, V2 + [0, 0, -0.16]]
    R = rot(np.radians(-20), 0, 0); draw_solid(d, V2, W / 2 * SS, (rungs[0] - 205) * SS, 175 * SS, C2, R)
    # 3D: Icosaxes (x = 1/phi^2) and Unborn Axes (x = 1/(phi sqrt5)) as truncated octahedra T(x) (#48, #88); scaled to one edge
    for xx, dx, col in ((phi, -330, C3a), (1 / phi, 330, C3b)):
        V = Tx(xx); V = V / np.linalg.norm(V, axis=1).max()
        draw_solid(d, V, (W / 2 + dx) * SS, (rungs[1] - 235) * SS, 215 * SS, col, rot(np.radians(-24), np.radians(32), np.radians(10)))
    # 4D: the 120-cell (Chapter 5), orthographic shadow after a 4D turn
    C, E2 = cell120(); w0 = C[:, 3].max()   # a cell centre lies on the w axis; project from just beyond that cell
    X3 = C[:, :3] / (1.08 * w0 - C[:, 3])[:, None]; X3 /= np.linalg.norm(X3, axis=1).max(); X3 = X3 @ rot(np.radians(-18), np.radians(22), 0).T
    draw_wire(img, X3[:, :2], E2, X3[:, 2], W / 2 * SS, (rungs[2] - 290) * SS, 265 * SS, C4, 4 * SS, (0.30, 1.0))
    # 8D: E8 as two 600-cells, one phi times the other, in the H4 Coxeter plane (8 rings of 30; Chapter 9)
    V6, E6 = cell600(); x, y = coxeter_plane(V6)
    for scale, col, wd, ar in ((phi, C8a, 2, (0.12, 0.30)), (1.0, C8b, 2, (0.15, 0.40))):
        P2 = np.c_[V6 @ x, V6 @ y] * scale / phi
        draw_wire(img, P2, E6, np.zeros(120) + np.linspace(0, 1, 120), W / 2 * SS, (rungs[3] - 330) * SS, 255 * SS, col, wd * SS, ar)
        dd = ImageDraw.Draw(img); r = 6 * SS
        for px, py in P2: X0, Y0 = W / 2 * SS + 255 * SS * px, (rungs[3] - 330) * SS - 255 * SS * py; dd.ellipse([X0 - r, Y0 - r, X0 + r, Y0 + r], fill=col + (255,))
    lad = img.resize((W, LADH), Image.LANCZOS).convert('RGB')
    # dimension marks, LED letters, left of the left rail
    can = np.array(lad, float)
    for y, t in zip(rungs, ('2D', '3D', '4D', '8D')):
        g = L.word(t, 60, lambda ch: GOLD if mono else (255, 255, 255)); L.paste(can, g, 165, y - 140); L.paste(can, g, W - 165, y - 140)   # both sides, so the ladder stands centred
    lad = Image.fromarray(np.clip(can, 0, 255).astype(np.uint8))
    # title panel (series style)
    N = W
    big = L.word('THE GOLDEN LADDER', int(N * 0.058), lambda ch: GOLD, big=(0, 4, 11))
    sub = L.word('GOLDEN CUTS FROM PLATO TO THE EIGHTH DIMENSION', int(N * 0.023), lambda ch: GOLD if mono else TEAL, big=(0, 12, 17, 23, 27, 34))
    by = L.word('* DICTO *', int(N * 0.040), lambda ch: GOLD if mono else BLUE, big=(0, 2, 3, 4, 5, 6, 8))
    panel = np.ones((Hc - LADH, N, 3)) * np.array(GROUND, float)
    yy = L.paste(panel, big, N / 2, 70); yy = L.paste(panel, sub, N / 2, yy + 70); L.paste(panel, by, N / 2, yy + 80)
    out = Image.new('RGB', (W, Hc), GROUND); out.paste(lad, (0, 0)); out.paste(Image.fromarray(np.clip(panel, 0, 255).astype(np.uint8)), (0, LADH))
    out.save(f'../golden-ladder-cover-{version}.png'); print('saved', version, flush=True)
if __name__ == '__main__':
    for v in sys.argv[1:] or ['A', 'B']: make(v)
    print('FINAL OK')
