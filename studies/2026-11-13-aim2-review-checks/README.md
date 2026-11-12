# Aim 2 paper: checks for the referee revision (13 November 2026)

Exact and numerical checks of statements added or reworded in "Geometry Gives Laws" after the hostile referee review.
Run on the compute node with Python 3 (sympy, numpy, scipy), 2 cores, 3 GB cage; pilot `data/revcheck-pilot.log`, full run `data/revcheck.log`, FINAL ok.

| check | what | status |
|---|---|---|
| R1 | Cube line: S(2) = cuboctahedron, its polar the rhombic dodecahedron (vol 2, Ω = 12); S(2)^∨ = S(3/2) is the **uniform truncated octahedron** (one edge length; the referee wrote "truncated cube"); the bridge polytope S(μ)° is the hull of the facet feet of S(μ)^∨, so Ω(S(μ); 0) = 3!·h^−6·vol(feet hull of S(c/μ)) at μ = 6/5, 3/2, 5/2, 14/5 = Table 1 | exact |
| NEG R1 | S(5/3) has two edge lengths; outside h² ≤ μ ≤ R² (μ = 1/2) the feet-hull relation fails (384 against 8): it is stated for the Turn Theorem's range only | exact |
| R2 | vol((P − y)°) = ∫ over P° of (1 − x·y)^−(d+1) dx: cube against octahedron, Taylor coefficients equal through order 6; NEG exponent −3 fails | exact |
| R3 | 600-cell line: Table 1 continuous at both middle walls; outer chambers Ω = 75(√5 − 1)/μ⁴ (μ < r²) and 1440(47√5 − 105) (μ > 1); turn images of the middle walls (5 + 2√5)/10 and (9 + 3√5)/16, not walls | exact |
| R4 | Chamber monomial: in every chamber of the cube, icosahedral and 600-cell lines each corner of S(μ) is a transversal meet, facet normals of rank d − j and corner normals of rank j, j = the power of 1/μ in Table 1; NEG at the wall μ = 2 the ranks add to 4 > 3 | numerical (tolerance 1e-7 / 1e-9) |
| R5 | Alternate-sector lemma: m = 3, 5, 7, 9 lines, sum of in-sector cone forms 0; all 2m sectors sum to 0; a cone and its antipode have one form; m = 2 gives twice one cone (point residue ±2); NEG one sector swapped is nonzero | exact |

Faults on the way (fixed, recorded): (1) R4 first counted active corner planes, not their rank: the octahedron corner inside the cube lies on 4 planes of rank 3; the statement is about the rank (the number of corner-type vertices in every simplex of the polar facet). (2) The 4D facet offset was read from the wrong column of qhull's equations (inradius 0.572). (3) Vertex enumeration of the 600-cell line by qhull (halfspace intersection, and the polar hull) gave spurious corners where corners are not simple; replaced by the flag corner of each chamber with all 720 constraints evaluated there. (4) R1 at μ = 1/2 and 4 failed: outside [h², R²] one facet type is absent, so the feet-hull form of the Turn Theorem holds only inside; kept as a negative control.

Used in the paper: §2 (the bridge and the turn), Proposition 4 and its proof (chamber monomials, moment identity), Proposition 5 (600-cell turn images), Table 1 (outer chambers), Theorem 3 (i) (the alternate-sector lemma for odd m, also m = 9 at the point at infinity).
