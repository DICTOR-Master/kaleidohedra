# Cube/octahedron changeover, exact. C = Z^3 (weight 0) and V = (1/2,1/2,1/2)+Z^3 (weight w): a power diagram, so the cells fill space
# face to face once each cell is shown to be exactly the cube |p_i| <= 1/2 cut by |x|+|y|+|z| <= S (S = 3/4 - w for C, 3/4 + w for V).
# Checks, in exact arithmetic (Fractions, and the fields Q(sqrt2), Q(sqrt5) with the K class of the octet study):
# (1) at each stop every corner of both cells passes the power test against every centre within distance 2;
# (2) the volumes sum to 1 for every w (a cubic identity: checked at 5 rational points, which proves it for a cubic);
# (3) factor x: the V cell is Koca's T(x) and the C cell T(1/x) when w = (x-1)/(4(x+1)) (checked as a polynomial identity);
# (4) w = 1/4 - 1/sqrt2: every edge of the truncated cube and the octahedron equal.
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'octet'))
from octet_special_exact import K
h = Fr(1, 2); ok = True
def say(c, m):
    global ok; ok &= bool(c); print(('PASS ' if c else 'FAIL ') + m)
def absK(a): return a if K.of(a).sign() >= 0 else -K.of(a)
def corners(S):
    P = {}
    for base in [(h, h, S - 1), (h, S - h, 0), (S, 0, 0), (h, h, h)]:
        for perm in itertools.permutations(base):
            for sg in itertools.product((1, -1), repeat=3):
                q = tuple(K.of(sg[i]) * perm[i] for i in range(3))
                if any(K.of(c).sign() < 0 for c in perm): continue
                if all((K.of(h) - absK(c)).sign() >= 0 for c in q) and (K.of(S) - sum((absK(c) for c in q), K(0))).sign() >= 0:
                    P[tuple(tuple(c.c) for c in q)] = q
    # keep only true corners: points where 3 independent planes meet (drop points inside a face or edge)
    return list(P.values())
def power_ok(cen, wc, S, wv):
    pts = corners(S)
    for p in pts:
        a = [p[i] + cen[i] for i in range(3)]; own = sum((x * x for x in p), K(0)) - wc
        for c in itertools.product(range(-2, 3), repeat=3):
            for off, wq in (((0, 0, 0), K(0)), ((h, h, h), K.of(wv))):
                q = [c[i] + off[i] for i in range(3)]
                if (own - (sum(((a[i] - q[i]) * (a[i] - q[i]) for i in range(3)), K(0)) - wq)).sign() > 0: return False, len(pts)
    return True, len(pts)
def stop(name, n, k, wv):
    K.n, K.k = n, k; wv = K.of(wv)
    r1 = power_ok((0, 0, 0), K(0), K(Fr(3, 4)) - wv, wv); r2 = power_ok((h, h, h), wv, K(Fr(3, 4)) + wv, wv)
    say(r1[0] and r2[0], f'{name}: every corner point of both cells passes the power test against all centres within 2 ({r1[1]}/{r2[1]} points)')
stop('truncated cubes + octahedra, w = -5/8', 2, 2, Fr(-5, 8))
stop('regular truncated cubes + octahedra, w = 1/4 - 1/sqrt2', 2, 2, K([Fr(1, 4), Fr(-1, 2)]))
stop('cuboctahedra + octahedra, w = -1/4', 2, 2, Fr(-1, 4))
K.n, K.k = 2, 5; phi = K([h, h]); stop('factor x = 1/phi (golden split shapes), w = -1/(4 phi^3)', 2, 5, K(-1) / (4 * phi * phi * phi))
stop('Kelvin, w = 0', 2, 2, Fr(0))
# (2) volumes. Cube cut by |x|+|y|+|z| <= S: (4/3)S^3 - 4(S-1/2)^3 for 1/2 <= S <= 1; 1 - (4/3)(3/2-S)^3 for 1 <= S <= 3/2; octahedron (4/3)S^3 for S <= 1/2
lo = lambda S: Fr(4, 3) * S**3 - 4 * (S - h)**3
hi = lambda S: 1 - Fr(4, 3) * (Fr(3, 2) - S)**3
pts1 = [Fr(-3, 4), Fr(-2, 3), Fr(-1, 2), Fr(-2, 5), Fr(-1, 4)]; pts2 = [Fr(-1, 4), Fr(-1, 8), Fr(0), Fr(1, 7), Fr(1, 4)]
say(all(hi(Fr(3, 4) - w) + Fr(4, 3) * (Fr(3, 4) + w)**3 == 1 for w in pts1), 'w in [-3/4, -1/4]: C + V volumes = 1 (cubic identity, 5 points)')
say(all(lo(Fr(3, 4) - w) + lo(Fr(3, 4) + w) == 1 for w in pts2), 'w in [-1/4, 1/4]: C + V volumes = 1 (cubic identity, 5 points)')
say(hi(Fr(3, 4) + Fr(1, 4)) == lo(Fr(1)), 'the two volume formulas agree at the rectified point (S = 1)')
# (3) factor x: T(x) = orbit of s(1+x, x, 0), s = 1/(2(1+x)): squares at 1/2, hexagons on |x|+|y|+|z| = (1+2x)/(2(1+x)).
# V cell S = 3/4 + w; claim w = (x-1)/(4(x+1)). Multiply out: 2(1+2x) = 3(1+x) + (x-1), linear in x, true at 2 points -> identity.
say(all(Fr(1 + 2 * x, 2 * (1 + x)) == Fr(3, 4) + Fr(x - 1, 4 * (x + 1)) and Fr(x + 2, 2 * (x + 1)) == Fr(3, 4) - Fr(x - 1, 4 * (x + 1)) for x in (1, 2, 3)),
    'V cell = T(x), C cell = T(1/x) at w = (x-1)/(4(x+1)): x = 1 Kelvin (w = 0), x -> 0 octahedra + cuboctahedra (w -> -1/4)')
K.n, K.k = 2, 5; xg = K([Fr(-1, 2), h])   # 1/phi
say((xg - 1) / (4 * (xg + 1)) == K(-1) / (4 * phi * phi * phi), 'golden split x = 1/phi sits at w = -1/(4 phi^3)')
# (4) regular truncated cube: cut leg l = 3/2 - S = 3/4 + w; triangle edge l*sqrt2, octagon middle edge 1 - 2l; octahedron edge (3/4+w)*sqrt2
K.n, K.k = 2, 2; wr = K([Fr(1, 4), Fr(-1, 2)]); l = K(Fr(3, 4)) + wr; s2 = K([0, 1])
say(l * s2 == 1 - 2 * l, 'w = 1/4 - 1/sqrt2: triangle edges = octagon edges = %s (= sqrt2 - 1), octahedron edge the same, so faces match' % (l * s2))
# (5) the Delian ratio (C cell twice the V cell) in the factor-x range: V = (4/3)u^3 - 4(u-1/2)^3 = 1/3 with u = 3/4 + w gives
# 16u^3 - 36u^2 + 18u - 1 = 0; no rational root (so irreducible over Q) and discriminant > 0 (three real roots): casus irreducibilis,
# no expression in real radicals. The root in [1/2, 1] is u = 0.63627..., w = -0.11373..., factor x = 0.37466...
cub = lambda u: 16*u**3 - 36*u**2 + 18*u - 1
cands = [Fr(s, b) for b in (1, 2, 4, 8, 16) for s in (1, -1)]
a_, b_, c_, d_ = 16, -36, 18, -1
disc = 18*a_*b_*c_*d_ - 4*b_**3*d_ + b_**2*c_**2 - 4*a_*c_**3 - 27*a_**2*d_**2
say(not any(cub(r) == 0 for r in cands) and disc > 0, 'Delian ratio C = 2V: 16u^3 - 36u^2 + 18u - 1 = 0 is irreducible with three real roots (disc %d): no formula in real radicals' % disc)
lo_, hi_ = Fr(63, 100), Fr(64, 100)
say(cub(lo_) * cub(hi_) < 0 and lo(lo_) < Fr(1, 3) < lo(hi_), 'its root in the factor-x range lies in (0.63, 0.64), where V passes 1/3')
print('ALL PASS' if ok else 'SOME FAIL')
