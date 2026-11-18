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
