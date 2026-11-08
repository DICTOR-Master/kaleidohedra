# tmin_tests.py -- exact t_min(S) = least t with S inside t P(S) (P = hull of the foot points of S's face planes).
# 1. SANITY (known case, #43 Theorem 1/2): the five Platonic solids give 9, 3, 3, 15-6sqrt5, 15-6sqrt5 exactly.
# 2. TEST of the theorem: octahedral solids (Archimedean, Catalan, #81/#91's cube-octahedron sweep P_mu =
#    [-1,1]^3 cut by |x|+|y|+|z| <= mu) exactly; random octahedral (also chiral, rotations only) orbit hulls in floats.
# 3. CONTRAST (float): pyritohedral (T_h) and tetrahedral (T) orbit hulls, where the theorem does not apply.
# Exact = sympy in Q, Q(sqrt2), Q(sqrt5): combinatorics from a float hull, every plane, foot point and ratio exact,
# t_min compared with 3 by the exact sign of 3 - t_min.
import itertools, sys, time
import numpy as np
import sympy as sp
from scipy.spatial import ConvexHull

t0 = time.time()
s2, s5 = sp.sqrt(2), sp.sqrt(5)
phi = (1 + s5) / 2

def planes(P):
    """exact face planes (N, d) with N.x <= d, d > 0, of the hull of the exact points P"""
    Pf = np.array([[float(c) for c in p] for p in P])
    hull = ConvexHull(Pf)
    out, seen = [], []
    for eq in hull.equations:
        n, off = eq[:3], -eq[3]
        if any(np.allclose(n, m, atol=1e-9) and abs(off - o) < 1e-9 for m, o in seen):
            continue
        seen.append((n, off))
        on = [i for i in range(len(P)) if abs(Pf[i] @ n - off) < 1e-8]
        p0 = P[on[0]]
        for j, k in itertools.combinations(on[1:], 2):
            N = (P[j] - p0).cross(P[k] - p0)
            if any(abs(float(c)) > 1e-9 for c in N):
                break
        N = sp.Matrix([sp.nsimplify(sp.radsimp(c)) for c in N])
        d = sp.radsimp(N.dot(p0))
        if float(d) < 0: N, d = -N, -d
        assert all(sp.simplify(N.dot(P[i]) - d) == 0 for i in on)       # exact coplanarity
        out.append((N, d))
    return out, hull

def corners(P):
    _, hull = planes(P)
    return [P[i] for i in sorted(set(hull.vertices))]

def tmin(P):
    P = corners(P)
    F, _ = planes(P)
    feet = [sp.Matrix([sp.radsimp(d * c / N.dot(N)) for c in N]) for N, d in F]
    G, _ = planes(feet)
    best, bestf = None, -1.0
    for v in P:
        for M, e in G:
            q = M.dot(v) / e
            qf = float(q)
            if qf > bestf + 1e-12:
                best, bestf = q, qf
    best = sp.nsimplify(sp.radsimp(best))
    R2 = max(sp.radsimp(v.dot(v)) for v in P)
    r2 = min(sp.radsimp(d**2 / N.dot(N)) for N, d in F)
    return best, sp.nsimplify(sp.radsimp(R2 / r2)), len(P), len(F)

def M(*c): return sp.Matrix(c)
def perms_signs(c, even=False):
    out = set()
    perms = itertools.permutations(range(3)) if not even else [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    for p in perms:
        for s in itertools.product([1, -1], repeat=3):
            out.add(tuple(sp.nsimplify(s[i] * c[p[i]]) for i in range(3)))
    return [sp.Matrix(x) for x in out]

def cyc_signs(c): return perms_signs(c, even=True)

checks = {}
print('1. SANITY: Platonic solids (exact)')
tet = [M(1, 1, 1), M(1, -1, -1), M(-1, 1, -1), M(-1, -1, 1)]
cube = perms_signs((1, 1, 1))
octa = perms_signs((1, 0, 0))
ico = cyc_signs((0, 1, phi))
dod = perms_signs((1, 1, 1)) + cyc_signs((0, 1 / phi, phi))
want = {'tetrahedron': 9, 'cube': 3, 'octahedron': 3, 'dodecahedron': 15 - 6 * s5, 'icosahedron': 15 - 6 * s5}
for name, P in [('tetrahedron', tet), ('cube', cube), ('octahedron', octa), ('dodecahedron', dod), ('icosahedron', ico)]:
    t, q, nv, nf = tmin(P)
    good = sp.simplify(t - want[name]) == 0 and sp.simplify(q - want[name]) == 0
    print(f'   {name:13s} V={nv:2d} F={nf:2d}  t_min = {t} = {float(t):.6f}   (R/r)^2 = {q}   {"ok" if good else "MISMATCH"}')
    checks['sanity ' + name] = good

print('2. TEST: octahedral solids (exact); theorem says t_min <= (R/r)^2 <= 3')
solids = {
    'cuboctahedron': perms_signs((1, 1, 0)),
    'truncated octahedron': perms_signs((0, 1, 2)),
    'rhombic dodecahedron': perms_signs((1, 1, 1)) + perms_signs((2, 0, 0)),
    'truncated cube': perms_signs((s2 - 1, 1, 1)),
    'rhombicuboctahedron': perms_signs((1, 1, 1 + s2)),
    'truncated cuboctahedron': perms_signs((1, 1 + s2, 1 + 2 * s2)),
    'tetrakis hexahedron': perms_signs((1, 1, 1)) + perms_signs((sp.Rational(3, 2), 0, 0)),
    'triakis octahedron': perms_signs((1 + s2, 0, 0)) + perms_signs((1, 1, 1)),
}
def Pmu(mu):
    """#91/#81 sweep: [-1,1]^3 cut by |x|+|y|+|z| <= mu (1 <= mu <= 3); corners exact"""
    pts = []
    if mu <= 2:
        pts += perms_signs((1, mu - 1, 0))
    else:
        pts += perms_signs((1, 1, mu - 2))
    return pts if mu not in (1, 3) else (octa if mu == 1 else cube)
for mu in [sp.Rational(k, 8) for k in range(9, 24)] + [phi, sp.sqrt(3)]:
    solids[f'P_mu, mu = {mu}'] = Pmu(mu)
worst = 0
for name, P in solids.items():
    t, q, nv, nf = tmin(P)
    def nonneg(x):
        x = sp.nsimplify(sp.radsimp(x))
        return x == 0 or bool(x > 0)          # exact zero test; sympy decides the sign of a nonzero radical
    ok3 = nonneg(3 - q) and nonneg(3 - t) and nonneg(q - t)
    checks['exact ' + name] = bool(ok3)
    worst = max(worst, float(t))
    print(f'   {name:40s} V={nv:2d} F={nf:2d}  t_min = {sp.nsimplify(t)} = {float(t):.6f}   (R/r)^2 = {q} = {float(q):.6f}   {"<= 3 ok" if ok3 else "EXCEEDS 3"}')
print(f'   largest t_min among the exact octahedral tests: {worst:.6f}')

# ---- float tests on random orbit hulls
def group(kind):
    Ms = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            A = np.zeros((3, 3))
            for i, j in enumerate(perm): A[j, i] = sg[i]
            Ms.append(A)
    det = lambda A: round(np.linalg.det(A))
    even = lambda A: tuple(np.argmax(np.abs(A), axis=0)) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    if kind == 'O': return [A for A in Ms if det(A) == 1]
    if kind == 'Oh': return Ms
    if kind == 'Th': return [A for A in Ms if even(A)]
    if kind == 'T': return [A for A in Ms if even(A) and det(A) == 1]

def tmin_float(P):
    h = ConvexHull(P)
    eqs = np.unique(np.round(h.equations, 10), axis=0)
    feet = np.array([e[:3] * (-e[3]) for e in eqs])
    hp = ConvexHull(feet)
    V = P[h.vertices]
    G = hp.equations
    t = ((V @ G[:, :3].T) / (-G[:, 3])).max()
    R = np.linalg.norm(V, axis=1).max(); r = (-eqs[:, 3]).min()
    return t, (R / r)**2

rng = np.random.default_rng(11)
print('2b. TEST (float): random orbit hulls, 1-3 random seed points')
for kind, n in [('O', 3000), ('Oh', 2000)]:
    G = group(kind); mx = 0
    for _ in range(n):
        seeds = rng.normal(size=(rng.integers(1, 4), 3)) * rng.uniform(0.3, 1, size=(1, 1))
        P = np.array([A @ s for s in seeds for A in G])
        t, q = tmin_float(P)
        mx = max(mx, t)
    print(f'   group {kind:2s}: {n} random hulls, max t_min = {mx:.6f}')
    checks[f'float {kind} max t_min <= 3'] = mx <= 3 + 1e-9
print('3. (float) groups without 4-fold axes: T_h (orbits 3-designs, bound 3) and T (2-designs, bound 9)')
for kind, n in [('Th', 2000), ('T', 2000)]:
    G = group(kind); mx = 0; arg = None
    for _ in range(n):
        seeds = rng.normal(size=(rng.integers(1, 3), 3))
        P = np.array([A @ s for s in seeds for A in G])
        t, q = tmin_float(P)
        if t > mx: mx, arg = t, seeds
    bound = 3 if kind == 'Th' else 9
    print(f'   group {kind:2s}: {n} random hulls, max t_min = {mx:.6f}  (bound {bound}: {"ok" if mx <= bound else "EXCEEDED"})')
    checks[f'float {kind} max t_min <= {bound}'] = mx <= bound + 1e-9
print(f'time {time.time()-t0:.1f}s')
for k, v in checks.items():
    if not v: print('  FAIL', k)
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
