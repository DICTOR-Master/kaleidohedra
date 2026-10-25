# Figures for the relay-census paper draft (#53, The Global Web of Bonds). Data: studies/2026-10-25-relay-census/data/raw
# (relay-summary.json, perovskite.json). The cell pictures are float power cells of the census site sets (same sites, units and
# weights as studies/2026-10-25-relay-census/scripts/networks.py), for drawing only; every number printed in a figure comes from
# the exact study data. Run on dicto-big-brother:  nice -n 10 ~/geom/bin/python make_figures.py <path to data/raw>
import json, os, sys
from itertools import product
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../../studies/2026-10-25-relay-census/data/raw")
S = json.load(open(os.path.join(RAW, "relay-summary.json")))
PV = json.load(open(os.path.join(RAW, "perovskite.json")))
GOLD, BLUE, TEAL, RED, INK, MUTED = "#b07d12", "#2f6db5", "#1a9a7a", "#b3261e", "#222222", "#777777"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": "#888", "axes.linewidth": 0.6,
                     "xtick.color": "#555", "ytick.color": "#555", "axes.labelcolor": INK, "savefig.dpi": 220})
def logo(fig): fig.text(0.995, 0.005, "DICTO", ha="right", va="bottom", fontsize=7, color="#b8962e", fontweight="bold", alpha=0.85)
def fr(s):
    if "/" in s: a, b = s.split("/"); return int(a) / int(b)
    return float(s)
def pretty(s): return s.replace("-", "−")

# ---------- Figure 1: all walks ----------
LANES = [("bcc", "CsCl (golden-loop sites)", "big", "small"), ("delian", "fluorite (Delian-loop sites)", "tet", "oct"),
         ("square", "square + centres", "corner", "centre"), ("honeycomb", "honeycomb + centres", "honeycomb", "centre"),
         ("kagome", "kagome + centres", "kagome", "centre"), ("nacl", "rock salt NaCl", "Na", "Cl"),
         ("zincblende", "zinc blende ZnS", "Zn", "S"), ("hcpholes", "hcp holes", "tet", "oct"),
         ("a15", "A15 Cr₃Si", "Si", "Cr"), ("c15", "C15 MgCu₂", "Mg", "Cu")]
TYPE = {"bcc": "gradual", "delian": "single switch", "square": "single switch", "honeycomb": "single switch",
        "kagome": "one like bond only", "nacl": "single switch", "zincblende": "gradual", "hcpholes": "gradual",
        "a15": "gradual", "c15": "gradual"}
def life(txt):
    lo, hi = txt[1:-1].split(", "); return fr(lo), fr(hi), txt[0] == "[", txt[-1] == "]"
fig, ax = plt.subplots(figsize=(7.4, 5.6))
for n, (key, name, A, B) in enumerate(LANES):
    d = S[key]; y = -n * 1.0; a, b = fr(d["range"][0]), fr(d["range"][1]); X = lambda v: (v - a) / (b - a)
    tp = d["types"]; AA = "-".join(sorted((A, A))); BB = "-".join(sorted((B, B))); AB = "-".join(sorted((A, B)))
    ax.plot([0, 1], [y, y], color=GOLD, lw=2.2, solid_capstyle="butt", zorder=2)
    for t, dy, col in ((AA, 0.22, BLUE), (BB, -0.22, TEAL)):
        lo, hi, lc, hc = life(tp[t])
        if lo == hi:
            ax.plot([X(lo)], [y + dy], "o", ms=4, color=col, zorder=3)
        else:
            ax.plot([X(lo), X(hi)], [y + dy, y + dy], color=col, lw=4, solid_capstyle="butt", zorder=3)
    for f in d["interior_flips"]:
        ax.plot([X(fr(f))] * 2, [y - 0.36, y + 0.36], color=INK, lw=0.9, zorder=4)
        ax.text(X(fr(f)), y + 0.40, pretty(f), ha="center", va="bottom", fontsize=6.8, color=INK)
    for h in d["hinge"]:
        ax.plot([X(fr(h))], [y], "D", ms=6.5, color=RED, mec="white", mew=0.6, zorder=5)
    ax.text(-0.015, y, pretty(d["range"][0]), ha="right", va="center", fontsize=6.8, color=MUTED)
    ax.text(1.015, y, pretty(d["range"][1]), ha="left", va="center", fontsize=6.8, color=MUTED)
    ax.text(-0.11, y + 0.08, name, ha="right", va="center", fontsize=8, color=INK)
    ax.text(-0.11, y - 0.24, f"above {A}–{A}, below {B}–{B} · {TYPE[key]}", ha="right", va="center", fontsize=5.9, color=MUTED)
# the golden loop is the overlap of the CsCl lane
a, b = -3, 3
ax.annotate("", xy=((1 - a) / (b - a), 0.80), xytext=((-1 - a) / (b - a), 0.80),
            arrowprops=dict(arrowstyle="<->", lw=0.7, color=GOLD))
ax.text(0.5, 0.86, "golden loop x = 0 … ∞", ha="center", va="bottom", fontsize=6.8, color=GOLD)
ax.set_xlim(-0.02, 1.02); ax.set_ylim(-len(LANES) + 0.35, 1.15); ax.axis("off")
from matplotlib.lines import Line2D
hd = [Line2D([], [], color=GOLD, lw=2.2, label="unlike bond (every lane: the whole open range)"),
      Line2D([], [], color=BLUE, lw=4, label="like bond of the kind whose weight rises"),
      Line2D([], [], color=TEAL, lw=4, label="like bond of the other kind"),
      Line2D([], [], color=INK, lw=0.9, label="flip (exact λ above)"),
      Line2D([], [], marker="D", ls="", color=RED, mec="white", label="switch point: only unlike bonds")]
fig.legend(handles=hd, loc="lower center", ncol=2, fontsize=6.8, frameon=False, bbox_to_anchor=(0.5, 0.0))
fig.text(0.5, 0.965, "each lane: λ = w_A − w_B across the whole range where both kinds have cells (ends at left and right)",
         ha="center", fontsize=7, color=MUTED)
fig.subplots_adjust(left=0.42, right=0.95, top=0.93, bottom=0.12)
logo(fig); fig.savefig(os.path.join(HERE, "fig1-all-walks.png")); plt.close(fig)

# ---------- float power cells (drawing only) ----------
def cells(G, T, motif, w, lam, centre_sites, K=3, R2=30.0):
    """Power cells (Euclidean coordinates) of the given motif indices; returns list of (kind, site, vertices, neighbours)."""
    G = np.array(G, float); L = np.linalg.cholesky(G).T; T = np.array(T, float); d = len(G)
    allp = []
    for kv in product(range(-K, K + 1), repeat=d):
        t = np.array(kv) @ T
        for j, (k, c) in enumerate(motif): allp.append((k, L @ (np.array(c, float) + t)))
    out = []
    for (kc, cc) in centre_sites:
        ci = L @ np.array(cc, float); S_ = [(k, c) for k, c in allp if 1e-9 < np.sum((c - ci) ** 2) < R2]
        A = np.array([2 * (c - ci) for _, c in S_]); b = np.array([c @ c - ci @ ci + w(kc, lam) - w(k, lam) for k, c in S_])
        nr = np.linalg.norm(A, axis=1)
        res = linprog(np.r_[np.zeros(d), -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * d + [(0, None)], method="highs")
        if res.status != 0 or res.x[-1] < 1e-9:
            out.append((kc, ci, None, [])); continue
        V = HalfspaceIntersection(np.c_[A, -b], res.x[:d]).intersections
        nb = []
        for q, (k, c) in enumerate(S_):
            on = V[np.abs(V @ A[q] - b[q]) < 1e-7 * max(1, nr[q])]
            if len(on) >= d and np.linalg.matrix_rank(on[1:] - on[0], tol=1e-6) == d - 1: nb.append((k, c))
        out.append((kc, ci, V, nb))
    return out

def poly2d(V):
    c = V.mean(0); return V[np.argsort(np.arctan2(V[:, 1] - c[1], V[:, 0] - c[0]))]

# ---------- Figure 2: the 2D walks at named stops ----------
sq = dict(G=[[1, 0], [0, 1]], T=[(2, 0), (0, 2)], motif=[("corner", (0, 0)), ("centre", (1, 1))])
hx = dict(G=[[1, .5], [.5, 1]], T=[(1, 1), (-1, 2)], motif=[("honeycomb", (0, 0)), ("honeycomb", (1, 0)), ("centre", (0, 1))])
def wA(A): return lambda k, lam: lam if k == A else 0.0
COL = {"corner": "#e9d9a8", "centre": "#cfe0f3", "honeycomb": "#e9d9a8"}
def draw2d(ax, net, A, lam, title, box):
    sites = []
    for kv in product(range(-4, 5), repeat=2):
        t = np.array(kv) @ np.array(net["T"], float)
        for k, c in net["motif"]: sites.append((k, tuple(np.array(c, float) + t)))
    L = np.linalg.cholesky(np.array(net["G"], float)).T
    sites = [(k, c) for k, c in sites if np.all(np.abs(L @ np.array(c)) < box + 1.6)]
    res = cells(net["G"], net["T"], net["motif"], wA(A), lam, sites, K=5, R2=16)
    for k, ci, V, nb in res:
        if V is None: continue
        ax.add_patch(Polygon(poly2d(V), closed=True, fc=COL[k], ec="#333", lw=0.9))
    for k, ci, V, nb in res:
        if V is None: continue
        for k2, c2 in nb:
            col = GOLD if k != k2 else (BLUE if k == A else TEAL); ls = "-" if k != k2 else "--"
            ax.plot([ci[0], c2[0]], [ci[1], c2[1]], color=col, lw=0.8, ls=ls, alpha=0.9, zorder=3)
    for k, ci, V, nb in res:
        ax.plot(ci[0], ci[1], "o", ms=2.4 if V is not None else 1.6, color=INK, zorder=4)
    ax.set_xlim(-box, box); ax.set_ylim(-box, box); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=7.4, color=INK)
fig, axs = plt.subplots(2, 3, figsize=(7.4, 5.3))
r2, r3 = 2 ** 0.5, 3 ** 0.5
draw2d(axs[0, 0], sq, "corner", -(2 * r2 - 2), "square + centres, λ = −(2√2 − 2)\nuniform 4.8.8 (centre octagons)", 2.6)
draw2d(axs[0, 1], sq, "corner", 0.0, "λ = 0: switch point\nsquare tiling, only unlike bonds", 2.6)
draw2d(axs[0, 2], sq, "corner", 2 * r2 - 2, "λ = 2√2 − 2\nuniform 4.8.8 (corner octagons)", 2.6)
draw2d(axs[1, 0], hx, "honeycomb", 1 - r3, "honeycomb + centres, λ = 1 − √3\nuniform 3.12.12", 2.1)
draw2d(axs[1, 1], hx, "honeycomb", -0.5, "λ = −1/2: switch point\ntrihexagonal 3.6.3.6, only unlike bonds", 2.1)
draw2d(axs[1, 2], hx, "honeycomb", 0.0, "λ = 0\nregular hexagonal tiling", 2.1)
hd = [Line2D([], [], color=GOLD, lw=1.1, label="unlike bond"),
      Line2D([], [], color=BLUE, lw=1.1, ls="--", label="corner–corner / honeycomb–honeycomb"),
      Line2D([], [], color=TEAL, lw=1.1, ls="--", label="centre–centre")]
fig.legend(handles=hd, loc="lower center", ncol=3, fontsize=7, frameon=False)
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.07, wspace=0.05, hspace=0.25)
logo(fig); fig.savefig(os.path.join(HERE, "fig2-2d-stops.png")); plt.close(fig)

# ---------- Figure 3: perovskite chamber map ----------
fig, ax = plt.subplots(figsize=(5.2, 3.2))
shade = ["#efe3bd", "#f6efd9", "#dbe8f5", "#e7efe0", "#f2f2f2"]
for n, ch in enumerate(PV["chambers"]):
    P = np.array([[fr(x) for x in v] for v in ch["verts"]])
    ax.add_patch(Polygon(P, closed=True, fc=shade[n % len(shade)], ec="#888", lw=0.5))
    c = P.mean(0); like = [t for t in ch["bond_types"] if t in ("A-A", "B-B", "X-X")]
    ax.text(c[0], c[1], "like: " + (", ".join(t.replace("-", "–") for t in like) or "none") + "\n" +
            ("A–B" if "A-B" in ch["bond_types"] else "no A–B"), ha="center", va="center", fontsize=6.6, color=INK)
ax.plot([0, 0], [-1, 1], color=BLUE, lw=1.4); ax.text(0.04, -0.93, "λ = 0: A–A born", fontsize=6.6, color=BLUE)
ax.plot([-2, 2], [1, -1], color=RED, lw=1.4); ax.text(-1.95, 1.04, "λ + 2μ = 0: A–B born", fontsize=6.6, color=RED, va="bottom")
ax.plot([0, 2], [1, -1], color=TEAL, lw=1.4); ax.text(1.62, -0.52, "λ + μ = 1:\nX–X dies", fontsize=6.6, color=TEAL, ha="left")
ax.set_xlim(-2.1, 2.1); ax.set_ylim(-1.1, 1.25); ax.set_aspect("equal")
ax.set_xlabel("λ = w_A − w_X"); ax.set_ylabel("μ = w_B − w_X"); ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_yticks([-1, 0, 1])
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); logo(fig); fig.savefig(os.path.join(HERE, "fig3-perovskite.png")); plt.close(fig)

# ---------- Figure 4: two 3D stops ----------
def faces3d(V):
    h = ConvexHull(V); groups = []
    for simp, eq in zip(h.simplices, h.equations):
        for g in groups:
            if np.allclose(g["eq"], eq, atol=1e-6): g["pts"].update(simp); break
        else: groups.append({"eq": eq, "pts": set(simp)})
    out = []
    for g in groups:
        P = V[list(g["pts"])]; n = g["eq"][:3]; c = P.mean(0); u = P[0] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        out.append(P[np.argsort(np.arctan2((P - c) @ v, (P - c) @ u))])
    return out
nacl = dict(G=np.eye(3), T=[(2, 0, 0), (0, 2, 0), (0, 0, 2)],
            motif=[("Na", (0, 0, 0)), ("Na", (1, 1, 0)), ("Na", (1, 0, 1)), ("Na", (0, 1, 1)),
                   ("Cl", (1, 0, 0)), ("Cl", (0, 1, 0)), ("Cl", (0, 0, 1)), ("Cl", (1, 1, 1))])
h = 0.5
a15 = dict(G=np.eye(3), T=[(2, 0, 0), (0, 2, 0), (0, 0, 2)],
           motif=[("Si", (0, 0, 0)), ("Si", (1, 1, 1))] + [("Cr", p) for p in [(h, 0, 1), (3 * h, 0, 1), (1, h, 0), (1, 3 * h, 0), (0, 1, h), (0, 1, 3 * h)]])
def cell3(net, A, lam, k, c):
    return cells(net["G"], net["T"], net["motif"], wA(A), lam, [(k, c)], K=2, R2=14)[0][2]
lamN = 4 - 2 * 3 ** 0.5
panels = [(nacl, "Na", lamN, "Na", (0, 0, 0), "NaCl, λ = 4 − 2√3: Na cell\n6 squares + 12 hexagons, all edges equal", "#e9d9a8"),
          (nacl, "Na", lamN, "Cl", (1, 0, 0), "NaCl, same λ: Cl cell\ncube (only unlike bonds)", "#cfe0f3"),
          (a15, "Si", 0.75, "Si", (0, 0, 0), "A15, λ = 3/4: Si cell\n20 triangles (icosahedral pattern)", "#e9d9a8"),
          (a15, "Si", 0.75, "Cr", (h, 0, 1), "A15, same λ: Cr cell\ntetrahedron (only unlike bonds)", "#cfe0f3")]
fig = plt.figure(figsize=(7.4, 2.6))
for n, (net, A, lam, k, c, title, col) in enumerate(panels):
    ax = fig.add_subplot(1, 4, n + 1, projection="3d"); V = cell3(net, A, lam, k, c); F = faces3d(V)
    ax.add_collection3d(Poly3DCollection(F, facecolor=col, edgecolor="#444", linewidths=0.6, alpha=0.95))
    m = V.mean(0); r = np.abs(V - m).max() * 1.05
    ax.set_xlim(m[0] - r, m[0] + r); ax.set_ylim(m[1] - r, m[1] + r); ax.set_zlim(m[2] - r, m[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(22, 32); ax.axis("off"); ax.set_title(title, fontsize=7, color=INK)
    print(title.split("\n")[0], "faces", sorted(len(f) for f in F))
fig.subplots_adjust(left=0, right=1, top=0.86, bottom=0.0, wspace=0.0)
logo(fig); fig.savefig(os.path.join(HERE, "fig4-3d-stops.png")); plt.close(fig)
print("figures written")
