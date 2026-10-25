# Atom onions: compose the two figures (one per loop) from the Blender renders (../renders) and the exact slice data
# (../data/raw/slices.json): (a), (b) the two atoms' onions, quarter cut open, labelled stop shells; (c) the meshing at one stop
# (3D, cut by the plane x = y); (d) the same plane section, flat, every cell with its onion. DICTO mark in the corner.
# Output: ../figures/fig1-golden-onions.png, ../figures/fig2-delian-onions.png (and copies to ~/Documents/papers-to-read/atom-onions).
import json, os, shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
REN = os.path.join(ROOT, "renders"); FIG = os.path.join(ROOT, "figures"); READ = os.environ.get("ONION_READ", os.path.expanduser("~/Documents/papers-to-read/atom-onions"))
LOGO = os.environ.get("ONION_LOGO", os.path.expanduser("~/k-research/papers/dicto-logo.png"))
SL = json.load(open(os.path.join(ROOT, "data/raw/slices.json")))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13})

def hexcol(h): return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
def pastel(h, k=0.45): c = hexcol(h); return c + (1 - c) * k
def dark(h, k=0.3): return hexcol(h) * (1 - k)

def onion_panel(ax, name, labels, cols, title, sub):
    im = Image.open(os.path.join(REN, f"{name}.png")); W = im.size[0]
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    pr = json.load(open(os.path.join(REN, f"{name}.json")))
    ax.imshow(bg, extent=(0, W, W, 0)); ax.set_xlim(0, W * 1.78); ax.set_ylim(W * 1.0, 0); ax.axis("off")
    A = sorted(pr["anchors"], key=lambda a: a["y"]); n = len(A)
    ys = np.linspace(W * 0.08, W * 0.94, n)  # labels in the order of their anchors on the screen
    for a, y in zip(A, ys):
        k = a["key"]; c = dark(cols[k], 0.25) if k != "point" else np.array([.25, .25, .25])
        ax.plot([a["x"]], [a["y"]], "o", ms=5, color=c, mec="white", mew=0.8, zorder=5)
        ax.annotate("", xy=(a["x"], a["y"]), xytext=(W * 1.04, y), arrowprops=dict(arrowstyle="-", color=c, lw=1.0, alpha=0.85, shrinkA=0, shrinkB=3))
        if k != "point":
            ax.add_patch(plt.Rectangle((W * 1.045, y - W * 0.017), W * 0.034, W * 0.034, color=pastel(cols[k]), ec=c, lw=1.2))
        ax.text(W * 1.095, y, labels[k], va="center", ha="left", fontsize=12, color=c, linespacing=1.05)
    ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=4)
    ax.text(0, W * 0.995, sub, fontsize=11.5, color="#444", va="bottom")

def meshing_panel(ax, name, title, sub):
    im = Image.open(os.path.join(REN, f"{name}.png")); W = im.size[0]
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    ax.imshow(bg); ax.axis("off"); ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=4)
    ax.text(0, W * 0.995, sub, fontsize=11.5, color="#444", va="bottom")

def slice_panel(ax, loop, cols, kindcol, kindname, title, notes):
    D = SL[loop]; hw, hh = D["half_w"], D["half_h"]
    for cell in D["cells"]:
        R = cell["rings"]; stops = [r for r in R if r["stop"] and r["key"] != "point"]
        for r in reversed(stops):  # outer first, inner on top
            ax.add_patch(Polygon(r["pts"], closed=True, fc=pastel(r["col"]), ec=dark(r["col"], 0.25), lw=1.1, zorder=2))
        for r in R:
            if not r["stop"]: ax.add_patch(Polygon(r["pts"], closed=True, fill=False, ec="#9aa0a6", lw=0.5, zorder=3))
        if stops: ax.add_patch(Polygon(stops[-1]["pts"], closed=True, fill=False, ec="#222", lw=1.8, zorder=4))
        ax.plot(*cell["uv"], "o", ms=5.5, color=hexcol(kindcol[cell["kind"]]) * 0.8, mec="white", mew=0.9, zorder=6)
    ax.set_xlim(-hw, hw); ax.set_ylim(-hh, hh); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp_ in ax.spines.values(): sp_.set_color("#bbb")
    ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=4)
    for (txt, xy, xyt, kind) in notes:
        ax.annotate(txt, xy=xy, xytext=xyt, fontsize=12, color=hexcol(kindcol[kind]) * 0.6, fontweight="bold", zorder=8,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=hexcol(kindcol[kind]) * 0.7, lw=1.0, alpha=0.93),
                    arrowprops=dict(arrowstyle="-|>", color=hexcol(kindcol[kind]) * 0.6, lw=1.3))

def logo(fig):
    L = Image.open(LOGO); ax = fig.add_axes([0.945, 0.006, 0.045, 0.045]); ax.imshow(L); ax.axis("off")

def save(fig, fname):
    os.makedirs(FIG, exist_ok=True); os.makedirs(READ, exist_ok=True)
    p = os.path.join(FIG, fname); fig.savefig(p, dpi=200, facecolor="white"); plt.close(fig); shutil.copy(p, os.path.join(READ, fname))
    print(p, Image.open(p).size)

# ---------------- Figure 1: golden ----------------
G = SL["colours"]["golden"]; K = SL["colours"]["kinds"]
fig = plt.figure(figsize=(16, 15.6))
fig.suptitle("The onions of the golden atoms (DICTONIC golden loop, factor x)", x=0.02, ha="left", fontsize=21, fontweight="bold", y=0.985)
fig.text(0.02, 0.953, "Each atom's cells along the loop are nested shells: raising x grows every big atom and shrinks every small one. Both onions are the one family\n"
         "T(y), y from 0 to ∞ (paper #48, Theorem 4), read from opposite ends: the big atom at x holds T(y) for y ≤ x, the small atom T(y) for y ≤ 1/x.\n"
         "The square faces (like bonds) stay on the fixed cube planes; only the hexagons (big–small bonds) move.", fontsize=12.5, color="#333", va="top")
ax = fig.add_axes([0.01, 0.50, 0.49, 0.41])
onion_panel(ax, "golden-onion", {"oct": "x = 0: octahedron", "ua": "x = 1/τ: T(1/τ),\nthe Unborn Axes", "kelvin": "x = 1: Kelvin's\ntruncated octahedron",
            "icosaxes": "x = τ: Icosaxes\n(the golden bond)", "cubo": "x → ∞: cuboctahedron"}, G,
            "(a) Big atom (on φℤ³)", "weight up as x rises: x = 0 at the core, x → ∞ outside")
ax = fig.add_axes([0.505, 0.50, 0.49, 0.41])
onion_panel(ax, "golden-onion", {"oct": "x → ∞: octahedron", "ua": "x = τ: Unborn Axes\n(the golden bond)", "kelvin": "x = 1: Kelvin's\ntruncated octahedron",
            "icosaxes": "x = 1/τ: T(τ),\nthe Icosaxes", "cubo": "x → 0: cuboctahedron"}, G,
            "(b) Small atom (cube centres)", "weight up as x falls: x → ∞ core, x → 0 outside; same shells as (a)")
ax = fig.add_axes([0.02, 0.085, 0.44, 0.39])
meshing_panel(ax, "golden-meshing", "(c) Meshing at x = τ", "Icosaxes (green) + Unborn Axes (orange) fill space; cut by the plane x = y, each cut cell shows its onion")
ax = fig.add_axes([0.50, 0.10, 0.48, 0.36])
PHI = (1 + 5 ** .5) / 2
slice_panel(ax, "golden", G, K, None, "(d) The plane x = y at x = τ, flat",
            [("big atom = Icosaxes:\n4 stop shells: octahedron,\nUnborn Axes, Kelvin, Icosaxes", (0, 0), (-1.45 * PHI, 0.62 * PHI), "big"),
             ("small atom = Unborn Axes:\n2 stop shells: octahedron,\nUnborn Axes", (2 ** .5 * PHI / 2, PHI / 2), (0.55 * PHI, 0.66 * PHI), "small")])
fig.text(0.02, 0.03, "Thin grey lines: shells between the stops. Moving the slider from x to x' > x moves the slab between T(x) and T(x') across every hexagon from the small atom\n"
         "to the big one: the big onion gains a shell, the small onion loses the same volume (V_big + V_small = φ³).",
         fontsize=11.5, color="#333", va="top", ha="left")
logo(fig); save(fig, "fig1-golden-onions.png")

# ---------------- Figure 2: Delian ----------------
Dc = SL["colours"]["delian"]
fig = plt.figure(figsize=(16, 15.6))
fig.suptitle("The onions of the Delian atoms (DICTONIC Delian loop, cut t)", x=0.02, ha="left", fontsize=21, fontweight="bold", y=0.985)
fig.text(0.02, 0.953, "Raising t grows every tetrahedron atom (cube centres) and shrinks every octahedron atom (odd points). The two onions differ, and both\n"
         "change type at the octet (t = 1/3), the one flip of the loop: the tet onion turns from tetrahedra to cut cubes (tet–tet faces born),\n"
         "the oct onion from cut rhombic dodecahedra to octahedra (oct–oct faces die). Like-bond faces never move; only the triangles (tet–oct) move.", fontsize=12.5, color="#333", va="top")
ax = fig.add_axes([0.01, 0.50, 0.49, 0.41])
onion_panel(ax, "delian-tet-onion", {"point": "t = 0: a point (the site)", "eqa": "equilateral (a),\nt = (2√6 − 3)/15: tetrahedron",
            "octet": "t = 1/3: octet tetrahedron", "half": "half and half,\nt = 1 − ∛6/3: cut cube", "samson": "Delian bond: Samson",
            "eqb": "equilateral (b),\nt = 5/3 − (2/3)√2: cut cube", "cube": "t = 1: cube"}, Dc,
            "(a) Tetrahedron atom", "weight up as t rises: t = 0 at the core, t = 1 outside")
ax = fig.add_axes([0.505, 0.50, 0.49, 0.41])
onion_panel(ax, "delian-oct-onion", {"point": "t = 1: a point (the site)", "eqb": "equilateral (b): octahedron", "delilah": "Delian bond: Delilah",
            "half": "half and half: octahedron", "octet": "t = 1/3: octet octahedron", "eqa": "equilateral (a): rhombic\ndodecahedron, 8 corners cut",
            "rd": "t = 0: rhombic\ndodecahedron"}, Dc,
            "(b) Octahedron atom", "weight up as t falls: t = 1 at the core, t = 0 outside")
ax = fig.add_axes([0.02, 0.085, 0.44, 0.39])
meshing_panel(ax, "delian-meshing", "(c) Meshing at the Delian bond", "Samsons (gold) + Delilahs (blue) fill space; cut by the plane x = y, each cut cell shows its onion")
ax = fig.add_axes([0.50, 0.10, 0.48, 0.36])
slice_panel(ax, "delian", Dc, K, None, "(d) The plane x = y at the Delian bond, flat",
            [("tet atom = Samson:\n4 stop shells: tetrahedron (a),\noctet tetrahedron, half and half,\nSamson", (0.5, -0.5 / 2 ** .5), (0.12, -1.04), "tet"),
             ("oct atom = Delilah:\n2 stop shells: octahedron (b),\nDelilah", (0.0, 0.0), (-1.55, 0.62), "oct")])
fig.text(0.02, 0.03, "Thin grey lines: shells between the stops. Moving the slider from t to t' > t moves a slab across every triangle (tet–oct face) from the octahedron atom\n"
         "to the tetrahedron atom: one onion gains a shell, the other loses the same volume (8 V_tet + 4 V_oct = 8, tetPiece units).",
         fontsize=11.5, color="#333", va="top", ha="left")
logo(fig); save(fig, "fig2-delian-onions.png")
