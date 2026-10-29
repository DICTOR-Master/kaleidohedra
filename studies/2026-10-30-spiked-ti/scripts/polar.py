# TI Star: the polar cycle. Polar reciprocation in the unit sphere about the common centre (point v -> plane x.v = 1) of every convex
# solid of one turn; the polars nest in reverse order. Is each polar similar to a solid of the turn (same shape up to scale)? If the
# polar of the whole turn is the turn again, the cycle is self-polar; otherwise the polar cycle is a new one.
import json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
cut = lambda H: (lambda W: W[ConvexHull(W).vertices])(HalfspaceIntersection(H, np.zeros(3)).intersections)
def polar(Q): V = Q[ConvexHull(Q).vertices]; return cut(np.hstack([V, -np.ones((len(V), 1))]))
def sig(Q):   # shape signature up to scale: corner count, face kinds, sorted normalised radii and edge lengths
    V = Q[ConvexHull(Q).vertices]; R = np.linalg.norm(V, axis=1).max(); V = V / R
    kinds = {}
    for eq in pl(V):
        n = sum(1 for p in V if abs(eq[:3] @ p + eq[3]) < 1e-7); kinds[n] = kinds.get(n, 0) + 1
    d = np.linalg.norm(V[:, None] - V[None], axis=2); m = d[d > 1e-9].min()
    edges = sorted({round(x, 5) for x in d[(d > 1e-9) & (d < 1.6 * m)].ravel()})
    return (len(V), tuple(sorted(kinds.items())), tuple(sorted({round(x, 5) for x in np.linalg.norm(V, axis=1)})), tuple(edges))
EQ = pl(P); nper = [sum(1 for p in P if abs(eq[:3] @ p + eq[3]) < 1e-8) for eq in EQ]
D_TI = cut(EQ[[n == 5 for n in nper]]); I_TI = cut(EQ[[n == 6 for n in nper]])
F = []; seen = set()
for eq in ConvexHull(P).equations:
    k = tuple(np.round(eq, 7))
    if k not in seen: seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
out = {}
for SCN, s in [('phi', phi), ('2', 2.0)]:
    tips = [s * P[f].mean(0) for f in F]
    pen = np.array([t for t, f in zip(tips, F) if len(f) == 5]); hexa = np.array([t for t, f in zip(tips, F) if len(f) == 6])
    core = cut(np.vstack([pl(pen), pl(hexa)]))
    S = {'TI': P, 'I_TI': I_TI, 'D_TI': D_TI, 'core': core, 'Ip': pen, 'Dh': hexa, 'K': np.vstack([pen, hexa])}
    sigs = {k: sig(v) for k, v in S.items()}
    rows = []
    for k, v in S.items():
        pv = polar(v); ps = sig(pv)
        match = [k2 for k2, s2 in sigs.items() if s2 == ps]
        kinds = dict(ps[1]); rows.append(dict(solid=k, polar_corners=ps[0], polar_faces=kinds, polar_radii=ps[2], polar_edge_lengths=ps[3], same_shape_as=match))
    out[SCN] = rows
json.dump(out, open('data/polar.json', 'w'), indent=1, ensure_ascii=False, default=str)
for SCN, rows in out.items():
    print('== s =', SCN)
    for r in rows: print(' polar of', r['solid'], ':', r['polar_corners'], 'corners', r['polar_faces'], 'radii', r['polar_radii'], 'edges', r['polar_edge_lengths'][:3], '-> same shape as', r['same_shape_as'])
