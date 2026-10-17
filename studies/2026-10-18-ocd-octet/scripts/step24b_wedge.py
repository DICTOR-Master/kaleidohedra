# DICTO 2026-10-18 octet study -- STEP 24b: the two wedges left after the phi^-2 half-octahedron, exactly: corners snapped to the exact
# corners of step 24's convex parts, convexity, faces, edge lengths and named angles (golden 63.43/116.57, Penrose 36/72/108/144).
import math
from exactpoly import *
S = load('step24-outer-corner.json'); M = load('step24-mesh.json')
exact_pts = [[q(x) for x in p] for piece in S['pieces'] for p in piece]
def snap(p):
    best = min(exact_pts, key=lambda e: sum((qf(a) - b) ** 2 for a, b in zip(e, p))); assert sum((qf(a) - b) ** 2 for a, b in zip(best, p)) < 1e-10; return best
NAMED = [('golden 63.43', (Fr(1, 5), Fr(0)), 1), ('golden 116.57', (Fr(1, 5), Fr(0)), -1), ('Penrose 36', (Fr(3, 8), Fr(1, 8)), 1), ('Penrose 144', (Fr(3, 8), Fr(1, 8)), -1),
         ('Penrose 72', (Fr(3, 8), Fr(-1, 8)), 1), ('Penrose 108', (Fr(3, 8), Fr(-1, 8)), -1), ('90', Z, 0), ('60', (Fr(1, 4), Fr(0)), 1), ('120', (Fr(1, 4), Fr(0)), -1),
         ('45', (Fr(1, 2), Fr(0)), 1), ('135', (Fr(1, 2), Fr(0)), -1), ('31.72 (half golden)', ((Fr(5) + 0) / 10 + Fr(1, 2) * 0, Fr(1, 10)), 1)]
def ang(u, w):
    uw = dot(u, w); c2 = qd(qm(uw, uw), qm(dot(u, u), dot(w, w))); s = sgn(uw)
    for nm, val, sg in NAMED:
        if c2 == val and s == sg: return nm
    return f'{math.degrees(math.acos(max(-1, min(1, qf(uw) / math.sqrt(qf(dot(u, u)) * qf(dot(w, w))))))):.2f}'
out = []
for part in M['parts']:
    C = [snap(p) for p in part['corners']]; vol = volume(C); Cf = np.array([[qf(x) for x in p] for p in C]); hh = ConvexHull(Cf)
    faces = []
    for e in np.unique(np.round(hh.equations, 9), axis=0):
        idx = [i for i in range(len(C)) if abs(Cf[i] @ e[:3] + e[3]) < 1e-9]
        c = Cf[idx].mean(0); n = e[:3]; u = Cf[idx[0]] - c; w = np.cross(n, u); idx = [idx[k] for k in np.argsort(np.arctan2((Cf[idx] - c) @ w, (Cf[idx] - c) @ u))]
        X = [C[i] for i in idx]
        faces.append(dict(corners=len(X), edges=[round(qf(dot(vsub(X[(k + 1) % len(X)], X[k]), vsub(X[(k + 1) % len(X)], X[k]))) ** .5, 5) for k in range(len(X))],
                          angles=[ang(vsub(X[k - 1], X[k]), vsub(X[(k + 1) % len(X)], X[k])) for k in range(len(X))]))
    out.append(dict(volume=qs_(vol), volume_float=qf(vol), mesh_volume=part['volume'], convex=abs(qf(vol) - part['volume']) < 1e-9, faces=faces))
print(json.dumps(out[0], indent=1)); print('second wedge same volume:', out[0]['volume'] == out[1]['volume'])
save('step24b-wedge.json', dict(mark=MARK, step='24b', wedges=out))
