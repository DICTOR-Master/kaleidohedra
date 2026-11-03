"""Shared exact tools for the study 2026-11-03-dual-pairs-dimensions (DICTO proposed: "can we find out similar interactions
with the other Platonic solids with their duals through the dimensions"). Builds on sixd_lib.py / cubes_lib.py (copied
unchanged from studies/2026-11-03-6d-golden-cubes): exact field K = Q(sqrt2, sqrt5).

Dual pair (P, P*): P = {n_f . x <= 1} with n_f = c_f/|c_f|^2 (c_f face centre), P* = conv(n_f) = {v . x <= 1}.
Section family (6D product P x P* cut by the flat y = x/mu):  S(mu) = P cap mu P* = {n_f.x <= 1, v.x <= mu}.
Hull family (the polars):                                       H(mu) = conv(P cup mu P*) = mu * polar(S(mu)).
Normalised parameter nu = mu / r^2 (r = inradius of P): nu = 1 is the dual end (S = r^2 P*), nu = (R/r)^2 the P end.
Corner cut of P at edge fraction x (x <= 1/2):   mu = R^2 - x e^2/2   (e = edge of P).
Corner cut of P* at edge fraction x:            1/mu = R*^2 - x e*^2/2 (R*, e* of P* = conv(n_f)).
"""
import itertools, json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sixd_lib import *          # noqa  (K, PHI, S2, S5, dot, similar, hull3, vertices_H, cut_solid, x_golden, check, dump ...)
import sixd_lib

DATA = os.path.join(HERE, '..', 'data')
sixd_lib.DATA = DATA


def norm2(v): return dot(v, v)


def kmin(L):
    m = L[0]
    for x in L[1:]:
        if x < m: m = x
    return m


def kmax(L):
    m = L[0]
    for x in L[1:]:
        if x > m: m = x
    return m


def faces_of(V):
    """exact faces (index lists) of conv(V), V in K^3 (corners only)"""
    return hull3(V)


def planes_of(V):
    """exact facet planes (n, d) with n.x <= d (d > 0) of conv(V) (origin inside), plus the corner list"""
    C, F = hull3(V)
    out = []
    for f in F:
        a, b, c = C[f[0]], C[f[1]], C[f[2]]
        u, w = vsub(b, a), vsub(c, a)
        n = (u[1]*w[2] - u[2]*w[1], u[2]*w[0] - u[0]*w[2], u[0]*w[1] - u[1]*w[0])
        k = 2
        while all(x.iszero() for x in n):          # collinear triple: take another corner
            c = C[f[k + 1]]; w = vsub(c, a); k += 1
            n = (u[1]*w[2] - u[2]*w[1], u[2]*w[0] - u[0]*w[2], u[0]*w[1] - u[1]*w[0])
        d = dot(n, a)
        if d < 0: n = tuple(-x for x in n); d = -d
        out.append((n, d))
    return C, F, out


def polar_pts(V):
    """corners of the polar of conv(V) in the unit sphere: n/d for each facet plane n.x <= d"""
    C, F, Pl = planes_of(V)
    return uniq([tuple(x / d for x in n) for n, d in Pl])


class Pair:
    """a regular polyhedron P (corners V) and its polar P*"""
    def __init__(self, name, V):
        self.name = name; self.V = uniq(V)
        C, F = hull3(self.V)
        self.F = F
        cents = [tuple(sum((C[i][k] for i in f), ZERO) / len(f) for k in range(3)) for f in F]
        self.N = [tuple(x / norm2(c) for x in c) for c in cents]                 # P = {n.x <= 1}, P* = conv(N)
        self.R2 = norm2(self.V[0]); self.r2 = norm2(cents[0])
        e2 = kmin([d2(a, b) for a, b in itertools.combinations(self.V, 2)]); self.e2 = e2
        self.rho2 = self.R2 - e2 / 4                                               # midradius^2
        self.Rs2 = norm2(self.N[0]); self.es2 = kmin([d2(a, b) for a, b in itertools.combinations(self.N, 2)])
        assert all(norm2(v) == self.R2 for v in self.V) and all(norm2(c) == self.r2 for c in cents)

    def H_planes(self, mu):
        return [(n, ONE) for n in self.N] + [(v, mu) for v in self.V]

    def S(self, mu):
        """section P cap mu P* (corners, exact)"""
        return fast_vertices_H(self.H_planes(mu))

    def Hull(self, mu):
        """conv(P cup mu P*) (corners, exact)"""
        pts = ([v for v in self.V if self.R2 > mu] + [vscale(mu, n) for n in self.N if mu * self.Rs2 > ONE])
        if not pts: pts = list(self.V)        # mu = R^2 and mu = r^2 cannot both hold
        if mu >= self.R2: pts = [vscale(mu, n) for n in self.N]
        if mu * self.Rs2 <= ONE: pts = list(self.V)
        C, F = hull3(pts)
        return C

    def mu_P(self, x):  return self.R2 - x * self.e2 / 2                  # cut P at fraction x
    def mu_Ps(self, x): return ONE / (self.Rs2 - x * self.es2 / 2)        # cut P* at fraction x
    def nu(self, mu): return mu / self.r2


def tight(A, B):
    """smallest t with conv(A) inside t conv(B) (exact): max over corners a of A and facets (n, d) of B of n.a/d"""
    _, _, Pl = planes_of(B)
    return kmax([dot(n, a) / d for a in A for n, d in Pl])


def touches(A, tB):
    """number of corners of A on the boundary of conv(tB) (exact)"""
    _, _, Pl = planes_of(tB)
    return sum(1 for a in A if any(dot(n, a) == d for n, d in Pl))


def is_phi_power(x):
    """x = phi^k for an integer k? returns k or None (exact)"""
    if not in_q5(x) or x <= 0: return None
    k = 0; y = x
    for _ in range(60):
        if y == ONE: return k
        if y > ONE: y = y / PHI; k += 1
        else: y = y * PHI; k -= 1
        if abs(k) > 40: break
    return None


def q5_norm(x):
    """field norm of x in Q(sqrt5): a^2 - 5c^2 (x = a + c sqrt5)"""
    a, b, c, d = x.v; assert b == 0 and d == 0
    return a * a - 5 * c * c


def kdesc(x):
    """description of a number: exact form, float, phi-power, field norm (if in Q(sqrt5))"""
    out = {'exact': kstr(x), 'float': float(x)}
    if in_q5(x):
        out['norm'] = str(q5_norm(x)); k = is_phi_power(x)
        out['phi_power'] = k
        a, b, c, d = x.v                       # also a + b phi form
        out['a_plus_b_phi'] = f'{a - c} + {2 * c} phi'
    return out


def save(fname, out):
    out['checks'] = sixd_lib.CHECKS; out['all_pass'] = all(c['pass'] for c in sixd_lib.CHECKS)
    with open(os.path.join(DATA, fname), 'w') as f: json.dump(out, f, indent=1, default=str)
    print(f'{sum(c["pass"] for c in sixd_lib.CHECKS)}/{len(sixd_lib.CHECKS)} checks pass -> data/{fname}', flush=True)


def kpow(x, n):
    y = ONE
    for _ in range(n): y = y * x
    return y


def fast_vertices_H(H):
    """vertices of {n.x <= d}, exact: floats find each vertex and its tight planes, three independent tight planes are then
    solved exactly (Cramer in K) and the vertex is checked exactly against every plane (same result as vertices_H, faster)"""
    import numpy as np
    from scipy.spatial import HalfspaceIntersection
    A = np.array([[float(x) for x in n] + [-float(d)] for n, d in H])
    hs = HalfspaceIntersection(A, np.zeros(3))
    V = np.unique(np.round(hs.intersections, 9), axis=0)
    out = {}
    for v in V:
        act = [i for i in range(len(H)) if abs(A[i, :3] @ v + A[i, 3]) < 1e-7]
        x = None
        for a, b, c in itertools.combinations(act, 3):
            x = solve3([H[a][0], H[b][0], H[c][0]], [H[a][1], H[b][1], H[c][1]])
            if x is not None: break
        assert x is not None and all(dot(n, x) <= d for n, d in H), 'exact vertex check failed'
        out.setdefault(key(x), x)
    return list(out.values())
