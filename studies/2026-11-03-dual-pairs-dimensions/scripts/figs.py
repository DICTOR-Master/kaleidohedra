"""Figures for the dual-pairs note. House colours as #89 / the 6D note (gold = golden face, teal = regular face, lilac = triangle,
blue = other polygon, grey = irregular); DICTO mark. Geometry in floating point for drawing only (every claim is checked in s1-s9).
fig1: the three 6D sweeps S(mu) = P cap mu P* (D.I, C.O, T.T), one strip per pair, with the nu-line coloured by field.
fig2: OG and the polar Dharma cycle: the seven stations in the dual-pair families, and the (mu, lambda) map.
fig3: the 4D sweeps (8D products) as parameter lines with their golden stations.
fig4: cycles as slices: the 24-cell honeycomb slice y1 = h (two tiles per BCC cell) and the Fibonacci station word.
usage (dicto-big-brother): python figs.py <out dir> <logo png>
"""
import os, sys, itertools, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import ConvexHull, HalfspaceIntersection
OUT, LOGO = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
G = (1 + 5 ** .5) / 2; R2 = 2 ** .5
GOLD, TEAL, LILAC, BLUE, GREY, EDGE, RED = '#d4af37', '#2bb3a3', '#c4a6ee', '#8fb3e0', '#c9c9c9', '#1d1d24', '#b03a48'
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
logo = plt.imread(LOGO); plt.rcParams['font.family'] = 'DejaVu Sans'
def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
M = rot(20, 28)
def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT)); return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))
def classify(Q):
    s = np.linalg.norm(np.roll(Q, -1, 0) - Q, axis=1)
    if np.ptp(s) < 1e-6 * s.max(): return LILAC if len(Q) == 3 else TEAL
    if len(Q) % 2 == 0:
        a, b = s[0::2], s[1::2]
        if np.ptp(a) < 1e-6 and np.ptp(b) < 1e-6:
            r = max(a[0], b[0]) / min(a[0], b[0])
            if abs(r - G) < 1e-6: return GOLD
    return LILAC if len(Q) == 3 else (BLUE if len(Q) == 4 and np.ptp(s) < 1e-6 else GREY)
def faces(P, colour=None):
    hl = ConvexHull(P); groups = {}
    for eq, sx in zip(np.round(hl.equations, 7), hl.simplices): groups.setdefault(tuple(eq), set()).update(sx)
    out = []
    for eq, g in groups.items():
        g = list(g); c = P[g].mean(0); n = np.array(eq[:3]); u = P[g[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        g.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); out.append((P[g], n, colour or classify(P[g])))
    return out
def draw(ax, F, lim, alpha=1.0):
    items = []
    for P, n, col in F:
        nn = M @ n
        if alpha == 1.0 and nn[2] <= 1e-9: continue
        R = P @ M.T; items.append((R[:, 2].mean(), R[:, :2], shade(col, nn)))
    items.sort(key=lambda t: t[0])
    ax.add_collection(PolyCollection([t[1] for t in items], facecolors=[t[2] + (alpha,) for t in items], edgecolors=EDGE, linewidths=0.45))
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal'); ax.axis('off')
def mark(fig):
    a = fig.add_axes([0.93, 0.006, 0.06, 0.06 * fig.get_figwidth() / fig.get_figheight()]); a.imshow(logo); a.axis('off')
cyc = lambda a, b, c: [(a, b, c), (c, a, b), (b, c, a)]
DOD = np.vstack([np.array(list(itertools.product((1, -1), repeat=3)), float),
                 np.array([v for s1 in (1, -1) for s2 in (1, -1) for v in cyc(0, s1 / G, G * s2)], float)])
CUBE = np.array(list(itertools.product((1, -1), repeat=3)), float)
TET = np.array([v for v in CUBE if np.prod(v) > 0])
def pair(V):
    h = ConvexHull(V); E = np.unique(np.round(h.equations, 9), axis=0); N = E[:, :3] / (-E[:, 3:])   # P = {N x <= 1}
    return V, N
def S(V, N, mu):
    A = np.vstack([np.hstack([N, -np.ones((len(N), 1))]), np.hstack([V, -mu * np.ones((len(V), 1))])])
    P = HalfspaceIntersection(A, np.zeros(3)).intersections
    return P[np.unique(np.round(P, 9), axis=0, return_index=True)[1]]
def Hull(V, N, mu):
    P = np.vstack([V, mu * N]); return P[ConvexHull(P).vertices]
def mups(V, N, x):   # dual-side cut
    Rs2 = (N[0] @ N[0]); d = np.linalg.norm(N[:, None] - N[None], axis=2); es2 = d[d > 1e-9].min() ** 2
    return 1 / (Rs2 - x * es2 / 2)
def mup(V, N, x):
    R2_ = V[0] @ V[0]; d = np.linalg.norm(V[:, None] - V[None], axis=2); e2 = d[d > 1e-9].min() ** 2
    return R2_ - x * e2 / 2
cN = {3: 1, 4: R2, 5: G}
xg = lambda c: G / (c + 2 * G); xl = lambda c: 1 / (G * c + 2)
FC = {'Q': '#555555', 'Q5': GOLD, 'Q2': TEAL, 'Q25': RED}
# ------------------------------------------------------------------ fig 1
rows = [('D·I  dodecahedron × icosahedron', DOD, 5, 3, ['icosahedron', 'Lesser GC\nIcosahedron', 'truncated\nicosahedron', 'Greater GC\nIcosahedron',
         'icosidodeca-\nhedron', 'Greater GC\nDodecahedron', 'truncated\ndodecahedron', 'Lesser GC\nDodecahedron', 'dodecahedron'],
         ['Q', 'Q5', 'Q5', 'Q5', 'Q5', 'Q5', 'Q5', 'Q5', 'Q5']),
        ('C·O  cube × octahedron (recap of the 6D study)', CUBE, 4, 3, ['octahedron', 'Unborn Axes', 'truncated\noctahedron', 'Icosaxes',
         'cubocta-\nhedron', 'Greater GC\nCube', 'truncated\ncube', 'Lesser GC\nCube', 'cube'], ['Q', 'Q5', 'Q', 'Q5', 'Q', 'Q25', 'Q2', 'Q25', 'Q']),
        ('T·T  tetrahedron × its polar', TET, 3, 3, ['tetrahedron\n(polar)', 'Lesser GC\nTetrahedron', 'truncated\ntetrahedron', 'Greater GC\nTetrahedron',
         'octahedron', 'Greater GC\nTetrahedron', 'truncated\ntetrahedron', 'Lesser GC\nTetrahedron', 'tetrahedron'], ['Q', 'Q5', 'Q', 'Q5', 'Q', 'Q5', 'Q', 'Q5', 'Q'])]
fig = plt.figure(figsize=(9.4, 7.6))
for r, (title, V0, nP, nS, labs, flds) in enumerate(rows):
    V, N = pair(V0); r2 = 1 / (N[0] @ N[0]); rho2 = mup(V, N, .5)
    mus = [r2, mups(V, N, xl(cN[nS])), mups(V, N, 1 / (cN[nS] + 2)), mups(V, N, xg(cN[nS])), rho2,
           mup(V, N, xg(cN[nP])), mup(V, N, 1 / (cN[nP] + 2)), mup(V, N, xl(cN[nP])), V[0] @ V[0]]
    y0 = 0.70 - r * 0.325
    fig.text(0.01, y0 + 0.255, title, fontsize=8.6, weight='bold', color='#222')
    for k, mu in enumerate(mus):
        ax = fig.add_axes([0.005 + k * 0.109, y0 + 0.075, 0.104, 0.17])
        P = (N if k == 0 else V) if k in (0, 8) else S(V, N, mu); P = P / np.linalg.norm(P, axis=1).max()
        draw(ax, faces(P), 1.05); ax.set_title(labs[k], fontsize=6.4, color='#222', pad=1)
    ax = fig.add_axes([0.03, y0, 0.9, 0.065]); nus = [m / r2 for m in mus]
    ax.set_xlim(nus[0] - 0.03 * (nus[-1] - nus[0]), nus[-1] + 0.03 * (nus[-1] - nus[0])); ax.set_ylim(-1, 1.3); ax.axis('off')
    ax.plot([nus[0], nus[-1]], [0, 0], color='#333', lw=1)
    for k, (nu, f) in enumerate(zip(nus, flds)):
        ax.plot([nu], [0], 'o', ms=5.5, color=FC[f], mec='#222', mew=0.4, zorder=4)
        ax.text(nu, 0.45 if k % 2 == 0 else -0.95, f'{nu:.3f}', ha='center', fontsize=6.2, color='#333')
    ax.text(nus[-1] + 0.025 * (nus[-1] - nus[0]), -0.15, 'ν', fontsize=8)
for i, (f, lab) in enumerate((('Q', 'ν rational'), ('Q5', 'ν in Q(√5)'), ('Q2', 'ν in Q(√2)'), ('Q25', 'ν needs Q(√2, √5)'))):
    fig.text(0.05 + 0.2 * i, 0.012, '●', color=FC[f], fontsize=9); fig.text(0.07 + 0.2 * i, 0.014, lab, fontsize=7.2)
fig.text(0.5, 0.982, 'Sections P ∩ μP* of the 6D products P × P* by the flats y = x/μ;  ν = μ/r² (dual end at 1); faces: gold golden, teal regular, lilac triangle',
         ha='center', fontsize=7.4)
mark(fig); fig.savefig(os.path.join(OUT, 'fig1-sweeps.png'), dpi=220, facecolor='white'); plt.close(fig)
# ------------------------------------------------------------------ fig 2: OG and the polar Dharma cycle
V, N = pair(DOD); r2 = 1 / (N[0] @ N[0]); rho2 = mup(V, N, .5); muTI = mups(V, N, 1 / 3)
PD = Hull(V, N, muTI)
hP = ConvexHull(PD); E = np.unique(np.round(hP.equations, 9), axis=0)
A = np.vstack([E, np.hstack([V, -rho2 * np.ones((20, 1))])]); OG = HalfspaceIntersection(A, np.zeros(3)).intersections
OG = OG[np.unique(np.round(OG, 9), axis=0, return_index=True)[1]]
c = 3 * (5 ** .5) - 6
st = [('dodecahedron\n(3/φ³) D', c * V, TEAL), ('icosidodecahedron\nS(φ²)', S(V, N, rho2), None), ('OG\nQ(μ_TI, φ²)', OG, None),
      ('pentakis dodeca-\nhedron H(μ_TI)', PD, BLUE), ('icosahedron\nH(3) = 3D*', 3 * N, None), ('rhombic triaconta-\nhedron (3/φ²)H(φ²)', 3 / rho2 * Hull(V, N, rho2), BLUE),
      ('dodecahedron\n3D = φ³ · (3/φ³)D', 3 * V, TEAL)]
fig = plt.figure(figsize=(9.4, 4.4))
lim = 1.05 * max(np.linalg.norm(p, axis=1).max() for _, p, _ in st)
for k, (lab, P, col) in enumerate(st):
    ax = fig.add_axes([0.005 + k * 0.141, 0.47, 0.137, 0.40])
    draw(ax, faces(P, col), lim); ax.set_title(lab, fontsize=6.8, pad=1)
    if k < 6: fig.text(0.141 * (k + 1) - 0.002, 0.66, '⊂', fontsize=12, ha='center', color='#7a5c00')
ax = fig.add_axes([0.08, 0.08, 0.5, 0.32])
ax.set_xlabel('μ (hull H(μ) = conv(D ∪ μD*), D with R² = 3)', fontsize=7); ax.set_ylabel('λ (cut by λD*)', fontsize=7)

ax.axhline(rho2, color=GOLD, lw=0.8, ls='--'); ax.text(1.92, rho2 + 0.03, 'λ = ρ² = φ² (rectification level)', fontsize=6.3, color='#7a5c00')
pts = [(muTI, rho2, 'OG', RED), (5 ** .5, rho2, 'golden relatives', GOLD), ((13 + 6 * 5 ** .5) / 11, rho2, '', GOLD),
       (muTI, 3, 'pentakis dodecahedron', BLUE), (rho2, 3, 'RT', BLUE)]
for x, y, t, col in pts:
    ax.plot([x], [y], 'o', color=col, mec='#222', mew=0.4, ms=6)
    if t == 'OG': ax.text(x, y + 0.05, t, fontsize=6.6, ha='center', color=RED)
    elif t == 'golden relatives': ax.text(2.32, y - 0.12, 'golden relatives at μ = √5 and (13 + 6√5)/11', fontsize=6.3, ha='center')
    elif t: ax.text(x + 0.015, y + 0.06, t, fontsize=6.3)
ax.set_xlim(r2 - 0.03, 3.05); ax.set_ylim(2.35, 3.1); ax.tick_params(labelsize=6.5)
fig.text(0.62, 0.36, 'Polar Dharma cycle, exact:\n(3/φ³)D ⊂ S(φ²) ⊂ OG ⊂ H(μ_TI) ⊂ 3D* ⊂ (3/φ²)H(φ²) ⊂ 3D\n'
         'μ_TI = (24 + 9√5)/19 (truncated icosahedron), φ² = ρ²\n'
         'four middle stations: the 6D sections/hulls unscaled\nclosure φ³ (given); all links tight: 225/2 − 99√5/2',
         fontsize=6.9, va='top', color='#222')
fig.text(0.5, 0.965, 'OG and the polar Dharma cycle in the D·I sweep', ha='center', fontsize=8.4, weight='bold')
mark(fig); fig.savefig(os.path.join(OUT, 'fig2-og-dharma.png'), dpi=220, facecolor='white'); plt.close(fig)
# ------------------------------------------------------------------ fig 3: 4D lines
fig, axs = plt.subplots(3, 1, figsize=(9.4, 4.6)); plt.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.08, hspace=0.9)
d4 = [('tesseract × 16-cell (μ from 16-cell 1 to tesseract 4)', 1, 4,
       [(1, '16-cell', 'Q'), (3 - G, 'L-GCT', 'Q5'), (1.5, 'trunc. 16-cell', 'Q'), (G, 'G-GCT', 'Q5'), (2, '24-cell', 'Q'),
        (2 + 1 / G ** 2, 'Unborn+G-GCT', 'Q5'), (2.5, 'bitrunc.', 'Q'), (G * G, 'Icosaxes+L-GCT', 'Q5'), (3, 'rect. tess.', 'Q'),
        (1 + 2.304114, 'G-GCC', 'Q25'), (2 + R2, 'trunc. tess.', 'Q2'), (1 + 2.533609, 'L-GCC', 'Q25'), (4, 'tesseract', 'Q')]),
      ('24-cell × 24-cell (μ from 1 to 2; self-dual point √2)', 1, 2,
       [(1, '24-cell*', 'Q'), (2 / G, 'Icosaxes*', 'Q5'), (4 / 3, 'rect.*', 'Q'), (R2, 'bitruncated', 'Q2'), (1.5, 'rect.', 'Q'),
        (G, 'Icosaxes+cubes', 'Q5'), (5 / 3, 'trunc.', 'Q'), (1.7236068, 'Unborn+cubes', 'Q5'), (2, '24-cell', 'Q')]),
      ('600-cell × 120-cell (ν = μ/r², 120-cell end at 1)', 1, 1 / 0.8567627457812106,
       [(1, '120-cell', 'Q'), (0.863584 / 0.856763, 'L-GCD', 'Q5'), (0.865488 / 0.856763, 'trunc. 120', 'Q5'), (0.867308 / 0.856763, 'G-GCD', 'Q5'),
        (0.872678 / 0.856763, 'rect. 120', 'Q5'), (0.881966 / 0.856763, 'G-GCI+L-GCT', 'Q5'), (0.885410 / 0.856763, 'bitrunc.', 'Q5'),
        (0.889196 / 0.856763, 'L-GCI+G-GCT', 'Q5'), (0.904508 / 0.856763, 'rect. 600', 'Q5'), (0.927051 / 0.856763, 'G-GCT', 'Q5'),
        (0.936339 / 0.856763, 'trunc. 600', 'Q5'), (0.947214 / 0.856763, 'L-GCT', 'Q5'), (1 / 0.856763, '600-cell', 'Q5')])]
for ax, (t, a, b, P) in zip(axs, d4):
    ax.set_xlim(a - 0.02 * (b - a), b + 0.02 * (b - a)); ax.set_ylim(-2.0, 1.6); ax.axis('off'); ax.plot([a, b], [0, 0], color='#333', lw=1)
    ax.set_title(t, fontsize=7.6, loc='left')
    for k, (x, lab, f) in enumerate(P):
        ax.plot([x], [0], 'o', ms=5.5, color=FC[f], mec='#222', mew=0.4, zorder=4)
        ax.text(x, [0.5, -1.05, 1.15, -1.75][k % 4] if len(P) > 12 else (0.5 if k % 2 == 0 else -1.05), lab, ha='center', fontsize=5.9)
mark(fig); fig.savefig(os.path.join(OUT, 'fig3-fourd.png'), dpi=220, facecolor='white'); plt.close(fig)
# ------------------------------------------------------------------ fig 4: 24-cell honeycomb slice + Fibonacci word
def COm(m):
    V, N = pair(CUBE); return S(V, N, m)
fig = plt.figure(figsize=(9.4, 3.6))
hs = [(0, 'h = 0'), (1 / G ** 2, 'h = 1/φ²'), (0.5, 'h = 1/2'), (1 / G, 'h = 1/φ'), (1, 'h = 1')]
for k, (h, t) in enumerate(hs):
    for j, m in enumerate((2 - h, 1 + h)):
        ax = fig.add_axes([0.01 + k * 0.195, 0.52 - j * 0.0, 0.09, 0.34]) if j == 0 else fig.add_axes([0.10 + k * 0.195, 0.52, 0.09, 0.34])
        P = COm(m); draw(ax, faces(P), 1.75)
    fig.text(0.10 + k * 0.195, 0.9, t, ha='center', fontsize=7.6)
fig.text(0.10, 0.47, 'left: tile at 2Z³ = C ∩ (2 − h)O;  right: tile at 2Z³ + (1,1,1) = C ∩ (1 + h)O;  per BCC cell the volumes add to 8 for every h',
         fontsize=6.8)
word = json.load(open(os.path.join(os.path.dirname(OUT.rstrip('/')), 'data', 's7-hyper.json')))['station_word_4_letters_first40']
col4 = {'p': '#e9d48a', 'q': GOLD, 'r': TEAL, 's': '#7fd0c5'}
ax = fig.add_axes([0.04, 0.08, 0.88, 0.25]); ax.axis('off'); ax.set_xlim(0, 40); ax.set_ylim(0, 1.6)
for i, ch in enumerate(word):
    ax.add_patch(plt.Rectangle((i, 0.3), 0.92, 0.7, color=col4[ch])); ax.text(i + 0.46, 0.55, ch, ha='center', fontsize=6)
ax.text(0, 1.2, 'golden-tilted slice (first look): tile rows at heights {k/φ}; p: CO..Icosaxes, q: Icosaxes..Kelvin, r: Kelvin..Unborn Axes, '
        's: Unborn Axes..O.  p+q vs r+s is the Fibonacci word', fontsize=6.6)
mark(fig); fig.savefig(os.path.join(OUT, 'fig4-honeycomb-slices.png'), dpi=220, facecolor='white'); plt.close(fig)
print('written')
