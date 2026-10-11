# Octahedral variant, first check (2026-10-12): the five octahedra on the twin core's corners (ID edge phi/2) versus the small
# icosahedron I(1/phi) at the centre and versus Pacioli's golden icosahedron-in-octahedron (corners dividing the octahedron's edges
# in the golden ratio). Which icosahedron is Pacioli-inscribed in these octahedra, and how does it compare with I(1/phi)?
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
ID = ref['ID'] * PHI / 2; Ic = ref['I'] / PHI
octs = []
for i, j, k in itertools.combinations(range(30), 3):
    a, b, c = ID[i], ID[j], ID[k]
    if abs(a @ b) < 1e-9 and abs(a @ c) < 1e-9 and abs(b @ c) < 1e-9:
        S = np.array([s * x for x in (a, b, c) for s in (1, -1)])
        if not any(all(np.min(np.linalg.norm(U - p, axis=1)) < 1e-9 for p in S) for U in octs): octs.append(S)
O = octs[0]; eo = min(np.linalg.norm(O[0] - w) for w in O[1:])
# Pacioli: on each octahedron edge the point dividing it in the golden ratio (12 edges -> 12 points, one per edge, chirally)
E = [(a, b) for a, b in itertools.combinations(range(6), 2) if abs(np.linalg.norm(O[a] - O[b]) - eo) < 1e-9]
best = None
for signs in itertools.product((0, 1), repeat=len(E)):
    P = np.array([O[a] + (1 / PHI if s else 1 - 1 / PHI) * (O[b] - O[a]) for (a, b), s in zip(E, signs)])
    d = sorted(np.linalg.norm(P[0] - w) for w in P[1:])
    if abs(d[0] - d[4]) < 1e-9 and abs(d[5] - d[0]) > 1e-6:          # five equal nearest neighbours: an icosahedron
        best = P; break
ep = sorted(np.linalg.norm(best[0] - w) for w in best[1:])[0]
match = all(np.min(np.linalg.norm(Ic - p, axis=1)) < 1e-6 for p in best)
print(f'5 octahedra on the ID corners, edge {eo:.6f}; Pacioli icosahedron in each: edge {ep:.6f} (= {ep / (1 / PHI):.6f} x the small icosahedron 1/phi); '
      f'coincides with I(1/phi): {match}; ratio power of phi: {np.log(ep / (1 / PHI)) / np.log(PHI):.6f}')
I1 = ref['I']                                   # icosahedron of edge 1, the network's own turn
for n, O in enumerate(octs):
    eo = min(np.linalg.norm(O[0] - w) for w in O[1:]); E = [(a, b) for a, b in itertools.combinations(range(6), 2) if abs(np.linalg.norm(O[a] - O[b]) - eo) < 1e-9]
    on_edges = sum(1 for v in I1 if any(np.linalg.norm(np.cross(v - O[a], O[b] - O[a])) < 1e-9 and 0 < (v - O[a]) @ (O[b] - O[a]) < eo ** 2 for a, b in E))
    print(f'  octahedron {n + 1}: corners of the network-frame icosahedron of edge 1 lying on its edges: {on_edges} of 12')
FID = ConvexHull(ID).equations
print('icosahedron of edge 1 inside the ID core:', bool(np.all(I1 @ FID[:, :3].T + FID[:, 3] <= 1e-9)), '; deepest corner', round(float((I1 @ FID[:, :3].T + FID[:, 3]).max()), 6))
