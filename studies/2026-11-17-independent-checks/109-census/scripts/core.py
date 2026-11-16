"""Independent core for the Paper #109 census cross-check (written from scratch).

Exact arithmetic in Q(phi), phi = (1+sqrt5)/2, elements stored as pairs (a, b) = a + b*phi.
Point sets are kept as exact coordinate vectors; group actions are built numerically and
turned into exact permutations by matching every image to a point (tolerance 1e-9, asserted).
Tones: T_k(S) = |S|^-2 sum_{x,y} G_k(<x,y>)/G_k(1); G_k = U_k on S^3, C_k^(3) on S^7.
"""
from fractions import Fraction as Fr
import itertools, math
import numpy as np

PHI = (1 + 5 ** 0.5) / 2

# ---------------- Q(phi) arithmetic: (a, b) = a + b phi ----------------
def qadd(x, y): return (x[0] + y[0], x[1] + y[1])
def qsub(x, y): return (x[0] - y[0], x[1] - y[1])
def qmul(x, y):
    a, b = x; c, d = y
    return (a * c + b * d, a * d + b * c + b * d)
def qconj(x):  # Galois: phi -> 1 - phi
    a, b = x
    return (a + b, -b)
def qnorm(x):
    a, b = x
    return a * a + a * b - b * b
def qdiv(x, y):
    n = qnorm(y)
    assert n != 0
    p = qmul(x, qconj(y))
    return (Fr(p[0]) / n, Fr(p[1]) / n)
def qfloat(x): return float(x[0]) + float(x[1]) * PHI
def qscale(x, r): return (x[0] * r, x[1] * r)
Z0 = (0, 0); Z1 = (1, 0)

def vdot(u, v):
    s = (0, 0)
    for a, b in zip(u, v):
        s = qadd(s, qmul(a, b))
    return s

# ---------------- icosians (doubled: 2x has entries in Z[phi]) ----------------
def even_perms4():
    out = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0:
            out.append(p)
    return out

def icosians_doubled():
    pts = set()
    for i in range(4):
        for s in (2, -2):
            v = [(0, 0)] * 4; v[i] = (s, 0); pts.add(tuple(v))
    for signs in itertools.product((1, -1), repeat=4):
        pts.add(tuple((s, 0) for s in signs))
    # 1/2 (0, 1, phi^-1, phi), even perms, all signs. phi^-1 = phi - 1 = (-1, 1)
    base = [(0, 0), (1, 0), (-1, 1), (0, 1)]
    for p in even_perms4():
        for signs in itertools.product((1, -1), repeat=3):
            v = [None] * 4
            sg = iter(signs)
            for pos, src in zip(p, range(4)):
                e = base[src]
                if src == 0:
                    v[pos] = e
                else:
                    s = next(sg); v[pos] = (s * e[0], s * e[1])
            pts.add(tuple(v))
    pts = sorted(pts)
    assert len(pts) == 120, len(pts)
    return pts

def tofloat(v): return np.array([qfloat(c) for c in v])

def qmulq(p, q):  # Hamilton product, float arrays (..., 4)
    a1, b1, c1, d1 = p[..., 0], p[..., 1], p[..., 2], p[..., 3]
    a2, b2, c2, d2 = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    return np.stack([a1*a2 - b1*b2 - c1*c2 - d1*d2,
                     a1*b2 + b1*a2 + c1*d2 - d1*c2,
                     a1*c2 - b1*d2 + c1*a2 + d1*b2,
                     a1*d2 + b1*c2 - c1*b2 + d1*a2], axis=-1)
def qbar(p):
    r = p.copy(); r[..., 1:] *= -1; return r

class Matcher:
    def __init__(self, F):
        self.F = np.asarray(F, float)
    def idx(self, Y):
        Y = np.asarray(Y, float)
        d = ((Y[:, None, :] - self.F[None, :, :]) ** 2).sum(-1)
        j = d.argmin(1)
        assert d[np.arange(len(Y)), j].max() < 1e-16, d[np.arange(len(Y)), j].max()
        return j

# ---------------- groups as permutations ----------------
def unit_group_tables(U):
    """U: float unit quaternions closed under multiplication. Returns mul, conj tables."""
    m = Matcher(U)
    n = len(U)
    mul = np.zeros((n, n), int)
    for i in range(n):
        mul[i] = m.idx(qmulq(np.repeat(U[i:i+1], n, 0), U))
    conj = m.idx(qbar(U))
    return mul, conj

def quaternion_maps(L, R, act_pts, bar_too=True):
    """All maps x -> l x rbar and x -> l xbar rbar (l in L, r in R, float quats) as
    permutations of act_pts (float, unit or not: maps are isometries). Deduplicated."""
    m = Matcher(act_pts)
    X = np.asarray(act_pts, float)
    perms = {}
    for bar in ((0, 1) if bar_too else (0,)):
        Xs = qbar(X) if bar else X
        for li, l in enumerate(L):
            lx = qmulq(np.repeat(l[None], len(X), 0), Xs)
            for ri, r in enumerate(R):
                y = qmulq(lx, np.repeat(qbar(r)[None], len(X), 0))
                p = tuple(m.idx(y))
                if p not in perms:
                    perms[p] = (li, ri, bar)
    P = np.array(list(perms.keys()), dtype=np.int32)
    return P, list(perms.values())

def perm_inverse(P):
    Q = np.empty_like(P)
    Q[np.arange(P.shape[0])[:, None], P] = np.arange(P.shape[1])[None, :]
    return Q

# ---------------- exact Gram codes and tones ----------------
def cheb_U(c, kmax):
    """U_0..U_kmax at c in Q(phi) (pairs of Fractions)."""
    c = (Fr(c[0]), Fr(c[1]))
    out = [(Fr(1), Fr(0)), qscale(c, 2)]
    for k in range(2, kmax + 1):
        out.append(qsub(qmul(qscale(c, 2), out[-1]), out[-2]))
    return out[:kmax + 1]

def gegen3(t, kmax):
    """C_k^(3)(t), t rational, k = 0..kmax."""
    t = Fr(t); lam = 3
    out = [Fr(1), 2 * lam * t]
    for n in range(2, kmax + 1):
        out.append((2 * t * (n + lam - 1) * out[-1] - (n + 2 * lam - 2) * out[-2]) / n)
    return out[:kmax + 1]

class ToneEngine:
    """Built from an exact Gram matrix given as integer codes into a list of cosine values."""
    def __init__(self, codes, cosvals, kind, kmax=20):
        self.codes = np.asarray(codes)
        self.kmax = kmax
        self.ncos = len(cosvals)
        self.kind = kind
        if kind == 'S3':
            self.G = [cheb_U(c, kmax) for c in cosvals]   # list of [pair]
            self.G1 = [k + 1 for k in range(kmax + 1)]
        elif kind == 'S7':
            self.G = [[(g, Fr(0)) for g in gegen3(c, kmax)] for c in cosvals]
            g1 = gegen3(1, kmax); self.G1 = g1
        else:
            raise ValueError
    def hist(self, idx):
        idx = np.asarray(idx)
        sub = self.codes[np.ix_(idx, idx)].ravel()
        return np.bincount(sub, minlength=self.ncos)
    def tones(self, idx):
        h = self.hist(idx); n = len(idx)
        out = []
        for k in range(1, self.kmax + 1):
            s = (Fr(0), Fr(0))
            for c, cnt in enumerate(h):
                if cnt:
                    s = qadd(s, qscale(self.G[c][k], int(cnt)))
            T = (s[0] / (n * n * self.G1[k]), s[1] / (n * n * self.G1[k]))
            out.append(T)
        return out
    def zeros(self, idx):
        return [k for k, T in enumerate(self.tones(idx), 1) if T == (0, 0)]

def exact_gram_codes(pts_exact, normsq=None):
    """pts_exact: list of Q(phi)^d vectors (int pairs or Fraction pairs). Returns codes, cosvals."""
    n = len(pts_exact)
    if normsq is None:
        normsq = vdot(pts_exact[0], pts_exact[0])
    for p in pts_exact:
        assert vdot(p, p) == normsq
    vals = {}; codes = np.zeros((n, n), np.int32)
    for i in range(n):
        for j in range(i, n):
            c = qdiv(vdot(pts_exact[i], pts_exact[j]), normsq)
            c = (Fr(c[0]), Fr(c[1]))
            k = vals.setdefault(c, len(vals))
            codes[i, j] = codes[j, i] = k
    cosvals = [None] * len(vals)
    for c, k in vals.items():
        cosvals[k] = c
    return codes, cosvals

# ---------------- orbits from generators ----------------
def orbit_labels(n, gens):
    parent = list(range(n))
    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for g in gens:
        for x in range(n):
            a, b = f(x), f(int(g[x]))
            if a != b:
                parent[a] = b
    roots = [f(x) for x in range(n)]
    lab = {}; out = np.empty(n, np.int32)
    for x, r in enumerate(roots):
        out[x] = lab.setdefault(r, len(lab))
    return out

def canon_set(mask_idx, Pinv_or_P, n):
    """Canonical form of a subset under a permutation group given as array P (images p[x]).
    Image of S under p is {p[x]}. Returns bytes of the lexicographically smallest bitmask."""
    P = Pinv_or_P
    m = np.zeros((P.shape[0], n), bool)
    rows = np.repeat(np.arange(P.shape[0]), len(mask_idx))
    m[rows, P[:, mask_idx].ravel()] = True
    packed = np.packbits(m, axis=1)
    # lexicographic min over rows
    order = np.lexsort(packed.T[::-1])
    return packed[order[0]].tobytes()
