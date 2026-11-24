"""Regions of the Resonus of the (n-1)-dimensional permutohedron, n = 3..6, i.e. of the resonance arrangement R_d (d = n-1):
hyperplanes sum_{i in S} y_i = 0, S a nonempty subset of {1..d}, in R^d.
Exact method: finite field method (Athanasiadis, Adv. Math. 122 (1996)): for a prime q not dividing any nonzero minor of the
0/1 coefficient matrix, chi(q) = #{y in F_q^d : no sum_{i in S} y_i = 0}. Minors of 0/1 matrices of size <= 5 are at most 5 in
absolute value (Hadamard's maximal-determinant values 1, 1, 2, 3, 5), so every prime q >= 7 is good.
chi is monic of degree d: d unknown coefficients, solved from d primes; checked on two more primes, by chi(1) = 0 (central
arrangement) and by the t^(d-1) coefficient = -(number of hyperplanes).
Regions = (-1)^d chi(-1) (Zaslavsky 1975)."""
import itertools
from fractions import Fraction as Fr
import numpy as np


def count(d, q):
    subsets = [S for k in range(1, d + 1) for S in itertools.combinations(range(d), k)]
    total = 0
    for y0 in range(q):  # slice on the first coordinate to keep memory small
        grid = np.array(list(itertools.product(range(q), repeat=d - 1)), dtype=np.int64).reshape(-1, d - 1)
        Y = np.concatenate([np.full((grid.shape[0], 1), y0, dtype=np.int64), grid], axis=1)
        ok = np.ones(Y.shape[0], dtype=bool)
        for S in subsets:
            ok &= (Y[:, list(S)].sum(axis=1) % q) != 0
        total += int(ok.sum())
    return total


def solve(A, b):
    n = len(A); M = [[Fr(x) for x in row] + [Fr(bb)] for row, bb in zip(A, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


PRIMES = [7, 11, 13, 17, 19, 23, 29]
ok = True
for n in range(3, 7):
    d = n - 1
    use = PRIMES[:d]; check = PRIMES[len(use):len(use) + 2]
    vals = {q: count(d, q) for q in use + check}
    # chi(t) = t^d + c_{d-1} t^{d-1} + ... + c_0
    A = [[q ** k for k in range(d - 1, -1, -1)] for q in use]; b = [vals[q] - q ** d for q in use]
    c = solve(A, b)
    chi = lambda t: t ** d + sum(ci * t ** k for ci, k in zip(c, range(d - 1, -1, -1)))
    good = (all(chi(q) == vals[q] for q in check) and all(x.denominator == 1 for x in c) and chi(1) == 0
            and c[0] == -(2 ** d - 1))
    regions = (-1) ** d * chi(-1)
    print(f"n={n} (dim {d}): hyperplanes {2 ** d - 1}, chi(t) coefficients {[1] + [int(x) for x in c]} (t^{d} .. t^0),",
          f"checked on q={check}: {good}; regions {regions}")
    ok &= good
print("FINAL ok" if ok else "FINAL fail")
