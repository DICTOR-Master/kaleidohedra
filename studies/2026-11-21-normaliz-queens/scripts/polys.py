"""Exact vertex sets in Q(phi): 600-cell (radius 2, as in #62) and 120-cell (radius sqrt8)."""
from itertools import permutations, product
from qphi import QP, PHI, IPHI, SQRT5, ONE, ZERO

EVEN = [p for p in permutations(range(4))
        if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]


def _place(vals, p):
    v = [None] * 4
    for k in range(4): v[p[k]] = vals[k]
    return tuple(v)


def _signed(base):
    idx = [i for i, x in enumerate(base) if x != ZERO]
    for sg in product((1, -1), repeat=len(idx)):
        b = list(base)
        for s, i in zip(sg, idx): b[i] = b[i] * s
        yield b


def _all_perms(base):
    out = set()
    for b in _signed(base):
        for p in permutations(range(4)): out.add(_place(b, p))
    return out


def _even_perms(base):
    out = set()
    for b in _signed(base):
        for p in EVEN: out.add(_place(b, p))
    return out


def cell600():
    V = set()
    V |= _all_perms([QP(2), ZERO, ZERO, ZERO])
    V |= _all_perms([ONE, ONE, ONE, ONE])
    V |= _even_perms([PHI, ONE, IPHI, ZERO])
    return sorted(V, key=lambda v: tuple(float(x) for x in v))


def cell120():
    I2 = IPHI * IPHI; P2 = PHI * PHI
    V = set()
    V |= _all_perms([ZERO, ZERO, QP(2), QP(2)])
    V |= _all_perms([ONE, ONE, ONE, SQRT5])
    V |= _all_perms([I2, PHI, PHI, PHI])
    V |= _all_perms([IPHI, IPHI, IPHI, P2])
    V |= _even_perms([ZERO, I2, ONE, P2])
    V |= _even_perms([ZERO, IPHI, PHI, SQRT5])
    V |= _even_perms([IPHI, ONE, PHI, QP(2)])
    return sorted(V, key=lambda v: tuple(float(x) for x in v))
