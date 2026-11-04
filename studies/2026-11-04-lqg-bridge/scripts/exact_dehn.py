#!/usr/bin/env python3
"""EXACT Dehn invariant for HexOct pieces (replaces the float screen there; ledger METHOD-FAILED 4 Nov).
All HexOct dihedrals lie in {π−2β, 2β, π−β, π/2+β} ∪ rational multiples of π, β = arccos(1/√3); so Dehn = (Σ c_e L_e) ⊗ β, c_e ∈ {−2, 2, −1, 1, 0}.
Squared edge lengths are rational in lattice coordinates (Δu² + ΔuΔv + Δv² + (2/3)Δz², layer units), so L_e = r_e √d_e (d squarefree): Dehn = 0 iff
Σ_{e: d_e = d} c_e r_e = 0 for every d — exact Fractions. Floats only identify which of the 7 angles an edge has (gaps of >= 10°)."""
import os, sys, math, itertools, numpy as np
from fractions import Fraction as Fr
from collections import defaultdict
from scipy.spatial import ConvexHull
HEX = os.path.expanduser('~/kres-tmp/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as Tl
os.chdir(here); Hh = math.sqrt(2/3)
b = math.degrees(math.acos(1/math.sqrt(3)))
ANG = {180 - 2*b: -2, 2*b: 2, 180 - b: -1, 90 + b: 1, 90: 0, 120: 0, 135: 0, 60: 0, 45: 0, 150: 0}
def coef(deg):
    k = min(ANG, key=lambda a: abs(a - deg)); assert abs(k - deg) < 1e-6, f'unknown dihedral {deg}'; return ANG[k]
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*Hh])
def sqfree(n):
    d, k = 1, 2
    while k*k <= n:
        while n % (k*k) == 0: n //= k*k
        k += 1
    return n
def split_sqrt(q):   # q = Fraction > 0 -> (r, d) with sqrt(q) = r*sqrt(d)
    a, bb = q.numerator, q.denominator; m = a*bb; d = sqfree(m); r2 = Fr(m, d)/(bb*bb); r = Fr(math.isqrt(r2.numerator), math.isqrt(r2.denominator)); assert r*r == r2; return r, d
def q_len(p, q):
    du, dv, dz = (Fr(p[i]) - Fr(q[i]) for i in range(3)); return du*du + du*dv + dv*dv + Fr(2, 3)*dz*dz
def exact_dehn(P):
    """P: list of exact lattice points (Fractions) of a convex piece; returns {d: Σ c r} (all zero <=> Dehn zero)."""
    P = list(dict.fromkeys(tuple(Fr(x) for x in p) for p in P)); X = np.array([cart(p) for p in P]); h = ConvexHull(X)
    fs = {}
    for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), set()).update(s)
    normals = {k: np.array(k[:3]) for k in fs}
    edges = defaultdict(list)
    for k, idx in fs.items():
        idx = list(idx); n = normals[k]; c = X[idx].mean(0); u = X[idx[0]] - c; w = np.cross(n, u)
        idx.sort(key=lambda i: math.atan2((X[i] - c) @ w, (X[i] - c) @ u))
        for a_, b_ in zip(idx, idx[1:] + idx[:1]): edges[frozenset((a_, b_))].append(k)
    S = defaultdict(Fr)
    for e, ks in edges.items():
        if len(ks) != 2: continue
        n1, n2 = normals[ks[0]], normals[ks[1]]; deg = 180 - math.degrees(math.acos(np.clip(n1 @ n2, -1, 1)))
        c = coef(deg)
        if c == 0: continue
        i, j = tuple(e); r, d = split_sqrt(q_len(P[i], P[j])); S[d] += c*r
    return dict(S)
if __name__ == '__main__':
    for word, L, nm in (('AB', 0, 'h'), ('ABC', 1, 'c')):
        for l in ('1/10', '1/5', '5/24', '11/48', '1/4', '7/24', '1/3', '17/48', '3/8', '2/5'):
            os.chdir(HEX); pcs, _ = Tl.tile(word, L, Fr(l)); os.chdir(here)
            row = []
            for k, up, s_, P, J in pcs:
                S = exact_dehn(P); z = all(v == 0 for v in S.values()); row.append(f"{k}{'+' if up else '-'}: {'ZERO' if z else 'nonzero ' + str({d: str(v) for d, v in S.items() if v != 0})}")
            print(f"{nm}-tile λ={l}: " + ' | '.join(dict.fromkeys(row)), flush=True)
