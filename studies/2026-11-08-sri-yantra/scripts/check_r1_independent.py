"""Independent check of the rational Sri Yantra R1 (written apart from model.py): rebuild the nine triangles from
data/quadratic-examples.json alone (base depth b_i, half-width w_i, apex depth; depth measured from the top of a circle of
diameter 1), and with exact fractions count every point inside the circle where THREE or more triangle sides meet. Also which
base corners lie exactly on the circle. Expect 18 triple points (the marmas)."""
import json, itertools
from fractions import Fraction as F
d = json.load(open('data/quadratic-examples.json'))['R1']
g = lambda x: F(x['a']) if isinstance(x, dict) else F(x)
T = {i: (g(d['b'][str(i)]), g(d['w'][str(i)]), g(d['apex'][str(i)])) for i in range(1, 10)}
segs = []   # (point p, point q): segment endpoints, coordinates (x, depth)
for i, (b, w, a) in T.items():
    L, R, A = (-w, b), (w, b), (F(0), a)
    segs += [(L, R, i), (L, A, i), (R, A, i)]
def inter(s, t):
    (x1, y1), (x2, y2), _ = s; (x3, y3), (x4, y4), _ = t
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0: return None
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    on = lambda p, q, r: min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])
    P = (px, py)
    return P if on(s[0], s[1], P) and on(t[0], t[1], P) else None
pts = {}
for s, t in itertools.combinations(segs, 2):
    P = inter(s, t)
    if P is not None: pts.setdefault(P, set()).update({id(s), id(t)})
corners = {(x, y) for (b, w, a) in T.values() for (x, y) in [(-w, b), (w, b), (0, a)]}
triple = [P for P, ls in pts.items() if len(ls) >= 3 and P not in corners and P[0] ** 2 + (P[1] - F(1, 2)) ** 2 < F(1, 4)]
oncircle = sorted(i for i, (b, w, a) in T.items() if w * w + (b - F(1, 2)) ** 2 == F(1, 4))
apex_on_circle = sorted(i for i, (b, w, a) in T.items() if a in (0, 1))
print('triple points (three or more sides through one point, not a corner):', len(triple))
print('triangles with base corners exactly on the circle:', oncircle, '| apexes on the circle:', apex_on_circle)
ok = len(triple) >= 18
print('FINAL ok' if ok else 'FINAL FAIL: fewer than 18 exact triple points')
