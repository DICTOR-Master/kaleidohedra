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

