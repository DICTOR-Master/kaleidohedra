# cubes_period.py: independent numerical test (our own code) of Blanco Gomez, "The least period of cubes modulo m" (aiXiv 2610.01408,
# ai-authored): least positive period of n^3 mod m is m/3 when 9 | m and m otherwise; T is a period iff m | 3T and m | T^3; the same
# for +-(n+a)^3 + c. Brute force: for each m <= M, test every divisor T of m (a period of an m-periodic sequence divides m... checked
# too: no non-divisor T < m is a period) on all n mod m.
import sys
M = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
def is_period(f, m, T): return all(f(n + T) % m == f(n) % m for n in range(m))
bad = []; crit_bad = []
for m in range(1, M + 1):
    f = lambda n: n ** 3
    least = next(T for T in range(1, m + 1) if is_period(f, m, T)) if m <= 400 else min(T for T in range(1, m + 1) if m % T == 0 and is_period(f, m, T))
    claim = m // 3 if m % 9 == 0 else m
    if least != claim: bad.append((m, least, claim))
    if m <= 600:
        for T in range(1, m + 1):
            if is_period(f, m, T) != (((3 * T) % m == 0) and ((T ** 3) % m == 0)): crit_bad.append((m, T)); break
trans_bad = []
for m in range(1, 301):
    claim = m // 3 if m % 9 == 0 else m
    for a, c, s in ((1, 0, 1), (5, 7, -1), (-3, 2, 1), (11, -4, -1)):
        g = lambda n: s * (n + a) ** 3 + c
        least = next(T for T in range(1, m + 1) if is_period(g, m, T))
        if least != claim: trans_bad.append((m, a, c, s, least)); break
print(f'least period = m/3 if 9|m else m: tested m <= {M} (all T for m <= 400, divisors beyond): mismatches {len(bad)} {bad[:3]}')
print(f'criterion (period iff m | 3T and m | T^3): every T tested for m <= 600: mismatches {len(crit_bad)} {crit_bad[:3]}')
print(f'translated/reflected +-(n+a)^3+c, four (a,c,sign), m <= 300: mismatches {len(trans_bad)} {trans_bad[:3]}')
print('FINAL ok' if not (bad or crit_bad or trans_bad) else 'FINAL FAIL')
