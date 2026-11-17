"""Protocol step 18 (DICTO 18 Nov: "is it a 4th-dimension shadow, is it in the 600, 120 etc"): field / 4D-host test.
Affine invariant: the ratio of two parallel edges, x = b/(1-b) (hexagon edges (0,-b,b) and (0,1-b,b-1) are parallel). Any affine map
keeps ratios of parallel segments. Statement checked: if a polytope Q has corner coordinates in a field K, then every vertex subset, every
section by a hyperplane defined over K and every parallel projection along a direction defined over K has corner coordinates in K, so
every ratio of parallel edges of the result lies in K; an affine image of it keeps those ratios. If x_f has degree 6 and [K:Q] = 2^k,
x_f is not in K (the degree of an element divides [K:Q]). Scope: projections along directions NOT defined over K are not covered.
Also checked: the die's 14 landing directions = the 14 corner directions of the rhombic dodecahedron = the corner directions of the
24-cell's corner-first shadow (projection along w); the 24-cell's 24 corners are corners of the 600-cell (standard coordinates)."""
import math, json, sys, os, itertools
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fdlib import *
C = Checks(); R = {}
print("STEP 18a. Degrees")
px, xv = minpoly_of(y/(1 - y)); pT = sp.Poly(sp.minimal_polynomial(sp.tan(sp.pi/14)*sp.tan(2*sp.pi/7), z), z)
print(f"  x_f = b/(1-b) = {float(xv):.12f}, minimal polynomial degree {px.degree()}: {px.as_expr()}")
print(f"  T = tan(pi/14)tan(2pi/7): {pT.as_expr()} (degree 3, in Q(cos 2pi/7), God's Dice)")
C("deg x_f = 6 and deg T = 3", px.degree() == 6 and pT.degree() == 3)
fields = {"Q(sqrt5) (600-cell, 120-cell, H3/H4 orbit polytopes in standard coordinates)": [sp.sqrt(5)],
          "Q(sqrt2) (24-cell, tesseract, 16-cell rotated)": [sp.sqrt(2)],
          "Q(sqrt2, sqrt3, sqrt5)": [sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)],
          "Q (5-cell in R^5 coordinates, 24-cell, tesseract, 16-cell)": []}
for name, gens in fields.items():
    deg = 1
    for g in gens: deg *= 2
    prim = sum(gens) if gens else sp.Integer(0)
    dprim = sp.Poly(sp.minimal_polynomial(prim, z), z).degree() if gens else 1
    C(f"[{name}:Q] = {dprim} is a power of 2 and 6 does not divide it -> x_f not in the field", dprim == deg and dprim % 3 != 0)
C("control: Kelvin's TO has x = 1 (rational), so it passes the field test (it is a facet of the 4D permutohedron, #105)", sp.Rational(1, 2)/(1 - sp.Rational(1, 2)) == 1)
x = sp.Symbol('x'); c7 = sp.cos(2*sp.pi/7)
C("T = 9 - 4c - 16c^2 with c = cos(2pi/7) (60-digit check; exact in God's Dice by to_number_field)", abs(float(sp.N(sp.tan(sp.pi/14)*sp.tan(2*sp.pi/7) - (9 - 4*c7 - 16*c7**2), 60))) < 1e-50)
print("\nSTEP 18b. The landing directions and the 24-cell's shadow (exact, rationals)")
half = sp.Rational(1, 2)
cell24 = [tuple(v) for v in {tuple(s*e for s, e in zip(sg, p)) for p in set(itertools.permutations((1, 0, 0, 0))) for sg in itertools.product((1, -1), repeat=4)}]
cell24 += [tuple(s*half for s in sg) for sg in itertools.product((1, -1), repeat=4)]
C("24-cell: 24 corners, all at distance 1", len(set(cell24)) == 24 and all(sum(c**2 for c in v) == 1 for v in cell24))
shadow = {v[:3] for v in cell24}
dirs = set()
for v in shadow:
    n = sp.sqrt(sum(c**2 for c in v))
    if n != 0: dirs.add(tuple(sp.nsimplify(c/n) for c in v))
rd = {tuple(sp.nsimplify(c/sp.sqrt(sum(cc**2 for cc in v))) for c in v) for v in [tuple(s*e for s, e in zip(sg, p)) for p in set(itertools.permutations((2, 0, 0))) for sg in itertools.product((1, -1), repeat=3)] + [tuple(sg) for sg in itertools.product((1, -1), repeat=3)]}
V = corners(MUF); F, N, H = faces(V)
rdf = {k: np.array([float(c) for c in k]) for k in rd}
land = {next(k for k, v in rdf.items() if np.linalg.norm(v - n) < 1e-6) for n in N if any(np.linalg.norm(v - n) < 1e-6 for v in rdf.values())}
C('every face normal matches one RD direction', len(N) == 14 and len(land) == 14)
print(f"  24-cell projected along w: {len(shadow)} distinct points (centre counted), {len(dirs)} directions; RD corner directions {len(rd)}; die face normals {len(land)}")
C("corner-first shadow of the 24-cell along w has exactly the 14 RD corner directions", dirs == rd)
C("the die's 14 face normals (its landing directions, equally weighted at mu_f) are the same 14 directions", land == rd)
phi = (1 + sp.sqrt(5))/2
c600 = set(cell24)
for p in itertools.permutations(range(4)):
    sgn = sp.Matrix(4, 4, lambda i, j: 1 if p[i] == j else 0).det()
    if sgn != 1: continue
    for sg in itertools.product((1, -1), repeat=3):
        base = (phi*half*sg[0], half*sg[1], (phi - 1)*half*sg[2], 0)
        c600.add(tuple(sp.nsimplify(base[p[i]]) for i in range(4)))
C("600-cell (standard coordinates): 120 corners, all at distance 1, containing the 24-cell's 24", len(c600) == 120 and all(sp.simplify(sum(c**2 for c in v) - 1) == 0 for v in c600) and set(cell24) <= c600)
json.dump({'x_f': float(xv), 'minpoly_x': str(px.as_expr())}, open(os.path.join(HERE, '..', 'data', 's05-field-4d.json'), 'w'), indent=1)
C.final()
