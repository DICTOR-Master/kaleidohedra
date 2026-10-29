# The five stages between the White Queen (600-cell) and the Red Queen (120-cell) (DICTO 2026-10-30), by Wythoff's construction:
# from one flag of the 600-cell (corner v, edge middle e, triangle centre f, cell centre c) the four mirrors are the hyperplanes
# through the origin and three of these points; a stage is the orbit, under the reflections, of the point at distance 1 from its
# ringed mirrors and on the others. Rings: 600-cell {v}, truncated 600-cell {v,e}, rectified {e}, bitruncated {e,f},
# rectified 120-cell {f}, truncated 120-cell {f,c}, 120-cell {c} (ring X = the mirror opposite point X). Numerical check
# (exact Q(sqrt5) form after): corners, edges all one length, cells by kind (corners, edges) from the convex hull.
import numpy as np, itertools, json, sys
phi = (1 + 5 ** .5) / 2
V = set()
for i in range(4):
    for s in (1, -1): v = [0.0] * 4; v[i] = s; V.add(tuple(v))
for s in itertools.product((.5, -.5), repeat=4): V.add(s)
base = (phi / 2, .5, 1 / (2 * phi), 0)
even = [p for p in itertools.permutations(range(4)) if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0]
for p in even:
    for s in itertools.product((1, -1), repeat=3):
        v = [0.0] * 4; vals = [base[0] * s[0], base[1] * s[1], base[2] * s[2], 0]
        for k in range(4): v[p[k]] = vals[k]
        V.add(tuple(round(x, 12) + 0.0 for x in v))
V = np.array(sorted(V)); assert len(V) == 120
D = np.linalg.norm(V[:, None] - V[None], axis=2); e0 = D[D > 1e-9].min()
nb = lambda i: [j for j in range(120) if abs(D[i, j] - e0) < 1e-9]
a = 0; b = nb(a)[0]; c = [k for k in nb(a) if k in nb(b)][0]; d = [k for k in nb(a) if k in nb(b) and k in nb(c) and k != c][0]
F = {'v': V[a], 'e': (V[a] + V[b]) / 2, 'f': (V[a] + V[b] + V[c]) / 3, 'c': (V[a] + V[b] + V[c] + V[d]) / 4}
keys = 'vefc'
N = {}
for X in keys:
    others = np.array([F[Y] for Y in keys if Y != X])
    n = np.linalg.svd(others)[2][-1]; n = n if n @ F[X] > 0 else -n; N[X] = n / np.linalg.norm(n)
adjs = {i: set(j for j in range(120) if abs(D[i, j] - e0) < 1e-9) for i in range(120)}
CELLS600 = [q for q in itertools.combinations(range(120), 4) if False]
T3 = [(i, j, k) for i in range(120) for j in adjs[i] if j > i for k in adjs[i] & adjs[j] if k > j]
CELLS600 = [(i, j, k, l) for i, j, k in T3 for l in adjs[i] & adjs[j] & adjs[k] if l > k]
assert len(CELLS600) == 600
R = [np.eye(4) - 2 * np.outer(N[X], N[X]) for X in keys]
from scipy.spatial import cKDTree
def orbit(p):
    # breadth-first under the four reflections; a new point is kept only if no kept point lies within 1e-7 (rounding to a grid
    # split single corners in two where a coordinate sat on a rounding boundary)
    p = p / np.linalg.norm(p); out = [p]; i = 0; grid = {}
    key = lambda q: tuple(np.floor(q * 1e5).astype(int))
    def near(q):
        k = key(q)
        for dk in itertools.product((-1, 0, 1), repeat=4):
            for j in grid.get(tuple(a + b for a, b in zip(k, dk)), ()):
                if np.linalg.norm(out[j] - q) < 1e-7: return True
        return False
    grid.setdefault(key(p), []).append(0)
    while i < len(out):
        for r in R:
            q = r @ out[i]
            if not near(q): grid.setdefault(key(q), []).append(len(out)); out.append(q)
        i += 1
    return np.array(out)
STAGES = [('600-cell (White Queen)', 'v'), ('truncated 600-cell', 've'), ('rectified 600-cell', 'e'), ('bitruncated 600-cell / 120-cell', 'ef'),
          ('rectified 120-cell', 'f'), ('truncated 120-cell', 'fc'), ('120-cell (Red Queen)', 'c')]
M = np.array([N[X] for X in keys])
res = []
for name, ring in STAGES:
    p = np.linalg.solve(M, np.array([1.0 if X in ring else 0.0 for X in keys]))
    X = orbit(p); X = X / np.linalg.norm(X[0])
    Dx = np.linalg.norm(X[:, None] - X[None], axis=2); m = Dx[Dx > 1e-9].min(); ne = int((np.abs(Dx - m) < 1e-7).sum() // 2)
    # every cell of this family lies square to a corner direction of the 600-cell (120) or a cell direction (600, the 120-cell's
    # corners); a direction gives a cell when the corners highest along it span 3 dimensions
    cells = {}
    for u in list(V) + [V[list(q)].mean(0) for q in CELLS600]:
        u = u / np.linalg.norm(u); h = X @ u; top = np.where(h > h.max() - 1e-9)[0]
        if len(top) >= 4 and np.linalg.matrix_rank(X[top[1:]] - X[top[0]], tol=1e-7) == 3: cells[tuple(np.round(u, 9))] = set(top)
    # and no other: every corner's highest directions are covered (each corner lies in at least 4 cells)
    cover = np.zeros(len(X), int)
    for cs in cells.values(): cover[list(cs)] += 1
    assert cover.min() >= 4, (name, cover.min())
    kinds = {}
    for cset in cells.values():
        cc = sorted(cset); sub = Dx[np.ix_(cc, cc)]; key = f'{len(cc)} corners {int((np.abs(sub - m) < 1e-7).sum() // 2)} edges'
        kinds[key] = kinds.get(key, 0) + 1
    r = {'stage': name, 'rings': ring, 'V': len(X), 'E': ne, 'cells': len(cells), 'kinds': kinds, 'edge_over_radius': round(m, 9)}
    res.append(r); print(json.dumps(r), flush=True)
json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else 'stages.json', 'w'), indent=1)
