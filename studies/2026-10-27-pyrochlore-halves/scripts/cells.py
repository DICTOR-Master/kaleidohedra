# Step 2: the space of a pyrochlore polytype shared out by weights, as #57: sites S (ball, layer k), C (hole over X at 3/4: a diamond
# atom), O (octahedral hole over Z at 1/2), Y (tetrahedral hole over Y at 1/4). Power cells (|x-p|^2 - w_p least). Weights
# w_S = w_C = a, w_O = b, w_Y = c. Find a with the S and C cells exactly the pyrochlore tetrahedra (edge 1/2), then show the voids.
import numpy as np, itertools, sys
from scipy.spatial import HalfspaceIntersection, ConvexHull
sys.path.insert(0, __file__.rsplit('/', 1)[0]); from pyro import H, A1, A2, xy, layer_types
def sites(word):
    n = len(word); out = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = 'ABC'.replace(X, '').replace(Y, '')
        out += [('S', k, xy(X) + [0, 0, k * H]), ('C', k, xy(X) + [0, 0, (k + .75) * H]),
                ('O', k, xy(Z) + [0, 0, (k + .5) * H]), ('Y', k, xy(Y) + [0, 0, (k + .25) * H])]
    return [(t, k, np.array(p, float)) for t, k, p in out]
def cell(word, i, W, reach=1.6):
    S = sites(word); T = len(word) * H; t0, k0, p0 = S[i]; hs = []
    for t, k, p in S:
        for a, b, l in itertools.product(range(-3, 4), range(-3, 4), range(-2, 3)):
            q = p + a * A1 + b * A2 + np.array([0, 0, l * T]); d = q - p0; dd = d @ d
            if dd < 1e-12 or dd > reach ** 2: continue
            # |x-p0|^2 - w0 <= |x-q|^2 - wq  <=>  2 d.x <= |q|^2-|p0|^2 - wq + w0  (x relative to p0: 2 d.y <= dd - wq + w0)
            hs.append(np.r_[2 * d, -(dd - W[t] + W[t0])])
    hs = np.array(hs)
    if _extra is not None: hs = np.vstack([hs, _extra])
    # a point well inside (Chebyshev centre by linear programming): the cell need not contain its own site
    from scipy.optimize import linprog
    nrm = np.linalg.norm(hs[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[hs[:, :3], nrm], b_ub=-hs[:, 3], bounds=[(-2, 2)] * 3 + [(0, None)])
    if not r.success or r.x[3] < 1e-9: return None                  # empty (or flat) cell
    try:
        V = HalfspaceIntersection(hs, r.x[:3]).intersections
    except Exception:
        return None
    return ConvexHull(V)
def cell_cut(word, i, W, sgn, mid):
    # the cell of site i with the extra half-space sgn * z <= sgn * mid (relative to the site): bottom half sgn = 1, top half sgn = -1
    global _extra
    _extra = np.array([[0, 0, sgn, -sgn * mid]]); try_ = cell(word, i, W); _extra = None; return try_
_extra = None
def describe(h):
    V = h.points[h.vertices]; E = set()
    for s in h.simplices:
        for a, b in itertools.combinations(s, 2): E.add(round(float(np.linalg.norm(h.points[a] - h.points[b])), 6))
    return len(V), round(h.volume, 6)
if __name__ == '__main__':
    tet = np.sqrt(2) / 12 * 0.5 ** 3                                    # regular tetrahedron of edge 1/2
    lo, hi = -0.5, 0.5
    for _ in range(50):                                                 # weight a making the ball's cell that tetrahedron (b = c = 0)
        a = (lo + hi) / 2; h = cell('ABC', 0, {'S': a, 'C': a, 'O': 0, 'Y': 0})
        v = h.volume if h else 0
        lo, hi = (a, hi) if v < tet else (lo, a)
    print(f'weight a = {a:.9f} (b = c = 0): ball cell volume {v:.9f}, regular tetrahedron {tet:.9f}')
    W = {'S': a, 'C': a, 'O': 0, 'Y': 0}
    for name, w in [('3C', 'ABC'), ('2H', 'AB'), ('4H', 'ABAC')]:
        S = sites(w); tot = 0; rows = []
        for i, (t, k, p) in enumerate(S):
            h = cell(w, i, W); nv, vol = describe(h) if h else (0, 0); tot += vol; rows.append(f'{t}{k}:{nv}v {vol}')
        print(name, ''.join(layer_types(w)), '| period volume', round(tot, 6), 'expected', round(len(w) * np.sqrt(2) / 2, 6), '|', ', '.join(rows))
