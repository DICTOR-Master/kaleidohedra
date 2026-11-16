# Hidden zeros in H4 / E8 polytopes: a census of unexplained silent degrees (15 Nov 2026)

**Verdict.** We took five polytopes: the 600-cell, the 120-cell, the 24-cell, the snub 24-cell and the E8 roots. In each, we took every orbit of every listed subgroup class of the symmetry group, every union of two such orbits, and every union of twisted classes. That gives 3232 distinct point sets. Their tones T₁ … T₂₀ were computed exactly. Of all their zero degrees, **all but a short list are explained** by one of eight mechanisms. The list is below. **Twisted silence** (DICTO's name; the mechanism is from the parallel golden-A4 study) shows up in four single twisted classes whose silence their symmetry does not force. The outer-twisted classes of 2I are only the golden pair: the 20-set (degrees 5, 7) and the 30-set (degrees 3, 6). The 20-set also lies in the snub 24-cell. Two small twisted classes from outer automorphisms of 2T and 2O also count: a 6-point set in the snub 24-cell (degree 3) and an 8-point set in the 24-cell (degree 2). Four further mechanisms turned up, all with exact checks:

- **Double Vision degree linkage.** On the 600-cell, T₇ = 0 implies T₅ = 0 for every rational weighting, and T₉ = 0 holds exactly when T₁₅ = 0. So the golden double zero is one rational condition.
- **The Double-Vision class pair** C ∪ (−σC) of 2I. It kills exactly degrees 3, 4, 5, 9 and 15.
- **Latitude rings.** These explain the 120-cell lead: the four 60-point A5-orbits are rational combinations of icosahedral latitude rings, and sin 5θ = 0 kills those rings in degree 4.
- **The E8 "bizonal" root.** The two 600-cells inside E8 sit exactly at the zeros of 5s² − 5s + 1, so they are silent in degree 4.

All controls passed: 6 controls and 80 in-run soundness checks, 0 failed.

| polytope | sets | unexplained zeros (degree: sets) | status |
|---|---|---|---|
| 600-cell | 808 | degree **8**: four classes of 30- and 60-point unions of [C3 × C5], [C5 × C5], [C3 × C10] and [C5 × C5].2 orbits (one condition each) | **OPEN** |
| 120-cell | 1482 | degree **8**: one 240-point union of two orbits of [C5 × 2T] (and its mirror image), one condition | **OPEN** |
| 24-cell | 144 | none | — |
| snub 24-cell | 257 | none beyond the Double-Vision class pair | — |
| E8 roots (8D) | 541 | degree **4**: 120-point unions with stabiliser 576 or 144 (96 + 24 and 72 + 48 split over the two 600-cell shells), one condition each | **OPEN** |

**Update 16 Nov:** all three OPEN rows are now explained (Hopf rings and restricted linkage for the 600-cell, Hopf rings down to one exact 3D identity for the 120-cell, W(E8)-images of shells and bizonal swap pairs for E8): see `studies/2026-11-16-remaining-silences/README.md`.

"One condition" means that the zero imposes a single rational linear condition on the stabiliser-invariant weightings of the polytope. It is a crossing, not a coincidence.

DICTO asked (15 Nov) for every hidden zero to be mapped before anyone else. The parallel study `studies/2026-11-15-fable-golden-a4/REPORT.md` explains the census's golden case. Section 1 of this README was written and committed blind, before that report was read. Computation, proofs and drafting were done with Claude (Anthropic).

## 0. Method

- **Point sets.** The 600-cell is the 120 unit icosians (2I). The 120-cell has one vertex per tetrahedral cell, at φ⁻²·(the sum of its corners), so that its squared radius is rational. The 24-cell is 2T, and the snub 24-cell is 2I ∖ 2T. The E8 roots are the 120 units together with φ⁻¹ times the units, with the rational form B(x, y) = a + b when ⟨x, y⟩ = a + b√5 (Conway and Sloane, SPLAG, ch. 8). The checks confirm 240 vectors with B ∈ {0, ±½, ±1}, and the E8 zeros (1–7, 9–11, 13, 15, 17, 19).
- **Exact arithmetic.** Coordinates are integer pairs a + bφ. Tones T_k(S) = |S|⁻² Σ G_k(cos) / G_k(1), with G_k = Chebyshev U_k in 4D and Gegenbauer C_k⁽³⁾ in 8D. This is the census normalisation. Kernels N_k = {rational weightings w : the degree-k harmonic part of w vanishes} are computed exactly with python-flint.
- **Groups.** The H4 elements are x ↦ l x r̄ and x ↦ l x̄ r̄. The subgroup catalogue holds every reflection subgroup, every cyclic subgroup and every two-generated subgroup (all three complete up to conjugacy). It also holds the quaternion families [L × R], [L × L].2, the diagonal and the Galois-twisted diagonal groups for every subgroup L of 2I, and it is closed under taking rotation parts and adjoining −I. That gives 179 classes in H4. F4 (24-cell) has 221 classes and the snub group (order 576) has 71. The E8 universe uses the H4 classes acting diagonally. Twisted classes {a x₀ α(a)⁻¹} were enumerated for every subgroup G of 2I (or 2O for the 24-cell) and every automorphism α, with every union of classes (every union when a subgroup has at most 9 twisted classes, unions of up to 3 classes otherwise). Unions of two orbits are kept for subgroups with at most 8 orbits (hz_census.py); this rule fixes the count 3232 (correction of 17 November 2026, found by the independent re-derivation in studies/2026-11-17-independent-checks/109-census).
- **Mechanisms, in order:**
  - **G**: the set's stabiliser has no invariant harmonic of degree k (Molien).
  - **X**: the set's full O(n) symmetry group has none (Gram automorphisms; Molien on the span).
  - **ZONAL**: the symmetry fixes one axis, its only invariant is the zonal harmonic, and the set lies on one latitude θ with U_k(cos θ) = 0, that is, sin((k+1)θ) = 0.
  - **TW**: twisted silence of a single twisted class, or no α-stable constituent at all. The intertwining identity ρ(g)S = Sρ(α(g)) is verified numerically for each case.
  - **SPAN**: the indicator lies in the exact rational span of explained-silent sets and the parity relations (S and −S), closed under the symmetry group.
  - **GAL**: as SPAN, but also closed under Double Vision (σ, then a fixed quaternion automorphism).
  - **RES**: every stabiliser-invariant weighting of the whole polytope is silent (conditions = 0). In the 120-cell this clears the [15, 17] zeros of one 120-point orbit of the twisted diagonal C5.2 group and of its unions. In E8 it clears the two shells (§6).
  - **OPEN**: none of the above.

## 2. The unexplained zeros (final)

| polytope | set | stabiliser | all zeros | OPEN | conditions | Galois-self |
|---|---|---|---|---|---|---|
| 600-cell | 30-point union, [C3 × C5] orbits (two mirror classes) | 15 | 1, 3, 4, 8 | **8** | 1 | no |
| 600-cell | 30-point union, [C5 × C5] orbits (two) | 50 | 1, 3, 4, 8 | **8** | 1 | no |
| 600-cell | 60-point union, [C3 × C10] orbits (two) | 60 | all odd, 4, 8 | **8** | 1 | no |
| 600-cell | 60-point union, [C5 × C5].2 orbits (two) | 200 | all odd, 4, 8 | **8** | 1 | no |
| 120-cell | 240-point union, [C5 × 2T] orbits (two) | 120 | 1–5, 7, 8, 9–11, 13, 15, 17, 19 | **8** | 1 | no |
| E8 | 120 roots, 96 + 24 over the two shells (two) | 576 | all odd, 4 | **4** | 1 | — |
| E8 | 120 roots, 72 + 48 (two) | 144 | all odd, 4 | **4** | 1 | — |

All the degree-8 cases carry their degree-4 zero for an explained reason (SPAN), and on the 600-cell T₈ = 0 implies T₄ = 0. They are products L·x·R of two cyclic groups. The twisted-class theorem does not cover them, because the left and right factors are independent and x₀ lies outside any group generated by them. No Galois relation (GAL) explains them.

**Cleared since the blind pass** (§1). The frames and 8-, 6- and 12-point sets are cleared by parity and latitude (ZONAL). The 24-, 36- and 48-point sets with degree 4 are cleared by SPAN. The golden 20-set and its 40-point union are cleared by TW and SPAN. The 20-point set with zeros 2, 5 (cosine ±½ class) is cleared by ZONAL.

## 3. Twisted silence across the five polytopes (the brief's point (c))

- **Single twisted classes with a zero that their symmetry does not force:** only the golden pair in the 600-cell.
  - The 20-set X: outer α of 2I, degrees **5, 7**, twisted character zero. Here hom-dim > 0 and the intertwining error is below 1e-7.
  - The 30-set F: outer α of 2I, degrees **3, 6**, twisted character zero.

  The 20-set reappears in the snub 24-cell, since it lies in 2I ∖ 2T.
- **Beyond 2I** (the brief's question, answered by the census):
  - Snub 24-cell: a 6-point twisted class of 2T under an OUTER automorphism kills degree 3 (stabiliser 6, symmetry 48, hom-dim 2).
  - 24-cell: an 8-point twisted class of 2O under an OUTER automorphism kills degree 2 (stabiliser 48 = symmetry 48, hom-dim 1).
  - Snub 24-cell: the 12-point ordinary classes of 2I kill degree 4. This is the classical class-character zero (α inner); in the 600-cell the latitude rule already explains it.

  The golden-A4 study (§3 D) expected nothing new from 2T and 2O, because their outer automorphisms are induced by rotations. The two small sets are consistent with that, but neither our latitude test nor our symmetry tests catch them. Twisted silence is the only explanation found for them. Ordinary classes (α inner: the 12-classes killing 4, the 20-classes killing 2 and 5, the 30-class killing the odd degrees) are explained already by the latitude rule, as the golden-A4 study predicted (its §3 C).
- **Unions of several twisted classes** (the zero comes from cancellation in a weighted twisted-character sum; listed in `data/tables.md`): 600-cell 68 sets, 24-cell 6, snub 24-cell 7. Their degrees are 2, 3, 4, 5, 6, 7, 9 and 15. Almost all of them are SPAN-explained from silent parts (600-cell 68, 24-cell 6, snub 24-cell 7). Two are not, and both are cleared by the next mechanism:
  - **Double-Vision class pair (new).** Let C be a conjugacy class of 2I of order 5 or 10, and σC its Galois image. The union C ∪ (−σC) (24 points) kills exactly **3, 4, 5, 9, 15** for k ≤ 20. Reason: for odd k only the faithful constituents count, and on −σC their characters are −σ(χ(C)). So the block sums are χ(C) − σχ(C), which vanish exactly when every constituent of V_k = Sym^k(C²) restricted to 2I is rational at C. The constituents 4s and 6 are rational there; 2, 2′, 3 and 3′ are not. For even k the block sums are traces, and only the 5, with χ = 0, vanishes. With the restriction list (V₃ = 4s, V₅ = 6, V₉ = 4s + 6, V₁₅ ⊇ V₃ by Klein's degree-12 form; V₇ and V₁₁ contain 2′ or 2), this predicts {3, 4, 5, 9, 15}, which is exactly the observed list. Checked on all six pairs of 12-classes (C ∪ −C kills all odd degrees, C ∪ σC kills only 4, C ∪ −σC kills 3, 4, 5, 9, 15). The character values are the standard 2I table, quoted and not recomputed here, and the agreement is for k ≤ 20 only. This set and the seven unions built from it (sizes 26, 54, 56, 64, 66, 94, 96; and the 24-set in the snub 24-cell) account for every 9/15 zero in the 600-cell and the snub 24-cell.
  - In the 24-cell, the twisted-union zeros (for example an 18-point union 6 + 12 under the outer automorphism of 2T, degree 3) are all SPAN-explained.
- **120-cell and E8:** no twisted class lies in them (their points are not group elements; the finite-group test fails).

## 4. The 120-cell lead (brief point (b))

These are the four 60-point A5-orbits that kill degree 4 (A5 = the Galois-twisted diagonal of 2I, the rotation part of the A4 Weyl group); data in `data/lead120.json`.

- **Hypothesis "A5's outer automorphism twists them": rejected as a forcing.** The normaliser of A5 in H4 has order 240 (±S5). Its odd elements (det −1, conjugation by an odd permutation: inner in S5, outer in A5) act with sign **+1** on the single A5-invariant degree-4 harmonic. They fix none of the four orbits: they permute them in one ±S5-orbit (1 ↔ 5, 7 ↔ 10, 1 ↔ 7). So the four zeros are **one** zero.
- **Galois swap.** One class of Double-Vision maps g∘σ normalises A5 and fixes each of the four orbits. That makes their degree-4 contents rational multiples of each other (the content of each fixed orbit lies on one rational line), but it does not force zero: the other fixed orbits (2, 8, 9, 11, 13) have nonzero contents in rational ratio (c₈/c₂ = −24/5, c₉/c₂ = −18/5).
- **Mechanism found (exact).** Each such 60-orbit is a **rational combination of icosahedral latitude rings**: 12-point sets at 36° and 72° about a vertex direction, which kill degree 4 because U₄(cos θ) = sin 5θ / sin θ = 0. Their 2400 H4-images span a space of rank 525, which equals the whole explained space E₄; the orbit's indicator lies in it (exact integer rank, job hz-lead2). So the lead is the latitude law of the icosahedral rings, carried by linearity.

## 5. Double Vision as degree linkage (all polytopes)

The rational kernels are nested. On the 600-cell and the snub 24-cell: T₆ ⇒ T₂, **T₇ ⇒ T₁, T₅**, T₈ ⇒ T₄, **T₉ ⇒ T₃, T₅, T₁₅**, T₁₀ ⇒ T₂, T₄, T₁₅ ⇒ T₃, T₅, T₉. So T₉ = 0 ⟺ T₁₅ = 0 for rational sets, and T₇ = 0 implies T₅ = 0 and T₁ = 0. In spin language, V₇ = 2′ + 6 and V₅ = 6: a rational set has zero 2′-part exactly when it has zero 2-part, which is the T₁ condition. That is Galois conjugation, so for rational sets of the 600-cell T₇ = 0 ⟺ T₅ = T₁ = 0. The 120-cell (not multiplicity-free) has weaker links, for example T₁₇ ⇒ 1, 3, 5, 7, 9, 11, 15. The full tables are in `data/tables.md`. The Galois closure (GAL) added nothing beyond SPAN in any polytope: Double Vision acts through linkage and through the class-pair rule, not by enlarging the explained spans.

## 6. E8 roots

- The two 120-point H4-orbits, one per 600-cell shell, kill degree 4. Their stabiliser H4, acting on R⁸ = R⁴ ⊕ R⁴, has exactly one invariant harmonic of degree 4. It is the bizonal h = |x∥|⁴ − 3|x∥|²|x⊥|² + |x⊥|⁴ (from Δh = 0). On S⁷ it equals 5s² − 5s + 1 with s = |x∥|², whose roots are s = (1 ± 1/√5)/2. These are **exactly** the parallel shares of the unit and φ⁻¹-unit icosians, so h vanishes on every E8 root. This is the Double Vision split of E8 seen by a harmonic, exact. The census records it as RES (conditions 0). The 240-set (all roots) is explained by W(E8), whose harmonic invariant degrees are 8, 12, 14, …. The symmetry-group search hit its cap there, so X is recorded by this known fact.
- The four 120-point unions in §2 stay OPEN. The bizonal part vanishes automatically for them, as for every root set, but their stabilisers (576, 144) have 2 or 3 further degree-4 invariants, and one condition remains.

## 7. Controls (job hz-ctl, all exact)

- **Known points.** The golden 20/30-sets give zeros {1, 2, 5, 7} and {1, 2, 3, 6}, by an independent sympy computation in A4 coordinates, and the same patterns occur among the 600-cell orbits. The 600-cell kills every k ≤ 20 except 12 and 20. The 24-cell kills exactly the degrees with no F4 invariant.
- **Random.** 3000 random subsets of the 600-cell (sizes 10–60) show 0 exact zeros.
- **Wrong mechanism.** The rule "a Galois-self set is silent in all odd degrees" fails on 232 of 360 sets. In every run, a fake Double Vision (a random permutation) used in the span closure was caught by the soundness check, because the span left the exact kernel.
- **In-run checks.** T_k = 0 ⟺ indicator in N_k (exact, every set checked); every explained span inside its kernel; the twisted intertwining identity. Totals: 600-cell 23/23, 120-cell 18/18, 24-cell 13/13, snub 24-cell 17/17, E8 9/9.

## 8. Prior art (free sources checked, 15 Nov)

- Web searches (standard): "spherical designs orbits finite group harmonic index Bannai Okuda Tagami"; "twisted conjugacy classes binary icosahedral group spherical design 600-cell harmonic"; "Koca W(A4) subgroup W(H4) orbits 600-cell quaternions".
- Found, by title and abstract only: Bannai, Okuda, Tagami, "Spherical designs of harmonic index t" (J. Approx. Theory 195, 2015; arXiv 1308.5101) and "More on …" (arXiv 1507.05373); Zhu, Bannai, Bannai, Kim, Yu, "On spherical designs of some harmonic indices" (Electron. J. Combin., 2017); Bannai, "Spherical t-designs which are orbits of finite groups" (J. Math. Soc. Japan 36, 1984); de la Harpe and Pache, "Spherical designs and finite group representations" (Eur. J. Combin.); Koca et al., "Branching of the W(H4) polytopes … under W(A4) and W(H3)" (arXiv 1106.2957), "Grand antiprism and quaternions" (arXiv 0906.2117); errorcorrectionzoo 600-cell page.
- None of them, at the level read, states the twisted-class silence, the Double-Vision class pair, the 600-cell degree linkage, or the E8 bizonal root. The harmonic-index framework (a set silent in one chosen degree) is the right home for these results and is credited. Goethals and Seidel 1981 and Delsarte, Goethals and Seidel 1977 were not reopened (the method is credited as in the law-giving census).

## 9. Files

- `scripts/hz_core.py`: arithmetic, tones, groups, Molien.
- `hz_universes.py`: the five polytopes, the Galois map, H4 from quaternions.
- `hz_groups.py`: the subgroup catalogue.
- `hz_twisted.py`: twisted classes and the intertwiner check (mechanism credited to the golden-A4 study).
- `hz_census.py`: the census.
- `hz_lead120.py` and `hz_lead120b.py`: the 120-cell lead.
- `hz_controls.py`: the controls.
- `hz_report.py`: makes `data/tables.md`.
- Data: `data/census-*.json` and `data/lead120.json`, with job logs in `data/logs/`; `data/census-U600-dev.json` is the data of the blind first pass (§1). Jobs: hz-pilot2, hz-u600b, hz-u120b, hz-e8b, hz-node, hz-u24, hz-ctl and hz-lead2, all FINAL ok. Also kept, superseded: hz-u600 and hz-e8 (stopped after a slow symmetry search, which was then bounded), hz-u120 (rerun with the latitude test on the full symmetry group), and hz-pilot (stopped, because it built the H4 two-generated catalogue for the 24-cell, which does not need it).

## Leads

- The degree-8 family of [Cm × Cn] products in the 600-cell, and the [C5 × 2T] union in the 120-cell. A product L·x·R silent in degree 8 needs an explanation by double cosets: the harmonic sum factorises as ρ(L-sum)·ρ(x)·ρ(R-sum).
- Prove the Double-Vision class-pair rule for every k (Klein's form gives periodicity 12) and list its kill set in full.
- Extend the catalogue to three-generated subgroups of H4. The present catalogue is complete for reflection, cyclic and two-generated subgroups only.

## 1. Blind (before reading Fable): unexplained zeros in the 600-cell, first pass (kept as committed)

Universe: the 120 vertices of the 600-cell. Subgroups covered so far (140 classes, up to conjugacy in H4): every reflection subgroup (16 classes), every cyclic subgroup, the quaternion families [L × R], [L × L].2, the diagonal and Galois-twisted diagonal subgroups for every subgroup L of 2I, and their rotation parts and ±I extensions. The two-generated subgroups were not yet included. Sets examined: every orbit, and every union of two orbits for groups with at most 8 orbits. That gives 291 distinct sets up to H4.

The tones T_k, k ≤ 20, are exact in Q(√5), with the census normalisation. A zero counts as explained when one of these holds: G, the set's stabiliser in H4 has no invariant harmonic of degree k (Molien); X, the set's full O(4) symmetry group has none; SPAN, the set's indicator lies in the rational span of explained-silent sets, closed under H4; GAL, as SPAN but also closed under Double Vision (√5 ↦ −√5, then a fixed quaternion automorphism). The column "cond" counts the independent rational conditions that the open zeros put on stabiliser-invariant weightings. In this pass GAL explained nothing beyond SPAN.

| size | kind | stabiliser order | symmetry order | all zeros | OPEN zeros | cond | Galois-self | source group |
|---|---|---|---|---|---|---|---|---|
| 20 | orbit | 120 | 120 | 1, 2, 5, 7 | **5, 7** | 1 | yes | A4 reflection group = twisted diag 2I (the census's golden 20-set) |
| 40 | union | 120 | 120 | 1, 2, 5, 7 | 5, 7 | 1 | yes | same group |
| 20 | orbit | 120 | 120 | 2, 5 | 2, 5 | 3 | yes | diag 2I.2 (H3 × A1 type) |
| 12 | orbit (×2 classes) | 120 | 120 | 4 | 4 | 1 | no | diag 2I.2 |
| 24 | orbit (×2) | 240 | 240 | odd, 4 | 4 | 1 | no | ±diag 2T |
| 48 | union (×2) | 240 / 48 | 240 / 48 | odd, 4 | 4 | 1–2 | yes | ±diag 2T |
| 24, 36, 36 | union | 36 | 36 | odd, 4 | 4 | 1 | mixed | [C6 × C6] |
| 30 (×2) | union | 15 | 15 | 1, 3, 4, 8 | 4, 8 | 1 | no | [C3 × C5] |
| 30 (×2) | union | 50 | 50 | 1, 3, 4, 8 | 4, 8 | 1 | no | [C5 × C5] |
| 60 (×2) | union | 60 | 60 | odd, 4, 8 | 4, 8 | 1 | no | [C3 × C10] |
| 60 (×2) | union | 200 | 200 | odd, 4, 8 | 4, 8 | 1 | no | [C5 × C5].2 |
| 6 | orbit | 24 | 48 | 3 | 3 | 2 | yes | twisted diag 2T |
| 8 | orbit | 24 | 48 | 2 | 2 | 2 | yes | diag Q8.2 |
| 4 | orbit | 12 | 24 | 2 | 2 | 2 | yes | diag Q8 (an orthonormal frame) |
| 12 | orbit | 24 | 24 | 2 | 2 | 2 | yes | diag 2T |

**Blind observation (degree linkage).** On the 600-cell the rational kernels are nested: T₇(S) = 0 implies T₅(S) = 0 and T₁(S) = 0 for every rational weighting S. Likewise T₈ ⇒ T₄, T₆ ⇒ T₂, T₉ ⇒ T₃, T₅, T₁₅, and T₁₀ ⇒ T₂, T₄. So the golden 20-set's double zero (5, 7) is **one** rational condition (cond = 1), not two.

Known first-pass gaps: the parity relation (S and −S have equal even tones) was not yet in SPAN, which is why the frame zeros are listed as open. The single-latitude Chebyshev roots (U_k(cos θ) = 0 at θ = jπ/(k+1)) were not yet tested. These are fixed in the next pass.
