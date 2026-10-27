# 4D shadows and slices against deltahedra (study, 2026-10-27)

Credit: DICTO (the idea), with Claude (computation). Research only, no app changes.

**One-line conclusion.** DICTO's prediction holds where the 4D shadow is a deltahedron pattern at all: no non-regular
all-triangle shadow or slice of the 5-, 16-, 24- or 600-cell is equilateral, the two that carry a convex deltahedron's
face pattern are variants of it (triangular bipyramid, edge ratio √(12/7) = 1.309; octahedron, ratio 2/√3 = 1.155,
which fills space where the regular octahedron cannot), and the 600-cell's icosahedral shadow and slice carry the
patterns of non-convex (dented / augmented) deltahedra and of none of the 8; regular deltahedra appear only as the
4D cells and vertex figures themselves, while 4 of the 15 non-regular patterns can be no deltahedron at all. Of the six large 600-cell slice patterns, one (48 vertices) has an exact
equilateral non-convex form with the slice's own symmetry (Slice-48, placeholder name); the other five have none with
their full symmetry.

**Status:** done (projections, layers and slices along all four principal directions of all four polytopes; exact
comparison; attachability of the two variants; Shadow-17 = two J11; the six large slices solved exactly under their
full symmetry, see the last section). Open: equilateral forms of the five other large patterns with less symmetry, and
the rotation-subgroup systems of V30 and V48 (too large for the Groebner basis).

DICTO's idea: "4th dimensional shadows may more closely represent any new deltahedron type family than they do the
original ones." Added: "compared old ones were different shapes with different attachability."

## Question

For the 4D regular polytopes whose 2-faces are all triangles (5-cell, 16-cell, 24-cell, 600-cell): are their 3D
shadows (parallel projections) and slices (hyperplane sections) closer to variant deltahedra (a known deltahedron's
face pattern with another shape: unequal edges, or dented) than to the 8 convex deltahedra, and do the variants attach
differently from the regular ones?

## Method

All arithmetic exact in Q(√5) (`scripts/q5.py`: numbers a + b√5 with rational a, b; exact signs). Floats only seed
the convex hulls; every hull face is then verified exactly (all points on one side of the exact plane, exact 2D hull
of each face, every edge in exactly two faces, Euler characteristic 2).

- `scripts/polytopes.py`: vertices. 5-cell: e_1…e_5 in R^5 (a regular 4-simplex has no rational coordinates in R^4),
  always projecting out (1,1,1,1,1) as well; 16-cell ±e_i; 24-cell permutations of (±1,±1,0,0); 600-cell (radius 2)
  permutations of (±2,0,0,0), (±1,±1,±1,±1), even permutations of (±φ,±1,±1/φ,0). Checked counts: 5/10/10/5,
  8/24/32/16, 24/96/96 (24 octahedral cells), 120/720/1200/600 (vertices/edges/triangles/tetrahedra). Directions:
  centroid of a vertex, an edge, a triangle and a cell through vertex 0, minus the centre.
- `scripts/shadows.py`: for each direction d, an exact orthogonal frame of the 3-space ⟂ d. **Shadow** = convex hull
  of all projected vertices (the outline solid). **Layers** = hull of the projected vertices of one height x·d (the
  nested shells of the shadow). **Slices** = hyperplane sections x·d = h through the centre and at every vertex height
  (vertices on the hyperplane plus every edge crossing it). Each solid: face pattern, degrees, exact squared edge
  lengths, exact dihedral cosines. 223 records, 157 solids (`data/shadows.json`).
- `scripts/classify.py`: every all-triangle solid against the 8 convex deltahedra by graph isomorphism (networkx;
  reference graphs built from coordinates and checked: planar, 3n−6 edges, degree sequences 3333 … 5^12; the snub
  disphenoid by forcing its D2d template equilateral). Named patterns: n-gonal bipyramids, pentakis dodecahedron,
  pentakis icosidodecahedron. For the remaining patterns, a numerical search for an equilateral form (Tsuruta et al.'s
  method: least squares on edge lengths, started from the shadow and 11 perturbations; accepted only with residual
  < 1e-10, no self-intersection, no 180° edge, positive volume). `data/all-triangle-matches.json`.
- `scripts/attach.py`: for the two variants, face congruence, exact dihedral angles, all edge stars (≤ 8 tiles)
  closing exactly to 360° (sympy: ∏(cos θ + i sin θ) = 1) from a pool of the variant, the regular counterpart,
  tetrahedron and octahedron (each scaled to that edge) and every other solid of the same 4D polytope with that edge
  length, and a face-to-face test round each star. Also the exact realisations of the two icosahedral patterns.
  `data/attachability.json`.
- `scripts/render.py`: the two renders.

Run on dicto-big-brother: `cd ~/kres-tmp/4d && PYTHONPATH=scripts ~/geom/bin/python scripts/shadows.py` then
`classify.py`, `attach.py`, `render.py` the same way.

## Results

Every all-triangle shadow, layer and slice, once each (repeats with the same graph, exact edge lengths and dihedral
angles are dropped: slices at ±h of the centrally symmetric polytopes, and for the 5-cell vertex-first = cell-first
and edge-first = face-first, which are the same axes by symmetry and give identical data). "Regular" = all edges
equal. Edge ratio = longest/shortest edge, exact.

| 4D source | Solid | V, F | Degrees | Face pattern match | Edge ratio | Deltahedron with this pattern | Attaches differently? how |
|---|---|---|---|---|---|---|---|
| 5-cell | vertex-first shadow; layer; slices at 4D-cell heights | 4, 4 | 3333 | tetrahedron | 1 | **regular** (it is a 4D cell) | same as regular |
| 5-cell | central vertex-first slice | 4, 4 | 3333 | tetrahedron | 1 | **regular** | same |
| 5-cell | **edge-first shadow** (TBP-5) | 5, 6 | 44433 | **triangular bipyramid J12** | √(12/7) = 1.309 | **variant** of J12 (convex, unequal edges) | **yes**: faces (√2, √(7/6), √(7/6)) match no face of J12 or of the 5-cell family; base edges 120° (cos −1/2): 3 copies close face to face round a base edge, which J12 alone never does; lateral edges arccos(1/8) = 82.82°: no star at all, so neither TBP-5 nor J12 fills space |
| 16-cell | vertex-first shadow; layer 0; central slice | 6, 8 | 444444 | octahedron | 1 | **regular** (vertex figure) | same |
| 16-cell | **edge-first shadow** = central edge-first slice (OCT-16) | 6, 8 | 444444 | **octahedron** | 2/√3 = 1.155 | **variant** of the octahedron (convex) | **yes**: it is two cube-centre pyramids base to base (square side √2, apices √2/2 off it); dihedrals 90° (4 square edges, stars of 4) and 120° (8 side edges, stars of 3), so it **fills space alone, face to face** (cubes of side √2 cut into their 6 centre pyramids, paired across faces = square bipyramidal honeycomb); the regular octahedron (109.47°) fills only with tetrahedra; no face-to-face contact with the regular tetrahedra/octahedra of its own family (isosceles vs equilateral faces; 2·90° + 70.53° + 109.47° = 360° exactly but the faces do not match) |
| 16-cell | face-first shadow | 8, 12 | 66444444 | hexagonal bipyramid | √(5/2) = 1.581 | **none can exist** (proof below) | — |
| 16-cell | central face-first slice | 8, 12 | 66444444 | hexagonal bipyramid | √3 = 1.732 | none can exist | — |
| 16-cell | cell-first layers and slices | 4, 4 | 3333 | tetrahedron | 1 | regular (4D cell) | same |
| 24-cell | vertex-first layer 0; cell-first layers ±1 | 6, 8 | 444444 | octahedron | 1 | regular (4D cell / vertex shell) | same |
| 600-cell | vertex-first layers (two sizes) | 12, 20 | 5^12 | icosahedron | 1 | regular (vertex shells) | same |
| 600-cell | cell-first layers (3 tetrahedra, 1 octahedron) | 4/6 | 3333 / 444444 | tetrahedron / octahedron | 1 | regular | same |
| 600-cell | **vertex-first shadow** = central vertex-first slice | 42, 80 | 6^30 5^12 | pentakis icosidodecahedron (none of the 8) | 2/√3 = 1.155 | **non-convex: the 12-dented icosahedron** (placeholder name), exact | no edge star with itself (dihedrals 164.48°, 155.91°: two < 360°, three > 360°), as for the icosahedron (138.19°) |
| 600-cell | **vertex-first slices at x·v = ±2** | 32, 60 | 6^20 5^12 | pentakis dodecahedron (none of the 8) | √(3/4 + √5/4) = 1.144 | **non-convex: augmented dodecahedron** (placeholder) and **dented dodecahedron = excavated dodecahedron**, exact | no edge star with itself (161.05°, 149.10°) |
| 600-cell | edge-first layer 0 | 12, 20 | 10^2 4^10 | decagonal bipyramid | φ√2 = 2.288 | **none can exist** | — |
| 600-cell | face-first layer 0 | 8, 12 | 66444444 | hexagonal bipyramid | √2 | **none can exist** | — |
| 600-cell | edge-first slices at ±(1+√5) | 17, 30 | 6^5 5^12 | none of the 8 | 2.927 | non-convex equilateral form: **two J11 base to base** (Shadow-17, placeholder; exact, see its section) | not studied |
| 600-cell | vertex-first slices at ±(√5−1) | 72, 140 | 10^12 5^60 | none | φ√2 = 2.288 | none with Ih or I symmetry (exact, last section) | — |
| 600-cell | edge-first slices at ±(3+√5)/2 | 32, 60 | 7^10 5^22 | none | φ² = 2.618 | none with D5d or D5 symmetry (exact)* | — |
| 600-cell | face-first slices at ±(4+2√5)/3 | 30, 56 | 8^6 5^24 | none | 3.618 | none with D3d symmetry (exact) | — |
| 600-cell | cell-first slices at ±(5+3√5)/4 | 28, 52 | 9^4 5^24 | none | φ√2 = 2.288 | none with Td or T symmetry (exact) | — |
| 600-cell | cell-first slices at ±(3+√5)/2 | 42, 80 | 10^6 5^36 | none | 4.815 | none with Td or T symmetry (exact) | — |
| 600-cell | cell-first slices at ±(2+√5)/2 | 48, 92 | 8^12 5^36 | none of the 8 | 3.618 | **non-convex equilateral form with Td symmetry: Slice-48** (placeholder; exact) | not studied |

Heights are x·d with d the unnormalised direction vector of `polytopes.py` (600-cell vertex-first: d = (2,0,0,0), so
x·d = 2 means x_1 = 1).

\* An earlier 40-start run with a dense solver reported an equilateral form at start 19 (residual 8e-15, non-convex),
but its coordinates were not kept. The exact solve (last section) shows that no D5d- or D5-symmetric form exists, so
that form, if real, had less symmetry; left undetermined.

Exact squared edge lengths and dihedral cosines of every row are in `data/shadows.json`. Examples: TBP-5 edges² 2 (3)
and 7/6 (6), dihedral cosines −1/2 and 1/8; OCT-16 edges² 2 (4) and 3/2 (8), cosines 0 and −1/2; 600-cell vertex-first
shadow (radius 2) edges² 6 − 2√5 (60) and 9/2 − 3√5/2 (60); vertex-first slice at 2: edges² 6 − 2√5 (30) and
28 − 12√5 (60).

No all-triangle shadow or slice of the 24-cell exists except its octahedral layers; its shadows and slices have square
or hexagonal faces (its cells are octahedra, and they project or cut into squares and hexagons).

### Count (distinct all-triangle solids, 27)

| Kind | Number | Where |
|---|---|---|
| regular convex deltahedron (tetrahedron, octahedron, icosahedron only) | 12 | vertex-first shadows of the 5- and 16-cell; vertex layers and slices through a 4D cell or vertex figure |
| variant of a convex deltahedron (same pattern, unequal edges) | 2 | TBP-5 (J12), OCT-16 (octahedron) |
| pattern of a non-convex deltahedron only, exact | 4 | 600-cell vertex-first shadow, 600-cell slice at 2, Shadow-17 (two J11), Slice-48 |
| pattern no deltahedron can have | 4 | hexagonal (3) and decagonal (1) bipyramids |
| no equilateral form with the slice's own symmetry (exact); less symmetric forms not excluded | 5 | the large 600-cell slices with 28, 30, 32, 42, 72 vertices |

J12 is the only non-Platonic convex deltahedron whose pattern appears; the pentagonal bipyramid, snub disphenoid,
triaugmented triangular prism and gyroelongated square bipyramid never appear.

## Proofs and exact constructions

**1. n-gonal bipyramid patterns with n ≥ 6 have no deltahedron.** Let apices A ≠ B and ring v_1…v_n, all ring
vertices at distance 1 from A and B: they lie on one circle of radius r = √(1 − |AB|²/4) < 1. Consecutive ring
vertices are 1 apart, so each step turns by θ = 2 arcsin(1/(2r)) > 60° about the circle's axis. If two consecutive
steps turn opposite ways, v_{j−1} = v_{j+1} (coincident vertices). So all steps turn one way, nθ = 2πk, and the ring is
the regular polygon {n/k}. If k = 1 then θ = 2π/n ≤ 60°, a contradiction. If k ≥ 2 the ring is a star polygon: two
of its sides cross at a point X, and both triangles from A over those sides contain the segment AX, so the faces
intersect. (A = B gives r = 1, θ = 60°, n = 6 and a flat hexagon.) Hence the hexagonal and decagonal bipyramid
shadows have no equilateral form of any kind. This agrees with Tsuruta et al.'s 8-vertex graph 8_7 "completely flat"
(their index cannot be confirmed without their plantri numbering).

**2. 12-dented icosahedron (placeholder name), the pattern of the 600-cell's vertex-first shadow.** An icosahedron of
edge 2 cut at its edge midpoints is an icosidodecahedron of edge 1 plus 12 corner pyramids, each an equilateral
pentagonal pyramid J2; exactly: θ_ID + β = π, where θ_ID = arccos(−√((5+2√5)/15)) is the icosidodecahedron dihedral
and β = 37.38° (cos β computed exactly in `attach.py`) the J2 base dihedral. So with the pyramids out the faces are
coplanar (not a deltahedron). Pushed in, every edge is 1, dihedrals 105.25° (θ_ID − β) on the 30 icosidodecahedron
edges and 221.81° (reflex) on the 60 pyramid edges, none 180°; the pit apex lies on the face axis at depth
h = √((5−√5)/10) = 0.526 < 1.376 (centre-to-pentagon distance), so each pit stays inside the cone from the centre
over its pentagon and the surface does not meet itself. Same 80-face pattern as the shadow, which is its convex
variant with two edge lengths in ratio 2/√3.

**3. Augmented and dented dodecahedron, the pattern of the 600-cell slice at height 2.** Dodecahedron (edge 1) with 12
J2 pyramids: outward, dodecahedron-edge dihedral θ_D + 2β = 191.32° ≠ 180° (exact check), pyramids in disjoint face
cones, so a non-convex deltahedron (augmented dodecahedron, placeholder name; not found in the sources checked).
Inward, θ_D − 2β = 41.81° > 0 and depth 0.526 < inradius 1.114, also a deltahedron: its 60 triangles lie exactly in
the 20 face planes of the dual icosahedron, three per plane (checked exactly in sympy: each pit triangle's normal is
parallel to a dodecahedron vertex), so it is the surface of the excavated dodecahedron, a known non-convex deltahedron.
The numerical search started from the slice found the augmented form (dihedrals 138.19°–191.32°).

**4. The variants' angles are irrational in degrees where it matters.** TBP-5's lateral dihedral has cos = 1/8, so it
is not a rational multiple of π (Niven: rational cosines of rational multiples of π are 0, ±1/2, ±1). Round an
interior point of a lateral edge, the other tiles contribute 82.82°, 120°, 180° or 360°; θ + (sum) = 2π would make θ a
rational multiple of π. So TBP-5 fills space in no tiling, face to face or not. The same argument with cos = 1/3 and
−7/9 shows the regular J12 fills space in no tiling by itself.

**5. The 600-cell's vertex-first sections at the dodecahedron and equator heights are not the vertex shells.** The
vertex shells (icosahedron, dodecahedron, icosahedron, icosidodecahedron; Wikipedia's "polyhedral sections") are the
hulls of the vertices at one height. The full hyperplane sections also contain the midpoints of 600-cell edges crossing
the hyperplane: e.g. (±1/φ, φ, 1, 0) is an edge (length 2/φ) crossing x_1 = 0 at (0, φ, 1, 0), which lies outside the
icosidodecahedron of the 30 equator vertices (checked exactly, and independently by linear programming). So the true
central section is the 42-vertex solid (same graph, edges and angles as the shadow), and the section at x_1 = 1 is the
32-vertex pentakis-dodecahedron-pattern solid, not the dodecahedron.

## Verdict on DICTO's prediction

Supported, with a qualification. Wherever a 4D shadow or slice is all triangles and not a copy of a 4D cell or vertex
figure, it is never a regular deltahedron (0 of 15); its pattern is either a variant of a convex deltahedron (2: the
5-cell's triangular bipyramid, the 16-cell's octahedron), or a pattern realised only by non-convex dented / augmented
deltahedra (4, all exact: the 600-cell's icosahedral shadow and slice, Shadow-17 = two J11, and Slice-48, the
600-cell's 48-vertex cell-first slice, whose equilateral form keeps the slice's tetrahedral symmetry). The edge spreads are small (1.144–1.309) for the two variants and the two icosahedral
matches, larger for Shadow-17 (2.93) and Slice-48 (3.62). The two variants also attach differently from their regular counterparts:
OCT-16 fills space alone (regular octahedron cannot), TBP-5 closes a three-around star at its base edges (J12 alone
closes none). The qualification: 4 of the 15 non-regular patterns are bipyramids that no deltahedron can take, and 5
large 600-cell slices have no equilateral form with their own symmetry (less symmetric forms not excluded); and the regular deltahedra that do appear (12) are exactly the 4D cells and
vertex figures, which are not new.

## Renders

- `renders/variants.png`: TBP-5 and OCT-16 (gold-brown) beside the regular J12 and octahedron (blue), with edge
  lengths, dihedrals and attachability.
- `renders/slice48.png`: the 600-cell's 48-vertex cell-first slice beside Slice-48, its equilateral form.
- `renders/icosahedral.png`: the 600-cell vertex-first shadow beside the 12-dented icosahedron; the 600-cell slice at
  height 2 beside the augmented dodecahedron.

## Files

- `scripts/q5.py`, `scripts/polytopes.py`, `scripts/shadows.py`, `scripts/classify.py`, `scripts/attach.py`,
  `scripts/render.py`
- `data/shadows.json` (all 223 records), `data/all-triangle-matches.json` (62 all-triangle records with matches and
  the numerical searches), `data/attachability.json`, `data/eqreal_600-cell_edge-first_slice_V17.npy` (Shadow-17's
  numerical equilateral coordinates)
- Large slices: `scripts/large_slices.py` (symmetry, orbits, reduced systems, belts), `scripts/solve_eig.py`,
  `scripts/count_exact.py`, `scripts/explore_real.py`, `scripts/verify_forms.py`, `scripts/exact_embed.py`,
  `scripts/render_slice48.py` (and the earlier `scripts/solve_slices.py`, `scripts/solve_sage.py`, `scripts/curve_v42.py`, which did not finish);
  `data/large-slices-systems.json` (exact reduced systems), `data/eig_*.json` (all real solutions with checks),
  `data/count_*.json`, `data/explore_V42_rotations.json`, `data/form_V48_full_36.json` / `.npy` (Slice-48).
- `prior-art.md`: every source checked.

## Shadow-17 pinned down (2026-10-27, DICTO: "maybe our rule of halves, swap rules or similar might help pin down Shadow-17")
The halves idea: cut Shadow-17's pattern (5-fold; tips of degree 5, rings 5-5-5 with the middle ring of degree 6) at its middle ring. Each half is a **J11** (gyroelongated pentagonal pyramid = diminished icosahedron). **Shadow-17's equilateral form = two J11 glued on their pentagons**: all 136 corner-to-corner distances of the saved numerical form agree with 2 × J11 to 4e-16, and both have exactly 45 unit edges. 2 × J11 is exact by construction (edge 1, Q(√5) coordinates), so Shadow-17 HAS an exact equilateral (non-convex) form; its 5 reflex edges are the shared pentagon's edges, 2 × 100.81° = 201.62° (the J11 triangle–pentagon dihedral doubled). Not claimed new (an obvious gluing; not checked against non-convex deltahedron lists). The J11 is DICTO's starting piece (gaps of dodecahedra/icosahedra). Script: scripts/shadow17_j11.py (slice rebuild there is in other units; the congruence check is the one above).

## The six large 600-cell slices: exact symmetric solve (2026-10-27, DICTO: "keep going on the six large 600-cell slices")

Question: for each of the six all-triangle 600-cell slices left undetermined above (28, 30, 32, 42, 48, 72 vertices),
does its face pattern have an equilateral, non-self-intersecting realisation?

**One-line conclusion.** One does: the 48-vertex cell-first slice has an exact equilateral form with the slice's own
tetrahedral symmetry Td (**Slice-48**, placeholder name; non-convex, dihedrals 81.75°–243.20°, embedding checked with
exact predicates); the other five have no equilateral form with their full symmetry group (exact, complete solution
sets), nor with the rotation subgroup where that was solvable; forms with less symmetry are not excluded.

**Status:** full-symmetry question settled exactly for all six; rotation subgroups settled for V72, V28, V32 and (up
to the exact count below) V42; the rotation-subgroup systems of V30 (15 unknowns) and V48 (12 unknowns) did not finish
(Groebner basis > 50 min); forms without these symmetries are not searched.

### Method

1. **Halves / caps first.** Rings of vertices along each slice's main axis (5-fold for V72 and V32, 3-fold for the
   others; `scripts/large_slices.py`, `belts`). Every slice has degree-5 tips and rings, but also rings of degree 7–10
   vertices (V32: 7; V30, V48: 8; V28: 9; V42, V72: 10) between them. No cap or band was recognised as a piece of the
   listed equal-edged solids (icosahedron caps, J11, antiprism bands, J2, octahedron/tetrahedron caps, the excavated or
   augmented dodecahedron, the 12-dented icosahedron), and the one form found below contains no icosahedral piece (no
   138.19° dihedral, no flat pentagonal cap). So the decision was made by method 2.
2. **Symmetry-reduced exact solve.** The geometric symmetry group G of each slice is computed exactly: every graph
   automorphism (networkx) induced by a linear map M with entries in Q(√5) that preserves the metric (M^T W M = W).
   In every case G is the whole automorphism group of the pattern (V72: Ih, order 120; V32: D5d, 20; V30: D3d, 12;
   V28, V42, V48: Td, 24). One vertex per orbit is placed in the fixed subspace of its stabiliser (exact basis), so
   the unknowns are a few coordinates; one equation |edge|² = 1 per edge orbit. Every system is square
   (unknowns = equations). Solved with Singular (passagemath-singular, installed in the geom venv) over Q(√5):
   Groebner basis, Krull dimension, N = dimension of the quotient ring (number of complex solutions with
   multiplicity, exact); all solutions by the eigenvalue method (multiplication matrix of a random linear form),
   each refined by Newton at 120 digits on the exact equations; **complete** when the number of distinct refined
   solutions equals N (then all solutions are simple and none is missed). Distinct and real counts cross-checked exactly
   (`scripts/count_exact.py`: characteristic polynomial of the exact multiplication matrix of two random linear forms,
   squarefree part, real roots isolated in the real algebraic numbers) for V72 (Ih: 8 / 4 real; I: 16 / 8), V28 (Td:
   32 / 12), V32 (D5d: 128 / 48) and V42 (T, saturated: 152 / 52; one linear form), all agreeing with the eigenvalue method; the
   check for V48 (192 solutions) did not finish within 50 minutes.
   Scripts: `scripts/solve_eig.py` (main), `scripts/solve_sage.py` and `scripts/solve_slices.py` (earlier versions,
   same results where they finished).
3. **Embedding.** Each real solution: distinct vertices, no 180° edge, clearance between faces
   (`scripts/verify_forms.py`; validated on the icosahedron and the augmented and dented dodecahedra), edge-through-face
   test; the candidate that passed was then checked with exact orientation predicates on 85-digit rational
   coordinates (`scripts/exact_embed.py`; every deciding predicate at least 0.012 in size, rounding error below
   1e-50; validated on the augmented dodecahedron).

### Results

| Slice | Symmetry used | Unknowns | Complex solutions (exact N) | Complete | Real | Embedded | Why the real ones fail |
|---|---|---|---|---|---|---|---|
| V72 (vertex-first, ±(√5−1)) | Ih | 3 | 8 | yes | 4 | 0 | coincident vertices |
| V72 | I (rotations) | 4 | 16 | yes | 8 | 0 | coincident vertices |
| V32 (edge-first, ±(3+√5)/2) | D5d | 7 | 128 | yes (exact count 128 / 48 real) | 48 | 0 | edges pierce faces (32), faces touch (16) |
| V32 | D5 | 10 | 640 | yes | 112 | 0 | self-intersection |
| V30 (face-first, ±(4+2√5)/3) | D3d | 10 | 464 | yes | 104 | 0 | edges pierce faces (100), faces touch (4) |
| V30 | D3 | 15 | not finished | — | — | — | Groebner basis > 50 min |
| V28 (cell-first, ±(5+3√5)/4) | Td | 5 | 32 | yes | 12 | 0 | edges pierce faces (10), edges cross exactly (2; contact distance 0 at 50 digits) |
| V28 | T | 7 | 64 | yes | 28 | 0 | coincident vertices (16), self-intersection (12) |
| V42 (cell-first, ±(3+√5)/2) | Td | 7 | 96 | yes | 32 | 0 | edges pierce faces (26), faces touch (2), coincident vertices (4) |
| V42 | T | 10 | a curve + 160 isolated (152 distinct, exact) | yes (distinct) | 52 | 0 | curve: 6 vertices at the centre; isolated: self-intersection |
| **V48** (cell-first, ±(2+√5)/2) | **Td** | 8 | 192 | yes | 48 | **2 (one shape)** | the other 46: edges pierce faces (44), faces touch (4) |
| V48 | T | 12 | not finished | — | — | — | Groebner basis > 50 min |

V42 with T: the solution set has dimension 1. Saturating by t0_0 (the coordinate of the 6-vertex orbit on the 2-fold
axes) leaves a zero-dimensional system (exact: Rabinowitsch ideal of dimension 0, N = 160), so every point of the curve
has t0_0 = 0: those 6 vertices all sit at the centre, never embedded. The isolated part has 160 solutions with
multiplicity, 152 distinct and 52 real (exact count, `scripts/count_exact.py`); the eigenvalue method found all 152
and all 52 real ones (two of them only after relaxing the reality test from 1e-80 to 1e-30), none embedded.

**Slice-48 (placeholder name).** The 600-cell's cell-first slice at height ±(2+√5)/2 (48 vertices, 138 edges,
92 triangles, degrees 8^12 5^36, Td) has an equilateral form with the same Td symmetry: all 138 edges equal (error
< 1e-84 after Newton), non-convex (24 of 48 vertices on the convex hull), dihedral angles 81.75° (24 edges), 130.98° (6),
135.83° (24), 143.83° (24), 191.03° (12), 197.94° (12), 216.17° (12), 243.20° (24); none is 180°, and no two faces meet
except along their common edges and vertices (exact predicates, smallest deciding predicate 0.012; nearest non-adjacent
parts 0.069 apart at edge 1). The two real solutions that pass are the same shape (one is the other turned by a
half-turn). Its coordinates are algebraic numbers, roots of the exact system in `data/large-slices-systems.json`
(V48, full); 60-digit values of the 8 unknowns and of all 48 vertices are in `data/form_V48_full_36.json`
(`data/form_V48_full_36.npy` in floats). It is a strict deltahedron (Tsuruta et al.'s conditions: closed, no
self-intersection, no 180° edge). It is not in the classes of non-convex deltahedra checked: Cundy's 17 and
Olshevsky's 11 biform deltahedra need two vertex types (Slice-48 has four vertex orbits and two degrees), Shephard's
and McNeill's isohedral ones are face-transitive (92 faces cannot form one orbit of a group of order 24), Trigg's are
spiral strips, Tsuruta et al. stop at 10 vertices. Not claimed new beyond that check.

What the reduction does not cover: equilateral forms of these patterns with less symmetry than G (or than its rotation
subgroup), and the rotation-subgroup systems of V30 and V48.

Render: `renders/slice48.png` (the convex slice, and Slice-48 from two sides).
