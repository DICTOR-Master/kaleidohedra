"""Figures for the 6D note. House colours as #89 (gold = golden face, teal = regular face, lilac = corner triangle,
blue = octahedron / other); DICTO mark. Geometry in floating point for drawing only (all claims are checked in s1-s4).
fig1: sections of cube x octahedron (6D) by the flats F_mu, with the mu-line coloured by the field of mu.
fig2: (a) shadow of the 6-cube = rhombic triacontahedron, (b) central section = dodecahedron, (c) Icosaxes with its two twin
      icosahedra, (d) Unborn Axes with the two twin dodecahedra (the 24 non-cube corners).
usage (compute-host): python figs.py <out dir> <logo png>
"""
import os, sys, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import ConvexHull

OUT, LOGO = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
G = (1 + 5 ** .5) / 2; R2 = 2 ** .5
xG = G / (R2 + 2 * G); xL = 1 / (G * R2 + 2)
GOLD, TEAL, LILAC, BLUE, GREY, EDGE, RED = '#d4af37', '#2bb3a3', '#c4a6ee', '#8fb3e0', '#c9c9c9', '#1d1d24', '#b03a48'
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
logo = plt.imread(LOGO)
plt.rcParams['font.family'] = 'DejaVu Sans'


def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
M = rot(22, 32)


def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT))
    return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))


def classify(Q):
    s = np.linalg.norm(np.roll(Q, -1, 0) - Q, axis=1)
    if len(Q) == 3: return LILAC
    if np.ptp(s) < 1e-7: return TEAL
    if len(Q) % 2 == 0:
        a, b = s[0::2], s[1::2]
        if np.ptp(a) < 1e-7 and np.ptp(b) < 1e-7:
            r = max(a[0], b[0]) / min(a[0], b[0])
            if abs(r - G) < 1e-7: return GOLD
    return GREY


def faces(P, colour=None):
    hl = ConvexHull(P); groups = {}
    for eq, sx in zip(np.round(hl.equations, 8), hl.simplices): groups.setdefault(tuple(eq), set()).update(sx)
    out = []
    for eq, g in groups.items():
        g = list(g); c = P[g].mean(0); n = np.array(eq[:3])
        u = P[g[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        g.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u))
        out.append((P[g], n, colour or classify(P[g])))
    return out


def draw(ax, F, lim, alpha=1.0):
    items = []
    for P, n, col in F:
        nn = M @ n
        if alpha == 1.0 and nn[2] <= 1e-9: continue
        R = P @ M.T; items.append((R[:, 2].mean(), R[:, :2], shade(col, nn)))
    items.sort(key=lambda t: t[0])
    ax.add_collection(PolyCollection([t[1] for t in items], facecolors=[t[2] + (alpha,) for t in items], edgecolors=EDGE,
                                     linewidths=0.5))
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal'); ax.axis('off')


def wire(ax, P, col, lw=0.9, ls='-'):
    D = np.linalg.norm(P[:, None] - P[None], axis=2); m = D[D > 1e-9].min()
    for i, j in zip(*np.where(np.abs(D - m) < 1e-7)):
        if i < j:
            a, b = P[i] @ M.T, P[j] @ M.T; ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=lw, ls=ls, zorder=5)


def CO(mu):
    """corners of {|x|_inf <= 1, |x|_1 <= mu}"""
    pts = set()
    for p in itertools.permutations((1.0, max(min(mu - 1, 1.0), 0.0) if mu <= 2 else 1.0, 0.0 if mu <= 2 else mu - 2)):
        for s in itertools.product((1, -1), repeat=3):
            pts.add(tuple(np.round(np.array(p) * s, 12)))
    P = np.array(sorted(pts))
    if mu <= 1 + 1e-12: P = np.array([p for p in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, p)) == 1], float) * mu
    return P


def mark(fig):
    a = fig.add_axes([0.925, 0.008, 0.065, 0.065 * fig.get_figwidth() / fig.get_figheight()]); a.imshow(logo); a.axis('off')


# ---------------------------------------------------------------- fig 1
sel = [(1.0, 'octahedron\nμ = 1', 'Q'), (3 - G, 'Unborn Axes\nμ = 3 − φ', 'Q5'), (G, 'Icosaxes\nμ = φ', 'Q5'),
       (2.0, 'cuboctahedron\nμ = 2', 'Q'), (3 - 2 * xG, 'Greater Golden\nCut Cube', 'Q25'), (1 + R2, 'truncated cube\nμ = 1 + √2', 'Q2'),
       (3 - 2 * xL, 'Lesser Golden\nCut Cube', 'Q25'), (2 + 1 / G, 'cut cube at\nμ = 2 + 1/φ', 'Q5'), (3.0, 'cube\nμ = 3', 'Q')]
FC = {'Q': '#555555', 'Q5': GOLD, 'Q2': TEAL, 'Q25': RED}
fig = plt.figure(figsize=(9.2, 3.1))
for k, (mu, t, fld) in enumerate(sel):
    ax = fig.add_axes([0.005 + k * 0.11, 0.40, 0.105, 0.45])
    P = CO(mu)
    draw(ax, faces(P, BLUE if mu == 1.0 else None), 1.75); ax.set_title(t, fontsize=7.4, color='#222')
ax = fig.add_axes([0.04, 0.09, 0.84, 0.27]); ax.set_xlim(0.95, 3.05); ax.set_ylim(-1.1, 1.3); ax.axis('off')
ax.plot([1, 3], [0, 0], color='#333', lw=1.2)
for x0, lab in ((1, 'octahedron'), (2, 'cuboctahedron'), (3, 'cube')):
    ax.plot([x0, x0], [-0.25, 0.25], color='#333', lw=1.2); ax.text(x0, -0.75, lab, ha='center', fontsize=7.2)
pts = [(1 + 1 / G ** 2, 'Q5', '3−φ'), (1.5, 'Q', '3/2'), (G, 'Q5', 'φ'), (2 + 1 / G ** 2, 'Q5', '2+1/φ²'),
       (3 - 2 * xG, 'Q25', 'μ_G'), (1 + R2, 'Q2', '1+√2'), (3 - 2 * xL, 'Q25', 'μ_L'), (2 + 1 / G, 'Q5', '2+1/φ')]
for x0, f, lab in pts:
    ax.plot([x0], [0], 'o', ms=6.5, color=FC[f], mec='#222', mew=0.5, zorder=4)
    dy = {'μ_G': 0.95, 'μ_L': 0.95, '2+1/φ²': -0.75, '1+√2': 0.45}.get(lab, 0.45)
    ax.text(x0, dy, lab, ha='center', fontsize=7, color='#222')
for i, (f, lab) in enumerate((('Q', 'rational'), ('Q5', 'in Q(√5)'), ('Q2', 'in Q(√2)'), ('Q25', 'needs Q(√2, √5)'))):
    ax.plot([2.38 + 0.0 * i], [0], alpha=0)
    fig.text(0.05 + 0.2 * i, 0.015, '●', color=FC[f], fontsize=9); fig.text(0.07 + 0.2 * i, 0.017, lab, fontsize=7.2)
fig.text(0.5, 0.955, 'Sections of cube × octahedron (6D) by the flats y = x/μ;  face colours: gold golden, teal regular, '
         'lilac triangle, grey other', ha='center', fontsize=7.6)
mark(fig); fig.savefig(os.path.join(OUT, 'fig1-cube-octahedron-6d.png'), dpi=220, facecolor='white'); plt.close(fig)

# ---------------------------------------------------------------- fig 2
A6 = np.array([(0, 1, G), (0, -1, G), (1, G, 0), (-1, G, 0), (G, 0, 1), (-G, 0, 1)])
Y = np.array(list(itertools.product((0, 1), repeat=6)), float) - 0.5
RT = Y @ A6; RT = RT[ConvexHull(RT).vertices]
cyc = lambda a, b, c: [(a, b, c), (c, a, b), (b, c, a)]
ico = np.array([v for s1 in (1, -1) for s2 in (1, -1) for v in cyc(0, s1, G * s2)], float)
dodn = np.array([v for s1 in (1, -1) for s2 in (1, -1) for v in cyc(0, s1 / G, G * s2)], float)
dod = np.vstack([np.array(list(itertools.product((1, -1), repeat=3)), float), dodn])
tw = lambda P: P[:, [1, 0, 2]]
fig, axs = plt.subplots(1, 4, figsize=(9.2, 2.75), gridspec_kw=dict(wspace=0.04))
draw(axs[0], faces(RT, GOLD), 4.1); axs[0].set_title('(a) shadow of the 6-cube:\nrhombic triacontahedron', fontsize=8)
s = 1 / np.abs(dod @ A6.T).max()
draw(axs[1], faces(dod * s * 2.6, TEAL), 2.0); axs[1].set_title('(b) central section of the\n6-cube: dodecahedron', fontsize=8)
IA = np.vstack([ico, tw(ico)])
draw(axs[2], faces(IA, None), 2.1, alpha=0.30); wire(axs[2], ico, '#7a5c00', 1.0); wire(axs[2], tw(ico), '#1f5fa8', 1.0, '--')
axs[2].set_title('(c) Icosaxes = hull of\ntwo twin icosahedra', fontsize=8)
UA = np.vstack([dodn, tw(dodn)])
draw(axs[3], faces(UA, None), 2.1, alpha=0.30); wire(axs[3], dod, '#7a5c00', 0.8); wire(axs[3], tw(dod), '#1f5fa8', 0.8, '--')
axs[3].set_title('(d) Unborn Axes = hull of the\n24 non-cube corners of two\ntwin dodecahedra', fontsize=8)
mark(fig); fig.savefig(os.path.join(OUT, 'fig2-cut-and-project.png'), dpi=220, facecolor='white'); plt.close(fig)
print('written')
