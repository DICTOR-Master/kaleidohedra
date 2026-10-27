"""The White Queen 600-cell: every slice of the 600-cell at a vertex layer, from the centre out to the tip, in its
four main directions (vertex-, edge-, face-, cell-first). Ivory faces on the dark background; the two slices with an
exact equilateral form named in #62 are ringed in gold (Shadow-17, Slice-48).
Run on dicto-big-brother after shadows.py:  ~/geom/bin/python scripts/render_white_queen.py
"""
import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

from render import BG, GOLD, mark

IVORY, EDGE = "#efe9dc", "#8f96a3"
ROWS = ["vertex-first", "edge-first", "face-first", "cell-first"]
TIP = {"vertex-first": 1, "edge-first": 2, "face-first": 3}       # the tip of the 600-cell in each direction
NAMED = {("edge-first", 17): "Shadow-17", ("cell-first", 48): "Slice-48"}


def hval(h):
    """numeric value of a height string such as '3/2 + 1/2√5'."""
    s = h.replace(" ", "").replace("-√5", "-1√5").replace("+√5", "+1√5")
    s = "1√5" if s == "√5" else s
    s = s.replace("√5", "*5**.5")
    return float(eval(s.replace("/", "/")))


NICE = {"-1 + √5": "√5 − 1", "-1/2 + 1/2√5": "(√5 − 1)/2", "-1/3 + 1/3√5": "(√5 − 1)/3"}
R = 1.75           # one scale for every panel, so the slices shrink towards the tip as they do in the 600-cell


def panel(ax, P, F, title, sub, named=None):
    ax.set_facecolor(BG)
    ax.set_axis_off()
    c = P.mean(0) if len(P) else np.zeros(3)
    P = P - c
    if len(F):
        ax.add_collection3d(Poly3DCollection([P[f] for f in F], facecolor=IVORY, edgecolor=EDGE,
                                             linewidths=0.35, alpha=0.82))
    else:
        if len(P) > 1:
            segs = [[P[i], P[j]] for i in range(len(P)) for j in range(i + 1, len(P))]
            ax.add_collection3d(Line3DCollection(segs, colors=IVORY, linewidths=1.6))
        ax.scatter(*P.T, color=IVORY, s=14)
    r = R
    for set_lim in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        set_lim(-r, r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(18, 32)
    col = GOLD if named else "white"
    ax.set_title(title + (f"\n{named}" if named else ""), color=col, fontsize=7.5, pad=-2)
    ax.text2D(0.5, -0.02, sub, transform=ax.transAxes, color="#aab0bb", fontsize=6, ha="center", va="top")


def main():
    S = pickle.load(open("data/solids.pkl", "rb"))
    rows = {d: [] for d in ROWS}
    for s in S:
        it = s["item"]
        if it["polytope"] == "600-cell" and it["kind"] == "slice" and hval(it["height"]) >= -1e-9:
            rows[it["direction"]].append((hval(it["height"]), it["height"], np.array(s["fV"]), s["faces"], it))
    ncol = max(len(v) + (d in TIP) for d, v in rows.items())
    plt.rcParams["figure.facecolor"] = BG
    fig = plt.figure(figsize=(2.05 * ncol, 2.35 * 4 + 1.2))
    for r, d in enumerate(ROWS):
        items = sorted(rows[d], key=lambda t: t[0])
        for c, (hv, h, P, F, it) in enumerate(items):
            ax = fig.add_subplot(4, ncol, r * ncol + c + 1, projection="3d")
            panel(ax, P, F, f"height {NICE.get(h, h)}", f"{it['V']} vertices · {it['F']} " + ("triangles" if it["all_triangles"] else "faces"),
                  NAMED.get((d, it["V"])))
        if d in TIP:
            ax = fig.add_subplot(4, ncol, r * ncol + len(items) + 1, projection="3d")
            n = TIP[d]
            e = (5 ** .5 - 1) / 2   # half the edge of this 600-cell (circumradius 2, edge √5 − 1)
            tip = {1: np.zeros((1, 3)), 2: np.array([[-e, 0, 0], [e, 0, 0]]),
                   3: np.array([[0, 2 * e / 3 ** .5, 0], [-e, -e / 3 ** .5, 0], [e, -e / 3 ** .5, 0]])}[n]
            panel(ax, tip, [], "tip", {1: "a vertex", 2: "an edge", 3: "a triangle"}[n])
        fig.text(0.008, 1 - (r + 0.55) / 4 * 0.86 - 0.07, d, color=GOLD, fontsize=10, rotation=90, va="center")
    fig.suptitle("The White Queen 600-cell: every slice at a vertex layer, from the centre out to the tip",
                 color="white", fontsize=13, y=0.985)
    fig.text(0.5, 0.955, "four directions · one scale throughout · exact coordinates in a + b√5 · heights with the tip at 1 + √5 · the far half mirrors the near half",
             color="#aab0bb", fontsize=8.5, ha="center")
    fig.subplots_adjust(left=0.03, right=0.99, top=0.93, bottom=0.02, wspace=0.02, hspace=0.25)
    mark(fig)
    fig.savefig("renders/white-queen-600.png", dpi=140, facecolor=BG)
    print("renders/white-queen-600.png", {d: len(v) for d, v in rows.items()})


if __name__ == "__main__":
    main()
