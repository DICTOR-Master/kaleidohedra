# DICTO 2026-10-11: "remarkably similar to a 4D polytope". The 600-cell seen down one vertex (circumradius 1, edge 1/phi) has
# shells point, icosahedron, dodecahedron, icosahedron, icosidodecahedron, ... Compare with the Lotus seed.
import sys, json, itertools, numpy as np
PHI = (1 + 5 ** .5) / 2
V = {tuple(0.5 * x for x in s) for s in itertools.product([-1, 1], repeat=4)}
for i in range(4):
    for s in (-1, 1): v = [0] * 4; v[i] = s; V.add(tuple(v))
ev = [PHI / 2, .5, 1 / (2 * PHI), 0]
for perm in itertools.permutations(range(4)):
    if sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4)) % 2: continue
    for s in itertools.product([-1, 1], repeat=3):
        b = [ev[0] * s[0], ev[1] * s[1], ev[2] * s[2], 0]; v = [0] * 4
        for k in range(4): v[perm[k]] = b[k]
        V.add(tuple(round(x, 12) for x in v))
V = np.array(sorted(V)); assert len(V) == 120
v0 = V[0]; Q, _ = np.linalg.qr(np.c_[v0, np.eye(4)[:, :3]]); B = Q[:, 1:4]
sh = {}
for x in V: sh.setdefault(round(float(x @ v0), 6), []).append(x @ B)
print('600-cell, circumradius 1, edge', round(float(min(np.linalg.norm(V[0] - w) for w in V[1:])), 6))
for h in sorted(sh, reverse=True):
    P = np.array(sh[h]); print(f'  height {h:+.4f}: {len(P):3d} vertices, radius {np.linalg.norm(P, axis=1).max():.6f}')
shell1 = np.array(sh[sorted(sh, reverse=True)[1]])
L = json.load(open(sys.argv[1]))[:113]
ico = [np.array(p['vertices']) for p in L if p['role'] == 'ico']
cen = [I.mean(0) for I in ico]; edge = lambda I: min(np.linalg.norm(I[0] - w) for w in I[1:])
small = min(ico, key=edge)
print('Lotus small icosahedron: edge', round(float(edge(small)), 6), 'circumradius', round(float(np.linalg.norm(small - small.mean(0), axis=1).max()), 6),
      '| 600-cell shell 1 radius', round(float(np.linalg.norm(shell1, axis=1).max()), 6))
C = np.array([c for c in cen if np.linalg.norm(c) > 1e-6])
print('Lotus 13 icosahedron centres: 1 at the origin +', len(C), 'at radius', np.round(np.unique(np.round(np.linalg.norm(C, axis=1), 6)), 6),
      '= phi^2 x shell-1 radius', round(PHI ** 2 * float(np.linalg.norm(shell1, axis=1).max()), 6))
e12 = sorted({round(float(np.linalg.norm(a - b)), 6) for a, b in itertools.combinations(C, 2)})[:1]
s12 = sorted({round(float(np.linalg.norm(a - b)), 6) for a, b in itertools.combinations(shell1, 2)})[:1]
print('  nearest-centre distance', e12, '= phi^2 x shell-1 edge', [round(PHI ** 2 * s12[0], 6)])
