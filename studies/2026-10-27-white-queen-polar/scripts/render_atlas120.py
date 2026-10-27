"""Red Queen 120-cell, stage 3 pictures (as render_atlas.py of #63). Floats for drawing only; every count and shape is
proved exactly in atlas120.py (data/atlas120.json, .pkl).
renders/atlas120-page.png : every slice pattern, centre to tip, in four directions, one scale; faces coloured by their
                            number of sides; gold labels: slices that are uniform solids (checked exactly).
renders/shadows120.png    : the four shadows (pentagon faces red, faces that are side-on cells flattened gold) and,
                            below, the front half of each: the front cells, which tile the shadow once.
usage (dicto-big-brother):  cd scripts && nice ~/geom/bin/python render_atlas120.py
"""
import json
import os
import pickle
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

import atlas120 as A                       # the exact model (corners, cells, directions); loads in about a second
from shadows import Space
from render import BG, GOLD, mark

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data"); OUT = os.path.join(HERE, "..", "renders")
ROWS = list(A.DIRS)
ROWNAME = {"vertex-first": "vertex-first (corner)", "edge-first": "edge-first", "face-first": "face-first (pentagon)",
           "cell-first": "cell-first (dodecahedron)"}
FCOL = {3: "#efe9dc", 4: "#9fb4c8", 5: "#c8504a", 6: "#d9a441", 7: "#7fae7a", 8: "#8b78c4", 9: "#4fa3a5", 10: "#d07fb0"}
FNAME = {3: "triangles", 4: "four-sided", 5: "pentagons", 6: "hexagons", 7: "heptagons", 8: "octagons", 9: "enneagons",
         10: "decagons"}
EDGE = "#2a2d35"
RAD = 1.65                                  # one scale: the corners lie at radius ≈ 1.851
SHORT = {"rhombicosidodecahedron": "rhombicosidodeca.", "truncated icosahedron": "truncated icosa.",
         "truncated dodecahedron": "truncated dodeca.", "icosidodecahedron": "icosidodecahedron",
         "regular dodecahedron": "dodecahedron", "regular tetrahedron": "tetrahedron",
         "regular triangular prism": "triangular prism", "regular pentagonal prism": "pentagonal prism"}


def tip_points(dim):
    e = 0.5
    if dim == 0:
        return np.zeros((1, 3))
    if dim == 1:
        return np.array([[-e / 2, 0, 0], [e / 2, 0, 0]])
    r = e / (2 * np.sin(np.pi / 5))
    return np.array([[r * np.cos(2 * np.pi * k / 5 + np.pi / 2), 0, r * np.sin(2 * np.pi * k / 5 + np.pi / 2)] for k in range(5)])


def panel(ax, P, F, title, sub, named=None, at_layer=True, tipdim=None):
    ax.set_facecolor(BG); ax.set_axis_off()
    P = np.asarray(P, float); P = P - P.mean(0)
    if F:
        ax.add_collection3d(Poly3DCollection([P[f] for f in F], facecolors=[FCOL.get(len(f), "#ffffff") for f in F],
                                             edgecolor=EDGE, linewidths=0.25, alpha=0.9))
    else:
        if tipdim == 2:
            ax.add_collection3d(Poly3DCollection([P], facecolors=FCOL[5], edgecolor=EDGE, linewidths=0.4))
        elif len(P) > 1:
            ax.add_collection3d(Line3DCollection([P], colors="#efe9dc", linewidths=1.6))
        ax.scatter(*P.T, color="#efe9dc", s=8)
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-RAD, RAD)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 32)
    col = GOLD if named else ("white" if at_layer else "#9fb4c8")
    ax.set_title(title + (f"\n{named}" if named else ""), color=col, fontsize=6.2, pad=-4)
    ax.text2D(0.5, 0.0, sub, transform=ax.transAxes, color="#aab0bb", fontsize=4.3, ha="center", va="top")


def subline(o):
    fs = o["face_sizes"]
    return f"{o['V']} v · " + " ".join(f"{v}×{k}" for k, v in sorted(fs.items(), key=lambda kv: int(kv[0])))


def atlas_page(wrap=12):
    J = json.load(open(os.path.join(DATA, "atlas120.json")))["slices"]
    K = pickle.load(open(os.path.join(DATA, "atlas120.pkl"), "rb"))["slices"]
    lines = []
    for d in ROWS:
        items = sorted([o for o in J if o["direction"] == d], key=lambda o: o["h"])
        for i in range(0, len(items), wrap):
            lines.append((d if i == 0 else "", d, items[i:i + wrap]))
    plt.rcParams["figure.facecolor"] = BG
    fig = plt.figure(figsize=(1.2 * wrap, 1.42 * len(lines) + 1.0))
    for r, (label, d, items) in enumerate(lines):
        for c, o in enumerate(items):
            ax = fig.add_subplot(len(lines), wrap, r * wrap + c + 1, projection="3d")
            if "dim" in o:
                panel(ax, tip_points(o["dim"]), [], "tip", {0: "a corner", 1: "an edge", 2: "a pentagon"}[o["dim"]],
                      tipdim=o["dim"])
                continue
            k = next(a for a in K if a["item"]["direction"] == d and a["item"]["height"] == o["height"]
                     and a["item"]["at_vertex_layer"] == o["at_vertex_layer"])
            named = SHORT.get(o.get("uniform_solid")) if o.get("uniform_solid") else None
            panel(ax, k["fV"], k["faces"], o["height"], subline(o), named, o["at_vertex_layer"])
        if label:
            fig.text(0.004, 1 - (r + 0.5) / len(lines) * 0.93 - 0.045, ROWNAME[label], color=GOLD, fontsize=7.5,
                     rotation=90, va="center")
    # legend
    xs = np.linspace(0.08, 0.80, len(FCOL))
    for x, (n, col) in zip(xs, FCOL.items()):
        fig.patches.append(matplotlib.patches.Rectangle((x, 0.012), 0.012, 0.008, transform=fig.transFigure, color=col))
        fig.text(x + 0.016, 0.016, FNAME[n], color="#c8c8c8", fontsize=7, va="center")
    fig.text(0.5, 0.996, "The Red Queen 120-cell: every slice pattern, from the centre out to the tip", color="white",
             fontsize=12, ha="center", va="top")
    fig.text(0.5, 0.981, "white labels: at a corner height · blue labels: the pattern over the whole gap to the next height "
             "(cut at mid-gap) · gold: a uniform solid (exact) · one scale · heights exact in a + b√5 · far half mirrors near half",
             color="#aab0bb", fontsize=7, ha="center", va="top")
    fig.subplots_adjust(left=0.025, right=0.998, top=0.965, bottom=0.03, wspace=0.0, hspace=0.34)
    mark(fig)
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "atlas120-page.png"), dpi=170, facecolor=BG)
    print("atlas120-page.png", len(lines), "rows")


def shade(P, F, base_cols, light=np.array([0.4, -0.5, 0.75])):
    light = light / np.linalg.norm(light); cols = []
    c0 = P.mean(0)
    for f, b in zip(F, base_cols):
        n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); n /= np.linalg.norm(n)
        if np.dot(n, P[f].mean(0) - c0) < 0:
            n = -n
        k = 0.35 + 0.65 * max(0.0, float(np.dot(n, light)))
        cols.append(tuple(np.clip(np.array(matplotlib.colors.to_rgb(b)) * k * 1.5, 0, 1)))
    return cols


def setup(ax, lim):
    ax.set_facecolor(BG); ax.set_axis_off()
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-lim, lim)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 32)


def shadows():
    J = json.load(open(os.path.join(DATA, "atlas120.json")))["shadows"]
    K = pickle.load(open(os.path.join(DATA, "atlas120.pkl"), "rb"))["shadows"]
    plt.rcParams["figure.facecolor"] = BG
    fig = plt.figure(figsize=(18, 9.2))
    kind_cmap = plt.cm.tab10
    for c, d in enumerate(ROWS):
        it, k = J[d], K[d]
        P = np.array(k["fV"]); F = k["faces"]
        cen = P.mean(0); P = P - cen
        lim = np.abs(P).max() * 1.02
        ax = fig.add_subplot(2, 4, c + 1, projection="3d"); setup(ax, lim)
        base = [FCOL[5] if len(f) == 5 else GOLD for f in F]
        ax.add_collection3d(Poly3DCollection([P[f] for f in F], facecolors=shade(P, F, base), edgecolors="#f2e6c8",
                                             linewidths=0.4))
        fs = it["face_sizes"]
        ax.set_title(f"{ROWNAME[d]} shadow", color="white", fontsize=11, pad=0)
        ax.text2D(0.5, 0.0, f"{it['V']} vertices · {it['E']} edges · {it['F']} faces: " +
                  " + ".join(f"{v} {FNAME.get(int(s), s + '-gons')}" for s, v in sorted(fs.items(), key=lambda kv: int(kv[0])))
                  + f"\n(gold = the {it['side_on']} side-on cells, flattened)", transform=ax.transAxes, color="#c8c8c8",
                  fontsize=8, ha="center", va="top")
        # the front half: the front cells, each a projected dodecahedron
        dv = A.DIRS[d][0]; sp = Space(4, dv, None)
        Y = np.array([[float(x) for x in sp.y(p)] for p in A.R]) * sp.mf - cen
        cs = [float(A.dot(A.W[i], dv)) for i in range(120)]
        front = [i for i in range(120) if cs[i] > 1e-12]
        lev = sorted({round(cs[i], 9) for i in front})
        ax = fig.add_subplot(2, 4, c + 5, projection="3d"); setup(ax, lim)
        polys, cols = [], []
        for i in front:
            col = plt.cm.viridis(0.15 + 0.8 * lev.index(round(cs[i], 9)) / max(1, len(lev) - 1))
            for p in A.CELL_PENTS[i]:
                polys.append(Y[p]); cols.append(col)
        ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors="#f2e6c8", linewidths=0.18, alpha=0.18))
        ax.set_title(f"front half: {it['front']} cells", color="white", fontsize=10, pad=0)
        ax.text2D(0.5, 0.0, f"they fill the shadow exactly once, and so do the {it['back']} back cells\n"
                  f"(exact volume) · {it['front_kinds']} kinds of front piece · colour = depth", transform=ax.transAxes,
                  color="#c8c8c8", fontsize=8, ha="center", va="top")
    fig.suptitle("The Red Queen 120-cell: its four shadows, and the front half of each", color="white", fontsize=14)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.06, wspace=0.02, hspace=0.18)
    mark(fig)
    fig.savefig(os.path.join(OUT, "shadows120.png"), dpi=130, facecolor=BG)
    print("shadows120.png")


if __name__ == "__main__":
    atlas_page()
    shadows()
