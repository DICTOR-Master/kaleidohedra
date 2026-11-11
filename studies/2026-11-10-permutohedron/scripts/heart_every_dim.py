# heart_every_dim.py, DICTO 12 Nov 2026 ("start the 4D vacuus permutohedron paper" -> #105 Version 4, lead 3: the heart in every dimension).
# Permutohedron of 1..n, n = 2m+1, centre value c = m+1. S_k = the section where k chosen coordinates all equal c (k-fold crossing of the
# central slices x_i = c). Claim tested: S_k is itself a permutohedron Perm(w_k) of n-k values. Method (exact, Fractions): a point y is in
# Perm(v) iff y is majorized by v (Rado 1952). S_k = {y : (c^k, y) majorized by v}. Its vertex in a generic direction u is found by LP;
# collect the sorted coordinates of the vertices in many directions -> w_k if all the same; then CONFIRM exactly: Perm(w_k) = S_k by
# (i) every permutation of w_k lies in S_k (majorization, exact) and (ii) the support functions agree in 200 random directions (LP vs sort).
# Controls: n = 5, k = 1 must give (1,2,4,5) (#105 Theorem 2) and k = 2 the regular hexagon (1,3,5); negative control: the verifier must
# REJECT three wrong value sets (12 Nov: earlier negative controls x1 = 4, x1 = x2 = 5/2 and the slice x1 + x2 = 6 were not negatives:
# every coordinate fix gives a permutohedron, and that slice's corners are corners of the solid; recorded in the README). RULE checked for every n, k: k = 2j-1 removes the middle 2j-1
# values; k = 2j removes the middle 2j+1 values and puts back the centre c.
import itertools, random, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
def majorized(x, v):
    xs = sorted(x, reverse=True); vs = sorted(v, reverse=True)
    if sum(xs) != sum(vs): return False
    a = b = 0
    for p, q in zip(xs, vs):
        a += p; b += q
        if a > b: return False
    return True
def support_LP(n, k, fixval, u):
    """max u.y over y in R^(n-k) with (fixval^k, y) majorized by 1..n (subset-sum constraints)."""
    v = list(range(1, n + 1)); top = [sum(sorted(v, reverse=True)[:s]) for s in range(n + 1)]
    d = n - k; A = []; b = []
    for s in range(1, n):
        for T in itertools.combinations(range(n), s):
            row = [1.0 if (k + j) in T else 0.0 for j in range(d)]; kin = sum(1 for t in T if t < k)
            A.append(row); b.append(top[s] - kin * fixval)
    r = linprog(-np.array(u, float), A_ub=A, b_ub=b, A_eq=[[1.0] * d], b_eq=[n * (n + 1) / 2 - k * fixval], bounds=[(None, None)] * d, method='highs')
    return -r.fun, r.x
def analyse(n, k, fixval, rng):
    v = list(range(1, n + 1)); d = n - k; sorts = set()
    for _ in range(60):
        u = [rng.random() for _ in range(d)]; _, y = support_LP(n, k, fixval, u)
        sorts.add(tuple(sorted(Fr(round(t * 2)) / 2 for t in y)))
    if len(sorts) != 1: return None, len(sorts)
    w = list(next(iter(sorts)))
    ok = all(majorized([Fr(fixval)] * k + list(p), v) for p in set(itertools.permutations(w)))
    for _ in range(200):
        u = [rng.random() for _ in range(d)]; h, _ = support_LP(n, k, fixval, u)
        hw = sum(a * b for a, b in zip(sorted(u), sorted(float(t) for t in w)))
        ok &= abs(h - hw) < 1e-7
    return (w if ok else None), 1
rng = random.Random(12); ok = True; out = []
for n in (3, 5, 7, 9):
    c = (n + 1) // 2
    for k in range(1, n - 1):
        w, ns = analyse(n, k, c, rng)
        gaps = None if w is None else [w[i + 1] - w[i] for i in range(len(w) - 1)]
        print(f"n {n} k {k}: section = {'Perm' + str(tuple(str(t) for t in w)) if w else 'NOT one permutohedron'}  gaps {gaps and [str(g) for g in gaps]}", flush=True)
        out.append((n, k, w)); ok &= w is not None
# controls
w51 = [w for (n, k, w) in out if n == 5 and k == 1][0]; w52 = [w for (n, k, w) in out if n == 5 and k == 2][0]
c1 = w51 == [1, 2, 4, 5]; c2 = w52 == [1, 3, 5]
def verify(n, k, fixval, w, rng):
    v = list(range(1, n + 1)); d = n - k
    good = all(majorized([Fr(fixval)] * k + list(p), v) for p in set(itertools.permutations(w)))
    for _ in range(100):
        u = [rng.random() for _ in range(d)]; h, _ = support_LP(n, k, fixval, u)
        good &= abs(h - sum(x * y for x, y in zip(sorted(u), sorted(float(t) for t in w)))) < 1e-7
    return good
wrong = [(5, 2, [2, 3, 5]), (7, 1, [1, 3, 3, 5, 6, 7]), (7, 4, [2, 4, 6])]
rej = [not verify(n, k, (n + 1) // 2, w, rng) for n, k, w in wrong]; c3 = all(rej); ns = sum(rej)
def rule(n, k):
    c = (n + 1) // 2; j = (k + 1) // 2; r = 2 * j - 1 if k % 2 else 2 * j + 1; lo = c - (r - 1) // 2
    w = [x for x in range(1, n + 1) if not lo <= x < lo + r]
    return sorted(w + ([c] if k % 2 == 0 else []))
c4 = all(w == rule(n, k) for (n, k, w) in out)
print(f"controls: n5k1 = (1,2,4,5) {c1}; n5k2 = (1,3,5) {c2}; verifier rejects {ns}/3 wrong value sets {c3}; rule holds for every n, k: {c4}")
print("FINAL ok" if ok and c1 and c2 and c3 and c4 else "FINAL FAIL")
