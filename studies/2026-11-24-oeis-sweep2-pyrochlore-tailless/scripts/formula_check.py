#!/usr/bin/env python3
"""Check the closed form (Ihara-Bass for the 6-regular pyrochlore network, q = 5, with its spectrum: -2 with weight 1/2,
2 + mu with weight 1/2, mu over diamond's spectrum whose even moments are A002895):
  Sum_{n>=1} a(n) x^n/n = -2*log(1-x^2) - (1/2)*log(1+6*x^2+25*x^4) + Sum_{k>=1} A002895(k)*(x/(1-2*x+5*x^2))^(2k)/(4k)
against the direct count (data/direct-n40.txt), exactly with rational power series to x^40."""
from fractions import Fraction as Fr
from math import comb
M = 40
def mul(a, b): 
    c = [Fr(0)] * (M + 1)
    for i, x in enumerate(a):
        if x:
            for j in range(M + 1 - i): c[i + j] += x * b[j]
    return c
def inv(a):
    b = [Fr(0)] * (M + 1); b[0] = Fr(1) / a[0]
    for n in range(1, M + 1): b[n] = -sum(a[k] * b[n - k] for k in range(1, n + 1)) / a[0]
    return b
def log1p(u):  # log(1+u), u[0] = 0
    out = [Fr(0)] * (M + 1); p = [Fr(1)] + [Fr(0)] * M
    for k in range(1, M + 1):
        p = mul(p, u)
        for i in range(M + 1): out[i] += Fr((-1) ** (k + 1), k) * p[i]
    return out
domb = lambda n: sum(comb(n, k) ** 2 * comb(2 * k, k) * comb(2 * n - 2 * k, n - k) for k in range(n + 1))
S = [Fr(0)] * (M + 1)
for i, v in enumerate(log1p([0, 0, -1] + [0] * (M - 2))): S[i] += -2 * v
for i, v in enumerate(log1p([0, 0, 6, 0, 25] + [0] * (M - 4))): S[i] += -v / 2
y = mul([0, 1] + [0] * (M - 1), inv([1, -2, 5] + [0] * (M - 2)))
y2 = mul(y, y); p = [Fr(1)] + [Fr(0)] * M
for k in range(1, M // 2 + 1):
    p = mul(p, y2)
    for i in range(M + 1): S[i] += Fr(domb(k), 4 * k) * p[i]
a = [n * S[n] for n in range(1, M + 1)]
assert all(x.denominator == 1 for x in a)
direct = [int(t) for t in open("data/direct-n40.txt").read().split()[-1].split(",")]
print("formula:", ",".join(str(int(x)) for x in a[:12]), "...")
print("FINAL ok formula == direct count, n = 1..40" if [int(x) for x in a] == direct else "FINAL FAIL")

# Ordinary g.f. in the shape of A402231 (Ihara-Bass for a 6-regular net, q = 5), with P(x) the g.f. of the closed walks
# per pyrochlore site (Sweep 1: w(n) = ((-2)^n + Sum_k C(n,2k) 2^(n-2k) A002895(k))/2):
#   G.f.: 4*x^2/(1-x^2) - 10*x^2/(1+5*x^2) + ((1-5*x^2)/(1+5*x^2))*(P(x/(1+5*x^2)) - 1)
w = [((-2) ** n + sum(comb(n, 2 * k) * 2 ** (n - 2 * k) * domb(k) for k in range(n // 2 + 1))) // 2 for n in range(M + 1)]
z = mul([0, 1] + [0] * (M - 1), inv([1, 0, 5] + [0] * (M - 2)))
Pz = [Fr(0)] * (M + 1); p = [Fr(1)] + [Fr(0)] * M
for n in range(1, M + 1):
    p = mul(p, z)
    for i in range(M + 1): Pz[i] += w[n] * p[i]
G = [Fr(0)] * (M + 1)
for i, v in enumerate(mul([0, 0, 4] + [0] * (M - 2), inv([1, 0, -1] + [0] * (M - 2)))): G[i] += v
for i, v in enumerate(mul([0, 0, 10] + [0] * (M - 2), inv([1, 0, 5] + [0] * (M - 2)))): G[i] -= v
for i, v in enumerate(mul(mul([1, 0, -5] + [0] * (M - 2), inv([1, 0, 5] + [0] * (M - 2))), Pz)): G[i] += v
print("FINAL ok g.f. == direct count, n = 1..40" if [int(x) for x in G[1:]] == direct and G[0] == 0 else "FINAL FAIL g.f.")
