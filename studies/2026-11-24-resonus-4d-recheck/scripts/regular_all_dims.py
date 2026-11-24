"""Claim check: which regular polytopes have Resonus = their whole mirror arrangement?
Exact. Polygons by exact angle arithmetic (lines as rational multiples of pi, mod pi); the 1D segment; the five
Platonic solids; simplex, cube and cross-polytope for n = 2..7; (the 4D rows are in recheck.py).
Prints FINAL ok only if every computed count matches the closed forms below."""
from fractions import Fraction as Fr
from itertools import product
import recheck as R
from recheck import K, PHI, check, vsub, vscale, dot, linekey, Poly, facets_by_subsets

out = []

# ---- polygons: corners at angles 2 pi j / m; lines by angle / pi mod 1 ----
for m in range(3, 41):
    # mirror lines of the dihedral group D_m are at angles pi j / m (j = 0..m-1)
    dm = {Fr(j, m) % 1 for j in range(m)}
    check(len(dm) == m, "D_m has m mirrors")
    normals = [Fr(2 * j + 1, m) % 1 for j in range(m)]           # edge-midpoint directions (2j+1) pi/m, as angle/pi
    resonus = {(x + Fr(1, 2)) % 1 for x in normals}                    # line parallel to the edge
    on = len(resonus & dm)
    exp_res = m if m % 2 else m // 2
    exp_on = 0 if m % 2 else m // 2
    check(len(resonus) == exp_res and on == exp_on, f"{m}-gon")
    out.append((f"{m}-gon", m, len(resonus), on, len(resonus) == m and on == m))

# ---- 1D segment ----
seg = Poly("segment", [(K(1),), (K(-1),)], [(K(1),), (K(-1),)], 1)
Rs, Ms = seg.resonus(), seg.mirrors()
out.append(("segment (1D)", len(Ms), len(Rs), len(Rs & Ms), Rs == Ms))

def row(P):
    Rs, Ms = P.resonus(), P.mirrors()
    out.append((P.name, len(Ms), len(Rs), len(Rs & Ms), Rs == Ms))
    return len(Ms), len(Rs), len(Rs & Ms)

# ---- Platonic solids (D, I, C, T, O order) ----
ph = PHI; ip = PHI - 1
D = [tuple(K(s) for s in sg) for sg in product((1, -1), repeat=3)]
for a, b in product((1, -1), repeat=2):
    for c in range(3):
        v = [K(0), a * ip, b * ph]; v = v[c:] + v[:c]; D.append(tuple(v))
Ic = []
for a, b in product((1, -1), repeat=2):
    for c in range(3):
        v = [K(0), K(a), b * ph]; v = v[c:] + v[:c]; Ic.append(tuple(v))
C = [tuple(K(s) for s in sg) for sg in product((1, -1), repeat=3)]
T = [tuple(K(s) for s in sg) for sg in product((1, -1), repeat=3) if sg[0] * sg[1] * sg[2] == 1]
O = [tuple(K(s if i == j else 0) for i in range(3)) for j in range(3) for s in (1, -1)]
for name, V, nf, exp in [("dodecahedron", D, 12, (15, 6, 0)), ("icosahedron", Ic, 20, (15, 10, 0)),
                         ("cube", C, 6, (9, 3, 3)), ("tetrahedron", T, 4, (6, 4, 0)), ("octahedron", O, 8, (9, 4, 0))]:
    A = facets_by_subsets(V, 3)
    check(len(A) == nf, name + " facets")
    got = row(Poly(name, V, A, 3))
    check(got == exp, f"{name} {got} vs {exp}")

# ---- simplex, cube, cross-polytope, n = 2..7 ----
for n in range(2, 8):
    one = tuple(K(1) for _ in range(n + 1))
    Vs = [tuple(K(Fr(n, n + 1)) if i == j else K(Fr(-1, n + 1)) for i in range(n + 1)) for j in range(n + 1)]
    As = []
    for j in range(n + 1):
        a = tuple(K(-(n + 1)) if i == j else K(0) for i in range(n + 1))
        As.append(vsub(a, vscale(dot(a, one) / (n + 1), one)))
    got = row(Poly(f"{n}-simplex", Vs, As, n, C=[one]))
    check(got == ((n + 1) * n // 2, n + 1, 0), f"{n}-simplex {got}")
    Vc = [tuple(K(s) for s in sg) for sg in product((1, -1), repeat=n)]
    Ac = [tuple(K(s if i == j else 0) for i in range(n)) for j in range(n) for s in (1, -1)]
    got = row(Poly(f"{n}-cube", Vc, Ac, n))
    check(got == (n * n, n, n), f"{n}-cube {got}")
    Vx = [tuple(K(s if i == j else 0) for i in range(n)) for j in range(n) for s in (1, -1)]
    Ax = [tuple(K(s) for s in sg) for sg in product((1, -1), repeat=n)]
    got = row(Poly(f"{n}-cross-polytope", Vx, Ax, n))
    check(got == (n * n, 2 ** (n - 1), n if n == 2 else 0), f"{n}-cross-polytope {got}")

print("name | mirrors | Resonus | Resonus on mirrors | Resonus = all mirrors")
for r in out: print(*r, sep=" | ")
eq = [r[0] for r in out if r[4]]
print("Resonus = whole mirror arrangement:", eq)
check(eq == ["segment (1D)"], "only the segment among these (the 4D: only the 120-cell, recheck.py)")
print(f"FINAL ok ({R.NCHK} exact checks)")
