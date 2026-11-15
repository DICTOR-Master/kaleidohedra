#!/usr/bin/env python3
"""Are the two golden A4 corner sets subsets of a 600-cell?  The 600-cell's 120 vertices (unit) are the H4 root system, closed under
reflection in its own members; so close the normalised set under reflections in its members (exact, Q(sqrt5) via sympy) and count.
Then split the closure into S5-orbits (sizes)."""
import itertools, sympy as sp
phi = (1 + sp.sqrt(5))/2
def centred(base):
    P = sorted(set(itertools.permutations(base)), key=str); m = sum(base)/5
    return [tuple(sp.nsimplify(sp.expand(x - m)) for x in p) for p in P]
def dot(a, b): return sp.nsimplify(sp.expand(sum(x*y for x, y in zip(a, b))))
def closure(P):
    n2 = dot(P[0], P[0]); S = {tuple(P)} and set(P); fr = list(P)
    while fr:
        nf = []
        for x in fr:
            for r in list(S):
                c = sp.nsimplify(sp.expand(2*dot(x, r)/n2))
                y = tuple(sp.nsimplify(sp.expand(a - c*b)) for a, b in zip(x, r))
                if y not in S:
                    S.add(y); nf.append(y)
                    if len(S) > 1000: return S
        fr = nf
    return S
SIZES = []
for name, base in (('20 corners at t = phi', (phi**2, phi**2, phi**2, phi, 0)), ('30 corners at t = 1/phi', (phi**2, phi**2, 1, 1, 0)), ('control t = 2', (3, 3, 3, 2, 0))):
    P = centred([sp.nsimplify(sp.expand(b)) for b in base])
    S = closure(P); SIZES.append(len(S))
    print(f'{name}: closure under reflection in its own members has {len(S) if len(S) <= 1000 else ">1000"} points', flush=True)
    if len(S) <= 1000:
        n2 = dot(P[0], P[0]); cs = sorted({str(sp.nsimplify(dot(P[0], q)/n2)) for q in S}); print('   cosines', cs, flush=True)
        # S5 orbits of the closure
        rem = set(S); orbs = []
        while rem:
            x = next(iter(rem)); o = {tuple(x[g[i]] for i in range(5)) for g in itertools.permutations(range(5))}; rem -= o; orbs.append(o)
        print('   S5-orbit sizes', sorted(len(o) for o in orbs), flush=True)
print('FINAL ok' if SIZES and SIZES[0] == 120 else 'FINAL FAIL (20-set closure is not a 600-cell)')
