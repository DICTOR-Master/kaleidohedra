"""q5.py for the replay of 2026-11-13-paradigm-exact: the number class Q5 and the vector helpers now come from the shape kernel
(kernel/exact.py, kernel/vec.py); everything from facets() on is the original module's text, unchanged (polytope tools: stage 2)."""
from fractions import Fraction as F
import itertools
from kernel.exact import Quad
from kernel import vec as _vec


class Q5(Quad):
    """a + b sqrt5 (kernel element; the original's repr and hash)"""
    __slots__ = ()
    D = 5; STYLE = '(a + b*sqrtd)'; HASH_PAIR = True


R5 = Q5(0, 1); PHI = Q5(F(1, 2), F(1, 2))
def v(*x): return tuple(Q5.c(t) for t in x)
def add(p, q): return _vec.add(p, q, out=tuple)
def sub(p, q): return _vec.sub(p, q, out=tuple)
def mul(k, p): return _vec.scale(k, p, out=tuple)
dot = _vec.dot3
def cross(p, q): return _vec.cross(p, q, out=tuple)
det3 = _vec.det3
iszero = _vec.iszero
def parallel_same(p, q): return iszero(cross(p, q)) and dot(p, q) > 0
def centroid(P): n = len(P); return tuple(sum((p[i] for p in P), Q5(0)) / n for i in range(3))

def facets(P):
    """Facets of conv(P) (P small, full-dimensional): list of (normal, offset, vertex index set), normal outward, n.x <= d on P.
    Brute force over triples; exact."""
    out = {}; n = len(P)
    for i, j, k in itertools.combinations(range(n), 3):
        nr = cross(sub(P[j], P[i]), sub(P[k], P[i]))
        if iszero(nr): continue
        d = dot(nr, P[i]); s = [(dot(nr, p) - d).sign() for p in P]
        if all(x <= 0 for x in s): pass
        elif all(x >= 0 for x in s): nr = tuple(-x for x in nr); d = -d
        else: continue
        on = frozenset(m for m in range(n) if dot(nr, P[m]) == d)
        out.setdefault(on, (nr, d))
    return [(nr, d, on) for on, (nr, d) in out.items()]

def order_face(P, idx, nr):
    """corners of a facet in counter-clockwise order seen from outside (exact angular sort by quadrant and cross sign)"""
    idx = list(idx); c = centroid([P[i] for i in idx]); e1 = sub(P[idx[0]], c); e2 = cross(nr, e1)
    def key_cmp(i):
        x, y = dot(sub(P[i], c), e1), dot(sub(P[i], c), e2)
        return (x, y)
    import functools
    def half(xy): x, y = xy; return 0 if (y.sign() > 0 or (y.sign() == 0 and x.sign() > 0)) else 1
    def cmp(i, j):
        a, b = key_cmp(i), key_cmp(j); ha, hb = half(a), half(b)
        if ha != hb: return ha - hb
        cr = a[0] * b[1] - a[1] * b[0]
        return -cr.sign()
    return sorted(idx, key=functools.cmp_to_key(cmp))

def hull_volume(P, F_=None):
    """exact volume of conv(P): fan from the centroid over the ordered facets"""
    F_ = F_ or facets(P); c = centroid(P); vol = Q5(0)
    for nr, d, on in F_:
        f = order_face(P, on, nr)
        for k in range(1, len(f) - 1):
            vol = vol + det3(sub(P[f[0]], c), sub(P[f[k]], c), sub(P[f[k + 1]], c))
    return vol / 6

def edges_of(P, F_):
    E = set()
    for nr, d, on in F_:
        f = order_face(P, on, nr)
        for k in range(len(f)): E.add(frozenset((f[k], f[(k + 1) % len(f)])))
    return E

def separated(P, Q, axes):
    """True if some axis n gives projections of P and Q meeting in at most one value (interiors disjoint)"""
    for n in axes:
        a = [dot(n, p) for p in P]; b = [dot(n, q) for q in Q]
        if max(a) <= min(b) or max(b) <= min(a): return True
    return False

class Body:
    """a convex polytope given by its corners: exact facets, edge directions, bounding box"""
    def __init__(self, P):
        self.P = list(P); self.F = facets(self.P); self.N = [nr for nr, d, on in self.F]
        self.E = [sub(self.P[i], self.P[j]) for i, j in (tuple(e) for e in edges_of(self.P, self.F))]
        self.lo = tuple(min(p[i] for p in self.P) for i in range(3)); self.hi = tuple(max(p[i] for p in self.P) for i in range(3))
    def volume(self): return hull_volume(self.P, self.F)
    def contains(self, x, strict=False):
        return all((dot(nr, x) < d) if strict else (dot(nr, x) <= d) for nr, d, on in self.F)

def disjoint(A, B):
    """exact: interiors of the convex bodies A, B are disjoint (separating axis theorem: facet normals, then edge cross products)"""
    for i in range(3):
        if A.hi[i] <= B.lo[i] or B.hi[i] <= A.lo[i]: return True
    if separated(A.P, B.P, A.N) or separated(A.P, B.P, B.N): return True
    ax = [c for a in A.E for b in B.E for c in [cross(a, b)] if not iszero(c)]
    return separated(A.P, B.P, ax)
