#!/usr/bin/env python3
"""God's Dice figure. DICTO · dictospheres.com
(a) the uniform truncated cube S(1+sqrt2), cube-family green (#488e48, element colours), solid faces, crisp edges.
(b) solid-angle face probabilities along the line S(mu) = cube ∩ mu·octahedron, with the stations; neutral palette.
Run: python fig_gods_dice.py (numpy, matplotlib). Output figures/gods-dice.png; FINAL line conditional."""
import itertools, math, os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__)); FIG = os.path.join(HERE, '..', 'figures'); os.makedirs(FIG, exist_ok=True)
GREEN = '#488e48'; INK = '#2b2b2b'; GREY = '#8a8a8a'; BG = '#fbfaf6'
r2 = math.sqrt(2); a = r2 - 1

def pC(mu):
    if mu <= 2:
        b = mu - 1; return math.atan(b * b / 2 / math.sqrt(1 + b * b)) / math.pi
    t = mu - 2; tt = (1 - t)**2 * (t + 2) / (math.sqrt(t * t + 2) * (t * t + 6 * t + 5))
    return 1 / 6 - 2 * math.atan(tt) / (3 * math.pi)

# truncated cube faces
V = set()
for p in itertools.permutations((1, 1, a)):
    for s in itertools.product((1, -1), repeat=3): V.add(tuple(x * y for x, y in zip(p, s)))
V = np.array(sorted(V))
faces = []
for n, off in [(e * s, 1) for e in np.eye(3) for s in (1, -1)] + [(np.array(s, float), 1 + r2) for s in itertools.product((1, -1), repeat=3)]:
    on = V[np.abs(V @ n - off) < 1e-9]; c = on.mean(0)
    e1 = on[0] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(n / np.linalg.norm(n), e1)
    ang = np.arctan2((on - c) @ e2, (on - c) @ e1); faces.append((on[np.argsort(ang)], n / np.linalg.norm(n)))
ok_faces = len(faces) == 14 and sum(len(f[0]) == 8 for f in faces) == 6 and sum(len(f[0]) == 3 for f in faces) == 8

fig = plt.figure(figsize=(11, 4.9), facecolor=BG)
ax = fig.add_subplot(1, 2, 1, projection='3d'); ax.set_facecolor(BG)
light = np.array([0.4, -0.55, 0.75]); light /= np.linalg.norm(light)
base = np.array(matplotlib.colors.to_rgb(GREEN))
for poly, n in faces:
    sh = 0.62 + 0.38 * max(0, n @ light)
    col = np.clip(base * sh + (1 - sh) * 0.05, 0, 1)
    pc = Poly3DCollection([poly], facecolor=col, edgecolor='#1d3a1d', linewidths=1.1, alpha=1.0)
    ax.add_collection3d(pc)
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1); ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=22, azim=-58); ax.set_axis_off()
ax.set_title('(a) the uniform truncated cube, μ = 1 + √2\neach octagon 0.15111, each triangle 0.01166\n(solid-angle model)',
             fontsize=10, color=INK)

bx = fig.add_subplot(1, 2, 2); bx.set_facecolor(BG)
ms = np.linspace(1, 3, 801)
P = np.array([pC(m) for m in ms]); Q = (1 - 6 * P) / 8
bx.plot(ms, P, color=INK, lw=2, label='each of the 6 faces on the cube planes')
bx.plot(ms, Q, color=GREY, lw=2, ls='--', label='each of the 8 faces on the octahedron planes')
bx.axhline(1 / 14, color='#b0b0b0', lw=0.9); bx.text(1.02, 1 / 14 + 0.003, '1/14', fontsize=9, color=INK)
muf = 1.7565821359450421
stations = [(1.5, 'Kelvin 3/2'), ((1 + 5**.5) / 2, 'φ'), (3**.5, '√3 (turn)'), (muf, 'fair die'), (2, 'cuboctahedron'), (1 + r2, 'truncated cube 1+√2')]
for m, lab in stations:
    bx.axvline(m, color='#d0d0d0', lw=0.8, zorder=0)
place = {'Kelvin 3/2': (0.006, 'left', 0.168, 'top'), 'φ': (-0.006, 'right', 0.168, 'top'), '√3 (turn)': (-0.006, 'right', 0.168, 'top'),
         'fair die': (0.006, 'left', 0.168, 'top'), 'cuboctahedron': (0.006, 'left', 0.047, 'bottom'), 'truncated cube 1+√2': (0.006, 'left', 0.022, 'bottom')}
for m, lab in stations:
    dx, ha, y, va = place[lab]
    bx.text(m + dx, y, lab, fontsize=8.5, color=INK, rotation=90, ha=ha, va=va)
bx.plot([muf], [1 / 14], 'o', color=INK, ms=5)
bx.plot([1 + r2, 1 + r2], [pC(1 + r2), (1 - 6 * pC(1 + r2)) / 8], 'o', color=GREEN, ms=6)
bx.set_xlim(1, 3); bx.set_ylim(0, 0.17)
bx.set_xlabel('μ   (octahedron 1 → cube 3)', color=INK); bx.set_ylabel('probability of one face', color=INK)
bx.set_title('(b) face probabilities along the line: fair only at μ_f = 1.75658', fontsize=10, color=INK)
bx.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=8.5, frameon=False)
for sp_ in bx.spines.values(): sp_.set_color('#999999')
bx.tick_params(colors=INK)
fig.text(0.995, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=8, color='#a08a3c')
fig.suptitle("God's Dice: the truncated cube as a die", fontsize=12.5, color=INK, y=0.995)
plt.tight_layout(rect=(0, 0.02, 1, 0.96))
out = os.path.join(FIG, 'gods-dice.png'); fig.savefig(out, dpi=170, facecolor=BG)
ok = ok_faces and abs(pC(muf) - 1 / 14) < 1e-12 and abs(pC(1 + r2) - 0.1511142798897884) < 1e-12 and os.path.getsize(out) > 20000
print('wrote', out); print('FINAL ok' if ok else 'FINAL FAIL')
