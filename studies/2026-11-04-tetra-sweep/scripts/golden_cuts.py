#!/usr/bin/env python3
"""Golden Dehn-zero truncated tetrahedra: corner cuts c_i ∈ {0} ∪ {φ^-j : 1 <= j <= J} (fractions of the edge), Σc = 1 (Dehn zero), c_i + c_j <= 1 (cuts may meet
on an edge but not overlap). Exact in Z[φ] (a + bφ). For each: Fibonacci approximants (n = F_{m}, k_i = F-numbers) that are octet polyforms in the census."""
import itertools, json
J = 8
def mul(x, y): a, b = x; c, d = y; return (a*c + b*d, a*d + b*c + b*d)  # φ² = φ + 1
inv = (-1, 1)   # 1/φ = φ - 1
P = [(1, 0)]
for j in range(J): P.append(mul(P[-1], inv))
vals = {0: (0, 0), **{j: P[j] for j in range(1, J + 1)}}
def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def le1(x):  # a + bφ <= 1 exactly
    a, b = x; a -= 1; # a + bφ <= 0
    if b == 0: return a <= 0
    # a + bφ <= 0  <=>  bφ <= -a; φ = (1+√5)/2 -> compare with integers: 2bφ = b + b√5
    lhs = b + 2*a  # need b√5 <= -(b + 2a)
    r = -lhs
    if b > 0: return r >= 0 and 5*b*b <= r*r
    return r >= 0 or 5*b*b >= r*r
res = []
for js in itertools.combinations_with_replacement([0] + list(range(1, J + 1)), 4):
    if sum(1 for j in js if j) < 2: continue
    c = [vals[j] for j in js]
    if add(*c) != (1, 0): continue
    if not all(le1(add(c[a], c[b])) for a, b in itertools.combinations(range(4), 2)): continue
    res.append(js)
F = [0, 1]
for _ in range(20): F.append(F[-1] + F[-2])
# approximant: φ^-j ≈ F_{m-j}/F_m
out = []
for js in res:
    apps = []
    for m in range(4, 12):
        k = tuple(F[m - j] if j else 0 for j in js); n = F[m]
        if sum(k) == n: apps.append((n, k))
    out.append({'cuts_phi_powers': js, 'cuts': [f'φ^-{j}' if j else '0' for j in js], 'approximants_exact_sum': apps[:4]})
    print(out[-1])
json.dump(out, open('data/golden-cuts.json', 'w'), indent=1)
