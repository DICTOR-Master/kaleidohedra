# DICTO 2026-10-21, Reuleaux Platonics finish: are the equal width spreads of dual pairs (1.2480 / 1.2477, 1.1109 / 1.1108 on the
# mesh) exact? Width without a mesh: the body B = common part of balls radius D (the solid's diameter) on the corners. Its support in
# direction u is attained at a candidate point: a ball's own extreme point v + D u, the extreme point of a circle where two spheres
# meet, or a point where three spheres meet; keep the candidates inside all balls. Width w(u) = h(u) + h(-u); min and max over u by
# a fine grid then local refinement (Nelder-Mead on the sphere), float64, compared on the symmetry axes.
import itertools, numpy as np
from scipy.optimize import minimize
phi = (1 + 5 ** .5) / 2
cyc = lambda v: [np.roll(v, k) for k in range(3)]
S = {'Tetrahedron': [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
     'Cube': list(itertools.product((1, -1), repeat=3)),
     'Octahedron': [s * e for e in np.eye(3) for s in (1, -1)],
     'Dodecahedron': list(itertools.product((1, -1), repeat=3)) + [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a / phi, b * phi]))],
     'Icosahedron': [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a, b * phi]))]}
LOOK = {'Cube': 'Octahedron', 'Octahedron': 'Cube', 'Dodecahedron': 'Icosahedron', 'Icosahedron': 'Dodecahedron'}
def body(V):
    V = np.array(V, float); D = max(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2)); return V, D
def tri_points(V, D):
    P = []
    for i, j, k in itertools.combinations(range(len(V)), 3):
        a, b, c = V[i], V[j], V[k]
        # |x-a|=|x-b|=|x-c|=D: x = q + t n, q on the circumcentre line
        n = np.cross(b - a, c - a); nn = n @ n
        if nn < 1e-12: continue
        q = a + (np.cross(n, b - a) * ((c - a) @ (c - a)) + np.cross(c - a, n) * ((b - a) @ (b - a))) / (2 * nn)
        r2 = D * D - (q - a) @ (q - a)
        if r2 < 0: continue
        for s in (1, -1): P.append(q + s * np.sqrt(r2 / nn) * n)
    return np.array(P)
def feasible(X, V, D, tol=1e-9): return np.all(np.linalg.norm(X[:, None] - V[None], axis=2) <= D + tol, axis=1)
def h(u, V, D, T):
    C = [V + D * u]                                                  # caps
    for i, j in itertools.combinations(range(len(V)), 2):            # circles
        a, b = V[i], V[j]; m = (a + b) / 2; e = (b - a) / np.linalg.norm(b - a); r2 = D * D - ((b - a) @ (b - a)) / 4
        if r2 <= 0: continue
        w = u - (u @ e) * e; nw = np.linalg.norm(w)
        if nw > 1e-12: C.append((m + np.sqrt(r2) * w / nw)[None])
    C.append(T); X = np.vstack(C); X = X[feasible(X, V, D)]
    return (X @ u).max()
def width(u, V, D, T): u = u / np.linalg.norm(u); return h(u, V, D, T) + h(-u, V, D, T)
out = {}
for name, V in S.items():
    V, D = body(V); V = V / D; D = 1.0; T = tri_points(V, D); T = T[feasible(T, V, D)]
    rng = np.random.default_rng(0); U = rng.normal(size=(3000, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
    W = np.array([width(u, V, D, T) for u in U])
    lo = min((minimize(lambda x: width(x, V, D, T), U[i], method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-14, 'maxiter': 4000}).fun for i in np.argsort(W)[:6]))
    hi = -min((minimize(lambda x: -width(x, V, D, T), U[i], method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-14, 'maxiter': 4000}).fun for i in np.argsort(-W)[:6]))
    out[name] = (lo, hi); print(f'Reuleaux {LOOK.get(name, name).lower():13s} (balls on the {name.lower()}): width {lo:.12f} .. {hi:.12f}, ratio {hi / lo:.12f}', flush=True)
for a, b in [('Cube', 'Octahedron'), ('Dodecahedron', 'Icosahedron')]:
    ra, rb = out[a][1] / out[a][0], out[b][1] / out[b][0]; print(f'{a}/{b}: ratios {ra:.12f} vs {rb:.12f}, difference {ra - rb:.2e}')
