# Flat face test (2026-10-11): can the side ring's outer face, a 60-degree trapezoid (top 1, bottom phi, legs 1/phi), be tiled
# exactly by the kit's face shapes at phi-power sizes? Faces: equilateral triangle; golden triangles (36-72-72 and 108-36-36);
# FUJI's hexagon (120 degrees, sides a and a/phi); regular pentagon. Rotations every 6 degrees (both the 60- and 36-degree
# families), generous on purpose: "no tiling" here means no tiling with any of these faces.
import sys, itertools, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix
PHI = (1 + 5 ** .5) / 2; KMIN = int(sys.argv[1]) if len(sys.argv) > 1 else 5; ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 2
def poly(turns, sides):
    P = [np.zeros(2)]; a = 0.0
    for s, t in zip(sides, turns):
        P.append(P[-1] + s * np.array([np.cos(a), np.sin(a)])); a += np.radians(t)
    assert np.linalg.norm(P[-1]) < 1e-9, 'polygon does not close'
    return np.array(P[:-1])
T = {'tri': poly([120, 120, 120], [1, 1, 1]),
     'gold36': poly([180 - 72, 180 - 36, 180 - 72], [1, PHI, PHI]),        # acute golden: sides 1, phi, phi (apex 36)
     'gold108': poly([180 - 36, 180 - 108, 180 - 36], [PHI, 1, 1]),        # obtuse golden: sides phi, 1, 1 (apex 108)
     'hex': poly([60] * 6, [1, 1 / PHI] * 3),
     'pent': poly([72] * 5, [1] * 5)}
area = lambda W: abs(np.sum(W[:, 0] * np.roll(W[:, 1], -1) - np.roll(W[:, 0], -1) * W[:, 1])) / 2
h = np.sqrt(3) / 2 / PHI
R = np.array([[0, 0], [PHI, 0], [PHI - 1 / (2 * PHI), h], [1 / (2 * PHI), h]])
def edges_eq(P):
    E = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]; n = np.array([b[1] - a[1], a[0] - b[0]]); n /= np.linalg.norm(n)
        E.append((n, -n @ a))
    c = P.mean(0); return [(n, d) if n @ c + d < 0 else (-n, -d) for n, d in E]
RE = edges_eq(R)
inside = lambda X, tol=1e-9: np.all(np.stack([X @ n + d for n, d in RE], -1) <= tol, -1)
shapes = []
for name, V in T.items():
    for k in range(-1, -KMIN - 1, -1):
        seen = set()
        for j in range(60):
            a = np.radians(6 * j); Rm = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
            W = (PHI ** k) * V @ Rm.T; W = W - W.mean(0)
            key = tuple(sorted(tuple(np.round(w, 6)) for w in W))
            if key in seen: continue
            seen.add(key); shapes.append((f'{name}@phi^{k}', W, area(W)))
print('shapes (face x size x turn):', len(shapes), flush=True)
P = R.copy(); place = {}
for rnd in range(ROUNDS):
    new = []
    for si, (nm, W, A) in enumerate(shapes):
        Tt = (P[:, None, :] - W[None, :, :]).reshape(-1, 2)
        ok = np.all(np.stack([(W @ n).max() + Tt @ n + d for n, d in RE], -1) <= 1e-7, -1)
        for t in Tt[ok]:
            key = (si, tuple(np.round(t, 6)))
            if key not in place: place[key] = W + t; new.append(W + t)
    if new:
        Q = np.unique(np.round(np.vstack([P] + new), 7), axis=0); print(f'round {rnd}: placements {len(place)}, points {len(P)} -> {len(Q)}', flush=True); P = Q
tree = cKDTree(P); keys = [k for k, W in place.items() if np.all(tree.query(W)[0] < 1e-6)]
print('snug placements', len(keys), flush=True)
rng = np.random.default_rng(2); S = rng.uniform([0, 0], [PHI, h], (200000, 2)); S = S[inside(S, -1e-9)][:30000]
M = lil_matrix((len(S), len(keys)), dtype=np.int8); areas = np.zeros(len(keys))
for c, k in enumerate(keys):
    W = place[k]; areas[c] = shapes[k[0]][2]; E = edges_eq(W)
    hit = np.where(np.all(np.stack([S @ n + d for n, d in E], -1) < -1e-9, -1))[0]; M[hit, c] = 1
M = csr_matrix(M); AR = np.sqrt(3) / 4 * (PHI ** 2 - 1)   # trapezoid area = (sqrt3/4)(phi^2 - 1^2)
res = milp(c=np.ones(len(keys)), constraints=[LinearConstraint(M, 1, 1), LinearConstraint(areas[None, :], AR - 1e-9, AR + 1e-9)],
           integrality=np.ones(len(keys)), bounds=Bounds(0, 1), options={'time_limit': float(sys.argv[3]) if len(sys.argv) > 3 else 1800})
print('MILP:', res.status, res.message)
if res.x is not None:
    from collections import Counter
    ch = [keys[i] for i in np.where(res.x > .5)[0]]; print('tiles:', dict(Counter(shapes[k[0]][0] for k in ch)))
    np.save('face-tiling.npy', np.array([place[k] for k in ch], dtype=object), allow_pickle=True)
