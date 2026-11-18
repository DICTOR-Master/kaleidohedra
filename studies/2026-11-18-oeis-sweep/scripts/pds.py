"""Poincare dodecahedral space S^3/2I (Queens book, Silent Queens, Theorem 3): multiplicity of the Laplace eigenvalue k(k+2),
i.e. the number of degree-k harmonics on S^3 invariant under the 120 icosians (left action). Odd k give 0 (-1 is in 2I),
so the sequence is indexed by k = 2n.

Method A: (k+1) * [t^k] (1 + t^30)/((1 - t^12)(1 - t^20))  (Molien series of 2I acting on C^2, A008651; harmonics of degree k
          on S^3 = V_{k/2} (x) V_{k/2}, left-invariant part = (k+1) * dim V_{k/2}^{2I}).
Method B: Aurich, Lustig and Steiner (2005), eqs. 26-27, closed formula r(beta), beta = k + 1.
Method C: character average over the conjugacy classes of 2I, (k+1)/120 * sum_q sin((k+1)theta_q)/sin(theta_q), in mpmath at
          60 digits, rounded (class rotation angles theta: 0 (1), pi (1), pi/2 (30), pi/3, 2pi/3 (20 each), pi/5, 2pi/5, 3pi/5,
          4pi/5 (12 each)).
Run: python pds.py"""
import mpmath as mp
mp.mp.dps = 60
NMAX = 100   # k = 0..200
K = 2 * NMAX
mol = [0] * (K + 1)
for a in range(0, K + 1, 12):
    for b in range(0, K + 1 - a, 20):
        for c in (0, 30):
            if a + b + c <= K: mol[a + b + c] += 1
A = [(k + 1) * mol[k] for k in range(K + 1)]
def r_als(b):
    if b == 1: return 1
    allowed = b in {13, 21, 25, 31, 33, 37, 41, 43, 45, 49, 51, 53, 55, 57} or (b % 2 == 1 and b >= 61)
    return b * ((b - 1) // 10 + (b - 1) // 6 + (b - 1) // 4 - (b - 3) // 2) if allowed else 0
B = [r_als(k + 1) for k in range(K + 1)]
classes = [(0, 1), (mp.pi, 1), (mp.pi / 2, 30), (mp.pi / 3, 20), (2 * mp.pi / 3, 20)] + [(j * mp.pi / 5, 12) for j in (1, 2, 3, 4)]
assert sum(m for _, m in classes) == 120
def chi(k, t):
    if t == 0: return mp.mpf(k + 1)
    if t == mp.pi: return mp.mpf((-1) ** k * (k + 1))
    return mp.sin((k + 1) * t) / mp.sin(t)
C = []
for k in range(K + 1):
    v = (k + 1) * sum(m * chi(k, t) for t, m in classes) / 120
    r = int(mp.nint(v)); assert abs(v - r) < mp.mpf(10) ** -40; C.append(r)
print('odd k all zero:', all(A[k] == 0 for k in range(1, K + 1, 2)) and all(C[k] == 0 for k in range(1, K + 1, 2)))
seq = [A[2 * n] for n in range(NMAX + 1)]
print('a(n) = multiplicity at k = 2n, n = 0..%d:' % NMAX); print(','.join(map(str, seq)))
print('A == B (ALS formula), k = 0..%d:' % K, A == B)
print('A == C (character average), k = 0..%d:' % K, A == C)
print('nonzero only, first 40:', ','.join(str(x) for x in seq if x)[:400])
print('FINAL ok' if A == B == C else 'FINAL FAIL')
