# Cut each Kepler–Poinsot valley (a hull minus its star) by the axes of the hull's faces, and test whether each part is one convex piece.
import numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
exec(open('kp.py').read().split('from scipy.sparse.csgraph')[0])
def valley_pieces(hull, parts, core, name):
    P = gap_points(hull, parts, core, n=1500000)
    n, d = planes(hull); u = P / np.linalg.norm(P, axis=1)[:, None]
    lab = np.argmax(u @ n.T, axis=1)                        # which hull face each point sits under
    vals = []
    for k in range(len(d)):
        Q = P[lab == k]; H = ConvexHull(Q)
        frac = len(Q) / len(P)
        vals.append((frac, H.volume, len(Q)))
    vol = hv(hull) - (hv(core) + sum(hv(p) for p in parts))
    fr = np.array([v[0] for v in vals]); hullvol = np.array([v[1] for v in vals])
    print(f'{name}: {len(d)} parts (one per hull face), each {fr.mean() * vol:.5f} by volume share; hull of its points {hullvol.mean():.5f}',
          '-> convex' if abs(hullvol.mean() - fr.mean() * vol) / (fr.mean() * vol) < 0.01 else '-> not convex')
    k = 0; Q = P[lab == k]; H = ConvexHull(Q); V = Q[H.vertices]
    # corners of that part: cluster hull vertices
    pts = []
    for v in V:
        if not any(np.linalg.norm(v - p) < 0.05 * np.linalg.norm(hull[0]) for p in pts): pts.append(v)
    print('   approx. corners of one part:', len(pts), ' at radii', sorted(set(np.round(np.linalg.norm(pts, axis=1), 2))))
valley_pieces(D1, GSD, I, 'valleys D1 - GSD')
valley_pieces(I2, SSD, D1, 'valleys I2 - SSD')
