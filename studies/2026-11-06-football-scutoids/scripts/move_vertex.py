"""Football scutoid study, step 3b: the scutoid move located precisely. The move is a corner of the cell partition where four cells meet:
the reference cell, its two diagonal neighbours of the same layer, and the cell of the next layer that is pushed out. Bodies are exact
convex pieces (ball, and each bridge cut in half at its middle plane); the distance from a point to a body is the true Euclidean
distance (to the nearest face polygon, edge or corner). Solve dist to all four equal (3 equations), starting from the voxel estimate,
then report the corner's height and which feature (face / edge / corner) of each body is nearest - if all are faces, the corner is the
meeting point of three bisector planes and is exact by linear algebra.
Run: STACK=loose|tight python3 tools/runjob.py <this> <data file>"""
import os, json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import least_squares
exec(open('cut_cells.py').read().split('def tri_samples')[0])
# ---- exact convex pieces: balls and half bridges
def hull_faces(P):
    H = ConvexHull(P); fs = {}
    for eq, s in zip(H.equations, H.simplices): fs.setdefault(tuple(np.round(eq, 9)), set()).update(s)
    out = []
    for eq, idx in fs.items():
        idx = list(idx); nn = np.array(eq[:3]); c = P[idx].mean(0); u = P[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(nn, u)
        idx.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); out.append((nn, P[idx]))
    return out
def seg_dist(p, a, b):
    t = np.clip((p - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1); q = a + t * (b - a); return np.linalg.norm(p - q), q
def poly_dist(p, nn, Q):
    """distance from p to the convex polygon Q (plane normal nn); and the kind of nearest feature"""
    d = (p - Q[0]) @ nn; proj = p - d * nn
    inside = all(np.cross(Q[(i + 1) % len(Q)] - Q[i], proj - Q[i]) @ nn >= -1e-12 for i in range(len(Q)))
    if inside: return abs(d), 'face'
    best = min((seg_dist(p, Q[i], Q[(i + 1) % len(Q)]) for i in range(len(Q))), key=lambda t: t[0])
    q = best[1]; kind = 'corner' if min(np.linalg.norm(q - v) for v in Q) < 1e-9 else 'edge'
    return best[0], kind
def body_parts(i, j, off):
    Vb, R = ball(i, j); parts = [hull_faces(Vb + off)]
    c = centre(i, j)
    for di, dj, d in ((1, 0, e1), (0, 1, e2), (-1, 0, -e1), (0, -1, -e2)):
        k1, f1 = face_toward(i, j, d); k2, f2 = face_toward(i + di, j + dj, -d)
        allp = np.vstack([f1, f2]); H = ConvexHull(allp); mid = c + d * D / 2; cut = []
        for s in H.simplices:
            for u, v in itertools.combinations(s, 2):
                su, sv = (allp[u] - mid) @ d, (allp[v] - mid) @ d
                if su * sv < 0: t = su / (su - sv); cut.append(allp[u] + t * (allp[v] - allp[u]))
        half = np.vstack([f1, np.array(cut)])
        parts.append(hull_faces(np.unique(np.round(half, 12), axis=0) + off))
    return parts
def dist(p, parts):
    best = (np.inf, None)
    for faces in parts:
        inside = all((p - Q[0]) @ nn <= 0 for nn, Q in faces)
        if inside: return 0.0, 'inside'
        best = min(best, min((poly_dist(p, nn, Q) for nn, Q in faces), key=lambda t: t[0]), key=lambda t: t[0])
    return best
def body(kind, p, q, r):
    i = 0 if kind == 0 else 1
    return body_parts(i, 0, p * P1 + q * P2 + r * T)
# ---- the moves seen in cell_track (reference X(0,0,0)); voxel heights as start
track = open('../data-track-tight.txt' if os.environ.get('STACK') == 'tight' else '../data-track.txt').read()
import re
moves = []
for line in track.split('cell Y:')[0].splitlines():
    m = re.match(r"\s+slice \d+ \(w ([-+.\d]+)\): (.*)", line)
    if m and 'SWAP-gain X(+1,-1,+0)' in m.group(2) and 'SWAP-lose' in m.group(2):
        lost = re.search(r"SWAP-lose ([XY])\(([-+\d]+),([-+\d]+),([-+\d]+)\)", m.group(2)); moves.append((float(m.group(1)), lost.groups(), 'gain'))
    if m and 'SWAP-lose X(+1,-1,+0)' in m.group(2) and 'SWAP-gain' in m.group(2):
        got = re.search(r"SWAP-gain ([XY])\(([-+\d]+),([-+\d]+),([-+\d]+)\)", m.group(2)); moves.append((float(m.group(1)), got.groups(), 'lose'))
print(f"moves of cell X(0,0,0) from the voxel run: {[(w, ''.join(g)) for w, g, _ in moves]}")
ref = body(0, 0, 0, 0); diag1 = body(0, 1, -1, 0); diag2 = body(0, -1, 1, 0)
results = []
for w0, (k, p, q, r_), _ in moves:
    other = body('XY'.index(k), int(p), int(q), int(r_))
    bodies4 = [ref, diag1, diag2, other]
    # start: the point of the slice at height w0 nearest to equidistance, via a coarse search near the cell's corner region
    best = None
    for uu, vv in itertools.product(np.linspace(-0.6, 0.6, 61), repeat=2):
        x = uu * P1 + vv * P2 + w0 * T
        ds = [dist(x, b)[0] for b in bodies4]; s = np.ptp(ds) + 0.01 * max(ds)
        if best is None or s < best[0]: best = (s, x)
    Mb = np.array([P1, P2, T]).T
    x0 = np.linalg.solve(Mb, best[1])
    f = lambda c: [dist(Mb @ c, bodies4[0])[0] - dist(Mb @ c, bodies4[i])[0] for i in (1, 2, 3)]
    r = least_squares(f, x0, bounds=(x0 - [0.15, 0.15, 0.08], x0 + [0.15, 0.15, 0.08]), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    x = Mb @ r.x; ds = [dist(x, b) for b in bodies4]
    # the four must be the nearest bodies there (no other cell closer)
    spread = np.ptp([d[0] for d in ds]); ok = spread < 1e-9 and np.all(np.abs(r.x - x0) < [0.149, 0.149, 0.079])
    results.append(ok)
    print(f"move near w {w0:+.3f} (other cell {k}({p},{q},{r_})): corner at height w = {r.x[2]:+.10f} of a period "
          f"({r.x[2] * h:+.8f} above the layer's middle plane); distance to the four bodies {[f'{d[0]:.10f}' for d in ds]} (spread {spread:.1e}); "
          f"nearest features {[d[1] for d in ds]}; {'CONVERGED inside the search box' if ok else 'NOT CONVERGED'}")
print("FINAL ok" if results and all(results) else "FINAL FAIL (a corner did not converge)")
