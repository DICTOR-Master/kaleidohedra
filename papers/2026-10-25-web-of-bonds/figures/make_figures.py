# Figures for the web-of-bonds paper draft (#52 proposed). Closed forms from studies/2026-10-25-web-of-bonds (README §2, symbolic.json)
# and studies/2026-10-25-physical-anchors (contact maps, windows, compounds.json). Run on dicto-big-brother: nice -n 10 ~/geom/bin/python make_figures.py
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
COMP = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else None
phi = (1 + 5 ** 0.5) / 2
r3, r2 = 3 ** 0.5, 2 ** 0.5
GOLD, BLUE, TEAL, INK, MUTED = "#b07d12", "#2f6db5", "#1a9a7a", "#222222", "#777777"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#888", "axes.linewidth": 0.6,
                     "xtick.color": "#555", "ytick.color": "#555", "axes.labelcolor": INK, "savefig.dpi": 220})

def logo(fig):
    fig.text(0.995, 0.01, "DICTO", ha="right", va="bottom", fontsize=7, color="#b8962e", fontweight="bold", alpha=0.8)

def golden_axis(ax):
    xs = {"0": 0, "1/3": 1/3, "1/τ": 1/phi, "1": 1, "τ": phi, "3": 3}
    ticks = [v/(1+v) for v in xs.values()] + [1]
    ax.set_xticks(ticks); ax.set_xticklabels(list(xs.keys()) + ["∞"])
    ax.set_xlim(0, 1); ax.set_xlabel("factor x  (axis spaced evenly in s = x/(1+x))")

def style(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color="#e6e6e6", lw=0.6); ax.set_axisbelow(True)

# ---------- Figure 1: bond areas ----------
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.9))
s = np.linspace(0, 1, 801)
bs = (r3/8)*phi**2*(1 + 2*s - 2*s*s)        # (x^2+4x+1)/(1+x)^2 = 1 + 2s - 2s^2
bb = phi**2*s*s/2; ss = phi**2*(1-s)**2/2
a.plot(s, bs, color=GOLD, lw=2, label="big–small (hexagon)")
a.plot(s, bb, color=BLUE, lw=2, ls="--", label="big–big (square)")
a.plot(s, ss, color=TEAL, lw=2, ls=":", label="small–small (square)")
for sv, lab in [(0.5, "Kelvin"), (1/phi, "τ"), (1/phi**2, "1/τ")]:
    a.axvline(sv, color="#cccccc", lw=0.6, zorder=0)
a.plot([0.5], [phi**2/8], "o", ms=5, color=INK); a.annotate("equal at Kelvin: φ²/8", (0.5, phi**2/8), (0.08, 0.42), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTED))
a.plot([1/phi]*2, [0.5, 1/(2*phi**2)], "o", ms=5, color=INK, mfc="white")
a.annotate("x = τ: 1/2", (1/phi, 0.5), (0.66, 0.43), fontsize=7.5)
a.plot([0.5], [(3*r3/16)*phi**2], "o", ms=5, color=GOLD); a.annotate("max (3√3/16)φ²", (0.5, (3*r3/16)*phi**2), (0.3, 0.9), fontsize=7.5)
golden_axis(a); a.set_ylim(0, 1.45); a.set_ylabel("area of one bond face (app units, L = φ)")
a.set_title("Golden loop: gradual hand-over", fontsize=9.5, loc="left", color=INK); style(a)
a.legend(fontsize=7, frameon=False, loc="upper center", ncol=1, bbox_to_anchor=(0.5, -0.24))

t = np.linspace(0, 1, 801)
ot = np.where(t <= 1/3, (9*r3/4)*t*t, (9*r3/16)*(1-t)**2)
oo = np.where(t <= 1/3, (r2/4)*(1-9*t*t), np.nan)
tt = np.where(t >= 1/3, (3*t-1)*(5-3*t)/8, np.nan)
b.plot(t, ot, color=GOLD, lw=2, label="oct–tet (triangle)")
b.plot(t, oo, color=BLUE, lw=2, ls="--", label="oct–oct (hexagon; rhombus at t = 0)")
b.plot(t, tt, color=TEAL, lw=2, ls=":", label="tet–tet (hexagon; square at t = 1)")
stops = [((2*6**0.5-3)/15, "eq. RD"), (1/3, "octet"), (1-6**(1/3)/3, "half"), (1-(2/3)*2**(-1/3), "Delian bond"), (5/3-(2/3)*r2, "eq. cube")]
for tv, lab in stops:
    b.axvline(tv, color="#cccccc", lw=0.6, zorder=0)
b.plot([1/3], [r3/4], "o", ms=5, color=GOLD); b.annotate("octet: √3/4, only oct–tet", (1/3, r3/4), (0.37, 0.47), fontsize=7.5)
td = 1-(2/3)*2**(-1/3)
b.plot([td, td], [2**(1/3)*r3/8, 0.5-2**(1/3)/4], "o", ms=5, color=INK, mfc="white")
b.set_xticks([0, (2*6**0.5-3)/15, 1/3, td, 5/3-(2/3)*r2, 1]); b.set_xticklabels(["0\nRD", "eq.\nRD", "1/3\noctet", "Delian\nbond", "eq.\ncube", "1\ncube"], fontsize=7.5)
b.set_xlim(0, 1); b.set_ylim(0, 0.62); b.set_xlabel("Delian slider t")
b.set_title("Delian loop: hand-over at the octet", fontsize=9.5, loc="left", color=INK); style(b)
b.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=1)
b.set_ylabel("area (app units, octet edge 1)")
fig.tight_layout(); logo(fig); fig.savefig(os.path.join(HERE, "fig1-bond-areas.png")); plt.close(fig)

# ---------- Figure 2: bonds per piece ----------
fig, axs = plt.subplots(2, 2, figsize=(7.4, 3.6), sharex="col")
def bars(ax, segs, pts, xmax):
    # segs: list of (x0, x1, [(count, color, hatch)]) open intervals; pts: list of (x, [(count,color)]) isolated points
    for x0, x1, parts in segs:
        y = 0
        for n, c, h in parts:
            ax.bar((x0+x1)/2, n, width=(x1-x0)*0.97, bottom=y, color=c, edgecolor="white", lw=1.2, hatch=h, alpha=0.9)
            y += n
        ax.text((x0+x1)/2, y+0.6, " + ".join(str(p[0]) for p in parts) + (f" = {y}" if len(parts) > 1 else ""), ha="center", fontsize=7.5)
    for x, parts, txt in pts:
        y = 0
        for n, c in parts:
            ax.plot([x, x], [y, y+n], color=c, lw=4, solid_capstyle="butt"); y += n
        ax.plot([x], [y], "o", ms=4, color=INK)
        ax.text(x, y+0.6, txt, ha="center", fontsize=7)
    ax.set_ylim(0, 24); ax.set_yticks([0, 4, 8, 12, 16, 20]); style(ax)
# golden: in s
bars(axs[0][0], [(0.0, 1.0, [(8, GOLD, ""), (6, BLUE, "//")])], [(0.0, [(8, GOLD)], "8")], 1)
axs[0][0].set_title("golden big piece", fontsize=9, loc="left")
bars(axs[1][0], [(0.0, 1.0, [(8, GOLD, ""), (6, TEAL, "..")])], [(1.0, [(8, GOLD)], "8")], 1)
axs[1][0].set_title("golden small piece", fontsize=9, loc="left"); golden_axis(axs[1][0])
bars(axs[0][1], [(0, 1/3, [(12, BLUE, "//"), (8, GOLD, "")]), (1/3, 1, [(8, GOLD, "")])],
     [(0.0, [(12, BLUE)], "12"), (1/3, [(8, GOLD)], ""), (1.0, [], "point")], 1)
axs[0][1].set_title("Delian oct piece", fontsize=9, loc="left")
bars(axs[1][1], [(0, 1/3, [(4, GOLD, "")]), (1/3, 1, [(4, GOLD, ""), (6, TEAL, "..")])],
     [(0.0, [], "point"), (1/3, [(4, GOLD)], ""), (1.0, [(6, TEAL)], "6")], 1)
axs[1][1].set_title("Delian tet piece", fontsize=9, loc="left")
axs[1][1].set_xticks([0, 1/3, 1]); axs[1][1].set_xticklabels(["0", "1/3 (octet)", "1"]); axs[1][1].set_xlim(-0.03, 1.03); axs[1][1].set_xlabel("Delian slider t")
axs[1][0].set_xlim(-0.03, 1.03)
for ax in axs[:, 0]: ax.set_ylabel("bonds")
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=GOLD, label="unlike bond (big–small / oct–tet)"), Patch(facecolor=BLUE, hatch="//", edgecolor="white", label="big–big / oct–oct"),
                    Patch(facecolor=TEAL, hatch="..", edgecolor="white", label="small–small / tet–tet")], loc="lower center", ncol=3, fontsize=7.5, frameon=False)
fig.tight_layout(rect=(0, 0.07, 1, 1)); logo(fig); fig.savefig(os.path.join(HERE, "fig2-bonds-per-piece.png")); plt.close(fig)

# ---------- Figure 3: the dual rhombic dodecahedron and its diagonal swap at the octet ----------
O = [np.array(v, float) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
Q = [np.array((a, b, c), float)/2 for a in (1,-1) for b in (1,-1) for c in (1,-1)]
rh = []  # 12 rhombi: two O corners (adjacent axes) + two Q corners
for i in range(6):
    for j in range(i+1, 6):
        if abs(np.dot(O[i], O[j])) < 1e-9:
            qs = [q for q in Q if np.dot(q, O[i]) > 0 and np.dot(q, O[j]) > 0]
            rh.append((O[i], O[j], qs[0], qs[1]))
fig = plt.figure(figsize=(7.4, 2.8))
titles = ["t < 1/3: long diagonals (oct–oct)\noctahedron + 8 tetrahedra",
          "t = 1/3, the octet: no diagonal\nweb bipartite (oct–tet only)",
          "t > 1/3: short diagonals (tet–tet)\ncube + 6 square pyramids"]
for k in range(3):
    ax = fig.add_subplot(1, 3, k+1, projection="3d"); ax.set_proj_type("ortho"); ax.view_init(elev=18, azim=28)
    polys = [[o1, q1, o2, q2] for o1, o2, q1, q2 in rh]
    ax.add_collection3d(Poly3DCollection(polys, facecolor="#f3ead2", edgecolor=GOLD, lw=0.9, alpha=0.18))
    for o1, o2, q1, q2 in rh:
        if k == 0: ax.plot(*zip(o1, o2), color=BLUE, lw=1.8, ls="--")
        if k == 2: ax.plot(*zip(q1, q2), color=TEAL, lw=1.8)
    ax.scatter(*np.array(O).T, s=26, color=BLUE, depthshade=False, label="oct site")
    ax.scatter(*np.array(Q).T, s=26, color=TEAL, marker="s", depthshade=False, label="tet site")
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); lim = 1.0; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_title(titles[k], fontsize=8, pad=-2)
fig.legend(handles=[plt.Line2D([], [], marker="o", ls="", color=BLUE, label="oct site (4-valent corner)"),
                    plt.Line2D([], [], marker="s", ls="", color=TEAL, label="tet site (3-valent corner)"),
                    plt.Line2D([], [], color=BLUE, ls="--", label="oct–oct bond (long diagonal, 1)"),
                    plt.Line2D([], [], color=TEAL, label="tet–tet bond (short diagonal, 1/√2)")],
           loc="lower center", ncol=2, fontsize=7, frameon=False)
fig.subplots_adjust(left=0, right=1, top=0.86, bottom=0.14, wspace=0); logo(fig)
fig.savefig(os.path.join(HERE, "fig3-diagonal-swap.png")); plt.close(fig)

# ---------- Figure 4: real compounds on the loops (contact model, Shannon effective ionic radii) ----------
if COMP:
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.2))
    rho = (2 - s)/(1 + s)
    a.axvspan(((3**0.5-1)/2)/(1+(3**0.5-1)/2), (3**0.5+1)/(2+3**0.5), color="#eef3fa", zorder=0)
    a.plot(s, rho, color=INK, lw=1.4)
    golden_axis(a); a.set_ylabel("radius ratio ρ = r_small / r_big"); a.set_ylim(0.4, 2.1); style(a)
    a.set_title("Golden loop = CsCl type", fontsize=9.5, loc="left")
    a.text(0.5, 1.95, "touching window", ha="center", fontsize=7.5, color=BLUE)
    gl = [c for c in COMP["compounds"] if c.get("x")]
    offs = {"CsCl": (0.02, 0.35), "CsBr": (-0.13, -0.32), "TlCl": (0.03, 0.28), "TlBr": (-0.11, -0.3), "CsI": (0.03, 0.22)}
    for c in gl:
        from fractions import Fraction
        x = float(Fraction(c["x"])); sv = x/(1+x)
        a.plot([sv], [c["rho_f"]], "o", ms=5, color=GOLD, mec="white", mew=0.8, zorder=3)
        dx, dy = offs[c["formula"]]
        a.annotate(c["formula"], (sv, c["rho_f"]), (sv+dx, c["rho_f"]+dy), fontsize=7, arrowprops=dict(arrowstyle="-", lw=0.4, color=MUTED))
    a.plot([0.5], [1], "o", ms=4, color=INK); a.annotate("Kelvin", (0.5, 1), (0.36, 0.72), fontsize=7)
    tt_ = np.linspace(0, 0.68, 600); b.plot(tt_, tt_/(1-tt_), color=INK, lw=1.4)
    b.axvspan(1-(2/3)**0.5, 1/3**0.5, color="#eef3fa", zorder=0)
    b.axvspan(1/6, 2/3, ymin=0, ymax=0.03, color="#c9d6ea", zorder=0)
    b.axvline(1/3, color="#999", lw=0.7, ls="--"); b.text(1/3, 1.55, "octet", ha="center", fontsize=7.5, color=MUTED)
    b.text((1-(2/3)**0.5+1/3**0.5)/2, 0.12, "touching window", ha="center", fontsize=7.5, color=BLUE)
    dl = [c for c in COMP["compounds"] if c.get("t")]
    pos = {"K2O": (0.6, 0.55), "BaF2": (0.6, 0.72), "PbF2": (0.6, 0.89), "SrF2": (0.6, 1.06), "CaF2": (0.6, 1.23), "CeO2": (0.645, 1.38),
            "CdF2": (0.40, 1.28), "ThO2": (0.42, 1.45), "UO2": (0.45, 1.62), "ZrO2 (cubic)": (0.47, 1.85), "Na2O": (0.31, 0.88), "Li2O": (0.19, 0.62)}
    sub = lambda f: f.replace("2", "₂")
    for c in dl:
        tv = c["t_f"]; col = GOLD if c["in_contact_window"] else "#c0392b"
        b.plot([tv], [c["rho_f"]], "o" if c["in_contact_window"] else "X", ms=5, color=col, mec="white", mew=0.6, zorder=3)
        px, py = pos[c["formula"]]
        b.annotate(sub(c["formula"].replace(" (cubic)", "")), (tv, c["rho_f"]), (px, py), fontsize=6.6, arrowprops=dict(arrowstyle="-", lw=0.4, color=MUTED))
    b.set_xlim(0, 0.7); b.set_ylim(0, 2.1); style(b)
    b.set_xlabel("Delian slider t  (bar: packings exist, 1/6 ≤ t ≤ 2/3)"); b.set_ylabel("ρ = r_tet-site / r_oct-site")
    b.set_title("Delian loop = fluorite type", fontsize=9.5, loc="left")
    b.plot([], [], "o", color=GOLD, label="in window"); b.plot([], [], "X", color="#c0392b", label="outside (tet–tet overlap)")
    b.legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(0.0, 1.0))
    fig.tight_layout(); logo(fig); fig.savefig(os.path.join(HERE, "fig4-compounds.png")); plt.close(fig)
print("figures written")
