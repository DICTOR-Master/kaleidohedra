# Figure 3 as a slice (GBP paper, DICTO 2026-10-16): a block of the bcc packing of Ogdoecontahedra with the front slab removed. On the cut
# plane (through copy centres, normal to a cube axis) the exact section: solids (gold), the non-golden shell inside each cut envelope (pink),
# the golden region between envelopes (cyan). Behind it the copies in depth. Writes data/fig3-slice.json for render_fig3.html.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T']); R = json.load(open('data/network-render.json'))
cube = np.array(R['cube']); Ec = np.array(json.load(open('data/bodhi-envelope-cut.json'))['envelope_cut'])
B = np.array([T[0] + T[1], T[0] + T[2], T[0]]).T; a = np.linalg.norm(T[0] + T[1])
n, up = cube[0], cube[1]; right = np.cross(up, n)

def faces(P):  # polygon faces of a convex hull, coplanar triangles merged, corners in order
    h = ConvexHull(P); groups = {}
    for s, e in zip(h.simplices, h.equations):
        k = tuple(np.round(e, 6)); groups.setdefault(k, set()).update(s)
    out = []
    for k, idx in groups.items():
        idx = list(idx); nn = np.array(k[:3]); c = P[idx].mean(0)
        u = P[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(nn, u)
        out.append([int(i) for i in sorted(idx, key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u))])
    return out

def section(P, c):
    h = ConvexHull(P); pts = []
    for s in h.simplices:
        for i, j in itertools.combinations(s, 2):
            da, db = P[i] @ n - c, P[j] @ n - c
            if da * db < 0: t = da / (da - db); pts.append(P[i] + t * (P[j] - P[i]))
    if len(pts) < 3: return None
    uv = np.unique(np.round(np.c_[np.array(pts) @ right, np.array(pts) @ up], 10), axis=0)
    return uv[ConvexHull(uv).vertices].tolist()

W = 1.05 * a; sites = []
for m in itertools.product(range(-5, 6), repeat=3):
    s = B @ np.array(m, float); d, u, v = s @ n, s @ right, s @ up
    if -2.1 * a <= d <= 0.6 * a and abs(u) <= W + 0.05 and abs(v) <= W + 0.05: sites.append(s.tolist())
caps = {'env': [], 'ocd': []}
for s in sites:
    for k, P in (('env', Ec), ('ocd', O)):
        S = section(P + np.array(s), 0.0)
        if S: caps[k].append(S)
def section3(P, m, c):   # 3D section polygon of P by the plane m.x = c, corners in order
    h = ConvexHull(P); pts = []
    for sp in h.simplices:
        for i, j in itertools.combinations(sp, 2):
            da, db = P[i] @ m - c, P[j] @ m - c
            if da * db < 0: t = da / (da - db); pts.append(P[i] + t * (P[j] - P[i]))
    if len(pts) < 3: return None
    Q = np.unique(np.round(np.array(pts), 10), axis=0); e1 = np.cross(m, [0.31, 0.57, 0.76]); e1 /= np.linalg.norm(e1); e2 = np.cross(m, e1)
    cc = Q.mean(0); return Q[np.argsort(np.arctan2((Q - cc) @ e2, (Q - cc) @ e1))].tolist()
walls = []   # solids cut by the block's four side walls, capped gold
for m in (right, -right, up, -up):
    for s in sites:
        S = section3(O + np.array(s), m, W)
        if S: walls.append(S)
caps['walls'] = walls
json.dump({'ocd': {'v': O.tolist(), 'f': faces(O)}, 'env': {'v': Ec.tolist(), 'f': faces(Ec)}, 'sites': sites, 'n': n.tolist(), 'up': up.tolist(),
           'right': right.tolist(), 'W': W, 'a': a, 'caps': caps}, open('data/fig3-slice.json', 'w'))
print('sites', len(sites), 'caps env/ocd', len(caps['env']), len(caps['ocd']), 'faces ocd/env', len(faces(O)), len(faces(Ec)))
