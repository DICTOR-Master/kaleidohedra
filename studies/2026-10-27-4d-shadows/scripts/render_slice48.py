"""Render: the 600-cell cell-first slice with 48 vertices (convex, unequal edges) beside its equilateral form
Slice-48 (placeholder name), two views of the form.  Dark background, gold DICTO mark.
Run on dicto-big-brother:  ~/geom/bin/python render_slice48.py
"""
import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from classify import signed_volume
from render import BG, draw, find, mark


def main():
    S = pickle.load(open("data/solids.pkl", "rb"))
    P0, F0 = find(S, "600-cell", "cell-first", "slice", "-1 - 1/2√5")
    P = np.load("data/form_V48_full_36.npy")
    F = [list(f) for f in F0]
    if signed_volume(P, F) < 0:
        F = [f[::-1] for f in F]
    plt.rcParams["figure.facecolor"] = BG
    fig = plt.figure(figsize=(15, 5.6))
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    draw(ax, P0, F0, "600-cell slice, 48 vertices", "convex, 92 triangles, degrees 8^12 5^36\n"
         "edge ratio (5+√5)/2 = 3.618", face="#8a5a2b", view=(20, 35))
    ax = fig.add_subplot(1, 3, 2, projection="3d")
    draw(ax, P, F, "Slice-48 (placeholder name)", "same pattern, all 138 edges equal; Td symmetry\n"
         "non-convex, dihedrals 81.75°–243.20°", face="#3d5f7f", view=(20, 35))
    ax = fig.add_subplot(1, 3, 3, projection="3d")
    draw(ax, P, F, "Slice-48, second view", "nearest non-adjacent parts 0.069 apart\n"
         "(edge 1); embedding checked exactly", face="#3d5f7f", view=(35.26, 45))
    fig.suptitle("The one large 600-cell slice pattern with a symmetric equilateral (deltahedral) form",
                 color="white", fontsize=12)
    mark(fig)
    fig.savefig("renders/slice48.png", dpi=150, facecolor=BG)


if __name__ == "__main__":
    main()
