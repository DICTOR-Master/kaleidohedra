# Forced fixed points: the search for a law-giving shape (14 Nov 2026)

**Verdict (14 Nov 2026): no NEW law-giving shape was found. At the DICTO silent zonohedron nothing is forced: its Q4 silence is a crossing, not the fixed point of any swap. The cuboctahedron with pyramids on two opposite squares is a known space-filler (Critchlow 1969), an affine rhombic dodecahedron; the swap forces only Minkowski's necessary condition there. Of the three fixed points taken from the swaps study's leads, all carry forced laws on known shapes. Zinc blende's swap forces Dehn zero and the largest wall area at the triakis truncated tetrahedron, the Voronoi cell of diamond; the wall-area maximum is new here. The small stellated and great dodecahedra have a smooth, forced critical point of t_min* at their turn, and it is a minimum. Rock salt's parity holds only trivially. The two controls qualify, and the random control fails. With pyramids on adjacent squares no tiling by translations exists (proved). No octet-aligned periodic cover exists up to index 48. Tilings with turned copies stay undecided.**

DICTO approved this search on 14 Nov 2026. It follows the swaps study (studies/2026-11-13-swaps-and-fixed-points). That study found the universal "laws at fixed points of swaps" false: a fixed point carries a law only where the swap forces one. The three ways it can force one are known in general, and they are credited at the point of use. (1) Parity: a quantity that changes sign under the swap vanishes at its fixed point. (2) Symmetry and concavity: an even quantity is critical at the fixed point (Palais 1979), and a maximum when it is concave (Lindelöf 1869 is the classical case). (3) Extra symmetry: the fixed object has a symmetry its neighbours lack, and that symmetry kills what it kills. Computation, proofs and drafting were done with Claude (Anthropic).

Scripts `scripts/forced.py` (the battery) and `scripts/adjacent_cover.py` (the cover search). Logs `data/forced.log`, `data/forced-pilot.log`, `data/adjacent-cover.log`, `data/adjacent-cover-pilot.log`, with data in the matching `.json` files. All runs were on the compute hosts through the job gate (jobs ffix-pilot, ffix, adjcover-pilot, adjcover). The battery used one process: 121 of 121 checks, 88 s, FINAL ok. The cover search used 16 worker processes: 15 of 15 checks, 753 s, FINAL ok; the controls behaved (the rhombohedron tiles at index 1, the opposite pair at index 4, the cuboctahedron alone has no cover at index 16). **Exact arithmetic decides every check.** That means sympy rationals and radicals, minimal polynomials and polynomial remainders, and the Q(√5) class of the stars census. Floats only order corners round a face, bracket roots for printing, and serve as a control on the area formula.

Reused code is executed from its own files, not retyped:
- the exact polytope engine of the swaps study (`polytope`, `measures`);
- the exact Dehn routine and the octet-cell cover model of studies/2026-11-14-chat-handoff (`exact_dehn`, `torus_cover`);
- `hull_faces` of studies/2026-11-04-dehn-screen;
- `hnf` and `solve` of studies/2026-11-04-tetra-sweep (the latter is Knuth's algorithm X);
- the flag line, folding and Q(√5) of studies/2026-11-09-regular-stars-census.

## 1. The battery and the rule

At a point x* of a line of solids (or of a set of placements):

| step | question |
|---|---|
| B1 swap | Is x* the fixed point of a GEOMETRIC involution of the line? That means a similarity, polarity, Galois conjugation, site swap, turn or placement inversion. Every point is the fixed point of some abstract involution (a ↦ x*²/a), so only geometric ones count. |
| B2 parity | Does a natural quantity change sign under the swap? Then it vanishes at x*. |
| B3 symmetry | Is a quantity even under the swap? Then x* is critical (at a kink, critical in Clarke's sense). If the quantity is concave, x* is a maximum; if convex, a minimum. |
| B4 extra symmetry | Does the object at x* have more symmetry than its neighbours, and what does that symmetry kill? |
| B5 values | Tiling, corner tones Q4, Q6, Q8, Q12, the canonical form (polar volume and its tones), Mahler volume, roundness (isoperimetric quotient IQ). |

**A shape qualifies only if B1 holds and one of B2–B4 forces a law there, proved exactly.** A caution found on the way: any affine function is odd under the reflection about its own zero. Dehn of the cuboctahedron with k pyramids, (24 − 12k)√2 ⊗ β, is odd under k ↦ 4 − k. That is not parity, because k ↦ 4 − k is not a geometric move. The rule requires the swap first and the parity second.

**Controls.** All three behave as required.

| control | swap | forced law | mechanism | result |
|---|---|---|---|---|
| μ = √3 on the cube–octahedron line S(μ) = [−1,1]³ ∩ μ·octahedron | the turn μ ↦ 3/μ (#81) | t_min = 5 − μ − 3/μ is even under the turn (exact identity); t′(√3) = 0, t″(√3) = −2√3/3 < 0, so the maximum 5 − 2√3 | B3 | **qualifies** |
| μ = 3/2, Kelvin's cell (same line, read as the CsCl cell) | the CsCl site swap μ ↦ 3 − μ | Dehn: −72√2/5, −24√2/5, 0, 24√2/5, 72√2/5 ⊗ β at μ = 6/5, 7/5, 3/2, 8/5, 9/5, odd under the swap, zero at 3/2. Wall area W even with W″ = 24 − 16√3 < 0, so the maximum is at Kelvin's cell | B2, B3 | **qualifies** |
| μ = 8/5 (random) | none: the turn gives 15/8, the swap 7/5 | Dehn 24√2/5 ⊗ β ≠ 0, t′ = 11/64, W′ = 12/5 − 8√3/5, all nonzero | none | **fails** |
| a = 1/2 on the zonohedron line (random) | none | no tone vanishes | none | **fails** |

The t_min closed form was rechecked here against the polytope engine at μ = 8/5, 7/4 and 19/10.

## 2. Shape A: the DICTO silent zonohedron

**The DICTO silent zonohedron** is the zonohedron whose corners are the signed permutations of (a, a + 1, a + 2), at a = a* = −1 + √(1 + √(5/6)) ≈ 0.383066, where the Q4 tone vanishes. DICTO named it on 14 Nov 2026. Its finding comes from DICTO's chat session of 13–14 Nov (handoff Lead 7). The exact confirmation of its Q4 = 0 and Dehn = 0 is in studies/2026-11-14-chat-handoff. Below, the line is a > 0 and the silent zonohedron is the member at a*.

**Structure (exact).** The solid is the zonotope of 9 zones: the 6 zones (eᵢ ± eⱼ)/2 of Kelvin's truncated octahedron and the 3 zones a·eᵢ of a cube. Its 48 corners are exactly the signed permutations of (a, a + 1, a + 2), checked at a = 1/3, 1, 5/2. Its faces are 6 octagons, 8 hexagons and 12 rectangles for every a > 0, since a zonotope's faces depend only on its zone directions. Exact measures:
- volume V(a) = 4(2a³ + 12a² + 21a + 8);
- area A(a) = 24a² + (48 + 24√2)a + 12 + 24√3;
- polar volume V(Z°) = 8/((a + 2)(3a + 3)(2a + 3)).

The polar volume comes from the one orbit of 48 tetrahedra on the corner (a + 2, a + 1, a), and was checked against the hull at a = 1/3, 2. The volume and area formulas were checked against the hull at a = 1/3 and 2. a* is a root of 6a⁴ + 24a³ + 24a² − 5, which is irreducible over ℚ. Its other three conjugates, −2.383, −1.295 and −0.705, are negative.

**B5 tiling: it does not fill space, at any a > 0, in any way.**
- Translations: every one of the 9 zones lies in 4 zone planes, so every belt has 8 faces. A parallelohedron has belts of 4 or 6 only (Venkov 1954; McMullen 1980), so there is no tiling by translations.
- Congruent copies, turned or mirrored, face-to-face or not: the dihedral angles are π/2 + β (125.26°, hexagon–octagon), 3π/4 (135°, octagon–rectangle) and π − β (144.74°, hexagon–rectangle), with β = arctan(1/√2). The angles are the same at every a. Take a generic point inside an edge of a tile. The tiles round it contribute their dihedral angle at that line, or π if the point lies inside one of their faces, and the total must be 2π. Since β/π is irrational (cos 2β = 1/3), the β-count must cancel and the π-parts must sum to 2. An exhaustive search over all such combinations finds none for any of the three edge kinds.

This is a proof, and it covers the Archimedean member (a = 1/√2) too, which is classically known not to tile alone.

**B5 tones of the corners.** The O_h-invariant harmonics have dimensions 1, 1, 1, 2 in degrees 4, 6, 8, 12 (Meyer 1954). All 48 corners form one orbit, so each tone is 48·H(a, a + 1, a + 2). Normalising each harmonic to H(e₁) = 1 gives these values at a*:

| tone | value at a* (on the unit sphere) | its zeros on a > 0 |
|---|---|---|
| Q4 | **0 exactly** (polynomial remainder by the minimal polynomial) | 0.383066 only |
| Q6 | −0.702720 | 1.110008 |
| Q8 | −0.178862 | 1.832584 |
| Q12 (two harmonics) | 0.414898, −0.072505 | 3.289033; 3.203362 |

The chat's 0.248 and 0.128 for Q6 and Q8 use another normalisation; zero or nonzero does not depend on it. So at a* the 48 corners form a spherical 5-design but not a 7-design. An orbit of a finite group is a t-design exactly when every invariant harmonic of degree up to t vanishes on it (Sobolev 1962; Goethals and Seidel 1981). The silence is the crossing of the line with the octahedral group's curve of 5-design orbits.

**B5 canonical form, Mahler volume, roundness.** No special point falls at a*:

| quantity (scale-free) | where it is special on a > 0 | at a* |
|---|---|---|
| canonical-form tone F4 (degree-4 harmonic integrated over the polar) | zero at 0.353858 | nonzero (exact) |
| F6, F8, second F12 | no zero on a > 0 | nonzero |
| first F12 | zero at 0.229609 | nonzero |
| Mahler volume V(Z)V(Z°) = 32(2a³ + 12a² + 21a + 8)/((a + 2)(3a + 3)(2a + 3)) | maximum at the root 0.579320 of 6a⁴ + 32a³ + 45a² − 22 | not critical (exact remainder) |
| roundness 36πV²/A³ | critical at 0.531884 | not critical (2V′A − 3VA′ = 423.59) |

**B1 swaps of the line, and the verdict: NOT FORCED.** No geometric involution of the line fixes a*.
- (i) Similarity. The ratio of the octagon–rectangle edge to the octagon–hexagon edge is 2a/√2 = √2·a. It changes strictly with a, so no two members are similar.
- (ii) Polarity. The polar has 48 triangular faces, so it is not a zonohedron and leaves the line.
- (iii) Galois conjugation. The conjugates of a* are negative, which is off the line.
- (iv) The fold a ↦ −2 − a. It is the only reparametrisation symmetry of the corner formula: it gives the same corner set, so it is the identity on solids. Every tone is even under it (ε = +1), so it forces no zero. Its fixed point a = −1 gives the cuboctahedron, which is off the zonohedron line. An even quantity is critical there only as a fold of the parameter, which is no law.
- (v) Möbius involutions. A parity zero needs an involution fixing a* that maps the zero set of Q4 to itself. That would need a harmonic quadruple among the four roots, and none exists (exact cross-ratios).

**Q4 = 0 at the silent zonohedron is accidental: a crossing, not a forced fixed point. It does not qualify.**

## 3. Shape B: the cuboctahedron with square pyramids on two squares

The solids are the cuboctahedron (corners the signed permutations of (1, 1, 0)) with equilateral square pyramids, apex 2eᵢ, on two of its squares. Dehn is (24 − 12k)√2 ⊗ β for k pyramids (handoff, exact), so it is zero for both two-pyramid placements.

**(i) Prior art for the opposite placement: KNOWN.** It is in Wikipedia's "Rhombic dodecahedron" article, section "Topologically equivalent forms" (read 14 Nov 2026). There it is a space-filling rhombic dodecahedron "with 4 square faces, and 60-degree rhombic faces, and D4h dihedral symmetry, order 16. It can be seen as a cuboctahedron with square pyramids attached on the top and bottom." The article cites Keith Critchlow, "Order in Space: A Design Source Book" (1969), pp. 56–57. Klitzing's incidence-matrix catalogue lists the same solid as "bauco", the bi-augmented cuboctahedron or "4fold rhombohedron", with 12 faces (rhombs and squares), 24 edges, 14 corners and dihedrals 125.264° and 109.471°. It names no space filling. The class is Fedorov's (1885): any non-singular affine image of a parallelohedron is a parallelohedron, as Grünbaum states in his 2010 Bilinski dodecahedron paper.

**Exact here: it is an affine rhombic dodecahedron.** The linear map L = [[1, 0, 0], [0, 1/2, 1/2], [0, 1/2, −1/2]] takes the rhombic dodecahedron (corners 2eᵢ and (±1, ±1, ±1)) exactly onto the opposite solid. Up to similarity, L stretches the rhombic dodecahedron by √2 along a 4-fold axis. L also takes the rhombic dodecahedron's fcc lattice onto the lattice (2, 1, 1), (0, 2, 0), (0, 0, 2) found by the handoff's cover. The solid has 4 zones and every belt has 6 faces (Venkov), so it is a parallelohedron of the rhombic-dodecahedron type. It has 12 faces (4 squares, 8 rhombi of 60°) and symmetry of order 16 (D4h).

**(ii) The swap.** The point inversion acts on the 15 placements of two pyramids. It fixes the 3 opposite placements and swaps the 12 adjacent ones in 6 pairs. Over all 64 placements of any number of pyramids, the solid is centrally symmetric exactly when the placement is fixed by the inversion (exact). Minkowski's conditions are a centrally symmetric solid with centrally symmetric faces (Minkowski 1897). They hold only for the 3 opposite two-pyramid placements:
- the cuboctahedron itself fails on its triangles;
- two opposite pairs fail on trapezoids;
- the octahedron fails on its triangles.

The symmetry orders are 16 for the opposite placement and 4 (C2v) for the adjacent one. Any symmetry permutes the square normals, so it is a signed permutation about the centroid.

**(iii) Adjacent placement (pyramids on +x and +y).**
- It has 13 corners and 12 faces: 2 isosceles trapezoids, 4 rhombi, 2 triangles and 4 squares.
- **No tiling by translations (PROVED).** It is not centrally symmetric, and its trapezoids are not, so Minkowski's theorem excludes a translation tiling.
- **Angles do not forbid a tiling.** The dihedral angles are π − 2β (109.47°, long edge and rhombus–rhombus) and π/2 + β (125.26°). Each edge kind can be surrounded: one 109.47° plus two 125.26° make 2π. So the angle argument that settles the silent zonohedron fails here, and Dehn is zero as well.
- **Cover search.** No octet-aligned periodic cover exists on any torus of index 4 to 48, with all 48 orientations of the cube group, every sublattice searched (8463 sublattices at index 48). Earlier, the handoff stopped at index 24.

**Verdict: UNDECIDED** for tilings by turned or mirrored copies that are not octet-aligned or have a larger period.

**(iv) Is a law forced at the opposite placement?** Only partly. The inversion swap forces central symmetry (B4) and so Minkowski's first condition. But the cuboctahedron and the four-pyramid solid are also inversion-fixed, and they do not tile. The tiling comes from Fedorov's classification (the affine rhombic dodecahedron), not from the swap. Dehn depends on k only, so no placement swap is odd on it. **The shape is known (1969), and the swap selects where a classical necessary condition can hold. It does not qualify as a new law-giving shape.**

## 4. Three unexamined fixed points from the swaps study's leads

The swaps study left 8 leads. Leads 1, 3 and 4 were done on 13 Nov (mirror-hexagonality, pure-swap-6d, palindromic-middles). Lead 6 is a near miss, not a fixed point. Lead 7 (self-dual honeycombs) and Lead 8 (the share h = 1/2) have no single defined quantity to test yet. The three most promising are Lead 2's two site swaps and Lead 5's star turn.

### 4.1 Zinc blende site swap (Lead 2): QUALIFIES (B2 and B3)

The setting is in the units of studies/2026-11-09-cscl-zincblende. Zn sites sit on 2D₃ with weight λ, and S sites on 2D₃ + (1, 1, 1) with weight 0. Write s = (3 + λ)/2, so s runs over (0, 3).
- The Zn cell is P(s) = {q·x ≤ s (q the four tetrahedral normals), |xᵢ ± xⱼ| ≤ 2}.
- The S cell was built from its own definition about (1, 1, 1).
- The swap is s ↦ 3 − s, with fixed point s = 3/2 (equal weights: diamond).

| check (exact; at s = 1/2, 6/5, 13/10, 7/5, 3/2, 8/5, 17/10, 9/5, 5/2) | result |
|---|---|
| Zn cell + S cell = lattice cell | 16 at every sample |
| Dehn(Zn cell) + Dehn(S cell) = 0 | at every sample (the two cells form a lattice fundamental domain) |
| Dehn(P(s)) = −Dehn(P(3 − s)) | at the four pairs: e.g. 12√2 at s = 1/2, −12√2 at 5/2; 72√2/5 at 6/5 |
| **B2: Dehn = 0 at s = 3/2** | **forced**; the fixed cell has 16 corners, 12 triangles and 4 hexagons: the **triakis truncated tetrahedron**, the Voronoi cell of diamond |
| wall area per site pair W(s) on (1, 2) | W = 2((6√2 − 8√3)s² + (24√3 − 18√2)s + 15√2 − 12√3), fitted on 5 points and exact on 3 more |
| **B3: W(s) = W(3 − s), W″ = 24√2 − 32√3 < 0** | **forced maximum at s = 3/2**: W = 3√2 + 12√3 ≈ 25.03 (at s = 1/2 and 5/2: (21√2 + 4√3)/2 ≈ 18.31) |

**Prior art.** The triakis truncated tetrahedron is the Voronoi cell of diamond, and it fills space (Conway, Burgiel and Goodman-Strauss, "The Symmetries of Things", 2008; Wikipedia "Space-filling polyhedron"). So its Dehn zero is known as a consequence. The wall-area maximum on the zinc blende weight walk is the exact analogue of the swaps study's Kelvin result (its K3). It was not found in the sources checked, but no literature search was made for it.

### 4.2 Rock salt site swap (Lead 2): parity VACUOUS; a kink maximum

A sites are the even-sum integer points with weight λ, and B sites the odd-sum points with weight 0, at unit spacing. The A cell is {|xᵢ| ≤ (1 + λ)/2, |xᵢ ± xⱼ| ≤ 1}. The swap λ ↦ −λ has fixed point λ = 0, where both cells are unit cubes.

| check (exact; λ = ±3/4, ±1/3, ±1/5, 0, 1/2) | result |
|---|---|
| cells sum to the lattice cell 2; Dehn sum 0 | yes |
| Dehn of each cell | **0 at every weight**: the cell is a cube chamfered on its 12 edges, with dihedrals 90°, 135° and 120°, all rational multiples of π. Parity holds, but trivially |
| W(λ) = 6(1 − \|λ\|)² + 3√2(2\|λ\| − λ²) | at every sample; even |
| shape at λ = 0 | a **kink**: one-sided slopes ∓(12 − 6√2); W is convex on each side |

The swap forces criticality only in Clarke's sense (0 lies between the one-sided slopes). That the cube is the maximum comes from the computed slope sign, not from concavity. **Weak: the object is the cube, and nothing is forced beyond the symmetric kink.**

### 4.3 The small stellated and great dodecahedra (Lead 5): a forced smooth MINIMUM (B3, convex)

These use the flag line of the stars census, S*(μ) = G·Δ(μ), with t_min* the largest x·y over the line solid and its flag-wise antipol. The turn is μ ↦ c/μ with fixed point hR. The study asked which swap carries the minimum.

| | c | hR | t_min*(hR) | branch through hR, t = A + Bμ + C/μ |
|---|---|---|---|---|
| small stellated dodecahedron | 24 + 8√5 | 2 + 2√5 | 15 − 6√5 | A = 15/2 − 7√5/2, B = −5/4 + 5√5/8, C = −5 + 5√5 |
| great dodecahedron | 984 + 440√5 | 22 + 10√5 | 15 − 6√5 | A = 15/2 − 7√5/2, B = −145/16 + 65√5/16, C = 20 + 10√5 |

On both sides of hR one corner pair is the maximum. Its branch was fitted on 3 exact points at hR ± k·10⁻⁴ and is exact on the 4th. The turn symmetry t*(μ) = t*(c/μ) is exact at hR ± 10⁻⁴. The same branch continues through hR (left and right coefficients agree) with C = B·c, so it is itself turn-symmetric. Hence t′(hR) = B − C/hR² = 0 exactly, which is **forced by the turn** (symmetric criticality). C > 0 makes the branch convex, so t″(hR) > 0 (0.0456 and 0.00097) and **the turn's fixed point is a smooth minimum**. That answers Lead 5: the turn itself carries the minimum. It is critical by symmetry and a minimum because the branch is convex, the mirror case of the convex polytopes, where the branch is concave.

## 5. Summary

| point | swap fixing it (B1) | forced law | qualifies? | shape known? |
|---|---|---|---|---|
| √3 on the C–O line (control) | turn μ ↦ 3/μ | t_min maximum 5 − 2√3 (B3) | yes | yes (#81, #43) |
| 3/2: Kelvin (control) | CsCl swap | Dehn 0 (B2), wall area maximum (B3) | yes | yes (Kelvin 1887) |
| 8/5 (random control) | none | none | no | — |
| silent zonohedron, a* ≈ 0.3831 | none (5 kinds of swap excluded) | none: Q4 = 0 is a crossing | **no** | the line's members are classical zonohedra; a* as the 5-design point: chat 13–14 Nov |
| CO + 2 opposite pyramids | placement inversion | central symmetry, hence Minkowski's first condition (B4); the tiling itself is Fedorov's | **no** (partly forced, classical) | yes (Critchlow 1969; Klitzing "bauco") |
| CO + 2 adjacent pyramids | none (swapped with its inverse) | no translation tiling (Minkowski) | — | not found |
| zinc blende s = 3/2 | site swap | Dehn 0 (B2), wall area maximum (B3) | **yes** | the cell yes (diamond Voronoi); the W law not found |
| rock salt, λ = 0 | site swap | Dehn vacuous; kink maximum | weak | yes (cube) |
| SSD and GD at hR | the turn | t_min* critical (forced), smooth minimum | **yes** | the solids yes; the minimum was observed on 9 Nov (stars census), proved smooth here |

**Lower true outcome.** A swap's fixed point carries a law when the swap is geometric and parity, symmetry with concavity or convexity, or extra symmetry act on a natural quantity there. Every point where this happened today is a known shape. The new exact content is:
- the wall-area maximum at the diamond cell;
- the smooth forced minimum of the stars' turn;
- the proof that the silent zonohedron fills space in no way;
- the proof that its silence is not forced.

## LEADS

1. **The silent zonohedron as a 5-design.** It is the 48-point O_h-orbit 5-design on the zonohedron line. The 5-design orbits form a curve on the sphere (Goethals–Seidel). Test where other natural lines of zonohedra (the B3 seed (a, b, 1), the two-parameter family) cross that curve, and whether any crossing is also a 7-design: Q4 = Q6 = 0, isolated points by dimension count.
2. **The adjacent two-pyramid cuboctahedron.** It needs a method beyond octet-aligned periodic covers: a local corona search with the long edge (2√2, 109.47°) as seed, which must be surrounded by exactly one 109.47° and two 125.26° wedges. Or a Hadwiger-type invariant that sees more than Dehn.
3. **Wall-area laws on all ten networks of #53.** Every network with a site swap has a forced Dehn zero and an even W. Test concave, convex or kink at each fixed weight. The CsCl and zinc blende cases are concave; rock salt has a kink.
4. **Stars: the sign rule.** Convex lines have a concave branch at the turn and stars of density 3 a convex one. Test the great stellated dodecahedron (local maximum at the turn, census) and the Schläfli–Hess stars for the sign of C − B·c and of C, and whether density alone decides it.
5. **Fold fixed points.** The silent zonohedron's corner formula folds at a = −1 onto the cuboctahedron. The extended line a ∈ (−1, 0) runs through non-zonohedral solids with corners the signed permutations of (|a|, a + 1, a + 2), from the cuboctahedron to Kelvin's cell. Test whether that stretch carries its own Q4 zero.

## Sources checked

**Literature for Shape B (web searches, 14 Nov 2026):**

- "cuboctahedron with square pyramids on two opposite square faces space-filling" (results: Wikipedia tetrahedral-octahedral honeycomb, MathWorld Cubic Close Packing and Cuboctahedron, mathematische-basteleien, matematicasvisuales);
- "bi-augmented cuboctahedron" (Klitzing bauco and ebauco pages; Wikipedia diminished rhombic dodecahedron, biaugmented truncated cube);
- "rhombic dodecahedron stretched along fourfold axis four square faces eight rhombi space filler" (Wikipedia Rhombic dodecahedron, IUCr model page, steelpillow Five Space-Filling Polyhedra, Wikipedia trapezo-rhombic dodecahedron, Wolfram Demonstrations, MathWorld Elongated Dodecahedron);
- "Goldberg convex polyhedral space-fillers list augmented cuboctahedron" (Wikipedia Space-filling polyhedron, Expanded cuboctahedron, robertlovespi);
- "cuboctahedron augmented two adjacent square faces pyramids tiles space" (nothing on the adjacent solid);
- a site-limited search of MathWorld, McCooey's site and Hart's site.

**Other sources.**

- **Pages read in full:** Klitzing "bauco"; Wikipedia "Rhombic dodecahedron" (the source of the Critchlow citation; Critchlow's book itself was not seen); MathWorld "Space-Filling Polyhedron" (its Goldberg 1972, 1974a, 1974b, 1977, 1979 and Grünbaum–Shephard 1980 references, none with the shape); Inchbald's "Five Space-Filling Polyhedra" page; Wikipedia "Space-filling polyhedron".
- **Reference library:** Grünbaum–Shephard 1980 ("Tilings with congruent tiles": parallelohedra, Fedorov, Minkowski); Grünbaum 2010 (Bilinski dodecahedron and assorted parallelohedra: affine images of parallelohedra); Fedorov 1885; the library's Goldberg 1972, 1974 and 1982 files (pentahedra, decahedra), not opened. McCooey's and Hart's catalogues returned no page on the shape. No Johnson-solid tiling list mentions it, since it is not a Johnson solid (its faces include rhombi).
- **Classical results named:** Palais 1979, Lindelöf 1869, Minkowski 1897, Fedorov 1885, Venkov 1954, McMullen 1980, Meyer 1954 (cubic harmonics), Sobolev 1962, Goethals–Seidel 1981, Dehn 1901, Kelvin 1887, Conway–Burgiel–Goodman-Strauss 2008.
- **Repository:** studies 2026-11-13-swaps-and-fixed-points (catalogue, K1–K5), 2026-11-14-chat-handoff (Leads 7, 8; cover model), 2026-11-13-near-but-never-on (pattern), 2026-11-09-cscl-zincblende (cells), 2026-11-09-regular-stars-census (flag line, turn values), 2026-11-04-dehn-screen, 2026-11-04-tetra-sweep, 2026-11-13-mirror-hexagonality, pure-swap-6d and palindromic-middles (leads done). Concordance ledger entries [74], [219], [220] and the 13 Nov swaps entry.

## Faults fixed on the way

The pilot (two runs) had two wrong expectations in checks, not in the mathematics.

- The belt count: every zone of the silent zonohedron has a belt of 8, not 6 for the Kelvin zones.
- The triakis truncated tetrahedron's face list: 12 triangles and 4 hexagons, 16 corners. The check had wrongly expected pentagons.

Both pilots were first refused by the pre-flight gate (ledger [220]). The overrides are recorded in the plans: the cover search extends to indices never searched, as DICTO's task asks, and the battery uses new methods.

## Ledger line

Concordance ledger entries of 14 Nov 2026: "forced fixed points: silent zonohedron", "forced fixed points: two-pyramid cuboctahedra", "forced fixed points: three lead fixed points".

DICTO · dictospheres.com
