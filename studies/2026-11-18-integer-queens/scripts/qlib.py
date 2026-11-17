"""Exact tools for the Integer Queens study (18 Nov 2026).
All points are integer vectors (E8 in sum-zero R^9 scaled by 3; E7 in sum-zero R^8 scaled by 4).
Every equality and rank is decided in integer arithmetic; floats are never used for a claim."""
import numpy as np, itertools, math
from fractions import Fraction as Fr
from sympy.utilities.iterables import multiset_permutations

class Checks:
    def __init__(self, log=print): self.ok = True; self.n = 0; self.log = log
    def __call__(self, cond, msg):
        self.n += 1; self.ok &= bool(cond); self.log(('PASS ' if cond else 'FAIL ') + msg); return bool(cond)
    def final(self):
        self.log(f'FINAL {"ok" if self.ok else "FAIL"} ({self.n} checks)')

def shell_seeds(m, q, N2):
    """all descending integer m-tuples y with sum 0, sum y_i^2 = N2, and all y_i congruent mod q (q=None: no condition)."""
    out = []; B = int(math.isqrt(N2))
    for c in (range(q) if q else [None]):
        vals = [v for v in range(B, -B - 1, -1) if c is None or v % q == c]
        def rec(pre, s, s2, last):
            k = len(pre)
            if k == m:
                if s == 0 and s2 == N2: out.append(tuple(pre))
                return
            for v in vals:
                if v > last: continue
                r = m - k - 1
                if s2 + v*v > N2: continue
                # remaining r entries are <= v: sum of remaining >= -sqrt(r*(N2-s2-v^2)), <= r*v
                rest2 = N2 - s2 - v*v
                if s + v + r*v < 0: break          # even with all remaining = v, sum stays negative
                if r == 0 and s + v != 0: continue
                if r > 0 and (s + v) ** 2 > r * rest2: continue
                rec(pre + [v], s + v, s2 + v*v, v)
        rec([], 0, 0, B + 1)
    return sorted(set(out), reverse=True)

def orbit(seed):
    """all distinct permutations of seed, as an int64 array"""
    return np.array(sorted(multiset_permutations(list(seed)), reverse=True), dtype=np.int64)

def n_perms(seed):
    from collections import Counter
    r = math.factorial(len(seed))
    for c in Counter(seed).values(): r //= math.factorial(c)
    return r

def index_of(X):
    return {x.tobytes(): i for i, x in enumerate(np.ascontiguousarray(X))}

def as_perm(X, Y, idx=None):
    """permutation p with Y[i] = X[p[i]]; None if Y is not a rearrangement of X"""
    idx = idx or index_of(X); p = []
    for y in np.ascontiguousarray(Y):
        j = idx.get(y.tobytes())
        if j is None: return None
        p.append(j)
    return p

def reflect(X, r):
    """exact reflection in the hyperplane perpendicular to integer r; returns None if not integral"""
    num = 2 * (X @ r); den = int(r @ r)
    if np.any(num % den): return None
    return X - np.outer(num // den, r)

# ---------- exact linear algebra over Z / Q ----------
def int_rank(rows):
    """exact rank of an integer matrix (list of int lists), Gaussian elimination over Q"""
    basis = []   # list of (pivot col, row as Fractions, normalised pivot 1)
    for r in rows:
        v = [Fr(int(x)) for x in r]
        for c, b in basis:
            if v[c] != 0:
                f = v[c]; v = [x - f*y for x, y in zip(v, b)]
        c = next((i for i, x in enumerate(v) if x != 0), None)
        if c is not None:
            p = v[c]; basis.append((c, [x / p for x in v]))
    return len(basis)

def independent_rows(rows, want):
    """greedy exact choice of up to `want` independent rows (indices)"""
    chosen = []
    for i, r in enumerate(rows):
        if int_rank([rows[j] for j in chosen] + [r]) == len(chosen) + 1:
            chosen.append(i)
            if len(chosen) == want: break
    return chosen

def nullspace_1(rows, ncol):
    """exact null vector of a (ncol-1) x ncol integer matrix of full rank, as a primitive integer vector, sign-normalised"""
    M = [[Fr(int(x)) for x in r] for r in rows]
    piv_cols = []; rnk = 0
    for c in range(ncol):
        p = next((i for i in range(rnk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rnk], M[p] = M[p], M[rnk]
        pv = M[rnk][c]; M[rnk] = [x / pv for x in M[rnk]]
        for i in range(len(M)):
            if i != rnk and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f*b for a, b in zip(M[i], M[rnk])]
        piv_cols.append(c); rnk += 1
    free = [c for c in range(ncol) if c not in piv_cols]
    if len(free) != 1: return None
    f = free[0]; v = [Fr(0)] * ncol; v[f] = Fr(1)
    for i, c in enumerate(piv_cols): v[c] = -M[i][f]
    L = 1
    for x in v: L = L * x.denominator // math.gcd(L, x.denominator)
    w = [int(x * L) for x in v]; g = 0
    for x in w: g = math.gcd(g, x)
    w = [x // g for x in w]
    s = next(x for x in w if x != 0)
    return tuple(-x for x in w) if s < 0 else tuple(w)

def line_key(v):
    """primitive integer direction up to sign"""
    v = [int(x) for x in v]; g = 0
    for x in v: g = math.gcd(g, x)
    v = [x // g for x in v]; s = next(x for x in v if x != 0)
    return tuple(-x for x in v) if s < 0 else tuple(v)

def plate_normal(V, d):
    """exact normal (in sum-zero R^d) of the linear span of the rows V (ridge corners); V spans d-2 dims... checked by caller"""
    rows = [list(map(int, v)) for v in V]
    idx = independent_rows(rows, d - 2)
    if len(idx) != d - 2: return None
    n = nullspace_1([rows[i] for i in idx] + [[1]*d], d)
    if n is None: return None
    if np.any(np.asarray(V, dtype=np.int64) @ np.array(n, dtype=np.int64)): return None
    return line_key(n)

# ---------- Weyl-group helpers ----------
def simple_roots(R):
    """simple roots of the root system R (integer rows) for a generic functional"""
    rng = np.random.default_rng(7)
    while True:
        c = rng.integers(-10**6, 10**6, R.shape[1])
        v = R @ c
        if np.all(v != 0): break
    P = R[v > 0]; keys = {p.tobytes() for p in P}
    simple = []
    for a in P:
        dec = any((a - b).tobytes() in keys for b in P if not np.array_equal(a, b))
        if not dec: simple.append(a)
    return np.array(simple)

def fundamental_weights(S, d):
    """omega_i in sum-zero R^d with 2<omega_i, a_j>/<a_j,a_j> = delta_ij, in the same (scaled) coordinates; exact.
    Returns exact sympy Rational vectors."""
    import sympy as sp
    M = sp.Matrix([[2*sp.Integer(int(x)) for x in a] for a in S] + [[1]*d])
    out = []
    for i in range(len(S)):
        rhs = sp.Matrix([int(S[i] @ S[i]) if j == i else 0 for j in range(len(S))] + [0])
        out.append(list(M.solve(rhs)))
    return out

def weyl_orbit(v, S):
    """orbit of integer vector v under reflections in simple roots S (exact, BFS); vectors must stay integral"""
    v = np.array(v, dtype=np.int64); seen = {v.tobytes(): v}; front = [v]
    nn = [int(a @ a) for a in S]
    while front:
        F = np.array(front); new = []
        for a, n2 in zip(S, nn):
            num = 2 * (F @ a)
            assert not np.any(num % n2), 'non-integral reflection'
            G = F - np.outer(num // n2, a)
            for g in G:
                k = g.tobytes()
                if k not in seen: seen[k] = g; new.append(g)
        front = new
    return np.array(list(seen.values()))
