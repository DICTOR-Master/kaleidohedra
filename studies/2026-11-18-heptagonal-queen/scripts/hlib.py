"""Exact tools for the Heptagonal Queen study (18 Nov 2026).
Numbers in a number field K = Q(t) are integer coefficient vectors on the power basis (1, t, ..., t^(n-1)).
Two fields: GOLD = Q(phi), phi^2 = phi + 1 (control), HEPT = Q(rho), rho = 2cos(pi/7), rho^3 = rho^2 + 2 rho - 1.
sigma = rho^2 - 1 (heptagon long diagonal / side; Steinbach 1997). Vectors are numpy int64 arrays (..., d, n).
All equalities are exact (integer coefficients); floats are used only to order and to evaluate signs of nonzero numbers."""
import numpy as np, itertools, math
from fractions import Fraction as Fr

class Field:
    def __init__(self, name, minpoly_low, root):
        # minpoly t^n = sum_k minpoly_low[k] t^k
        self.name = name; self.n = n = len(minpoly_low); self.root = root
        pw = {}
        for k in range(2*n - 1):
            if k < n: v = [0]*n; v[k] = 1
            else:
                prev = pw[k-1]; v = [0] + prev[:-1]; top = prev[-1]
                v = [v[i] + top*minpoly_low[i] for i in range(n)]
            pw[k] = v
        M = np.zeros((n, n, n), dtype=np.int64)
        for i in range(n):
            for j in range(n): M[i, j] = pw[i+j]
        self.M = M; self.basis_f = np.array([root**k for k in range(n)])
    def el(self, *c): v = np.zeros(self.n, dtype=np.int64); v[:len(c)] = c; return v
    def mul(self, a, b): return np.einsum('...i,...j,ijk->...k', a, b, self.M)
    def f(self, a): return np.asarray(a) @ self.basis_f
    def ip(self, X, Y):
        """inner products: X (..., d, n), Y (..., d, n) -> (..., n), summing over d"""
        return np.einsum('...di,...dj,ijk->...k', X, Y, self.M)

GOLD = Field('Q(phi)', [1, 1], (1 + 5**0.5)/2)
RHO = 2*math.cos(math.pi/7)
HEPT = Field('Q(rho)', [-1, 2, 1], RHO)

def canon_orbit(sorted_vals, K):
    """all distinct permutations of a tuple of field elements (each an int vector), as array (N, d, n)"""
    vals = [tuple(int(x) for x in v) for v in sorted_vals]
    perms = set(itertools.permutations(vals))
    return np.array(sorted(perms), dtype=np.int64)

def centre(X):
    """d*x - sum(x): maps to the sum-zero hyperplane, scaled by d (uniform scale for all orbits of one study)"""
    d = X.shape[-2]
    return d*X - X.sum(axis=-2, keepdims=True)

def keyrows(A): return [a.tobytes() for a in np.ascontiguousarray(A).reshape(A.shape[0], -1)]

def uniq_pts(X):
    seen = {}; out = []
    for x, k in zip(X, keyrows(X)):
        if k not in seen: seen[k] = 1; out.append(x)
    return np.array(out)

def isometry_group(K, X, want_perms=True, cap=10**6):
    """All linear isometries g with g(X) = X, X (N, d, n) exact and spanning its sum-zero space.
    Backtracking on images of a base (exact inner-product constraints); at each leaf, g is determined and is verified by
    inner-product signatures: g(x) = z iff <z, y_j> = <x, b_j> for all j (base spans). Returns (order, perms)."""
    N = X.shape[0]; Xf = np.array([[K.f(c) for c in x] for x in X])
    norms = K.ip(X, X); nk = keyrows(norms)
    lab = {k: i for i, k in enumerate(dict.fromkeys(nk))}; nl = np.array([lab[k] for k in nk])
    # base: greedy rank, choose next by rarest inner-product class with chosen ones
    base = [0]; r = np.linalg.matrix_rank(Xf[[0]])
    rows = {}
    def row(i):
        if i not in rows: rows[i] = K.ip(X, np.broadcast_to(X[i], X.shape))
        return rows[i]
    dim = np.linalg.matrix_rank(Xf)
    while len(base) < dim:
        best = None
        for i in range(N):
            if np.linalg.matrix_rank(Xf[base + [i]]) == len(base) + 1:
                sig = tuple(row(b)[i].tobytes() for b in base)
                cnt = None
                # count how many points share this signature (smaller = fewer branches)
                m = np.ones(N, bool)
                for b in base: m &= np.all(row(b) == row(b)[i], axis=1)
                m &= (nl == nl[i])
                cnt = m.sum()
                if best is None or cnt < best[0]: best = (cnt, i)
        base.append(best[1])
    m = len(base)
    sigB = np.stack([row(b) for b in base], axis=1)   # (N, m, n)
    sigBk = keyrows(sigB)
    found = []
    def rec(level, imgs):
        if level == m:
            Y = np.stack([row(y) for y in imgs], axis=1)
            d = {k: j for j, k in enumerate(keyrows(Y))}
            perm = []
            for k in sigBk:
                j = d.get(k)
                if j is None: return
                perm.append(j)
            found.append(np.array(perm, dtype=np.int32) if want_perms else 1)
            if len(found) > cap: raise RuntimeError('cap')
            return
        b = base[level]
        mask = (nl == nl[b])
        for j, y in enumerate(imgs): mask &= np.all(row(y) == row(base[j])[b], axis=1)
        for z in np.nonzero(mask)[0]:
            rec(level + 1, imgs + [int(z)])
    rec(0, [])
    return len(found), found

def orbits_of(perms, N):
    parent = list(range(N))
    def fd(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for p in perms:
        for i, j in enumerate(p):
            a, b = fd(i), fd(int(j))
            if a != b: parent[a] = b
    return sorted(np.bincount([fd(i) for i in range(N)])[np.bincount([fd(i) for i in range(N)]) > 0].tolist())

class Checks:
    def __init__(self, log=print): self.ok = True; self.n = 0; self.log = log
    def __call__(self, cond, msg):
        self.n += 1; self.ok &= bool(cond); self.log(('PASS ' if cond else 'FAIL ') + msg)
    def final(self):
        self.log(f'FINAL {"ok" if self.ok else "FAIL"} ({self.n} checks)')
