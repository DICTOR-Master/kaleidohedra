"""Full-page plates for 'Alicia in Wonderland' version 3 (DICTO 2026-10-31: "full page cards/plates" to give the shapes room).
Three groups, all drawn with one renderer (a z-buffer, so no sorting faults): solid shaded faces, dark edges about 2 px wide at the
plate's printed size, antialiased by 3x supersampling, no haze; the book's dark figure ground and the DICTO mark in each corner.
  1. the named slices of the two Queens in the DICTO solids dataset v6 (exact models, decimal coordinates used for drawing);
     faces coloured by their number of sides as in the book's atlas pages (triangles ivory, four-sided faces blue, ...);
  2. the White Queen's 15 Cleo shells: the 600 cells of the 600-cell round the vertex v = (2,0,0,0), grouped by the height of their
     centre along v, in perspective from an eye at height -21/10 (as studies/2026-10-27-white-queen-600/scripts/cleo_shells.py);
  3. the Red Queen's 9 cell layers: the 120 dodecahedra of the 120-cell built from the White Queen (corners = her cell centres),
     grouped by the height of their centre along v, perspective from just beyond the opposite cell (as render_red_queen.py).
Colours of groups 2 and 3 as the book's Figures 6.3 and 8.1 (viridis from 0.15 to 0.95, core gold); the shells inside the one shown
are drawn in dark grey so the nesting can be seen. Floats for drawing only; every count is checked here and written to plates.json.
Run on dicto-big-brother:  ~/geom/bin/python render_plates.py <dataset-v6 dir> <600cell-source.json> <dicto-logo.png> <out dir>
"""
import csv, json, os, sys
from collections import defaultdict
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import ConvexHull

DS, SRC, LOGO, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
SIZE, SS = 2000, 3                      # final pixels (the plate picture prints 178 mm wide: 285 dpi), supersampling
BG = np.array([11, 13, 18]) / 255       # the book's figure ground #0b0d12
GOLD = "#d4af37"
EDGE = np.array([0x1d, 0x20, 0x27]) / 255
LW = 2.2                                # edge width in final pixels
FCOL = {3: "#efe9dc", 4: "#9fb4c8", 5: "#c8504a", 6: "#d9a441", 7: "#7fae7a", 8: "#8b78c4", 9: "#4fa3a5", 10: "#d07fb0"}
LIGHT = np.array([-0.45, 0.55, 0.70]); LIGHT /= np.linalg.norm(LIGHT)
rgb = lambda h: np.array(matplotlib.colors.to_rgb(h))


def view(elev, azim):
    """rotation taking world coordinates to camera (x right, y up, z towards the viewer), as matplotlib's view_init."""
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), np.sin(a), 0], [-np.sin(a), np.cos(a), 0], [0, 0, 1]])
    # after Rz: look along -x' ... use a camera whose forward axis is the world direction (cos e cos a, cos e sin a, sin e)
    f = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    up0 = np.array([0, 0, 1.0])
    r = np.cross(up0, f); r /= np.linalg.norm(r)
    u = np.cross(f, r)
    return np.array([r, u, f])


def render(polys, cols, edges, R, path, fill=0.86, front=None):
    """polys: list of (k,3) arrays (planar, any orientation); cols: rgb per poly; edges: list of (2,3) arrays; front: number of
    leading polys (the shell shown) that win depth ties with the rest (faces shared with the inner shells)."""
    N = SIZE * SS
    allp = np.vstack(polys) @ R.T
    c = (allp.max(0) + allp.min(0)) / 2
    ext = max(allp[:, 0].max() - allp[:, 0].min(), allp[:, 1].max() - allp[:, 1].min()) / 2
    sc = fill * N / 2 / ext
    def scr(P):
        Q = (P @ R.T - c)
        return np.column_stack([N / 2 + Q[:, 0] * sc, N / 2 - Q[:, 1] * sc, Q[:, 2] * sc])
    Z = np.full((N, N), -np.inf, np.float32); ID = np.full((N, N), -1, np.int32)
    shade = []
    for k, P in enumerate(polys):
        Q = P @ R.T
        n = np.cross(Q[1] - Q[0], Q[2] - Q[0])
        for i in range(2, len(Q) - 1):          # a robust normal for polygons with a near-degenerate first triangle
            m = np.cross(Q[i] - Q[0], Q[i + 1] - Q[0])
            if np.linalg.norm(m) > np.linalg.norm(n): n = m
        n /= np.linalg.norm(n)
        if n[2] < 0: n = -n                     # two-sided: light the side facing the viewer
        d = max(0.0, float(n @ LIGHT))
        s = 0.34 + 0.58 * d + 0.18 * d ** 12      # ambient + diffuse + a small highlight
        shade.append(np.clip(np.asarray(cols[k]) * s + 0.06 * d ** 12, 0, 1))
        S = scr(P)
        if front is not None and k < front: S[:, 2] += 2.0   # depth bias, supersampled pixels
        for i in range(1, len(S) - 1):           # fan triangles
            A, B, C = S[0], S[i], S[i + 1]
            x0, x1 = int(max(0, np.floor(min(A[0], B[0], C[0])))), int(min(N - 1, np.ceil(max(A[0], B[0], C[0]))))
            y0, y1 = int(max(0, np.floor(min(A[1], B[1], C[1])))), int(min(N - 1, np.ceil(max(A[1], B[1], C[1]))))
            if x1 < x0 or y1 < y0: continue
            den = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
            if abs(den) < 1e-9: continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l1 = ((B[1] - C[1]) * (X - C[0]) + (C[0] - B[0]) * (Y - C[1])) / den
            l2 = ((C[1] - A[1]) * (X - C[0]) + (A[0] - C[0]) * (Y - C[1])) / den
            l3 = 1 - l1 - l2
            m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
            z = l1 * A[2] + l2 * B[2] + l3 * C[2]
            zb = Z[y0:y1 + 1, x0:x1 + 1]; ib = ID[y0:y1 + 1, x0:x1 + 1]
            w = m & (z > zb)
            zb[w] = z[w]; ib[w] = k
    img = np.empty((N, N, 3), np.float32); img[:] = BG
    SH = np.array(shade)
    hit = ID >= 0
    img[hit] = SH[ID[hit]]
    # edges: sampled densely, kept where they are not behind a face, stamped as discs
    rad = LW * SS / 2; eps = 0.004 * N
    off = [(dx, dy) for dx in range(-int(np.ceil(rad)), int(np.ceil(rad)) + 1) for dy in range(-int(np.ceil(rad)), int(np.ceil(rad)) + 1)
           if dx * dx + dy * dy <= rad * rad]
    pts = []
    for E in edges:
        S = scr(np.asarray(E, float))
        L = np.hypot(*(S[1, :2] - S[0, :2])); n = max(2, int(L / 0.5))
        t = np.linspace(0, 1, n)[:, None]
        pts.append(S[0] * (1 - t) + S[1] * t)
    if pts:
        P = np.vstack(pts)
        xi = np.clip(P[:, 0].astype(int), 0, N - 1); yi = np.clip(P[:, 1].astype(int), 0, N - 1)
        # visible if no face is clearly in front, looking at the pixel and its neighbours (silhouettes)
        zmin = Z[yi, xi]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            zmin = np.minimum(zmin, Z[np.clip(yi + dy, 0, N - 1), np.clip(xi + dx, 0, N - 1)])
        vis = (P[:, 2] >= zmin - eps) | ~np.isfinite(zmin)
        xi, yi = xi[vis], yi[vis]
        M = np.zeros((N, N), bool)
        for dx, dy in off:
            M[np.clip(yi + dy, 0, N - 1), np.clip(xi + dx, 0, N - 1)] = True
        img[M] = EDGE
    im = Image.fromarray((img * 255).round().astype(np.uint8)).resize((SIZE, SIZE), Image.LANCZOS)
    logo = Image.open(LOGO).convert("RGBA"); w = int(SIZE * 0.07)
    logo = logo.resize((w, w), Image.LANCZOS)
    im = im.convert("RGBA"); im.alpha_composite(logo, (SIZE - w - int(SIZE * 0.025), SIZE - w - int(SIZE * 0.025)))
    im.convert("RGB").save(path, optimize=True)


def faces_of(d):
    V = np.array([[float(x) for x in v["decimal"]] for v in d["vertices"]])
    return V, d["faces"]


facts = {"slices": [], "shells": [], "layers": []}

# ---- 1. slices
INDEX = {r["dataset_file"]: r for r in csv.DictReader(l for l in open(os.path.join(DS, "index.csv")) if not l.startswith("#"))}
SLICES = ["lion", "jabberwock", "tweedledum", "tweedledee", "mad-hatter", "march-hare", "jubjub", "alicia", "alice", "white-rabbit",
          "humpty-dumpty", "unicorn", "bandersnatch", "haigha", "hatta", "red-king", "walrus", "red-knight", "white-knight"]
for slug in SLICES:
    f = f"solids/dicto-{slug}.json"; d = json.load(open(os.path.join(DS, f))); row = INDEX[f]
    V, F = faces_of(d); V = V - V.mean(0)
    # check: the face counts drawn are the dataset's
    by = defaultdict(int)
    for fc in F: by[str(len(fc))] += 1
    assert dict(by) == {k: v for k, v in d["faces_by_sides"].items()}, slug
    assert len(V) == d["f_vector"]["vertices"] and len(F) == d["f_vector"]["faces"]
    polys = [V[fc] for fc in F]; cols = [rgb(FCOL[len(fc)]) for fc in F]
    edges = {tuple(sorted((fc[i], fc[(i + 1) % len(fc)]))) for fc in F for i in range(len(fc))}
    assert len(edges) == d["f_vector"]["edges"]
    render(polys, cols, [V[list(e)] for e in edges], view(22, 32), os.path.join(OUT, f"slice-{slug}.png"))
    facts["slices"].append({"slug": slug, "file": f, "name": d["name"], "D": row["universal_number"], "paper": row["paper"],
                            "doi": row["dicto_doi"], "note": row["prior_art_or_note"], "status": row["status"],
                            "f_vector": d["f_vector"], "faces_by_sides": d["faces_by_sides"], "symmetry": d["symmetry"],
                            "convex": d["convex"], "scale_note": d["scale_note"], "volume": d["volume"]})
    print("slice", slug, flush=True)

# ---- 2. the White Queen's Cleo shells
S = json.load(open(SRC)); V4 = np.array(S["vertices"], float); cells = S["cells"]
v = V4[0]; dh = v / np.linalg.norm(v)                         # v = (2, 0, 0, 0)
B = np.linalg.svd(np.eye(4) - np.outer(dh, dh))[0][:, :3]
h = V4 @ dh                                                   # heights along v (v at +2)
EYE = -2.1
P3 = np.array([(x - (x @ dh) * dh) @ B / (hx - EYE) for x, hx in zip(V4, h)])
cent = [round(float(np.mean(h[c])), 9) for c in cells]
keys = sorted(set(cent), reverse=True)
SH = [[c for c, k in zip(cells, cent) if k == key] for key in keys]
assert len(SH) == 15 and sum(map(len, SH)) == 600
COL = plt.cm.viridis(np.linspace(0.15, 0.95, len(SH)))[:, :3]
TRI = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
INNER = rgb("#5b606c")
# one view for all fifteen: off a five-fold axis of the core (towards one of the 12 corners round v)
nb = [i for i in range(120) if abs(np.linalg.norm(V4[i] - v) - (5 ** 0.5 - 1)) < 1e-6]
assert len(nb) == 12
ax5 = P3[nb[0]] / np.linalg.norm(P3[nb[0]])
def frame_from(axis, tilt_deg, spin_deg):
    a = axis / np.linalg.norm(axis)
    t = np.cross(a, [0.3, 0.5, 0.8]); t /= np.linalg.norm(t)
    tl = np.radians(tilt_deg); fwd = np.cos(tl) * a + np.sin(tl) * t
    up0 = np.cross(fwd, t); up0 /= np.linalg.norm(up0)
    sp = np.radians(spin_deg)
    r = np.cross(up0, fwd); r /= np.linalg.norm(r); u = np.cross(fwd, r)
    r, u = np.cos(sp) * r + np.sin(sp) * u, -np.sin(sp) * r + np.cos(sp) * u
    return np.array([r, u, fwd])
RW = frame_from(ax5, 21, 0)
def tet_edges(c): return [P3[[c[i], c[j]]] for i in range(4) for j in range(i + 1, 4)]
for k in range(15):
    polys, cols, edges = [], [], []
    col = rgb(GOLD) if k == 0 else COL[k]
    for c in SH[k]:
        for t in TRI: polys.append(P3[[c[i] for i in t]]); cols.append(col)
        edges += tet_edges(c)
    for j in range(k):
        for c in SH[j]:
            for t in TRI: polys.append(P3[[c[i] for i in t]]); cols.append(INNER)
            edges += tet_edges(c)
    nf = 4 * len(SH[k])
    render(polys, cols, edges, RW, os.path.join(OUT, f"wq-shell-{k:02d}.png"), front=nf)
    facts["shells"].append({"shell": k, "cells": len(SH[k]), "so_far": sum(len(s) for s in SH[:k + 1]), "centre_height": keys[k]})
    print("shell", k, len(SH[k]), flush=True)

# ---- 3. the Red Queen's cell layers
R4 = np.array([V4[c].mean(0) for c in cells])                # her corners: the White Queen's cell centres
cov = defaultdict(list)
for ci, c in enumerate(cells):
    for i in c: cov[i].append(ci)
RC = [cov[i] for i in range(120)]                             # her cells: the 20 corners round each White Queen vertex
assert all(len(c) == 20 for c in RC)
hR = R4 @ dh; he = hR.min() * 21 / 20
PR = np.array([(p - (p @ dh) * dh) @ B / ((p @ dh) - he) for p in R4])
hc = V4 @ dh; levels = sorted(set(np.round(hc, 9)), reverse=True)
L = [[i for i in range(120) if abs(hc[i] - lv) < 1e-7] for lv in levels]
assert [len(x) for x in L] == [1, 12, 20, 12, 30, 12, 20, 12, 1]
e2 = min(np.sum((R4[a] - R4[b]) ** 2) for a in RC[0] for b in RC[0] if a != b)
def dodeca(cell):
    """the 12 pentagons of one Red Queen cell (faces of the hull of its projected corners, coplanar triangles merged)."""
    pts = PR[cell]; H = ConvexHull(pts); groups = defaultdict(set)
    for simp, eq in zip(H.simplices, H.equations):
        groups[tuple(np.round(eq, 6))].update(int(t) for t in simp)
    out = []
    for key, vs in groups.items():
        vs = list(vs); n = np.array(key[:3]); cc = pts[vs].mean(0)
        u = pts[vs[0]] - cc; u /= np.linalg.norm(u); w = np.cross(n, u)
        vs.sort(key=lambda t: np.arctan2((pts[t] - cc) @ w, (pts[t] - cc) @ u))
        out.append(pts[vs])
    assert len(out) == 12 and all(len(f) == 5 for f in out)
    return out
def cell_edges(c): return [PR[[a, b]] for k, a in enumerate(c) for b in c[k + 1:] if abs(np.sum((R4[a] - R4[b]) ** 2) - e2) < 1e-7]
COLR = plt.cm.viridis(np.linspace(0.15, 0.95, len(L)))[:, :3]
core5 = PR[RC[L[1][0]]].mean(0)                              # a neighbour cell of the core: its direction is a 5-fold axis
RR = frame_from(core5, 21, 0)
for k in range(9):
    polys, cols, edges = [], [], []
    col = rgb(GOLD) if k == 0 else COLR[k]
    for i in L[k]:
        for f in dodeca(RC[i]): polys.append(f); cols.append(col)
        ce = cell_edges(RC[i]); assert len(ce) == 30; edges += ce
    for j in range(k):
        for i in L[j]:
            for f in dodeca(RC[i]): polys.append(f); cols.append(INNER)
            edges += cell_edges(RC[i])
    render(polys, cols, edges, RR, os.path.join(OUT, f"rq-layer-{k}.png"), front=12 * len(L[k]))
    facts["layers"].append({"layer": k, "cells": len(L[k]), "so_far": sum(len(x) for x in L[:k + 1]), "centre_height": float(levels[k])})
    print("layer", k, len(L[k]), flush=True)

json.dump(facts, open(os.path.join(OUT, "plates.json"), "w"), indent=1, ensure_ascii=False)
print("done")
