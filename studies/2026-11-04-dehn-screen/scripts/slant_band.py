"""DICTO 4 Nov: banded half-cells with a LEANING hexagonal prism band ("slanted hexagonal prisms with a double angle"). Bottom half B (hexagon at z=0),
band from z=0 to z=t leaning by s (top hexagon = bottom hexagon + (s, t)), top half T placed on the top hexagon (straight or twisted 60°).
Chevron: two leaning prisms, s then back by -s (total shift 0). Convex iff hull volume = sum of the parts. Directions s: toward the upper-layer balls
(angles 30, 150, 270°) and toward the other holes (90, 210, 330°), length k/√3 (k = 1 is one hole offset)."""
import math, itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('scripts/halfcell.py').read().split('print("RD"')[0])
T = half(RD, True); B = half(RD, False); hexa = T[np.abs(T[:, 2]) < 1e-9]
vT, vB = ConvexHull(T).volume, ConvexHull(B).volume; A_hex = ConvexHull(hexa[:, :2]).volume
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
def banded(sx, sy, t, twist=False, chevron=False):
    if chevron:
        mid = hexa + np.array([sx, sy, t/2]); top = hexa + np.array([0, 0, t]); band = np.vstack([hexa, mid, top]); shift = np.array([0, 0, t])
    else:
        top = hexa + np.array([sx, sy, t]); band = np.vstack([hexa, top]); shift = np.array([sx, sy, t])
    TT = (T @ rz(math.pi/3).T if twist else T) + shift
    U = np.unique(np.round(np.vstack([B, band, TT]), 9), axis=0); hu = ConvexHull(U)
    parts = vT + vB + A_hex*t
    return abs(hu.volume - parts) < 1e-7*parts, hu.volume/parts
print('hexagon area', round(A_hex, 6), '| upright band (s = 0), t = 0.3: convex', banded(0, 0, .3)[0], '| twisted', banded(0, 0, .3, True)[0])
for dname, angs in (('toward upper balls', (30, 150, 270)), ('toward other holes', (90, 210, 330))):
    for k in (0.25, 0.5, 1.0):
        for t in (0.2, 0.5, 1.0):
            r = []
            for tw in (False, True):
                c, q = banded(k/math.sqrt(3)*math.cos(math.radians(angs[0])), k/math.sqrt(3)*math.sin(math.radians(angs[0])), t, tw); r.append(f"{'twist' if tw else 'straight'} {'CONVEX' if c else f'dented ({q:.3f})'}")
            print(f'lean {dname}, k={k}, band t={t}: ' + ', '.join(r))
for k in (0.25, 1.0):
    for t in (0.5, 1.0):
        c, q = banded(k/math.sqrt(3), 0, t, chevron=True); print(f'chevron (out and back), k={k}, t={t}: {"CONVEX" if c else f"dented ({q:.3f})"}')
