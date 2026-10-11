# DICTO's dodecahedral Chain (2026-10-11): D(1) = 12 pentagonal pyramids (J2, edge 1; bases on D's faces, points inward on the
# corners of the small icosahedron) + I(1/phi) + 30 AXE + 20 CLEO, all taken from the Lotus seed. Each stage leaves the old
# pyramids off: D(phi^2n) = Chain-grown I(phi^(2n-1)) + 12 J2 + 30 AXE + 20 CLEO at the stage's size.
# Checks: D regular with edge 1; every piece inside D; no piece of the Lotus seed crosses D's surface; volumes add up.
import json, sys, numpy as np
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
L = json.load(open(sys.argv[1]))[:113]
vol = lambda V: ConvexHull(np.array(V)).volume
ico = [p for p in L if p['role'] == 'ico']
small = min(ico, key=lambda p: vol(p['vertices'])); big = [p for p in ico if p is not small]
S = np.array(small['vertices'])
caps, bases = [], []
for p in big:
    V = np.array(p['vertices'])
    a = min(range(12), key=lambda i: np.min(np.linalg.norm(S - V[i], axis=1)))
    assert np.min(np.linalg.norm(S - V[a], axis=1)) < 1e-4, 'outer icosahedron does not touch a small-icosahedron corner'
    nb = [i for i in range(12) if abs(np.linalg.norm(V[i] - V[a]) - 1) < 1e-4]
    assert len(nb) == 5
    caps.append([V[a].tolist()] + [V[i].tolist() for i in nb]); bases += [V[i] for i in nb]
D = np.unique(np.round(np.array(bases), 5), axis=0)
H = ConvexHull(D); E = H.equations
edges = sorted({round(float(np.linalg.norm(D[i] - D[j])), 5) for i in range(len(D)) for j in range(i) if np.linalg.norm(D[i] - D[j]) < 1.01})
print(f'D: {len(D)} corners, {len(H.equations)} hull planes (merged faces 12 expected), edge lengths {edges}')
inside = lambda V: np.all(np.array(V) @ E[:, :3].T + E[:, 3] <= 1e-5)
crosses = lambda V: (np.array(V) @ E[:, :3].T + E[:, 3]).max() > 1e-5 and (np.array(V) @ E[:, :3].T + E[:, 3]).max(axis=0).min() < -1e-5
cap_vol = vol(caps[0])
parts = {'axe': [p for p in L if p['role'] == 'axe' and inside(p['vertices'])],
         'cleo': [p for p in L if p['role'] == 'cleo' and inside(p['vertices'])]}
print('inside D:', {k: len(v) for k, v in parts.items()}, '; small icosahedron inside:', inside(small['vertices']),
      '; pyramids inside:', all(inside(c) for c in caps))
# no Lotus piece may straddle D's surface (outer pieces must be wholly outside)
straddle = 0
for p in L:
    if p is small or p['role'] == 'ico': continue
    d = np.array(p['vertices']) @ E[:, :3].T + E[:, 3]
    if d.max() > 1e-5 and not inside(p['vertices']) and np.all(d.min(axis=0) < -1e-5): straddle += 1
print('Lotus gap pieces straddling D:', straddle)
dv = (15 + 7 * 5 ** .5) / 4
total = vol(small['vertices']) + 12 * cap_vol + sum(vol(p['vertices']) for v in parts.values() for p in v)
print(f'volumes: D {dv:.12f}  pieces {total:.12f}  (12 pyramids {12 * cap_vol:.6f}, I(1/phi) {vol(small["vertices"]):.6f})')
out = [{'r': 'ico', 'v': small['vertices']}] + [{'r': 'cap', 'v': c} for c in caps] + \
      [{'r': k, 'v': p['vertices']} for k, v in parts.items() for p in v]
json.dump({'note': 'DICTO dodecahedral Chain stage 0: D(1) = I(1/phi) + 12 J2 + 30 AXE + 20 CLEO (Lotus-seed frame, edge 1). Convex pieces: faces = hull.',
           'dodecahedron': D.tolist(), 'pieces': out, 'checks': {'D_volume': dv, 'pieces_volume': total}}, open(sys.argv[2], 'w'))
