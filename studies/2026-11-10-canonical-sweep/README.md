# Aim 2, chunk 2: the canonical form along the cube–octahedron sweep (10 Nov 2026; DICTO "yes 1 then 2")
S(μ) = cube [-1,1]^3 ∩ μ·octahedron (|x|+|y|+|z| <= 1); Hopscotch walls μ = 1, 2, 3; the turn μ ↦ 3/μ (fixed point √3).
scripts/canon_sweep.py (exact, sympy; compute-host) - FINAL ok.

1. BRIDGE CHECKED: the canonical form of S(μ) (positive-geometry formula: sum over a triangulation of the simplex forms
   <Z0Z1Z2Z3>^3 / prod <Y ...>, every simplex positively oriented) equals 3!·vol of the polar of S(μ) about the same point, exactly,
   at a generic point near the centre (1/97, 1/89, 1/83), in every chamber (7 samples). (Two faults fixed on the way: inner
   triangulation faces through the centre gave 0/0 - evaluate at a generic point; unoriented simplices gave a wrong sum.)
2. THE CANONICAL FORM AT THE CENTRE is one power of μ per chamber; the degree drops by one at each wall:
   Ω(S(μ); 0) = 3!·vol(S*) = 48/μ^3 (0<μ<1), 48/μ^2 (1<μ<2), 24/μ (2<μ<3), 8 (μ>3).
   Continuous, a KINK exactly at every Hopscotch wall and nowhere else; continued, no piece has a pole except μ = 0.
   So the walls of the sweep are exactly the non-smooth points of its canonical form: here the "poles meet the walls" in the form of
   kinks; the only pole is at μ = 0 (the collapsed octahedron).
3. vol(S)·vol(S*) (Mahler volume): 32/3 at both ends (the cube/octahedron equality case), 32(−2μ^3+9μ^2−9μ+3)/(3μ^2) on (1,2),
   16(μ^3−9μ^2+27μ−21)/(3μ) on (2,3); maximum at the root of 2μ^3 − 9μ + 6 = 0, μ = 1.631223, value 14.375086; NOT at the turn's
   √3 (14.290624); not symmetric under μ ↦ 3/μ (M(3/2) = 128/9, M(2) = 40/3). The turn does not act on these volumes.
DICTO 10 Nov during this step: "is it possible that the paradigm has the shape of a polyhedra"; "walls could be cell walls":
the #61 walls in the (s, λ) plane are lines (λ = −9s/8, −5s/8, −s/8, 3s/8 through the origin, and λ = −(4−s)/24): its chambers are
polygons - cells of a fan. NEXT: figure of the #61 chamber map; chunk 3 (the turn in canonical-form language); the icosahedral sweep.

## Aim 2, chunk 3: the turn in canonical-form language (12 Nov 2026; `scripts/canon_turn.py`, log `data/canon-turn.log`, FINAL ok)
Both sweeps S(μ) = P ∩ μ·P* of a polar pair: cube/octahedron (as in chunk 2) and, new, icosahedron (0, ±1, ±φ)/its polar
dodecahedron. Canonical form by Warren's vertex formula (fan over the dual polygon at a vertex on more than three facets).
Controls (all held, 39 checks): cube form 8/∏(1−y_i²); Warren = the chunk-2 triangulation formula at a generic point for μ = 1/2,
3/2, 5/2, 5 (octahedron end included); one dropped vertex term is caught; Ω(S;0) = 3!·vol(S*) exactly in all 8 chambers; odd orders
vanish and the order-2 term is isotropic; for the icosahedral group the order-4 term is isotropic too; a wrong turn μ ↦ 2/μ does not
fix the insphere point; cube walls = 1, 2, 3.

1. **The turn's fixed point is the insphere point (proved, any polar pair).** P = {a·x ≤ 1} with all facets at distance r and all
   vertices at distance R: the sweep runs from μ_lo = r² (S = μP*) to μ_hi = R² (S = P); the turn is μ ↦ r²R²/μ; S(μ) has all its
   facets at one distance exactly at μ = rR, its fixed point. Cube: 1, 3, turn 3/μ, fixed point √3. Icosahedron: μ_lo = (7+3√5)/6,
   μ_hi = (5+√5)/2, turn constant (25+11√5)/6, fixed point √((25+11√5)/6) = 2.875087.
2. **S(turn μ) is similar to S(μ) only at the fixed point** (exact, both sweeps). A similarity keeps the two facet types (6 vs 8, 20
   vs 12 facets), so it keeps the ratio ρ(μ) = μ/(rR) of their distances, and ρ(turn μ) = 1/ρ(μ). Since a canonical form determines
   its polytope (its poles are the facet planes), Ω(S(turn μ)) is never a turned or rescaled copy of Ω(S(μ)) except at μ = rR.
3. **The turn does not keep the walls.** Cube walls 1, 2, 3 go to 3, 3/2, 1; icosahedral walls (7+3√5)/6, φ² = (3+√5)/2,
   (5+√5)/2 go to (5+√5)/2, (5+2√5)/3, (7+3√5)/6. The ends swap; the middle (rectified) wall goes off the wall set in both.
4. **Ω(S;0), one power of μ per chamber (exact; the icosahedral sweep is new):** cube 48/μ³, 48/μ², 24/μ, 8 (chunk 2);
   icosahedron 20(3+√5)/μ³, 60(3−√5)/μ², 60(7−3√5)/μ, 12(25−11√5). Under the turn no weighted form μ^k·Ω(S;0), k = 0..3, is
   symmetric along the sweep; the only symmetric samples lie where μ and turn μ are both in the fixed point's own chamber, where
   μ^k·Ω is constant (cube k = 2 on (3/2, 2); icosahedron k = 1). Nothing more than that.
5. **Expansion at the centre** Ω(S(μ); t·u) = c0 + c2 t² + c4 t⁴ + …, anisotropy = difference between two axes at the first order
   where the group allows one. Cube (exact): c2/c0 = 10/(3μ²), (μ²+2μ+7)/(3μ²), (2μ²+2μ+3)/(3μ²), 1; order-4 anisotropy/c0 =
   −28/(9μ⁴), 2(μ⁴+2μ³+μ²−4μ−14)/(9μ⁴), (3μ⁴+2μ³−2μ²−8μ−12)/(9μ⁴), 1/3. It vanishes once on the sweep, at the root μ = 1.692590
   of μ⁴+2μ³+μ²−4μ−14 in (1, 2): near the fixed point √3 = 1.732051 but NOT at it. At √3: c2/c0 = (10+2√3)/9, anisotropy/c0 =
   4(√3−1)/81, slope 4/27 + 100√3/243 ≠ 0 (no extremum). Icosahedron (order 6; checked exactly at 5 rational μ per chamber, zeros
   and values in 40-digit arithmetic): the order-6 anisotropy changes sign once (400-point scan per chamber), at μ = 2.891793 in (φ², (5+√5)/2): again near the fixed
   point 2.875087 but not at it; at the fixed point c2/c0 = 0.778317, anisotropy/c0 = 0.000432, slope −0.0263.
**Conclusion.** In canonical-form language the turn's fixed point is special only as the insphere point (all poles of Ω at one
distance) and the one μ where S(turn μ) is a copy of S(μ); the turn is not a symmetry of the canonical forms, of their values at the
centre, or of the walls. The point where Ω is roundest (anisotropy zero) and the Mahler maximum (chunk 2, μ = 1.631) both fall
near the fixed point, not on it. Faults fixed on the way: the octahedron/icosahedron ends are not simple (fan over the dual polygon);
nested radicals defeated two exact comparisons (squares compared; unnormalised axes); exact one-fraction forms over Q(√5) did not
finish in 2 h (replaced by exact checks at sample μ plus a numeric scan); the first run's root filter missed the cube zero.
NEXT (chunk 4): the associahedron sanity case (bi-adjoint scalar amplitudes).

### Chunk 3, closed forms of the icosahedral numbers (12 Nov 2026; `scripts/canon_closed.py`, log `data/canon-closed.log`, FINAL ok)
In the chamber (φ², (5+√5)/2) every facet of S has b = 1 or b = μ, so each expansion coefficient is a polynomial in ν = 1/μ over
Q(√5), built exactly (controls: equal to the chunk-3 sums at μ = 27/10, 3, 7/2; values equal to the chunk-3 numbers to 1e-12;
minimal polynomials irreducible and vanishing to 1e-30; a perturbed polynomial does not vanish):
- Ω(S;0) = c0 = (420 − 180√5)·ν; c2 = (200 − 80√5)·ν·(ν² + (1 − √5/5)ν + 19/2 − 41√5/10) (along a unit axis);
- order-6 anisotropy (vertex axis minus face axis) = (640 − 128√5)/9 · ν · Q(ν), Q(ν) = ν⁶ + (1 − √5/5)ν⁵ + (−17/5 + 8√5/5)ν⁴
  + (−58/5 + 26√5/5)ν³ + (114/5 − 51√5/5)ν² + (−47/5 + 21√5/5)ν − 4698/5 + 2101√5/5;
- **the roundest point μ* = 2.891792659030825043 is 1/ν* for the root ν* of Q in (2/(5+√5), 1/φ²); over Q, μ* is a root of the
  irreducible 199μ¹² + 402μ¹¹ + 370μ¹⁰ − 1298μ⁹ − 8365μ⁸ − 26016μ⁷ − 47052μ⁶ + 52μ⁵ + 789μ⁴ − 670μ³ − 150μ² + 50μ + 25;**
- **at the turn's fixed point μ = √((25+11√5)/6): c2/c0 = 0.778317125037227435, root of 405x⁴ − 12960x³ + 107820x² − 105840x
  + 23024; anisotropy/c0 = 0.000431717368330967, root of 5189853515625x⁴ − 712524600000000x³ + 22113819590400000x² +
  81386864640000x − 39257636864** (both irreducible, degree 4).
So μ* is an algebraic number of degree 12, not the fixed point (degree 4: (6μ² − 25)² = 605) and not in Q(√5): the closeness of the
two is not an identity.
