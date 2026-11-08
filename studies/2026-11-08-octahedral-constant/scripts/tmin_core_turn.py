# tmin_core_turn.py -- does #81's core turn mu <-> 3/mu on the cube-octahedron sweep P_mu keep t_min (and (R/r)^2)?
# P_mu = [-1,1]^3 cut by |x|+|y|+|z| <= mu, 1 <= mu <= 3. Exact (sympy), using tmin() from tmin_tests.py.
import sys, io, contextlib
import sympy as sp
src = open('tmin_tests.py').read().split("checks = {}")[0]      # reuse the exact routines only
exec(src)
octa = perms_signs((1, 0, 0)); cube = perms_signs((1, 1, 1))
def Pmu(mu):
    if mu == 1: return octa
    if mu == 3: return cube
    return perms_signs((1, mu - 1, 0)) if mu <= 2 else perms_signs((1, 1, mu - 2))
mus = [sp.Rational(k, 16) for k in range(17, 48)] + [sp.sqrt(3), (1 + sp.sqrt(5)) / 2, 1 + sp.sqrt(2) / 2]
same_t, same_q, rows, below3, closed = True, True, [], True, True
def formula(mu):
    # Proposition D (README): closed form on 1 < mu < 3
    if mu <= sp.Rational(3, 2): return mu
    if mu <= 2: return 5 - mu - 3 / mu
    return 3 / mu

for mu in mus:
    nu = sp.nsimplify(sp.radsimp(3 / mu))
    t1, q1, *_ = tmin(Pmu(mu)); t2, q2, *_ = tmin(Pmu(nu))
    et = sp.simplify(t1 - t2) == 0; eq = sp.simplify(q1 - q2) == 0
    same_t &= et; same_q &= eq
    closed &= sp.simplify(t1 - formula(mu)) == 0
    below3 &= bool(sp.nsimplify(3 - t1) >= 0) and bool(sp.nsimplify(3 - t2) >= 0)
    print(f'  mu = {str(mu):18s} 3/mu = {str(nu):22s} t_min: {str(sp.nsimplify(t1)):22s} {str(sp.nsimplify(t2)):22s} {"equal" if et else "DIFFER"}   (R/r)^2 equal: {eq}')
print('t_min invariant under mu <-> 3/mu on all tested mu:', same_t, '| (R/r)^2 invariant:', same_q)
print('closed form mu / 5 - mu - 3/mu / 3/mu matches every exact t_min:', closed)

# General form (proved in README, Proposition 2): for S = {N_k.x <= d_k} with every plane a facet, P(S) = conv(d_k N_k/|N_k|^2)
# has polar S^v = {N_k.x <= |N_k|^2/d_k}; t_min(S) = max_{x in S, y in S^v} x.y, symmetric, so t_min(S) = t_min(S^v)
# whenever every plane of S^v is a facet too. FLOAT test on random three-family octahedral solids (planes on the
# 4-, 2- and 3-fold axes at random depths), skipping draws where a plane is redundant in S or S^v.
import itertools, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
dirs = {4: [v for v in itertools.product([-1,0,1], repeat=3) if sum(map(abs, v)) == 1],
        2: [v for v in itertools.product([-1,0,1], repeat=3) if sum(map(abs, v)) == 2],
        3: [v for v in itertools.product([-1,1], repeat=3)]}
def solid(depth):
    N = np.array([v for k in (4, 2, 3) for v in dirs[k]], float)
    d = np.array([depth[k] for k in (4, 2, 3) for v in dirs[k]], float)
    hs = HalfspaceIntersection(np.hstack([N, -d[:, None]]), np.zeros(3))
    V = hs.intersections; h = ConvexHull(V)
    facet = all(np.sum(np.abs(V @ n - dd) < 1e-9) >= 3 for n, dd in zip(N, d))
    return N, d, V, facet
def tmin_planes(N, d, V):
    feet = d[:, None] * N / np.sum(N * N, axis=1)[:, None]
    G = ConvexHull(feet).equations
    return ((V @ G[:, :3].T) / (-G[:, 3])).max()
rng = np.random.default_rng(5); tested = worst = 0
for _ in range(3000):
    dep = {4: 1.0, 2: rng.uniform(1.0, 2.0), 3: rng.uniform(1.0, 3.0)}
    N, d, V, f1 = solid(dep)
    if not f1: continue
    d2 = np.sum(N * N, axis=1) / d
    _, _, V2, f2 = solid({4: d2[0], 2: d2[6], 3: d2[-1]})
    if not f2: continue
    t1, t2 = tmin_planes(N, d, V), tmin_planes(N, d2, V2)
    tested += 1; worst = max(worst, abs(t1 - t2))
print(f'float: {tested} three-family solids with all planes facets in S and S^v: max |t_min(S) - t_min(S^v)| = {worst:.2e}')
# conditional final line: the theorem's bound t_min <= 3 holds at every tested mu; the invariance is reported above


print('FINAL ok' if below3 and same_t and closed and tested > 100 and worst < 1e-9 else f'FINAL FAIL: below3={below3} tested={tested} worst={worst}')
