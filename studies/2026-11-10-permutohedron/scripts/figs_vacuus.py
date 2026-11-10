"""Figures for the 4D Vacuus paper (11 Nov 2026). Exact geometry, drawn with matplotlib (solid faces, crisp edges, no haze).
  fig-web.png    the web of bonds: 120 orderings of 1..5 in rows by distance from 12345 (out-of-order pairs), the 240 bonds coloured by
                 which neighbouring values they swap; one of the 768 shortest routes 12345 -> 54321 in gold.
  fig-heart.png  the heart: one central slice (1..5 without the middle value) as a solid, its six squares (4D faces it carries) in gold,
                 and the four regular hexagons through its centre where it crosses the other four central slices.
  fig-dictonic.png  DICTONIC's T(x) at x = 1/2, 1, tau as permutohedra of (-q, -p, p, q), each with its four values on a line."""
import itertools, math, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial import ConvexHull
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
GOLD, VIOLET = '#c9a227', '#7a4fb5'
BOND = {1: '#2f6fb3', 2: '#3c9a5a', 3: '#c0392b', 4: '#7a4fb5'}           # swap of values k <-> k+1

# ---------- web of bonds ----------
n = 5; V = list(itertools.permutations(range(1, n + 1)))
inv = lambda p: sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
rows = {}
for p in V: rows.setdefault(inv(p), []).append(p)
pos = {}
for k, ps in rows.items():
    ps.sort(key=lambda p: sum((i - 2) * (p[i] - 3) for i in range(5)))          # a smooth left-right order
    for t, p in enumerate(ps): pos[p] = ((t - (len(ps) - 1) / 2) * 1.0, -k * 1.55)
def swap(p, k): return tuple(k + 1 if x == k else k if x == k + 1 else x for x in p)
fig, ax = plt.subplots(figsize=(10, 7.2), dpi=220)
for p in V:
    for k in range(1, 5):
        q = swap(p, k)
        if p < q:
            (x1, y1), (x2, y2) = pos[p], pos[q]; ax.plot([x1, x2], [y1, y2], color=BOND[k], lw=0.6, alpha=0.75, zorder=1)
route = [tuple(range(1, 6))]
for k in [4, 3, 4, 2, 3, 4, 1, 2, 3, 4]:                                       # a reduced word for 54321 (bubble sort in reverse)
    route.append(swap(route[-1], k))
assert route[-1] == (5, 4, 3, 2, 1) and len(set(route)) == 11
ax.plot([pos[p][0] for p in route], [pos[p][1] for p in route], color=GOLD, lw=3.2, zorder=2, solid_capstyle='round')
for p in V:
    x, y = pos[p]; on = p in route
    ax.scatter([x], [y], s=26 if on else 9, color=GOLD if on else '#222', zorder=3, edgecolors='white' if on else 'none', linewidths=0.6)
for p in (route[0], route[-1]):
    ax.annotate(''.join(map(str, p)), pos[p], xytext=(0, 9 if p == route[0] else -15), textcoords='offset points', ha='center', fontsize=10, fontweight='bold')
for k, ps in rows.items():
    ax.text(min(pos[p][0] for p in ps) - 1.2, -k * 1.55, f'{k}: {len(ps)}', ha='right', va='center', fontsize=7.5, color='#555')
for k, c in BOND.items(): ax.plot([], [], color=c, lw=2, label=f'swap {k} ↔ {k + 1}')
ax.plot([], [], color=GOLD, lw=3, label='a shortest route (one of 768)')
ax.legend(loc='lower right', fontsize=8, frameon=False); ax.set_axis_off(); ax.set_aspect('equal')
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
fig.savefig(f'{OUT}/fig-web.png', bbox_inches='tight'); plt.close(fig)

# ---------- 3D helpers ----------
H = np.array([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]) / 2.0          # orthonormal rows, orthogonal to (1,1,1,1): an isometry
def perm4(vals): return np.array(sorted(set(itertools.permutations(vals))), float)
def hullfaces(X):
    hh = ConvexHull(X); groups = {}
    for simp, eq in zip(hh.simplices, hh.equations): groups.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    faces = []
    for eq, idx in groups.items():
        idx = list(idx); c = X[idx].mean(0); nrm = np.array(eq[:3]); u = X[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(nrm, u)
        idx.sort(key=lambda i: math.atan2((X[i] - c) @ w, (X[i] - c) @ u)); faces.append(idx)
    return faces
def draw_solid(ax, X, faces, colour_of, alpha=1.0, edge='#222', lw=0.9):
    polys = [X[f] for f in faces]; cols = [colour_of(f) for f in faces]
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors=edge, linewidths=lw, alpha=alpha))
def view(ax, r):
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.view_init(elev=22, azim=-58)

# ---------- the heart ----------
P4 = perm4((-2, -1, 1, 2)); X = P4 @ H.T; F = hullfaces(X)
fig = plt.figure(figsize=(7.5, 7.5), dpi=220); ax = fig.add_subplot(111, projection='3d')
# the four crossing hexagons first, nearly solid; the slice as a see-through crystal shell over them (see-through shell standard)
HEXC = ['#7a4fb5', '#2f6fb3', '#3c9a5a', '#c0392b']
for j in range(4):
    pts = []
    for p in itertools.permutations((2, 0, -2)):
        y = list(p); y.insert(j, 0); pts.append(np.array(y, float) @ H.T)
    pts = np.array(pts); c = pts.mean(0); nrm = np.cross(pts[1] - pts[0], pts[2] - pts[0]); u = pts[0] - c; w = np.cross(nrm, u)
    order = sorted(range(6), key=lambda i: math.atan2((pts[i] - c) @ w, (pts[i] - c) @ u))
    ax.add_collection3d(Poly3DCollection([pts[order]], facecolors=[HEXC[j]], edgecolors=HEXC[j], linewidths=1.6, alpha=0.55))
ax.add_collection3d(Poly3DCollection([X[f] for f in F if len(f) == 4], facecolors=GOLD, edgecolors='#5a4a10', linewidths=1.2, alpha=0.85))
ax.add_collection3d(Poly3DCollection([X[f] for f in F if len(f) == 6], facecolors=(0.85, 0.88, 0.95, 0.06), edgecolors='#333', linewidths=1.0))
view(ax, 2.05)
fig.savefig(f'{OUT}/fig-heart.png', bbox_inches='tight'); plt.close(fig)

# ---------- DICTONIC T(x) as permutohedra ----------
tau = (1 + 5 ** 0.5) / 2
stops = [('x = 1/2', (-2, -1, 1, 2), 'heart of the 4D permutohedron'), ('x = 1 (Kelvin)', (-3, -1, 1, 3), 'the 3D permutohedron'),
         ('x = τ (golden bond)', (-tau ** 3, -1, 1, tau ** 3), 'values ±τ³, ±1')]
fig = plt.figure(figsize=(12, 5.2), dpi=220)
for k, (lab, vals, sub) in enumerate(stops):
    X = perm4(vals) @ H.T; X /= np.abs(X).max(); F = hullfaces(X)
    ax = fig.add_subplot(1, 3, k + 1, projection='3d')
    draw_solid(ax, X, F, lambda f: (0.93, 0.80, 0.35, 0.95) if len(f) == 4 else (0.42, 0.62, 0.86, 0.95), lw=0.8)
    view(ax, 0.95); ax.set_title(f'{lab}\n{sub}', fontsize=10)
    # the four values on a line
    ins = fig.add_axes([0.06 + k * 0.325, 0.20, 0.24, 0.06]); ins.set_axis_off(); m = max(abs(v) for v in vals)
    ins.plot([-1.05, 1.05], [0, 0], color='#888', lw=0.8)
    for v in vals: ins.plot([v / m], [0], 'o', color='#222', ms=4)
    ins.plot([0], [0], '|', color='#c0392b', ms=10); ins.set_xlim(-1.15, 1.15); ins.set_ylim(-1, 1)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
fig.savefig(f'{OUT}/fig-dictonic.png', bbox_inches='tight'); plt.close(fig)
import os
made = [f'{OUT}/{n}.png' for n in ('fig-web', 'fig-heart', 'fig-dictonic')]
ok = all(os.path.exists(m) and os.path.getsize(m) > 50000 for m in made)
print('FINAL ok' if ok else f'FINAL FAIL: missing or empty figures {made}')
