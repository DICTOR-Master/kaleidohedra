"""Exact tile and point counts per cell on every rung (Theorem 3a): tiles of type {i,j,k} per cell = |det(g_l, g_m, g_n)| / covol(Lambda_perp)
with {l,m,n} the complementary triple; prolate or oblate by the physical rhombohedron's volume; points = tiles. Lambda_perp = Z-span of the
rational hidden vectors g_i (q = rung's ratio); its covolume = gcd of the 3x3 minors of the integer-scaled generator matrix / scale^3."""
import itertools, math, sympy as sp
from functools import reduce
phi = (1 + sp.sqrt(5)) / 2
def dirs(t): return [sp.Matrix([1, t, 0]), sp.Matrix([-1, t, 0]), sp.Matrix([0, 1, t]), sp.Matrix([0, -1, t]), sp.Matrix([t, 0, 1]), sp.Matrix([t, 0, -1])]
E = dirs(phi)
for n, m in ((1, 1), (2, 1), (3, 2), (5, 3), (8, 5), (13, 8), (21, 13)):
    q = sp.Rational(m, n); G = dirs(-q)
    den = sp.ilcm(*[sp.fraction(x)[1] for g in G for x in g]); Gi = [[int(x * den) for x in g] for g in G]
    minors = [abs(sp.Matrix([Gi[a], Gi[b], Gi[c]]).det()) for a, b, c in itertools.combinations(range(6), 3)]
    cov = sp.Rational(reduce(math.gcd, [int(x) for x in minors if x]), den ** 3)
    pro = obl = 0
    for tri in itertools.combinations(range(6), 3):
        comp = [x for x in range(6) if x not in tri]
        cnt = abs(sp.Matrix.hstack(*[G[x] for x in comp]).det()) / cov
        vphys = sp.nsimplify(abs(sp.Matrix.hstack(*[E[x] for x in tri]).det()))
        if cnt == 0: continue
        if sp.N(vphys) > 4.5: pro += cnt   # prolate 2 phi^2 = 5.236, oblate 2 phi = 3.236
        else: obl += cnt
    print(f"rung {n}/{m}: prolate {pro} + oblate {obl} = {pro + obl}  (ratio {float(pro/obl):.6f})")
print("FINAL ok")
