"""Card picture for #62 on dictospheres.com (1440 x 1080): Shadow-17 (two J11 glued on their pentagons) and
Slice-48, the two equal-edged solids from the 600-cell. Run on dicto-big-brother:  ~/geom/bin/python scripts/render_card62.py
"""
import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

from classify import signed_volume
from render import BG, draw, find, mark, icosahedron


def shadow17():
    I = icosahedron()
    top = int(np.argmax(I[:, 2]))
    tri = [list(s) for s in ConvexHull(I).simplices]
    keep = [i for i in range(12) if i != top]
    ring = [i for i in keep if any(top in f and i in f for f in tri)]
    n = I[top] / np.linalg.norm(I[top])          # five-fold axis through the removed vertex
    z1 = I[ring[0]] @ n
    J = I[keep]
    idx = {v: k for k, v in enumerate(keep)}
    F1 = [[idx[a] for a in f] for f in tri if top not in f]
    # mirror the J11 through the plane of its pentagon; the pentagon's corners are shared
    M = J - 2 * np.outer(J @ n - z1, n)
    a = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); a /= np.linalg.norm(a); b = np.cross(n, a)
    rest = [k for k, v in enumerate(keep) if v not in ring]
    P = np.vstack([J, M[rest]])
    mi = {k: (k if keep[k] in ring else len(J) + rest.index(k)) for k in range(len(J))}
    F2 = [[mi[a] for a in f[::-1]] for f in F1]
    F = F1 + F2
    P = np.column_stack([P @ a, P @ b, P @ n])     # five-fold axis upright
    if signed_volume(P, F) < 0:
        F = [f[::-1] for f in F]
    return P, F


def main():
    S = pickle.load(open("../data/solids.pkl", "rb"))
    _, F0 = find(S, "600-cell", "cell-first", "slice", "-1 - 1/2√5")
    P48 = np.load("../data/form_V48_full_36.npy"); F48 = [list(f) for f in F0]
    if signed_volume(P48, F48) < 0:
        F48 = [f[::-1] for f in F48]
    P17, F17 = shadow17()
    plt.rcParams["figure.facecolor"] = BG
    fig = plt.figure(figsize=(9.6, 7.2))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    draw(ax, P17, F17, "Shadow-17", "two J11 glued on their pentagons\n17 vertices · 30 triangles", face="#b8862e", view=(8, 30))
    ax = fig.add_subplot(1, 2, 2, projection="3d")
    draw(ax, P48, F48, "Slice-48", "92 equal triangles · tetrahedral symmetry", face="#3d5f7f", view=(20, 35))
    fig.suptitle("Shadows of the Fourth Dimension: equal-edged solids from the 600-cell", color="white", fontsize=12, y=0.93)
    mark(fig)
    fig.savefig("../renders/card62.png", dpi=150, facecolor=BG)


if __name__ == "__main__":
    main()
