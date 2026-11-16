"""The five point sets and their symmetry groups, built from scratch."""
import itertools
import numpy as np
from fractions import Fraction as Fr
from core import *

def build_2I():
    D = icosians_doubled()                       # exact, doubled
    U = np.array([tofloat(v) for v in D]) / 2.0  # float unit quaternions
    mul, conj = unit_group_tables(U)
    return D, U, mul, conj

def galois_alpha_2I(D, U):
    """alpha(x) = c gal(x) c^-1, c = (j+k)/sqrt2: (a,b,c,d) -> (a,-b,d,c) after Galois. Index map."""
    m = Matcher(U)
    img = []
    for v in D:
        g = [qconj(e) for e in v]
        w = (g[0], (-g[1][0], -g[1][1]), g[3], g[2])
        img.append(tofloat(w) / 2)
    return m.idx(np.array(img))

def build_2O_float():
    """2O as float unit quaternions: 2T (24) plus the 24 of the form (+-1,+-1,0,0)/sqrt2 (all perms)."""
    pts = set()
    for i in range(4):
        for s in (1, -1):
            v = [0.0] * 4; v[i] = s; pts.add(tuple(v))
    for signs in itertools.product((0.5, -0.5), repeat=4):
        pts.add(signs)
    r = 2 ** -0.5
    for i, j in itertools.combinations(range(4), 2):
        for si in (r, -r):
            for sj in (r, -r):
                v = [0.0] * 4; v[i] = si; v[j] = sj; pts.add(tuple(v))
    P = np.array(sorted(pts))
    assert len(P) == 48
    return P

def is_2T_float(U):
    """2T inside 2I: the 24 Hurwitz units (+-1,0,0,0) perms and (+-1/2)^4."""
    a = np.abs(U)
    return np.all((np.isclose(a, 0) | np.isclose(a, 1) | np.isclose(a, 0.5)), axis=1)
