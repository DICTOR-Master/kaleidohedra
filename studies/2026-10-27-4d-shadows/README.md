# 4D shadows and slices against deltahedra (study, 2026-10-27)

Credit: DICTO (the idea), with Claude (computation). Research only, no app changes.

**One-line conclusion.** DICTO's prediction holds where the 4D shadow is a deltahedron pattern at all: no non-regular
all-triangle shadow or slice of the 5-, 16-, 24- or 600-cell is equilateral, the two that carry a convex deltahedron's
face pattern are variants of it (triangular bipyramid, edge ratio √(12/7) = 1.309; octahedron, ratio 2/√3 = 1.155,
which fills space where the regular octahedron cannot), and the 600-cell's icosahedral shadow and slice carry the
patterns of non-convex (dented / augmented) deltahedra and of none of the 8; regular deltahedra appear only as the
4D cells and vertex figures themselves, while 4 of the 15 non-regular patterns can be no deltahedron at all.

**Status:** done (projections, layers and slices along all four principal directions of all four polytopes; exact
comparison; attachability of the two variants). Open: 6 large slice patterns (28–72 vertices) have no equilateral
form found in 12 numerical starts each, which proves nothing either way.

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
| 600-cell | edge-first slices at ±(1+√5) | 17, 30 | 6^5 5^12 | none of the 8 | 2.927 | non-convex equilateral form **found numerically** (Shadow-17, placeholder; 5 reflex edges, dihedrals 138.19°–201.62°; not exact) | not studied |
| 600-cell | vertex-first slices at ±(√5−1) | 72, 140 | 10^12 5^60 | none | φ√2 = 2.288 | none found (12 starts) | — |
| 600-cell | edge-first slices at ±(3+√5)/2 | 32, 60 | 7^10 5^22 | none | φ² = 2.618 | none found (12 starts)* | — |
| 600-cell | face-first slices at ±(4+2√5)/3 | 30, 56 | 8^6 5^24 | none | 3.618 | none found (12 starts) | — |
| 600-cell | cell-first slices at ±(5+3√5)/4 | 28, 52 | 9^4 5^24 | none | φ√2 = 2.288 | none found (12 starts) | — |
| 600-cell | cell-first slices at ±(3+√5)/2 | 42, 80 | 10^6 5^36 | none | 4.815 | none found (12 starts) | — |
| 600-cell | cell-first slices at ±(2+√5)/2 | 48, 92 | 8^12 5^36 | none | 3.618 | none found (12 starts) | — |

Heights are x·d with d the unnormalised direction vector of `polytopes.py` (600-cell vertex-first: d = (2,0,0,0), so
x·d = 2 means x_1 = 1).

\* An earlier 40-start run with a dense solver reported an equilateral form at start 19 (residual 8e-15, non-convex),
but its coordinates were not kept and the recorded 12-start rerun did not find it; left undetermined.

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
| pattern of a non-convex deltahedron only, exact | 2 | 600-cell vertex-first shadow, 600-cell slice at 2 |
| pattern of a non-convex deltahedron only, numerical | 1 | Shadow-17 |
| pattern no deltahedron can have | 4 | hexagonal (3) and decagonal (1) bipyramids |
| undetermined | 6 | the large 600-cell slices |

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
deltahedra (3: the 600-cell's icosahedral shadow and slice exactly, Shadow-17 numerically). The edge spreads are small
(1.144–1.309) exactly in those matches. The two variants also attach differently from their regular counterparts:
OCT-16 fills space alone (regular octahedron cannot), TBP-5 closes a three-around star at its base edges (J12 alone
closes none). The qualification: 4 of the 15 non-regular patterns are bipyramids that no deltahedron can take, and 6
large 600-cell slices are undetermined; and the regular deltahedra that do appear (12) are exactly the 4D cells and
vertex figures, which are not new.

## Renders

- `renders/variants.png`: TBP-5 and OCT-16 (gold-brown) beside the regular J12 and octahedron (blue), with edge
  lengths, dihedrals and attachability.
- `renders/icosahedral.png`: the 600-cell vertex-first shadow beside the 12-dented icosahedron; the 600-cell slice at
  height 2 beside the augmented dodecahedron.

## Files

- `scripts/q5.py`, `scripts/polytopes.py`, `scripts/shadows.py`, `scripts/classify.py`, `scripts/attach.py`,
  `scripts/render.py`
- `data/shadows.json` (all 223 records), `data/all-triangle-matches.json` (62 all-triangle records with matches and
  the numerical searches), `data/attachability.json`, `data/eqreal_600-cell_edge-first_slice_V17.npy` (Shadow-17's
  numerical equilateral coordinates)
- `prior-art.md`: every source checked.
