# DICTO 2026-10-20 "how efficiently does it fill space by itself?": densest LATTICE packing (float search) of the OTT and the DBT,
# both centrally symmetric. Translates K+u, K+v are disjoint iff u - v lies outside the interior of 2K, so a lattice with basis B packs
# K iff every nonzero lattice vector v has gauge_2K(v) = max_i n_i.v / (2 d_i) >= 1. Minimise |det B| from many random starts
# (SLSQP), then check with lattice vectors up to coefficient 3 and with mesh overlaps of the 26 nearest copies (manifold3d).
# Sanity: the octahedron (Minkowski 18/19 = 0.947368) and the rhombic triacontahedron (0.801741, Torquato-Jiao / Betke-Henk).
import json, sys, itertools, math, numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
H = '/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
def load(f): return np.array([[fq(c) for c in v] for v in json.load(open(H + f))['V']])
DB = load('dbt-exact.json'); OT = load('cut8-exact.json')
n1 = np.ones(3) / 3 ** .5; Eq = ConvexHull(DB).equations; Eq = Eq[np.abs(np.abs(Eq[:, :3] @ n1) - 1) > 1e-6]
from scipy.spatial import HalfspaceIntersection
RT = HalfspaceIntersection(Eq, np.zeros(3)).intersections
OCT = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
def planes(P):
    E = ConvexHull(P).equations; out = []
    for e in E:
        if not any(np.allclose(e, u, atol=1e-9) for u in out): out.append(e)
    E = np.array(out); return E[:, :3] / (-E[:, 3:4])     # n.x <= 1 form
C2 = np.array([c for c in itertools.product(range(-2, 3), repeat=3) if any(c)])
C3 = np.array([c for c in itertools.product(range(-3, 4), repeat=3) if any(c)])
def run(name, P, starts=300, seed=1):
    N = planes(P); vol = ConvexHull(P).volume; scale = np.cbrt(vol)
    gauge = lambda V: (V @ N.T).max(axis=1) / 2          # gauge of 2K
    def cons(b, C=C2): return gauge(C @ b.reshape(3, 3)) - 1
    def reduced(b):   # Minkowski-reduced basis (keeps the lattice non-degenerate, so short vectors have small coefficients)
        B = b.reshape(3, 3); n = [B[i] @ B[i] for i in range(3)]; out = [n[1] - n[0], n[2] - n[1]]
        for i, j in ((0, 1), (0, 2), (1, 2)): out += [n[i] - 2 * (B[i] @ B[j]), n[i] + 2 * (B[i] @ B[j])]
        for s1, s2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)): v = B[2] + s1 * B[0] + s2 * B[1]; out.append(v @ v - n[2])
        return np.array(out)
    rng = np.random.default_rng(seed); best = None
    for k in range(starts):
        b0 = rng.normal(size=(3, 3)) * scale * 1.5
        b0 *= 1.3 / max(1e-9, cons(b0.ravel()).min() + 1) if cons(b0.ravel()).min() + 1 > 0 else 1
        r = minimize(lambda b: abs(np.linalg.det(b.reshape(3, 3))), b0.ravel(), method='SLSQP', constraints=[{'type': 'ineq', 'fun': cons}, {'type': 'ineq', 'fun': reduced}], options={'maxiter': 400, 'ftol': 1e-12})
        if not r.success: continue
        b = r.x; c3 = cons(b, C3).min()
        if c3 < -1e-7 or reduced(b).min() < -1e-7 or abs(np.linalg.det(b.reshape(3, 3))) < 0.3 * vol: continue
        d = vol / abs(np.linalg.det(b.reshape(3, 3)))
        if best is None or d > best[0] + 1e-9: best = (d, b.reshape(3, 3))
    d, B = best
    # mesh check: copies at the 26 nearest lattice points must not overlap the central one
    K = m3.Manifold.hull_points(P); ov = 0
    for c in itertools.product(range(-1, 2), repeat=3):
        if any(c): ov += (K ^ K.translate(np.array(c) @ B)).volume()
    contacts = int(np.sum(np.abs(cons(B.ravel(), C3)) < 1e-6)) // 2
    print(f'{name}: densest lattice packing found {d:.6f}  (volume {vol:.6f}, cell {abs(np.linalg.det(B)):.6f}; contact pairs {contacts}; overlap with 26 neighbours {ov:.2e})', flush=True)
    return d, B
res = {}
for name, P, st in (('octahedron', OCT, 120), ('rhombic triacontahedron', RT, 300), ('DICTO OTT', OT, 400), ('DICTO DBT', DB, 400)):
    d, B = run(name, P, st); res[name] = dict(density=d, basis=B.round(6).tolist())
json.dump(res, open(H + 'lattice-pack.json', 'w'), indent=1); print('saved lattice-pack.json')
