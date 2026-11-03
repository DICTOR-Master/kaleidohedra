# Referee report: draft #91, Main Theorem (a) and (b)

Scope: Main Theorem (a) (Lemma 1) and (b) (tesseract × 16-cell), Section 3, with the proof and the s5 checks. Own exact recomputation on dicto-big-brother (sympy): vertices of K ∩ μK* derived from the 24 halfspaces at μ = 5/4, 3/2, 2, 9/4, 5/2, 27/10, 3, 7/2, φ², 2 + 1/φ²; cells and corner matching by explicit construction in the same frame.

## Verdict

(a) **correct.** (b) **correct, with small fixes** (wording and one placeholder check; no mathematical error).

What I confirmed exactly:
- Corners of S(μ) are the signed permutations of (1, μ−1, 0, 0), (1, 1, μ−2, 0), (1, 1, 1, μ−3) on the three open intervals; 48, 96, 64 corners; 24 three-dimensional cells (8 cube-facet + 16 on facets of μK*) at every μ in (1, 4), integers 2 and 3 included.
- 2 < μ < 3: cube-facet cell = C ∩ λO, λ = μ−1, corners (1, λ−1, 0): the octahedron cut at x = (λ−1)/λ; hexagon ratio corner/original = (λ−1)/(2−λ). Golden iff λ = φ (ratio φ, Greater = Icosaxes) or λ = 3−φ (ratio 1/φ, Lesser = Unborn Axes), matching #88 Table 2 and #90 Table 2.
- 16-cell-facet cell = slice of the unit 4-cube at level μ; corners (1, 1, h, 0), h = μ−2; tetrahedron cut at x = (1−h)/(2−h), ratio (1−h)/h. Golden iff h = 1/φ² (Greater) or h = 1/φ (Lesser), matching #89 Main Theorem (a).
- The two solution sets coincide: {1+φ, 4−φ} = {2+1/φ, 2+1/φ²}. Labels as stated: φ² → Icosaxes + Lesser GCT; 2+1/φ² → Unborn Axes + Greater GCT. Shared hexagon has sides √2·h and √2·(1−h), so the ratio flips between the two cells.
- 1 < μ < 2: cube cells are regular octahedra (λ < 1); tetrahedral cells cut at (μ−1)/μ, golden at μ = φ (Greater) and 3−φ (Lesser), as the text says. 3 < μ < 4: tetrahedral cells regular; cube cells are cut cubes with octagon ratio (1−t)/(√2 t), t = μ−3, golden at μ ≈ 3.3041, 3.5336, both of degree 4 (√2 enters). μ = 2 gives the 24-cell (24 octahedra), μ = 3 the rectified tesseract. So no other μ in (1, 4) is all-golden.
- Lemma 1: μ = v·v − x(v·v − v·w) = R² − xe²/2 is right; endpoints x = 0, 1/2 and the dual end check. The s5 corner matching (`similar`) is a true corner-to-corner bijection verified exactly on all pairwise distances.

## Errors and gaps (numbered)

1. **Proof (b), paragraph 3, cube cells.** The cut fraction is never stated; the reader must get x = (λ−1)/λ from "corners (1, λ−1, 0)". Fix: add "the plane x₁ = 1 meets the edge from (λ, 0, 0) to (0, λ, 0) at fraction x = (λ−1)/λ, so by Lemma 1 for the octahedron (R = 1, e = √2: 1/λ = 1 − x) and #88, x = 1/φ² gives λ = φ and x = 1/(φ√5) gives λ = 3 − φ."
2. **"Only if", same paragraph.** "Neither is a golden cut" for regular cells uses that a golden cut has x > 0 (#88 Theorem 2: both roots in (0, ½)). Say so in one clause; otherwise a regular octahedron could be read as the cut x = 0.
3. **Statement (b), "μ not an integer".** The count 24 holds at μ = 2 and 3 as well (24-cell; rectified tesseract); only μ = 1, 4 lose cells. Either drop the restriction from the count and keep it only for "cut" cell types, or say "1 < μ < 4" and note the integer points are the 24-cell and the rectified tesseract, not golden. The "exactly when" is then proved on the whole open interval.
4. **Lemma 1 range.** The formula is a corner cut only for 0 < x ≤ ½ (ρ² ≤ μ ≤ R²); beyond ½ the planes pass the edge midpoints and S(μ) is a cut of P*, not "P cut at x". Add the range.
5. **s5, line "hexagons swap the roles" (`check(..., True)`).** This is a hardcoded pass, not a computation, yet the paper says "(s5, exact)" for the local reason after the proof. Fix: compute the shared hexagon's sides (√2·h, √2·(1−h)) or drop "(s5, exact)" for that sentence.
6. **s5 `t16_vertices`** asserts the corner set (signed permutations) rather than deriving it from the 24 inequalities; only the float `fsection` derives it. Not an error (I derived it exactly, it agrees), but the data note should say "corner set assumed, checked in floating point".

## Wording that overclaims

- "which proves (b)" after the coincidence proves only the "if" direction; the "only if" is the three preceding sentences. Say "the two golden sets coincide, which with the preceding gives (b)".
- Nothing else in (a) or (b) overclaims. The theorem's reliance on #88, #89 Main Theorem (a) and #90 Table 2 is correct as cited.
