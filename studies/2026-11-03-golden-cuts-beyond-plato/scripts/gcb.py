"""Golden cuts beyond Plato: shared geometry (floating point, used for construction and checks only;
every theorem value is computed exactly in the step scripts).

- archimedean(name): vertices (edge 1) of the 13 Archimedean solids and the elongated square gyrobicupola
- platonic(name), kepler_poinsot(name)
- faces(V): convex-hull faces as cyclic vertex lists (coplanar triangles merged)
- catalan(name): polar dual of the Archimedean solid, vertex orbits by Archimedean face size (snub triangles split)
- cut(V, F, y): vertex truncation, cut distance y[v] along every edge at vertex v; returns new vertices, faces,
  and for every original face its side list [(kind, length)] with kind 'corner' or 'orig'
"""
import itertools
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize

g = (1 + 5 ** .5) / 2
r2 = 2 ** .5


def _even_perms(v):
    a, b, c = v
    return [(a, b, c), (b, c, a), (c, a, b)]


def _all_perms(v):
    return list(set(itertools.permutations(v)))


def _signs(v):
    out = set()
    for s in itertools.product([1, -1], repeat=3):
        out.add(tuple(si * x for si, x in zip(s, v)))
    return list(out)


def _orbit(seeds, perms):
    P = set()
    for s in seeds:
        for p in perms(s):
            for q in _signs(p):
                P.add(tuple(round(x, 12) for x in q))
    return np.array(sorted(P), float)


def unit_edge(V):
    D = np.linalg.norm(V[:, None] - V[None], axis=2)
    return V / D[D > 1e-9].min()


def _rot(axis, ang):
    a = np.asarray(axis, float); a = a / np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def _group(gens):
    G = [np.eye(3)]
    frontier = [np.eye(3)]
    while frontier:
        nxt = []
        for A in frontier:
            for B in gens:
                C = B @ A
                if not any(np.allclose(C, X, atol=1e-9) for X in G):
                    G.append(C); nxt.append(C)
        frontier = nxt
    return G


def _snub(kind):
    if kind == 'cube':
        G = _group([_rot((0, 0, 1), np.pi / 2), _rot((1, 1, 1), 2 * np.pi / 3)])
        nf = 38
    else:
        G = _group([_rot((0, 1, g), 2 * np.pi / 5), _rot((1, 1, 1), 2 * np.pi / 3)])
        nf = 92
    assert len(G) in (24, 60), len(G)

    def orbit(p):
        p = p / np.linalg.norm(p)
        return np.array([A @ p for A in G])

    def obj(p):
        P = orbit(p); d = np.sort(np.linalg.norm(P - P[0], axis=1))[1:6]
        return float(np.var(d / d.mean())) + (0 if d[5 - 1] < 1.3 * d[0] else 1)
    rng = np.random.default_rng(1)
    for _ in range(400):
        r = minimize(obj, rng.normal(size=3), method='Nelder-Mead', options=dict(xatol=1e-14, fatol=1e-30, maxiter=20000))
        if r.fun < 1e-24:
            P = orbit(r.x)
            if len(faces(P)) == nf:
                return unit_edge(P)
    raise RuntimeError('snub not found')


def archimedean(name):
    if name == 'truncated tetrahedron':
        P = [p for s in _all_perms((3, 1, 1)) for p in _signs(s) if sum(x < 0 for x in p) % 2 == 0]
        return unit_edge(np.array(P, float))
    if name == 'cuboctahedron': return unit_edge(_orbit([(1, 1, 0)], _all_perms))
    if name == 'truncated cube': return unit_edge(_orbit([(r2 - 1, 1, 1)], _all_perms))
    if name == 'truncated octahedron': return unit_edge(_orbit([(0, 1, 2)], _all_perms))
    if name == 'rhombicuboctahedron': return unit_edge(_orbit([(1, 1, 1 + r2)], _all_perms))
    if name == 'truncated cuboctahedron': return unit_edge(_orbit([(1, 1 + r2, 1 + 2 * r2)], _all_perms))
    if name == 'snub cube': return _snub('cube')
    if name == 'icosidodecahedron': return unit_edge(_orbit([(0, 0, g), (.5, g / 2, g * g / 2)], _even_perms))
    if name == 'truncated dodecahedron': return unit_edge(_orbit([(0, 1 / g, 2 + g), (1 / g, g, 2 * g), (g, 2, g + 1)], _even_perms))
    if name == 'truncated icosahedron': return unit_edge(_orbit([(0, 1, 3 * g), (1, 2 + g, 2 * g), (g, 2, g ** 3)], _even_perms))
    if name == 'rhombicosidodecahedron': return unit_edge(_orbit([(1, 1, g ** 3), (g * g, g, 2 * g), (2 + g, 0, g * g)], _even_perms))
    if name == 'truncated icosidodecahedron':
        return unit_edge(_orbit([(1 / g, 1 / g, 3 + g), (2 / g, g, 1 + 2 * g), (1 / g, g * g, -1 + 3 * g),
                                 (2 * g - 1, 2, 2 + g), (g, 3, 2 * g)], _even_perms))
    if name == 'snub dodecahedron': return _snub('dodecahedron')
    if name == 'elongated square gyrobicupola':
        V = archimedean('rhombicuboctahedron'); top = V[:, 2] > V[:, 2].max() - 1e-9
        V = V.copy(); V[top] = V[top] @ _rot((0, 0, 1), np.pi / 4).T
        return V
    raise KeyError(name)


ARCH = ['truncated tetrahedron', 'cuboctahedron', 'truncated cube', 'truncated octahedron', 'rhombicuboctahedron',
        'truncated cuboctahedron', 'snub cube', 'icosidodecahedron', 'truncated dodecahedron', 'truncated icosahedron',
        'rhombicosidodecahedron', 'truncated icosidodecahedron', 'snub dodecahedron']
# DICTO order for the Platonic solids
PLATONIC = ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron', 'octahedron']


def platonic(name):
    if name == 'tetrahedron': return unit_edge(np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float))
    if name == 'cube': return unit_edge(np.array(list(itertools.product([1, -1], repeat=3)), float))
    if name == 'octahedron': return unit_edge(_orbit([(1, 0, 0)], _all_perms))
    if name == 'icosahedron': return unit_edge(_orbit([(0, 1, g)], _even_perms))
    if name == 'dodecahedron': return unit_edge(_orbit([(1, 1, 1), (0, 1 / g, g)], _even_perms))
    raise KeyError(name)


def faces(V, tol=1e-7):
    """Convex-hull faces of V as cyclic (counter-clockwise from outside) index lists."""
    h = ConvexHull(V)
    planes = {}
    for eq in h.equations:
        n, d = eq[:3], -eq[3]
        key = tuple(np.round(np.r_[n, d], 6))
        planes[key] = (n, d)
    out = []
    for n, d in planes.values():
        idx = [i for i in range(len(V)) if abs(V[i] @ n - d) < tol]
        c = V[idx].mean(0); u = V[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((V[i] - c) @ w, (V[i] - c) @ u))
        out.append(idx)
    return out


def edges_of(F):
    E = set()
    for f in F:
        for a, b in zip(f, f[1:] + f[:1]):
            E.add((min(a, b), max(a, b)))
    return sorted(E)


def catalan(name):
    """Polar dual of the Archimedean solid `name` (w.r.t. the unit sphere). Returns (V, F, orbit) where orbit[v]
    labels the Catalan vertex by the Archimedean face it comes from: 'n|neighbour sizes'."""
    A = archimedean(name); FA = faces(A)
    V = []
    orbit = []
    for f in FA:
        P = A[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        if n @ P[0] < 0: n = -n
        V.append(n / (n @ P[0]))
        # orbit label = face size + sizes of the edge-neighbouring faces (separates the two square orbits of the
        # rhombicuboctahedron and the two triangle orbits of the snubs; checked against the known orbit sizes)
        nb = sorted(len(h) for h in FA if len(set(h) & set(f)) == 2)
        lab = str(len(f)) + '|' + ''.join(map(str, nb))
        orbit.append(lab)
    V = np.array(V)
    F = faces(V)
    return V, F, orbit


def cut(V, F, y):
    """Truncate every vertex v at distance y[v] along each of its edges. Returns (W, sides) where sides[i] is the
    cyclic list of (kind, length) of the cut face i, kind 'corner' (made by a corner cut) or 'orig' (rest of an edge)."""
    pts = {}
    for f in F:
        for a, b in zip(f, f[1:] + f[:1]):
            for u, v in ((a, b), (b, a)):
                e = V[v] - V[u]; pts[(u, v)] = V[u] + y[u] * e / np.linalg.norm(e)
    sides = []
    for f in F:
        s = []
        m = len(f)
        for i in range(m):
            u, v, w = f[i - 1], f[i], f[(i + 1) % m]
            p_in, p_out = pts[(v, u)], pts[(v, w)]           # the two cut points at corner v
            s.append(('corner', float(np.linalg.norm(p_out - p_in))))
            s.append(('orig', float(np.linalg.norm(pts[(w, v)] - p_out))))
        sides.append(s)
    W = np.unique(np.round(np.array(list(pts.values())), 10), axis=0)
    return W, sides


def check_cut_is_convex_truncation(V, F, y):
    """The cut solid is the hull of the cut points; check that every cut point is a hull vertex and the face count is
    |F| + |V| (every original face kept, every corner replaced by one face)."""
    W, _ = cut(V, F, y)
    h = ConvexHull(W)
    FW = faces(W)
    return len(set(h.vertices)) == len(W) and len(FW) == len(F) + len(V), len(FW)
