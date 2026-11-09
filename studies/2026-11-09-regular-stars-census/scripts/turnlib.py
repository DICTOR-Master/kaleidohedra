# turnlib.py -- shared code for the turn theorem (study 2026-11-09-turn-theorem).
# Exact arithmetic in Q(sqrt5) (Q5 from q5.py, copied from studies/2026-11-09-icosahedral-line); any dimension d.
#
# Normalisation. A regular polytope P is given by its exact corners V (centre 0). Its facets are N.x <= 1 (exact), so every facet
# has |N| = 1/h. The polar line is
#     S(mu) = {N_i.x <= 1} ∩ {V_j.x <= mu},     h^2 <= mu <= R^2,
# (the corner plane V_j.x = mu passes through the flag point of squared radius mu on the axis of V_j). The antipol (same normals,
# inverted distances d -> |n|^2/d) is S^v(mu) = {N.y <= |N|^2} ∩ {V.y <= R^2/mu} = |N|^2 . S(c/mu), c = h^2 R^2.
#
# Closed form (the theorem): with the squared flag radii h^2 = r_{d-1} < ... < r_0 = R^2 as nodes,
#     t_min(S(mu)) = E min(U_mu, U_{c/mu}) / h^2,
# where U_a is the two-point law on the nodes bracketing a with mean a, the two laws independent.
import itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from q5 import Q5, PHI, IPHI, ZERO, ONE

def Z(x): return x if isinstance(x, Q5) else Q5(x)
def vec(*xs): return tuple(Z(x) for x in xs)
def dotv(u, v):
    s = ZERO
    for a, b in zip(u, v): s = s + a * b
    return s
def flv(v): return np.array([x.f() for x in v])
def scal(k, v): return tuple(k * x for x in v)

def solve(A, b):
    """exact Gauss-Jordan over Q5; A list of rows (d x d), b list; None if singular"""
    n = len(A); M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if not (M[r][col] == ZERO)), None)
        if piv is None: return None
        M[col], M[piv] = M[piv], M[col]
        inv = M[col][col].inv()
        M[col] = [x * inv for x in M[col]]
        for r in range(n):
            if r != col and not (M[r][col] == ZERO):
                f = M[r][col]; M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return tuple(M[i][n] for i in range(n))

def rank(pts):
    a = np.array(pts, dtype=float)
    return 0 if len(a) == 0 else int(np.linalg.matrix_rank(a, tol=1e-9))

def facets(V):
    """exact facet normals N (N.x <= 1) of conv(V), V exact, 0 strictly inside"""
    d = len(V[0]); F = np.array([flv(v) for v in V]); hull = ConvexHull(F)
    out = set()
    for eq in hull.equations:
        on = [i for i in range(len(V)) if abs(F[i] @ eq[:d] + eq[d]) < 1e-9]
        sel = []
        for i in on:   # d linearly independent corners on the facet (the facet plane misses 0)
            if rank([F[j] for j in sel + [i]]) == len(sel) + 1: sel.append(i)
            if len(sel) == d: break
        N = solve([V[i] for i in sel], [ONE] * d)
        assert N is not None
        out.add(N)
    out = sorted(out, key=lambda n: tuple(x.f() for x in n))
    for N in out:   # exact: every corner inside, at least d on the facet
        s = [(dotv(N, v) - ONE).sign() for v in V]
        assert all(x <= 0 for x in s) and sum(1 for x in s if x == 0) >= d
    return out

def flag(V, Nf):
    """exact flag points q_0 (corner), q_1 (edge midpoint), ..., q_{d-1} (facet centre) of a regular polytope, as centroids of a
    chain of faces through one corner; returns (q list, squared radii list)"""
    d = len(V[0]); v0 = V[0]
    on = [frozenset(i for i, v in enumerate(V) if dotv(N, v) == ONE) for N in Nf]
    at0 = [s for s in on if 0 in s]
    face = at0[0]; chain = {d - 1: face}
    for k in range(d - 2, 0, -1):   # face of dimension k containing v0, inside the previous face
        best = None
        for s in at0:
            t = face & s
            pts = [flv(V[i]) - flv(v0) for i in t]
            if rank(pts) == k and (best is None or len(t) > len(best)): best = t
        face = best; chain[k] = face
    chain[0] = frozenset([0])
    q = []
    for k in range(d):
        idx = sorted(chain[k]); m = Q5(Fr(1, len(idx)))
        c = tuple(m * sum((V[i][j] for i in idx), ZERO) for j in range(d))
        q.append(c)
    r2 = [dotv(x, x) for x in q]
    return q, r2

def gram_check(q, r2):
    """q_j.q_k = r2[max(j,k)] for all j, k (the flag Gram identity)"""
    d = len(q)
    return all(dotv(q[j], q[k]) == r2[max(j, k)] for j in range(d) for k in range(d))

def corners(planes, tol=1e-7):
    """exact corners of {N.x <= b}: float half-space intersection for combinatorics, exact solve from d independent active planes,
    exact check against every plane. Returns sorted list of exact corners."""
    d = len(planes[0][0])
    A = np.array([np.r_[flv(N), -b.f()] for N, b in planes])
    hs = HalfspaceIntersection(A, np.zeros(d))
    pts = []
    for p in hs.intersections:
        if not any(np.abs(p - q).max() < 1e-7 for q in pts): pts.append(p)
    Af = A[:, :d]; bf = -A[:, d]
    out = set()
    for p in pts:
        act = [i for i in range(len(planes)) if abs(Af[i] @ p - bf[i]) < tol * max(1, abs(bf[i]))]
        # greedy independent subset
        sel = []
        for i in act:
            if rank([Af[j] for j in sel + [i]]) == len(sel) + 1: sel.append(i)
            if len(sel) == d: break
        assert len(sel) == d, 'no independent active set'
        x = solve([planes[i][0] for i in sel], [planes[i][1] for i in sel])
        # exact sign on every plane within 1e-6 of x (float), float margin > 1e-6 on all others
        sl = Af @ flv(x) - bf
        near = [i for i in range(len(planes)) if abs(sl[i]) < 1e-6]
        assert all(sl[i] < -1e-6 for i in range(len(planes)) if abs(sl[i]) >= 1e-6), 'corner outside a plane (float margin)'
        sg = {i: (dotv(planes[i][0], x) - planes[i][1]).sign() for i in near}
        assert all(v <= 0 for v in sg.values()), 'corner outside a plane (exact)'
        assert frozenset(i for i, v in sg.items() if v == 0) == frozenset(act), 'float/exact active sets differ'
        out.add(x)
    return sorted(out, key=lambda v: tuple(x.f() for x in v))

def line_planes(Nf, V, mu):
    return [(N, ONE) for N in Nf] + [(v, Z(mu)) for v in V]

def antipol_planes(planes):
    return [(N, dotv(N, N) / b) for N, b in planes]

def tmin_brute(X, Y, exact_all=True, tol=1e-9):
    """max x.y over corner sets; exact over all pairs, or exact over the float-selected near-maximal pairs"""
    if exact_all:
        return max(dotv(x, y) for x in X for y in Y)
    Xf = np.array([flv(x) for x in X]); Yf = np.array([flv(y) for y in Y])
    G = Xf @ Yf.T; m = G.max()
    cand = np.argwhere(G > m - tol * max(1, abs(m)))
    return max(dotv(X[i], Y[j]) for i, j in cand)

# ---------- closed form ----------
def bracket(a, nodes):
    """two-point law on the nodes (ascending) bracketing a with mean a: [(value, prob)]"""
    for r, A in zip(nodes, nodes[1:]):
        if r <= a <= A:
            if a == r: return [(r, ONE)]
            if a == A: return [(A, ONE)]
            p = (a - r) / (A - r)
            return [(r, ONE - p), (A, p)]
    raise ValueError('outside the nodes')

def Emin(a, b, nodes):
    s = ZERO
    for u, p in bracket(a, nodes):
        for v, q in bracket(b, nodes):
            s = s + p * q * (u if u <= v else v)
    return s

def tmin_closed(mu, nodes, h2, c):
    return Emin(Z(mu), Z(c) / Z(mu), nodes) / h2

def tmin_closed_f(mu, nodes, h2, c):
    """float version"""
    def br(a):
        for r, A in zip(nodes, nodes[1:]):
            if r - 1e-15 <= a <= A + 1e-15:
                p = (a - r) / (A - r); return [(r, 1 - p), (A, p)]
        raise ValueError
    a, b = mu, c / mu
    return sum(p * q * min(u, v) for u, p in br(a) for v, q in br(b)) / h2

# ---------- polytopes (exact corners) ----------
def perms_signs(base, even=False):
    out = set(); d = len(base)
    for perm in itertools.permutations(range(d)):
        if even:
            inv = sum(1 for i in range(d) for j in range(i + 1, d) if perm[i] > perm[j])
            if inv % 2: continue
        p = [base[i] for i in perm]
        for s in itertools.product((1, -1), repeat=d):
            out.add(tuple(Z(s[i]) * Z(p[i]) for i in range(d)))
    return sorted(out, key=lambda v: tuple(x.f() for x in v))

def tetrahedron(): return [vec(1, 1, 1), vec(1, -1, -1), vec(-1, 1, -1), vec(-1, -1, 1)]
def cube(): return perms_signs((1, 1, 1))
def octahedron(): return perms_signs((1, 0, 0))
def icosahedron(): return perms_signs((ZERO, ONE, PHI), even=True)
def dodecahedron(): return sorted(set(perms_signs((ONE, ONE, ONE)) + perms_signs((ZERO, PHI, IPHI), even=True)),
                                  key=lambda v: tuple(x.f() for x in v))
def simplex4():
    # (2,0,0,0), ..., (0,0,0,2), (t,t,t,t) with t = (1 - sqrt5)/2, shifted to the centroid
    t = ONE - PHI
    P = [vec(2, 0, 0, 0), vec(0, 2, 0, 0), vec(0, 0, 2, 0), vec(0, 0, 0, 2), (t, t, t, t)]
    g = tuple(Q5(Fr(1, 5)) * sum((p[j] for p in P), ZERO) for j in range(4))
    return [tuple(p[j] - g[j] for j in range(4)) for p in P]
def tesseract(): return perms_signs((1, 1, 1, 1))
def cross16(): return perms_signs((1, 0, 0, 0))
def cell24(): return perms_signs((1, 1, 0, 0))
def cell600():
    h = Q5(Fr(1, 2))
    return sorted(set(perms_signs((1, 0, 0, 0)) + perms_signs((h, h, h, h)) +
                      perms_signs((h * PHI, h, h * IPHI, ZERO), even=True)), key=lambda v: tuple(x.f() for x in v))
def cell120():
    S5 = Q5(0, 1); P2 = PHI * PHI; IP2 = IPHI * IPHI
    pts = set(perms_signs((0, 0, 2, 2)) + perms_signs((ONE, ONE, ONE, S5)) + perms_signs((IP2, PHI, PHI, PHI)) +
              perms_signs((IPHI, IPHI, IPHI, P2)) + perms_signs((ZERO, IP2, ONE, P2), even=True) +
              perms_signs((ZERO, IPHI, PHI, S5), even=True) + perms_signs((IPHI, ONE, PHI, Q5(2)), even=True))
    return sorted(pts, key=lambda v: tuple(x.f() for x in v))

def setup(V):
    """facets, flag, constants of a regular polytope with corners V"""
    Nf = facets(V)
    q, r2 = flag(V, Nf)
    n2 = {dotv(N, N) for N in Nf}; R2 = {dotv(v, v) for v in V}
    assert len(n2) == 1 and len(R2) == 1, 'not one face distance and one corner radius'
    n2 = n2.pop(); R2 = R2.pop(); h2 = ONE / n2
    assert r2[0] == R2 and r2[-1] == h2
    c = h2 * R2
    nodes = sorted(set(r2), key=lambda x: x.f())
    return dict(N=Nf, V=V, q=q, r2=r2, h2=h2, R2=R2, c=c, n2=n2, nodes=nodes)
