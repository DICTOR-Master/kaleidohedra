"""The Vacuus of the permutohedron in every dimension (11 Nov 2026). The Vacuus of a solid = the central hyperplanes that carry its ridges
(faces one dimension below the cells: edges of a 3D solid, 2-faces of a 4D one). For the permutohedron of 1..n (dimension n - 1) a ridge
is an ordered split of 1..n into three blocks (B1, B2, B3) of sizes (a, b, c); with the centre it spans one hyperplane, whose normal is
constant on each block (derived by hand, checked here):  c1 = b c (b + c),  c2 = -a c (a + 2b + c),  c3 = a b (a + b).
Prediction: N(n) = sum over a < c of n!/(a! b! c!)  +  sum over a = c of C(n, b)   (a, b, c >= 1, a + b + c = n).
Check by brute force: list every ridge from its corners, solve for its hyperplane exactly, count distinct ones; also the congruence classes
(orbits under coordinate permutations and central inversion). FINAL ok only if the formula and brute force agree for every n."""
import itertools, sys
from fractions import Fraction as F
from math import comb, factorial, gcd, lcm
from collections import Counter

def nullvec(rows):
    M = [list(map(F, r)) for r in rows]; m = len(M[0]); piv = []; r = 0
    for c in range(m):
        pr = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]; M[r] = [x / M[r][c] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0: M[i] = [x - M[i][c] * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(m) if c not in piv]; assert len(free) == 1
    v = [F(0)] * m; v[free[0]] = F(1)
    for i, c in enumerate(piv): v[c] = -M[i][free[0]]
    L = lcm(*[x.denominator for x in v]); w = [int(x * L) for x in v]; g = gcd(*w); w = [x // g for x in w]
    s = next(x for x in w if x); return tuple(x if s > 0 else -x for x in w)

def predicted(n):
    tot, parts = 0, []
    for a in range(1, n):
        for c in range(1, n):
            b = n - a - c
            if b < 1: continue
            if a < c: k = factorial(n) // (factorial(a) * factorial(b) * factorial(c)); tot += k; parts.append(((a, b, c), k))
            elif a == c: k = comb(n, b); tot += k; parts.append(((a, b, c), k))
    return tot, parts

fails = []
for n in range(3, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 8):
    vals = [2 * v - (n + 1) for v in range(1, n + 1)]                       # doubled and centred: integers, sum 0
    hyper = set(); ridges = 0
    for comp in [(a, b, n - a - b) for a in range(1, n) for b in range(1, n) if n - a - b >= 1]:
        a, b, c = comp
        for B1 in itertools.combinations(range(n), a):
            rest = [i for i in range(n) if i not in B1]
            for B2 in itertools.combinations(rest, b):
                B3 = [i for i in rest if i not in B2]; ridges += 1
                # the ridge's corners: blocks take the low, middle, high values, permuted inside each block (enough: a spanning subset)
                lo, mid, hi = vals[:a], vals[a:a + b], vals[a + b:]
                pts = []
                for p1 in list(itertools.permutations(lo))[:a]:
                    for p2 in list(itertools.permutations(mid))[:b]:
                        for p3 in list(itertools.permutations(hi))[:c]:
                            x = [0] * n
                            for blk, pp in ((B1, p1), (B2, p2), (B3, p3)):
                                for i, v in zip(blk, pp): x[i] = v
                            pts.append(x)
                # spanning: all cyclic shifts inside each block (dimension (a-1)+(b-1)+(c-1) = n-3) plus one point
                pts = []
                base = [0] * n
                for blk, pp in ((B1, lo), (B2, mid), (B3, hi)):
                    for i, v in zip(blk, pp): base[i] = v
                pts.append(base)
                for blk in (B1, B2, list(B3)):
                    for t in range(len(blk) - 1):                        # swap neighbours t, t+1 inside the block: a direction
                        y = base[:]; y[blk[t]], y[blk[t + 1]] = y[blk[t + 1]], y[blk[t]]; pts.append(y)
                nv = nullvec([[1] * n] + pts)
                # the closed form
                c1, c2, c3 = b * c * (b + c), -a * c * (a + 2 * b + c), a * b * (a + b)
                w = [0] * n
                for blk, cv in ((B1, c1), (B2, c2), (B3, c3)):
                    for i in blk: w[i] = cv
                g = gcd(*w); w = [x // g for x in w]; s = next(x for x in w if x); w = tuple(x if s > 0 else -x for x in w)
                if w != nv: fails.append(f'n={n} closed form differs at {comp}'); break
                hyper.add(nv)
    pred, parts = predicted(n)
    # corrected count (11 Nov, after the first run: even n FAILED): the two-valued hyperplanes (a = c) are the unordered splits {S, T}
    # of the n positions with S = B1 u B3 of EVEN size >= 2; for even n the split (a, b, a) and (b/2, 2a, b/2) give the same hyperplane.
    # Three-valued (a != c): each hyperplane from exactly one ordered split and its reverse.
    three = sum(k for (a, b, c), k in parts if a != c)
    two = 2 ** (n - 1) - 1 if n % 2 else 2 ** (n - 2) - 1
    two_seen = sum(1 for h in hyper if len(set(h)) == 2); three_seen = sum(1 for h in hyper if len(set(h)) == 3)
    print(f'   two-valued {two_seen} (predicted {two}), three-valued {three_seen} (predicted {three})')
    pred = three + two
    orbits = Counter(tuple(sorted(Counter(h).values())) + (tuple(sorted(set(abs(x) for x in h))),) for h in hyper)
    ok = len(hyper) == pred
    print(f'n={n} (dimension {n - 1}): ridges {ridges}, central hyperplanes {len(hyper)}, formula {pred}  {"PASS" if ok else "FAIL"}; '
          f'by kind ' + ', '.join(f'{k}:{v}' for k, v in parts))
    if not ok: fails.append(f'n={n}')
print('FINAL ok' if not fails else f'FINAL FAIL {fails}')
