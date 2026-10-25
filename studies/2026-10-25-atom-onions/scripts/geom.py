# Atom onions: render geometry (floats, from the closed forms that onions_exact.py proves). Writes ../data/raw/scene-*.json for
# blender_render.py and ../data/raw/slices.json for compose.py. App units: golden L = phi (icosahedron edge 1), Delian octet edge 1.
#   onion scenes: one atom, its stop shells (translucent, coloured, with edges) and faint in-between shells, quarter cut open
#     (the wedge x > 0, y > 0 removed); on the two cut half-planes the sections: opaque pastel bands between the stop shells and
#     rings (the stop shells' outlines); a label anchor for every stop shell.
#   meshing scenes: the cells of both kinds at one stop round a site, cut by the plane x = y (the half x - y > 0 removed); the cut
#     face shows every cut cell's onion (bands and rings up to its own shell at the stop).
#   slices: the exact plane section x = y of the whole filling at the stop, every cell with its onion (for the flat panel).
import json, os, itertools
import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "../data/raw")
PHI = (1 + 5 ** 0.5) / 2; R2 = 2 ** -0.5

# ---------------- shells ----------------
def golden_T(sv):  # signed permutations of (1, s, 0) * phi/2
    P = set()
    for p in set(itertools.permutations((1.0, sv, 0.0))):
        for g in itertools.product((1, -1), repeat=3): P.add(tuple(round(a * b * PHI / 2, 12) + 0.0 for a, b in zip(p, g)))
    return np.array(sorted(P))
def tet_shell(t):  # krp-core tetPiece about its site, / sqrt2
    q = np.array([.5] * 3); C = [np.array(c, float) for c in itertools.product((0, 1), repeat=3)]
    even = [c for c in C if sum(c) % 2 == 0]; odd = [c for c in C if sum(c) % 2 == 1]
    if t <= 0: return np.zeros((1, 3))
    if t <= 1 / 3: P = [q + 3 * t * (v - q) for v in even]
    else:
        a = 1.5 * (1 - t); P = even + [o + a * (v - o) for o in odd for v in even if abs(np.linalg.norm(v - o) - 1) < 1e-9]
    return (np.array(P) - q) * R2
def oct_shell(t):  # krp-core octPiece about its site, / sqrt2
    if t >= 1: return np.zeros((1, 3))
    E = np.eye(3); c = np.zeros(3)
    if t >= 1 / 3: a = 1.5 * (1 - t); P = [g * a * e for e in E for g in (1, -1)]
    else:
        P = [g * e for e in E for g in (1, -1)]
        for sg in itertools.product((-1, 1), repeat=3):
            q = np.array(sg) / 2
            for i in range(3):
                v = np.zeros(3); v[i] = sg[i]; P.append(q + 3 * t * (v - q))
    return np.array(P) * R2

def polytope(P):
    """convex polytope from points: unique vertices, faces (ordered loops, outward), planes (n, b) with n.p <= b"""
    P = np.unique(np.round(P, 10), axis=0)
    if len(P) < 4: return {"V": P, "F": [], "H": []}
    h = ConvexHull(P); groups = {}
    for simp, eq in zip(h.simplices, h.equations):
        key = tuple(np.round(eq, 7)); groups.setdefault(key, set()).update(simp.tolist())
    F, H = [], []
    for key, idx in groups.items():
        n = np.array(key[:3]); b = -key[3]; idx = list(idx); Q = P[idx]; c = Q.mean(0)
        u = Q[0] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        ang = np.arctan2((Q - c) @ v, (Q - c) @ u); F.append([idx[k] for k in np.argsort(ang)]); H.append((n, b))
    return {"V": P, "F": F, "H": H}

def section(poly, n0, b0):
    """polygon of the polytope cut by the plane n0.p = b0 (ordered points), or [] """
    V, F = poly["V"], poly["F"]
    if not F: return []
    pts = []
    E = set()
    for f in F:
        for k in range(len(f)): E.add(tuple(sorted((f[k], f[(k + 1) % len(f)]))))
    for i, j in E:
        a, b = V[i] @ n0 - b0, V[j] @ n0 - b0
        if abs(a) < 1e-12: pts.append(V[i])
        if abs(b) < 1e-12: pts.append(V[j])
        if a * b < 0: pts.append(V[i] + (V[j] - V[i]) * a / (a - b))
    if len(pts) < 3: return []
    pts = np.unique(np.round(np.array(pts), 10), axis=0)
    c = pts.mean(0); u = pts[0] - c
    if np.linalg.norm(u) < 1e-12: return []
    u /= np.linalg.norm(u); v = np.cross(n0, u)
    ang = np.arctan2((pts - c) @ v, (pts - c) @ u); pts = pts[np.argsort(ang)]
    # drop collinear points
    keep = [p for k, p in enumerate(pts) if np.linalg.norm(np.cross(pts[k - 1] - p, pts[(k + 1) % len(pts)] - p)) > 1e-10]
    return np.array(keep) if len(keep) >= 3 else []

def clip(poly, n, b):  # keep n.p <= b (Sutherland-Hodgman)
    out = []
    for k in range(len(poly)):
        P, Q = poly[k], poly[(k + 1) % len(poly)]
        dp, dq = P @ n - b, Q @ n - b
        if dp <= 1e-12: out.append(P)
        if dp * dq < 0: out.append(P + (Q - P) * dp / (dp - dq))
    return out

def hexcol(h): return [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
def pastel(h, k=0.5): c = np.array(hexcol(h)); return list(c + (1 - c) * k)
def dark(h, k=0.45): return list(np.array(hexcol(h)) * (1 - k))

# ---------------- the onions ----------------
GOLD = {"oct": "#8e6cc9", "ua": "#e8913f", "kelvin": "#35aebf", "icosaxes": "#56a866", "cubo": "#7f93a8"}
GS = [("oct", 0.0), ("ua", 1 / PHI ** 2), ("kelvin", 0.5), ("icosaxes", 1 / PHI), ("cubo", 1.0)]          # golden T(y) by s(y) = y/(1+y)
GFAINT = [0.12, 0.25, 0.44, 0.56, 0.75, 0.88]
DCOL = {"eqa": "#2e8b9a", "octet": "#c0392b", "half": "#8e6cc9", "samson": "#d9a33a", "delilah": "#3f6fb0", "eqb": "#7a9a2e", "rd": "#8fa3b8", "cube": "#8a8f98"}
TB = 1 - (2 / 3) * 2 ** (-1 / 3)
DST = [("eqa", (2 * 6 ** .5 - 3) / 15), ("octet", 1 / 3), ("half", 1 - 6 ** (1 / 3) / 3), ("bond", TB), ("eqb", 5 / 3 - (2 / 3) * 2 ** .5)]
TET_SHELLS = [("eqa", DST[0][1]), ("octet", 1 / 3), ("half", DST[2][1]), ("samson", TB), ("eqb", DST[4][1]), ("cube", 1.0)]
OCT_SHELLS = [("eqb", DST[4][1]), ("delilah", TB), ("half", DST[2][1]), ("octet", 1 / 3), ("eqa", DST[0][1]), ("rd", 0.0)]
TFAINT = [0.06, 0.2, 0.27, 0.6, 0.86, 0.94]; OFAINT = [0.94, 0.86, 0.6, 0.27, 0.2, 0.06]

def onion_shells(kind):
    """inside-out list of (key, colour, points, stop?)"""
    if kind == "golden":
        S = [(k, GOLD[k], golden_T(sv), True, sv) for k, sv in GS] + [(None, "#9aa0a6", golden_T(sv), False, sv) for sv in GFAINT]
        return sorted(S, key=lambda r: r[4])
    if kind == "tet":
        S = [(k, DCOL[k], tet_shell(tv), True, tv) for k, tv in TET_SHELLS] + [(None, "#9aa0a6", tet_shell(tv), False, tv) for tv in TFAINT]
        return sorted(S, key=lambda r: r[4])
    S = [(k, DCOL[k], oct_shell(tv), True, 1 - tv) for k, tv in OCT_SHELLS] + [(None, "#9aa0a6", oct_shell(tv), False, 1 - tv) for tv in OFAINT]
    return sorted(S, key=lambda r: r[4])

def tri_fan(loop):
    return [[loop[0], loop[k], loop[k + 1]] for k in range(1, len(loop) - 1)]

def add_mesh(objs, name, polys, col, alpha, kind="surface", rough=0.35):
    V, Fs = [], []
    for loop in polys:
        if len(loop) < 3: continue
        b = len(V); V += [list(map(float, p)) for p in loop]; Fs.append(list(range(b, b + len(loop))))
    if Fs: objs.append({"type": "mesh", "name": name, "V": V, "F": Fs, "col": col, "alpha": alpha, "kind": kind, "rough": rough})

def add_tubes(objs, name, lines, col, r):
    L = [[list(map(float, p)) for p in l] for l in lines if len(l) >= 2]
    if L: objs.append({"type": "tubes", "name": name, "lines": L, "col": col, "r": r})

def onion_scene(kind, fname, cam_dir, anchor_dir):
    shells = onion_shells(kind); objs, anchors = [], []
    # the wedge {x > |y|} (round the +x axis) is removed; kept = {x - y <= 0} U {x - y >= 0, x + y <= 0}; cut half-planes:
    # A = {x = y, x + y >= 0} (outward normal nA) and B = {x = -y, x - y >= 0} (outward normal nB). Diagonal planes: they contain the
    # body diagonals, the normals of the moving (unlike-bond) faces, so the sections show the shells apart.
    nA = np.array([1., -1, 0]) / 2 ** .5; nB = np.array([1., 1, 0]) / 2 ** .5
    cuts = [(nA, nB), (nB, nA)]  # (plane normal = outward, in-plane keep direction >= 0)
    nst = 0; size = 0; NSTOP = sum(1 for r in shells if r[3]) + 1
    for idx, (key, col, P, stop, prm) in enumerate(shells):
        poly = polytope(P); V = poly["V"]; size = max(size, np.linalg.norm(V, axis=1).max())
        if not poly["F"]:  # a point
            objs.append({"type": "sphere", "name": f"point", "c": [0, 0, 0], "r": 0.022 * (1.2 if kind != "golden" else 1.5), "col": dark("#555555", 0)}); continue
        faces = [V[f] for f in poly["F"]]
        kept = []
        for f in faces:
            kept.append(clip(list(f), nA, 0.0))
            g = clip(list(f), -nA, 0.0); kept.append(clip(g, nB, 0.0))
        kept = [k for k in kept if len(k) >= 3]
        if stop:
            add_mesh(objs, f"shell-{key}", kept, hexcol(col), 0.22, "surface")
            # edges of the kept faces that are true polytope edges (not cut lines)
            E = []
            for f in poly["F"]:
                for k in range(len(f)):
                    a, b = V[f[k]], V[f[(k + 1) % len(f)]]
                    E.append((a, b))
            segs = []
            for a, b in {(tuple(a), tuple(b)) if tuple(a) < tuple(b) else (tuple(b), tuple(a)) for a, b in E}:
                a, b = np.array(a), np.array(b)
                ts = np.linspace(0, 1, 2)
                # split the segment where it enters the wedge
                pts = [a + (b - a) * w for w in np.linspace(0, 1, 41)]
                cur = []
                for p in pts:
                    inw = p @ nA > 1e-9 and p @ nB > 1e-9
                    if not inw: cur.append(p)
                    elif cur: segs.append(cur); cur = []
                if len(cur) >= 2: segs.append(cur)
            segs = [[s_[0], s_[-1]] for s_ in segs if np.linalg.norm(s_[-1] - s_[0]) > 1e-6]
            add_tubes(objs, f"edges-{key}", segs, dark(col, 0.35), 0.0045 * size / 1.0)
            nst += 1
        else:
            add_mesh(objs, f"faint-{idx}", kept, [0.6, 0.62, 0.65], 0.035, "surface")
        # sections on the two cut half-planes
        for ci, (n0, keepdir) in enumerate(cuts):
            sec = section(poly, n0, 0.0)
            if len(sec) == 0: continue
            half = clip(list(sec), -keepdir, 0.0)  # keep keepdir.p >= 0
            if len(half) < 3: continue
            # polyline without the segment on the wedge axis (keepdir.p = 0)
            H = np.array(half); on = np.abs(H @ keepdir) < 1e-9
            m = len(H); start = next(k for k in range(m) if on[k] and not on[(k + 1) % m])
            line = [H[(start + k) % m] for k in range(m + 1)]
            while len(line) > 2 and abs(line[-1] @ keepdir) < 1e-9 and abs(line[-2] @ keepdir) < 1e-9: line.pop()
            if stop:
                layer = NSTOP - nst  # inner shells on top (nearer the camera)
                add_mesh(objs, f"band-{key}-{ci}", [list(np.array(half) + n0 * 0.0007 * layer)], pastel(col, 0.45), 1.0, "band", rough=0.8)
                add_tubes(objs, f"ring-{key}-{ci}", [[p + n0 * 0.012 for p in line]], dark(col, 0.25), 0.007 * size)
            else:
                add_tubes(objs, f"fring-{idx}-{ci}", [[p + n0 * 0.011 for p in line]], [0.55, 0.57, 0.6], 0.0028 * size)
        if stop:
            d = np.array(anchor_dir, float); d /= np.linalg.norm(d)
            rr = min((b / (n @ d) for n, b in poly["H"] if n @ d > 1e-12), default=0)
            anchors.append({"key": key, "p": list(map(float, d * rr + np.array([0, 0.013, 0])))})
    if kind in ("tet", "oct"):  # the site itself: the tet atom at t = 0, the oct atom at t = 1
        objs.append({"type": "sphere", "name": "point", "c": [0, 0, 0], "r": 0.025 * size, "col": [0.25, 0.25, 0.25]})
        anchors.insert(0, {"key": "point", "p": [0, 0, 0]})
    scene = {"objs": objs, "anchors": anchors, "cam_dir": cam_dir, "size": float(size), "target": [0, 0, 0], "zoom": 2.15}
    json.dump(scene, open(os.path.join(OUT, fname), "w"))
    return scene

# ---------------- meshing at a stop ----------------
def sites(loop, R, centre):
    out = []
    rng = range(-4, 5)
    for m in itertools.product(rng, repeat=3):
        m = np.array(m, float)
        if loop == "golden":
            cand = [("big", m * PHI), ("small", (m + .5) * PHI)]
        else:
            cand = [("tet", (m + .5) * R2)] + ([("oct", m * R2)] if int(m.sum()) % 2 else [])
        par = int(m.sum()) % 2  # the cube's parity: in odd cubes the tetrahedron piece is mirrored (krp-core tetPiece)
        for k, c in cand:
            if np.linalg.norm(c - centre) <= R: out.append((k, c, par))
    return out

def cell_onion(loop, kind, stop_prm, par=0):
    """the onion of an atom of `kind` up to its shell at the meshing stop: list of (key, colour, points) inside out (stop shells only),
    plus faint shells"""
    if loop == "golden":
        sv = stop_prm if kind == "big" else 1 - stop_prm
        S = [(k, GOLD[k], golden_T(v), True) for k, v in GS if v <= sv + 1e-12] + [(None, "#9aa0a6", golden_T(v), False) for v in GFAINT if v < sv]
        S.sort(key=lambda r: len(r[2]) and np.abs(r[2]).max()); return S
    if kind == "tet":
        M = np.array([-1.0 if par else 1.0, 1.0, 1.0])
        S = [(k, DCOL[k], tet_shell(v) * M, True) for k, v in TET_SHELLS if v <= stop_prm + 1e-12] + [(None, "#9aa0a6", tet_shell(v) * M, False) for v in TFAINT if v < stop_prm]
    else:
        S = [(k, DCOL[k], oct_shell(v), True) for k, v in OCT_SHELLS if v >= stop_prm - 1e-12] + [(None, "#9aa0a6", oct_shell(v), False) for v in OFAINT if v > stop_prm]
    S.sort(key=lambda r: np.abs(r[2]).max()); return S

KINDCOL = {"big": GOLD["icosaxes"], "small": GOLD["ua"], "tet": DCOL["samson"], "oct": DCOL["delilah"]}
def meshing_scene(loop, stop_prm, centre, R, fname, cam_dir):
    n0 = np.array([1., -1, 0]) / 2 ** .5  # removed half: n0.(p - centre) > 0
    b0 = n0 @ centre
    objs = []; size = 0
    for kind, c, par in sites(loop, R, centre):
        S = cell_onion(loop, kind, stop_prm, par)
        outer = polytope(S[-1][2] + c); V = outer["V"]
        if (V @ n0 - b0).min() > -1e-9: continue  # entirely in the removed half
        size = max(size, np.linalg.norm(V - centre, axis=1).max())
        kept = [clip(list(V[f]), n0, b0) for f in outer["F"]]
        add_mesh(objs, f"cell-{kind}", kept, hexcol(KINDCOL[kind]), 1.0, "solid", rough=0.5)
        E = []
        for f in outer["F"]:
            for k in range(len(f)):
                a, b = V[f[k]], V[f[(k + 1) % len(f)]]
                da, db = a @ n0 - b0, b @ n0 - b0
                if da > 1e-9 and db > 1e-9: continue
                if da > 1e-9: a = a + (b - a) * da / (da - db)
                if db > 1e-9: b = b + (a - b) * db / (db - da)
                E.append([a, b])
        add_tubes(objs, f"cedges-{kind}", E, dark(KINDCOL[kind], 0.55), 0.006)
        if abs(c @ n0 - b0) > 1e-9: continue  # site off the cut plane: its cut face (if any) is just its outer section
        nst = 0
        for key, col, P, stop in S:
            poly = polytope(P + c)
            if not poly["F"]:
                objs.append({"type": "sphere", "name": "point", "c": list(map(float, c)), "r": 0.02, "col": [0.3, 0.3, 0.3]}); continue
            sec = section(poly, n0, b0)
            if len(sec) == 0: continue
            if stop:
                nst += 1
                add_mesh(objs, f"band-{key}", [list(np.array(sec) + n0 * 0.0008 * (len(S) + 1 - nst))], pastel(col, 0.4), 1.0, "band", rough=0.8)
                add_tubes(objs, f"ring-{key}", [list(np.array(sec) + n0 * 0.012)] , dark(col, 0.25), 0.0065)
            else:
                add_tubes(objs, "fring", [list(np.array(sec) + n0 * 0.011)], [0.55, 0.57, 0.6], 0.0025)
    # close the polylines of rings
    for o in objs:
        if o["type"] == "tubes" and (o["name"].startswith("ring") or o["name"] == "fring"):
            o["lines"] = [l + [l[0]] for l in o["lines"]]
    scene = {"objs": objs, "anchors": [], "cam_dir": cam_dir, "size": float(size), "target": list(map(float, centre))}
    json.dump(scene, open(os.path.join(OUT, fname), "w"))

# ---------------- the flat slice x = y ----------------
def slice_data(loop, stop_prm, centre, half_w, half_h):
    n0 = np.array([1., -1, 0]) / 2 ** .5; e1 = np.array([1., 1, 0]) / 2 ** .5; e2 = np.array([0., 0, 1])
    cells = []
    for kind, c, par in sites(loop, 6, centre):
        if abs(c @ n0) > 1e-9: continue
        uv = np.array([(c - centre) @ e1, (c - centre) @ e2])
        if abs(uv[0]) > half_w + 1.2 or abs(uv[1]) > half_h + 1.2: continue
        rings = []
        for key, col, P, stop in cell_onion(loop, kind, stop_prm, par):
            poly = polytope(P + c)
            if not poly["F"]: rings.append({"key": "point", "pts": [list(uv)], "stop": True}); continue
            sec = section(poly, n0, 0.0)
            if len(sec) == 0: continue
            rings.append({"key": key, "col": col, "stop": stop, "pts": [[float((p - centre) @ e1), float((p - centre) @ e2)] for p in sec]})
        cells.append({"kind": kind, "uv": list(map(float, uv)), "rings": rings})
    return {"cells": cells, "half_w": half_w, "half_h": half_h}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cam = [1.0, 0.18, 0.62]; anch = [1.0, -1.0, -1.32]  # in cut half-plane B, across a moving face, square to the view
    onion_scene("golden", "scene-golden-onion.json", cam, anch)
    onion_scene("tet", "scene-delian-tet-onion.json", cam, anch)
    onion_scene("oct", "scene-delian-oct-onion.json", cam, anch)
    meshing_scene("golden", 1 / PHI, np.zeros(3), 1.02 * PHI, "scene-golden-meshing.json", [1.0, -1.0, 0.75])
    cD = np.array([0, 0, 1.0]) * R2
    meshing_scene("delian", TB, cD, 1.25, "scene-delian-meshing.json", [1.0, -1.0, 0.75])
    sl = {"golden": slice_data("golden", 1 / PHI, np.zeros(3), 1.5 * PHI, 1.0 * PHI), "delian": slice_data("delian", TB, cD, 1.6, 1.1),
          "colours": {"golden": GOLD, "delian": DCOL, "kinds": KINDCOL}}
    json.dump(sl, open(os.path.join(OUT, "slices.json"), "w"))
    for f in sorted(os.listdir(OUT)):
        if f.startswith("scene"): d = json.load(open(os.path.join(OUT, f))); print(f, len(d["objs"]), "objects, size", round(d["size"], 3), "anchors", [a["key"] for a in d["anchors"]])
    print("slices:", {k: len(v["cells"]) for k, v in sl.items() if k != "colours"})
