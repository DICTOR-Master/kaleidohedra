"""Search over small-height rational parameters (u, v, Q, S) near Huet's classical yantra.
For each admissible yantra (Theorem Q) the field is Q(sqrt Delta).  We record
 - every case where Delta is a rational SQUARE (a fully rational yantra),
 - every case where Delta = delta * square for a small square-free delta (|delta| <= 30),
 - the admissible case closest to Huet's classical depths, per height bound.
Exact Fractions throughout; the multiprocessing pool only splits the grid."""
import sys, time
from fractions import Fraction as Fr
from math import isqrt, gcd
from multiprocessing import Pool
from model import solve, order_ok

HUET = None  # classical depths b1..b9 computed once (float) from Chiodo's equivalent of Huet's choice
SMALL = [d for d in range(-30, 31) if d not in (0, 1) and all(d % (p * p) for p in range(2, 6))]


def fr_in(lo, hi, maxden):
    s = set()
    for q in range(1, maxden + 1):
        for p in range(int(lo * q), int(hi * q) + 2):
            f = Fr(p, q)
            if lo <= f <= hi: s.add(f)
    return sorted(s)


def is_sq(n):
    return n >= 0 and isqrt(n) ** 2 == n


def classify(D):
    """D rational: return 1 if square, delta if D = delta * square with delta in SMALL, else None."""
    n = D.numerator * D.denominator  # sqrt(n/d) = sqrt(n d)/d
    if is_sq(n): return 1
    for d in SMALL:
        if n % d == 0 and is_sq(n // d): return d
    return None


def work(args):
    u, v, Qs, Ss = args
    P = v * v / (1 + v * v); R = 1 / (1 + u * u); w3 = v / (1 + v * v); w7 = u / (1 + u * u)
    hits, best = [], None
    for Q in Qs:
        for S in Ss:
            if not (P < Q < R < S < 1): continue
            box = {}
            def sq(z):
                box['D'] = z
                import math
                return Fr(math.sqrt(float(z))) if z >= 0 else None
            try:
                tri = None
                for root in (0, 1):
                    t = solve(P, Q, R, S, w3, w7, sq, root)   # float sqrt only to locate the branch
                    if t['disc'] is not None and t['disc'] >= 0 and order_ok(t, 1e-12): tri = t; break
            except (ZeroDivisionError, TypeError):
                continue
            if tri is None: continue
            D = tri['disc']
            c = classify(D)
            if c is not None: hits.append((str(u), str(v), str(Q), str(S), c, str(D)))
            dev = max(abs(float(tri['b'][i]) - HUET[i - 1]) for i in range(1, 10))
            h = max(x.denominator for x in (u, v, Q, S))
            if best is None or dev < best[0]: best = (dev, str(u), str(v), str(Q), str(S), h)
    return hits, best


def huet():
    import math
    P, Q, R, S = 0.332, 0.537, 0.602, 0.835
    t = solve(P, Q, R, S, math.sqrt(P * (1 - P)), math.sqrt(R * (1 - R)), math.sqrt, 1)
    return [t['b'][i] for i in range(1, 10)]


def init():
    global HUET
    HUET = huet()


if __name__ == '__main__':
    maxden = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    t0 = time.time(); init()
    U = fr_in(0.74, 0.88, maxden); V = fr_in(0.64, 0.77, maxden)
    Qs = fr_in(0.50, 0.58, maxden); Ss = fr_in(0.79, 0.90, maxden)
    jobs = [(u, v, Qs, Ss) for u in U for v in V]
    print(f'grid: {len(U)} u x {len(V)} v x {len(Qs)} Q x {len(Ss)} S = {len(U)*len(V)*len(Qs)*len(Ss)} cases (max denominator {maxden})', flush=True)
    hits, bests = [], []
    with Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 22, initializer=init) as pool:
        for k, (h, b) in enumerate(pool.imap_unordered(work, jobs, chunksize=4)):
            hits += h
            if b: bests.append(b)
            if k % 200 == 0: print(f'  [{time.time()-t0:.0f}s] {k}/{len(jobs)} slope pairs, hits so far {len(hits)}', file=sys.stderr, flush=True)
    bests.sort()
    print('closest admissible cases to Huet\'s classical depths (max |db|, u, v, Q, S, max denominator):')
    for b in bests[:8]: print('  ', f'{b[0]:.5f}', *b[1:])
    print(f'square Delta (rational yantra): {sum(1 for h in hits if h[4] == 1)}')
    print(f'Delta = small delta x square: {sum(1 for h in hits if h[4] != 1)}')
    for h in hits[:40]: print('   HIT u,v,Q,S =', h[:4], 'delta =', h[4])
    print(f'time {time.time()-t0:.0f}s')
    print('FINAL ok' if len(bests) > 0 else 'FINAL FAIL search found no admissible case')
