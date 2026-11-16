#!/usr/bin/env python3
"""Figure 2, the 600-cell in its five groups: the 120 corners coloured by S5-orbit (X, −X, R, F, −F), dark app ground.
Corners are exact (Q(√5)) from the queens-construct study (studies/2026-11-16-queens-construct/scripts/qlib.py, build_600):
the closure of X under reflection in its own members, split into the S5-orbits exactly as in that study's fig_orbits.py.
Floats are used for drawing only.
Projection: the Coxeter plane of H4 (the 30-fold view, four rings of 30), where all 120 corners are distinct. (Every plane
kept by an element of S5 stacks corners of different orbits on one another: 31, 45 and 37 distinct points for the 5-, 4- and
3-cycle planes, so no S5-symmetric plane shows all corners.) Depth for shading: a coordinate of the complementary plane.
Edges: the 720 edges of the 600-cell, depth-shaded. Corners: shaded balls, painted back to front with the edges.
Colours (element colours of the Kaleidohedra app): X Fire, −X Water, R Void, F Wind, −F Earth (see the caption).
Usage: fig_600orbits.py out.png  (ends FINAL ok / FINAL FAIL)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'studies', '2026-11-16-queens-construct', 'scripts'))
from qlib import build_600, vkey, vneg, flt
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

GROUND = '#05050a'; INK = '#e6e1d3'; DIM = '#8d8a82'
EL = {'Fire': (205, 62, 40), 'Water': (58, 112, 205), 'Void': (138, 92, 196), 'Wind': (232, 200, 82), 'Earth': (72, 142, 72)}
fails = []
def check(ok, msg):
    print(('CHECK ok   ' if ok else 'CHECK FAIL ') + msg, flush=True)
    if not ok: fails.append(msg)

P5, X, Y = build_600()
kX = {vkey(p) for p in X}; kmX = {vkey(vneg(p)) for p in X}; kF = {vkey(p) for p in Y}; kmF = {vkey(vneg(p)) for p in Y}
def lab(p):
    k = vkey(p)
    return 0 if k in kX else 1 if k in kmX else 3 if k in kF else 4 if k in kmF else 2
L = np.array([lab(p) for p in P5]); A = np.array([flt(p) for p in P5]); A = A / np.linalg.norm(A, axis=1)[:, None]
check(len(P5) == 120 and [int((L == i).sum()) for i in range(5)] == [20, 20, 20, 30, 30], 'exact 600-cell: orbits 20, 20, 20, 30, 30')
R = A[L == 2]
check(np.allclose(np.sort(np.abs(np.round(R * np.sqrt(2), 9)), axis=1), np.tile([0, 0, 0, 1, 1], (20, 1))), 'R is the 20 A4 roots ±(e_i − e_j)/√2')
G = A @ A.T; PHI = (1 + 5 ** 0.5) / 2
E = [(i, j) for i in range(120) for j in range(i + 1, 120) if abs(G[i, j] - PHI / 2) < 1e-9]
check(len(E) == 720, f'720 edges (cosine φ/2): {len(E)}')

# 4D coordinates on the sum-zero hyperplane, then the Coxeter plane of H4: the eigenplane (angle 2π/30) of a Coxeter element,
# a product of four reflections in corners whose eigen-angles are 2π·1/30 and 2π·11/30 (found by a seeded search, then checked).
Bm = np.linalg.qr(np.array([[1, -1, 0, 0, 0], [0, 1, -1, 0, 0], [0, 0, 1, -1, 0], [0, 0, 0, 1, -1]], float).T)[0].T
A4 = A @ Bm.T
def refl(r): return np.eye(4) - 2 * np.outer(r, r)
rng = np.random.default_rng(0); C = None
for _ in range(50000):
    M = np.eye(4)
    for i in rng.choice(120, 4, replace=False): M = M @ refl(A4[i])
    w = np.linalg.eigvals(M)
    if sorted(set(np.round(np.abs(np.angle(w)) * 30 / (2 * np.pi), 6))) == [1.0, 11.0]: C = M; break
check(C is not None and np.allclose(np.linalg.matrix_power(C, 30), np.eye(4)) and not np.allclose(np.linalg.matrix_power(C, 15), np.eye(4)),
      'Coxeter element of H4 found: order 30, eigen-angles 2π/30 and 22π/30')
w, V = np.linalg.eig(C)
def plane(theta):
    j = int(np.argmin(np.abs(np.angle(w) - theta))); u, v = V[:, j].real.copy(), V[:, j].imag.copy()
    u /= np.linalg.norm(u); v -= u * (u @ v); v /= np.linalg.norm(v); return u, v
u, v = plane(2 * np.pi / 30); u2, v2 = plane(2 * np.pi * 11 / 30)
check(abs(u @ u2) < 1e-9 and abs(v @ v2) < 1e-9 and abs(u @ v2) < 1e-9, 'the two eigenplanes are orthogonal')
xy = np.c_[A4 @ u, A4 @ v]
k0 = int(np.argmax(np.where(L == 2, np.hypot(*xy.T), -1)))       # turn the picture so that one outer R corner points up
t = np.pi / 2 - np.arctan2(xy[k0, 1], xy[k0, 0]); xy = xy @ np.array([[np.cos(t), np.sin(t)], [-np.sin(t), np.cos(t)]])
rr = np.round(np.hypot(*xy.T), 6)
check(len({tuple(np.round(p, 6)) for p in xy}) == 120, '120 distinct points in the Coxeter plane (no corner hidden)')
check(sorted(np.unique(rr, return_counts=True)[1].tolist()) == [30, 30, 30, 30], 'four rings of 30')
check(all(np.allclose(np.sort(xy[L == a], 0), np.sort(-xy[L == b], 0)) for a, b in ((0, 1), (3, 4), (2, 2))),
      'the half-turn of the picture (−1) swaps X with −X and F with −F and keeps R')
z = A4 @ u2; z = (z - z.min()) / np.ptp(z)      # depth: one coordinate of the complementary plane
D = np.linalg.norm(xy[:, None] - xy[None], axis=-1) + np.eye(120) * 9; sep = D.min() / np.abs(xy).max()
rad = 0.36 * sep * np.abs(xy).max()
check(rad > 0, 'ball radius positive')
W_IN, H_IN, DPI = 10.0, 7.0, 220
fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=GROUND)
ax = fig.add_axes([0.01, 0.03, 0.66, 0.94]); ax.set_facecolor(GROUND); ax.set_aspect('equal'); ax.axis('off')
lim = np.abs(xy).max() * 1.06 + rad; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
check(abs((ax.get_position().width * W_IN) - (ax.get_position().height * H_IN)) < 0.01, 'square model frame: one scale for x and y')
NAMES = [('X', 'golden, hull = solid A', 'Fire'), ('−X', 'its mirror image', 'Water'), ('R = C3', 'A4 roots, hull = expanded 5-cell', 'Void'),
         ('F', 'golden, hull = solid B', 'Wind'), ('−F', 'its mirror image', 'Earth')]
COL = [np.array(EL[n[2]]) / 255 for n in NAMES]
items = [('e', (z[i] + z[j]) / 2, (i, j)) for i, j in E] + [('b', z[i] + 1e-3, i) for i in range(120)]
for kind, dz, it in sorted(items, key=lambda t: t[1]):
    if kind == 'e':
        i, j = it; g = 0.22 + 0.5 * dz
        ax.plot([xy[i, 0], xy[j, 0]], [xy[i, 1], xy[j, 1]], color=(g, g * 0.97, g * 0.92), lw=0.55 + 0.35 * dz, solid_capstyle='round', zorder=1 + dz)
    else:
        i = it; c = COL[L[i]] * (0.55 + 0.45 * dz); r = rad * (0.85 + 0.3 * dz)
        ax.add_patch(Circle(xy[i], r, color=tuple(np.clip(c * 0.55, 0, 1)), zorder=1 + dz + 1e-4))       # dark rim
        for f, w in ((0.86, 0.0), (0.62, 0.30), (0.36, 0.62)):                                        # lit, solid shading
            ax.add_patch(Circle(xy[i] + np.array([-0.18, 0.18]) * r * (1 - f), r * f, color=tuple(np.clip(c * (1 - w) + w, 0, 1)), zorder=1 + dz + 2e-4))
# legend
for k, (nm, sub, el) in enumerate(NAMES):
    y = 0.80 - k * 0.12; n = int((L == k).sum())
    lax = fig.add_axes([0.69, y - 0.02, 0.04, 0.04 * W_IN / H_IN]); lax.set_aspect('equal'); lax.axis('off'); lax.set_xlim(-1, 1); lax.set_ylim(-1, 1)
    lax.add_patch(Circle((0, 0), 0.9, color=tuple(COL[k] * 0.55)));
    for f, w in ((0.86, 0.0), (0.62, 0.30), (0.36, 0.62)): lax.add_patch(Circle((-0.16 * (1 - f), 0.16 * (1 - f)), 0.9 * f, color=tuple(np.clip(COL[k] * (1 - w) + w, 0, 1))))
    fig.text(0.745, y + 0.012, f'{nm}  ({n} corners)', color=tuple(np.clip(COL[k] * 1.15, 0, 1)), fontsize=11, va='center')
    fig.text(0.745, y - 0.025, f'{sub}; {el}', color=DIM, fontsize=8.4, va='center')
fig.text(0.69, 0.94, 'The 600-cell: 120 corners,', color=INK, fontsize=11.5)
fig.text(0.69, 0.905, 'five S5-orbits', color=INK, fontsize=11.5)
fig.text(0.69, 0.16, 'Coxeter plane of H4 (30-fold view);', color=DIM, fontsize=8.2)
fig.text(0.69, 0.13, 'opposite corners: Fire–Water, Wind–Earth, Void–Void.', color=DIM, fontsize=8.2)
fig.text(0.985, 0.02, 'DICTO · dictospheres.com', color='#9a978f', fontsize=8, ha='right', va='bottom')
fig.savefig(sys.argv[1], dpi=DPI, facecolor=GROUND)
from PIL import Image
im = Image.open(sys.argv[1]); check(im.size == (int(W_IN * DPI), int(H_IN * DPI)), f'frame {im.size} at the asserted aspect')
print('FINAL ok' if not fails else 'FINAL FAIL', flush=True)
