"""Figures for the results note (house colours and renderer of the Star Cores figures, figs_paper_a.py: orthographic
painter, Lambert shading, dark edges; DICTO mark bottom right). Faces: gold = an original face that became a golden
truncated polygon (ratio phi); teal = an original face that became a regular polygon; lilac = a corner face.
usage (dicto-big-brother): python figs.py <out dir> <logo png>
"""
import json, os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import gcb

OUT, LOGO = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
G = gcb.g
GOLD, TEAL, LILAC, EDGE, GREY = '#d4af37', '#2bb3a3', '#c4a6ee', '#1d1d24', '#c9ccd3'
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
logo = plt.imread(LOGO)


def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz


def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT))
    return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))


def colour(P):
    L = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)
    if len(P) < 6: return LILAC
    if np.ptp(L) < 1e-7 * L.max(): return TEAL
    a, b = L[0::2], L[1::2]
    if np.ptp(a) < 1e-7 and np.ptp(b) < 1e-7 and abs(max(a[0], b[0]) / min(a[0], b[0]) - G) < 1e-7: return GOLD
    return GREY


def render(ax, W, title, view=(20, 24)):
    W = W - W.mean(0); F = gcb.faces(W); M = rot(*view); items = []
    for f in F:
        P = W[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        if n @ P.mean(0) < 0: n = -n
        nn = M @ n
        if nn[2] <= 1e-9: continue
        Q = P @ M.T; items.append((Q[:, 2].mean(), Q[:, :2], shade(colour(P), nn)))
    items.sort(key=lambda t: t[0])
    ax.add_collection(PolyCollection([t[1] for t in items], facecolors=[t[2] for t in items], edgecolors=EDGE, linewidths=0.5, joinstyle='round'))
    lim = 1.08 * np.linalg.norm(W, axis=1).max(); ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title, fontsize=8.5)


def mark(fig):
    a = fig.add_axes([0.925, 0.008, 0.065, 0.065 * fig.get_figwidth() / fig.get_figheight()]); a.imshow(logo); a.axis('off')


def cutA(name, x):
    V = gcb.archimedean(name); F = gcb.faces(V); return gcb.cut(V, F, [x] * len(V))[0]


xL3, xG5 = 1 / (G + 2), 1 / 3
# Figure 1: the icosidodecahedron and snub dodecahedron cuts, White Knight, and the depth chart
fig, axs = plt.subplots(2, 3, figsize=(10.5, 7.2), gridspec_kw=dict(wspace=0.22, hspace=0.2))
render(axs[0, 0], cutA('icosidodecahedron', xL3), 'icosidodecahedron, x = 1/(φ√5)\ntriangles golden, decagons regular')
render(axs[0, 1], cutA('icosidodecahedron', xG5), 'icosidodecahedron, x = 1/3\npentagons golden, hexagons regular')
wk = json.load(open(os.path.expanduser('~/kres-tmp/dataset-v7/solids/dicto-white-knight.json')))
render(axs[0, 2], np.array([[float(c) for c in v['decimal']] for v in wk['vertices']]), "White Knight (DICTO)\nsame faces, rectangles turned")
render(axs[1, 0], cutA('snub dodecahedron', xL3), 'snub dodecahedron, x = 1/(φ√5)\ntriangles golden, decagons regular')
render(axs[1, 1], cutA('snub dodecahedron', xG5), 'snub dodecahedron, x = 1/3\npentagons golden, hexagons regular')
ax = axs[1, 2]
ns = [3, 4, 5, 6, 8, 10]; k = [2 * np.cos(np.pi / n) for n in ns]
ax.plot(ns, [G / (c + 2 * G) for c in k], 'o-', color='#8e5bd6', label='greater: corner sides long')
ax.plot(ns, [1 / (G * c + 2) for c in k], 's-', color=TEAL, label='lesser: original sides long')
ax.plot(ns, [1 / (c + 2) for c in k], '^:', color='#888', label='regular 2n-gon')
ax.set_xlabel('face sides n', fontsize=8); ax.set_ylabel('cut x (edge 1)', fontsize=8); ax.tick_params(labelsize=7)
ax.set_xticks(ns); ax.legend(fontsize=6.5, frameon=False); ax.set_title('golden cut of an n-gon face:\none depth each, all different', fontsize=8.5)
ax.set_box_aspect(0.9)
mark(fig); fig.savefig(os.path.join(OUT, 'fig1-archimedean.png'), dpi=220, facecolor='white'); plt.close(fig)

# Figure 2: the rhombic Catalan golden cuts
rh = json.load(open(os.path.join(DATA, 's2b-rhombic.json')))['rhombic']
fig, axs = plt.subplots(1, 4, figsize=(10, 3.1), gridspec_kw=dict(wspace=0.03))
i = 0
for cat, r in rh.items():
    for c in r['cuts']:
        lab = c['cut'].split()[0]
        render(axs[i], np.array(c['vertices_edge1']), f'{cat}\n{lab}: a/b = {"φ" if lab == "greater" else "1/φ"}'); i += 1
mark(fig); fig.savefig(os.path.join(OUT, 'fig2-rhombic.png'), dpi=220, facecolor='white'); plt.close(fig)

# Figure 3: sections. Tesseract vertex-first at h = 1/phi^2, 1/2, 1/phi; 120-cell cell-first golden dodecahedra
sys.argv = [sys.argv[0]]
src = open(os.path.join(HERE, 's4_sections4d.py')).read().split('# ---------------------------------------------------------------- targets')[0]
NS = {'__file__': os.path.join(HERE, 's4_sections4d.py')}; exec(src, NS)
fig, axs = plt.subplots(1, 5, figsize=(10, 2.75), gridspec_kw=dict(wspace=0.03))
D, V, E = NS['directions']('8-cell'); d = D['vertex-first'] / np.linalg.norm(D['vertex-first'])
for ax, h, t in zip(axs[:3], (1 / G ** 2, .5, 1 / G), ('h = 1/φ²', 'h = 1/2', 'h = 1/φ')):
    P = NS['section'](V, E, d, h)       # d unit (1,1,1,1)/2: layer heights 0 and 1 as in s5
    render(ax, P, f'tesseract, vertex-first\n{t}')
m = json.load(open(os.path.join(DATA, 's4-sections4d.json')))['matches']
D, V, E = NS['directions']('120-cell'); d = D['cell-first'] / np.linalg.norm(D['cell-first']); top = (V @ d).max()
for ax, key, t in zip(axs[3:], ('dodecahedron greater', 'dodecahedron lesser'), ('1/φ²', '1/φ')):
    mm = next(r for r in m if r['solid'].startswith(key) and r['polytope'] == '120-cell')
    render(ax, NS['section'](V, E, d, mm['height']), f'120-cell, cell-first\n{t} of the gap')
mark(fig); fig.savefig(os.path.join(OUT, 'fig3-sections.png'), dpi=220, facecolor='white'); plt.close(fig)

# Figure 4: golden pentagons and pentagrams (Kepler-Poinsot faces), side by side
fig, axs = plt.subplots(1, 4, figsize=(10, 2.75), gridspec_kw=dict(wspace=0.05))
ang = np.pi / 2 + 2 * np.pi * np.arange(5) / 5; C = np.c_[np.cos(ang), np.sin(ang)]
for ax, step, x, t in zip(axs, (1, 1, 2, 2), (1 / 3, (7 - 5 ** .5) / 22, 1 / 3, (7 + 5 ** .5) / 22),
                          ('pentagon, x = 1/3\ngreater', 'pentagon, x = (7−√5)/22\nlesser', 'pentagram, x = 1/3\nlesser', 'pentagram, x = (7+√5)/22\ngreater')):
    order = [(step * i) % 5 for i in range(5)]; P = C[order]; P = P / np.linalg.norm(P[1] - P[0])
    ax.plot(*np.r_[P, P[:1]].T, ':', color='#999', lw=0.7)
    Q = []
    for i in range(5):
        u, v, w = P[i - 1], P[i], P[(i + 1) % 5]
        Q += [v + x * (u - v), v + x * (w - v)]
    Q = np.array(Q); ax.fill(*Q.T, color=GOLD, alpha=0.35, lw=0); ax.plot(*np.r_[Q, Q[:1]].T, '-', color=EDGE, lw=1.0)
    for j in range(10):
        a_, b_ = Q[j], Q[(j + 1) % 10]
        ax.plot(*np.c_[a_, b_], '-', color=('#8e5bd6' if j % 2 == 0 else EDGE), lw=1.6 if j % 2 == 0 else 1.0)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(t, fontsize=8.5)
mark(fig); fig.savefig(os.path.join(OUT, 'fig4-pentagrams.png'), dpi=220, facecolor='white'); plt.close(fig)
print('figures written to', OUT)
