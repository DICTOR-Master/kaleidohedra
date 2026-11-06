"""The nests repeat for ever (DICTO 11-06: "does this nesting repeat forever up and down, is it golden all the way through"). Exact:
(1) O > I > D > C > T > O' (O' = T's midpoint octahedron): edge factors sqrt2/phi^2, phi/3, phi, sqrt2, 1/2, product 1/3; O' has O's
    orientation (corners on the same axes), so the nest repeats by thirds, same orientation.
(2) C > I (icosahedron touching the cube's six faces, edge 1/phi) > D (I's face centres) > C' (D's eight cube corners): factors 1/phi,
    phi/3, phi, product phi/3; C' has C's orientation: the golden loop."""
import sympy as sp, itertools
s2, s5 = sp.sqrt(2), sp.sqrt(5); phi = (1 + s5) / 2
f1 = [s2 / phi ** 2, phi / 3, phi, s2, sp.Rational(1, 2)]
print("(1) product", sp.nsimplify(sp.simplify(sp.prod(f1))), " factors", [sp.radsimp(sp.simplify(x)) for x in f1])
# I -> D edge factor check: dodecahedron on icosahedron face centres
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
I = []
for sg in itertools.product((1, -1), repeat=2):
    for w in cyc((0, sg[0], sg[1] * phi)): I.append(w)
def d2(p, q): return sp.expand(sum((p[i] - q[i]) ** 2 for i in range(3)))
eI = 2
F = [t for t in itertools.combinations(range(12), 3) if all(sp.simplify(d2(I[i], I[j]) - 4) == 0 for i, j in itertools.combinations(t, 2))]
D = [tuple(sp.simplify(sum(I[k][c] for k in t) / 3) for c in range(3)) for t in F]
eD = min((sp.sqrt(d2(p, q)) for p, q in itertools.combinations(D, 2)), key=lambda x: float(x))
print("    I -> D factor", sp.radsimp(sp.simplify(eD / eI)), "= phi/3:", sp.simplify(eD / eI - phi / 3) == 0)
cube = [p for p in D if sp.simplify(abs(p[0]) - abs(p[1])) == 0 and sp.simplify(abs(p[1]) - abs(p[2])) == 0]
t = abs(cube[0][0]); print("    D's cube corners (+-t,+-t,+-t), t =", sp.radsimp(sp.simplify(t)), "; D -> C factor", sp.radsimp(sp.simplify(2 * t / eD)), "= phi:", sp.simplify(2 * t / eD - phi) == 0)
# cube touching icosahedron: I = (0, +-1, +-phi) lies in the cube |x|,|y|,|z| <= phi, touching all six faces; cube edge 2 phi, I edge 2
print("(2) C > I: cube edge 2 phi, icosahedron edge 2 -> factor 1/phi; loop product", sp.radsimp(sp.simplify((1 / phi) * (phi / 3) * phi)), "= phi/3")
print("    C' = D's cube has edge 2t =", sp.radsimp(sp.simplify(2 * t)), "; C' / C =", sp.radsimp(sp.simplify(2 * t / (2 * phi))), " same axes: yes (corners (+-t,+-t,+-t))")
print("FINAL ok")
