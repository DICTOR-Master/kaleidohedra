"""Hidden zeros census, core: exact point sets in Q(sqrt5) (integer pairs a + b*phi), exact inner-product index matrices, exact tones,
ambient permutation groups with multiplication tables, Gram-automorphism symmetry groups, Molien dimensions of invariant harmonics.

Conventions.
* A coordinate is a pair (a, b) of integers meaning a + b*phi, phi = (1 + sqrt5)/2; a point is stored scaled by a fixed integer s.
* Galois conjugation sigma: sqrt5 -> -sqrt5, i.e. phi -> 1 - phi, (a, b) -> (a + b, -b)  ("Double Vision").
* Tones (same normalisation as the law-giving census): T_k(S) = (1/|S|^2) sum_{x,y in S} G_k(<x,y>/r^2) / G_k(1), G_k the Gegenbauer
  polynomial of the sphere (Chebyshev U_k in 4D, C_k^(3) in 8D). T_k(S) >= 0 and T_k(S) = 0 iff S is silent in degree k.
"""
import itertools, numpy as np
from fractions import Fraction as F

PHI = (1 + 5 ** 0.5) / 2
PHIC = 1 - PHI          # Galois conjugate of phi

# ---------------- Q(sqrt5) numbers as Fraction pairs (a + b*phi) ----------------
def qm(x, y):
    a, b = x; c, d = y
    return (a * c + b * d, a * d + b * c + b * d)
def qa(x, y): return (x[0] + y[0], x[1] + y[1])
def qs(x, y): return (x[0] - y[0], x[1] - y[1])
def qsc(c, x): return (c * x[0], c * x[1])
def qsig(x): return (x[0] + x[1], -x[1])
def qf(x): return float(x[0]) + float(x[1]) * PHI
def qstr(x):
    a, b = x
    # a + b*phi = (a + b/2) + (b/2) sqrt5
    r, s = F(a) + F(b, 2), F(b, 2)
    if s == 0: return str(r)
    return f'{r}{"+" if s > 0 else "-"}{abs(s)}*sqrt5'

def gegen_table(cos_vals, kmax, dim):
    """exact G_k(c)/G_k(1) for every c in cos_vals (Fraction pairs); dim 4 -> U_k, dim 8 -> C_k^(3). Returns list over k of lists over c."""
    lam = F(dim - 2, 2)
    out = []
    one = (F(1), F(0))
    Pm = [one for _ in cos_vals]
    P = [qsc(2 * lam, c) for c in cos_vals]
    g1m, g1 = F(1), 2 * lam      # G_k(1)
    out.append([one for _ in cos_vals]); out.append([qsc(1 / g1, p) for p in P])
    for k in range(1, kmax):
        Pn = [qsc(F(1, k + 1), qs(qsc(2 * (k + lam), qm(c, p)), qsc(k + 2 * lam - 1, pm))) for c, p, pm in zip(cos_vals, P, Pm)]
        g1n = (2 * (k + lam) * g1 - (k + 2 * lam - 1) * g1m) / (k + 1)
        out.append([qsc(1 / g1n, p) for p in Pn])
        Pm, P, g1m, g1 = P, Pn, g1, g1n
    return out

# ---------------- point sets ----------------
def even_perms4():
    return [p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]

def cell600():
    """600-cell = the 120 unit icosians, scaled by 2: integer pairs, shape (120, 4, 2)."""
    pts = set()
    for i in range(4):
        for s in (1, -1):
            v = [(0, 0)] * 4; v[i] = (2 * s, 0); pts.add(tuple(v))
    for sg in itertools.product((1, -1), repeat=4):
        pts.add(tuple((s, 0) for s in sg))
    base = [(0, 1), (1, 0), (-1, 1), (0, 0)]       # phi, 1, 1/phi, 0  (times 1/2 before scaling)
    for p in even_perms4():
        for sg in itertools.product((1, -1), repeat=3):
            v = [None] * 4
            for slot in range(4):
                c = base[slot]
                if slot < 3: c = (sg[slot] * c[0], sg[slot] * c[1])
                v[p[slot]] = c
            pts.add(tuple(v))
    P = sorted(pts)
    assert len(P) == 120
    return np.array(P, dtype=np.int64)

def ip_pairs(X, Y):
    """exact inner products of integer-pair point arrays (N,n,2),(M,n,2) -> (a, b) int arrays (N,M): <x,y> = a + b*phi."""
    XA, XB, YA, YB = X[..., 0], X[..., 1], Y[..., 0], Y[..., 1]
    a = XA @ YA.T + XB @ YB.T
    b = XA @ YB.T + XB @ YA.T + XB @ YB.T
    return a, b

def to_float(X):
    return X[..., 0] + X[..., 1] * PHI
def to_float_conj(X):
    return X[..., 0] + X[..., 1] * PHIC

def keyrows(X):
    return [tuple(map(int, r.ravel())) for r in X]

def galois_points(X):
    """sigma on coordinates: (a, b) -> (a + b, -b)"""
    Y = X.copy(); Y[..., 0] = X[..., 0] + X[..., 1]; Y[..., 1] = -X[..., 1]
    return Y

def qmul_pts(L, X):
    """quaternion product l*x for integer-pair quaternions (scaled by 2 each); returns 2*(l x) (exact division by 2 checked)."""
    def zm(x, y):  # elementwise Z[phi] product of arrays (...,2)
        a, b = x[..., 0], x[..., 1]; c, d = y[..., 0], y[..., 1]
        return np.stack([a * c + b * d, a * d + b * c + b * d], -1)
    l0, l1, l2, l3 = [L[..., i, :] for i in range(4)]
    x0, x1, x2, x3 = [X[..., i, :] for i in range(4)]
    r0 = zm(l0, x0) - zm(l1, x1) - zm(l2, x2) - zm(l3, x3)
    r1 = zm(l0, x1) + zm(l1, x0) + zm(l2, x3) - zm(l3, x2)
    r2 = zm(l0, x2) - zm(l1, x3) + zm(l2, x0) + zm(l3, x1)
    r3 = zm(l0, x3) + zm(l1, x2) - zm(l2, x1) + zm(l3, x0)
    R = np.stack([r0, r1, r2, r3], -2)
    assert (R % 2 == 0).all()
    return R // 2

def qconj_pts(X):
    Y = X.copy(); Y[..., 1:, :] *= -1; return Y

# ---------------- index matrices and tones ----------------
class Universe:
    """A finite point set on a sphere with exact inner products in Q(sqrt5) (or an exact rational 'B-form' for E8)."""
    def __init__(self, name, X, dim, Xf, ipfun=None, kmax=20):
        self.name, self.X, self.dim, self.Xf, self.kmax = name, X, dim, Xf, kmax
        self.N = len(X)
        if ipfun is None:
            a, b = ip_pairs(X, X)
        else:
            a, b = ipfun(X, X)
        pairs = np.stack([a, b], -1).reshape(-1, 2)
        uniq, inv = np.unique(pairs, axis=0, return_inverse=True)
        self.IM = inv.reshape(self.N, self.N).astype(np.int32)
        n0 = (int(a[0, 0]), int(b[0, 0]))
        assert (a.diagonal() == n0[0]).all() and (b.diagonal() == n0[1]).all(), 'not on one sphere'
        assert n0[1] == 0, 'squared radius must be rational in the stored scale'
        self.r2 = n0[0]
        self.cos = [(F(int(u), self.r2), F(int(v), self.r2)) for u, v in uniq]
        self.ncos = len(self.cos)
        self.G = gegen_table(self.cos, kmax, dim)
        # rational-coefficient form of the table: Ga[k][c], Gb[k][c] (Fractions)
        self.keyidx = {k: i for i, k in enumerate(keyrows(X))}

    def tones_counts(self, cnt):
        """exact tones from a count vector over cosine classes (sum over ordered pairs), unnormalised by |S|^2"""
        out = []
        for k in range(self.kmax + 1):
            a = sum((int(n) * g[0] for n, g in zip(cnt, self.G[k]) if n), F(0))
            b = sum((int(n) * g[1] for n, g in zip(cnt, self.G[k]) if n), F(0))
            out.append((a, b))
        return out

    def tones(self, S):
        S = np.asarray(sorted(S))
        cnt = np.bincount(self.IM[np.ix_(S, S)].ravel(), minlength=self.ncos)
        t = self.tones_counts(cnt)
        n2 = len(S) ** 2
        return [(a / n2, b / n2) for a, b in t]

    def zeros(self, S):
        return [k for k, (a, b) in enumerate(self.tones(S)) if a == 0 and b == 0 and k >= 1]

# ---------------- ambient permutation group with multiplication table ----------------
class Ambient:
    def __init__(self, perms, basis):
        self.P = np.ascontiguousarray(perms.astype(np.int32))
        self.n = len(perms); self.basis = list(basis)
        N = perms.shape[1]
        self.base = N
        keys = self._keys(self.P[:, self.basis])
        o = np.argsort(keys); self.sk = keys[o]; self.so = o
        assert len(np.unique(keys)) == self.n, 'basis does not separate elements'
        idn = np.arange(N, dtype=np.int32)
        self.e = self.index_of(idn[None, :])[0]
        self.mul = np.empty((self.n, self.n), dtype=np.int16 if self.n < 32768 else np.int32)
        PB = self.P[:, self.basis]
        for i in range(self.n):
            self.mul[i] = self.index_of_basis(self.P[i][PB])      # perm_i o perm_j  (j applied first)
        self.inv = np.argmax(self.mul == self.e, axis=1).astype(np.int32)
        assert (self.mul[np.arange(self.n), self.inv] == self.e).all()

    def _keys(self, B):
        k = np.zeros(len(B), dtype=np.int64)
        for c in range(B.shape[1]): k = k * self.base + B[:, c]
        return k
    def index_of_basis(self, B):
        k = self._keys(B); pos = np.searchsorted(self.sk, k)
        assert (self.sk[np.minimum(pos, self.n - 1)] == k).all(), 'element not in ambient'
        return self.so[pos]
    def index_of(self, perms):
        return self.index_of_basis(perms[:, self.basis])

    def closure(self, gens):
        """indices of the subgroup generated by gens (indices)"""
        gens = np.unique(np.asarray(gens, dtype=np.int64))
        inS = np.zeros(self.n, bool); inS[self.e] = True
        cur = np.array([self.e]); allS = [cur]
        while len(cur):
            new = np.unique(self.mul[np.ix_(cur, gens)].ravel())
            new = new[~inS[new]]
            inS[new] = True; cur = new; allS.append(new)
        return np.nonzero(inS)[0]

    def classes(self):
        if hasattr(self, '_cls'): return self._cls
        cls = -np.ones(self.n, dtype=np.int32); reps = []
        for i in range(self.n):
            if cls[i] >= 0: continue
            conj = self.mul[self.mul[:, i], self.inv]        # c i c^-1 over all c
            cls[np.unique(conj)] = len(reps); reps.append(i)
        self._cls, self._reps = cls, reps
        return cls

    def conj_set(self, S, c):
        return self.mul[self.mul[c, S], self.inv[c]]

    def is_conjugate(self, S1, gens1, S2):
        """is the subgroup S1 (generated by gens1) conjugate to S2 (index arrays)?"""
        if len(S1) != len(S2): return False
        in2 = np.zeros(self.n, bool); in2[S2] = True
        ok = np.ones(self.n, bool)
        for g in gens1:
            im = self.mul[self.mul[:, g], self.inv]      # c g c^-1 for all c
            ok &= in2[im]
            if not ok.any(): return False
        return bool(ok.any())

# ---------------- float matrices and Molien ----------------
def span_basis(Xf, idx=None, tol=1e-9):
    idx = range(len(Xf)) if idx is None else idx
    B = []; M = np.zeros((0, Xf.shape[1]))
    for i in idx:
        M2 = np.vstack([M, Xf[i]])
        if np.linalg.matrix_rank(M2, tol) > len(B): B.append(i); M = M2
        if len(B) == Xf.shape[1]: break
    return B

def float_mats(Xf, perms, basis):
    """matrices (in an orthonormal basis of span{X[basis]}) of the linear maps sending X[basis] -> X[perm[basis]]."""
    Q, _ = np.linalg.qr(Xf[basis].T)            # n x r orthonormal
    Z = Xf @ Q                                   # coordinates in the span
    Zb_inv = np.linalg.inv(Z[basis].T)
    # L = Z[p(b)]^T @ inv(Z[b]^T)
    L = np.transpose(Z[perms[:, basis]], (0, 2, 1)) @ Zb_inv
    return L

def molien_series(mats, kmax):
    """average over the group of the series of 1/det(I - t g), up to t^kmax (float)."""
    ev = np.linalg.eigvals(mats)                         # (g, r)
    g, r = ev.shape
    S = np.zeros((g, kmax + 1), complex); S[:, 0] = 1
    pw = ev[:, :, None] ** np.arange(kmax + 1)[None, None, :]
    for j in range(r):
        T = np.zeros_like(S)
        for k in range(kmax + 1):
            T[:, k] = (S[:, :k + 1] * pw[:, j, k::-1]).sum(1)
        S = T
    m = S.mean(0)
    assert np.abs(m.imag).max() < 1e-6
    return m.real

def harm_dims(mats, kmax, full_dim):
    """dimension of G-invariant harmonics of degree k <= kmax.
    If the matrices act on the whole space (r = full_dim): coefficients of Molien*(1 - t^2).
    If they act on a proper subspace W (r < full_dim) and the group is Sym_W x O(W-perp): coefficients of the Molien series on W."""
    r = mats.shape[1]
    m = molien_series(mats, kmax)
    if r == full_dim:
        h = m.copy(); h[2:] -= m[:-2]
    else:
        h = m
    hr = np.rint(h)
    assert np.abs(h - hr).max() < 1e-5, f'Molien not integral: {np.abs(h - hr).max()}'
    return [int(x) for x in hr]

def harm_char_table(mats, kmax, full_dim):
    """per-element harmonic characters chi_k(g) (float), so that dim Harm_k^H = mean over H; full-space action only."""
    ev = np.linalg.eigvals(mats); g, r = ev.shape
    S = np.zeros((g, kmax + 1), complex); S[:, 0] = 1
    pw = ev[:, :, None] ** np.arange(kmax + 1)[None, None, :]
    for j in range(r):
        T = np.zeros_like(S)
        for k in range(kmax + 1): T[:, k] = (S[:, :k + 1] * pw[:, j, k::-1]).sum(1)
        S = T
    H = S.real.copy(); H[:, 2:] -= S.real[:, :-2]
    return H

# ---------------- symmetry group of a subset (Gram automorphisms) ----------------
def sym_perms(IM, Xf, cap=400000):
    """All permutations of the points that extend to orthogonal maps of their span: exact (IM entries are exact value classes).
    Returns (perms array (|Sym|, n) local indices, basis list) or (None, basis) if more than cap."""
    n = len(IM)
    basis = span_basis(Xf)
    r = len(basis)
    nv = int(IM.max()) + 1
    def enc(M):
        k = np.zeros(M.shape[0], dtype=np.int64)
        for c in range(M.shape[1]): k = k * nv + M[:, c]
        return k
    ref = enc(IM[:, basis]); refsort = np.sort(ref)
    if len(np.unique(ref)) != n: raise RuntimeError('basis signatures not unique')
    out = []
    diag = IM[0, 0]
    def rec(ys):
        i = len(ys)
        if len(out) > cap: return
        if i == r:
            sig = enc(IM[:, ys])                          # signature of every point w.r.t. the image basis
            o = np.argsort(sig); ss = sig[o]
            pos = np.searchsorted(ss, ref)
            if (pos < n).all() and (ss[np.minimum(pos, n - 1)] == ref).all():
                out.append(o[pos])                        # point x -> point with the same signature w.r.t. images
            return
        need = IM[basis[i], basis[:i]]
        cand = np.nonzero(IM.diagonal() == diag)[0]
        for j, y in enumerate(ys):
            cand = cand[IM[cand, y] == need[j]]
        for c in cand:
            if c in ys: continue
            rec(ys + [int(c)])
    rec([])
    if len(out) > cap: return None, basis
    return np.array(out, dtype=np.int32), basis

def orbits_from_gens(gen_perms, N):
    parent = np.arange(N)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for p in gen_perms:
        for i in range(N):
            a, b = find(i), find(int(p[i]))
            if a != b: parent[a] = b
    roots = np.array([find(i) for i in range(N)])
    return [np.nonzero(roots == r)[0] for r in np.unique(roots)]
