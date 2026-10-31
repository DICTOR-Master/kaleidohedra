"""Queen Geodes (DICTO 2026-10-31): the nested shells of the two Queens drawn (1) as a split geode and (2) as a da Vinci sheet,
part sepia line drawing in Leonardo's skeletal 'vacuus' manner (as his polyhedra for Pacioli's De Divina Proportione), part filled.

Geometry and renderer are copied from papers/book-queens/plates/render_plates.py (that script runs its argv at import):
  - the White Queen: the 600 cells of the 600-cell round v = (2,0,0,0), in perspective from an eye at height -21/10 along v,
    grouped into 15 Cleo shells by the height of their centre (shell 14, round -v, wraps the whole picture, so it is never drawn);
  - the Red Queen: the 120 dodecahedra of the 120-cell (corners = the White Queen's cell centres), perspective from just beyond
    the opposite cell, grouped into 9 layers (layers 7 and 8 are huge in this projection, so they are never drawn);
  - the z-buffer renderer (3x supersampled, solid faces, dark edges stamped where no face is in front), extended with per-edge
    colour and depth-graded line width, a parchment ground and a caption.
Colours of the shells as the book (viridis 0.15-0.95 over the 15 shells / 9 layers, core gold).

The geode cut: every drawn cell is a convex polyhedron in the 3D picture; the rind cells are clipped by the cut plane (exactly, by
the hull of their corners behind the plane and the points where their edges cross it) and their cut faces are drawn as polished
stone; the crystal cells are kept whole when they lie wholly behind a second plane a little below the cut, so the cavity floor is
the jagged face of the inner shells, points up. Floats for drawing only; counts are checked and written to geodes.json.
Run on dicto-big-brother:  ~/geom/bin/python queen_geodes.py <600cell-source.json> <dicto-logo.png> <out dir> [font.ttf]
"""
import json, os, sys
from collections import defaultdict
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull

SRC, LOGO, OUT = sys.argv[1:4]
FONT = sys.argv[4] if len(sys.argv) > 4 else "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
os.makedirs(OUT, exist_ok=True)
SIZE, SS = 2000, 3
DARK = np.array([11, 13, 18]) / 255                 # the book's figure ground #0b0d12
PAPER = np.array([0xef, 0xe6, 0xd2]) / 255          # parchment
GOLD = "#d4af37"
EDGE = np.array([0x1d, 0x20, 0x27]) / 255
SEPIA = np.array([0x5b, 0x3a, 0x1e]) / 255          # iron-gall / sepia ink
SEPIA_FILL = np.array([0x4a, 0x30, 0x1a]) / 255
LIGHT = np.array([-0.45, 0.55, 0.70]); LIGHT /= np.linalg.norm(LIGHT)
rgb = lambda h: np.array(matplotlib.colors.to_rgb(h))
facts = {}


# ------------------------------------------------------------------ geometry (from render_plates.py)
S = json.load(open(SRC)); V4 = np.array(S["vertices"], float); cells = S["cells"]
v = V4[0]; dh = v / np.linalg.norm(v)
B = np.linalg.svd(np.eye(4) - np.outer(dh, dh))[0][:, :3]
h = V4 @ dh
EYE = -2.1
P3 = np.array([(x - (x @ dh) * dh) @ B / (hx - EYE) for x, hx in zip(V4, h)])
cent = [round(float(np.mean(h[c])), 9) for c in cells]
keys = sorted(set(cent), reverse=True)
SH = [[c for c, k in zip(cells, cent) if k == key] for key in keys]
assert len(SH) == 15 and sum(map(len, SH)) == 600
assert [len(s) for s in SH] == [20, 20, 30, 60, 60, 60, 20, 60, 20, 60, 60, 60, 30, 20, 20]
COL = plt.cm.viridis(np.linspace(0.15, 0.95, len(SH)))[:, :3]
TRI = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
nb = [i for i in range(120) if abs(np.linalg.norm(V4[i] - v) - (5 ** 0.5 - 1)) < 1e-6]
assert len(nb) == 12
ax5W = P3[nb[0]] / np.linalg.norm(P3[nb[0]])

R4 = np.array([V4[c].mean(0) for c in cells])
cov = defaultdict(list)
for ci, c in enumerate(cells):
    for i in c: cov[i].append(ci)
RC = [cov[i] for i in range(120)]
assert all(len(c) == 20 for c in RC)
hR = R4 @ dh; he = hR.min() * 21 / 20
PR = np.array([(p - (p @ dh) * dh) @ B / ((p @ dh) - he) for p in R4])
hc = V4 @ dh; levels = sorted(set(np.round(hc, 9)), reverse=True)
L = [[i for i in range(120) if abs(hc[i] - lv) < 1e-7] for lv in levels]
assert [len(x) for x in L] == [1, 12, 20, 12, 30, 12, 20, 12, 1]
COLR = plt.cm.viridis(np.linspace(0.15, 0.95, len(L)))[:, :3]
ax5R = PR[RC[L[1][0]]].mean(0); ax5R /= np.linalg.norm(ax5R)


def merged_faces(pts, tol=6):
    """faces of the convex hull of pts, coplanar triangles merged, each as an ordered list of indices into pts."""
    H = ConvexHull(pts); groups = defaultdict(set)
    for simp, eq in zip(H.simplices, H.equations):
        groups[tuple(np.round(eq, tol))].update(int(t) for t in simp)
    out = []
    for key, vs in groups.items():
        vs = list(vs); n = np.array(key[:3]); cc = pts[vs].mean(0)
        u = pts[vs[0]] - cc; u /= np.linalg.norm(u); w = np.cross(n, u)
        vs.sort(key=lambda t: np.arctan2((pts[t] - cc) @ w, (pts[t] - cc) @ u))
        out.append((vs, n))
    return out


def cell_W(c):
    """a White Queen cell (tetrahedron) as (corners, faces)."""
    return P3[c], [list(t) for t in TRI]


def cell_R(i):
    """a Red Queen cell (dodecahedron) as (corners, faces)."""
    pts = PR[RC[i]]; F = [f for f, _ in merged_faces(pts)]
    assert len(F) == 12 and all(len(f) == 5 for f in F)
    return pts, F


def clip(V, F, n, d):
    """the part of the convex cell (V, F) on the side x.n <= d. Returns (polys, is_cut flags) or None if nothing is left."""
    s = V @ n - d
    if s.max() <= 1e-7: return [V[f] for f in F], [False] * len(F)
    if s.min() >= -1e-7: return None
    pts = [V[i] for i in range(len(V)) if s[i] <= 1e-7]
    E = {tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f in F for i in range(len(f))}
    for a, b in E:
        if min(s[a], s[b]) < -1e-7 and max(s[a], s[b]) > 1e-7: pts.append(V[a] + (V[b] - V[a]) * s[a] / (s[a] - s[b]))
    pts = np.unique(np.round(np.array(pts), 10), axis=0)
    polys, cut = [], []
    for vs, nn in merged_faces(pts):
        P = pts[vs]; polys.append(P); cut.append(bool(np.all(np.abs(P @ n - d) < 1e-7)))
    assert sum(cut) == 1, (s, cut)
    return polys, cut


def poly_edges(polys):
    return [np.array([P[i], P[(i + 1) % len(P)]]) for P in polys for i in range(len(P))]


def dedupe(segs):
    seen, out = set(), []
    for E in segs:
        k = tuple(sorted((tuple(np.round(E[0], 6)), tuple(np.round(E[1], 6)))))
        if k not in seen: seen.add(k); out.append(E)
    return out


def frame(fwd, up):
    """camera rows [right, up, towards viewer]."""
    f = fwd / np.linalg.norm(fwd)
    r = np.cross(up, f); r /= np.linalg.norm(r); u = np.cross(f, r)
    return np.array([r, u, f])


def perp(a, hint=(0.3, 0.5, 0.8)):
    t = np.cross(a, hint); return t / np.linalg.norm(t)


# ------------------------------------------------------------------ renderer (render_plates.render, extended)
def shade_solid(col, n):
    d = max(0.0, float(n @ LIGHT))
    return np.clip(np.asarray(col) * (0.34 + 0.58 * d + 0.18 * d ** 12) + 0.06 * d ** 12, 0, 1)


def shade_wash(col, n):
    """a soft watercolour wash: the colour thinned with paper, gentle light, never dark."""
    d = max(0.0, float(n @ LIGHT))
    base = 0.64 * np.asarray(col) + 0.36 * PAPER
    return np.clip(base * (0.80 + 0.26 * d), 0, 1)


def render(polys, cols, edgesets, R, bg, shader, fill=0.86, front=None, centre=None, ext=None):
    """polys: (k,3) arrays; cols: rgb per poly; edgesets: list of dicts {segs, color, w (px) or (wnear, wfar)};
    front: indices of polys that win depth ties (+2 supersampled px). Returns an RGB float image N x N (supersampled)."""
    N = SIZE * SS
    allp = np.vstack([np.vstack(polys)] + [np.vstack(es["segs"]) for es in edgesets if es["segs"]]) @ R.T
    c = (allp.max(0) + allp.min(0)) / 2 if centre is None else centre
    if ext is None: ext = max(allp[:, 0].max() - allp[:, 0].min(), allp[:, 1].max() - allp[:, 1].min()) / 2
    sc = fill * N / 2 / ext
    zlo, zhi = (allp[:, 2].min() - c[2]) * sc, (allp[:, 2].max() - c[2]) * sc
    def scr(P):
        Q = (P @ R.T - c)
        return np.column_stack([N / 2 + Q[:, 0] * sc, N / 2 - Q[:, 1] * sc, Q[:, 2] * sc])
    Z = np.full((N, N), -np.inf, np.float32); ID = np.full((N, N), -1, np.int32)
    shade = []; fr = set(front or [])
    for k, P in enumerate(polys):
        Q = P @ R.T
        n = np.cross(Q[1] - Q[0], Q[2] - Q[0])
        for i in range(2, len(Q) - 1):
            m = np.cross(Q[i] - Q[0], Q[i + 1] - Q[0])
            if np.linalg.norm(m) > np.linalg.norm(n): n = m
        n /= np.linalg.norm(n)
        if n[2] < 0: n = -n
        shade.append(shader(cols[k], n))
        Sx = scr(P)
        if k in fr: Sx[:, 2] += 2.0
        for i in range(1, len(Sx) - 1):
            A, Bv, C = Sx[0], Sx[i], Sx[i + 1]
            x0, x1 = int(max(0, np.floor(min(A[0], Bv[0], C[0])))), int(min(N - 1, np.ceil(max(A[0], Bv[0], C[0]))))
            y0, y1 = int(max(0, np.floor(min(A[1], Bv[1], C[1])))), int(min(N - 1, np.ceil(max(A[1], Bv[1], C[1]))))
            if x1 < x0 or y1 < y0: continue
            den = (Bv[1] - C[1]) * (A[0] - C[0]) + (C[0] - Bv[0]) * (A[1] - C[1])
            if abs(den) < 1e-9: continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l1 = ((Bv[1] - C[1]) * (X - C[0]) + (C[0] - Bv[0]) * (Y - C[1])) / den
            l2 = ((C[1] - A[1]) * (X - C[0]) + (A[0] - C[0]) * (Y - C[1])) / den
            l3 = 1 - l1 - l2
            m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
            z = l1 * A[2] + l2 * Bv[2] + l3 * C[2]
            zb = Z[y0:y1 + 1, x0:x1 + 1]; ib = ID[y0:y1 + 1, x0:x1 + 1]
            w = m & (z > zb)
            zb[w] = z[w]; ib[w] = k
    img = np.empty((N, N, 3), np.float32); img[:] = bg
    SHd = np.array(shade); hit = ID >= 0
    img[hit] = SHd[ID[hit]]
    eps = 0.004 * N
    for es in edgesets:
        if not es["segs"]: continue
        pts = []
        for E in es["segs"]:
            Sx = scr(np.asarray(E, float))
            Ln = np.hypot(*(Sx[1, :2] - Sx[0, :2])); n = max(2, int(Ln / 0.5))
            t = np.linspace(0, 1, n)[:, None]
            pts.append(Sx[0] * (1 - t) + Sx[1] * t)
        P = np.vstack(pts)
        xi = np.clip(P[:, 0].astype(int), 0, N - 1); yi = np.clip(P[:, 1].astype(int), 0, N - 1)
        zmin = Z[yi, xi]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            zmin = np.minimum(zmin, Z[np.clip(yi + dy, 0, N - 1), np.clip(xi + dx, 0, N - 1)])
        vis = (P[:, 2] >= zmin - eps) | ~np.isfinite(zmin)
        xi, yi, zz = xi[vis], yi[vis], P[vis, 2]
        w = es["w"]
        if np.isscalar(w):
            groups = [(w, np.ones(len(xi), bool))]
        else:                                           # depth-graded: near lines heavy, far lines light (6 steps)
            t = np.clip((zz - zlo) / max(zhi - zlo, 1e-9), 0, 1)
            q = np.minimum((t * 6).astype(int), 5)
            groups = [(w[1] + (w[0] - w[1]) * (j + 0.5) / 6, q == j) for j in range(6)]
        M = np.zeros((N, N), bool)
        for wj, sel in groups:
            rad = wj * SS / 2; rr = int(np.ceil(rad))
            for dx in range(-rr, rr + 1):
                for dy in range(-rr, rr + 1):
                    if dx * dx + dy * dy <= rad * rad:
                        M[np.clip(yi[sel] + dy, 0, N - 1), np.clip(xi[sel] + dx, 0, N - 1)] = True
        img[M] = es["color"]
    return img


def finish(img, path, caption=None, ink=SEPIA):
    im = Image.fromarray((img * 255).round().astype(np.uint8)).resize((SIZE, SIZE), Image.LANCZOS).convert("RGBA")
    logo = Image.open(LOGO).convert("RGBA"); w = int(SIZE * 0.07)
    logo = logo.resize((w, w), Image.LANCZOS)
    im.alpha_composite(logo, (SIZE - w - int(SIZE * 0.025), SIZE - w - int(SIZE * 0.025)))
    if caption:
        dr = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, 40)
        tw = dr.textlength(caption, font=f)
        dr.text(((SIZE - tw) / 2, SIZE - 92), caption, font=f, fill=tuple(int(255 * x) for x in ink))
    im = im.convert("RGB"); im.save(path, optimize=True)
    return im


# ------------------------------------------------------------------ the two pictures for one Queen
STONE_OUT = [rgb("#6e675f"), rgb("#776f66"), rgb("#80776d")]     # rind outside, outer band first
STONE_CUT = [rgb("#b3a998"), rgb("#c4b9a6"), rgb("#d2c7b3")]     # polished cut bands, outer band first


def geode(name, cellf, groups, cols, rind, crystals, axis, sink, tilt, off, path):
    """rind: group indices (outermost first) clipped at the plane x.n = 0; crystals: group indices kept whole when wholly below
    x.n = -sink * R (R = radius of the drawn ball)."""
    o = np.radians(off)                                   # the cut normal: the five-fold axis turned by `off` degrees
    n = np.cos(o) * axis + np.sin(o) * perp(axis, (0.9, -0.2, 0.4)); n /= np.linalg.norm(n)
    Rball = max(np.linalg.norm(cellf(c)[0], axis=1).max() for g in rind for c in groups[g])
    polys, pc, segs_r, segs_c = [], [], [], []
    kept = {"rind": {}, "crystals": {}}
    for j, g in enumerate(rind):
        cnt = 0
        for c in groups[g]:
            V, F = cellf(c); r = clip(V, F, n, 0.0)
            if r is None: continue
            cnt += 1
            for P, isc in zip(*r):
                polys.append(P); pc.append(STONE_CUT[min(j, 2)] if isc else STONE_OUT[min(j, 2)])
            segs_r += poly_edges(r[0])
        kept["rind"][g] = cnt
    ncut = len(polys)
    for g in crystals:
        cnt = 0
        for c in groups[g]:
            V, F = cellf(c)
            if (V @ n).max() > -sink * Rball + 1e-9: continue
            cnt += 1
            for f in F: polys.append(V[f]); pc.append(cols[g])
            segs_c += poly_edges([V[f] for f in F])
        kept["crystals"][g] = cnt
    fwd = np.cos(np.radians(tilt)) * n + np.sin(np.radians(tilt)) * perp(n)
    Rm = frame(fwd, n)
    img = render(polys, pc, [{"segs": dedupe(segs_r + segs_c), "color": EDGE, "w": 2.0}], Rm, DARK, shade_solid,
                 front=list(range(ncut)))
    finish(img, path)
    facts[name + "-geode"] = {"rind_groups": rind, "crystal_groups": crystals, "cells_drawn": kept, "sink": sink,
                              "tilt_from_cut_normal_deg": tilt, "cut_normal_off_fivefold_deg": off, "polygons": len(polys)}
    print(name, "geode", kept, flush=True)


def davinci(name, cellf, groups, cols, lines, filled, axis, caption, path, cut=(1.0, 0.85, 0.45)):
    """isometric (orthographic, elevation arctan(1/sqrt 2) = 35.26 deg above the plane normal to the five-fold axis):
    groups in `lines` as sepia edges only (whole, graded by depth: near lines heavy), groups in `filled` as soft washes with fine
    sepia edges, cut open by a plane through the centre (normal = cut[0] towards the viewer + cut[1] right + cut[2] up), so the
    nested shells show as bands on the cut face."""
    up = axis; hz = perp(up)
    el = np.arctan(1 / np.sqrt(2))
    Rm = frame(np.cos(el) * hz + np.sin(el) * up, up)
    nc = cut[0] * Rm[2] + cut[1] * Rm[0] + cut[2] * Rm[1]; nc /= np.linalg.norm(nc)
    polys, pc, segs_f, segs_l = [], [], [], []
    kept = {}
    for g in filled:
        cnt = 0
        for c in groups[g]:
            V, F = cellf(c); r = clip(V, F, nc, 0.0)
            if r is None: continue
            cnt += 1
            for P in r[0]: polys.append(P); pc.append(cols[g])
            segs_f += poly_edges(r[0])
        kept[g] = cnt
    nl = {}
    for g in lines:                                      # line cells: whole, but those with their centre in front of the cut
        nl[g] = 0                                        # are left out, so the cut face is not drawn over
        for c in groups[g]:
            V, F = cellf(c)
            if V.mean(0) @ nc > 0: continue
            nl[g] += 1; segs_l += poly_edges([V[f] for f in F])
    segs_l = dedupe(segs_l); segs_f = dedupe(segs_f)
    img = render(polys, pc, [{"segs": segs_f, "color": SEPIA_FILL, "w": 1.6}, {"segs": segs_l, "color": SEPIA, "w": (3.4, 1.5)}],
                 Rm, PAPER, shade_wash, fill=0.80)
    finish(img, path, caption)
    facts[name + "-davinci"] = {"line_groups": lines, "filled_groups": filled, "filled_cells_drawn": kept, "line_cells_drawn": nl, "line_edges": len(segs_l),
                                "filled_polygons": len(polys), "elevation_deg": float(np.degrees(el)), "cut_normal_camera": list(cut)}
    print(name, "davinci", len(segs_l), "line edges", kept, flush=True)


# DICTO 2026-10-31: "the colours should speak": the White Queen as diamond (clear white to cool steel-blue outwards), the Red Queen
# as ruby (bright pink-red to deep garnet outwards); the core stays gold. QG_PAL=book gives the book's viridis shells.
def ramp(c0, c1, n): a, b = rgb(c0), rgb(c1); return [a + (b - a) * t for t in np.linspace(0, 1, n)]
if os.environ.get("QG_PAL", "gems") == "gems":
    colsW = [rgb(GOLD)] + ramp("#fbfdff", "#8fa6bd", 14)
    colsR = [rgb(GOLD)] + ramp("#ff3d6e", "#5c0717", 8)
else:
    colsW = [rgb(GOLD)] + [COL[k] for k in range(1, 15)]
    colsR = [rgb(GOLD)] + [COLR[k] for k in range(1, 9)]
GW = SH
GR = L
CFG = json.loads(os.environ.get("QG_CFG", "{}"))
which = os.environ.get("QG_ONLY", "wg,wd,rg,rd").split(",")
if "wg" in which:
    geode("white", cell_W, GW, colsW, CFG.get("w_rind", [10, 9]), CFG.get("w_cry", [3, 4, 5, 6, 7, 8]), ax5W,
          CFG.get("w_sink", 0.0), CFG.get("w_tilt", 50), CFG.get("w_off", 17), os.path.join(OUT, "queen-geode-white.png"))
if "wd" in which:
    davinci("white", cell_W, GW, colsW, CFG.get("w_lines", [7, 8]), CFG.get("w_fill", list(range(7))), ax5W,
            "The White Queen · 600-cell · Cleo shells", os.path.join(OUT, "queen-davinci-white.png"))
if "rg" in which:
    geode("red", cell_R, GR, colsR, CFG.get("r_rind", [4]), CFG.get("r_cry", [1, 2, 3]), ax5R,
          CFG.get("r_sink", 0.0), CFG.get("r_tilt", 50), CFG.get("r_off", 17), os.path.join(OUT, "queen-geode-red.png"))
if "rd" in which:
    davinci("red", cell_R, GR, colsR, CFG.get("r_lines", [4]), CFG.get("r_fill", [0, 1, 2, 3]), ax5R,
            "The Red Queen · 120-cell · layers", os.path.join(OUT, "queen-davinci-red.png"))
# ------------------------------------------------------------------ the 2 x 2 sheet (rows: White, Red; columns: geode, da Vinci)
names = [["queen-geode-white.png", "queen-davinci-white.png"], ["queen-geode-red.png", "queen-davinci-red.png"]]
labels = [["The White Queen · geode", "The White Queen · da Vinci"], ["The Red Queen · geode", "The Red Queen · da Vinci"]]
if all(os.path.exists(os.path.join(OUT, n)) for r in names for n in r):
    T, G, TOP, LAB = 860, 26, 110, 64                     # tile, gutter, title band, label band
    W = 2 * T + 3 * G; H = TOP + 2 * (T + LAB) + G
    sheet = Image.new("RGB", (W, H), tuple(int(255 * x) for x in DARK)); dr = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(FONT, 50); fl = ImageFont.truetype(FONT, 32)
    t = "Queen Geodes"; dr.text(((W - dr.textlength(t, font=ft)) / 2, 30), t, font=ft, fill=(228, 220, 200))
    for i in range(2):
        for j in range(2):
            x = G + j * (T + G); y = TOP + i * (T + LAB)
            sheet.paste(Image.open(os.path.join(OUT, names[i][j])).resize((T, T), Image.LANCZOS), (x, y))
            dr.text((x + (T - dr.textlength(labels[i][j], font=fl)) / 2, y + T + 12), labels[i][j], font=fl, fill=(228, 220, 200))
    sheet.save(os.path.join(OUT, "queen-geodes-sheet.png"), optimize=True)
    print("sheet", sheet.size, flush=True)
prev = json.load(open(os.path.join(OUT, "geodes.json"))) if os.path.exists(os.path.join(OUT, "geodes.json")) else {}
prev.update(facts); prev["config"] = CFG
json.dump(prev, open(os.path.join(OUT, "geodes.json"), "w"), indent=1)
print("done")
