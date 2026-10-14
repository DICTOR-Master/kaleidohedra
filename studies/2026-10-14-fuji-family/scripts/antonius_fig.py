# Figure data for the Cleo-Icos & Antonius section (DICTO, 2026-10-14): (a) one golden rhombohedron = Cleo-Icos + Antonius + Cleo-Icos,
# pulled apart along its axis; (b) 8 rhombohedra (2 x 2 x 2) filling space, pulled apart; (c) the rhombic hexecontahedron as 20 Cleo-Icos
# + 20 Antonius + 20 Cleo-Icos, pulled apart. Colours: Cleo-Icos w1 (wisteria), Antonius w0 (cyan). DICTO · dictospheres.com
import itertools, json, os
import numpy as np
from scipy.spatial import ConvexHull
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
phi = (1 + 5 ** .5) / 2
V = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float) / 5 ** .5
E = 2 / 5 ** .5
F = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(V[a] - V[b]) - E) < 1e-9 for a, b in itertools.combinations(t, 2))]
def split(u, v, w, t=np.zeros(3)):
    s = u + v + w
    return [('w1', np.array([t, t + u, t + v, t + w])), ('w0', np.array([u, v, w, u + v, v + w, w + u]) + t), ('w1', np.array([t + s, t + s - u, t + s - v, t + s - w]))]
def mesh(parts, push):
    verts, faces, tags = [], [], []
    for tag, P, d in parts:
        Q = P + d * push; h = ConvexHull(Q); b0 = len(verts); verts += Q.tolist()
        for e in np.unique(np.round(h.equations, 9), axis=0):
            on = np.where(np.abs(Q @ e[:3] + e[3]) < 1e-7)[0]; c = Q[on].mean(0); a = Q[on[0]] - c; a /= np.linalg.norm(a); bb = np.cross(e[:3], a)
            faces.append([int(b0 + i) for i in on[np.argsort(np.arctan2((Q[on] - c) @ bb, (Q[on] - c) @ a))]]); tags.append(tag)
    return dict(v=verts, f=faces, t=tags)
a, b, c = F[0]; u, v, w = V[a], V[b], V[c]; ax = (u + v + w) / np.linalg.norm(u + v + w)
one = [(t, P, ax * (k - 1)) for k, (t, P) in enumerate(split(u, v, w))]
block = []
for i, j, k in itertools.product((0, 1), repeat=3):
    t = i * u + j * v + k * w
    block += [(tg, P, (t + (u + v + w) / 2) * 0.35 + ax * (n - 1) * 0.12) for n, (tg, P) in enumerate(split(u, v, w, t))]
rhex = []
for f in F:
    p, q, r = V[list(f)]; d = (p + q + r) / np.linalg.norm(p + q + r)
    rhex += [(tg, P, d * (0.12 + 0.18 * n)) for n, (tg, P) in enumerate(split(p, q, r))]
json.dump({'ant_one': mesh(one, 0.18), 'ant_block': mesh(block, 1.0), 'ant_rhex': mesh(rhex, 1.0)}, open(os.path.join(ROOT, 'paper', 'figures', 'antonius.json'), 'w'))
print('axis', ax.round(5).tolist())
