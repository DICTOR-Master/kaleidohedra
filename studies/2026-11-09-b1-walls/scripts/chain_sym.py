# B1 / #80, #81: DICTO's growth rule T (#38), T(S) = {x : v.x <= v.v for every corner v of S}, run with the depth s as a SYMBOL.
# Edge-cut cube S0(s) = {|x_i| <= 1, |x_i +- x_j| <= 2s} (#80's planes x = +-1 and (+-1, +-1, 0).x <= 2s).
# At a rational sample s0 the face structure of every step is found exactly; each corner is then solved in the field Q(s)
# (Cramer on three of its planes), every other incidence is checked to hold identically, and every non-incident plane gives a
# slack that must keep its sign: its numerator's real roots are the walls (Hopscotch: incidence events of the chain). Between the
# nearest walls on either side of s0 (the hop) every step has the same structure, so the closure identity checked in Q(s)
# (step k = g(s) x step j, corner by corner) holds on the whole hop.
# Usage: python chain_sym.py <s0> <steps> [cube]  -> prints per step corners, kinds, hop; closure; FINAL
import sys, itertools, json, time
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy.spatial import HalfspaceIntersection
s = sp.Symbol('s'); K = sp.QQ.frac_field(s); R = K.to_domain().ring if hasattr(K, 'to_domain') else None
def kel(x): return K.from_sympy(sp.sympify(x))
ZERO, ONE = kel(0), kel(1)
def ev(x, s0):
    n = sp.Poly(x.numer.as_expr(), s).eval(sp.Rational(s0)); d = sp.Poly(x.denom.as_expr(), s).eval(sp.Rational(s0))
    return Fr(int(sp.fraction(n / d)[0]), int(sp.fraction(n / d)[1]))
def evF(x, s0):
    num = x.numer; den = x.denom
    a = num(sp.Rational(s0)) if callable(num) else None
    return Fr(str(sp.Rational(a))) if a is not None else None
def evq(x, s0):
    r = sp.Rational(x.numer.as_expr().subs(s, sp.Rational(s0))) / sp.Rational(x.denom.as_expr().subs(s, sp.Rational(s0)))
    return Fr(int(r.p), int(r.q))
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def det3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

def sym_halfspace(planes, s0):
    """planes: list of (n (3 K-elements), c (K)). Returns corners (K-vectors), corner values at s0, tight sets, slack polys."""
    P0 = [(tuple(evq(x, s0) for x in n), evq(c, s0)) for n, c in planes]
    Nf = np.array([[float(x) for x in n] for n, c in P0]); cf = np.array([float(c) for n, c in P0])
    X = HalfspaceIntersection(np.hstack([Nf, -cf[:, None]]), np.zeros(3)).intersections
    X = X[np.unique(np.round(X, 9), axis=0, return_index=True)[1]]
    C0 = {}
    for x in X:
        tight = [i for i in range(len(P0)) if abs(Nf[i] @ x - cf[i]) < 1e-7 * max(1, abs(cf[i]))]
        tri = next(t for t in itertools.combinations(tight, 3) if det3(*(P0[i][0] for i in t)) != 0)
        A = [P0[i][0] for i in tri]; b = [P0[i][1] for i in tri]; D = det3(*A)
        sol = tuple(det3(*[tuple(b[r] if k == col else A[r][k] for k in range(3)) for r in range(3)]) / D for col in range(3))
        C0[sol] = None
    corners0 = list(C0)
    out, tights, polys = [], [], set()
    for c0 in corners0:
        sl0 = [dot(n, c0) - c for n, c in P0]
        assert all(v <= 0 for v in sl0), 'corner outside'
        T = [i for i, v in enumerate(sl0) if v == 0]
        tri = next(t for t in itertools.combinations(T, 3) if det3(*(P0[i][0] for i in t)) != 0)
        A = [planes[i][0] for i in tri]; b = [planes[i][1] for i in tri]; D = det3(*A)
        polys.add(D.numer.as_expr()); polys.add(D.denom.as_expr())
        c = tuple(det3(*[tuple(b[r] if k == col else A[r][k] for k in range(3)) for r in range(3)]) / D for col in range(3))
        for i in range(len(planes)):
            sl = dot(planes[i][0], c) - planes[i][1]
            if i in T: assert sl == ZERO, 'incidence holds only at the sample (s0 is a wall)'
            else: polys.add(sl.numer.as_expr()); polys.add(sl.denom.as_expr())
        out.append(c); tights.append(frozenset(T))
    kinds = {}
    for i in range(len(planes)):
        k = sum(1 for T in tights if i in T)
        if k >= 3: kinds[k] = kinds.get(k, 0) + 1
    return out, corners0, tights, polys, dict(sorted(kinds.items()))

def factors(polys):
    F = set()
    for p in polys:
        p = sp.Poly(p, s)
        if p.degree() <= 0: continue
        for f, m in sp.factor_list(p)[1]:
            f = sp.Poly(f, s); F.add(f.monic().as_expr())
    return F

def hop(F, s0, lo, hi):
    a, b = lo, hi; s0 = sp.Rational(s0); roots = []
    for f in F:
        for r in sp.Poly(f, s).real_roots():
            if lo < r < hi: roots.append((r, f))
            if lo < r < s0 and (a == lo or r > a): a = r
            if s0 < r < hi and (b == hi or r < b): b = r
    assert all(r != s0 for r, f in roots), 's0 is a wall'
    return a, b

def similar_sym(A, B):
    """B = g * A corner by corner (parallel, same direction, common squared ratio), as identities in Q(s); None if not."""
    if len(A) != len(B): return None
    g = None
    for v in B:
        m = None
        for u in A:
            if all(x == ZERO for x in cross(u, v)) and True:
                m = u; break
        if m is None: return None
        r = dot(v, v) / dot(m, m)
        if dot(v, m) == ZERO: return None
        if g is None: g = r
        elif r != g: return None
    return g

if __name__ == '__main__':
    s0 = Fr(sys.argv[1]); N = int(sys.argv[2]); t0 = time.time()
    lo, hi = sp.Rational(1, 2), sp.Rational(1)
    ax4 = [tuple(kel(x) for x in v) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
    ax2 = []
    for i, j in itertools.combinations(range(3), 2):
        for a, b in itertools.product((1, -1), repeat=2):
            v = [0, 0, 0]; v[i] = a; v[j] = b; ax2.append(tuple(kel(x) for x in v))
    planes = [(n, ONE) for n in ax4] + [(n, kel(2 * s)) for n in ax2]
    hist = []; HOP = (lo, hi); res = dict(s0=str(s0), steps=[])
    V, V0, T, polys, kinds = sym_halfspace(planes, s0)
    F = factors(polys); h = hop(F, s0, lo, hi); HOP = (max(HOP[0], h[0]), min(HOP[1], h[1]))
    print(f'step 0: {len(V)} corners, kinds {kinds}, hop ({h[0]}, {h[1]}) ~ ({float(h[0]):.6f}, {float(h[1]):.6f}), {time.time()-t0:.0f}s', flush=True)
    hist.append((V, kinds)); closed = None
    for k in range(1, N + 1):
        planes = [(v, dot(v, v)) for v in V]
        V, V0, T, polys, kinds = sym_halfspace(planes, s0)
        F = factors(polys); h = hop(F, s0, lo, hi); HOP = (max(HOP[0], h[0]), min(HOP[1], h[1]))
        print(f'step {k}: {len(V)} corners, kinds {kinds}, hop ({h[0]}, {h[1]}) ~ ({float(h[0]):.6f}, {float(h[1]):.6f}), '
              f'{len(F)} wall factors, max degree {max((sp.Poly(f, s).degree() for f in F), default=0)}, {time.time()-t0:.0f}s', flush=True)
        for j, (A, ka) in enumerate(hist):
            if ka == kinds:
                g = similar_sym(A, V)
                if g is not None:
                    closed = dict(enters=j, period=k - j, gain2=str(sp.factor(g.as_expr()))); break
        hist.append((V, kinds))
        if closed: break
    print('chain hop', HOP, f'~ ({float(HOP[0]):.6f}, {float(HOP[1]):.6f})')
    print('closure', closed)
    print('FINAL ok' if closed else 'FINAL FAIL: no closure identity on this hop within the steps run')
