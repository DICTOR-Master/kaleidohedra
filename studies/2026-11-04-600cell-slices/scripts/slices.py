#!/usr/bin/env python3
"""600-cell slices (Concordance 6.1 row '600-cell slices': IQ, Mahler, Dehn). Corners: 120 unit icosians; edges at distance 1/φ (720 edges, checked).
Section by a·x = h: hull of edge crossings (+ corners on the plane) in an orthonormal frame of the hyperplane. Axes: corner-first a = a corner; cell-first a = centre of a tetrahedral cell."""
import sys, itertools, math, json, numpy as np
from scipy.spatial import ConvexHull
sys.argv = sys.argv[:1] + ['x', '8', '300']; exec(open('scripts/dehn.py').read().split("if __name__")[0])
phi = (1 + 5**.5)/2
V = [p for p in itertools.product((-1, 1, 0), repeat=4) if sum(abs(x) for x in p) == 1]
V += [tuple(s/2 for s in sg) for sg in itertools.product((1, -1), repeat=4)]
base = (phi/2, 1/2, 1/(2*phi), 0)
evenp = [p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
for p in evenp:
    for sg in itertools.product((1, -1), repeat=3):
        v = [0]*4; vals = [base[0]*sg[0], base[1]*sg[1], base[2]*sg[2], 0]
        for i in range(4): v[p[i]] = vals[i]
        V.append(tuple(v))
V = np.unique(np.round(np.array(V, float), 12), axis=0); assert len(V) == 120
D = np.linalg.norm(V[:, None] - V[None], axis=2); E = [(i, j) for i in range(120) for j in range(i + 1, 120) if abs(D[i, j] - 1/phi) < 1e-9]; assert len(E) == 720
def frame(a):
    a = a/np.linalg.norm(a); M = np.linalg.qr(np.column_stack([a, np.eye(4)[:, :3]]))[0]; return a, M[:, 1:4]
def section(a, h):
    a, F = frame(a); pts = [V[i] for i in range(120) if abs(V[i] @ a - h) < 1e-12]
    for i, j in E:
        s, t = V[i] @ a - h, V[j] @ a - h
        if s*t < 0: pts.append(V[i] + (V[j] - V[i])*(s/(s - t)))
    P = np.array(pts) @ F
    return np.unique(np.round(P, 10), axis=0)
def meas(P):
    h = ConvexHull(P); c = P[h.vertices].mean(0); Q = P - c; h = ConvexHull(Q)
    pol = np.array([eq[:3]/(-eq[3]) for eq in h.equations]); X, Fc = hull_faces(Q[h.vertices]); d = dehn(X, Fc)
    return 36*math.pi*h.volume**2/h.area**3, h.volume*ConvexHull(pol).volume, d['dehn_zero'], len(h.vertices)
cell = V[[0]].copy()
# a tetrahedral cell: 4 mutually adjacent corners containing V[0]
nb = [j for j in range(120) if abs(D[0, j] - 1/phi) < 1e-9]
tri = next((x, y, z) for x, y, z in itertools.combinations(nb, 3) if all(abs(D[p, q] - 1/phi) < 1e-9 for p, q in ((x, y), (x, z), (y, z))))
axes = {'corner-first': V[0], 'cell-first': V[[0, *tri]].mean(0)}
out = {}
for nm, a in axes.items():
    an = a/np.linalg.norm(a); hs = sorted({round(float(v @ an), 9) for v in V}); hmax = hs[-1]
    rows = []
    for h in np.linspace(0, hmax - 1e-6, 400):
        try: rows.append((float(h), *meas(section(a, h))))
        except Exception: pass
    iq = max(rows, key=lambda r: r[1]); ma = max(rows, key=lambda r: r[2]); dz = sorted({round(r[0], 4) for r in rows if r[3]})
    out[nm] = {'IQ_max': iq[:2], 'Mahler_max': (ma[0], ma[2]), 'dehn_zero_heights': dz[:40], 'n_dehn_zero': len(dz), 'n': len(rows),
               'IQ_at_0': rows[0][1], 'Mahler_at_0': rows[0][2], 'corners_at_0': rows[0][4]}
    print(nm, json.dumps(out[nm]), flush=True)
json.dump(out, open('data/slices.json', 'w'), indent=1)
