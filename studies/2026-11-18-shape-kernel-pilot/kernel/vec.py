"""Vectors of exact numbers (Quad, Fraction, int, or pairs through kernel.pairs): the helpers every copy carries beside its number type.
The container follows the first argument (tuple in, tuple out; list in, list out) unless out= is given, so the tuple-returning
q5.py copies and the list-returning qf.py copies are both reproduced."""
from .exact import Quad, ZERO


def _out(u, out): return out or (list if isinstance(u, list) else tuple)
def v(*x): return tuple(Quad.c(t) for t in x)
def add(u, w, out=None): return _out(u, out)(a + b for a, b in zip(u, w))
def sub(u, w, out=None): return _out(u, out)(a - b for a, b in zip(u, w))
def scale(k, u, out=None): return _out(u, out)(k * a for a in u)
def mulk(u, k, out=None): return _out(u, out)(a * k for a in u)
def dot(u, w):
    s = 0
    for a, b in zip(u, w): s = a * b + s
    return s
def dot3(u, w): return u[0] * w[0] + u[1] * w[1] + u[2] * w[2]
def cross(u, w, out=None):
    return _out(u, out)((u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]))
def det3(a, b, c): return dot3(a, cross(b, c))
def iszero(u): return all(x == 0 for x in u)
def centroid(P):
    n = len(P); return tuple(sum((p[i] for p in P), Quad(0)) / n for i in range(len(P[0])))
def fl(u):
    import numpy as np
    return np.array([float(x) for x in u])
