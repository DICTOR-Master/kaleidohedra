# Figure (DICTO 2026-10-14): Pacioli's three golden rectangles and the 20 Cleo-Icos. (a) the 20 Cleo-Icos pulled slightly apart with the
# three rectangles through the centre; (b) the rectangles alone, each cut by its diagonals: the short-side triangles (63.43° at the
# centre, Cleo-Icos side faces) wisteria, the long-side triangles (116.57°) gold. DICTO · dictospheres.com
import itertools, json, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
phi = (1 + 5 ** .5) / 2
V = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float) / 2
F = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(V[a] - V[b]) - 1) < 1e-9 for a, b in itertools.combinations(t, 2))]
def rect(z):
    P = [p for p in V if abs(p[z]) < 1e-9]; c = np.zeros(3); n = np.eye(3)[z]; u = P[0] / np.linalg.norm(P[0]); w = np.cross(n, u)
    return sorted(P, key=lambda p: np.arctan2(p @ w, p @ u))
RECTS = [rect(z) for z in range(3)]
def mesh(items):
    v, f, t = [], [], []
    for tag, polys in items:
        for P in polys:
            b = len(v); v += [list(map(float, p)) for p in P]; f.append(list(range(b, b + len(P)))); t.append(tag)
    return dict(v=v, f=f, t=t)
def slab(P, n, th=0.006):    # a thin plate so the rectangle shows from both sides
    P = np.array(P); top = P + n * th; bot = P - n * th; out = [list(top), list(bot[::-1])]
    for k in range(len(P)): out.append([top[k], top[(k + 1) % len(P)], bot[(k + 1) % len(P)], bot[k]])
    return out
a_items = []
for f in F:
    c = V[list(f)].mean(0); d = c / np.linalg.norm(c) * 0.42; T = [np.zeros(3) + d] + [V[i] + d for i in f]
    a_items.append(('w1', [[T[1], T[2], T[3]], [T[0], T[2], T[1]], [T[0], T[3], T[2]], [T[0], T[1], T[3]]]))
for z, R in enumerate(RECTS): a_items.append(('w2', slab(R, np.eye(3)[z])))
b_items = []
for z, R in enumerate(RECTS):
    n = np.eye(3)[z]
    for k in range(4):
        p, q = R[k], R[(k + 1) % 4]; short = abs(np.linalg.norm(p - q) - 1) < 1e-9
        b_items.append(('w1' if short else 'w2', slab([np.zeros(3), p, q], n, 0.004)))
json.dump({'pac_a': mesh(a_items), 'pac_b': mesh(b_items)}, open(os.path.join(ROOT, 'paper', 'figures', 'pacioli.json'), 'w'))
print('ok')
