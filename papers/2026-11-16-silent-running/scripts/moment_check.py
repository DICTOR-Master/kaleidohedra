"""Silent Running, Proposition 7: odd moments of the golden 20-set X (perms of (φ²,φ²,φ²,φ,0), centred, unit radius).
Exact Gegenbauer (Chebyshev U) coefficients in rational arithmetic; numerical moments in random directions. Pure Python; seconds."""
import itertools, random, math
from fractions import Fraction as Fr
U = [[Fr(1)], [Fr(0), Fr(2)]]  # coefficient lists, U_{j+1} = 2t U_j - U_{j-1}
for j in range(1, 7):
    a = [Fr(0)] + [2 * c for c in U[j]]; b = U[j - 1] + [Fr(0)] * (len(a) - len(U[j - 1]))
    U.append([x - y for x, y in zip(a, b)])
def expand(k):  # t^k = sum_j e[j] U_j, by peeling off the top degree
    r = [Fr(0)] * k + [Fr(1)]; e = [Fr(0)] * (k + 1)
    for j in range(k, -1, -1):
        c = r[j] / U[j][j]; e[j] = c
        r = [x - c * (U[j][i] if i < len(U[j]) else 0) for i, x in enumerate(r)]
    return e
def coeff(k, j): return expand(k)[j]
c33, c53, c73 = coeff(3, 3), coeff(5, 3), coeff(7, 3)
print('U3 coefficient of t^3, t^5, t^7:', c33, c53, c73, ' ratios', c53 / c33, c73 / c33)
assert c53 / c33 == 1 and c73 / c33 == Fr(7, 8)
phi = (1 + 5 ** 0.5) / 2
X = sorted(set(itertools.permutations((phi**2, phi**2, phi**2, phi, 0.0))))
m = sum(X[0]) / 5
X = [[a - m for a in x] for x in X]; r = math.sqrt(sum(a * a for a in X[0])); X = [[a / r for a in x] for x in X]
assert len(X) == 20
random.seed(1); worst = 0
for _ in range(400):
    u = [random.gauss(0, 1) for _ in range(5)]; mu = sum(u) / 5; u = [a - mu for a in u]; n = math.sqrt(sum(a * a for a in u)); u = [a / n for a in u]
    p = {k: sum(sum(a * b for a, b in zip(x, u)) ** k for x in X) for k in (3, 5, 7)}
    worst = max(worst, abs(p[5] - p[3]), abs(p[7] - 7 / 8 * p[3]))
print('max |p5 - p3|, |p7 - 7/8 p3| over 400 directions:', worst)
print('FINAL ok' if worst < 1e-12 else 'FINAL FAIL')
