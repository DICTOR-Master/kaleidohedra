# DICTO's sphere method on the Lotus seed's gap: fill it from big to small with spheres on a golden ladder
# (radius r0, r0/phi, r0/phi^2, ...), each placed at the point of greatest clearance together with its whole
# icosahedral orbit (all images must fit), until no sphere of that size fits; then the next size down.
# Then the contact network: which spheres touch each other or a solid, and whether any sphere crosses the
# resin cuts (the faces between AXE, FUJI and CLEO).
import json, sys, math, itertools, collections, numpy as np
from scipy.optimize import minimize
PHI = (1 + 5 ** 0.5) / 2
P = json.load(open(sys.argv[1])); LEVELS = int(sys.argv[2]) if len(sys.argv) > 2 else 5
def planes(V, faces):
    V = np.asarray(V); c = V.mean(0); N = []; D = []
    for f in faces:
        a, b, d = V[f[0]], V[f[1]], V[f[2]]; n = np.cross(b - a, d - a); n /= np.linalg.norm(n)
        if n @ (c - a) > 0: n = -n
        N.append(n); D.append(n @ a)
    return np.array(N), np.array(D)
solids = [planes(p['vertices'], p['faces']) for p in P if p['role'] == 'ico']
gaps = [(p['role'], *planes(p['vertices'], p['faces'])) for p in P if p['role'] != 'ico']
allV = np.array([v for p in P for v in p['vertices']])
# the hull: the big icosahedron = convex hull of all vertices; its planes from the 12 farthest vertices' faces
from scipy.spatial import ConvexHull
H = ConvexHull(allV); HN = H.equations[:, :3]; HD = -H.equations[:, 3]
def clearance(X, spheres):
    X = np.atleast_2d(X)
    c = np.min(HD[None, :] - X @ HN.T, axis=1)                      # inside the hull
    for N, D in solids: c = np.minimum(c, np.max(X @ N.T - D[None, :], axis=1))  # outside each solid (plane bound)
    if spheres:
        C = np.array([s[0] for s in spheres]); R = np.array([s[1] for s in spheres])
        c = np.minimum(c, np.min(np.linalg.norm(X[:, None, :] - C[None], axis=2) - R[None], axis=1))
    return c
# icosahedral symmetry of the cluster: orthogonal maps of the 12 hull vertices onto themselves
hv = allV[H.vertices]; hv = hv[np.argsort(-np.linalg.norm(hv, axis=1))][:12]
mats = []
for i, j in itertools.permutations(range(12), 2):
    pass
a0, b0 = hv[0], next(v for v in hv[1:] if abs(np.linalg.norm(v - hv[0]) - np.min([np.linalg.norm(w - hv[0]) for w in hv[1:]])) < 1e-6)
def frame(a, b):
    e1 = a / np.linalg.norm(a); e2 = b - (b @ e1) * e1; e2 /= np.linalg.norm(e2); return np.array([e1, e2, np.cross(e1, e2)])
F0 = frame(a0, b0); L0 = np.linalg.norm(a0 - b0)
key = lambda Y: frozenset(tuple(np.round(y, 5)) for y in Y)
HK = key(hv)
for a in hv:
    for b in hv:
        if abs(np.linalg.norm(a - b) - L0) > 1e-6: continue
        for flip in (1, -1):
            F = frame(a, b); F[2] *= flip; M = F.T @ F0
            if key(hv @ M.T) == HK and not any(np.allclose(M, m) for m in mats): mats.append(M)
print('symmetries', len(mats), flush=True)
def orbit(x): 
    pts = []
    for M in mats:
        y = M @ x
        if not any(np.linalg.norm(y - q) < 1e-6 for q in pts): pts.append(y)
    return pts
# candidate points: a grid over the cluster's bounding ball, kept where the clearance is positive
Rb = np.max(np.linalg.norm(allV, axis=1)); g = np.linspace(-Rb, Rb, 90)
G = np.array(np.meshgrid(g, g, g, indexing='ij')).reshape(3, -1).T
G = G[np.linalg.norm(G, axis=1) <= Rb]
G = G[clearance(G, []) > 0]
print('grid points in the gap', len(G), flush=True)
spheres = []; log = []
r0 = None
for lvl in range(LEVELS):
    placed = 0; fails = 0
    while True:
        cl = clearance(G, spheres)
        i = int(np.argmax(cl))
        best = minimize(lambda x: -clearance(x, spheres)[0], G[i], method='Nelder-Mead', options={'xatol': 1e-8, 'fatol': 1e-10, 'maxiter': 600})
        x, c = best.x, -best.fun
        r = (r0 if r0 is not None else c) / PHI ** lvl
        if c < r - 1e-9: break
        orb = orbit(x)
        # copies that crowd the sphere itself: snap it onto their common symmetry axis or plane (their average)
        near = [y for y in orb if np.linalg.norm(y - x) < 2 * r - 1e-7]
        if len(near) > 1:
            x = np.mean(near, axis=0); c = clearance(x, spheres)[0]
            if r0 is None: r = c
            orb = orbit(x)
        # the whole orbit must fit, against the solids, the hull, earlier spheres and each other
        if c < r - 1e-7 or min(clearance(np.array(orb), spheres)) < r - 1e-7 or any(np.linalg.norm(p - q) < 2 * r - 1e-7 for p, q in itertools.combinations(orb, 2)):
            G = G[np.linalg.norm(G - x, axis=1) > r]  # skip this spot
            fails += 1
            if len(G) == 0 or fails > 300: break
            continue
        if r0 is None: r0 = r
        spheres += [(p, r, lvl) for p in orb]; placed += len(orb)
    if r0 is None: print('nothing placed'); break
    log.append((lvl, r0 / PHI ** lvl, placed)); print(f'level {lvl}: radius {r0 / PHI ** lvl:.6f}, placed {placed}', flush=True)
    G = G[clearance(G, spheres) > 0]
# where are the spheres, by resin piece; does any sphere cross a resin cut (a face shared by two gap pieces)?
def piece_of(x):
    for role, N, D in gaps:
        if np.all(x @ N.T - D <= 1e-7): return role
    return 'none'
cross = collections.Counter(); where = collections.Counter()
for x, r, lvl in spheres:
    role = piece_of(x); where[(lvl, role)] += 1
    for _, N, D in gaps:
        inside = np.all(x @ N.T - D <= 1e-9)
        if inside and np.min(D - x @ N.T) < r - 1e-6: cross[lvl] += 1; break
print('sphere centres by level and resin piece:', dict(sorted(where.items())))
print('spheres crossing a resin cut, by level:', dict(cross))
# contacts
cont = collections.Counter()
for (x, r, l), (y, s, m) in itertools.combinations(spheres, 2):
    if abs(np.linalg.norm(x - y) - (r + s)) < 1e-5: cont[(min(l, m), max(l, m))] += 1
print('sphere-sphere touches by level pair:', dict(cont))
json.dump({'levels': log, 'spheres': [[list(map(float, x)), float(r), int(l)] for x, r, l in spheres]}, open('lotus-spheres.json', 'w'))
