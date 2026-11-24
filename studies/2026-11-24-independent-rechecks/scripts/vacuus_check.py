# Independent recheck of Theorem A (type A plates, counts vs A402191) and of the uniform type-B count of study
# 2026-11-24-a402191-vacuus.  Own code: vertices listed, facet inequalities tested on the vertices, ridges found as
# pairs of facets whose common vertices have the right rank, each plate solved from the ridge's own vertices
# (null space), then compared with the stated equation and counted.
import sys, itertools, json, math
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from qr import Q


class Basis:
    """Incremental row-echelon basis over a field (entries Fraction or Q)."""
    def __init__(self, zero): self.rows = []; self.piv = []; self.zero = zero
    def add(self, v):
        v = list(v)
        for r, p in zip(self.rows, self.piv):
            f = v[p]
            if not isz(f): v = [a - f * b for a, b in zip(v, r)]
        for p, a in enumerate(v):
            if not isz(a):
                inv = 1 / a if not isinstance(a, Q) else Q(1, 0, a.r) / a
                self.rows.append([x * inv for x in v]); self.piv.append(p); return True
        return False


def isz(a): return a.iszero() if isinstance(a, Q) else a == 0


def null1(rows, n, one, zero):
    """1-dim null space of the given rows (asserted)."""
    B = Basis(zero)
    for r in rows: B.add(r)
    # reduce to RREF
    R = [list(r) for r in B.rows]; P = list(B.piv)
    for i in range(len(R)):
        for j in range(len(R)):
            if j != i and not isz(R[j][P[i]]):
                f = R[j][P[i]]; R[j] = [a - f * b for a, b in zip(R[j], R[i])]
    free = [c for c in range(n) if c not in P]
    assert len(free) == 1, ('null space dim', len(free))
    w = [zero] * n; w[free[0]] = one
    for i, p in enumerate(P): w[p] = -R[i][free[0]]
    return w


def canon(w):
    k = next(i for i, a in enumerate(w) if not isz(a)); f = w[k]
    return tuple(a / f for a in w)


def type_a(n):
    O = F(n + 1, 2)
    verts = list(itertools.permutations(range(1, n + 1)))
    Y = [tuple(F(x) - O for x in v) for v in verts]
    subsets = [S for k in range(1, n) for S in itertools.combinations(range(n), k)]
    tight = {}
    for S in subsets:
        k = len(S); m = k * (k + 1) // 2; bits = 0
        for idx, v in enumerate(verts):
            s = sum(v[i] for i in S)
            assert s >= m                      # valid inequality on every vertex
            if s == m: bits |= 1 << idx
        tight[S] = bits
    def rank(bits, stop):
        B = Basis(F(0)); r = 0; idx = 0
        while bits:
            if bits & 1:
                if B.add(Y[idx]):
                    r += 1
                    if r >= stop: return r
            bits >>= 1; idx += 1
        return r
    for S in subsets: assert rank(tight[S], n) == n - 1, 'not a facet'    # linear rank n-1 of y's = facet
    ridges = []
    for S, T in itertools.combinations(subsets, 2):
        b = tight[S] & tight[T]
        if b and rank(b, n - 1) == n - 2: ridges.append((S, T, b))
    assert len(ridges) == 3 ** n - 3 * 2 ** n + 3
    plates = {}; formula_ok = True; on_two = True
    for S, T, b in ridges:
        # completeness: the ridge's vertices are tight for exactly two of the listed facets
        if sum(1 for U in subsets if tight[U] & b == b) != 2: on_two = False
        rows = []; B = Basis(F(0)); idx = 0; bb = b
        while bb:
            if bb & 1 and B.add(Y[idx]): rows.append(Y[idx])
            bb >>= 1; idx += 1
        w = null1(rows + [tuple(F(1) for _ in range(n))], n, F(1), F(0))
        # stated equation
        A_, C_ = (S, T) if set(S) < set(T) else (T, S)
        assert set(A_) < set(C_), 'ridge facets not nested'
        B1 = set(A_); B2 = set(C_) - B1; B3 = set(range(n)) - set(C_)
        a, bsz, c = len(B1), len(B2), len(B3)
        wf = [F(c * (a + bsz)) if i in B1 else F(a * (bsz + c)) if i in B3 else F(0) for i in range(n)]
        mean = sum(wf) / n; wf = [x - mean for x in wf]
        if canon(wf) != canon(w): formula_ok = False
        plates.setdefault(canon(w), []).append((S, T))
    return dict(n=n, vertices=len(verts), facets=len(subsets), ridges=len(ridges), plates=len(plates),
                formula_matches_every_ridge=formula_ok, every_ridge_on_exactly_two_facets=on_two,
                ridges_per_plate=sorted({len(v) for v in plates.values()}))


def type_b_uniform(n):
    lam = [Q(1, n - k, 2) for k in range(1, n + 1)]          # 1 + (n-k) sqrt2, k = 1..n
    Lam = [Q(0, 0, 2)]
    for x in lam: Lam.append(Lam[-1] + x)
    verts = []
    for p in itertools.permutations(range(n)):
        for s in itertools.product((1, -1), repeat=n):
            verts.append(tuple(s[i] * lam[p[i]] for i in range(n)))
    facets = []
    for k in range(1, n + 1):
        for S in itertools.combinations(range(n), k):
            for e in itertools.product((1, -1), repeat=k): facets.append((S, e))
    assert len(facets) == 3 ** n - 1
    tight = []
    for S, e in facets:
        bits = 0
        for idx, v in enumerate(verts):
            s = sum((ei * v[i] for i, ei in zip(S, e)), Q(0, 0, 2))
            d = (Lam[len(S)] - s).sign(); assert d >= 0
            if d == 0: bits |= 1 << idx
        tight.append(bits)
    def rank(bits, stop):
        B = Basis(Q(0, 0, 2)); r = 0; idx = 0
        while bits:
            if bits & 1 and B.add(verts[idx]):
                r += 1
                if r >= stop: return r
            bits >>= 1; idx += 1
        return r
    for b in tight: assert rank(b, n + 1) == n, 'not a facet'
    ridges = []
    for i, j in itertools.combinations(range(len(facets)), 2):
        b = tight[i] & tight[j]
        if b and rank(b, n) == n - 1: ridges.append((i, j, b))
    plates = {}
    for i, j, b in ridges:
        rows = []; B = Basis(Q(0, 0, 2)); idx = 0; bb = b
        while bb:
            if bb & 1 and B.add(verts[idx]): rows.append(verts[idx])
            bb >>= 1; idx += 1
        w = null1(rows, n, Q(1, 0, 2), Q(0, 0, 2))
        plates.setdefault(canon(w), []).append(b)
    # opposite ridge: vertex set negated
    vidx = {v: k for k, v in enumerate(verts)}
    def neg(b):
        out = 0; idx = 0
        while b:
            if b & 1: out |= 1 << vidx[tuple(-x for x in verts[idx])]
            b >>= 1; idx += 1
        return out
    one_and_opposite = all(len(v) == 2 and neg(v[0]) == v[1] for v in plates.values())
    return dict(n=n, vertices=len(verts), facets=len(facets), ridges=len(ridges),
                ridges_formula=5 ** n - 2 * 3 ** n + 1, plates=len(plates),
                plates_formula=(5 ** n - 2 * 3 ** n + 1) // 2, each_plate_one_ridge_and_opposite=one_and_opposite)


if __name__ == '__main__':
    which = sys.argv[1]; ns = [int(x) for x in sys.argv[2].split(',')]
    for n in ns:
        r = type_a(n) if which == 'A' else type_b_uniform(n)
        print(json.dumps(r), flush=True)
