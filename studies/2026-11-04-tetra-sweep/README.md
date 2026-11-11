# Tetrahedron sweep and the roundness column (4 Nov 2026) — Concordance 6.1 gaps, methods combined

DICTO 4 Nov: "try recorded concordance gaps with interesting leads, and a combinatory approach of new and current methods".
Row 3 of the tests × families grid (tetrahedron sweep T ∩ μ(−T)) had only the harmonic test; the 4D sweep had no roundness or Mahler entry.
Scripts on compute-host (~/study-runs/2026-11-04-tetra-sweep, python3); data/ holds every output.

## 1. Tetrahedron sweep: three outside tests (scripts/measures.py, data/measures.json)
T = {−v·x ≤ 1}, −T = {v·x ≤ 1}, v the corners of a regular tetrahedron; μ ∈ (1/3, 3); octahedron at μ = 1; S(1/μ) = −S(μ)/μ (symmetry μ ↔ 1/μ).
For 1 ≤ μ ≤ 3 the corner cut is t = (3 − μ)/4 of the edge.
- Isoperimetric: V ∝ 1 − 4t³, A ∝ 1 − 2t²; d log IQ/dt = 12t(1 − 2t)/((1 − 4t³)(1 − 2t²)) > 0, so the maximum is exactly at the octahedron (the symmetry's fixed point).
- Mahler: polar volume 8/μ exactly; f(μ) = 4(μ³ − 9μ² + 27μ − 11)/(3μ). Ends 64/9 (tetrahedron, the conjectured minimum for all convex bodies), octahedron 32/3
  (a local MINIMUM here), maxima at μ* = (11 − √33)/4 ≈ 1.3139 (root of 2μ² − 11μ + 11, from 2μ³ − 9μ² + 11 = (μ + 1)(2μ² − 11μ + 11)) and 1/μ*; f ≈ 11.3723. No named station.
- Dehn: 6 hexagon–hexagon edges (1 − 2t)a at α = arccos(1/3), 12 hexagon–triangle edges t·a at π − α: Dehn = 6a(1 − 4t) ⊗ α. ZERO exactly at t = 1/4, μ = 2 (and μ = 1/2).
  Checked from the hull (coefficient 0 at μ = 2; −5.66 at the Archimedean truncated tetrahedron μ = 5/3).

## 2. The Dehn-zero member tiles space (scripts/tile_octet.py, corona.py, verify_tiling.py)
S(2) = T(4) minus its four corner T(1). It is a union of octet-honeycomb cells: 16 + 4 tetrahedra and 10 octahedra. T(n) minus corners has (n − 4) more tetrahedra
than twice its octahedra (second difference of C(n,3)), so the octet's 2 : 1 ratio holds only at n = 4: the density condition and Dehn zero pick the same member.
- Exact cover of the octet cells on periodic tori fcc/L (all Hermite-normal-form sublattices; count checked against Σ b c²). Controls: rhombohedron tiles at N = 1; a lone tetrahedron never.
- Result: a periodic tiling at index N = 20, two pieces per period (the piece and its point inverse), L = B·[[10,1,4],[0,2,1],[0,0,1]].
  Independent check with real polytopes: 2 × 20 = 40 = period volume; no overlaps among 18,489 nearby pairs (separating axes); coverage: all 15,512 random points within radius 5.9 lie in exactly one copy
  (the 162 misses all lie beyond 5.9: copies needing lattice coefficients > 7 in the skewed basis were not generated — window artefact, scripts/diag_gaps.py).
- Local patches (corona.py) close to radius 12 (≈ 360 pieces) with almost no backtracking: the tiling is nearly forced.
- Bug found and fixed on the way: the first HNF enumeration used wrong off-diagonal ranges (right count, wrong lattices), so N = 20 was first reported empty.
- PRIOR ART (library, read): this tiling is KNOWN — Damasceno, Engel & Glotzer, ACS Nano 6, 609 (2012) (truncated tetrahedra, β-tin structure);
  Gabbrielli, Jiao & Torquato, PRE 86, 041141 (2012), Fig. 15: "chopping the four corners ... edge length 1/4 ... each truncated tetrahedron contains 20 tetrahedra and 10 octahedra".
  Ours: the Dehn screen on the sweep picks out exactly this tiler (as it picks Kelvin on the cube–octahedron sweep), and Dehn zero = octet density at n = 4. Not a new tiling.

## 3. Roundness on the n-dimensional sweep: μ = √n (scripts/sweep4d.py, sqrt_n.py)
Prediction from 3D (√3) tested in 4D: the isoperimetric maximum of [−1,1]⁴ ∩ {|x|₁ ≤ μ} is at μ = 2, the 24-cell (IQ = V³/A⁴ = 2⁻¹¹ exactly). Mahler maximum ≈ 16.7466 at μ ≈ 2.2837
(no station; 16 at the 24-cell; 32/3 at both ends = 16 × 2/3, the tesseract–16-cell product).
Exact for n = 2 … 12 (Irwin–Hall formulas): d log IQ/dμ = 0 at μ = √n, and it is the global maximum. n = 2: the regular octagon.
EXPLANATION (classical): at μ = √n every facet, cube and cross-polytope, is at distance 1 — the polytope is circumscribed about the unit ball — and by LINDELÖF'S THEOREM
(1869; Fejes Tóth) the isoperimetric optimum among polytopes with given facet normals is the one circumscribed about a ball. Same reason for the octahedron on the tetrahedron sweep,
and for NO station on the CO–RD sweep (the CO's facets never all touch one sphere).
CORRECTION for the record: the "exact √3 coincidence" (mahler-sweep, #94 v2 draft, Concordance waiting list) is Lindelöf's theorem, not a new coincidence;
the core turn μ ↔ 3/μ has √3 as fixed point for the same reason (it swaps the two facet distances). Wording in #94 v2 must say so.

## Q6 on the tetrahedron sweep (scripts/tetra_q6.py)
m = 0 coefficient about the 3-fold axis (the cubic l = 6 invariant is one-dimensional, so a zero would be a sign change): Q4 changes sign once, μ ≈ 1.8055 (and 1/μ); Q6 never — the sweep is never silent in degree 6.

## Reformulation (4 Nov): the Dehn-zero truncated tetrahedra are exactly P(t) = T ∩ (2(−T) + t)
Cut c_i = (3 − μ_i)/4 with planes v_i·x ≤ μ_i; the four planes bound an inverted tetrahedron of size fixed by Σμ_i (Σv_i = 0); Σc = 1 ⇔ Σμ = 8 ⇔ cutter = 2(−T).
So the family is one translation parameter t. Conjecture: P(t) tiles with −P(t) for all admissible t (6/6 lattice cases do, 2 per period).
