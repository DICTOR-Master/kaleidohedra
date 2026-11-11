"""Platonic book Ch11: the icosahedron shares 4D space only with the tetrahedron. Take the 600-cell's 120 corners (the 8 + 16 + 96
standard ones), remove the 24 of its inscribed 24-cell (the 8 axis points and 16 half-integer points), take the hull of the other 96:
count its cells and check they are 24 regular icosahedra and 120 regular tetrahedra (the snub 24-cell). Control: the full 600-cell's hull
has 600 regular tetrahedra."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
V = [s * 2 * np.eye(4)[i] for i in range(4) for s in (1, -1)] + [np.array(s, float) for s in itertools.product((1, -1), repeat=4)]
ev = [p for p in itertools.permutations(range(4)) if sum(p[a] > p[b] for a in range(4) for b in range(a + 1, 4)) % 2 == 0]
for p in ev:
    for s in itertools.product((1, -1), repeat=3):
        b = [s[0] * phi, s[1], s[2] / phi, 0]; v = np.zeros(4)
        for i in range(4): v[p[i]] = b[i]
        V.append(v)
V = np.unique(np.round(np.array(V), 9), axis=0); assert len(V) == 120
def cells(P):
    h = ConvexHull(P); G = {}
    for s, eq in zip(h.simplices, h.equations): G.setdefault(tuple(np.round(eq, 6)), set()).update(s)
    out = []
    for idx in G.values():
        Q = P[list(idx)]; d = np.linalg.norm(Q[:, None] - Q[None], axis=2); e = d[d > 1e-9].min()
        deg = ((np.abs(d - e) < 1e-6).sum(1))
        kind = {(4, 3): 'tetrahedron', (12, 5): 'icosahedron'}.get((len(Q), int(deg.max())), f'{len(Q)} corners') if deg.min() == deg.max() else 'irregular'
        out.append(kind)
    from collections import Counter
    return Counter(out)
full = cells(V); print('600-cell cells:', dict(full))
keep = [v for v in V if not (np.isclose(np.abs(v).max(), 2) and np.sum(np.abs(v) > 1e-9) == 1) and not np.allclose(np.abs(v), 1)]
snub = cells(np.array(keep)); print(len(keep), 'corners left; cells:', dict(snub))
print('FINAL ok' if full == {'tetrahedron': 600} and snub == {'icosahedron': 24, 'tetrahedron': 120} else 'FINAL FAIL')
