"""Calibrating the wall method on the 2D hat family (DICTO 10 Nov: "yes calibrate on the 2D hat family"). Tile(a, b) (Smith, Myers,
Kaplan, Goodman-Strauss 2023): the hat's outline with its unit-type edges (directions multiples of 60°) scaled by a and its √3-type edges
(odd multiples of 30°) by b; hat = Tile(1, √3). Known answer: periodic at a = 0 (chevron), b = 0 (comet) and a = b (with reflections);
aperiodic otherwise. Slider t = b / (a + b) (a = 1 - t, b = t). Walls = where the set of possible side-by-side contacts of two copies
(any of 12 rotations/reflections, corner on corner, touching along an edge stretch, no overlap) changes. Scan t on a fine grid, refine
every change by bisection. Calibration passes if the walls are exactly t = 0, 1/2, 1."""
import math, sys, numpy as np
from shapely.geometry import Polygon
from shapely import affinity
s3 = math.sqrt(3)
HAT = [(0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1), (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2)]   # Kaplan's hatviz points, lattice coords
cart = lambda p: (p[0] + p[1] / 2, p[1] * s3 / 2)
P = [cart(p) for p in HAT]
E = [(P[(i + 1) % len(P)][0] - P[i][0], P[(i + 1) % len(P)][1] - P[i][1]) for i in range(len(P))]
kind = []
for e in E:
    L = math.hypot(*e); ang = math.degrees(math.atan2(e[1], e[0])) % 360
    kind.append('a' if abs(ang / 60 - round(ang / 60)) < 1e-9 else 'b')               # 60° multiples: a-type; odd 30°: b-type
lens = [math.hypot(*e) for e in E]
assert all(abs(l - (1 if k == 'a' else s3)) < 1e-9 or abs(l - 2) < 1e-9 for l, k in zip(lens, kind)), (lens, kind)
unitv = [(e[0] / (1 if k == 'a' else s3), e[1] / (1 if k == 'a' else s3)) for e, k in zip(E, kind)]   # a-edges keep length 1 or 2 (in units of a)
def tile(t):
    a, b = 1 - t, t; pts = [(0.0, 0.0)]
    for u, k in zip(unitv, kind):
        f = a if k == 'a' else b; pts.append((pts[-1][0] + f * u[0], pts[-1][1] + f * u[1]))
    assert math.hypot(*pts[-1]) < 1e-9, 'family does not close'
    return pts[:-1]
OR = [(r, m) for m in (False, True) for r in range(6)]
def oriented(pts, r, m):
    out = []
    for x, y in pts:
        if m: y = -y
        c, s = math.cos(math.radians(60 * r)), math.sin(math.radians(60 * r)); out.append((c * x - s * y, s * x + c * y))
    return out
def contacts(t, eps=1e-7):
    A = Polygon(tile(t)).buffer(0); va = list(A.exterior.coords)[:-1]; found = set()
    for r, m in OR:
        Bp = oriented(tile(t), r, m)
        for pa in va:
            for pb in Bp:
                dx, dy = pa[0] - pb[0], pa[1] - pb[1]; B = Polygon([(x + dx, y + dy) for x, y in Bp])
                if B.intersection(A).area > eps: continue
                if A.boundary.intersection(B.boundary).length < 1e-4: continue
                found.add((r, m, round(dx, 5), round(dy, 5)))
    # describe contacts scale-free: orientation + which corner pair (by index) meet; count distinct
    return len(found)
grid = [k / 200 for k in range(1, 200)]
print('START hat family: contact counts on t = b/(a+b) in (0, 1)', flush=True)
counts = []
for k, t in enumerate(grid):
    counts.append(contacts(t))
    if k % 20 == 0: print(f'PROGRESS {k / len(grid):.2f} t = {t:.3f}: {counts[-1]} contacts', flush=True)
walls = []
for k in range(len(grid) - 1):
    if counts[k] != counts[k + 1]:
        lo, hi = grid[k], grid[k + 1]; cl = counts[k]
        for _ in range(30):
            m = (lo + hi) / 2
            if contacts(m) == cl: lo = m
            else: hi = m
        walls.append(((lo + hi) / 2, counts[k], counts[k + 1]))
spots = {t: contacts(t) for t in (0.5, 1 / (1 + s3), s3 / (1 + s3))}
print('counts along the slider (every 0.05):', [counts[k] for k in range(9, 199, 10)])
print('walls found (t, count below, count above):', [(round(w, 6), a, b) for w, a, b in walls])
print(f'at t = 1/2: {spots[0.5]} contacts (neighbours {contacts(0.49)}, {contacts(0.51)}); hat t = {1/(1+s3)*s3:.4f}?')
ok = all(abs(w - 0.5) < 1e-6 for w, _, _ in walls) and spots[0.5] != contacts(0.49)
print('FINAL ok (walls exactly at 1/2 inside (0,1))' if ok else 'FINAL FAIL: walls other than 1/2 (or none at 1/2) - see list')
