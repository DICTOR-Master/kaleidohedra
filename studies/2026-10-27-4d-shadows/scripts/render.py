"""Two renders (matplotlib, dark background, gold DICTO mark).
renders/variants.png   : 5-cell edge-first shadow vs regular J12; 16-cell edge-first shadow vs regular octahedron
renders/icosahedral.png: 600-cell vertex-first shadow vs its equilateral form (12-dented icosahedron);
                         600-cell vertex-first slice at height 2 vs its equilateral form (augmented dodecahedron)
Run on dicto-big-brother after shadows.py:  ~/geom/bin/python render.py
"""
import math
import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

BG = "#0b0d12"
GOLD = "#d4af37"
PHI = (1 + 5 ** 0.5) / 2
EDGE_COLS = ["#7fd4ff", "#ff9f5a", "#b48cff", "#7dff9a"]


def find(S, poly, direc, kind, height=None):
    for s in S:
        it = s["item"]
        if it["polytope"] == poly and it["direction"] == direc and it["kind"] == kind and \
                (height is None or it.get("height") == height):
            return np.array(s["fV"]), s["faces"]


def hull_faces(P):
    """faces of a convex hull, coplanar triangles merged (float, drawing only)."""
    H = ConvexHull(P)
    groups = {}
    for simp, eq in zip(H.simplices, H.equations):
        key = tuple(np.round(eq, 6))
        groups.setdefault(key, set()).update(int(t) for t in simp)
    faces = []
    for key, vs in groups.items():
        vs = list(vs)
        n = np.array(key[:3]); c = P[vs].mean(0)
        u = P[vs[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        vs.sort(key=lambda t: math.atan2(np.dot(P[t] - c, w), np.dot(P[t] - c, u)))
        faces.append(vs)
    return faces


def draw(ax, P, F, title, sub, face="#2f6f9f", alpha=0.55, view=(18, 30)):
    P = np.asarray(P, float)
    P = P - P.mean(0)
    P = P / np.abs(P).max()
    polys = [[P[v] for v in f] for f in F]
    base = np.array(matplotlib.colors.to_rgb(face))
    light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    cols = []
    for f in F:
        n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]])
        n = n / np.linalg.norm(n)
        if np.dot(n, np.mean([P[v] for v in f], 0)) < 0:
            n = -n
        k = 0.35 + 0.65 * max(0.0, float(np.dot(n, light)))
        cols.append(tuple(np.clip(base * k * 1.6, 0, 1)))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors="#f2e6c8", linewidths=0.6,
                                         alpha=1.0))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(*view)
    ax.set_axis_off()
    ax.set_facecolor(BG)
    ax.set_title(title, color="white", fontsize=11, pad=0)
    ax.text2D(0.5, 0.02, sub, transform=ax.transAxes, color="#c8c8c8", fontsize=8.5, ha="center", va="bottom")


def mark(fig):
    fig.text(0.985, 0.015, "DICTO", color=GOLD, fontsize=11, ha="right", va="bottom", fontweight="bold",
             family="serif")


def icosahedron(scale=1.0):
    P = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            for k in range(3):
                P.append(np.roll([0, s1, s2 * PHI], k))
    return np.array(P, float) * scale


def dodecahedron():
    P = [list(s) for s in np.array(np.meshgrid([1, -1], [1, -1], [1, -1])).T.reshape(-1, 3)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            for k in range(3):
                P.append(np.roll([0, s1 / PHI, s2 * PHI], k))
    return np.array(P, float)


def pyramids(P, F, sign):
    """replace each pentagon of (P, F) by an equilateral pentagonal pyramid, outward (+1) or inward (-1)."""
    P = [p for p in P]
    out = []
    for f in F:
        if len(f) == 3:
            out.append(f); continue
        c = np.mean([P[v] for v in f], 0)
        e = np.linalg.norm(P[f[0]] - P[f[1]])
        R = np.linalg.norm(P[f[0]] - c)
        h = math.sqrt(e * e - R * R)
        n = c / np.linalg.norm(c)
        P.append(c + sign * h * n)
        a = len(P) - 1
        for i in range(len(f)):
            out.append([f[i], f[(i + 1) % len(f)], a])
    return np.array(P), out


def main():
    S = pickle.load(open("data/solids.pkl", "rb"))
    plt.rcParams["figure.facecolor"] = BG
    # ---------------------------------------------------------------- render 1
    fig = plt.figure(figsize=(12, 9))
    P, F = find(S, "5-cell", "edge-first", "shadow")
    ax = fig.add_subplot(2, 2, 1, projection="3d")
    draw(ax, P, F, "5-cell edge-first shadow", "J12 pattern; edges √2 (3), √(7/6) (6); ratio √(12/7) = 1.309\n"
         "dihedrals 120° (base) and arccos(1/8) = 82.82°: three close round a base edge; no space filling",
         face="#8a5a2b", view=(12, 20))
    tri = np.array([[math.cos(2 * math.pi * k / 3), math.sin(2 * math.pi * k / 3), 0] for k in range(3)])
    h = math.sqrt(3) * math.sqrt(2 / 3)
    J12 = np.vstack([tri, [[0, 0, h], [0, 0, -h]]])
    ax = fig.add_subplot(2, 2, 2, projection="3d")
    draw(ax, J12, hull_faces(J12), "regular triangular bipyramid J12", "all edges equal; dihedrals 70.53°, 141.06°\n"
         "no edge star with itself alone; no space filling", face="#3d5f7f", view=(12, 20))
    P, F = find(S, "16-cell", "edge-first", "shadow")
    ax = fig.add_subplot(2, 2, 3, projection="3d")
    draw(ax, P, F, "16-cell edge-first shadow", "octahedron pattern; edges √2 (4), √(3/2) (8); ratio 2/√3 = 1.155\n"
         "two cube-centre pyramids: dihedrals 90°, 120°; fills space (square bipyramidal honeycomb)",
         face="#8a5a2b", view=(15, 35))
    O = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
    ax = fig.add_subplot(2, 2, 4, projection="3d")
    draw(ax, O, hull_faces(O), "regular octahedron", "dihedral arccos(−1/3) = 109.47°\n"
         "fills space only with tetrahedra (octet)", face="#3d5f7f", view=(15, 35))
    fig.suptitle("4D shadows with the face pattern of a convex deltahedron (gold-brown) and the regular one (blue)",
                 color="white", fontsize=12)
    mark(fig)
    fig.savefig("renders/variants.png", dpi=150, facecolor=BG)
    plt.close(fig)
    # ---------------------------------------------------------------- render 2
    fig = plt.figure(figsize=(12, 9))
    P, F = find(S, "600-cell", "vertex-first", "shadow")
    ax = fig.add_subplot(2, 2, 1, projection="3d")
    draw(ax, P, F, "600-cell vertex-first shadow", "convex, 80 triangles (pentakis icosidodecahedron pattern)\n"
         "edges 2/φ and √(9/2 − 3√5/2); ratio 2/√3 = 1.155", face="#8a5a2b")
    # equilateral form: icosidodecahedron (edge midpoints of an icosahedron) with 12 pyramids pushed in
    I = icosahedron()
    Ih = ConvexHull(I)
    edges = set()
    for s in Ih.simplices:
        for i in range(3):
            edges.add(tuple(sorted((int(s[i]), int(s[(i + 1) % 3])))))
    M = np.array([(I[a] + I[b]) / 2 for a, b in edges])
    Fm = hull_faces(M)
    Pd, Fd = pyramids(M, Fm, -1)
    ax = fig.add_subplot(2, 2, 2, projection="3d")
    draw(ax, Pd, Fd, "equilateral form: 12-dented icosahedron", "same pattern, all 120 edges equal; non-convex\n"
         "(pushed out the pyramids lie flat: the icosahedron of edge 2)", face="#3d5f7f")
    P, F = find(S, "600-cell", "vertex-first", "slice", "2")
    ax = fig.add_subplot(2, 2, 3, projection="3d")
    draw(ax, P, F, "600-cell slice at x·v = 2 (v a vertex)", "convex, 60 triangles (pentakis dodecahedron pattern)\n"
         "edges 2/φ and 2√(7 − 3√5); ratio 1.144", face="#8a5a2b")
    D = dodecahedron()
    Pa, Fa = pyramids(D, hull_faces(D), +1)
    ax = fig.add_subplot(2, 2, 4, projection="3d")
    draw(ax, Pa, Fa, "equilateral form: augmented dodecahedron", "same pattern, all 90 edges equal; non-convex\n"
         "(dodecahedron edges 191.32°; pushed in: dented dodecahedron)", face="#3d5f7f")
    fig.suptitle("600-cell shadow and slice (gold-brown) and the deltahedra with the same face pattern (blue)",
                 color="white", fontsize=12)
    mark(fig)
    fig.savefig("renders/icosahedral.png", dpi=150, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    main()
