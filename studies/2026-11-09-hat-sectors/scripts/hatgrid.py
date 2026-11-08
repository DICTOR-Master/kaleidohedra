# Kite grid (deltoidal trihexagonal tiling) and the hat polykite, exact integer arithmetic.
# Points are integer pairs (a, b) = a*e1 + b*e2 with e1 = (1, 0), e2 = (1/2, sqrt3/2).
# Hexagon centres: lattice spanned by U = (2, 2) and rot(U) = (-2, 4); hexagon circumradius 2,
# apothem sqrt3, so kite edges are sqrt3 (centre-midpoint) and 1 (midpoint-vertex).
# Hexagon vertex directions from a centre: rot^k (2, 0); their class (k mod 2) is the
# bipartite colour of the honeycomb vertex (globally consistent, checked in selftest).
# Hat outline: C. S. Kaplan's hatviz coordinates (hexPt integer points), Smith et al. 2023.
from fractions import Fraction as F
from math import sqrt

def rot(p, k=1):
    a, b = p
    for _ in range(k % 6):
        a, b = -b, a + b
    return (a, b)

def refl(p):            # reflection in the e1 line (a centre-vertex line through the origin centre)
    a, b = p
    return (a + b, -b)

# 12 linear parts: ('r', j) = rot^j ; ('s', j) = refl o rot^j  (reflection line at angle -30 j degrees;
# j even: centre-vertex (CV) line, j odd: centre-midpoint (CM) line)
LIN = [('r', j) for j in range(6)] + [('s', j) for j in range(6)]

def apply(g, p):
    kind, j = g
    q = rot(p, j)
    return refl(q) if kind == 's' else q

U = (2, 2)
UR = rot(U)

def centre(i, j):
    return (i * U[0] + j * UR[0], i * U[1] + j * UR[1])

def add(p, q):
    return (p[0] + q[0], p[1] + q[1])

def kite(c, k):
    """kite k of hexagon at centre c: (C, M_prev, V_k, M_next), V_k = c + rot^k(2,0)"""
    return (c, add(c, rot((1, 1), k - 1)), add(c, rot((2, 0), k)), add(c, rot((1, 1), k)))

def kite_key(kt):
    return tuple(sorted(kt))

HAT = [(0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1), (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2)]

def area2(poly):        # twice the signed area, in lattice units (true area = value * sqrt3/4)
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s

def inside(pt, poly):   # exact even-odd test, pt never on boundary here (kite interior points)
    x, y = pt; c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = F(x1) + F(y - y1) * F(x2 - x1) / F(y2 - y1)
            if x < xi:
                c = not c
    return c

def hexdist(i, j):
    return (abs(i) + abs(j) + abs(i + j)) // 2

def kites_of_hat():
    """find an aligned position of the hat; return (offset t, list of (centre, k)) with hat+t = union of 8 kites"""
    A_hat = abs(area2(HAT))
    for i in range(-3, 4):
        for j in range(-3, 4):
            pass
    # offsets: integer points mod the centre lattice (index 12) -- try a window
    for ta in range(-4, 5):
        for tb in range(-4, 5):
            poly = [add(p, (ta, tb)) for p in HAT]
            got = []
            for ci in range(-4, 5):
                for cj in range(-4, 5):
                    c = centre(ci, cj)
                    for k in range(6):
                        kt = kite(c, k)
                        m = (F(sum(p[0] for p in kt), 4), F(sum(p[1] for p in kt), 4))
                        if inside(m, poly):
                            got.append((c, k))
            if len(got) == 8 and sum(abs(area2(kite(c, k))) for c, k in got) == A_hat:
                return (ta, tb), got
    raise RuntimeError('hat not aligned')

def kite_class(c, k):
    return k % 2

def selftest():
    # vertex class consistency: each honeycomb vertex gets one class from all 3 hexagons
    cls = {}
    for ci in range(-3, 4):
        for cj in range(-3, 4):
            c = centre(ci, cj)
            for k in range(6):
                v = kite(c, k)[2]
                cls.setdefault(v, set()).add(k % 2)
    assert all(len(s) == 1 for s in cls.values()), 'vertex class inconsistent'
    # group: rot and refl preserve the kite set around the origin
    ks = {kite_key(kite(centre(i, j), k)) for i in range(-3, 4) for j in range(-3, 4) for k in range(6)}
    for g in LIN:
        for k in range(6):
            kk = kite_key(tuple(apply(g, p) for p in kite((0, 0), k)))
            assert kk in ks
    return True

if __name__ == '__main__':
    selftest()
    t, ks = kites_of_hat()
    from collections import Counter
    print('hat offset', t, 'kites', ks)
    print('hat area2', abs(area2(HAT)), 'kite area2', abs(area2(kite((0, 0), 0))))
    print('kite directions', Counter(k for c, k in ks), 'classes', Counter(k % 2 for c, k in ks))
    print('hexagons used', len({c for c, k in ks}))
