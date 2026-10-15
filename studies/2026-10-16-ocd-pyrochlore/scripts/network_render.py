# Render data: a patch of the double network (two interpenetrating hexagon-joined diamond networks = one bcc lattice packing).
import json, numpy as np, itertools, sys
from scipy.spatial import ConvexHull
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
N = json.load(open('data/network.json')); T = np.array(N['T']); O = np.array(N['ocd'])
h = ConvexHull(O); pl = []
for e in h.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
F = []
for e in pl:
    idx = [i for i in range(len(O)) if abs(O[i] @ e[:3] + e[3]) < 1e-7]; Qp = O[idx]; c = Qp.mean(0)
    a = Qp[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Qp - c) @ b, (Qp - c) @ a))])
# bcc frame: the 8 hexagon-contact directions +-t_i are cube corners; cube axes = (t_i + t_j) directions
cube = [T[0] + T[1], T[0] + T[2], T[0] + T[3]]; cube = [c / np.linalg.norm(c) for c in cube]
assert all(abs(cube[a] @ cube[b]) < 1e-9 for a, b in itertools.combinations(range(3), 2)), 'cube axes'
sites = []
for m in itertools.product(range(-3, 4), repeat=4):
    p = sum(mm * t for mm, t in zip(m, T))
    k = sum(m) % 4                                         # sublattice: 0 = A, 1 = B, 2 = A', 3 = B'
    if all(abs(p @ c) <= 2.2 for c in cube) and not any(np.allclose(p, s[0]) for s in sites): sites.append((p, k))
up = cube[1]; view = cube[0]
json.dump({'v': O.tolist(), 'f': F, 'sites': [[s[0].tolist(), s[1]] for s in sites], 'view': view.tolist(), 'up': up.tolist(), 'cube': [c.tolist() for c in cube]},
          open('data/network-render.json', 'w'))
print(len(sites), 'copies; sublattices', {k: sum(1 for s in sites if s[1] == k) for k in range(4)})
