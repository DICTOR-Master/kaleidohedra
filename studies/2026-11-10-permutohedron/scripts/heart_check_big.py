# heart_check_big.py, DICTO 12 Nov 2026 (hearts for 17, 19, 21 values, Figure 3b in 3 rows of 3). Theorem 2b checked for large n, where
# heart_every_dim.py's subset-sum LP (2^n rows) is too big. Birkhoff form: x is in Perm(1..n) iff x = B v with B doubly stochastic
# (n^2 variables). Support of the k-fold crossing S_k (x_1 = ... = x_k = c) in direction u: max u . x_rest over such B; compared with
# the support of Perm(w_k) (sorted dot product) in 100 random directions; and every order of w_k lies in S_k (majorization, exact).
# Control: a deliberately wrong value set is rejected. usage: python3 heart_check_big.py 17 19 21
import sys, random, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
def rule(n, k):
    c = (n + 1) // 2; j = (k + 1) // 2; r = 2 * j - 1 if k % 2 else 2 * j + 1; lo = c - (r - 1) // 2
    return sorted([x for x in range(1, n + 1) if not lo <= x < lo + r] + ([c] if k % 2 == 0 else []))
def majorized(x, v):
    xs = sorted(x, reverse=True); vs = sorted(v, reverse=True); a = b = 0
    if sum(xs) != sum(vs): return False
    for p, q in zip(xs, vs):
        a += p; b += q
        if a > b: return False
    return True
def check(n, k, w, rng, trials=100):
    v = np.arange(1, n + 1, dtype=float); c = (n + 1) // 2; N = n * n
    A = lil_matrix((2 * n + k, N)); b = []
    for i in range(n):
        for j in range(n): A[i, i * n + j] = 1; A[n + j, i * n + j] = 1
    b += [1] * (2 * n)
    for i in range(k):
        for j in range(n): A[2 * n + i, i * n + j] = v[j]
        b.append(c)
    A = A.tocsr(); good = all(majorized([c] * k + list(p), list(range(1, n + 1))) for p in set(itertools.permutations(w)))
    for _ in range(trials):
        u = [rng.random() for _ in range(n - k)]; obj = np.zeros(N)
        for t, i in enumerate(range(k, n)): obj[i * n:(i + 1) * n] = -u[t] * v
        r = linprog(obj, A_eq=A, b_eq=b, bounds=(0, None), method='highs'); h = -r.fun
        good &= abs(h - sum(x * y for x, y in zip(sorted(u), sorted(w)))) < 1e-7
        if not good: break
    return good
rng = random.Random(21); ok = True
for n in map(int, sys.argv[1:]):
    for k in (n - 4, n - 3, n - 2):
        g = check(n, k, rule(n, k), rng); ok &= g; print(f"n {n} k {k}: Perm{tuple(rule(n, k))} = crossing: {g}", flush=True)
n = int(sys.argv[1]); bad = rule(n, n - 3); bad = [bad[0], bad[1] + 1, bad[2]]
neg = not check(n, n - 3, bad, rng, 20); print(f"control: wrong set {bad} rejected: {neg}")
print("FINAL ok" if ok and neg else "FINAL FAIL")
