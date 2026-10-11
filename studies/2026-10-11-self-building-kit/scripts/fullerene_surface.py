# DICTO 2026-10-11: "fullerene chain architecture showing in the Lotus seed". The surface of Chain steps 1 and 2: which piece faces
# lie on the outer icosahedron's 20 face planes, by shape and size; checks that they cover each face exactly.
import json, sys, numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
D = json.load(open(sys.argv[1]))
def area(P):
    P = np.array(P); n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
    return abs(sum(np.cross(P[i], P[(i + 1) % len(P)]) for i in range(len(P))) @ n) / 2
for st in ('1', '2'):
    L = D[st]; allv = np.array([v for p in L for v in p['v']])
    H = ConvexHull(allv); planes = []
    for e in H.equations:                                   # merge near-equal planes (the data has 5-digit coordinates)
        if not any(np.linalg.norm(e[:3] - q[:3]) < 1e-3 and abs(e[3] - q[3]) < 1e-3 for q in planes): planes.append(e)
    planes = np.array(planes)
    R = np.linalg.norm(allv, axis=1).max(); E = R / np.sin(2 * np.pi / 5)     # outer icosahedron edge
    big_area = np.sqrt(3) / 4 * E ** 2
    kinds = Counter(); tot = 0; per_face = Counter()
    for p in L:
        V = np.array(p['v'])
        for f in p['f']:
            P = V[f]
            for k, e in enumerate(planes):
                if np.all(abs(P @ e[:3] + e[3]) < 2e-4):
                    sides = [np.linalg.norm(P[i] - P[(i + 1) % len(P)]) for i in range(len(P))]
                    if len(P) == 6: name = f'hexagon (sides {min(sides):.4f}/{max(sides):.4f})'
                    else: name = f'{len(P)}-gon, {p["r"]} face, side {max(sides):.4f}'
                    kinds[name] += 1; a = area(P); tot += a; per_face[k] += a
                    break
    print(f'\nstep {st}: outer icosahedron edge phi^{np.log(E) / np.log(PHI):.3f}, {len(planes)} face planes; surface pieces:')
    for k, n in sorted(kinds.items()): print(f'   {n:5d} x {k}')
    print(f'   covered area / 20 faces = {tot / (20 * big_area):.6f}; per face min/max = {min(per_face.values()) / big_area:.6f} / {max(per_face.values()) / big_area:.6f}')
    # curvature points: the outer icosahedron's 12 corners (5 triangles meet, the pentagonal caps); every other surface point is flat
    corners = np.unique(np.round(allv[np.isclose(np.linalg.norm(allv, axis=1), R, atol=1e-4)], 4), axis=0)
    print(f'   pentagonal caps (corners where 5 faces meet): {len(corners)}')
