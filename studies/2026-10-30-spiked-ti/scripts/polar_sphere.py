# TI Star: the sphere about which the middle of a turn is self-polar. Ip and Dh are polar to each other in the sphere of radius rho with
# rho^2 = R(Ip) * r(Dh) (circumradius of the icosahedron times inradius of the dodecahedron); check also rho^2 = R(Dh) * r(Ip), that
# polar(K) = core and polar(core) = K exactly at rho, and where the polars of TI, I_TI, D_TI and s.TI fall among the turn's solids.
import json, numpy as np
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
def same(A, B): return abs(ConvexHull(A).volume - ConvexHull(B).volume) < 1e-8 * ConvexHull(B).volume and np.all(A @ pl(B)[:, :3].T + pl(B)[:, 3] < 1e-8)
def rel(A, B):
    if same(A, B): return 'same'
    d = A @ pl(B)[:, :3].T + pl(B)[:, 3]
    if np.all(d <= 1e-9): return 'inside'
    d2 = B @ pl(A)[:, :3].T + pl(A)[:, 3]
    if np.all(d2 <= 1e-9): return 'contains'
    return 'crosses'
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
    R = lambda Q: np.linalg.norm(Q, axis=1).max(); r = lambda Q: (-pl(Q)[:, 3]).min()
    rho2a, rho2b = R(pen) * r(hexa), R(hexa) * r(pen); rho = rho2a ** .5
    S = {'TI': P, 'I_TI': I_TI, 'D_TI': D_TI, 'core': core, 'Ip': pen, 'Dh': hexa, 'K': K, 's·TI': s * P}
    pol = {k: polar(v, rho) for k, v in S.items()}
    checks = dict(rho=rho, rho2_two_ways=[rho2a, rho2b], polar_Ip_is_Dh=bool(same(pol['Ip'], hexa)), polar_Dh_is_Ip=bool(same(pol['Dh'], pen)),
                  polar_K_is_core=bool(same(pol['K'], core)), polar_core_is_K=bool(same(pol['core'], K)))
    place = {f'polar({k})': {k2: rel(v, S[k2]) for k2 in S} for k, v in pol.items() if k in ('TI', 'I_TI', 'D_TI', 's·TI')}
    vols = {f'polar({k})': round(ConvexHull(v).volume / VT, 6) for k, v in pol.items()}
    out[SCN] = dict(checks=checks, placement=place, volumes_over_TI=vols, rho_over_TI_radius=rho / R(P))
print(json.dumps(out, indent=1, ensure_ascii=False, default=float)); json.dump(out, open('data/polar-sphere.json', 'w'), indent=1, ensure_ascii=False, default=float)
