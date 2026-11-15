# Hidden zeros in H4 / E8 polytopes: a census of unexplained silent degrees (15 Nov 2026)

**Status: work in progress. Section 1 is the BLIND table, written before reading the parallel golden-A4 study. Nothing in it uses that study's mechanism.**

## 1. Blind (before reading Fable): unexplained zeros in the 600-cell, first pass

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
