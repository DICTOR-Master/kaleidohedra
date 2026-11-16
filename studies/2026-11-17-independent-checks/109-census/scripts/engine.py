"""Generic group / orbit / set machinery for the independent census (from scratch)."""
import itertools, math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from core import *

RNG = np.random.default_rng(12345)
_W = RNG.integers(1, 2**61, size=4096, dtype=np.int64) | 1

def rowkey(A):
    """Hash rows of an integer or float-rounded array to int64."""
    A = np.asarray(A)
    if A.dtype.kind == 'f':
        A = np.rint(A * 2**24).astype(np.int64)
    A = A.astype(np.int64)
    w = _W[:A.shape[-1]]
    with np.errstate(over='ignore'):
        return (A * w).sum(-1)

class FastMatch:
    def __init__(self, X):
        self.X = np.asarray(X, float)
        k = rowkey(self.X)
        self.o = np.argsort(k, kind='stable'); self.k = k[self.o]
        assert len(np.unique(self.k)) == len(self.k)
    def idx(self, Y):
        Y = np.asarray(Y, float); sh = Y.shape[:-1]
        Y2 = Y.reshape(-1, Y.shape[-1])
        k = rowkey(Y2)
        pos = np.searchsorted(self.k, k); pos[pos >= len(self.k)] = 0
        assert (self.k[pos] == k).all(), 'unmatched image'
        j = self.o[pos]
        assert np.abs(self.X[j] - Y2).max() < 1e-9
        return j.reshape(sh)

def quat_left(l):
    """matrix of x -> l x"""
    E = np.eye(4)
    return np.stack([qmulq(l, E[i]) for i in range(4)], axis=1)
def quat_right(r):
    E = np.eye(4)
    return np.stack([qmulq(E[i], r) for i in range(4)], axis=1)
BAR = np.diag([1.0, -1, -1, -1])

def maps_matrices(Lq, Rq, bars=(0, 1)):
    """matrices of x -> l x rbar (bar=0) and x -> l xbar rbar (bar=1); returns (mats, labels)."""
    Lm = np.array([quat_left(l) for l in Lq]); Rm = np.array([quat_right(qbar(r)) for r in Rq])
    mats, labs = [], []
    for b in bars:
        for i in range(len(Lq)):
            for j in range(len(Rq)):
                M = Lm[i] @ Rm[j]
                if b: M = M @ BAR
                mats.append(M); labs.append((i, j, b))
    return np.array(mats), labs

class PermGroup:
    """A finite group of orthogonal 4x4 matrices, faithful on a reference point set."""
    def __init__(self, mats, ref):
        ref = np.asarray(ref, float)
        m = FastMatch(ref)
        P = m.idx(np.einsum('gij,nj->gni', mats, ref))
        keys = rowkey(P)
        _, first = np.unique(keys, return_index=True)
        first = np.sort(first)
        self.mats = mats[first]; self.P = P[first].astype(np.int32)
        self.N, self.n = self.P.shape
        k = rowkey(self.P); self.ko = np.argsort(k); self.kk = k[self.ko]
        assert len(np.unique(self.kk)) == self.N
        self.Pinv = perm_inverse(self.P)
        self.det = np.rint(np.linalg.det(self.mats)).astype(int)
        self.tr = np.trace(self.mats, axis1=1, axis2=2)
        self.ident = self.id_of(np.arange(self.n)[None])[0]
        negs = np.where(np.all(np.isclose(self.mats, -np.eye(4)), axis=(1, 2)))[0]
        self.neg = int(negs[0]) if len(negs) else None
    def id_of(self, rows):
        k = rowkey(rows); pos = np.searchsorted(self.kk, k); pos[pos >= self.N] = 0
        assert (self.kk[pos] == k).all(), 'not in group'
        return self.ko[pos]
    def try_id(self, rows):
        k = rowkey(rows); pos = np.searchsorted(self.kk, k); pos[pos >= self.N] = 0
        ok = self.kk[pos] == k
        return np.where(ok, self.ko[pos], -1)
    def mats_ids(self, mats, ref_match):
        """ids of given matrices (or -1 if the map is not in the group / not a symmetry)."""
        out = []
        for M in mats:
            Y = ref_match.X @ M.T
            k = rowkey(Y); pos = np.searchsorted(ref_match.k, k); pos[pos >= len(ref_match.k)] = 0
            if not (ref_match.k[pos] == k).all():
                out.append(-1); continue
            p = ref_match.o[pos]
            out.append(int(self.try_id(p[None])[0]))
        return np.array(out)
    def compose(self, a, b):  # (a o b)[x] = a[b[x]]
        return int(self.id_of(self.P[a][self.P[b]][None])[0])
    def inv(self, a):
        return int(self.id_of(self.Pinv[a][None])[0])
    def conj_all(self, g):
        """ids of h g h^-1 for all h."""
        rows = np.take_along_axis(self.P, self.P[g][self.Pinv], axis=1)
        return self.id_of(rows)
    def conj_by(self, c):
        """ids of c x c^-1 for all x."""
        ci = self.Pinv[c]
        rows = self.P[c][self.P[:, ci]]
        return self.id_of(rows)
    def classes(self):
        cls = -np.ones(self.N, int); reps = []
        for g in range(self.N):
            if cls[g] < 0:
                c = self.conj_all(g); cls[c] = len(reps); reps.append(g)
        return reps, cls
    def pair_reps(self, rng=RNG, ngen=10):
        """(g, h) with g a class rep and h a representative of each orbit of C(g) acting on G by
        conjugation (orbits computed from random centraliser elements: never misses a class, may repeat)."""
        reps, cls = self.classes()
        pairs = []
        for g in reps:
            cg = self.conj_all(g); C = np.where(cg == g)[0]
            gens = list(rng.choice(C, size=min(ngen, len(C)), replace=False)) + [g]
            perms = [self.conj_by(int(c)) for c in gens]
            lab = components(self.N, perms)
            _, first = np.unique(lab, return_index=True)
            pairs += [(g, int(h)) for h in first]
        return reps, pairs

def components(n, perms):
    if not perms:
        return np.arange(n, dtype=np.int32)
    rows = np.concatenate([np.arange(n)] * len(perms))
    cols = np.concatenate([np.asarray(p) for p in perms])
    A = coo_matrix((np.ones(len(rows), np.int8), (rows, cols)), shape=(n, n))
    _, lab = connected_components(A, directed=True, connection='weak')
    # relabel by first occurrence
    _, first, inv = np.unique(lab, return_index=True, return_inverse=True)
    order = np.argsort(first); rank = np.empty_like(order); rank[order] = np.arange(len(order))
    return rank[inv].astype(np.int32)

def schreier_even(G, gens):
    """generators of the orientation-preserving part of <gens> (ids)."""
    odd = [s for s in gens if G.det[s] < 0]
    if not odd:
        return list(gens)
    t = odd[0]; ti = G.inv(t)
    out = set()
    for s in gens:
        if G.det[s] > 0:
            out.add(s); out.add(G.compose(G.compose(t, s), ti))
        else:
            out.add(G.compose(s, ti)); out.add(G.compose(t, s))
    out.discard(G.ident)
    return sorted(out)

def variants(G, gens):
    """the group, its rotation part, the group with -I, and that one's rotation part."""
    out = [tuple(sorted(set(gens)))]
    out.append(tuple(schreier_even(G, gens)))
    if G.neg is not None:
        gn = list(gens) + [G.neg]
        out.append(tuple(sorted(set(gn))))
        out.append(tuple(schreier_even(G, gn)))
    return out

def reflection_subgroups(G):
    """all reflection subgroups up to conjugacy, as lists of reflection ids."""
    R = np.where((G.det < 0) & np.isclose(G.tr, 2.0))[0]
    ridx = {int(r): i for i, r in enumerate(R)}
    nR = len(R)
    # conjugation action of every group element on reflections
    CR = np.zeros((G.N, nR), np.int32)
    for i, r in enumerate(R):
        CR[:, i] = [ridx[int(x)] for x in G.conj_all(int(r))]
    # CR[h, i] = index of h r_i h^-1 ; table A[i, j] = r_i r_j r_i
    A = CR[R]  # A[i, j]
    def closure(S):
        S = set(S)
        while True:
            new = {int(A[i, j]) for i in S for j in S} - S
            if not new: return frozenset(S)
            S |= new
    def canon(S):
        m = np.zeros((G.N, nR), bool)
        idx = np.array(sorted(S))
        m[np.repeat(np.arange(G.N), len(idx)), CR[:, idx].ravel()] = True
        pk = np.packbits(m, axis=1)
        o = np.lexsort(pk.T[::-1]); return pk[o[0]].tobytes()
    seen = {}; frontier = [frozenset()]
    seen[canon(frozenset()) if False else b''] = frozenset()
    while frontier:
        nxt = []
        for S in frontier:
            for i in range(nR):
                if i in S: continue
                T = closure(S | {i})
                c = canon(T)
                if c not in seen:
                    seen[c] = T; nxt.append(T)
        frontier = nxt
    out = [sorted(int(R[i]) for i in S) for S in seen.values() if S]
    return out, R

def subgroups_of_unit_group(mul, conj, n, conjugators=None):
    """all subgroups (as sorted index tuples) of a finite unit group given by its multiplication
    table, up to conjugacy within the group. All subgroups of 2I and 2O are 2-generated."""
    def close(gs):
        S = {0} if False else set()
        e = int(np.where((mul == np.arange(n)[None, :]).all(1))[0][0])
        S = {e}; fr = [e]
        while fr:
            nf = []
            for x in fr:
                for g in gs:
                    y = int(mul[x, g])
                    if y not in S:
                        S.add(y); nf.append(y)
            fr = nf
        return frozenset(S)
    subs = set()
    for a in range(n):
        for b in range(a, n):
            subs.add(close([a, b]))
    # up to conjugacy
    reps = {}
    for S in subs:
        key = min(tuple(sorted(int(mul[mul[c, x], conj[c]]) for x in S)) for c in (range(n) if conjugators is None else conjugators))
        reps[key] = key
    return sorted(reps.values(), key=lambda s: (len(s), s))

def automorphisms(Sub, mul, conj):
    """all automorphisms of the subgroup Sub (tuple of indices) as dicts, brute force on 2 gens."""
    S = list(Sub); n = len(S)
    Sset = set(S)
    # find a generating pair (or single)
    def close(gs):
        e = [x for x in S if all(mul[x, y] == y for y in S)][0]
        T = {e}; fr = [e]
        while fr:
            nf = []
            for x in fr:
                for g in gs:
                    y = int(mul[x, g])
                    if y not in T: T.add(y); nf.append(y)
            fr = nf
        return T
    gens = None
    for a in S:
        if len(close([a])) == n: gens = [a]; break
    if gens is None:
        for a, b in itertools.combinations(S, 2):
            if len(close([a, b])) == n: gens = [a, b]; break
    # words for every element in terms of gens (BFS)
    e = [x for x in S if all(mul[x, y] == y for y in S)][0]
    word = {e: []}; fr = [e]
    while fr:
        nf = []
        for x in fr:
            for gi, g in enumerate(gens):
                y = int(mul[x, g])
                if y not in word: word[y] = word[x] + [gi]; nf.append(y)
        fr = nf
    auts = []
    for imgs in itertools.product(S, repeat=len(gens)):
        f = {}
        for x, w in word.items():
            y = e
            for gi in w: y = int(mul[y, imgs[gi]])
            f[x] = y
        if len(set(f.values())) != n: continue
        if all(f[int(mul[x, y])] == mul[f[x], f[y]] for x in S for y in S):
            auts.append(f)
    return auts
