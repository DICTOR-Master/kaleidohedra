"""Amber-Goldberg study (21 Nov 2026): stand-in for the scutoid stand-in study's resin.py, so that amber.py of the amber-cell sweep runs
UNCHANGED (byte-identical copy in this folder) on Goldberg cores, whose coordinates are not in Q(sqrt5).
Q is replaced by R, a 60-digit real (own mpmath context, unaffected by amber.py's mp.dps = 40) with sign() = 0 when |x| < 1e-40 and
key() = x rounded to 25 digits.  So every "exact" test of amber.py becomes a 60-digit test with tolerance 1e-40 (stated in the README).
dot, cross, vsub, vadd, vsc, det3, act, congruent, LAMBDA: copied unchanged from resin.py.  TH: the 24-element T_h (cyclic permutations x
signs) for achiral cores; for chiral cores (Goldberg GP(m,n) with 0 < n < m) only its 12 rotations T (even number of sign changes), since
the core has no improper symmetry.  ident (angle identification by PSLQ in the basis pi, alpha, beta, gamma) is not used here: returns None."""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
CTX = mp.MPContext(); CTX.dps = 60
TOL = CTX.mpf(10)**-40
SCALE = 10**25

def _c(x):
    if isinstance(x, R): return x.v
    if isinstance(x, Fr): return CTX.mpf(x.numerator)/x.denominator
    return CTX.mpf(x)

class R:
    __slots__ = ("v",)
    def __init__(s, a=0, b=0):
        s.v = _c(a) if not b else _c(a) + _c(b)*CTX.sqrt(5)
    @staticmethod
    def of(v): r = R.__new__(R); r.v = v; return r
    def __add__(s, o): return R.of(s.v + _c(o))
    __radd__ = __add__
    def __neg__(s): return R.of(-s.v)
    def __sub__(s, o): return R.of(s.v - _c(o))
    def __rsub__(s, o): return R.of(_c(o) - s.v)
    def __mul__(s, o): return R.of(s.v*_c(o))
    __rmul__ = __mul__
    def __truediv__(s, o): return R.of(s.v/_c(o))
    def __rtruediv__(s, o): return R.of(_c(o)/s.v)
    def sign(s): return 0 if abs(s.v) < TOL else (1 if s.v > 0 else -1)
    def __float__(s): return float(s.v)
    def mpf(s): return mp.mpf(CTX.nstr(s.v, 55))
    def key(s): return int(CTX.nint(s.v*SCALE))
    def __repr__(s): return CTX.nstr(s.v, 30)
Q = R
PHI = R(Fr(1, 2), Fr(1, 2))
def vadd(u, v): return [u[i] + v[i] for i in range(3)]
def vsub(u, v): return [u[i] - v[i] for i in range(3)]
def vsc(k, u): return [k*u[i] for i in range(3)]
def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def cross(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
def det3(a, b, c): return dot(a, cross(b, c))

def chiral(name):
    if name.startswith(("GP_", "GPc_")):
        m, n = map(int, name.split("_")[1:3]); return 0 < n < m
    return False
TH_FULL = [(c, s) for c in range(3) for s in itertools.product((1, -1), repeat=3)]
_solid = sys.argv[1] if len(sys.argv) > 1 else ""
TH = [g for g in TH_FULL if g[1].count(-1) % 2 == 0] if chiral(_solid) else TH_FULL
def act(g, x):
    c, s = g; y = [x[(i - c) % 3] for i in range(3)]
    return [y[i]*s[i] for i in range(3)]

LAMBDA = mp.pi - mp.acos(mp.sqrt(7 + 3*mp.sqrt(5))/4)
def ident(theta): return None

def congruent(A, B):
    """isometry (proper or improper) mapping vertex set A onto B, float search (copied from resin.py)"""
    if len(A) != len(B): return False
    cA, cB = A.mean(0), B.mean(0); A0, B0 = A - cA, B - cB
    idx = [0]
    for i in range(1, len(A)):
        M = A0[idx + [i]]
        if np.linalg.matrix_rank(M, 1e-8) == len(idx) + 1: idx.append(i)
        if len(idx) == 3: break
    for t in itertools.permutations(range(len(B)), 3):
        if any(abs(np.dot(A0[idx[a]], A0[idx[a]]) - np.dot(B0[t[a]], B0[t[a]])) > 1e-7 for a in range(3)): continue
        R_ = np.linalg.solve(A0[idx], B0[list(t)]).T
        if np.abs(R_.T @ R_ - np.eye(3)).max() > 1e-7: continue
        M = (R_ @ A0.T).T
        if all(np.min(np.linalg.norm(B0 - m, axis=1)) < 1e-7 for m in M): return True
    return False
