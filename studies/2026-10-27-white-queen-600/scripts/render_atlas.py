"""The White Queen 600-cell (#63): pictures of the atlas (atlas600.py) and of the shadows.
renders/atlas600.png : every slice type, centre to tip, in four directions; vertex-height slices and the slices between
                       them alternate; triangles ivory, squares silver-blue; one scale throughout.
renders/shadows600.png: the four shadows, and Humpty Dumpty (Slice-48) beside its slice.
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python render_atlas.py
"""
import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

from classify import signed_volume
from render import BG, GOLD, draw, find, mark

IVORY, SILVER, EDGE = "#efe9dc", "#9fb4c8", "#7f8692"
ROWS = ["vertex-first", "edge-first", "face-first", "cell-first"]
NAMED = {("edge-first", "1 + √5"): "Shadow-17", ("cell-first", "1 + 1/2√5"): "Humpty Dumpty"}
R = 1.75


def panel(ax, P, F, title, sub, named=None, at_layer=True):
    ax.set_facecolor(BG); ax.set_axis_off()
    P = np.asarray(P, float); P = P - P.mean(0)
    if len(F):
        polys = [P[f] for f in F]
        cols = [IVORY if len(f) == 3 else SILVER for f in F]
        ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolor=EDGE, linewidths=0.3, alpha=0.85))
    else:
        if len(P) > 1:
            ax.add_collection3d(Line3DCollection([[P[i], P[j]] for i in range(len(P)) for j in range(i + 1, len(P))],
                                                 colors=IVORY, linewidths=1.6))
        ax.scatter(*P.T, color=IVORY, s=12)
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-R, R)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 32)
    col = GOLD if named else ("white" if at_layer else "#9fb4c8")
    ax.set_title(title + (f"\n{named}" if named else ""), color=col, fontsize=6.5, pad=-4)
    ax.text2D(0.5, 0.0, sub, transform=ax.transAxes, color="#aab0bb", fontsize=5.2, ha="center", va="top")


def tip_points(o):
    e = (5 ** .5 - 1) / 2
    return {0: np.zeros((1, 3)), 1: np.array([[-e, 0, 0], [e, 0, 0]]),
            2: np.array([[0, 2 * e / 3 ** .5, 0], [-e, -e / 3 ** .5, 0], [e, -e / 3 ** .5, 0]])}[o["dim"]]


def atlas():
    A = pickle.load(open("../data/atlas600.pkl", "rb"))
    import json
    J = json.load(open("../data/atlas600.json"))
    ncol = max(sum(1 for o in J if o["direction"] == d) for d in ROWS)
    plt.rcParams["figure.facecolor"] = BG
    fig = plt.figure(figsize=(1.55 * ncol, 1.9 * 4 + 1.3))
    for r, d in enumerate(ROWS):
        items = sorted([o for o in J if o["direction"] == d], key=lambda o: o["h"])
        for c, o in enumerate(items):
            ax = fig.add_subplot(4, ncol, r * ncol + c + 1, projection="3d")
            lay = "at a vertex height" if o["at_vertex_layer"] else "between"
            if "dim" in o:
                panel(ax, tip_points(o), [], "tip", {0: "a vertex", 1: "an edge", 2: "a triangle"}[o["dim"]])
                continue
            k = next(a for a in A if a["item"]["direction"] == d and a["item"]["height"] == o["height"])
            fs = o["face_sizes"]
            sub = f"{o['V']} v · {fs.get('3', 0)} tri" + (f" · {fs['4']} sq" if fs.get("4") else "")
            panel(ax, k["fV"], k["faces"], o["height"], sub, NAMED.get((d, o["height"])) if o["at_vertex_layer"] else None,
                  o["at_vertex_layer"])
        fig.text(0.006, 1 - (r + 0.5) / 4 * 0.87 - 0.075, d, color=GOLD, fontsize=10, rotation=90, va="center")
    fig.suptitle("The White Queen 600-cell: every slice, from the centre out to the tip", color="white", fontsize=14, y=0.988)
    fig.text(0.5, 0.958, "white labels: slices at a vertex height (all triangles where the pattern allows) · blue labels: the slice "
             "type that holds over the whole gap to the next height · triangles ivory, squares blue · one scale · exact in a + b√5 · "
             "the far half mirrors the near half", color="#aab0bb", fontsize=8, ha="center")
    fig.subplots_adjust(left=0.02, right=0.995, top=0.935, bottom=0.02, wspace=0.0, hspace=0.3)
    mark(fig)
    fig.savefig("../renders/atlas600.png", dpi=130, facecolor=BG)


def shadows():
    S = pickle.load(open("../data/solids.pkl", "rb"))
    plt.rcParams["figure.facecolor"] = BG
    fig = plt.figure(figsize=(18, 8.4))
    for c, d in enumerate(ROWS):
        P, F = find(S, "600-cell", d, "shadow")
        it = next(s["item"] for s in S if s["item"]["polytope"] == "600-cell" and s["item"]["direction"] == d and s["item"]["kind"] == "shadow")
        ax = fig.add_subplot(2, 4, c + 1, projection="3d")
        fs = it["face_sizes"]
        draw(ax, P, F, f"{d} shadow", f"{it['V']} vertices · " + " · ".join(f"{v} {'triangles' if k == '3' else k + '-gons'}" for k, v in sorted(fs.items())),
             face="#cfc6b2", view=(18, 32))
    P0, F0 = find(S, "600-cell", "cell-first", "slice", "-1 - 1/2√5")
    P = np.load("../data/form_V48_full_36.npy"); F = [list(f) for f in F0]
    if signed_volume(P, F) < 0:
        F = [f[::-1] for f in F]
    ax = fig.add_subplot(2, 4, 6, projection="3d")
    draw(ax, P0, F0, "cell-first slice, 48 vertices", "convex, edges unequal", face="#cfc6b2", view=(20, 35))
    ax = fig.add_subplot(2, 4, 7, projection="3d")
    draw(ax, P, F, "Humpty Dumpty", "the same 92 triangles, every edge equal\n(Slice-48 in #62)", face="#3d5f7f", view=(20, 35))
    fig.suptitle("The White Queen 600-cell: its four shadows, and Humpty Dumpty put back together", color="white", fontsize=14)
    mark(fig)
    fig.savefig("../renders/shadows600.png", dpi=130, facecolor=BG)


if __name__ == "__main__":
    atlas()
    shadows()
