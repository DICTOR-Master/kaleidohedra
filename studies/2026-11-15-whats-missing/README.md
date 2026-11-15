# What's missing: hidden swaps, unused involutions and the periodic points of the hops (15 Nov 2026)

**Verdict (15 Nov 2026): no new law-giving fixed point was found. Every law forced today is classical: Brunn's central-slice maximum (at the fixed slices of evacuation and of the longest element w0), symmetric criticality (Palais) in the twist family of Narcissus, and an orbit lemma of the icosahedral group (the regular hulls of the pentakis cycle). Of the 17 laws that had no swap, 1 is in fact forced at a swap's fixed point (Kelvin's half of the Dehn test, already proved as the CsCl parity), 6 are carried by a swap as an invariance or a swapped pair (Hexagonality, Window, width, one-way-only, the all-golden 4D pair, the 4D Vacuus heart), 1 has only an algebraic swap (valley rule), and 9 have none. Gale and Alexander duality force nothing; the registry holds no Alexander fixed point. The hops have no periodic points beyond their fixed points, and DICTO's growth rule T is the polarity swap up to scale.**

DICTO approved this study on 15 Nov 2026. It continues studies/2026-11-13-swaps-and-fixed-points (23 swaps; 45 proved laws, 9 at a fixed point, 24 with a swap in some role, 17 with none) and studies/2026-11-14-forced-fixed-points (the battery and its controls). The rule is unchanged: a finding **qualifies** only if a law is FORCED at the fixed point of a GEOMETRIC involution, by parity, by symmetry with concavity, or by extra symmetry, proved exactly, with the controls passing. Computation, proofs and drafting were done with Claude (Anthropic).

Script `scripts/missing.py`; logs `data/missing.log` (full) and `data/missing-pilot.log`; data `data/missing.json`, `data/missing-pilot.json`. Runs on the compute host through the job gate: pilots wmiss-pilot (stopped: one step too slow, rewritten in exact Q(√5) arithmetic) and wmiss-pilot2 (99 checks, FINAL ok); full run wmiss (108 checks, 0 FAIL, 81 s, FINAL ok). **Exact arithmetic decides every check**: Python fractions for the rational polytopes (slices of permutohedra, the tetrahedron, the 5-cell), exact Q(√5) for the reflection groups, sympy radicals and DomainMatrix ranks over Q(√d) for the rest. Floats only order corners round a face. Reused code is executed from its own files, not retyped: the header and the whole control section of the forced study's `forced.py` (with its exact polytope engine and exact Dehn routine), and `recog_solid` of studies/2026-11-13-platonic-fans-law.

## Controls

| control | swap | forced law | result |
|---|---|---|---|
| √3 on the cube–octahedron line | the turn μ ↦ 3/μ | t_min = 5 − μ − 3/μ even, t″(√3) < 0: maximum 5 − 2√3 | **qualifies** (rerun unchanged) |
| 3/2, Kelvin's cell | the CsCl site swap μ ↦ 3 − μ | Dehn −72√2/5, −24√2/5, 0, 24√2/5, 72√2/5 at 6/5 … 9/5: odd, zero at 3/2; wall area even and concave | **qualifies** |
| 8/5 (random) | none | Dehn 24√2/5 ≠ 0; nothing critical | **fails** |
| Brunn, tetrahedron along a 3-fold axis | none negates the direction | slice areas at s = −1, 0, 1: the face slice is largest, not the middle | **fails**, as required |
| Brunn, 5-cell along e₁ | none negates the direction | the facet slice (s = 0) beats the centroid level (s = 1/5) | **fails**, as required |
| twist family at a random angle (cos θ = 3/5) | none | the tone's derivative is nonzero | **fails**, as required |

## Part 1. Hidden swaps behind the 17 laws with no swap

For each law, its parameter was tested against μ ↔ c/μ, μ ↔ c − μ, the Möbius involutions, Galois conjugation in Q(√2), Q(√3), Q(√5), polar duality and mirror image.

| law | verdict | the swap | fixed point | exact reason |
|---|---|---|---|---|
| #66/#67 Hexagonality Law | SWAP FOUND, NOT FORCED | c ↔ h, h ↦ 1 − h | h = 1/2 (the word chch) | every affine law is odd about its own midpoint (checked symbolically for f = A + Bh); at 1/2 it returns the mean f(cc), f(hh), the Swap Rule itself; f(c/h) is affine only if B = 0, so no c/μ or non-affine Möbius swap keeps the law |
| #84 Window Law | SWAP FOUND, NOT FORCED | c ↔ h and word reversal | — | linear in word shares, which both swaps permute; the only odd quantity, F(ch) − F(hc), vanishes as an invariance (mirror-hexagonality study) |
| #94 Silent Golden Station | NONE as a swap of the line; forced by extra symmetry | turn (3/φ), CsCl swap (3 − φ), μ ↦ 2/μ (2/φ): none silent; the B3 seed reversal goes to the stretch of corners (1, 1, b), which has no Q₄ zero; the only Möbius involution fixing 1/φ that keeps the poles ±i is a ↦ (2 − a)/(2a + 1), and it sends φ off the zero set | — | **hidden Galois swap**: Icosaxes (the octahedron truncated at 1/φ² of each edge) is fixed by √5 ↦ −√5 up to similarity (a·σ(a) = −1), but so is a = 1/φ³, which is not silent. The silence comes from the 12 even-permutation corners forming a regular icosahedron, a 5-design (Goethals–Seidel): extra symmetry of the halves |
| #100 Dehn test | **SWAP FOUND, FORCED** (already proved) | CsCl site swap μ ↦ 3 − μ | 3/2, Kelvin | Theorem 1.1's Kelvin zero is the parity of the swaps study (K4; control above). On the truncated tetrahedra T ∩ (−kT), Dehn = 24√2(k − 2) ⊗ β (β = arccos 1/√3; exact at k = 1, 3/2, 2, 5/2); the only swap is the fold k ↦ 1/k, the similarity x ↦ −x/k (S(1/2) = −S(2)/2 exactly), under which Dehn is even (D(2/3) = (2/3)·D(3/2) = −8√2): no forced zero; the fold's fixed point, the octahedron, has Dehn −24√2 |
| #45 width theorem | SWAP FOUND (invariance), NOT FORCED | polar duality D ↔ I, C ↔ O | the tetrahedron | the width w = √(3 + ρ²) − ρ depends only on ρ = r/R, which duality keeps (reproduces (√30 − √3)/3); at the self-dual tetrahedron the formula does not apply (classical Reuleaux tetrahedron). Also w(ρ)·w(−ρ) = 3, an algebraic turn whose fixed point ρ = 0 is no solid |
| #85 valley rule | ALGEBRAIC SWAP ONLY | (s ↦ 1/s, α ↦ π/2 − α, γ ↦ π/2 − γ) keeps tan γ_k = s^k tan α; an involution of one solid only when α = π/4, the cube | t = 2 on the cube | t ↦ t/(t − 1) is harmonic conjugation about the centre and the mirror point (cross-ratio −1): projective, not geometric; what it forces (γ = π/4, coplanar valleys, the rhombic dodecahedron) is the formula's own value |
| #93 one way only | SWAP FOUND (invariance), NOT FORCED | CsCl swap exchanges P_μ, Q_μ | 3/2 | the law holds at every μ of the walk |
| #105 4D Vacuus counts | SWAP FOUND (pair), NOT AT THE FIXED POINT | CsCl swap: the DICTO 1:2 Truncated Octahedron (μ = 4/3) ↔ the 2:1 (5/3) | 3/2 (Kelvin, the permutohedron of 1, 2, 3, 4) | distance patterns of the three permutohedra match the C–O cells at 4/3, 5/3, 3/2 exactly; the counts are integers with no parameter |
| #91 all-golden 4D solids | SWAP FOUND (pair), NOT FORCED | μ ↦ 5 − μ on K ∩ μK* (tesseract, 16-cell), 2 < μ < 3: the B4 seed reversal (0, 1 − a, a, 0) ↦ (0, a, 1 − a, 0) | μ = 5/2: the bitruncated tesseract (corners sperm(1, 1, 1/2, 0)) | φ² + 2 + 1/φ² = 5, so the two all-golden polytopes are a swapped PAIR. On the 8 cube cells the swap is exactly the CsCl swap μ₃ ↦ 3 − μ₃ (Icosaxes ↔ its partner 3 − φ); on the 16 tetrahedral cells it pairs non-similar truncated tetrahedra (cuts (2 − φ)/(3 − φ) and 1/φ²), so it is not a similarity there; at the fixed point the B4 degree-4 corner tone is −1440 ≠ 0 |
| #44 face pyramids | NONE | duality sends {C}, {T, O}, {C, T, O} to {O}, {T, C}, {C, T, O}: only the last fills | — | the law is not duality-invariant; mirror and Galois act trivially or leave the five |
| #47 every mix fills | NONE | — | — | universal over the 31 mixes: every permutation of D, I, C, T, O keeps it |
| #106 one world | NONE | — | — | the same |
| #77 face to face | NONE | — | — | discrete, no parameter |
| #92 pyramid tilings = stackings | NONE | — | — | c ↔ h and reversal permute tilings; complement fixes no word |
| #101 held by shape | NONE | — | — | the layer inversion fixes the locked octahedra, but also the cubes of the upright cube layer, which are free (#101's own calibration) |
| Permutohedron Family Theorem 1 | NONE | reversal and x ↦ (n + 1) − x fix every member | the whole line | reversal maps intervals to intervals of equal size (n = 4 … 7), so it fixes Π and Loday's associahedron and every point between: it singles none out; Π tiles and L does not, so no s ↦ 1 − s is geometric |
| Laves locality theorem | NONE | — | — | the six-layer window is symmetric about its gap |

**Tally.** Forced at a fixed point: 1 (#100's Kelvin half). Invariance or pair: 6. Algebraic only: 1. None: 9. With these readings the 45 laws of the swaps study sort as AT 10, NEAR 1, AXIS 1, INV + PAIR 20, HOP 3 (with #80 now read as polarity up to scale, Part 3), algebraic 1, NONE 9.

## Part 2. Known involutions not yet used

| involution | its action on DICTO's objects | fixed points (exact) | battery there | forced law |
|---|---|---|---|---|
| **Schützenberger's evacuation** | on orderings it is w ↦ w₀ w w₀: reverse the row and replace bell b by n + 1 − b (checked: RSK(w₀ w w₀) = (evac P, evac Q) for all of S₁ … S₇) | rows: the centrally symmetric ones, 2^k k! (n = 1 … 7); tableaux: self-evacuating = domino tableaux for every shape of even size ≤ 8 (Stembridge 1996; Stanley 2009), and Σ (self-evacuating)² = 2^k k!; on the permutohedron: the slice by the fixed space is its projection, a type-B permutohedron, sperm(1, 3, …, 2k − 1) (n = 2k) or sperm(1, …, k) (n = 2k + 1), checked by exact vertex enumeration (n = 4: the octagon; n = 6: 48 corners) | the 3D fixed slices are the forced study's zonohedron line at a = 1/2 (n = 6) and a = 1 (n = 7): every corner tone Q4 … Q12 and canonical-form tone F4 … F12 nonzero, Mahler (derivative 68/225, −488/675) and roundness not critical, no tiling (forced study's proof), Dehn 0 as for every zonotope | **Brunn**: the fixed slice is the largest parallel slice, exact: Kelvin's cell, octagon area 7 against 23/4 and 4 at offsets ±1/4, ±1/2; 6-permutohedron, volume 138 against 89 and 212/3, even in the offset. Classical (Brunn 1887; Minkowski) |
| **change ringing** (Paradigm Ch. 15) | the same move on rows | plain hunt on 4, 6, 8, 10 bells: every row fixed; on 5, 7, 9, 11 bells the hunt goes to the hunt that starts with the other change (the two halves of Theorem 13.7); Plain Bob Minimus goes to the method with lead-end 34 in place of 12, and 8 of its 24 rows are fixed | — | none beyond the symmetry itself |
| **the longest element w₀** (A3, B3, H3, A4, B4, F4, H4) | reverses sweeps (the fundamental chamber to its negative) | built as a product of 6, 9, 15, 10, 16, 24, 60 reflections (the numbers of positive roots); w₀ = −1 for B3, H3, B4, F4, H4 (the centre); w₀ = −ε for A3 (a fixed line) and A4 (a fixed plane) | the 4D permutohedron's sweep is a time palindrome, i down-edges at height h ↔ 4 − i at −h, h-vector (1, 26, 66, 26, 1) (#104) | **Brunn**: central slices are the largest of their parallels. The DICTO 1:2 Truncated Octahedron (the slice x₅ = 3, the heart of the 4D Vacuus, #105) has volume 140/3 against 1835/48 and 259/6 at t = ±1/2, ±1; the tetrahedron's square slice (area 2 against 3/2) across a direction negated by w₀; the 5-cell's middle slice x₁ − x₅ = 0 (1/12 against 9/256). Classical |
| **Gale duality** | n points in R^d ↔ n points in R^(n−d−1); a fixed point (self-associated set) needs n = 2d + 2: 8 corners in space, 6 corners of a disc | of 9 exactly recognised 8-corner registry solids, all 7 hexahedra (cube, rhombohedron, 60° rhombic prism, leaning square prism, both golden rhombohedra, Reuleaux cube corners) are self-associated (quadric rank 7: the products of opposite face planes give the net, Coble); the gyrobifastigium and triakis tetrahedron are not (rank 8); every hexagonal #87 disc tested lies on a conic: cuboctahedron 4, tetrakis hexahedron 6, elongated square bipyramid 2, bilunabirotunda 2 | the octahedron frustum is self-associated (rank 7) with Dehn −3√2 ⊗ arccos(1/3) ≠ 0 (angles π/2 ∓ β/2, π − β exact), so it fills no space (Debrunner 1980); the cuboctahedron's discs are self-associated while its Dehn invariant is nonzero | **none** |
| **Alexander duality** | the disc edges S of a solid ↔ (E ∖ S)* in the dual graph; a fixed point needs V = F, \|S\| = E/2 and χ(S) = 1 | none: of the 77 registry solids with V = F, the only ones with discs are the gyrobifastigium (4 of 14 edges) and the bilunabirotunda (12 of 26) | — | **none** (no fixed point exists) |
| **chirality** | mirror image | Narcissus (exactly 3 vertical mirrors), Covenant (centrally symmetric about its hexagon centre, 14 corners), the straight join of two Narcissus (the twisted cube: 6 improper symmetries among the 12 candidates, so achiral), the common core of the two chiral compounds of five tetrahedra | every battery quantity (tiling, Dehn, tones, form, Mahler, roundness, wall area) is O(3)-invariant, so even under the mirror: nothing vanishes | in the **twist family** (the second Narcissus turned by θ on the hexagon) the mirror acts as θ ↦ −θ and fixes θ = 0 and 60°: the degree-4 and degree-6 corner tones are critical exactly there (Palais), not at cos θ = 3/5; the θ-dependent part Σ P₄(cos γ) has second derivative 70 and −70 there (a minimum and a maximum). The two fives are mirror images (exact), both have the 20 three-fold directions as face normals, so they share one core, which is therefore achiral: the regular icosahedron (the classical Kepler–Coxeter compound). Criticality only; no new law |

The twin Vacuus Angeli are Galois twins, not mirror images; their hulls have full icosahedral symmetry (twin-vacuus study), so the mirror fixes them and forces nothing.

## Part 3. Cycles (hops): periodic points

| cycle | periodic points (exact) | forced there |
|---|---|---|
| #69 Fibonacci hop s ↦ 1/(1 + s) | for every iterate k ≤ 20 the fixed-point equation is F_k (s² + s − 1) = 0, and M² is hyperbolic (trace 3): only the two fixed points 1/φ and −φ | the share 1/φ² (#69); no reversing swap is geometric: nothing new |
| #80 DICTO's growth rule T(S) = {x : v·x ≤ v·v} | T(tetrahedron) = −3 × tetrahedron (a fixed point on shapes); T²(cube) = 3 × cube; T²(dodecahedron) = (15 − 6√5) × dodecahedron (period 2) | T is the polarity swap on shapes (catalogue row 13), of infinite order only through the scale; at its fixed point the law reads gain 9 = 3², the main theorem restated |
| pentakis four-step cycle (twin-vacuus) | every pentakis start: period 4 on the twin side, D_{k+4} = c·D_k with c in Q(√5) (exact in that study; cited, not rerun) | the twin hulls at k ≡ 0, 2 are a regular dodecahedron and icosahedron for every start. Forced by symmetry: the icosahedral group's orbits of directions have sizes 12, 20, 30, 60, 120, so an invariant polytope with 12 facets has them on the 5-fold axes at one distance, and with 20 on the 3-fold axes (classical). The facet counts themselves are observed |
| golden cycles × φ³ (#38a), the crossed golden loop, the nest by thirds (#99) | every member, in shape space; none as solids (the scale is not 1) | polarity or a fixed nest composed with a scale; no involution of the cycle singles out a member: nothing |
| the OG chain | none: the OG family does not cycle and has no gnomon polynomial (twin-vacuus, og-margin) | — |

## CANDIDATES FOR AN INDEPENDENT REFEREE

Each is stated so that it can be attacked.

1. **#91 pair.** On K ∩ μK* with K = [−1, 1]⁴, 2 < μ < 3, the map μ ↦ 5 − μ is the B4 seed reversal (0, 1 − a, a, 0) ↦ (0, a, 1 − a, 0), a = μ − 2; it swaps the two all-golden polytopes μ = φ² and μ = 2 + 1/φ²; on the cube cells it is the CsCl site swap; its fixed point is the bitruncated tesseract, whose degree-4 tone is nonzero.
2. **#100 reclassified.** Theorem 1.1's zero at Kelvin's cell is forced by the CsCl swap (Dehn odd, 12√2(3 − 2μ)); the zero at the cube is not at any swap's fixed point.
3. **Evacuation slice.** The slice of the n-permutohedron by the fixed space of x ↦ (n + 1)𝟙 − w₀x equals its projection and is the type-B permutohedron of (1, 3, …, 2k − 1) for n = 2k and of (1, …, k) for n = 2k + 1; at n = 6, 7 it is the silent-zonohedron line at a = 1/2, 1, where nothing in the battery is forced.
4. **Bells.** On an even number of bells every row of the plain hunt is fixed by reversing the row and replacing b by n + 1 − b; on an odd number the move exchanges the two hunts; Plain Bob Minimus goes to the method with lead-end 34.
5. **Brunn at the heart.** The DICTO 1:2 Truncated Octahedron is the largest slice x₅ = const of the 4D permutohedron; more generally every evacuation-fixed or w₀-fixed slice of a centrally symmetric permutohedron is the largest in its parallel family.
6. **Gale.** The corners of every hexahedron with planar faces are self-associated; the octahedron frustum shows that this forces neither tiling nor Dehn zero; the hexagonal discs of the cuboctahedron, tetrakis hexahedron, elongated square bipyramid and bilunabirotunda lie on conics.
7. **Alexander.** No registry solid is a fixed point of S ↦ (E ∖ S)* (condition: V = F and half the edges on discs).
8. **Twist family.** In the family of two Narcissus joined on the hexagon and turned by θ, every smooth mirror-invariant quantity is critical at the straight join and at Covenant; the straight join is achiral.
9. **T is a swap.** DICTO's growth rule is polar reciprocation up to scale; the tetrahedron is its fixed point on shapes.
10. **Icosaxes and Galois.** Icosaxes is fixed by √5 ↦ −√5 up to similarity; no Möbius involution preserving Q₄ on the cube–octahedron line fixes it; its silence is the 5-design property of its two icosahedra.
11. **Pentakis regularity.** The regular twin hulls of the pentakis cycle follow from icosahedral symmetry and the facet counts 12 and 20.

## Faults fixed on the way

- The Dehn check of the truncated tetrahedra first expected 12√2(k − 2); the exact routine measures in β = arccos(1/√3), where the coefficient is 24√2(k − 2). The expectation was wrong, not the mathematics.
- The slice jobs first failed to start (the process pool's default start method); now forked explicitly.
- The w₀ step for H4 ran over 7 minutes in symbolic radicals; the pilot was stopped and the step rewritten in exact Q(√5) arithmetic (the field class of the #87 study). The second pilot and the full run passed.
- The preflight gate first refused the pilot on ledger entry [225]; the plans record that this run only reruns the forced study's control section and does not revisit its three fixed points.

## Sources checked

- **Repository:** studies 2026-11-13-swaps-and-fixed-points (catalogue, K1–K9, leads), 2026-11-14-forced-fixed-points (battery, controls, the silent-zonohedron data), 2026-11-13-palindromic-middles, 2026-11-13-pure-swap-6d, 2026-11-13-mirror-hexagonality, 2026-11-13-platonic-fans-law (fans law, data), 2026-11-13-platonic-disc-ranking (registry), 2026-11-11-twin-vacuus (pentakis cycle, Angeli), 2026-11-06-crossed-nest, 2026-11-04-narcissus-cube (Narcissus corners), 2026-11-12-laves-three-layer-swap, 2026-11-14-chat-handoff; paper abstracts of #44, #45, #47, #66, #67, #77, #80, #84, #85, #91, #92, #93, #94, #99, #100, #101, #105, #106, #38a, Narcissus and Covenant, Narcissus Keyed, the Permutohedron Family; The Permutohedron Paradigm (chapter list; change ringing is Chapter 15); the Concordance ledger digest (entry [225]).
- **Classical results named at the point of use**, from standard knowledge, not reread for this study: Schützenberger (evacuation; RSK of the reverse-complement word, 1963, 1972), Stembridge 1996 and Stanley 2009 (self-evacuating tableaux and domino tableaux), Coxeter and Bourbaki (w₀ = −1 exactly for the groups listed), Brunn 1887 and Minkowski (central sections), Gale 1956, Coble and Eisenbud–Popescu 2000 (self-associated point sets), Alexander 1922, Palais 1979, Goethals–Seidel 1981, Debrunner 1980, Kepler and Coxeter (compounds of five tetrahedra). The reference library was not searched.

## Ledger line

Concordance ledger entry of 15 Nov 2026, "what's missing: hidden swaps, unused involutions, hop periodic points".

DICTO · dictospheres.com
