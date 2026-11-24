#!/usr/bin/env python3
"""Figures for "The Vacuus and the Resonus" in the manner of Leonardo's drawings for Pacioli's De divina proportione (1509):
the solid as an empty frame of shaded wooden struts on a parchment ground, the planes as hatched washes. Geometry exact
(corners in Q(sqrt5) as floats only for drawing; every plane and edge is chosen by exact tests in pacioli.py / the catalogue).

Figure 5 (Proposition 1, the golden rectangles): left, the icosahedron with its three golden rectangles in x = 0, y = 0, z = 0
(each rectangle's two short sides are edges of the icosahedron); right, the 15 rectangles as 5 triples of mutually perpendicular
planes, one small icosahedron per triple.
Run with a venv that has numpy + matplotlib:  python scripts/leonardo.py [outdir]"""
import sys, os, itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "../renders")
PHI = (1 + 5 ** 0.5) / 2
PAPER = "#efe2c4"; INK = "#4a2f17"; WOOD = "#c79c5e"; WOOD_BACK = "#dcc39a"; WASH = "#9c6b35"

def ico():
    V = []
    for a, b in itertools.product((1, -1), repeat=2):
        for v in ((0, a, b * PHI), (a, b * PHI, 0), (b * PHI, 0, a)):
            V.append(np.array(v, float))
    E = [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(np.linalg.norm(V[i] - V[j]) - 2) < 1e-9]
    assert len(V) == 12 and len(E) == 30
    return V, E

def rot(yaw, pitch):
    cy, sy, cp, sp_ = np.cos(yaw), np.sin(yaw), np.cos(pitch), np.sin(pitch)
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]); Rx = np.array([[1, 0, 0], [0, cp, -sp_], [0, sp_, cp]])
    return Rx @ Ry

def best_view(V, E, normals=(), tries=4000, seed=3):
    """yaw, pitch whose projection keeps every corner well clear of every other corner and of every strut not at it,
    and shows every given plane open (its normal at least 35 degrees from the picture plane, none face-on)"""
    rng = np.random.default_rng(seed); best = (-1, None)
    for _ in range(tries):
        yaw, pitch = rng.uniform(0, np.pi), rng.uniform(0.15, 0.6)
        M = rot(yaw, pitch); P = [(M @ v)[:2] for v in V]
        if normals and not all(0.4 < abs((M @ n)[2]) / np.linalg.norm(n) < 0.8 for n in normals): continue
        g = min(np.linalg.norm(P[i] - P[j]) for i, j in itertools.combinations(range(len(P)), 2))
        for i, j in E:
            a, b = P[i], P[j]; d = b - a
            for k, p in enumerate(P):
                if k in (i, j): continue
                t = np.clip((p - a) @ d / (d @ d), 0, 1); g = min(g, np.linalg.norm(a + t * d - p))
        if g > best[0]: best = (g, (yaw, pitch))
    return best[1], best[0]

def rectangles(V, E):
    """the 15 golden rectangles: an edge and its opposite edge (corners negated)"""
    key = {tuple(np.round(v, 9)): i for i, v in enumerate(V)}
    seen, out = set(), []
    for i, j in E:
        a, b = key[tuple(np.round(-V[i], 9))], key[tuple(np.round(-V[j], 9))]
        k = frozenset((i, j, a, b))
        if k in seen: continue
        seen.add(k); out.append([i, j, a, b])          # i-j and a-b are the short sides (edges); j-a, b-i the long sides
    assert len(out) == 15
    for r in out:
        p = [V[t] for t in r]
        assert abs(np.linalg.norm(p[0] - p[1]) - 2) < 1e-9 and abs(np.linalg.norm(p[1] - p[2]) - 2 * PHI) < 1e-9
    return out

def triples(V, R):
    n = [np.cross(V[r[0]], V[r[1]]) for r in R]; n = [x / np.linalg.norm(x) for x in n]
    T = [t for t in itertools.combinations(range(15), 3) if all(abs(n[a] @ n[b]) < 1e-9 for a, b in itertools.combinations(t, 2))]
    assert len(T) == 5 and sorted(sum(T, ())) == list(range(15))
    return T

def draw(ax, V, E, rects, M, scale=1.0, off=(0, 0), lw=1.0, joints=None):
    P = [M @ v for v in V]
    xy = lambda p: (off[0] + scale * p[0], off[1] + scale * p[1])
    items = []
    for k, r in enumerate(rects):
        q = [P[t] for t in r]
        items.append((np.mean([x[2] for x in q]), "rect", (q, ("#b5823f", "#8f5f2c", "#d2a868")[k % 3])))
    for i, j in E:
        items.append(((P[i][2] + P[j][2]) / 2, "edge", (P[i], P[j])))
    zs = [z for z, _, _ in items]; zmin, zmax = min(zs), max(zs)
    for z, kind, g in sorted(items, key=lambda t: t[0]):
        t = (z - zmin) / (zmax - zmin + 1e-12)              # 0 back, 1 front
        if kind == "rect":
            g, tone = g
            poly = [xy(p) for p in g]
            ax.add_patch(Polygon(poly, closed=True, facecolor=tone, alpha=0.42, edgecolor="none", zorder=1 + z))
            ax.add_patch(Polygon(poly, closed=True, facecolor="none", edgecolor=INK, linewidth=0.6 * lw, alpha=0.6, zorder=1 + z))
        else:
            (x1, y1), (x2, y2) = xy(g[0]), xy(g[1])
            back = (g[0][2] + g[1][2]) / 2 < -1e-9
            if back:   # struts behind the centre: a thin pale line, as Leonardo's hidden bars
                ax.plot([x1, x2], [y1, y2], color=INK, lw=0.9 * lw * scale ** 0.5 * 2, alpha=0.5, zorder=1 + z + 0.5, solid_capstyle="round")
                continue
            w = (5.0 + 2.5 * t) * lw * scale ** 0.5
            ax.plot([x1, x2], [y1, y2], color=INK, lw=w + 1.6 * lw, solid_capstyle="round", zorder=1 + z, alpha=0.55 + 0.45 * t)
            ax.plot([x1, x2], [y1, y2], color=WOOD if t > 0.45 else WOOD_BACK, lw=w, solid_capstyle="round", zorder=1 + z + 1e-3)
    for k, p in enumerate(P):  # joints (front half only; corners of the solid only)
        if p[2] < -1e-9 or (joints is not None and k not in joints): continue
        x, y = xy(p); t = (p[2] - zmin) / (zmax - zmin + 1e-12)
        ax.plot(x, y, "o", ms=(4 + 3 * t) * lw * scale ** 0.5, mfc=WOOD, mec=INK, mew=0.8 * lw, zorder=1 + p[2] + 5e-3)

def parchment(fig):
    ax = fig.add_axes([0, 0, 1, 1], zorder=-10); ax.axis("off")
    yy, xx = np.mgrid[-1:1:400j, -1:1:800j]
    r = np.sqrt(xx ** 2 * 0.6 + yy ** 2)
    base = np.array(matplotlib.colors.to_rgb(PAPER))
    rng = np.random.default_rng(7)
    img = base[None, None, :] * (1 - 0.10 * r[..., None] ** 2) + 0.015 * rng.standard_normal((400, 800, 1))
    ax.imshow(np.clip(img, 0, 1), extent=[0, 1, 0, 1], aspect="auto")

def fig_pacioli(out):
    V, E = ico(); R = rectangles(V, E); T = triples(V, R)
    axes = [i for i, r in enumerate(R) if sum(abs(np.cross(V[r[0]], V[r[1]])) > 1e-9) == 1]   # normals along x, y, z
    assert len(axes) == 3 and any(set(axes) == set(t) for t in T)
    fig = plt.figure(figsize=(12, 6), dpi=200); parchment(fig)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 2.0); ax.set_ylim(0, 1.0); ax.set_aspect("equal"); ax.axis("off")
    (yaw, pitch), gap = best_view(V, E, normals=[np.cross(V[R[i][0]], V[R[i][1]]) for i in axes])
    print(f"view yaw {yaw:.3f} pitch {pitch:.3f}, smallest projected gap {gap:.3f} (edge 2)")
    M = rot(yaw, pitch)
    draw(ax, V, E, [R[i] for i in axes], M, scale=0.215, off=(0.52, 0.52), lw=1.25)
    small = [(1.22, 0.70), (1.52, 0.70), (1.82, 0.70), (1.37, 0.30), (1.67, 0.30)]
    for t, o in zip(T, small):
        draw(ax, V, E, [R[i] for i in t], M, scale=0.068, off=o, lw=0.75)
    fig.savefig(out, dpi=200)
    print("wrote", out)


# ---------------------------------------------------------------- the other three figures
def solid_edges(V, L):
    E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[i] - V[j]) - L) < 1e-9]
    return E

def poly_order(V, idx, n):
    """corners idx of a planar polygon with normal n, in cyclic order"""
    c = np.mean([V[i] for i in idx], axis=0); u = V[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    return sorted(idx, key=lambda i: np.arctan2((V[i] - c) @ w, (V[i] - c) @ u))

def fig_dual(out):
    """Theorem D: the octahedron's Vacuus (3 square sheets) and the cube's Resonus (3 middle squares) are the same 3 planes"""
    Vo = [np.array(v, float) for k in range(3) for s in (1, -1) for v in [tuple(s if t == k else 0 for t in range(3))]]
    Eo = solid_edges(Vo, 2 ** 0.5); assert len(Eo) == 12
    Vc = [np.array(v, float) for v in itertools.product((1, -1), repeat=3)]
    Ec = solid_edges(Vc, 2.0); assert len(Ec) == 12
    N = [np.eye(3)[k] for k in range(3)]
    # octahedron: each square sheet = the 4 corners in the plane x_k = 0, and its 4 edges lie in it (a full sheet)
    So = [poly_order(Vo, [i for i, v in enumerate(Vo) if abs(v[k]) < 1e-9], N[k]) for k in range(3)]
    for k, sq in enumerate(So):
        assert sum(1 for i, j in Eo if i in sq and j in sq) == 4
    # cube: the middle square of the plane x_k = 0 (corners = midpoints of the 4 edges parallel to e_k)
    Vc2 = list(Vc); Sc = []
    for k in range(3):
        mids = [(Vc[i] + Vc[j]) / 2 for i, j in Ec if abs(abs((Vc[i] - Vc[j])[k]) - 2) < 1e-9]
        assert len(mids) == 4
        idx = list(range(len(Vc2), len(Vc2) + 4)); Vc2 += mids; Sc.append(poly_order(Vc2, idx, N[k]))
    fig = plt.figure(figsize=(12, 6), dpi=200); parchment(fig)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 2.0); ax.set_ylim(0, 1.0); ax.set_aspect("equal"); ax.axis("off")
    (yaw, pitch), gap = best_view(Vc, Ec, normals=N)
    print(f"dual view yaw {yaw:.3f} pitch {pitch:.3f}, gap {gap:.3f}")
    M = rot(yaw, pitch)
    draw(ax, Vo, Eo, So, M, scale=0.33, off=(0.50, 0.50), lw=1.25)
    draw(ax, Vc2, Ec, Sc, M, scale=0.23, off=(1.50, 0.50), lw=1.25, joints=range(8))
    fig.savefig(out, dpi=200); print("wrote", out)

def prism(n):
    c = [np.array([np.cos(2 * np.pi * j / n), np.sin(2 * np.pi * j / n)]) for j in range(n)]
    e = np.linalg.norm(c[1] - c[0])
    V = [np.array([p[0], p[1], s * e / 2]) for s in (1, -1) for p in c]
    E = solid_edges(V, e); assert len(E) == 3 * n
    return V, E, e

def fig_prisms(out):
    """Proposition B1: the hexagonal prism's 3 planes that are both a Vacuus plate (through 2 opposite upright edges) and a
    Resonus plane (parallel to 2 opposite squares); the octagonal prism, where the two kinds of plane miss each other"""
    fig = plt.figure(figsize=(12, 6), dpi=200); parchment(fig)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 2.0); ax.set_ylim(0, 1.0); ax.set_aspect("equal"); ax.axis("off")
    for n, off in ((6, (0.50, 0.50)), (8, (1.50, 0.50))):
        V, E, e = prism(n)
        up = [(j, j + n) for j in range(n)]                                    # upright edges
        plates = [poly_order(V, [j, j + n, j + n // 2, j + n // 2 + n], np.cross(V[j], V[j + n])) for j in range(n // 2)]
        sq_norm = [np.array([np.cos(np.pi * (2 * k + 1) / n), np.sin(np.pi * (2 * k + 1) / n), 0]) for k in range(n // 2)]
        shared = [P for P in plates if any(np.linalg.norm(np.cross(np.cross(V[P[0]] - V[P[2]], V[P[1]] - V[P[2]]), m)) < 1e-9 for m in sq_norm)]
        assert len(shared) == (n // 2 if n % 4 == 2 else 0)
        if n == 6:
            show = shared
        else:   # one upright-edge plate and the Resonus plane of the squares next to it: different planes, 22.5 degrees apart
            m = sq_norm[0]; t = np.cross(m, [0, 0, 1]); r = np.linalg.norm(V[0][:2])
            res = [np.array([s1 * r * t[0], s1 * r * t[1], s2 * e / 2]) for s1, s2 in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
            V = V + res; show = [plates[0], list(range(2 * n, 2 * n + 4))]
        up_y = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)          # turn the prism axis upright in the picture
        yaw = {6: 0.30, 8: 0.25}[n]
        draw(ax, V, E, show, rot(yaw, 0.32) @ up_y, scale=0.27, off=off, lw=1.25, joints=range(2 * n))
    fig.savefig(out, dpi=200); print("wrote", out)

def fig_sphere(out):
    """Theorem C2: the Resonus on the sphere: cuboctahedron, 7 great circles, all 32 regions triangles (simplicial); icosidodecahedron,
    16 great circles, 140 triangles and 12 pentagons (not simplicial)"""
    co = [np.eye(3)[k] for k in range(3)] + [np.array(v, float) for v in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1))]
    ic = [np.array(v, float) for a in (1, -1) for v in ((0, 1, a * PHI), (1, a * PHI, 0), (a * PHI, 0, 1))]      # 6 five-fold axes
    ic += [np.array(v, float) for v in itertools.product((1, -1), (1, -1), (1,))] + \
          [np.array(v, float) for a in (1, -1) for v in ((0, a / PHI, PHI), (a / PHI, PHI, 0), (PHI, 0, a / PHI))]          # 10 three-fold axes
    assert len(co) == 7 and len(ic) == 16
    fig = plt.figure(figsize=(12, 6), dpi=200); parchment(fig)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 2.0); ax.set_ylim(0, 1.0); ax.set_aspect("equal"); ax.axis("off")
    M = rot(0.5, 0.42); R = 0.40
    for N, (cx, cy) in ((co, (0.5, 0.5)), (ic, (1.5, 0.5))):
        ax.add_patch(matplotlib.patches.Circle((cx, cy), R, facecolor="#e2cfa6", edgecolor=INK, lw=1.6, alpha=0.9, zorder=1))
        ax.add_patch(matplotlib.patches.Circle((cx - 0.12 * R, cy + 0.14 * R), 0.62 * R, facecolor="#f4e8cf", edgecolor="none", alpha=0.55, zorder=1.1))
        t = np.linspace(0, 2 * np.pi, 721)
        for n in N:
            n = n / np.linalg.norm(n); u = np.cross(n, [0.3, 0.5, 0.7]); u /= np.linalg.norm(u); w = np.cross(n, u)
            P = np.array([M @ (np.cos(a) * u + np.sin(a) * w) for a in t])
            front = P[:, 2] >= 0
            for mask, style in ((front, dict(color=INK, lw=1.5, alpha=0.95, zorder=3)), (~front, dict(color=INK, lw=0.6, alpha=0.30, zorder=2))):
                Q = np.where(mask[:, None], P, np.nan)
                ax.plot(cx + R * Q[:, 0], cy + R * Q[:, 1], **style)
    fig.savefig(out, dpi=200); print("wrote", out)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    made = []
    for f, name in ((fig_pacioli, "leonardo-fig5-golden-rectangles.png"), (fig_dual, "leonardo-fig6-octahedron-cube.png"),
                    (fig_prisms, "leonardo-fig7-prisms.png"), (fig_sphere, "leonardo-fig8-sphere.png")):
        out = os.path.join(OUT, name); f(out); made.append(os.path.getsize(out) > 0)
    print("FINAL ok" if len(made) == 4 and all(made) else "FINAL FAIL: a figure was not written")
