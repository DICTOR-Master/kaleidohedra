# The fair 14-face die: the full new-shape protocol (18 Nov 2026)

DICTO · dictospheres.com

**Question (DICTO, 18 Nov 2026):** "it is a new shape, it needs to be hit with everything that we ever do or find out about new shapes, where it fits in our studies exactly; if none, create." He later added: "is it a 4th-dimension shadow, is it in the 600, 120 etc".

**Answer.** No such procedure existed, so one was written: `papers/new-shape-protocol.md`, 21 steps. This study runs every applicable step on the fair 14-face die (placeholder name "Fair Fourteen"; DICTO names it). All seven scripts end FINAL ok (81 checks in the five computing scripts, plus the figure and library-search controls).

The die is an isogonal solid with symmetry group Oh: one corner orbit, two edge orbits and two face orbits. It is not a uniform, Johnson, Catalan, zonohedral or parallelohedral solid. It sits at **no** named station of the cube–octahedron line, and no law found so far singles it out: its fairness is a crossing, not a forced point.

It does not tile space alone (Dehn invariant nonzero). It **does** tile together with its swap partner S(3 − μ_f), as a CsCl pair. Its landing directions are exactly the bcc 14-shell. Those are the 14 corner directions of the rhombic dodecahedron, which is the 24-cell's corner-first shadow, and the 24-cell lies in the 600-cell. The solid itself **cannot** be a shadow, section or corner subset of any polytope with coordinates in a field of degree 2^k (600-cell, 120-cell, 24-cell, tesseract, 16-cell, 5-cell), whenever the map is defined over that field. Its affine invariant has degree 6, and its field is heptagonal.

Labels: **exact** (symbolic algebra or proof), **certified** (interval arithmetic, from God's Dice), **computed** (floating point or Monte Carlo). Computation, scripts and drafting were done with Claude (Anthropic).

## The shape

S(μ) = [−1, 1]³ ∩ {|x| + |y| + |z| ≤ μ} at μ_f = 1 + √(2T), with T = tan(π/14)·tan(2π/7) and μ_f = 1.7565821359…

- Corners: the 24 permutations of (±1, ±b, 0), with b = μ_f − 1 = 0.7565821359.
- Faces: 6 squares of side √2·b = 1.069969, and 8 hexagons. The hexagons are truncated triangles with alternate edges √2·b and √2(1 − b) = 0.344245.
- Every face subtends 4π/14 from the centre.

Known before this study (`studies/2026-11-18-gods-dice`): the exact value, its uniqueness on the line, the minimal polynomial μ⁶ − 6μ⁵ − 3μ⁴ + 52μ³ − 97μ² + 74μ − 13, the rolling check, and the prior art. Existence is an instance of Diaconis and Keller's "fair by continuity" (1989). Rawlins (US 11033806) uses the same equal-solid-angle rule for other dice. The print model is in `../2026-11-18-gods-dice/print/`.

## Results, one row per protocol step

Control shape: Kelvin's truncated octahedron (TO), μ = 3/2.

| # | Step | Fair die | Label | Control |
|---|---|---|---|---|
| 1 | Exact definition | b is the root of y⁶ − 18y⁴ − 4y² + 8 (irreducible) near 0.7566; the minimal polynomial of μ_f reproduces God's Dice; p(square) = 1/14 to 50 digits | exact | T is a root of x³ − 9x² − x + 1 to 55 digits |
| 2 | Counts, group, orbits | 24 corners, 36 edges, 14 faces, Euler 2; group exactly Oh (order 48); orbits: corners 1, edges 2, faces 2 (**isogonal, not isohedral**); one circumradius 1.253960 | exact | TO the same |
| 3 | Known solid? | Similarity invariant x = b/(1 − b) = 3.1081619210 (ratio of the parallel hexagon edges), degree 6: 13x⁶ + 4x⁵ − 78x⁴ − 144x³ − 116x² − 48x − 8. Not uniform or Johnson (faces not regular), not Catalan (2 face orbits), not a zonohedron or parallelohedron (hexagons not centrally symmetric) | exact | TO: x = 1 |
| 4 | Station of its line? | **None.** The gcd with every station's minimal polynomial is 1: walls 1, 2, 3; Kelvin 3/2; Icosaxes φ (#94); turn fixed point √3; Q6 zero 1.34543; Q8 zero (√13 − 1)/2; Mahler maxima (2μ³ − 9μ + 6, 2μ³ − 9μ² + 21); canonical order-4 anisotropy root 1.69259. Under the law-giving census definition (2026-11-15) fairness is a crossing: no involution of the line fixes it | exact | the stations are re-found by their polynomials |
| 5 | Turn and swap | Turn partner 3/μ_f = 1.7078621 (p(square) 0.06421, not fair). Swap partner 3 − μ_f = 1.2434179 (p(square) 0.00916). Turn Law t_min(μ_f) = 1.5355558, 0.00034 below the maximum 5 − 2√3 at √3 | exact | TO t_min = 3/2 |
| 6 | Measures | Volume 5.4944476716 (degree 6), area 16.3490750852 (degree 12), IQ 0.7813055 (line maximum 0.781640 at √3), Mahler 14.2454806 (degree 6; Kelvin 128/9), Ω(S;0) = 48/μ_f² = 15.5562285 | exact (closed forms checked against the hull at 6 points) | TO volume 4, area 3 + 6√3, Ω 64/3 |
| 7 | Dehn | 24√2(3 − 2μ_f) ⊗ arccos(1/√3) = −17.4174 ⊗ arccos(1/√3) ≠ 0; the independent PSLQ screen agrees | exact; screen computed | cube and TO zero, octahedron nonzero |
| 8 | Harmonic fingerprint | Corners: Q4 0.1203455 (exact: (5/2)√(7/12)·\|⟨x⁴+y⁴+z⁴⟩ − 3/5\|, with a cubic minimal polynomial), Q6 .5059, Q8 .2274, Q10 .1461, Q12 .3181, Q14 .1189, Q16 .2986; Ŵ4 −0.1593, Ŵ6 −0.0132; none silent. Landing (normals weighted by solid angle) = **bcc 14-shell**, Q4 = √(7/12)/21 exactly | Q4 exact, others computed | fcc .1909/.5745, bcc .0364/.5107 |
| 9 | Tiles alone? | **No** (Dehn ≠ 0; Debrunner 1980). The forced-sector search is not needed | exact | — |
| 10 | Tiles with partners? | **Yes, with S(3 − μ_f) as a CsCl pair**: die on 2ℤ³, partner on 2ℤ³ + (1,1,1). V(μ) + V(3 − μ) = 8 identically, the pair's Dehn sum is 0, there is no interior overlap with any of 34 neighbours (separating axes), and 200 000 random points each lie in exactly one piece. With regular octahedra: n/a (that filling holds only on chamber II) | exact identity; overlap computed | an oversized partner overlaps (the test can fail) |
| 11 | Foam wall area | W(μ_f) = 1.6587612 per unit volume, below Kelvin's 1.67404. Exact: W(μ) = 15/4 − 9μ/2 + 3μ²/2 + √3(−μ² + 3μ − 3/2), largest only at 3/2 | exact | Kelvin 1.67404 reproduced |
| 12 | Interlocking slab | n/a: the CsCl tiling has no flat one-tile-thick layer (the Concordance's CsCl-pairs cell) | — | — |
| 13 | Halves | Turning one half 60° about a 3-fold axis, or 45° about a 4-fold axis, gives a dented solid: no convex gyro form | computed | CO turned 60° is convex (J27); TO dented |
| 14 | Vacuus | 36 fins in 2 kinds: 24 square–hexagon fins (apex 50.508495°) and 12 hexagon–hexagon fins (15.779003°), so not isofin. One strut length. Both apex angles are **irrational multiples of π, exactly**: 2cos has minimal polynomial 7z³ − 70z² + 84z − 8 and 49z⁶ + 10976z⁴ − 50176z² + 32768 respectively, neither monic. Kind: **heart** | exact | CO fin 60° integral; cube fin non-integral |
| 15 | Origami | Two nets: square fan 202.034°, hexagon fan 198.862°. Both are below 360°, so it folds as modular origami | computed | — |
| 16 | Centre pyramids | 6 square pyramids of volume 0.381611 and 8 hexagon pyramids of 0.400598, all of solid angle 4π/14. Dehn of each pyramid is nonzero (screen). Three "equal share" points of the line are distinct: equal solid angle μ_f = 1.756582, equal face area μ_a = 1.766745 (2b² = (√3/2)(μ² − 3b²)), equal pyramid volume μ_v = 1.773753 (root of 2μ³ − 2μ² − 5μ + 4). The insphere point is √3 = 1.732051 | exact equations; screen computed | the cube's pyramid has Dehn zero |
| 17 | Field / 4D host | See below. **Not a K-shadow** of any polytope with coordinates in a field of degree 2^k; the landing directions **are** a 24-cell shadow | exact | TO: x = 1, passes |
| 18 | Densest packing | not run: the studies have no tested script (Betke–Henk 2000 is in the library) | — | — |
| 19 | Prior art | Full text of 348 library PDFs: "fair dice" only in Diaconis–Keller 1989; "14-sided/14-face" in 5 files, none about dice; no tan(π/14). OEIS digit searches for μ_f, T and x_f: no results. Earlier sources in God's Dice. McCooey's catalogue not checked (blocked). **Not found** in the sources checked | — | control term "Diaconis" found |
| 20 | Placement | below; Concordance patch `data/concordance-patch.json` | — | — |
| 21 | Render and model | `figures/fair-die-full.png`: solid, see-through shell with the Vacuus struts, and the pull-apart of the 14 centre pyramids. Print model in God's Dice | computed | 14 equal solid angles checked in the figure script |

### Step 17: the field / 4D-host test (DICTO: "is it a 4th-dimension shadow, is it in the 600, 120 etc")

- **Affine invariant.** The hexagon edges (0, −b, b) and (0, 1 − b, b − 1) are parallel. Their length ratio x = b/(1 − b) is kept by every affine map. x_f has degree 6 over ℚ, and b_f² = 2T with T cubic in ℚ(cos 2π/7) (T = 9 − 4c − 16c², c = cos 2π/7).
- **Statement (elementary, checked case by case).** Let Q have corner coordinates in a field K. Take a corner subset, a section by a hyperplane defined over K, or a parallel projection along a direction defined over K. The result has corners in K, so its ratios of parallel edges lie in K, and any affine image keeps them. An element of degree 6 cannot lie in a field of degree 2^k, because the degree of an element divides the degree of the field.
- **Consequence.** The fair die is not obtained this way, up to affine maps, from any polytope with coordinates in ℚ, ℚ(√2), ℚ(√5) or ℚ(√2, √3, √5). That covers the 600-cell, 120-cell, 24-cell, tesseract, 16-cell, 5-cell and the H3/H4 orbit polytopes in standard coordinates.
- **Scope.** Projections along directions not defined over K are not covered.
- **Control.** Kelvin's TO has x = 1, which is rational, and it is a facet of the 4D permutohedron (#105).
- **The harmonic signature does live in the Queens** (exact). The die's 14 landing directions, equally weighted at μ_f, are the 14 corner directions of the rhombic dodecahedron. These are exactly the corner directions of the 24-cell's corner-first shadow (8 corners (±1,0,0,0) and 16 corners (±½,±½,±½,±½) projected along w). The 24-cell's 24 corners are corners of the 600-cell (120 corners checked). So the die's landing law is a 4D shadow even though the solid is not one.

## PLACEMENT

**Concordance** (`data/concordance-patch.json`, RFC 6902 operations; concordance.json is not edited here):
1. A new family row, "the fair 14-face die (cube–octahedron line, μ_f)". All 9 test cells are filled: 6 values and 3 n/a with reasons (forced-sector search, interlocking, and foam wall area given for the CsCl pair).
2. The **CsCl pairs (#90)** foam cell is extended with the fair pair's W = 1.658761.
3. On the **cube–octahedron sweep** row it is a new point of the line, but it is not a station of any test, so that row is unchanged.
4. The **centre pyramids** row: the die's pyramids are the equal-solid-angle pyramids. They are not isohedral and their Dehn is nonzero. This is recorded in the new row, not in the T/C6/R12/RT row.

**Papers** (numbers from the Concordance's `papers`):
- #90 (the cube–octahedron line and its CsCl pairs, Prop. 6). The die and its partner S(3 − μ_f) are one CsCl pair.
- #48 The Golden Split, Theorem 4. In its x-form the die is T(x_f), x_f = 3.10816, and T(1/x_f) is the partner. Kelvin is x = 1 and Icosaxes x = τ.
- #94 The Silent Golden Station: harmonic sweep; the die is not silent.
- #51 The Delian Bond: power-line member w_f = (3/2 − μ_f)/2 = −0.128291.
- #87 DICTO Vacuus Solids: a heart-kind entry with 2 fin kinds and 1 strut.
- #100 The Dehn Test Picks the Lone Tilers: the die is not a lone tiler but tiles with a partner.
- #44, #77, #92, #93 (centre pyramids): an equal-solid-angle pyramid set.
- #105: the control's 4D home.
- Drafts: the Turn Law (turn partner, t_min) and Geometry Gives Laws (aim 2: fairness is a crossing, not a forced law).

**Books:** Book Two, *Space-Fillers and Lattice Moves* (the CsCl pair tiling), and Book Three, *DICTONIC Bonds* (the golden bond slider), both through these papers. Classed by the solid, it belongs with the cube in the cube colour (#488e48).

**App:** the shape needs one home (no crossover), which is a Polyhedraverse entry. The DICTONIC world's Golden bond slider already sweeps T(x) with T(1/x). A stop at x_f = 3.10816, labelled with the die, would show the fair pair, and it would link to the Polyhedraverse entry. This is a proposal only; no app was changed.

## LEADS
1. **Densest lattice packing** (step 18). Write and calibrate a Betke–Henk script; the TO, with density 1, is the control.
2. **Equal-share points.** Solid angle (1.75658), face area (1.76675) and pyramid volume (1.77375) are three distinct "fair" points just past √3. Physical dice may fall between them. A bouncing simulation or a print test would show which law a real roll follows.
3. **Heptagonal lead (outside the plan).** The field ℚ(cos 2π/7) is the field of 7-fold symmetry. Is the die a shadow of an A6 or 7-fold polytope along a direction defined over that field? Not computed.
4. **Fair dice on other lines.** Run the same protocol on the fair point of the icosahedron–dodecahedron line (32 faces) and the tetrahedron line.
5. McCooey's catalogue comparison (blocked; `mccooey-comparison`).

## Files
- `scripts/fdlib.py`: shared definitions; exact minimal polynomials at b_f by resultants.
- `scripts/s01_identity_stations.py`: steps 1–5, 29 checks.
- `scripts/s02_measures.py`: steps 6–8, 19 checks.
- `scripts/s03_space.py`: steps 9–13, 10 checks.
- `scripts/s04_vacuus_pyramids.py`: steps 14–16, 11 checks.
- `scripts/s05_field_4d.py`: step 17, 12 checks.
- `scripts/s06_figure.py`: the figure.
- `scripts/s07_library_search.sh`: library full-text search.
- Logs and JSON are in `data/` (one `.log` per script, each ending FINAL ok), with `data/s07-oeis-queries.txt` and `data/concordance-patch.json`.
- All runs were on a compute machine, each under 5 minutes.
- Reused methods, each credited at its point of use: `_lib/methods.py` overlap; `2026-11-04-dehn-screen/scripts/dehn.py`; the twist of `2026-11-04-halves/scripts/sweep_twist.py`; the fingerprint of `2026-11-18-gods-dice/scripts/fair_identity.py` (Steinhardt–Nelson–Ronchetti 1983); the closed forms of `2026-11-04-mahler-sweep` and `2026-11-10-canonical-sweep`; t_min of `2026-11-09-turn-theorem`.
- Fault fixed on the way: polar volumes were first computed from face planes rounded to 9 digits, which failed the closed-form check. The unrounded planes are now used.
