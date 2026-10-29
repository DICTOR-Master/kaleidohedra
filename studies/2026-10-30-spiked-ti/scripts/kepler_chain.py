# Spike-rule test (DICTO 10-30: can the four-step numbers be made exactly 5 and 12?). Parameter-free rule: Kepler's first stellation along
# each face's axis: the tip over face f is the nearest point beyond f, on the line through the centre and the foot of f, where the plane of
# one of f's edge-neighbours meets that line. For TI this puts the pentagon tips at the corners of TI's own icosahedron (its hexagon planes)
# and the hexagon tips at the corners of its own dodecahedron (its pentagon planes). Iterate S -> hull of tips; record the shapes, whether
# the chain repeats, and the radius factor per step and per period, with an attempt to recognise them in Q(sqrt5).
import json, numpy as np, sympy as sp
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return V, list(out.values())
def shape(V):
    W = V / np.linalg.norm(V, axis=1).max(); d = np.linalg.norm(W[:, None] - W[None], axis=2)
    return (len(W), tuple(sorted({round(x, 6) for x in d.ravel() if x > 1e-9})[:5]), tuple(sorted({round(x, 6) for x in np.linalg.norm(W, axis=1)})))
def tips(V, FL):
    T = []
    for fi, (eq, ids) in enumerate(FL):
        n = eq[:3]; d = -eq[3]; best = None
        for fj, (eq2, ids2) in enumerate(FL):
            if fj == fi or len(set(ids) & set(ids2)) < 2: continue   # edge-neighbours only
            den = eq2[:3] @ n
            if abs(den) < 1e-12: continue
            lam = -eq2[3] / den                                       # point lam*n on plane 2
            if lam > d + 1e-9 and (best is None or lam < best): best = lam
        T.append(best * n)
    return np.array(T)
def recog(x):
    try: return str(sp.nsimplify(x, [sp.sqrt(5)], tolerance=1e-10))
    except Exception: return None
S = P; rows = []; shapes = [shape(P)]
for k in range(12):
    V, FL = facelist(S); TP = tips(V, FL)
    f = np.linalg.norm(TP, axis=1).max() / np.linalg.norm(V, axis=1).max(); sh = shape(TP)
    rep = [i for i, s0 in enumerate(shapes) if s0 == sh]
    rows.append(dict(step=k + 1, corners=sh[0], radius_factor=f, radius_factor_sq=f * f, recognised_sq=recog(f * f), repeats=rep))
    shapes.append(sh); S = TP
    if rep: break
per = None
if rows[-1]['repeats']:
    i0 = rows[-1]['repeats'][0]; per = len(rows) - i0
    prod = np.prod([r['radius_factor'] for r in rows[i0:]]); rows.append(dict(period=per, period_radius_factor=prod, recognised_sq=recog(prod * prod)))
print(json.dumps(rows, indent=1)); json.dump(rows, open('data/kepler-chain.json', 'w'), indent=1)
