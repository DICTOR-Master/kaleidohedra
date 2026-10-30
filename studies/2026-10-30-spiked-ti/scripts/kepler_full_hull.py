# Kepler chain with the full hull (DICTO 10-30: "is there no value in exploring the spiked hull and how that might be rectified or filled").
# The second Kepler step failed because some corners of the solid stand outside the hull of the spike tips. Rectified rule: the next solid
# is the hull of the whole star, its corners and its tips together. For each step: which corners of the solid and which tips are corners of
# that hull, its faces, its shape (against TI, Catalan pentakis, Star Halo, core, and earlier steps), the gap hull minus star, and the chain.
import json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return V, list(out.values())
def ktips(V, FL):
    T = []
    for fi, (eq, ids) in enumerate(FL):
        n = eq[:3]; d = -eq[3]; best = None
        for fj, (eq2, ids2) in enumerate(FL):
            if fj == fi or len(set(ids) & set(ids2)) < 2: continue
            den = eq2[:3] @ n
            if abs(den) < 1e-12: continue
            lam = -eq2[3] / den
            if lam > d + 1e-9 and (best is None or lam < best): best = lam
        T.append(best * n)
    return np.array(T)
def shape(V):
    W = V / np.linalg.norm(V, axis=1).max(); d = np.linalg.norm(W[:, None] - W[None], axis=2)
    return (len(W), tuple(sorted({round(x, 6) for x in d.ravel() if x > 1e-9})[:5]), tuple(sorted({round(x, 6) for x in np.linalg.norm(W, axis=1)})))
def kinds(Q):
    V, FL = facelist(Q); c = {}
    for _, ids in FL: c[len(ids)] = c.get(len(ids), 0) + 1
    return dict(sorted(c.items()))
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
cut = lambda H: (lambda W: W[ConvexHull(W).vertices])(HalfspaceIntersection(H, np.zeros(3)).intersections)
V0, F0 = facelist(P)
refs = {'TI': P, 'Catalan pentakis': cut(np.hstack([V0, -np.ones((len(V0), 1))])), 'Star Halo': np.array([(-eq[3]) * eq[:3] for eq, _ in F0])}
pen = np.array([phi * V0[ids].mean(0) for _, ids in F0 if len(ids) == 5]); hexa = np.array([phi * V0[ids].mean(0) for _, ids in F0 if len(ids) == 6])
refs['core'] = cut(np.vstack([pl(pen), pl(hexa)]))
rows = []; S = P; seen = [('S0', shape(P))]
for k in range(8):
    V, FL = facelist(S); T = ktips(V, FL); A = np.vstack([V, T]); h = ConvexHull(A)
    hv = set(h.vertices); n_corners_kept = sum(1 for i in hv if i < len(V)); n_tips = sum(1 for i in hv if i >= len(V))
    H = A[sorted(hv)]
    spikes_vol = sum(ConvexHull(np.vstack([V[ids], T[fi]])).volume for fi, (_, ids) in enumerate(FL))
    star = ConvexHull(V).volume + spikes_vol
    sh = shape(H); same = [nm for nm, R in refs.items() if shape(R[ConvexHull(R).vertices]) == sh] + [nm for nm, s0 in seen if s0 == sh]
    rows.append(dict(step=k + 1, from_corners=len(V), hull_corners=len(H), of_which_old_corners=n_corners_kept, of_which_tips=n_tips, hull_faces=kinds(H),
                     star_over_S=star / ConvexHull(V).volume, hull_over_star=h.volume / star, gap_over_S=(h.volume - star) / ConvexHull(V).volume,
                     radius_factor=float(np.linalg.norm(H, axis=1).max() / np.linalg.norm(V, axis=1).max()), same_shape_as=same))
    seen.append((f'S{k + 1}', sh)); S = H
    if same and k > 0: break
print(json.dumps(rows, indent=1, default=float)); json.dump(rows, open('data/kepler-full-hull.json', 'w'), indent=1, default=float)
