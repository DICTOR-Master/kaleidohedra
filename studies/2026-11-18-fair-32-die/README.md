# The fair 32-face die: Lucky 7's sibling on the dodecahedron–icosahedron line (18 Nov 2026)

DICTO · dictospheres.com

**DICTO (18 Nov 2026):** "So is it part of a family", then "Yes". Prediction tested: the fair N-face member of a dual line carries the numbers of the regular (N/2)-gon (Lucky 7: 14 faces, the heptagon).

## Answer

- **The fair member exists.** It is D ∩ μI, with the dodecahedron's faces at 1 and the icosahedron's at μ_f = 1.0043619497034105611510248108974… It has 12 pentagons and 20 truncated triangles, and every face subtends 4π/32.
  - Faces: 12 regular pentagons, 20 hexagons with all angles 120° (truncated triangles).
  - Checks: every pentagon share = 1/32, every hexagon share = 1/32, total 1, symmetry check OK.
- **Like Lucky 7, it sits just past the equal-depth member.** The equal-depth member is at μ = 1, where all 32 faces touch one sphere (Lindelöf's roundest). The cube–octahedron line shows the same order: √3, then Lucky 7 at 1.7566.
- **The prediction holds for R².** Its circumradius squared is
  R² = 35 − 20√2 + 8√10 − 14√5 + (−40 + 30√2 + 16√5 − 12√10)·√(2+√2) = 1.182325095144630…
  - R² lies in Q(cos(2π/16), √5): the 16-gon's numbers together with the golden √5.
  - Its minimal polynomial is x⁸ − 280x⁷ + 10220x⁶ − 121800x⁵ + 483350x⁴ − 609000x³ + 255500x² − 35000x + 625. It is irreducible over Q and splits completely over Q(cos π/8, √5).
  - Lucky 7's analogue: R² = tan²(2π/7), in the heptagon's field Q(cos 2π/7).
  - r = 1 (the pentagons), so r/R = 0.919668996877…
- **Status.**
  - The value and the field come from 140-digit arithmetic: PSLQ found the polynomial, then sympy checked exactly that the closed form is a root of that polynomial.
  - That the polynomial is R²'s true minimal polynomial is certified numerically, not proved by hand. A hand proof, as for Lucky 7, is still to do.
  - μ_f's own minimal polynomial was not found up to degree 24 at 140 digits, which is consistent with degree 16. Do not quote a polynomial for μ_f.

## Fault caught (one fault, once)

The first run took the icosahedron in the wrong orientation relative to the dodecahedron. The triangle shares came out unequal, and the cube–octahedron control could not catch this because it is symmetric under that swap.

- Fixed: dual-aligned vertex sets.
- Guard: the script now stops with FAIL unless all faces of each family have equal solid angle.

## Files

- `scripts/fair_line.py co|di`: hull from the plane triples (double precision for the combinatorics, then 140-digit vertices), the Van Oosterom–Strackee solid angles, the root and PSLQ.
  - Control: `co` reproduces Lucky 7 (μ_f = 1 + √(2T) to 10⁻¹⁴¹, with minimal polynomials degree 6 and 3).
  - Output: data/co.log, data/di.log.
- `scripts/field_test.py`: factorisation over the fields (data/field.log).
- `scripts/exact_form.py`: the closed form of R² and its exact check (data/exact.log).
- All runs on a compute host, FINAL ok.

## LEADS

1. Hand proof of the R² identity, as Theorem 3A.1 (b) is for Lucky 7.
2. Does every face-transitive pair of a dual line follow the (N/2)-gon rule? The tetrahedron pairing is trivial: the octahedron.
3. Bouncing (lower faces more stable) moves both fair members. Test by printing and throwing.

## Part 2: more lines, and the rule tested (DICTO: "23 faces 18 faces 24 faces?", then "Run away!")

`scripts/fair_line2.py MODE` gives each line's fair member, with the scale-invariant (R/r)², its polynomial and a field test; `scripts/galois_check.py` tests whether it is abelian, that is, whether it lies in the field of some regular polygon (Kronecker–Weber).
- Control `co`: Lucky 7, (R/r)² = 19 − 8c − 32c² with c = cos 2π/7.
- Both scripts end FINAL ok (data/f2-*.log, data/galois.log).

| faces | line | μ_f (B faces at μ, unit normals) | (R/r)² minimal polynomial degree | polygon field? |
|---|---|---|---|---|
| 10 | tetrahedron ∩ cube | 1.065916595114… | 8 (6 real roots of 8) | **no**: mixed signature, not Galois |
| 14 | cube ∩ octahedron (Lucky 7) | 1.014163169041… (= 1.7566/√3) | 3 | **yes**: Q(cos 2π/7) |
| 18 | cube ∩ rhombic dodecahedron | 1.031250509130… | 6 (4 real roots of 6) | **no**: mixed signature |
| 20 | octahedron ∩ rhombic dodecahedron | 1.037024760344… | 4 | **yes**: splits over Q(cos 2π/10, √2) |
| 32 | dodecahedron ∩ icosahedron | 1.004361949703… | 8 | **yes**: Q(cos 2π/16, √5) |

Answer: every line has a fair member, but the polygon rule holds for 14, 20 and 32 faces only. For 10 and 18 the numbers belong to no regular polygon's field: the polynomial has both real and complex roots, so the field is not Galois. Why exactly these three is not yet understood (LEAD).
- 23 faces: impossible in symmetric families, since every face orbit has an even number of faces.
- 24 faces: not run.

The polynomials are found by PSLQ at 140 digits and certified numerically. The signature test (counting real roots) is exact once the polynomial is right.

## Part 3: the Vacuus of the fair dice (DICTO: "Is there a vacuus if not a polygon")

`scripts/vacuus_check.py` and `scripts/vacuus_axes.py` take one plate through the centre and each edge, then the angle of each plate normal to every symmetry axis, and test whether that angle is a rational multiple of π (PSLQ at 100 digits, denominator ≤ 200). Control: Lucky 7 shows 2π/7. Output: data/vacuus.log and data/vacuus-axes.log, FINAL ok.

| faces | sloping plates (off the mirrors) | kind | angle to a symmetry axis |
|---|---|---|---|
| 10 | 12 | single fins (1 edge each) | **7π/30** |
| 14 (Lucky 7) | 12 | 2 edges each | **2π/7** |
| 18 | 12 | 2 edges each | **5π/18** |
| 20 | 12 | 2 edges each | **π/5** |
| 32 | 30 | 2 edges each | **5π/16** |

The other plates of each die lie on the group's mirrors, at the familiar angles π/2, π/3, π/4, and so on.

Answer: every fair die has a polygon angle in its Vacuus, including the 10- and 18-face dice, whose lengths ((R/r)²) lie in no polygon field. So the polygon is always in the angles, and only in some cases in the lengths.

Reason, a conjecture not yet proved: fairness fixes each face's solid angle at 4π/N. By Girard's theorem the solid angle of the cone over a face is (sum of the angles between consecutive Vacuus plates) − (n − 2)π. So the plate angles are tied to rational multiples of π. Converting angles into lengths needs a square root, and that root stays inside a polygon field only for 14, 20 and 32 faces. The step from the dihedral angles to the axis angle still needs a proof.

LEAD: prove the axis-angle formula for each line, and explain the denominators 30, 7, 18, 5 and 16.

## Part 4: all eight axis lines (DICTO: "Are we sure there are no more")

The lines on which both face families sit on symmetry axes:
- cubic group: 6/8/12;
- tetrahedral group: 4 with 6 or 12;
- icosahedral group: 12/20/30.

Lines with off-axis faces form infinite families and were not run. Added here: `tr`, `dt` and `it`. The `it` run used a narrowed grid (argv 0.95 1.10 31). Output: data/f2-tr.log, f2-dt.log, f2-it.log, new-lines-axes-galois.log, it.txt.

| faces N | line | μ_f | hidden angle (sloping plates to an axis) | as a multiple of π/N | lengths (R/r)² in a polygon field? |
|---|---|---|---|---|---|
| 10 | T ∩ C | 1.06591660 | 7π/30 | 7/3 | no (not Galois) |
| 14 | C ∩ O (Lucky 7) | 1.01416317 | 2π/7 | 4 | yes |
| 16 | T ∩ RD | 1.06921054 | 5π/24 | 10/3 | no (not Galois) |
| 18 | C ∩ RD | 1.03125051 | 5π/18 | 5 | no (not Galois) |
| 20 | O ∩ RD | 1.03702476 | π/5 | 4 | yes (with √2) |
| 32 | D ∩ I | 1.00436195 | 5π/16 | 10 | yes (with √5) |
| 42 | D ∩ RT | 1.00726832 | 13π/42 | 13 | unknown (no polynomial up to degree 24) |
| 50 | I ∩ RT | 1.01558430 | 9π/50 | 9 | unknown (no polynomial up to degree 24) |

**Observed pattern** (8 of 8 lines; a conjecture, not proved):
- A fair N-face die hides the regular N-gon in its Vacuus: the sloping plates make a whole multiple of π/N with a symmetry axis.
- On the two tetrahedral lines the multiple is a third of a whole number, so they hide the 3N-gon.

The lengths follow a polygon field only for 14, 20 and 32 faces.

## Part 5 — the hidden angles proved by hand; every fair die in closed form (18 Nov 2026)
DICTO: "Try to find the rest and write a proof by hand please."
- scripts/corners.py: per face, the spherical corner angles of the face cone (angles between consecutive plates), Girard check
  (excess = 4pi/N on every face, all eight lines), and for every sloping plate its neighbours. Result (data/corners-*.log):
  on every line the A faces are regular m-gons (m = order of their axis), all corner angles alpha = ((m-2)pi + 4pi/N)/m,
  every sloping plate is an A-face edge plate whose neighbour round the A face is its own mirror image; B-B plates lie on mirrors.
- Hand proof (paper #111 Theorem 6): mirror through a corner bisects the corner angle, so the plate meets it at
  theta = alpha/2 = pi/2 - (N-2)pi/(mN). All eight PSLQ angles reproduced. kpi/N iff 2m | (m-2)N+4; tetrahedral lines N = 4 mod 6 -> pi/3N.
- scripts/exact_mu.py (Corollary 7): Napier, cos rho = cot(pi/m) cot theta; |corner| = tan(pi/m) tan theta; mu_f = b.a + (b.u) sqrt(tan^2(pi/m)tan^2 theta - 1).
  Agrees with the computed mu_f to 1e-90 on all eight; control Lucky 7 (1+sqrt(2T))/sqrt3 OK. data/exact-mu.log FINAL ok.
  First run FAILED on T∩RD only: the B-face normal was taken as the centroid direction, wrong on an irregular pentagon; fixed to the true plane normal, rerun FINAL ok.
- O∩RD: 3tan^2(pi/5) - 1 = (3 - sqrt5)^2, mu_f = (2sqrt2 + 3 - sqrt5)/(2sqrt3) exact.
- 42 and 50: exact closed forms now exist (degree search no longer needed); fields not determined.

## Part 6 — the mixed lines (DICTO 18 Nov: "have we really found them all?")
Enumeration: a fair member needs each family to be ONE orbit of the line's group (else 2 equations, 1 parameter).
Cube and icosahedron frames share Th (order 24) and T (12). Under Th: C, O, RD, D whole; I splits 8+12, RT 6+24. Under T: T, D whole.
New lines (fair_line2.py modes cd, od, td, rdd; all FINAL ok, SYMMETRY CHECK OK):
- C∩D 18 faces (Th) mu_f 1.0384442830, faces 4,6: squares are rectangles (cube axes only 2-fold in Th): no rational plate angle (corners-cd.log).
- O∩D 20 faces (Th) mu_f 1.0265315223, faces 3,7: theta = pi/5 (Theorem 6, rotations only); R/r = 8 - 3sqrt5 (PSLQ quadratic, 140 digits), mu^2 = (65-22sqrt5)/15.
- T∩D 16 faces (chiral T) mu_f 1.0603736500, faces 3,6: theta = 5pi/24; left and right hands.
- RD∩D 24 faces (Th) mu_f 0.9991525381 (< 1: first fair die inside the sphere), faces 7,4: no regular faces, no rational angle (corners-rdd.log).
Controls with a split family (ci C∩I 26, ort O∩RT 38, trt T∩RT 34): SYMMETRY CHECK FAIL at the A crossing = no fair member there (expected).
Trivial lines through face-transitive solids (T∩T' octahedron, O∩(I\O) icosahedron, ...) left out.
Corollary 7 closed form verified for od, td to 1e-90 (exact-mu-new.log FINAL ok); cd fails it as expected (rectangles).
Theorem 6 generalised: only the m rotations about the face axis are needed (regular spherical m-gon bisected by the plane through axis and corner).
Figures: fig_vacuus.py guards that the drawn axis views are m-fold symmetric (0 misses on all ten); the O∩D and T∩D views turn without a mirror.
Faults fixed: a hook-blocked command had silently dropped a fair_line2.py edit (KeyError 'cd'): reapplied and grep-verified before running;
a brace glob in scp failed and skipped this README entry: refetched file by file.
