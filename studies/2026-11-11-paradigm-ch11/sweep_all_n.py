"""Chapter 11: Proposition 5.1 in every dimension: sweeping the permutohedron of 1..n by u.x (u increasing), the corners with i edges
below number the Eulerian numbers A(n, i); check n = 3..7 by listing all orderings and counting down edges directly."""
import itertools, random
def euler(n): 
    A = [[1]]
    for m in range(2, n + 1): A.append([(k + 1) * (A[-1][k] if k < len(A[-1]) else 0) + (m - k) * (A[-1][k - 1] if k >= 1 else 0) for k in range(m)])
    return A[-1]
ok = True
for n in range(3, 8):
    u = sorted(random.random() for _ in range(n)); cnt = [0] * n
    for x in itertools.permutations(range(1, n + 1)):
        f = sum(a * b for a, b in zip(u, x)); pos = {v: i for i, v in enumerate(x)}; d = 0
        for k in range(1, n):
            y = list(x); y[pos[k]], y[pos[k + 1]] = k + 1, k
            d += sum(a * b for a, b in zip(u, y)) < f
        cnt[d] += 1
    print(n, cnt, euler(n)); ok &= cnt == euler(n)
print('FINAL ok' if ok else 'FINAL FAIL')
