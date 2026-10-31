"""Queen Geodes (DICTO 2026-10-31): the nested shells of the two Queens drawn (1) as a split geode and (2) as a da Vinci sheet,
part sepia line drawing in Leonardo's skeletal 'vacuus' manner (as his polyhedra for Pacioli's De Divina Proportione), part filled.

Geometry and renderer are copied from papers/book-queens/plates/render_plates.py (that script runs its argv at import):
  - the White Queen: the 600 cells of the 600-cell round v = (2,0,0,0), in perspective from an eye at height -21/10 along v,
    grouped into 15 Cleo shells by the height of their centre (shell 14, round -v, wraps the whole picture, so it is never drawn);
  - the Red Queen: the 120 dodecahedra of the 120-cell (corners = the White Queen's cell centres), perspective from just beyond
    the opposite cell, grouped into 9 layers (layers 7 and 8 are huge in this projection, so they are never drawn);
  - the z-buffer renderer (3x supersampled, solid faces, dark edges stamped where no face is in front), extended with per-edge
    colour and depth-graded line width, a parchment ground and a caption.
Colours: pale gems (diamond White Queen, ruby Red Queen), core gold, basalt rind; see README (round 2).

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
HALF = LIGHT + np.array([0, 0, 1.0]); HALF /= np.linalg.norm(HALF)     # mirror direction for highlights (viewer along +z)


def shade_solid(col, n):
    d = max(0.0, float(n @ LIGHT))
    return np.clip(np.asarray(col) * (0.34 + 0.58 * d + 0.18 * d ** 12) + 0.06 * d ** 12, 0, 1)


def shade_stone(col, n):
    """basalt: dark, matt, with enough light range that its edges and silhouette still read on the dark ground."""
    d = max(0.0, float(n @ LIGHT))
    return np.clip(np.asarray(col) * (0.62 + 0.52 * d), 0, 1)


def gem_spec(n):
    h = max(0.0, float(n @ HALF))
    return min(1.0, 0.95 * h ** 40 + 0.20 * h ** 6)


def shade_gem(col, n):
    """pale crystal: soft body light, and faces near the mirror direction flash to near-white."""
    d = max(0.0, float(n @ LIGHT))
    base = np.asarray(col) * (0.62 + 0.38 * d)
    return np.clip(base + (1 - base) * gem_spec(n), 0, 1)


def shade_wash(col, n):
    """a soft watercolour wash: the colour thinned with paper, gentle light, never dark."""
    d = max(0.0, float(n @ LIGHT))
    base = 0.64 * np.asarray(col) + 0.36 * PAPER
    return np.clip(base * (0.80 + 0.26 * d), 0, 1)


class Scene:
    """z-buffer of planar polygons. polys: (k,3) arrays; cols: rgb per poly; shaders: one shading function per poly;
    front: indices of polys that win depth ties (+2 supersampled px); extra: further points that must fit in the frame."""

    def __init__(self, polys, cols, shaders, R, bg, fill=0.86, front=None, extra=()):
        N = self.N = SIZE * SS
        allp = np.vstack([np.vstack(polys)] + [np.vstack(e) for e in extra if len(e)]) @ R.T
        c = (allp.max(0) + allp.min(0)) / 2
        ext = max(allp[:, 0].max() - allp[:, 0].min(), allp[:, 1].max() - allp[:, 1].min()) / 2
        sc = fill * N / 2 / ext
        self.zlo, self.zhi = (allp[:, 2].min() - c[2]) * sc, (allp[:, 2].max() - c[2]) * sc
        self.scr = lambda P: np.column_stack([N / 2 + ((P @ R.T - c)[:, 0]) * sc, N / 2 - ((P @ R.T - c)[:, 1]) * sc,
                                               ((P @ R.T - c)[:, 2]) * sc])
        Z = np.full((N, N), -np.inf, np.float32); ID = np.full((N, N), -1, np.int32)
        shade, spec = [], []; fr = set(front or [])
        for k, P in enumerate(polys):
            Q = P @ R.T
            n = np.cross(Q[1] - Q[0], Q[2] - Q[0])
            for i in range(2, len(Q) - 1):
                m = np.cross(Q[i] - Q[0], Q[i + 1] - Q[0])
                if np.linalg.norm(m) > np.linalg.norm(n): n = m
            n /= np.linalg.norm(n)
            if n[2] < 0: n = -n
            shade.append(shaders[k](cols[k], n)); spec.append(gem_spec(n))
            Sx = self.scr(P)
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
        self.Z, self.ID, self.polys, self.spec = Z, ID, polys, np.array(spec)
        img = np.empty((N, N, 3), np.float32); img[:] = bg
        SHd = np.array(shade); hit = ID >= 0
        img[hit] = SHd[ID[hit]]
        self.img = img

    def _samples(self, segs):
        pts = []
        for E in segs:
            Sx = self.scr(np.asarray(E, float))
            Ln = np.hypot(*(Sx[1, :2] - Sx[0, :2])); n = max(2, int(Ln / 0.5))
            t = np.linspace(0, 1, n)[:, None]
            pts.append(Sx[0] * (1 - t) + Sx[1] * t)
        return np.vstack(pts)

    def _front_z(self, xi, yi):
        N, Z = self.N, self.Z
        zmin = Z[yi, xi]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            zmin = np.minimum(zmin, Z[np.clip(yi + dy, 0, N - 1), np.clip(xi + dx, 0, N - 1)])
        return zmin

    def edges(self, segs, color, w, hidden=False, alpha=1.0, through=None, depth=None):
        """stamp edges. Visible parts by default; hidden=True draws only the parts behind a face, and only where that face is
        in `through` (a bool per poly: the crystal faces one sees through) and no deeper than `depth` (final px) behind it.
        w: width in final px, or (near, far) for depth-graded lines. alpha < 1 blends the ink over what is there."""
        if not segs: return
        N = self.N; eps = 0.004 * N
        P = self._samples(segs)
        xi = np.clip(P[:, 0].astype(int), 0, N - 1); yi = np.clip(P[:, 1].astype(int), 0, N - 1)
        zf = self._front_z(xi, yi)
        vis = (P[:, 2] >= zf - eps) | ~np.isfinite(zf)
        if hidden:
            idf = self.ID[yi, xi]
            sel = ~vis & (idf >= 0)
            sel &= through[np.maximum(idf, 0)]
            if depth is not None: sel &= (self.Z[yi, xi] - P[:, 2]) < depth * SS
        else:
            sel = vis
        xi, yi, zz = xi[sel], yi[sel], P[sel, 2]
        if np.isscalar(w):
            groups = [(w, np.ones(len(xi), bool))]
        else:                                           # depth-graded: near lines heavy, far lines light (6 steps)
            t = np.clip((zz - self.zlo) / max(self.zhi - self.zlo, 1e-9), 0, 1)
            q = np.minimum((t * 6).astype(int), 5)
            groups = [(w[1] + (w[0] - w[1]) * (j + 0.5) / 6, q == j) for j in range(6)]
        M = np.zeros((N, N), bool)
        for wj, s in groups:
            rad = wj * SS / 2; rr = int(np.ceil(rad))
            for dx in range(-rr, rr + 1):
                for dy in range(-rr, rr + 1):
                    if dx * dx + dy * dy <= rad * rad:
                        M[np.clip(yi[s] + dy, 0, N - 1), np.clip(xi[s] + dx, 0, N - 1)] = True
        self.img[M] = self.img[M] * (1 - alpha) + np.asarray(color) * alpha

    def glints(self, which, count, size, outline=None, spacing=0.045):
        """crisp four-pointed glints at the brightest visible corners of the polys in `which`: a corner's brightness is the
        highest mirror highlight among its faces; corners are taken brightest first, at least `spacing` x picture apart."""
        N = self.N; best = {}
        for k in np.nonzero(which)[0]:
            for p in self.polys[k]:
                key = tuple(np.round(p, 6))
                if self.spec[k] > best.get(key, (-1, None))[0]: best[key] = (self.spec[k], p)
        cand = sorted(best.values(), key=lambda t: -t[0])
        S = self.scr(np.array([p for _, p in cand])) if cand else np.zeros((0, 3))
        chosen = []
        for (s, p), (x, y, z) in zip(cand, S):
            if len(chosen) >= count or s < 0.02: break
            xi, yi = int(np.clip(x, 0, N - 1)), int(np.clip(y, 0, N - 1))
            zf = self._front_z(np.array([xi]), np.array([yi]))[0]
            if np.isfinite(zf) and z < zf - 0.004 * N: continue          # hidden corner
            ids = self.ID[max(0, yi - 4):yi + 5, max(0, xi - 4):xi + 5].ravel()
            if np.count_nonzero(which[ids[ids >= 0]]) < 0.4 * len(ids): continue   # a corner shown mostly on stone or paper
            if any((x - a) ** 2 + (y - b) ** 2 < (spacing * N) ** 2 for a, b, _ in chosen): continue
            chosen.append((x, y, s))
        mask = Image.new("L", (N, N), 0); dm = ImageDraw.Draw(mask)
        omask = Image.new("L", (N, N), 0); do = ImageDraw.Draw(omask)
        for x, y, s in chosen:
            L = size * SS * (0.6 + 0.4 * s); wst = L * 0.10
            star = lambda L, wst: [(x + L, y), (x + wst, y + wst), (x, y + L), (x - wst, y + wst), (x - L, y),
                                   (x - wst, y - wst), (x, y - L), (x + wst, y - wst)]
            if outline is not None: do.polygon(star(L + 2.2 * SS, wst + 1.6 * SS), fill=255)
            dm.polygon(star(L, wst), fill=255)
        if outline is not None:
            o = np.asarray(omask, np.float32)[..., None] / 255
            self.img = self.img * (1 - o) + np.asarray(outline) * o
        m = np.asarray(mask, np.float32)[..., None] / 255
        self.img = self.img * (1 - m) + np.array([1.0, 1.0, 1.0]) * m
        return len(chosen)


def finish(img, path, caption=None, ink=SEPIA):
    im = Image.fromarray((np.clip(img, 0, 1) * 255).round().astype(np.uint8)).resize((SIZE, SIZE), Image.LANCZOS).convert("RGBA")
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
BASALT_OUT = [rgb("#2f343e"), rgb("#343a44")]       # rind outside: deep blue-black grey, outer band first
BASALT_CUT = [rgb("#565e6b"), rgb("#5e6673")]       # polished cut bands, a little lighter
EDGE_ROCK = np.array([0x0e, 0x10, 0x14]) / 255


def geode(name, cellf, groups, cols, rind, crystals, axis, sink, tilt, off, path, glint_ink):
    """rind: group indices (outermost first) clipped at the plane x.n = 0; crystals: group indices kept whole when wholly below
    x.n = -sink * R (R = radius of the drawn ball). Crystals pale gems: highlights, their hidden edges faintly through, glints."""
    o = np.radians(off)                                   # the cut normal: the five-fold axis turned by `off` degrees
    n = np.cos(o) * axis + np.sin(o) * perp(axis, (0.9, -0.2, 0.4)); n /= np.linalg.norm(n)
    Rball = max(np.linalg.norm(cellf(c)[0], axis=1).max() for g in rind for c in groups[g])
    polys, pc, sh, segs_r, segs_c = [], [], [], [], []
    kept = {"rind": {}, "crystals": {}}
    for j, g in enumerate(rind):
        cnt = 0
        for c in groups[g]:
            V, F = cellf(c); r = clip(V, F, n, 0.0)
            if r is None: continue
            cnt += 1
            for P, isc in zip(*r):
                polys.append(P); pc.append(BASALT_CUT[min(j, 1)] if isc else BASALT_OUT[min(j, 1)]); sh.append(shade_stone)
            segs_r += poly_edges(r[0])
        kept["rind"][g] = cnt
    ncut = len(polys)
    for g in crystals:
        cnt = 0
        for c in groups[g]:
            V, F = cellf(c)
            if (V @ n).max() > -sink * Rball + 1e-9: continue
            cnt += 1
            for f in F: polys.append(V[f]); pc.append(cols[g]); sh.append(shade_gem)
            segs_c += poly_edges([V[f] for f in F])
        kept["crystals"][g] = cnt
    gem = np.array([i >= ncut for i in range(len(polys))])
    fwd = np.cos(np.radians(tilt)) * n + np.sin(np.radians(tilt)) * perp(n)
    sc = Scene(polys, pc, sh, frame(fwd, n), DARK, front=list(range(ncut)))
    segs_c = dedupe(segs_c)
    sc.edges(segs_c, [1, 1, 1], 1.1, hidden=True, alpha=0.42, through=gem, depth=160)   # seen through the crystal in front
    sc.edges(dedupe(segs_r), EDGE_ROCK, 2.0)
    sc.edges(segs_c, EDGE, 1.8)
    ng = sc.glints(gem, 32, 26, outline=glint_ink)
    finish(sc.img, path)
    facts[name + "-geode"] = {"rind_groups": rind, "crystal_groups": crystals, "cells_drawn": kept, "sink": sink,
                              "tilt_from_cut_normal_deg": tilt, "cut_normal_off_fivefold_deg": off, "polygons": len(polys),
                              "glints": ng}
    print(name, "geode", kept, "glints", ng, flush=True)


def davinci(name, cellf, groups, core_col, cols, glint_ink, lines, filled, axis, caption, path, cut=(0.7, 0.3, 1.0), fracture=0.0):
    """isometric (orthographic, elevation arctan(1/sqrt 2) = 35.26 deg above the plane normal to the five-fold axis):
    groups in `lines` as sepia edges only (whole, graded by depth: near lines heavy); the core (group 0) whole, solid gold, standing
    out of the cut, pale crystal (fracture > 0: each core cell moved out from the centre by fracture x core radius, so the pieces
    read as a fractured gem); the other groups in `filled` cut open by a plane through the centre (normal = cut[0] towards the
    viewer + cut[1] right + cut[2] up), in their deep gem colours with lighter cut faces; highlights, hidden edges through, glints."""
    up = axis; hz = perp(up)
    el = np.arctan(1 / np.sqrt(2))
    Rm = frame(np.cos(el) * hz + np.sin(el) * up, up)
    nc = cut[0] * Rm[2] + cut[1] * Rm[0] + cut[2] * Rm[1]; nc /= np.linalg.norm(nc)
    polys, pc, sh, segs_core, segs_f, segs_l = [], [], [], [], [], []
    rcore = max(np.linalg.norm(cellf(c)[0], axis=1).max() for c in groups[0])
    for c in groups[0]:
        V, F = cellf(c)
        m = V.mean(0)
        if fracture and np.linalg.norm(m) > 1e-9: V = V + m / np.linalg.norm(m) * fracture * rcore
        for f in F: polys.append(V[f]); pc.append(core_col); sh.append(shade_gem)
        segs_core += poly_edges([V[f] for f in F])
    ncore = len(polys)
    kept = {0: len(groups[0])}
    for g in filled:
        if g == 0: continue
        cnt = 0
        for c in groups[g]:
            V, F = cellf(c); r = clip(V, F, nc, 0.0)
            if r is None: continue
            cnt += 1
            for P, isc in zip(*r):
                polys.append(P); pc.append(0.72 * cols[g] + 0.28 if isc else cols[g]); sh.append(shade_gem)
            segs_f += poly_edges(r[0])
        kept[g] = cnt
    nl = {}
    for g in lines:                                      # line cells: whole, but only the far half (centre behind the plane
        nl[g] = 0                                        # through the centre facing the viewer), so nothing is drawn over the cut
        for c in groups[g]:
            V, F = cellf(c)
            if V.mean(0) @ Rm[2] > 0: continue
            nl[g] += 1; segs_l += poly_edges([V[f] for f in F])
    segs_l = dedupe(segs_l); segs_f = dedupe(segs_f); segs_core = dedupe(segs_core)
    gem = np.ones(len(polys), bool)                     # core and shells are all crystal
    sc = Scene(polys, pc, sh, Rm, PAPER, fill=0.80, front=list(range(ncore)), extra=segs_l)
    sc.edges(segs_f, SEPIA_FILL, 1.0, hidden=True, alpha=0.28, through=gem, depth=90)   # not the core's: they hatch its gaps
    sc.edges(segs_f, SEPIA_FILL, 1.5)
    sc.edges(segs_core, SEPIA_FILL, 1.9)
    sc.edges(segs_l, SEPIA, (3.4, 1.5))
    ng = sc.glints(gem, 16, 24, outline=glint_ink)
    finish(sc.img, path, caption)
    facts[name + "-davinci"] = {"line_groups": lines, "filled_groups": filled, "core_cells_whole": len(groups[0]),
                                "filled_cells_drawn": kept, "line_cells_drawn": nl, "line_edges": len(segs_l),
                                "filled_polygons": len(polys), "elevation_deg": float(np.degrees(el)),
                                "cut_normal_camera": list(cut), "glints": ng, "core_fracture": fracture}
    print(name, "davinci", len(segs_l), "line edges", kept, "glints", ng, flush=True)


# DICTO 2026-10-31: the White Queen as diamond, the Red Queen as ruby, the core gold. Round 2 ("stand out more ... pale translucent
# sparkly"): pale crystals: diamond near-white to faint ice-blue outwards, ruby pale rose to clear pink-red outwards.
def ramp(c0, c1, n): a, b = rgb(c0), rgb(c1); return [a + (b - a) * t for t in np.linspace(0, 1, n)]
# Round 3 (DICTO): the crystals back to the deep ramps (diamond to steel-blue, ruby to garnet); only the da Vinci core goes pale.
colsW = [rgb(GOLD)] + ramp("#fbfdff", "#8fa6bd", 14)
colsR = [rgb(GOLD)] + ramp("#ff3d6e", "#5c0717", 8)
GW = SH
GR = L
CFG = json.loads(os.environ.get("QG_CFG", "{}"))
which = os.environ.get("QG_ONLY", "wg,wd,rg,rd").split(",")
ICE, ROSE = rgb("#7f97ae"), rgb("#b34a66")            # glint outlines on paper
if "wg" in which:
    geode("white", cell_W, GW, colsW, CFG.get("w_rind", [10, 9]), CFG.get("w_cry", [3, 4, 5, 6, 7, 8]), ax5W,
          CFG.get("w_sink", 0.0), CFG.get("w_tilt", 50), CFG.get("w_off", 17), os.path.join(OUT, "queen-geode-white.png"), ICE)
if "wd" in which:
    davinci("white", cell_W, GW, rgb(CFG.get("w_core", "#eef5fb")), colsW, ICE,
            CFG.get("w_lines", [7, 8]), CFG.get("w_fill", list(range(7))), ax5W,
            "The White Queen · 600-cell · Cleo shells", os.path.join(OUT, "queen-davinci-white.png"),
            tuple(CFG.get("cut", (0.7, 0.3, 1.0))), CFG.get("w_fracture", 0.06))
if "rg" in which:
    geode("red", cell_R, GR, colsR, CFG.get("r_rind", [4]), CFG.get("r_cry", [1, 2, 3]), ax5R,
          CFG.get("r_sink", 0.0), CFG.get("r_tilt", 50), CFG.get("r_off", 17), os.path.join(OUT, "queen-geode-red.png"), ROSE)
if "rd" in which:
    davinci("red", cell_R, GR, rgb(CFG.get("r_core", "#ffd6df")), colsR, ROSE,
            CFG.get("r_lines", [4]), CFG.get("r_fill", [0, 1, 2, 3]), ax5R,
            "The Red Queen · 120-cell · layers", os.path.join(OUT, "queen-davinci-red.png"),
            tuple(CFG.get("cut", (0.7, 0.3, 1.0))))
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
