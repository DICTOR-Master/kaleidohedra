#!/usr/bin/env python3
"""The two A4 golden coincidences of the census: exact point sets, symmetry group order (automorphisms of the exact Gram matrix),
sub-orbit structure, and the tones of every degree <= 24 at the point (exact in Q(sqrt5))."""
import itertools, sys, sympy as sp
from collections import Counter
phi = (1 + sp.sqrt(5))/2
def pts(base):
    P = sorted(set(itertools.permutations(base)), key=str)
    m = sum(base)/5
    return [tuple(sp.nsimplify(sp.expand(x - m)) for x in p) for p in P]
def gram(P):
    return [[sp.nsimplify(sp.expand(sum(a*b for a, b in zip(p, q)))) for q in P] for p in P]
def autos(Gm):
    """number of permutations preserving the Gram matrix (= order of the symmetry group of the point set, which spans R^4)"""
    n = len(Gm); key = [[str(x) for x in r] for r in Gm]
    count = 0
    # base: points 0..3 that span: choose greedily
    def extend(m, assigned):
        nonlocal count
        if len(m) == n:
            count += 1; return
        i = len(m)
        for j in range(n):
            if j in assigned: continue
            if key[i][i] != key[j][j]: continue
            if all(key[i][m_] == key[j][m[m_]] for m_ in range(i)):
                m.append(j); assigned.add(j); extend(m, assigned); m.pop(); assigned.discard(j)
    extend([], set())
    return count
def tone(P, k, d=4):
    x = sp.Symbol('x'); U = sp.chebyshevu(k, x)
    nn = sum(a*a for a in P[0]); tot = 0
    for q in P:
        c = sp.nsimplify(sp.expand(sum(a*b for a, b in zip(P[0], q))/nn)); tot += U.subs(x, c)
    return sp.nsimplify(sp.expand(tot))
RES = {}
for name, base in (('o3o3x3x at t = phi (20 corners)', (phi**2, phi**2, phi**2, phi, 0)), ('o3x3o3x at t = 1/phi (30 corners)', (phi**2, phi**2, 1, 1, 0)),
                   ('control: o3o3x3x at t = 2 (20 corners)', (3, 3, 3, 2, 0))):
    P = pts([sp.nsimplify(sp.expand(b)) for b in base]); Gm = gram(P)
    cos = Counter(str(sp.nsimplify(sp.expand(Gm[0][j]/Gm[0][0]))) for j in range(len(P)))
    print(f'{name}: {len(P)} points; cosines from one point: {dict(cos)}', flush=True)
    print(f'   symmetry group order (Gram automorphisms) = {autos(Gm)}  (S5 = 120, S5 x {{+-1}} = 240)', flush=True)
    zs = [k for k in range(1, 25) if tone(P, k) == 0]
    print(f'   degrees k <= 24 with tone exactly 0: {zs}', flush=True); RES[name[:7]] = zs
ok = RES.get('o3o3x3x') == [1, 2, 5, 7] and RES.get('o3x3o3x') == [1, 2, 3, 6] and RES.get('control') == [1, 2]
print('FINAL ok' if ok else 'FINAL FAIL (zero degrees differ from the census)')
