# TI Star: the cycle and its polar cycle in one space. Bring the polar solids into the same turn (between TI and s.TI) by scaling with
# powers of s, and list all distinct solids of the merged turn in order, with every inclusion between them.
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
def polar(Q, rho): V = Q[ConvexHull(Q).vertices]; return cut(np.hstack([V, -rho ** 2 * np.ones((len(V), 1))]))
def inside(A, B): return bool(np.all(A @ pl(B)[:, :3].T + pl(B)[:, 3] <= 1e-9))
EQ = pl(P); nper = [sum(1 for p in P if abs(eq[:3] @ p + eq[3]) < 1e-8) for eq in EQ]
D_TI = cut(EQ[[n == 5 for n in nper]]); I_TI = cut(EQ[[n == 6 for n in nper]])
F = []; seen = set()
for eq in ConvexHull(P).equations:
    k = tuple(np.round(eq, 7))
    if k not in seen: seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
VT = ConvexHull(P).volume; out = {}
for SCN, s in [('phi', phi), ('2', 2.0)]:
    tips = [s * P[f].mean(0) for f in F]
    pen = np.array([t for t, f in zip(tips, F) if len(f) == 5]); hexa = np.array([t for t, f in zip(tips, F) if len(f) == 6])
    core = cut(np.vstack([pl(pen), pl(hexa)])); K = np.vstack([pen, hexa])
    rho = (np.linalg.norm(pen, axis=1).max() * (-pl(hexa)[:, 3]).min()) ** .5
    S = {'TI': P, 'I_TI': I_TI, 'D_TI': D_TI, 'core': core, 'Ip': pen, 'Dh': hexa, 'K': K, 's·TI': s * P}
    # polar solids scaled into [TI, s.TI]
    for k in ('TI', 'I_TI', 'D_TI'):
        Q = polar(S[k], rho); n = 0
        while not inside(Q, s * P) or not inside(P, Q):
            Q = Q / s; n += 1
            if n > 6: break
        S[f'polar({k})/s^{n}'] = Q
    names = sorted(S, key=lambda k: ConvexHull(S[k]).volume)
    inc = [(a, b) for a, b in itertools.permutations(names, 2) if inside(S[a], S[b])]
    cover = [(a, b) for a, b in inc if not any((a, c) in inc and (c, b) in inc for c in names if c not in (a, b))]
    cross = [(a, b) for a, b in itertools.combinations(names, 2) if (a, b) not in inc and (b, a) not in inc]
    out[SCN] = dict(rho=rho, order=[(k, round(ConvexHull(S[k]).volume / VT, 6), len(ConvexHull(S[k]).vertices)) for k in names], covers=cover, crossing_pairs=cross)
print(json.dumps(out, indent=1, ensure_ascii=False, default=float)); json.dump(out, open('data/merged-turn.json', 'w'), indent=1, ensure_ascii=False, default=float)
