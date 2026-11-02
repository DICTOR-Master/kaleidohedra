# Do Icosaxes and Unborn Axes (the golden truncated octahedra) appear as slices of the 24-cell? Sweep hyperplane x4 = h (an octahedral-symmetric
# direction: the 24-cell's vertex-first direction (1,0,0,0) after relabelling) and also the cell-first direction (1,1,1,1)/2; at each h build the
# section (convex hull of edge crossings), keep sections with 6 squares + 8 hexagons, report the hexagon side ratio and where it equals phi.
import itertools, numpy as np
from scipy.spatial import ConvexHull
g = (1 + 5 ** .5) / 2
V = np.array(sorted({tuple(s * np.array(p)) for p in set(itertools.permutations([1, 1, 0, 0])) for s in itertools.product([1, -1], repeat=4)} - {(0, 0, 0, 0)}), float)
V = np.unique(V, axis=0); V = V[np.linalg.norm(V, axis=1) > 0]
E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[i] - V[j]) - 2 ** .5) < 1e-9]
print(len(V), 'vertices', len(E), 'edges')
def section(d, h):
    d = d / np.linalg.norm(d); B = np.linalg.svd(d[None])[2][1:]          # basis of the hyperplane
    P = []
    for i, j in E:
        a, b = V[i] @ d - h, V[j] @ d - h
        if a * b < 0: t = a / (a - b); P.append(((V[i] + t * (V[j] - V[i])) @ B.T))
    if len(P) < 4: return None
    P = np.unique(np.round(np.array(P), 10), axis=0); hull = ConvexHull(P); faces = {}
    for eq in hull.equations:
        k = tuple(np.round(eq, 5)); faces.setdefault(k, set())
    sizes = []; ratios = []
    for k in faces:
        n = np.array(k[:3]); c = k[3]; idx = [i for i, p in enumerate(P) if abs(n @ p + c) < 1e-4]; Q = P[idx]
        if len(Q) < 3: continue
        cen = Q.mean(0); a0 = Q[0] - cen; b0 = np.cross(n, a0); Q = Q[np.argsort(np.arctan2((Q - cen) @ b0, (Q - cen) @ a0))]
        L = [np.linalg.norm(Q[(i + 1) % len(Q)] - Q[i]) for i in range(len(Q))]; sizes.append(len(Q))
        if len(Q) == 6: ratios.append(max(L) / min(L))
    return sorted(sizes), ratios
for name, d in (('cell-first (cell centre (1,0,0,0))', np.array([1., 0, 0, 0])), ('cell-first (cell centre (1,1,1,1)/2)', np.array([1., 1, 1, 1]))):
    prev = None
    for h in np.linspace(0, np.linalg.norm(V[0]) * 0.999 / 1, 4001):
        hh = h if name == 'vertex-first' else h * 1.0
        r = section(d, hh)
        if r is None: continue
        sz, rat = r
        if sz.count(4) == 6 and sz.count(6) == 8 and len(sz) == 14 and rat:
            rr = np.mean(rat)
            if prev is not None and (prev - g) * (rr - g) <= 0: print(f'{name}: hexagon ratio crosses φ near h = {hh:.5f} (golden truncated octahedron as a slice)')
            if prev is not None and (prev - 1) * (rr - 1) <= 0: print(f'{name}: ratio crosses 1 near h = {hh:.5f} (Archimedean truncated octahedron)')
            prev = rr
        else: prev = None
print('done')
