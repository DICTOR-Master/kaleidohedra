# CsCl and zinc blende: #53 Observation 2 proved (2026-11-09)

**Conclusion.** #53 Observation 2 is **true exactly**, on all three intervals and for both kinds. The reason is one lemma: the zinc blende unlike face is the CsCl unlike face scaled by −2 (Theorem E). Both faces are slices of a cube by the same power plane. The flips ±1 and the ends ±3 are where that plane passes the cube's corners. The volumes then follow from the weight derivative of a power cell, and the like faces follow from the pyramid formula. The hole types play no part.

**Status: PROVED** (Theorem E and Corollary F; 95/95 exact checks, `scripts/obs2_proof.py`, FINAL ok). **REFUTED**: lead 1 of the switch-theorem study ("scaled circuits"): the flip circuits of the two networks differ, and scaling moves the flips. **PARTIAL, closer**: #53 Observation 3. Proposition D gives the like-bond births directly from the sites, as one linear programme per like pair, and the walk type is the sign of τ_A + τ_B. For centrosymmetric pairs the value has a closed form (the midpoint rule). Checks: `scripts/likebirth.py`, see the table below. A closed rule that reads the type off the symmetry or the hole type alone is still open.

DICTO proposed the two DICTONIC loops, the web of bonds and the question behind #53's observations (#53 §5–6). DICTO chose this gap on 9 November 2026. Computation, proofs and drafting were done with Claude (Anthropic).

## Set-up (the units of #53, Table 1)

- **CsCl:** big sites B = 2ℤ³ (kind A, weight λ), small sites 2ℤ³ + (1,1,1) (kind B, weight 0).
- **Zinc blende:** Zn = 2D₃ = {2k : k ∈ ℤ³, k₁+k₂+k₃ even} (kind A, weight λ), S = 2D₃ + (1,1,1) (kind B, weight 0).
- Both networks have the range (−3, 3). Write s = (3 + λ)/2. The zinc blende sites are half of the CsCl sites. The other half, (2,0,0) + zinc blende, is a translate of zinc blende.

## The statement in #53 (Observation 2, verbatim)

> On each of the three intervals (−3, −1), (−1, 1) and (1, 3), every bond-face area and every cell volume in zinc blende is the same polynomial in λ as in CsCl up to a constant factor: unlike faces 4 times larger, like faces 1/√2 times, volumes twice; the flips (±1) and the ends (±3) are the same. For example, on (−1, 1) the like bonds have area (1 ± λ)²/(2√2) in zinc blende against (1 ± λ)²/2 in CsCl, and the unlike bonds √3(3 − λ²) against (√3/4)(3 − λ²). The face counts differ (16 against 14 on (−1, 1)). [...] We have no explanation of the coincidence.

## Theorem E (the unlike faces are homothetic)

**(i) The cells.** For −3 < λ < 3:
- The CsCl big cell at 0 is P_C(s) = {|x|₁ ≤ s, |xᵢ| ≤ 1}, an octahedron cut by a cube. The small cell at (1,1,1) is (1,1,1) + P_C(3 − s).
- The zinc blende Zn cell at 0 is P_Z(s) = {q·x ≤ s for q ∈ Q, |xᵢ ± xⱼ| ≤ 2}, a tetrahedron cut by a rhombic dodecahedron, with Q = {(1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1)}. The S cell at (1,1,1) is (1,1,1) − P_Z(3 − s).

**(ii) The unlike faces.** The CsCl face between big 0 and small (1,1,1) is

  F_C(s) = {x₁ + x₂ + x₃ = s, 0 ≤ xᵢ ≤ 1},

which is the slice of the unit cube [0,1]³, spanned by the two bonded sites, by the power plane. The zinc blende face between Zn 0 and S (1,1,1) lies in the same plane and is

  F_Z(s) = {x₁ + x₂ + x₃ = s, s − 2 ≤ xᵢ ≤ s} = s(1,1,1) − 2·F_C(s).

So F_Z is F_C scaled by −2 about the foot (s/3)(1,1,1) of the bond, for every λ in the range. Area(F_Z) = 4·Area(F_C).

*Proof.*
- (i), CsCl, by hand. The planes of P_C come from the 8 nearest small sites and the 6 nearest big sites, so the cell lies in P_C. Conversely, take x ∈ P_C. For a big site 2k, |x − 2k|² − |x|² = 4Σ(kᵢ² − kᵢxᵢ) ≥ 4Σ(kᵢ² − |kᵢ|) ≥ 0. For a small site m (odd coordinates, aᵢ = |mᵢ| ≥ 1), x·m ≤ Σ|xᵢ|aᵢ ≤ s + Σ(aᵢ − 1). This is at most s + Σ(aᵢ² − 1)/2 = (|m|² + λ)/2, because (aᵢ − 1)² ≥ 0. So no site cuts P_C.
- (i), zinc blende, by an exact finite check (C2). The 16 nearest planes give a polytope whose corner set is constant on each open interval: every triple of planes keeps its feasibility. Every site within a proved-safe radius satisfies every corner at both closed ends of the interval. The slacks are affine in λ, so they are non-negative on the whole interval. Sites beyond the radius cannot cut the cell, since (|p| − R)² ≥ R² + |λ|.
- The B cells follow from the symmetries x ↦ (1,1,1) + x (CsCl) and x ↦ (1,1,1) − x (zinc blende). Both exchange the kinds and send λ to −λ (C3).
- (ii) On the plane Σxᵢ = s, the constraint |x|₁ ≤ s is equivalent to xᵢ ≥ 0, and |x − (1,1,1)|₁ ≤ 3 − s is equivalent to xᵢ ≤ 1. In zinc blende, the Zn planes q·x ≤ s give xᵢ ≤ s, and the Zn–Zn planes xⱼ + xₖ ≤ 2 give xᵢ ≥ s − 2. The S planes give the same two bounds. The remaining planes are implied. ∎

## Corollary F (#53 Observation 2)

On each interval, and for each kind:

| quantity | zinc blende / CsCl |
|---|---|
| each unlike face | 4 |
| each cell volume | 2 |
| each like face | 1/√2 |

The flips (±1) and the ends (±3) are the same in both networks.

*Proof.*
1. **Flips and ends.** The like and unlike faces change type exactly when the plane Σx = s passes corners of [0,1]³:
   - s = 1 and s = 2 give λ = ∓1;
   - s = 0 and s = 3 give λ = ∓3.

   The corner sets of both cells are constant on the three intervals (C2), and F_Z changes with F_C.
2. **Volumes.** For a power cell, dV_A/dλ = Σ over unlike faces of area/(2d). Like bisectors do not move, because like sites carry equal weights. Each unlike plane moves at rate 1/(2d), and dV/dh_f equals the area of face f. Both networks have d = √3.
   - CsCl: 8 faces of area a(λ).
   - Zinc blende: 4 faces of area 4a(λ), twice the sum.

   V_A → 0 as λ → −3 in both, so V_Zn = 2·V_big on (−3, 3). For B, use the same argument from λ = 3.
3. **Like faces.** Apply the pyramid formula 3V = Σ h_f·A_f to the A cell. The unlike height is h_u = (3 + λ)/(2√3) in both networks. The like heights are 1 (CsCl, 6 faces) and √2 (zinc blende, 12 faces). The site symmetry group (m3̄m, resp. 4̄3m) acts transitively on the like neighbours, so all like faces of a cell are congruent. Then

   12·√2·A_like(Zn) = 3·V_Zn − 4·h_u·A_un(Zn) = 2·(3·V_big − 8·h_u·A_un(big)) = 2·6·1·A_like(big),

   so A_like(Zn) = A_like(big)/√2. ∎

The numbers on each interval (exact; identical to #53's census polynomials, C5):

| interval | kind | unlike face, CsCl | ratio | like face, CsCl | ratio | volume, CsCl | ratio | faces (unlike + like) CsCl / ZnS |
|---|---|---|---|---|---|---|---|---|
| (−3, −1) | A | √3(λ+3)²/8 | 4 | — | — | (λ+3)³/6 | 2 | 8+0 / 4+0 |
| (−3, −1) | B | √3(λ+3)²/8 | 4 | −(λ²+6λ+1)/2 | 1/√2 | −(λ³+9λ²+27λ−21)/6 | 2 | 8+6 / 4+12 |
| (−1, 1) | A | (√3/4)(3−λ²) | 4 | (1+λ)²/2 | 1/√2 | −(λ³−9λ−12)/3 | 2 | 8+6 / 4+12 |
| (−1, 1) | B | (√3/4)(3−λ²) | 4 | (1−λ)²/2 | 1/√2 | (λ³−9λ+12)/3 | 2 | 8+6 / 4+12 |
| (1, 3) | A | √3(λ−3)²/8 | 4 | −(λ²−6λ+1)/2 | 1/√2 | (λ³−9λ²+27λ+21)/6 | 2 | 8+6 / 4+12 |
| (1, 3) | B | √3(λ−3)²/8 | 4 | — | — | −(λ−3)³/6 | 2 | 8+0 / 4+0 |

The like faces are not similar. On (−1, 1) the CsCl like face is a square and the zinc blende like face is a triangle with apex (1,1,−1), which is a CsCl small site missing from zinc blende. Only their areas are proportional, and that proportionality is forced by the volume and unlike-face identities. The unlike faces are genuinely homothetic.

**On #53's remark about holes.** The remark is correct (the tetrahedral hole of fcc is the shallow hole; Conway–Sloane ch. 4) but irrelevant. What matters is that in both networks each unlike bond is the long diagonal of a cube whose corners carry the like neighbours, at scale 1 in CsCl and scale 2 in zinc blende. The power plane slices both cubes. The factor −2 is the scale and the reversal of the cube's orientation.

## The switch-theorem view (Theorem A tools; brief's hypotheses)

- **Scaled circuits: no.** Scaling the CsCl sites by 2 multiplies S₀ by 4 and leaves S_A unchanged, so the flips move to λ* = ±4 (C9). The coincidence holds at the same λ, so it is not a scaling of circuits.
- **Shared circuits: no.** Every zinc blende circuit is a CsCl circuit with the same S₀/S_A, because the coordinates and kinds are the same. But the empty spheres differ:
  - The zinc blende dual cell at λ = −1 is centred at (1,−1,1), a CsCl small site missing from zinc blende. Its power sphere holds 4 Zn and 6 S, with power 4, while that missing site has power 0 there.
  - At λ = +1 the dual cell is centred at the missing big site (2,0,0), where the sphere power is 3 and the missing site's power is −1.

  So neither sphere is empty in CsCl. Conversely, none of the 48 CsCl dual cells at λ = ±1 lies inside the zinc blende sites (C9). The two networks reach the same flip values through different circuits. What they share is the face lemma: in both, the flips are the λ at which the power plane passes the corners of the unit cube.
- **One family between them.** Theorem E does not need one. A two-weight family is possible: give the removed half a weight lowered by μ, so that μ → ∞ deletes it. It is not needed for the proof and was not computed (LEADS 3).

## Proposition D (#53 Observation 3: the like-bond births from the sites)

For a site a of kind K let f_a(x) = max over unlike sites b of (|x − a|² − |x − b|²). Each term is affine in x. Let U_a(ℓ) = {f_a ≤ ℓ}, the cell a would have against the unlike sites alone. Put

  τ_K = min over like pairs (a, a′) of min_x max(f_a(x), f_a′(x)),

one linear programme per pair. Then, inside the open range:
- A–A bonds exist exactly for λ > τ_A;
- B–B bonds exist exactly for λ < −τ_B;
- the hand-over is **gradual iff τ_A < −τ_B** and **a single switch iff τ_A = −τ_B**;
- τ_A > −τ_B never happens.

*Proof.* If the U_a have pairwise disjoint interiors, then each A cell equals its U_a. Its facets all lie on unlike planes and it is contained in U_a, so it equals the intersection of their halfspaces, which contains U_a. So there are no A–A facets. Conversely, if two U's overlap in an open set, the A cells there share an A–A facet: points with π_a′ < π_a lie in the interior of both U's. Each U_a grows with λ, so the births are monotone. A value τ_A > −τ_B would give an open interval of switch points, but switch points are flips (Theorem B), and flips are finite in number. ∎

**Midpoint rule.** If the midpoint m of a like pair is a centre of symmetry of the two-kind site set, the pair's value is ℓ²/4 − δ², with ℓ the like distance and δ the distance from m to the nearest unlike site. The proof uses convexity: averaging a minimiser with its image gives m. In zinc blende the midpoints are not symmetry centres, and the minimiser (−1,−1,−1) is again a missing CsCl site.

Results (exact LP certificates; the pairs that can matter are bounded by ℓ²/4 − R² ≤ τ, with R the covering radius of the unlike sites):

| network | range | τ_A | τ_B | τ_A + τ_B | type (τ) = type (walk) | midpoint rule |
|---|---|---|---|---|---|---|
| square + centres | (−2, 2) | 0 | 0 | 0 | switch at 0 | 8/8 pairs |
| honeycomb + centres | (−1, 1) | −1/2 | 1/2 | 0 | switch at −1/2 | 12/12 |
| kagome + centres | (−1, 1) | −1 | 1 | 0 | one like bond (−τ_B = −1 is the range end) | 6/6 |
| CsCl | (−3, 3) | −1 | −1 | −2 | gradual on (−1, 1) | 12/12 |
| fluorite | (−3/8, 3/8) | −1/8 | 1/8 | 0 | switch at −1/8 | 96/96 |
| rock salt | (−1, 1) | 0 | 0 | 0 | switch at 0 | 96/96 |
| zinc blende | (−3, 3) | −1 | −1 | −2 | gradual on (−1, 1) | no symmetric pair; minimiser (−1,−1,−1), a missing CsCl site |
| hcp holes | (−11/24, 3/8) | −11/24 | −5/24 | −2/3 | gradual on (−11/24, 5/24) | no symmetric pair |
| A15 | (−5/4, 5/4) | 1/4 | −3/4 | −1/2 | gradual on (1/4, 3/4) | 24/24 |
| C15 | (−11, 11) | −5 | −9 | −14 | gradual on (−5, 9) | 32/32 |
| h-BN (control) | (−1, 1) | 0 | 0 | 0 | switch at 0 | no symmetric pair |
| sodalite (control) | (−2, 2) | 0 | 0 | 0 | switch at 0 | 24/24 |

All 12 τ values equal the like-bond births and deaths of the exact walks; τ_A + τ_B ≤ 0 everywhere, with equality exactly at the switching networks (kagome: equality at the range end, a degenerate case with one like bond).

This changes the status of Observation 3. The type is now read from two numbers computed from the sites, without walking λ, and in the centrosymmetric cases from distances alone (ℓ²/4 − δ²). It is a finite criterion that comes from the sites, but not yet a rule that predicts the type from symmetry or hole type.

## Checks

| Script | What | Result |
|---|---|---|
| `scripts/obs2_proof.py` | C1 sanity (fluorite octet −1/8; CsCl and zinc blende flip circuits ±1); C2 cells = nearest-neighbour polytopes on each interval (exact); C3 symmetries; C4 Theorem E (−2 homothety, cube slice); C5 every face and volume = #53 census; C6 the ratios 4, 1/√2, 2; C7 the two identities; C8 #53 engine corners = ours at 7 λ; C9 circuits and scaling | **95/95 PASS**, FINAL ok |
| `scripts/likebirth.py` | Proposition D on the 12 networks: τ_A, τ_B by exact LP, against the walks' bond lives; τ_A + τ_B ≤ 0; midpoint rule on inversion-symmetric pairs | **33/33 PASS**, FINAL ok (about 10 min) |

All arithmetic is exact (Fractions, sympy). Floats only order polygon corners, propose LP vertices and size the search radius, with a margin. Heavy runs were done on the research computer with `~/geom/bin/python`. Data: `data/obs2.json`, `data/obs2-checks.txt`, `data/likebirth.json`, `data/likebirth-checks.txt`, `data/likebirth-stdout.txt`.

## Findings on #53

- **No numerical error.** Every polynomial in Observation 2 is exact, including (1 ± λ)²/(2√2), √3(3 − λ²) and the factor 2 on volumes.
- **Incomplete wording.** "The face counts differ (16 against 14 on (−1, 1))" is right. On the outer intervals the counts are 4 against 8 for the vanishing kind and 16 against 14 for the other.
- **"Every bond-face area … the same polynomial"** holds face by face. But only the unlike faces are similar figures; the like faces are a square or octagon in CsCl against a triangle or pentagon in zinc blende.
- **The hole remark** is correct but not the reason. "No explanation" can now be replaced by Theorem E.
- **The Remark's wording** "the points 2(a, b, c) of 2ℤ³ with a + b + c even" is clear enough; "2D₃" is right.

## Prior art (sources checked)

- **Standard and used:**
  - The weight derivative of a power-cell volume (face area over twice the distance). Aurenhammer, Hoffmann and Aronov, "Minkowski-type theorems and least-squares clustering", *Algorithmica* 20 (1998) 61–76, cited from memory and not re-read. The same derivative appears in the semi-discrete optimal transport literature (web query result: arXiv:2409.07873, abstract page). Edelsbrunner–Koehl, "The weighted-volume derivative of a space-filling diagram", PNAS 100 (2003) 2203 (ISTA record page, abstract only).
  - The pyramid formula and dV/dh_f = area (Minkowski).
  - Deep and shallow holes of D₃: Conway–Sloane, *SPLAG*, ch. 4, as in #53 [18].
- **DICTO's reference library** (`~/kaleidohedra-references`, semantic search with `ask-library` and a text grep of its manifests and INDEX). Semantic queries:
  - "power diagram of zinc blende and caesium chloride, cell volumes as functions of the weight";
  - "derivative of power cell volume with respect to weights equals face area over distance";
  - "radical tessellation of binary crystal structures CsCl NaCl ZnS";
  - "Voronoi cell of diamond lattice triakis truncated tetrahedron".

  Grep terms: zinc blende, sphalerite, CsCl, caesium/cesium chloride, radical, Laguerre, power diagram, Minkowski, face area, derivative, Aurenhammer, Hoffmann, semi-discrete, tetrahedral hole. Relevant hits, none stating the CsCl–zinc blende relation:
  - Wang et al. 2018 (DEM binary crystals, radical tessellation) and Richard–Oger–Troadec–Gervois 1998 (binary assemblies), title and abstract only;
  - Leunissen et al. 2005 (CsCl Voronoi constructions of colloids), page snippet;
  - Koca et al. 2018 (Voronoi and Delaunay cells of W(D_n)), title;
  - Koca et al. 2020 (deep and shallow holes, citing Conway–Sloane), page snippet;
  - Gabbrielli–Jiao–Torquato 2012, page snippet;
  - several semi-discrete optimal transport titles, and Nielsen 2026 on power distances.
- **Web queries (2):** "power diagram derivative of cell volume with respect to weight equals face area divided by twice distance"; "radical tessellation zinc blende CsCl cell volume as function of radius ratio". The second returned only textbook radius-ratio pages.
- **Also re-read for this study:** #53 §5 and the relay-census README "4. Zinc blende" and prior-art notes, and the switch-theorem study (Theorems A–C).
- **Verdict.** The two identities used are classical. Theorem E (the −2 homothety of the unlike faces, and with it Observation 2) and Proposition D with the midpoint rule were not found in these sources. "Not found" is limited to them.

## LEADS

1. **Other dimensions.** In dimension d, ℤ^d-type CsCl (2ℤ^d ∪ 2ℤ^d + 1) against its half (2D_d ∪ 2D_d + 1). Does the unlike face stay a scaled cube slice? For d = 2 the half has only 2 unlike neighbours, so the counting changes. A quick exact test with this script's `cell()` generalised to d.
2. **Other pairs.** Corollary F's argument is a transfer principle. Two networks with the same unlike distance whose unlike faces are similar with a fixed ratio, and with one like-face orbit per kind, have proportional walks. Screen #53's other networks and the DICTONIC networks (HexOct, TRD, RD-cross) for such pairs; the hcp holes against fluorite is the obvious candidate, and it is known to fail (extra flip at 5/24), so the screen should say exactly where.
3. **The two-weight bridge.** Weight the missing half of CsCl down by μ and walk (λ, μ) to see the CsCl dual cells turn into the zinc blende ones (Theorem A in two parameters, as in lead 3 of the switch-theorem study).
4. **Observation 3, last step.** Prove the midpoint rule's hypothesis (an inversion centre at the minimising like pair) for all centrosymmetric two-kind structures. Then for those, gradual iff Σ_K (ℓ_K²/4 − δ_K²) < 0: a closed rule from distances.
5. **Paper home** (route via the Concordance destinations; DICTO decides). Theorem E and Corollary F close #53 Observation 2, and Proposition D advances Observation 3. They fit with yesterday's Theorems A–C as a "Version 2 adds …" of #53, or as one short note.

## Ledger line (for the Concordance; not entered by this study)

`{"question": "#53 Obs 2: CsCl <-> zinc blende polynomial coincidence; Obs 3 criterion", "method": "obs2_proof.py exact cells per interval + face homothety + derivative/pyramid identities; likebirth.py exact LP tau_A, tau_B on 12 nets", "status": "SETTLED (Obs 2); PARTIAL (Obs 3)", "result": "Obs 2 true exactly: ZnS unlike face = s(1,1,1) - 2 x CsCl unlike face (cube slice), so volumes x2 by dV/dlam = sum A/(2d), like faces x1/sqrt2 by 3V = sum hA; flip circuits differ, scaling moves flips to +-4; Obs 3: like bonds born at LP values tau, gradual iff tau_A < -tau_B, switch iff equal; midpoint rule for centrosymmetric pairs", "retry": "never (Obs 2); Obs 3 only toward a closed rule", "study": "2026-11-09-cscl-zincblende", "date": "2026-11-09"}`

## Files

`scripts/`: obs2_proof.py, likebirth.py. `data/`: obs2.json, obs2-checks.txt, likebirth.json, likebirth-checks.txt, likebirth-stdout.txt. Imports #53's engine and networks from `../2026-10-25-relay-census/scripts` and the control networks from `../2026-11-08-switch-theorem/scripts`.
