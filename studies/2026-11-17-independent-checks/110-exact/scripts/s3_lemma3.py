"""Item 3, exact: Lemma 3 (a)-(c): counts per wall and W(H4)-transitivity."""
from common import *

L = Log('logs/s3_lemma3.log')
B = load_base()
P, Q, W, WQ = B['P'], B['Q'], B['W'].astype(np.int64), B['WQ'].astype(np.int64)
mir, crs = wall_sets(P, Q)
G = gram(P)
idx = {canon_point(p): i for i, p in enumerate(P)}
EDGE_IP, HALF = np.array([25, 50]), np.array([25, 25])
R2 = np.array([50, 50])

def per_wall(sets, X, wallset, label):
    keys = [canon_dir(v) for v in plate_normals(X[np.array([s[:3] for s in sets])])]
    inw = sum(k in wallset for k in keys)
    c = {}
    for k in keys:
        c[k] = c.get(k, 0) + 1
    return inw, sorted(set(c.values())), len(c)

def transitive(sets, perms):
    S = {tuple(sorted(s)) for s in sets}
    s0 = np.array(sorted(next(iter(S))))
    orb = {tuple(sorted(r)) for r in perms[:, s0]}
    return len(orb) == len(S) and orb <= S, len(orb)

# (a) edge triangles
tris = [tuple(t) for t in B['tris']]
inw, per, nw = per_wall(tris, P, mir, 'tri')
L.check('(a) edge triangles on mirrors', inw, 1200)
L.check('(a) edge triangles per mirror', (per, nw), ([20], 60))
pent = [tuple(p) for p in B['pent']]
inw, per, nw = per_wall(pent, Q, mir, 'pent')
L.check('(a) pentagons of the dual 120-cell on mirrors', inw, 720)
L.check('(a) pentagons per mirror', (per, nw), ([12], 60))
# (b) golden rectangles: sides an edge and a radius
rects = set()
for a in range(120):
    for b in np.nonzero(zeq(G[a], EDGE_IP[None]))[0]:
        u = P[b] - P[a]
        for c in range(120):
            v = P[c] - P[b]
            if zeq(zdot(v, v), R2) and zeq(zdot(u, v), np.array([0, 0])):
                d = idx.get(canon_point(P[a] + v))
                if d is not None:
                    rects.add(tuple(sorted((a, int(b), c, d))))
rects = sorted(rects)
L.check('(b) golden rectangles (edge x radius)', len(rects), 1800)
# order the corners around the rectangle for plate use: any 3 corners are non-collinear
inw, per, nw = per_wall(rects, P, mir, 'rect')
L.check('(b) golden rectangles on mirrors', inw, 1800)
L.check('(b) golden rectangles per mirror', (per, nw), ([30], 60))
ok, n = transitive(rects, W)
L.check('(b) W(H4) transitive on golden rectangles (exact orbit)', (ok, n), (True, 1800))
# (c) radius triangles: three corners pairwise at distance = radius (60 deg)
adj60 = zeq(G, HALF[None, None])
rt = cliques(adj60, 3)
L.check('(c) radius triangles', len(rt), 2400)
inw, per, nw = per_wall(rt, P, crs, 'rt')
L.check('(c) radius triangles on cross walls', inw, 2400)
L.check('(c) radius triangles per cross wall', (per, nw), ([8], 300))
ok, n = transitive(rt, W)
L.check('(c) W(H4) transitive on radius triangles (exact orbit)', (ok, n), (True, 2400))
ok, n = transitive(tris, W)
L.check('(a) W(H4) transitive on edge triangles (exact orbit)', (ok, n), (True, 1200))
L.final()
