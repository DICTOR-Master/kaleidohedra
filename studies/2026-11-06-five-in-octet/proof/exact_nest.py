"""Theorem (Five in the octet) - exact check in Q(sqrt2, sqrt5) (DICTO 11-06: "start on theorem").
Octahedron O of edge 1: corners (+-1/sqrt2, 0, 0) and cyclic.
(a) Pacioli icosahedron I: (0, +-a, +-b) cyclic, with a, b on O's edges: |a| + |b| = 1/sqrt2 and b = phi a  -> edge 2a = sqrt2/phi^2.
(b) D = I's 20 face centres: regular dodecahedron (check all 30 edges equal, 20 corners on one sphere).
(c) C = the 8 corners of D of the form (+-t, +-t, +-t): t = 1/(3 sqrt2), i.e. exactly O's 8 face centres: C is O's dual cube, edge sqrt2/3.
(d) T = 4 alternate corners of C: edge 2/3.
(e) C - T = 4 corner pyramids, each congruent to O's centre pyramid scaled by 2/3.
(f) In the octet's tetrahedron of edge 1: the edge midpoints give an octahedron of edge 1/2, so the same nest at half size; corners cut at
    1/3 give the Archimedean truncated tetrahedron of edge 1/3, containing that octahedron."""
import itertools, sympy as sp
s2, s5 = sp.sqrt(2), sp.sqrt(5); phi = (1 + s5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = []
    for sg in itertools.product((1, -1), repeat=3):
        for w in cyc(tuple(sp.nsimplify(x * y) if False else x * y for x, y in zip(sg, v))):
            if not any(all(sp.simplify(w[i] - u[i]) == 0 for i in range(3)) for u in S): S.append(w)
    return S
def d2(p, q): return sp.nsimplify(sp.expand(sum((p[i] - q[i]) ** 2 for i in range(3))))
def simp(x): return sp.radsimp(sp.simplify(x))
O = orbit((1 / s2, 0, 0))
a = simp(1 / (s2 * (1 + phi))); b = simp(phi * a)
I = orbit((0, a, b))
print("(a) |I| =", len(I), " corner on O's edge: a + b =", simp(a + b), "= 1/sqrt2:", simp(a + b - 1 / s2) == 0, "; edge 2a =", simp(2 * a), "= sqrt2/phi^2:", simp(2 * a - s2 / phi ** 2) == 0)
# faces of I: triples at mutual distance 2a
e2 = simp((2 * a) ** 2)
F = [t for t in itertools.combinations(range(12), 3) if all(simp(d2(I[i], I[j]) - e2) == 0 for i, j in itertools.combinations(t, 2))]
D = [tuple(simp(sum(I[k][c] for k in t) / 3) for c in range(3)) for t in F]
r2 = {simp(sum(x ** 2 for x in p)) for p in D}
dd = sorted({simp(d2(p, q)) for p, q in itertools.combinations(D, 2)}, key=lambda x: float(x))
eD2 = dd[0]; nE = sum(1 for p, q in itertools.combinations(D, 2) if simp(d2(p, q) - eD2) == 0)
print("(b) |D| =", len(D), " one sphere:", len(r2) == 1, " shortest distance^2", eD2, "occurs", nE, "times (30 = regular dodecahedron)")
C = [p for p in D if simp(abs(p[0]) - abs(p[1])) == 0 and simp(abs(p[1]) - abs(p[2])) == 0]
t = abs(C[0][0]); print("(c) |C| =", len(C), " t =", simp(t), "= 1/(3 sqrt2):", simp(t - 1 / (3 * s2)) == 0, " (O's face centres are (+-1,+-1,+-1)/(3 sqrt2)); edge", simp(2 * t))
T = [p for p in C if sp.sign(p[0] * p[1] * p[2]) > 0]
print("(d) |T| =", len(T), " edge^2", {simp(d2(p, q)) for p, q in itertools.combinations(T, 2)}, "(edge 2/3)")
# (e) corner pyramid: a corner of C not in T, with its 3 neighbours in T: legs 2t (right angles); O's centre pyramid: legs 1/sqrt2, right angles
legs = [simp(sp.sqrt(d2(c, q))) for c in C if c not in T for q in T if simp(d2(c, q) - (2 * t) ** 2) == 0][:3]
print("(e) corner pyramid legs", legs, " / O's centre-pyramid legs 1/sqrt2 =", simp(legs[0] / (1 / s2)), "(2/3)")
# (f) tetrahedron of edge 1 in the octet: midpoints -> octahedron edge 1/2; thirds -> truncated tetrahedron edge 1/3
Tt = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; Tt = [tuple(sp.Rational(1, 1) * x / (2 * s2) for x in p) for p in Tt]
M = [tuple((Tt[i][c] + Tt[j][c]) / 2 for c in range(3)) for i, j in itertools.combinations(range(4), 2)]
print("(f) midpoint octahedron edge^2", sorted({simp(d2(p, q)) for p, q in itertools.combinations(M, 2)}, key=float)[0], "(1/4: edge 1/2)")
U = [tuple(Tt[i][c] + k * (Tt[j][c] - Tt[i][c]) for c in range(3)) for i, j in itertools.permutations(range(4), 2) for k in (sp.Rational(1, 3),)]
print("    truncated tetrahedron: shortest edge^2", sorted({simp(d2(p, q)) for p, q in itertools.combinations(U, 2)}, key=float)[0], "(1/9: edge 1/3)")
print("FINAL ok")
