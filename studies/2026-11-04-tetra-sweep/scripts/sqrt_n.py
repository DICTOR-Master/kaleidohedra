#!/usr/bin/env python3
"""Conjecture (from 2D regular octagon, 3D sqrt3 exact, 4D 24-cell): on the sweep [-1,1]^n ∩ {|x|_1 <= mu} the isoperimetric quotient V^(n-1)/A^n is maximal at mu = sqrt n,
the fixed point of mu <-> n/mu. Exact: V = 2^n F_n(mu), F_n = Irwin–Hall CDF; A = 2^n (sqrt n F_n'(mu) + n F_{n-1}(mu - 1))."""
import sympy as sp, json
m = sp.symbols('mu', positive=True)
def F(n, x): return sum((-1)**k*sp.binomial(n, k)*sp.Max(x - k, 0)**n for k in range(n + 1))/sp.factorial(n)
def Fp(n, x, k0):  # piece valid for k0 < x < k0+1
    return sum((-1)**k*sp.binomial(n, k)*(x - k)**n for k in range(k0 + 1))/sp.factorial(n)
res = {}
for n in range(2, 13):
    r = sp.sqrt(n); k0 = int(sp.floor(r)); 
    if r == k0: k0s = [k0 - 1, k0]
    else: k0s = [k0]
    out = []
    for k in k0s:
        V = Fp(n, m, k); Fn1 = Fp(n - 1, m - 1, k - 1) if k >= 1 else 0
        A = sp.sqrt(n)*sp.diff(V, m) + n*Fn1
        g = (n - 1)*sp.diff(V, m)/V - n*sp.diff(A, m)/A
        val = sp.nsimplify(sp.simplify(g.subs(m, r)))
        # numeric global max over (1, n)
        out.append(str(val))
    import numpy as np, math
    def iq(x):
        k = int(math.floor(x)); V = float(Fp(n, sp.Float(x), k)); A = float((sp.sqrt(n)*sp.diff(Fp(n, m, k), m) + n*(Fp(n - 1, m - 1, k - 1) if k >= 1 else 0)).subs(m, x))
        return (n - 1)*math.log(V) - n*math.log(A)
    xs = [1 + (n - 1)*i/4000 for i in range(1, 4000)]; best = max(xs, key=iq)
    res[n] = {'dlogIQ_at_sqrt_n': out, 'numeric_argmax': best, 'sqrt_n': float(r)}
    print(n, res[n], flush=True)
json.dump(res, open('data/sqrt_n.json', 'w'), indent=1)
