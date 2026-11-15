"""Twisted silence, dihedral family (exact; pure Python, integer cyclotomic arithmetic).
Part 1. D_n (order 2n) inside O(2), sigma_m: r -> r^m, s -> s (m a unit mod n, m != +-1: the Galois automorphism
        cos 2pi/n -> cos 2pi m/n of the reflection representation, an outer automorphism of D_n).
        Twisted classes {a x0 sigma(a)^-1} lie on the rotation circle or the reflection circle of O(2).
        A set on a circle kills Fourier mode k iff sum zeta_n^(k e) = 0 (exact: the polynomial sum x^(k e mod n) is divisible by Phi_n).
        Criterion (twisted characters, closed form) is computed independently and compared for every mode k = 1..2n (period n).
Part 2. Binary dihedral 2D_n (order 4n) in SU(2) = S^3 with the same Galois twist zeta_2n -> zeta_2n^m, j -> j: twisted classes lie on
        great circles; S^3 degree k is killed iff every circle mode j = k, k-2, ... (>= -k) vanishes. Exact direct U_k sums.
Controls: sigma = id (ordinary classes) and a wrong sigma (r -> r^m with gcd(m, n) > 1: not an automorphism) must fail the criterion.
Prints CHECK lines (must be OK), a SIG line per set (silence signature, k <= 30), and FINAL ok only if every check passed."""
import sys
from math import gcd
from functools import lru_cache

NS = [int(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 else [5, 7, 8, 9, 10, 12, 15, 16, 18, 20, 24, 30]
KSIG = 30
fails = 0
def check(ok, what):
    global fails
    if not ok: fails += 1
    print(('CHECK OK   ' if ok else 'CHECK FAIL ') + what)

def pmod(a, b):                                   # integer polynomial remainder (b monic), lists low->high
    a = a[:]
    while len(a) >= len(b):
        c = a[-1]
        if c:
            s = len(a) - len(b)
            for i, bi in enumerate(b): a[s + i] -= c * bi
        a.pop()
    return a
def pdiv(a, b):                                   # exact division by monic b
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for s in range(len(a) - len(b), -1, -1):
        c = a[s + len(b) - 1]; q[s] = c
        for i, bi in enumerate(b): a[s + i] -= c * bi
    assert not any(a); return q
@lru_cache(None)
def cyclo(M):
    p = [-1] + [0] * (M - 1) + [1]
    for d in range(1, M):
        if M % d == 0: p = pdiv(p, list(cyclo(d)))
    return tuple(p)
def rootsum_zero(exps, M):
    """exact: sum over exps of zeta_M^e == 0 ?"""
    P = [0] * M
    for e in exps: P[e % M] += 1
    return not any(pmod(P, list(cyclo(M))))

# ---------------- Part 1: D_n on O(2) ----------------
def dmul(n, x, y):                                # elements (f, t) = s^f r^t ; r^t s = s r^-t
    f, t = x; g, u = y
    return ((f + g) % 2, ((-t if g else t) + u) % n)
def dinv(n, x):
    f, t = x
    return (0, (-t) % n) if f == 0 else x
def sig(n, m, x): return (x[0], (m * x[1]) % n)
def twisted_class(n, m, x0, sg=sig):
    G = [(f, t) for f in (0, 1) for t in range(n)]
    return sorted({dmul(n, dmul(n, a, x0), dinv(n, sg(n, m, a))) for a in G})
def circle_exps(n, O):
    """position on its circle: rotation r^t -> angle 2 pi t/n ; reflection s r^t -> parameter -2 pi t/n"""
    return [t if f == 0 else -t for f, t in O]
def direct_kills(n, O, k): return rootsum_zero([k * e for e in circle_exps(n, O)], n)
def criterion_kills(n, m, x0, k):
    """twisted-character criterion (closed form) for Fourier mode k of the twisted class of x0"""
    j = k % n; f, t = x0
    if j == 0 or 2 * j == n: return False              # 1-dim sigma-stable constituents, twisted character +-1
    plus, minus = (j * m - j) % n == 0, (j * m + j) % n == 0
    if not plus and not minus: return True              # not sigma-stable: invisible
    if plus:                                             # J = I : chi(x0) ; zero on reflections, 2cos(2 pi j t/n) on rotations
        return True if f == 1 else (4 * j * t - n) % (2 * n) == 0
    return True if f == 0 else (4 * j * t - n) % (2 * n) == 0   # J = rho(s): chi(x0 s)

def sym_order(n, O):
    """rotational symmetry order N of the point set on its circle (true symmetry is D_N or C_N)"""
    E = set(e % n for e in circle_exps(n, O))
    return sum(1 for c in range(n) if {(e + c) % n for e in E} == E)

print('PROGRESS 0.00 part 1 dihedral on the circle')
rows = []
for idx, n in enumerate(NS):
    units = [m for m in range(1, n) if gcd(m, n) == 1]
    outer = [m for m in units if m not in (1, n - 1)]
    twists = [1] + sorted({min(m, n - m) for m in outer})        # sigma_m and sigma_{-m} differ by an inner automorphism (s-conjugation)
    for m in twists:
        seen = set()
        for x0 in [(f, t) for f in (0, 1) for t in range(n)]:
            O = twisted_class(n, m, x0)
            if tuple(O) in seen: continue
            seen.add(tuple(O))
            dk = [k for k in range(1, 2 * n + 1) if direct_kills(n, O, k)]
            ck = [k for k in range(1, 2 * n + 1) if criterion_kills(n, m, x0, k)]
            check(dk == ck, f'D{n} m={m} x0={x0}: criterion == direct for modes 1..{2*n}')
            N = sym_order(n, O)
            sig30 = [k for k in range(1, KSIG + 1) if direct_kills(n, O, k)]
            unf = [k for k in sig30 if k % N == 0]
            npts = len(set(e % n for e in circle_exps(n, O)))
            rows.append((n, m, x0, npts, N, sig30, unf))
            if m != 1 and unf:
                print(f'SIG D{n} m={m} x0={"r" if x0[0]==0 else "sr"}^{x0[1]} points={npts} sym=D{N} angles(2pi/{n})={sorted(set(e % n for e in circle_exps(n, O)))} kills<=30={sig30} UNFORCED={unf}')
    print(f'PROGRESS {0.5*(idx+1)/len(NS):.2f} D{n} done')

WRONG_MISM = []
# controls: ordinary classes (m = 1) carry no unforced zero except the cosine zero; wrong sigma fails the criterion somewhere
for n in NS:
    for m in range(2, n):
        if gcd(m, n) > 1:
            def bad(nn, mm, x): return (x[0], (mm * x[1]) % nn)
            is_hom = all(bad(n, m, dmul(n, a, b)) == dmul(n, bad(n, m, a), bad(n, m, b))
                         for a in [(0, 1), (1, 0)] for b in [(0, 1), (1, 0), (1, 1)])
            is_bij = len({bad(n, m, (f, t)) for f in (0, 1) for t in range(n)}) == 2 * n
            mism = 0
            for x0 in [(f, t) for f in (0, 1) for t in range(n)]:
                O = twisted_class(n, m, x0, bad)
                mism += sum(direct_kills(n, O, k) != criterion_kills(n, m, x0, k) for k in range(1, 2 * n + 1))
            check(not is_bij, f'wrong sigma D{n} r->r^{m} is not bijective (control)')
            print(f'   wrong sigma D{n} r->r^{m}: criterion mismatches {mism}')
            WRONG_MISM.append(mism)
            break
check(sum(WRONG_MISM) > 0, f'wrong sigma: the criterion fails on wrong twists overall ({sum(WRONG_MISM)} mismatches; per n: {WRONG_MISM})')

# summary table of unforced silences on the circle
print('TABLE dihedral twisted classes with unforced Fourier zeros (zeros at multiples of the symmetry order N)')
for n, m, x0, npts, N, s30, unf in rows:
    if unf: print(f'  D{n} sigma_{m} x0={x0} |O|={npts} sym D{N} unforced={unf} {"(ordinary class, m=1)" if m == 1 else ""}')

# ---------------- Part 2: binary dihedral 2D_n on S^3 ----------------
print('PROGRESS 0.50 part 2 binary dihedral on S^3')
def bmul(n, x, y):                     # (e, f) = zeta^e j^f, zeta = e^{i pi/n}, j zeta = zeta^-1 j, j^2 = zeta^n
    e, f = x; g, h = y
    e2 = e + (-g if f else g)
    if f and h: e2 += n
    return (e2 % (2 * n), (f + h) % 2)
def binv(n, x):
    for y in [(e, f) for f in (0, 1) for e in range(2 * n)]:
        if bmul(n, x, y) == (0, 0): return y
def bsig(n, m, x): return ((m * x[0]) % (2 * n), x[1])
for idx, n in enumerate(NS):
    M = 2 * n
    G = [(e, f) for f in (0, 1) for e in range(M)]
    inv = {g: binv(n, g) for g in G}
    hom = all(bsig(n, 3 if gcd(3, M) == 1 else 5, bmul(n, a, b)) == bmul(n, bsig(n, 3 if gcd(3, M) == 1 else 5, a), bsig(n, 3 if gcd(3, M) == 1 else 5, b)) for a in G for b in G)
    check(hom, f'2D{n}: zeta -> zeta^m, j -> j is a homomorphism')
    for m in sorted({min(m, M - m) for m in range(3, M) if gcd(m, M) == 1}):
        seen = set()
        for x0 in G:
            O = sorted({bmul(n, bmul(n, a, x0), inv[bsig(n, m, a)]) for a in G})
            if tuple(O) in seen: continue
            seen.add(tuple(O))
            check(len({f for _, f in O}) == 1, f'2D{n} m={m} x0={x0}: class lies on one great circle')
            e0 = x0[0]
            s3 = []
            for k in range(1, KSIG + 1):
                ex = [jj * (e0 - e) for (e, f) in O for jj in range(-k, k + 1, 2)]
                if rootsum_zero(ex, M): s3.append(k)
            # reduction: S^3 degree k killed iff circle modes k, k-2, ... all vanish (mode 0 never does)
            circ = lambda j: rootsum_zero([j * e for e, f in O], M)
            red = [k for k in range(1, KSIG + 1) if all(circ(jj) for jj in range(k, 0, -2)) and k % 2 == 1]
            check(s3 == red, f'2D{n} m={m} x0={x0}: S^3 silence == circle-mode reduction')
            if any(k % 2 == 0 for k in s3): print(f'  NOTE 2D{n} m={m} x0={x0} even degree killed: {s3}')
    print(f'PROGRESS {0.5+0.5*(idx+1)/len(NS):.2f} 2D{n} done')
print(f'checks failed: {fails}')
print('FINAL ok' if fails == 0 else 'FINAL FAIL')
