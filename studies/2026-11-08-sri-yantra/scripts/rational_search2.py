"""Search for RATIONAL Sri Yantras near Huet's classical one.  Theorem Q: for rational (u, v, Q, S)
the yantra lives in Q(sqrt Delta); it is rational exactly when the odd part f(u,v,Q,S) of Delta
(../data/discriminant-data.txt) is a rational square.  For each (u, v, Q) on a grid, f is a
degree-6 polynomial in S; we test S = p/q over many denominators with exact integer arithmetic
(gmpy2.is_square), then re-check every hit with the full exact model (model.solve over Q) and the
configuration test.  usage: rational_search2.py <max den u,v,Q> <max den S> <processes>"""
import sys, time
from fractions import Fraction as Fr
from multiprocessing import Pool
import sympy as sp, gmpy2
from model import solve, order_ok, all_conditions

u_, v_, Q_, S_ = sp.symbols('u v Q S')
ODD = sp.sympify(open('../data/discriminant-data.txt').read().splitlines()[1], locals={'u': u_, 'v': v_, 'Q': Q_, 'S': S_})
COEF = [sp.lambdify((u_, v_, Q_), c, modules=[{}]) for c in sp.Poly(ODD, S_).all_coeffs()]  # high -> low
DEG = len(COEF) - 1
HUET = None


def fr_in(lo, hi, maxden):
    s = set()
    for q in range(1, maxden + 1):
        for p in range(int(lo * q), int(hi * q) + 2):
            f = Fr(p, q)
            if lo <= f <= hi: s.add(f)
    return sorted(s)


def huet():
    import math
    P, Q, R, S = 0.332, 0.537, 0.602, 0.835
    t = solve(P, Q, R, S, math.sqrt(P * (1 - P)), math.sqrt(R * (1 - R)), math.sqrt, 1)
    return [t['b'][i] for i in range(1, 10)]


def exact_rational_yantra(u, v, Q, S):
    P = v * v / (1 + v * v); R = 1 / (1 + u * u); w3 = v / (1 + v * v); w7 = u / (1 + u * u)
    if not (P < Q < R < S < 1): return None
    def sq(z):
        n, d = gmpy2.isqrt(z.numerator), gmpy2.isqrt(z.denominator)
        if z < 0 or n * n != z.numerator or d * d != z.denominator: raise ValueError('not a square')
        return Fr(int(n), int(d))
    for root in (0, 1):
        try:
            t = solve(P, Q, R, S, w3, w7, sq, root)
        except (ValueError, ZeroDivisionError):
            return None
        if order_ok(t, 0) and all(c == 0 for _, c in all_conditions(t)): return t
    return None


def work(args):
    u, v, Q, Sq = args
    c = [Fr(f(u, v, Q)) for f in COEF]
    L = 1
    for x in c: L = L * x.denominator // gmpy2.gcd(L, x.denominator)
    a = [int(x * L) for x in c]
    hits = []
    for (p, q) in Sq:
        N = homog(a, p, q)
        M = N * L
        if M >= 0 and gmpy2.is_square(M):
            S = Fr(p, q); t = exact_rational_yantra(u, v, Q, S)
            if t is not None:
                dev = max(abs(float(t['b'][i]) - HUET[i - 1]) for i in range(1, 10))
                hits.append((dev, str(u), str(v), str(Q), str(S)))
    return hits


def homog(a, p, q):
    """q^DEG * f(p/q) = sum a[k] p^(DEG-k) q^k  (a listed from the highest power of S down)."""
    D = len(a) - 1
    return sum(ak * p ** (D - k) * q ** k for k, ak in enumerate(a))


def init():
    global HUET
    HUET = huet()


if __name__ == '__main__':
    d1, d2, npr = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t0 = time.time(); init()
    U = fr_in(0.76, 0.86, d1); V = fr_in(0.64, 0.76, d1); Qs = fr_in(0.51, 0.56, d1)
    Sq = [(f.numerator, f.denominator) for f in fr_in(0.80, 0.90, d2)]
    jobs = [(u, v, Q, Sq) for u in U for v in V for Q in Qs]
    print(f'grid: {len(U)} u x {len(V)} v x {len(Qs)} Q = {len(jobs)} slices; {len(Sq)} values of S each; '
          f'{len(jobs) * len(Sq)} tests (u,v,Q denominators <= {d1}, S denominators <= {d2}); odd part degree {DEG} in S', flush=True)
    hits = []
    with Pool(npr, initializer=init) as pool:
        for k, h in enumerate(pool.imap_unordered(work, jobs, chunksize=2)):
            hits += h
            if k % 300 == 0: print(f'  [{time.time()-t0:.0f}s] {k}/{len(jobs)} slices, rational yantras so far {len(hits)}', file=sys.stderr, flush=True)
    # self-test: the first rational yantra (found by rational_search.py) must be re-found by this test
    init(); known = work((Fr(19, 24), Fr(2, 3), Fr(8, 15), [(8, 9)]))
    print('self-test, R1 = (19/24, 2/3, 8/15, 8/9) re-found:', bool(known))
    hits.sort()
    print(f'rational Sri Yantras found (all conditions re-checked exactly over Q, configuration admissible): {len(hits)}')
    print('closest to Huet classical depths first (max |db|, u, v, Q, S):')
    for h in hits[:30]: print('  ', f'{h[0]:.5f}', *h[1:])
    print(f'time {time.time()-t0:.0f}s')
    print('FINAL ok' if len(jobs) > 0 and known else 'FINAL FAIL empty grid or self-test failed')
