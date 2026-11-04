import sys, numpy as np, json
src = open('scripts/verify_tiling.py').read().split("vol_piece = hS.volume")[0]
exec(src)
from scipy.spatial import ConvexHull, Delaunay
D = [Delaunay(c) for c in copies]; rng = np.random.default_rng(1); X = rng.uniform(-5, 5, (20000, 3))
cnt = np.zeros(len(X), int)
for d in D: cnt += d.find_simplex(X) >= 0
G = X[cnt == 0]
eqs = [ConvexHull(c).equations for c in copies]
# signed distance of each gap point to the nearest copy (max over facets <= 0 inside)
dist = [min(np.max(e[:, :3] @ g + e[:, 3]) for e in eqs) for g in G]
cen = np.array([c.mean(0) for c in copies])
print('copies', len(copies), 'gap points', len(G), 'dist to nearest copy: max', max(dist), 'median', float(np.median(dist)))
print('gap pts sample', np.round(G[:5], 3).tolist())
print('distance of gap points to origin max/min', float(np.linalg.norm(G, axis=1).max()), float(np.linalg.norm(G, axis=1).min()))
# is each gap point inside some copy's cells? classify by octet cell
