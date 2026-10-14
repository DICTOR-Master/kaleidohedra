# Figure (DICTO 2026-10-14): Pacioli's three golden rectangles and the 20 Cleo-Icos. (a) crystal view: all 20 Cleo-Icos as glass (the 6 on the rectangles' short sides wisteria), and the
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
# (a) DICTO 2026-10-14: the icosahedron mostly empty: its edges as thin rods, and only the Cleo-Icos the rectangles define, one on each
# of the 6 short sides (the face on the side of that edge away from the rectangle's plane's first axis), with the three rectangles.
def rod(p, q, r=0.012):
    d = q - p; d /= np.linalg.norm(d); e1 = np.cross(d, [1, 0, 0] if abs(d[0]) < .9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
    ring = [r * (np.cos(t) * e1 + np.sin(t) * e2) for t in np.linspace(0, 2 * np.pi, 7)[:-1]]
    return [[p + ring[k], p + ring[(k + 1) % 6], q + ring[(k + 1) % 6], q + ring[k]] for k in range(6)]
defining = set()
for z, R in enumerate(RECTS):
    for k in range(4):
        p, q = R[k], R[(k + 1) % 4]
        if abs(np.linalg.norm(p - q) - 1) > 1e-9: continue
        f = [t for t in F if all(any(np.allclose(V[i], x) for i in t) for x in (p, q))]
        defining.add(max(f, key=lambda t: V[list(t)].mean(0) @ np.roll(np.eye(3)[z], 1)))
# crystal: all 20 Cleo-Icos as glass, the 6 the rectangles define in wisteria, the other 14 pale blue
for f in F:
    T = [np.zeros(3)] + [V[i] for i in f]
    a_items.append(('w1g' if f in defining else 'w5g', [[T[1], T[2], T[3]], [T[0], T[2], T[1]], [T[0], T[3], T[2]], [T[0], T[1], T[3]]]))
for z, R in enumerate(RECTS): a_items.append(('w2', slab(R, np.eye(3)[z])))
b_items = []
for z, R in enumerate(RECTS):
    n = np.eye(3)[z]
    for k in range(4):
        p, q = R[k], R[(k + 1) % 4]; short = abs(np.linalg.norm(p - q) - 1) < 1e-9
        b_items.append(('w1' if short else 'w2', slab([np.zeros(3), p, q], n, 0.004)))
json.dump({'pac_a': mesh(a_items), 'pac_b': mesh(b_items)}, open(os.path.join(ROOT, 'paper', 'figures', 'pacioli.json'), 'w'))
print('ok')
