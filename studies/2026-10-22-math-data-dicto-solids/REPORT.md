# Report for DICTO: math-data dataset (first build 2026-10-22, second pass 2026-10-23, version 2 2026-10-24, version 3 2026-10-27, version 4 2026-10-28)

Created by DICTO · dictospheres.com · CC BY-SA 4.0. Branch `math-data-dataset` (local only, not pushed). Nothing on Zenodo, the
apps, the papers, DISCOVERIES.md or the website was changed.

## Version 7 (2026-11-01)

Released on DICTO's word (2026-11-01, "all publish ok"). Adds D106 Cube Pearl, D107 Golden Clasp, D108 Hamlet and D109 Ophelia (DICTO's names, 31 October 2026), exact in ℚ(√5), built by `build/build_v7.py` (14/14 build checks) from the study code of studies 2026-10-31-star-cores-names; credit line as version 6. Paper field (agent, 2026-11-01): #80 The Gains of DICTO's Growth Rule (10.5281/zenodo.23822907) for the Cube Pearl (Section 6: the edge-cut cube at s = 3/5, all 32 corners on one sphere) and for Hamlet and Ophelia (Section 6: the OG chain's steps five and six, 452 and 642 corners); the Golden Clasp's depths 1 : 1/φ : 3/4 are in no published paper (#80 says only that the truncated cuboctahedron's faces at other depths close in four steps), so its paper field names the studies and it has no DICTO DOI. #81 Core Cycles restates the edge-cut cube result (s ≤ 3/5) but names none of the four; #85 is not yet published. check.py: one change, the float rounding of a + b√5 (now from a 40-digit √5; Hamlet's and Ophelia's coordinates failed the 1e-14 decimal test only through cancellation in the old float formula); 1569 checks, all pass. index.csv: four rows (163 in all).

## Version 4 (2026-10-28)

Version 3 is published (Zenodo record 23680729). Version 4 is built on the same branch (local only, not pushed) and is **not released**:
it waits for DICTO's reading.

### What was added

- **Three solids** (names exactly as in the papers), each with a unit-volume copy:
  - #61 *The Swap Rule* (DICTO DOI: 10.5281/zenodo.23682596, v2 record 23683033): **Ganesha**, at the parameters of the paper's Figure 1
    (stacking ACBC, layer spacing² = (3/4)(2/3), i.e. s = 3/4; weight λ = 1/10; the tetrahedral hole over X at 3/4 of the gap between layer
    1, type c, and layer 2, type h; census site 4). 30 corners, 45 edges, 17 faces (6 triangles, 3 squares, 4 hexagons, 3 octagons, one
    12-gon), C3v, convex, in ℚ(√3); volume (68881403/165888000)√3 here = 0.254274 at ball spacing 1. New, **D84**.
  - #62 *Shadows of the Fourth Dimension* (DICTO DOI: 10.5281/zenodo.23687223, record 23687224): **Shadow-17**, two J11 of edge 1 glued on
    their pentagons (the second the mirror image of the first in the pentagon's plane). 17 corners, 45 unit edges, 30 triangles, D5h,
    non-convex, in ℚ(√5); volume 25/12 + 3√5/4 (twice J11). Status (DICTO 2026-10-28): new construction from a known piece (J11, Johnson's
    gyroelongated pentagonal pyramid, Johnson 1966); the equal-edged form of the 600-cell's outer edge-first slices (#62). **D86**.
  - #63 *The White Queen 600-cell* (DICTO DOI: 10.5281/zenodo.23690856, v2 record 23702910): **Humpty Dumpty**, the real 48-vertex
    cell-first slice of the 600-cell at height 1 + √5/2. 48 corners (12 of degree 8, 36 of degree 5), 138 edges of eight lengths, 92
    triangles, Td, convex, in ℚ(√5); volume 2627/60 + 1213√5/60 at the dataset's scale (below). New (#63: not found in the sources checked),
    **D85**.
- **index.csv**: three rows (in_dataset y; D84, D85, D86); **d-numbers.md**, **README** and `published/records.json` (#61, #62, #63) updated.

### Decisions (and who made them)

- **Sources executed, not re-derived** (agent; copies in `build/sources/`, research branch commit 0620db53): #61's `splash.py` `net_for`
  (the #57 stacking with the layer spacing as a parameter) with the census engine of version 3; #62/#63's `q5.py` and `polytopes.py` (the
  exact 600-cell and its four directions) with the cut of `atlas600.py`. Shadow-17 is exact by the construction of #62's
  `shadow17_j11.py` (two J11, edge 1), built here from the icosahedron (0, ±1/2, ±φ/2) and checked against the study's own numerical
  equal-edged form of the slice (`eqreal_600-cell_edge-first_slice_V17.npy`: all 136 distances agree to 4.4·10⁻¹⁶).
- **Ganesha's parameters** (agent): those of #61 Figure 1, the one piece the paper draws and names; the piece is the one `export_swap.py`
  exports (first tetrahedral hole over X with a c layer below and an h layer above). Other spacings and weights give other members of the
  same family; they are not separate files. Field ℚ(√3): at s = 3/4 the layer spacing at ball spacing √2 is 1, so the period along (1, 1, 1)
  has length 4 and the coordinates need √3/3.
- **Humpty Dumpty's scale** (agent): an orthonormal frame of the 3-space of the slice needs √|d|² = √((7 + 3√5)/4) besides √5 (|d|² is not
  a square in ℚ(√5)). Scaling the slice by |d| removes it: the imaginary part of conj(d)·p (quaternions) is exact in ℚ(√5). So the file is
  Humpty Dumpty scaled by |d| ≈ 1.8512 from the 600-cell of circumradius 2; its squared edges divided by 7/4 + 3√5/4 are the atlas values
  exactly (checked). The unit-volume copy removes the question of scale.
- **Statuses and D-numbers**: Ganesha and Humpty Dumpty new (the papers' prior art: not found in the sources checked), D84, D85 in order of
  publication (#61, #63). Shadow-17: first filed as known pieces; DICTO decided (2026-10-28) "new construction from a known piece (J11)",
  D86, the next free number. D1–D83 unchanged.

### Checks

- **check.py on dicto-big-brother: TOTAL: 1062 checks, 1062 passed, 0 failed; 44 solids, 6 packings (fills), 4 packings (not fills).**
  New: Ganesha 21, Shadow-17 21 (non-convex: no convexity check), Humpty Dumpty 22. The other 998 checks are those of version 3, all passing.
- **Build log** `build/build_v4.log.json`: 22 PASS, 0 FAIL (every published value: f-vectors, faces, squared edges, symmetry order and
  class; Ganesha's two halves at its gap's mid-plane are 0.058005 and 0.196269 at ball spacing 1, as #61 Figure 1, and add up exactly;
  Shadow-17 = the study's numerical form and = 2 J11 in volume; Humpty Dumpty's edges = the atlas's eight exact values).

### Checked against the published papers (#61 v2, #62 v1, #63 v1/v2; the PDFs in the research repository's papers folders)

- #61 Figure 1: ACBC, spacing² = ¾·⅔, λ = 1/10, part volumes 0.058005 and 0.196269: equal (to the 6 printed places).
- #62: Shadow-17 has 17 vertices and 30 triangles, two J11 glued on their pentagons, every edge 1, five folded edges (2 × 100.81°): equal.
- #63: 48 vertices (12 of degree 8, 36 of degree 5), 138 edges, 92 triangles, Td, convex, edge ratio up to (5 + √5)/2: equal (the largest
  over the smallest squared edge is (15 + 5√5)/2, the atlas's `edge_ratio2_exact`).
- **Disagreements with a published paper: none found.**

### Not added in version 4, and why

- #59 v2 (DICTO DOI: 10.5281/zenodo.23677485): the **Icosaxes Bloom** (twenty Icosaxes touching along edges, twelve open windows) and the
  **Icosaxes Bud** (sealed round a hollow) are not single solids: the format holds one closed 2-manifold with no inner cavity. The
  **Icosaxes Seed** is one solid, but its twenty Icosaxes pass through each other: the study proves the stops exactly (`exact.py`) and
  keeps the joined solid only as a float manifold3d mesh (`S3-union.obj`); no exact union exists in the study, and the `composition` key
  needs interior-disjoint pieces. The same for the **Lotus Jewel Bloom, Bud and Seed**.
- #60 *DICTO Janus c/h Pyrochlore* (10.5281/zenodo.23678750): no new named pieces (the name is the paper's title; its Janus pieces are
  unnamed members of #57's kind).
- #62: **Slice-48** = **Fallen Humpty** (#63's name): numeric only. Its equal-edged form is a real root of a polynomial system over ℚ(√5),
  found and refined to 120 digits (`form_V48_full_36.json` keeps 85-digit rational approximations); no exact closed form, so it is not
  in this exact dataset. The other forms of #62 are not claimed new: TBP-5 and OCT-16 (unequal-edged variants; OCT-16 is the cell of the
  known square bipyramidal honeycomb), the 12-dented icosahedron and the augmented dodecahedron (placeholder names, obvious
  constructions), the excavated dodecahedron (known).

### Open questions for DICTO

1. Shadow-17: DECIDED by DICTO, 28 October 2026: new construction from a known piece (J11), D86.
2. Ganesha: one file at #61's Figure 1 parameters (as now); the Ganesha pieces form a family in s and λ.

## Version 3 (2026-10-27)

Version 2 is published (Zenodo concept DOI 10.5281/zenodo.23606967, record 23608590). Version 3 is built on the same branch (local only,
not pushed) and is **not released**: it waits for DICTO's reading.

### What was added

- **Twelve solids** (DICTO's names, exactly as typed), each with a unit-volume copy:
  - #55 *David and Goliath* (DICTO DOI: 10.5281/zenodo.23632358): **Goliath** (12 corners, 20 triangles, Th; the convex hull of Jessen's
    icosahedron, known) and **David** (tetragonal disphenoid, D2d, known), in ℚ.
  - #56 *Sonsam and Lahdeli* (DICTO DOI: 10.5281/zenodo.23635823): **Sonsam** (19 corners; 6 triangles, 3 pentagons, 3 hexagons, a nonagon;
    C3v) and **Lahdeli** (12 corners; 2 triangles, 6 pentagons; D3d) in ℚ(t); **Ian Dury** (16 corners, C3v) and **Blockhead** (10 corners,
    C3v) in ℚ.
  - #57 *The Rule of Halves* (DICTO DOI: 10.5281/zenodo.23647898): **Chucky** (19 corners, C3v), **Fang** (7 corners, C3v) and the
    **Triskelion Tetrahedron** (16 corners, 4 triangles + 6 hexagons, Td), in ℚ.
  - #59 *The Icosaxes Hexa* (DICTO DOI: 10.5281/zenodo.23677485, version 2): **Keyaxes** (32 corners, 54 faces, S6), **Icosaxes Hexa** (144
    corners, 86 faces, Oh) and **Lotus Hexa** (200 corners, 366 faces, Th), non-convex, in ℚ(√5).
- **index.csv**: twelve rows (in_dataset y); **D76–D83** for Sonsam, Lahdeli, Ian Dury, Blockhead, Chucky, Fang, Triskelion Tetrahedron,
  Keyaxes. **d-numbers.md** and **README** updated; `published/records.json` lists the four records.

### Decisions (and who made them)

- **Sources executed, not re-derived** (agent, as in version 2; copies in `build/sources/`, research branch commit 41e1213c): #55's
  `exact_a15.py` (the A15 cells in Fractions); the census engine (`engine.py`, `networks.py`) and `stackings.py` give the exact planes of
  the power cells of the holes of any close-packed stacking; each cell is then solved exactly in the dataset's field. #59: the #48 objects
  of version 2 (`golden_split_exact.py`, `keyed_polar_exact.py`) keyed as krp-core `golden-split.js` does (INTO_BIG: the #48 Tricap taken
  out; INTO_SMALL: the Tricap mirrored in its base plane, added); the Hexas as in k-mix `bloom-geometry.js` `hexa()`.
- **Fields** (agent): the hole pieces have rational coordinates at ball spacing √2 with the close-packed layers perpendicular to (1, 1, 1)
  (the frame of Samson and Delilah); so all of them are in ℚ except Sonsam and Lahdeli, whose weight t is the root of
  1536t³ + 5184t² − 3384t + 11 in (−1/8, 5/24) (#56 Theorem 2). Their corners are affine in t, so the field is the cubic field ℚ(t), stated
  honestly as `"Q(t)"` with a `field_definition` (minimal polynomial, isolating interval). The cubic has three real roots, so the norm
  trick of ℚ(∛2) does not decide signs; the checker uses exact interval arithmetic on a bisected isolating interval instead. √2 is not
  needed in any coordinate.
- **Frames**: each hole piece moved so that its hole is at the origin; Goliath about its Si site, David about its Cr site (its centroid);
  the Keyaxes about its centre; the two Hexas about their middle piece. Sonsam, Ian Dury, Chucky and Fang are not centred on their holes,
  so their unit-volume copies are scaled about the corner centroid (as the Dodeca-13 Wedge and Needle).
- **Which piece**: Sonsam and Ian Dury and Blockhead are the cell of the census hcpholes site 2 (tetrahedral hole (0, 0, 3/8)); all four
  tetrahedral sites give the same polynomial and, by symmetry, congruent pieces. Lahdeli is site 0. Chucky and Fang are site 0 of ABAC (the
  gap between layer 0, type c, and layer 1, type h: hexagonal top, cubic bottom), as in the study's `exact_named.py`; their mirror images
  (the next gap) are not separate files. The Triskelion Tetrahedron is ABAC site 2 (nearest layer of type c).
- **Keyaxes**: dents on the two hexagons facing ±(1, 1, 1), keys on the other six (any opposite pair gives the same solid up to a symmetry
  of the Lotus Jewel Axes' group Th).
- **Composition key** for the non-convex #59 solids (agent): pieces (convex dataset solids) minus dents plus keys, with "mirrored tricap"
  as a second kind of Tricap. A new key name, so the version 2 `decomposition` checks are untouched.
- **Kinds and D-numbers**: hole pieces are filed as kind "solid" (as Samson and Delilah). The Icosaxes Hexa and Lotus Hexa are filed as
  "cluster" (eight Icosaxes round an Unborn Axes as one solid, like the DICTO Hexa), so they get no D-number. Goliath and David are known
  (#55: "Goliath is not a new shape"; David the empty Cr4 tetrahedron), no D-number. The Triskelion Tetrahedron is filed as new (D82): the
  name marks one member of Samson's family, as Samson (D71) marks another; the #57 study notes it is congruent to the cubic octet's piece at
  5/24 (not new to the stackings). Both are DICTO's call (d-numbers.md, open questions 3 and 4).

### Checks

- **check.py on dicto-big-brother: TOTAL: 998 checks, 998 passed, 0 failed; 41 solids, 6 packings (fills), 4 packings (not fills)**
  (1 min 51 s). New: 9 convex solids × 22 (Sonsam and Lahdeli 23, with the field check), Keyaxes and Icosaxes Hexa 29, Lotus Hexa 28 (7
  composition checks each; no published value for the Lotus Hexa).
- **Versions 1 and 2 unchanged**: the committed check.py (version 2) and the new one, run with `-v` on the version 1 + 2 files alone, give
  the same 712 checks, line for line, all passing.
- **Corruption tests** (each on a copy; each must fail, and did): a Sonsam corner moved by 1/100 in ℚ(t) (12 failed: planarity, volume,
  convexity, edges, symmetry, published values …); Lahdeli's isolating interval widened to (−1/8, 1), which holds two roots (1 failed: the
  field check); a Keyaxes key relabelled as an unmirrored Tricap (1 failed: the Tricap kind); a Lotus Hexa corner piece moved onto
  another (3 failed: pieces disjoint, Tricap placement, corners); an Icosaxes Hexa face reversed (11 failed); a wrong group order of Chucky
  (1 failed: the symmetry group check).
- **Build log** `build/build_v3.log.json`: 77 PASS, 0 FAIL (every published value; Goliath's corners = Jessen's set ×1/2; 2 Goliaths +
  6 Davids = the cubic cell; the cubic irreducible with one root in the stretch, t = 0.003266956983…; 4 Sonsams + 2 Lahdelis = the hcp
  cell exactly in ℚ(t); at 5/24 the octahedral cell is the 60° rhombohedron of volume √2/54 and 4 Ian Durys + 2 rhombohedra = the cell;
  the Triskelion Tetrahedron = the cubic octet's tetrahedral piece at 5/24 (same faces, same exact volume, corners congruent); Chucky and
  Fang are exactly the means of their cubic and hexagonal parents; Keyaxes = φ² = Icosaxes + 4 Tricaps; Icosaxes Hexa = 8 Icosaxes +
  1 Unborn Axes; Lotus Hexa = Icosaxes Hexa + 56 Tricaps).

### Checked against the published papers (#55 v1 record 23632359, #56 v1 23635824, #57 v1 23647899, #59 v2 23679142; the PDFs as kept in
the research repository's papers folders)

- #55: Goliath = conv{(0, ±1/2, ±1) cyclic}, 20 triangles, 12 corners of degree 5, 30 edges (squared lengths 1 and 3/2), volume 7/2;
  David: corners (0, ±1/2, 1), (1, 0, 1/2), (1, 0, 3/2) (moved here by −(1/2, 0, 1)), edges 1 and √(3/2), volume 1/6; 2 · 7/2 + 6 · 1/6 = 8:
  all equal.
- #56: the cubic 1536λ³ + 5184λ² − 3384λ + 11, irreducible, one root in (−1/8, 5/24), λ ≈ 0.0032669570; Sonsam 19/30/13 (6 triangles, 3
  pentagons, 3 hexagons, one 9-gon), Lahdeli 12/18/8 (2 triangles, 6 pentagons), both √2/6; Ian Dury 16/27/13 (6, 3, 4), 13√2/54; the
  rhombohedron √2/54; Blockhead 10/18/10 (6, 3, 1), √2/4: all equal (volumes × 2√2 in this frame).
- #57: Chucky 19 corners (3 triangles, 3 squares, 6 pentagons, a nonagon), 383√2/768; Fang 7 corners (4 triangles, 3 squares), 5√2/324;
  Triskelion Tetrahedron 16 corners (4 triangles, 6 hexagons), 79√2/324; Chucky and Fang the means of √2/2 and 191√2/384, of √2/81 and
  √2/54: all equal.
- #59 (v2): Keyaxes φ² = (3 + √5)/2; Icosaxes Hexa 9 + 17√5/3 (version 2's corrected value; version 1's 9 + 6√5 was the uncorrected sum);
  Tricap (1 − √5/3)/8 = (3 − √5)/24: all equal. The Lotus Hexa's volume is not stated in #59; here 16 + 10√5/3 ≈ 23.4536, and the study's
  float value (K2) is 23.454.
- **Disagreements with a published paper: none found.**

### Open questions for DICTO

1. The Icosaxes Hexa and Lotus Hexa: clusters without D-numbers (as now) or solids with D84, D85 (since version 4: the next free numbers).
2. The Triskelion Tetrahedron: new with D82 (as now), or a named member of a known family without a number.
3. The keyed forms of #56 (Sonsam-K, Lahdeli-K, Ian Dury-K, Rhombo-K) are float constructions in #56 (exact by the rule, but the study
   keeps only floats); they and #59's Bloom/Bud/Seed clusters are not in this version.

## Version 2 (2026-10-24)

Version 1 is published (Zenodo concept DOI 10.5281/zenodo.23606967, record 23606968, built from commit 98e3fbb). Version 2 is built on the
same branch (local only, not pushed) and is **not released**: it waits for DICTO's reading.

### What was added

- **Six solids, the six DICTONIC SOLIDS** (DICTO's names, exactly as typed): from #48 *The Golden Split* (DICTO DOI:
  10.5281/zenodo.23596362) the **Icosaxes** and the **Unborn Axes** (convex truncated octahedra, Oh), the **Lotus Jewel Axes** (non-convex:
  the Icosaxes with its 8 Tricaps removed, a dent on each hexagon) and the **Dodecaxes** (non-convex: the Unborn Axes with its 8 Tricaps
  added, a key on each hexagon), both Th; from #51 *The Delian Bond* (DICTO DOI: 10.5281/zenodo.23606828) **Samson** (convex, 16 corners,
  10 faces: 4 triangles, 6 hexagons, Td) and **Delilah** (the regular octahedron, Oh). Each with a unit-volume copy, as in version 1.
- **Three fills, the three DICTONIC BONDS**: `dicto-golden-bond` (Icosaxes at φℤ³, Unborn Axes at φℤ³ + (φ/2)(1, 1, 1); #48 Main
  theorem (f)), `dicto-keyed-bond` (Lotus Jewel Axes and Dodecaxes at the same places; #48 Theorem 3), `dicto-delian-bond` (8 Samsons and
  4 Delilahs per cube of side 2; #51).
- **index.csv**: six new rows (in_dataset y) and a new column `universal_number` for every row; **d-numbers.md** (new).

### Decisions (and who made them)

- **Names exactly as typed; one name per shape, the first name DICTO chose wins** (DICTO 2026-10-23, version 1 decisions, applied):
  Icosaxes, Unborn Axes, Lotus Jewel Axes, Dodecaxes, Samson, Delilah. Delilah is the regular octahedron (status "known", note "known shape
  (regular octahedron)"); its row is named "Delilah" as asked (under the one-name rule DICTO may prefer "Regular octahedron (Delilah)":
  his call).
- **Status labels** (from #48 and #51, no new claim): Icosaxes and Unborn Axes *known* (Koca et al. 2015, non-regular truncated octahedra
  x = τ and x = 1/τ; new route); Lotus Jewel Axes and Dodecaxes *new*; Samson *new* (a new proportion, #51); Delilah *known* (regular
  octahedron).
- **Second number field** (agent's choice, as briefed): Samson and Delilah are exact in ℚ(∛2), not ℚ(√5). Every file now names its
  field (`"Q(sqrt(5))"` or `"Q(2**(1/3))"`); exact strings are sympy-parsable in that field (`a + b*2**(1/3) + c*2**(2/3)`). The
  checker's new field class decides signs exactly by the norm a³ + 2b³ + 4c³ − 6abc (it has the sign of the number, because the other two
  conjugates are complex conjugates), so no floating point decides anything.
- **Frames**: #48's frame (icosahedron edge 1, lattice spacing φ) for the four golden solids; the Unborn Axes and Dodecaxes are moved so
  that their centre, #48's cube centre (φ/2)(1, 1, 1), is at the origin (their corners are then exactly "all permutations of
  (±1/(2φ), ±φ/2, 0)" as in #48). Samson and Delilah are in the frame of the #51 study (octet in a cube of side 2, octet edge √2), each
  moved to its own centre: #51's octet edge 1 would need √2, which is not in ℚ(∛2). At octet edge 1 (#51) divide lengths by √2 and
  volumes by 2√2: volume 2/3 here is √2/6 there; Delilah's edge 2^(1/6) here is 2^(−1/3) there. Stated in each `scale_note`.
- **Keying of the keyed bond**: every Tricap on the dodecahedron side (each Icosaxes carries 8 dents, each Unborn Axes 8 keys), which is
  the Lotus Jewel network itself; #48 Theorem 3 says any keying fills, this file fixes this one.
- **Tricap orientation**: #48's cyclic orientation, as in keyed_polar_exact.py (base corners = corners of the Unborn, apex = a corner of
  the Unborn's dodecahedron cube). The checker tests it for every Tricap; the mirrored Tricaps (the bug found on 10-24) fail.
- **True face lists**: each dented or keyed hexagon becomes the 3 triangles left of the hexagon plus the Tricap's 3 side faces; coplanar
  neighbours sharing an edge would be merged, and none are: 54 faces each (48 triangles, 6 squares), 32 corners, 84 edges.
- **Symmetry of a solid**: now the group of maps taking corners to corners *and faces to faces*. Needed because the dents and keys sit at
  cube corners: the corner sets of the Lotus Jewel Axes and Dodecaxes have full octahedral symmetry (48), the solids only pyritohedral
  (Th, 24). For every version 1 solid the group is unchanged (all their checks pass as before).
- **Polyhedraverse**: the six solids exist as DICTO_ICOSAXES, DICTO_UNBORN_AXES, DICTO_LOTUS_JEWEL_AXES, DICTO_DODECAXES, DICTO_SAMSON,
  DICTO_DELILAH on the K branch `dictonic-world` (not merged, not live), so `in_polyhedraverse` is "n" for now; switch to "y" when it ships.

### Checks

- **check.py on dicto-big-brother: TOTAL: 712 checks, 712 passed, 0 failed; 29 solids, 6 packings (fills), 4 packings (not fills)**
  (80 s). Version 1's 550 checks are all still there and pass unchanged; new: 6 solids × 22, 7 decomposition checks each for the Lotus
  Jewel Axes and the Dodecaxes, 5 + 5 for the golden and Delian bonds, 6 for the keyed bond.
- The keyed bond is proved without a convex split: the golden bond tiles (exact, convex pieces), the keyed bond has the same lattice and
  placements, each keyed piece is its convex piece ∓ 8 Tricaps (re-proved), and every dent is exactly one key moved by a lattice vector.
- **Corruption tests** (each on a copy; each must fail, and did): a Samson corner moved by 1/100 (ℚ(∛2): 14 checks failed, among them
  planarity, volume, symmetry and the Delian bond's volume sum); a Lotus Jewel Axes corner moved by 1/100 (16 failed, among them the
  decomposition's corners and face planes); the Lotus Jewel Axes' Tricaps mirrored x ↔ y (4 failed: the orientation test, the face planes,
  and the keyed bond's dent–key match and conclusion); the keyed bond with the Dodecaxes moved onto the Icosaxes site (3 failed).
- **Build log** `build/build_v2.log.json`: 49 PASS, 0 FAIL (study objects; every published value; corner sets as stated in #48; all 16
  Tricaps of volume (3 − √5)/24; the Unborn plus its 8 Tricaps is the regular dodecahedron of edge 1/φ; Delilah's corners
  (±2^(−1/3), 0, 0); the other tetrahedron cell is Samson turned a quarter turn about z; the three bonds' volume sums).
- **Sources**: the study scripts were executed, not re-derived (copies in `build/sources/`): golden_split_exact.py and
  octet_special_exact.py are byte-identical to the copies in the published #48 and #51 records (study zips golden-split-study-066a46a and
  delian-bond-study-4e98aa8); keyed_polar_exact.py (the Tricaps and the keyed pair) is from the research branch, commit e9aed63 (written
  after #48 was published; it is not in the #48 record).

### Checked against the published papers (#48 v1, record 23596363; #51 v1, record 23606829)

- #48: Icosaxes corners all permutations of (±½, ±φ/2, 0), Unborn Axes c + all permutations of (±1/(2φ), ±φ/2, 0); 8 hexagons and 6
  squares each; full octahedral symmetry; hexagon sides 1/√2 and 1/(φ√2), Icosaxes squares 1/√2, Unborn Axes squares 1/(φ√2); volumes
  1 + 2√5/3 and 1 + √5/3, together φ³ = 2 + √5 (the golden bond's cell); Tricap volume (3 − √5)/24; Lotus Jewel Axes √5 = 1 + 2√5/3 −
  8(3 − √5)/24, Dodecaxes 2 = 1 + √5/3 + 8(3 − √5)/24; the Unborn plus its 8 Tricaps is the dodecahedron of edge 1/φ: all equal.
- #51: Samson 16 corners, 10 faces (4 triangles, 6 hexagons), Delilah a regular octahedron; equal volumes √2/6 at octet edge 1 (2/3 here,
  8 Samsons + 4 Delilahs = the cube of side 2); Delilah's edge 2^(−1/3) at octet edge 1 (squared 2^(1/3) here); Samson's edges 1/∛2 and
  (1 − 2^(−1/3))/√2 at octet edge 1 (squared 2^(1/3) and 1 + 2^(1/3)/2 − 2^(2/3) here): all equal.
- **Disagreements with a published paper: none found.**

### universal_number (index.csv)

Filled for 5 of 122 rows, only where the number is certain: Dogstar = Hart 1996, tetrahedral stellations of the dodecahedron, no. 8 (as
cited in #42); AXE = Mosseri–Sadoc t6 and CLEO = Mosseri–Sadoc t4 (both scaled by 1/τ; DICTO confirmed 10-23); Half octahedron P = J1
(the square pyramid with equilateral triangles, half the regular octahedron); Delilah = U5; W2 (regular octahedron: Maeder's uniform index,
Wenninger's model number). Conventions in the README. Empty elsewhere: the other known shapes (Bain's, the parallelepiped and rhombohedron
of F1, the Cleo-Icos, the tetrahedron face pyramid, the Reuleaux tetrahedron, the Icosaxes and Unborn Axes, which are Koca et al.'s
non-uniform truncated octahedra) have no catalogue number we are sure of.

**D-numbers (DICTO's decision, 2026-10-24).** DICTO chose D-numbers as his permanent catalogue numbers (T stays a piece's label within a
piece set; # papers; F findings; t1–t6 Mosseri–Sadoc). They are in `universal_number`: **D1–D71** for 71 single new solids and pieces in
order of first publication (D1 = DICTO skewed rhombic dodecahedron … D71 = Samson), and **D72–D75** for the four rows that group several
pieces (dented tetrahedron L/R, DICTO Fill set pieces, Cleo Towers, Polar Cleo Towers; one number per group row for now, placed after
D71 so the 71 keep their order). Known and rediscovered shapes get none; the 9 solids and pieces among them without an outside number are
listed in `d-numbers.md`. No shape has both an outside number and a D-number (the rule: outside number first, "; ", then D). In all,
80 of 122 rows carry a number: 5 outside, 75 D. No published paper used a T-number before (all paper sources searched).

### Totals (version 2)

index.csv: 122 rows: **104 new, 4 rediscovered, 14 known**. Counting grouped rows one by one: **125 new, 4 rediscovered, 15 known, 144
named shapes**. By kind (rows): 42 solids, 47 pieces, 14 clusters, 16 structures, 1 compound, 2 curved bodies. Of the 144, **29 are in
this dataset**; with 6 fills and 4 non-filling packings.

### Open questions for DICTO

1. D-numbers for the four grouped rows (D72–D75): one per group, as now, or one per piece (from D76 on).
2. Delilah's row name: "Delilah" (as now) or "Regular octahedron (Delilah)" under the one-name rule.

## Second pass (2026-10-23), DICTO's decisions

- **Status labels confirmed by DICTO 2026-10-23** (see Inventory totals).
- **One name per shape: the first name DICTO chose wins; a shape with an established literature name keeps that name with DICTO's
  beside it (DICTO 2026-10-23).** So Oktaktis (#43) is merged into Cleo-Icos (named first, #29): its index.csv row is deleted and the
  Cleo-Icos row notes "appears in #43 as the OTT's octahedral ray, there called Oktaktis (DICTO DOI: 10.5281/zenodo.23532013)"; its
  Polyhedraverse id OTT_CLEO_ICOS is listed beside ICOSA_FACE_PYRAMID.
- **Non-filling published packings added** (`packings-nonfilling/`): OG on bcc (#31), OCD Stella on bcc (#31a), DBT on the gyrated
  octet and OTT on the octet (#37a). Every density equals its paper exactly: (9225 − 3915√5)/608 = 77.43%, 151/2 − 267√5/8 = 87.12%,
  493/6 − 73√5/2 = 55.02%, 176/3 − 26√5 = 52.89%. **No value disagreed with a paper; none was left out.** The OCD Stella packing
  needed the solid itself, so the DICTO OCD Stella (#31a) is now in `solids/`, built exactly from the planes the paper states (golden
  envelope of inradius 2/3, 20 three-fold planes at squared distance 14/27 − 10√5/243, the bcc Voronoi cell); it matches the paper
  (48 corners, 50 faces 6/24/20, volume (−4064 + 2240√5)/729, pyritohedral; companion C 72 corners, (−18880 + 9760√5)/2187) and the
  study's float corners (corner matching). Choices, from the papers: the OG's bcc packing is the one whose joint hexagons point along
  (±1, ±1, ±1) (one of its five, #31); the OTT is given on the octet (#37a: the same density in every stacking); the DBT on the gyrated
  octet with the next layer as its mirror twin (= the half-turn about (1,1,1), checked exactly).
- **Unit volume as a second common size**: every solid keeps its paper frame and also has `unit_volume` (scale s = V^(−1/3), exact
  symbolic; corners as 15-place decimals) and `solids/<slug>-unit-volume.off`. Centre: the exact corner centroid, which is the paper
  frame's origin for 21 solids; the Dodeca-13 Wedge and Needle are scaled about their corner centroid.
- **Check of Jewel-Tetra / Jewel-Octa (#41) against the F15 clusters** (DJ_TETRAHEDRAL_CLUSTER, DJ_OCTAHEDRAL_CLUSTER, Polyhedraverse
  in kaleidohedra krp-core): **the same solids.** Built from the #41 study's definitions (the Jewel of jewel_exact.py, cells as in
  cluster_exact.py), corner matching up to rotation/reflection and scale: Jewel-Tetra 131 corners ↔ 131 (surface 228 faces both),
  Jewel-Octa 188 corners ↔ 188 (170 surface corners, 288 faces both), max deviation < 1e-15, scale φ/2 (Polyhedraverse's display
  scale), identity rotation; the face sets coincide too. index.csv still lists them as separate rows (not changed, as asked).

## What is in it

- **23 solids**, all exact in ℚ(√5), each with exact corners + 15-digit decimals, faces wound outward, f-vector, symmetry, exact
  volume and edge lengths, normalisation, source and published values:
  - OG family first: DICTO Hecatodihedron (#28), DICTO Ogdoecontahedron (#31), DICTO GTI and FPD (#38), DICTO KRE, PHE, TPP, DPHP,
    TPH, TQH, TQP, TQHD (#39), DICTO Metaxyhexecontahedron (#35a), DICTO Palintriacontahedron (#35b), DBT and OTT (#37a).
  - Then in finding order: DICTO skewed rhombic dodecahedron (F1), skewed ED F16 and F18 (F7), DICTO Jewel (F10/#41), Dodeca-13
    Wedge and Needle (F13).
  - Added 2026-10-23: DICTO OCD Stella (F31a/#31a).
- **3 packings** (published fills): the skewed RD (DICTO FCC) and both skewed EDs, each tiling space by translation.
- **4 packings that do not fill space** (published): OG bcc 77.43%, OCD Stella bcc 87.12%, DBT gyrated octet 55.02%, OTT octet 52.89%.
- **A unit-volume copy of every solid** (JSON key `unit_volume` + `-unit-volume.off`).
- **check.py: 550 checks, 550 passed, 0 failed** (23 solids, 3 fills, 4 non-fills, unit-volume copies; about 2 minutes on dicto-node).
  It also failed, as it should, on corrupted copies (reversed face, moved corner, wrong group order, an extra overlapping piece; and
  on 2026-10-23 a shrunken non-filling lattice, a wrong published percentage, a moved unit-volume corner: 9 checks failed).

## Inventory totals (index.csv)

116 rows: **101 new, 4 rediscovered, 11 known** (Oktaktis merged into Cleo-Icos; the F15 Jewel clusters merged into Jewel-Tetra and Jewel-Octa and the F16 Sunstar clusters into Sunstar-Tetra and Sunstar-Octa, DICTO's choice of the concise #41/#42 names; 2026-10-23). Some rows group several named shapes
(Cleo Towers: 8 pieces; Polar Cleo Towers: 7 + core ray; the four new Reuleaux bodies; DICTO Fill set pieces: 4; dented tetrahedron
L/R; Q and Q′). Counting those one by one: **122 new, 4 rediscovered, 12 known, 138 named shapes in all**. By kind (rows): 36 solids,
47 pieces, 14 clusters, 16 structures, 1 compound, 2 curved bodies. Of the 138, 23 are in this dataset.

Rediscovered: regular-hexagon ED (F5, Grünbaum 2010), Dogstar (Hart 1996, stellation 8), Sunstar Lattice (Hart's honeycomb),
Bodhi seed (partly: Kabai's cluster layer). The status column copies the wording of DISCOVERIES.md and the papers; it makes no new
claim. The labels set from the text, DICTO all-rhombus block and DICTO flattened rhombohedron as "known" (a parallelepiped and a
rhombohedron, parts of F1), Oktaktis as "known" (#43: exactly the Cleo-Icos shape; now merged into the Cleo-Icos row) and Cleo-Icos as
"known shape, DICTO's name", are confirmed by DICTO 2026-10-23.

## Checked against the published papers

Downloaded the latest published PDFs from Zenodo (records listed in `published/records.json`) and compared exactly:
- #28: H has 80 corners, 180 edges, 102 faces (60 triangles, 30 rhombi, 12 pentagons); volume (−365 + 189√5)/4 ≈ 14.4042 (paper: 14.4042).
- #31: OG 102, 180, 80; 60 kites, 20 hexagons; volume (−1000 + 1240√5)/1539; squared edges 2/9 − 2√5/27 and 86/3249 + 2√5/361: all equal.
  The OG built by the #39 construction is the #31 OG scaled (corner-matching test, scale² = 27/8 + 9√5/8), and its volume at that
  size is (525 + 185√5)/57, as #39 states.
- #38: T⁴(ID) = (35 − 15√5)·ID = (10/φ⁴)·ID exactly.
- #39: all eight f-vectors (92/180/90, 180/270/92, 212/390/180, 270/420/152; 80/210/132, 132/270/140, 140/300/162, 162/360/200) and
  the exact volumes of the study's exact_upward/exact_downward.json (the paper's Tables) equal.
- #35a, #35b: closed forms, 32/90/60, volumes 410/27 + 550√5/81 and 50/3 + 50√5/9, both squared edge lengths: equal.
- #37a: DBT (−872 + 440√5)/81, 30/60/32, D3d; OTT (−608 + 320√5)/81, 24 corners, 38 faces, Th: equal.
- #31 (bcc packing) and #31a (OCD Stella and its packing), #37a (DBT on the gyrated octet, OTT on the octet): densities and the OCD
  Stella's values as in the second-pass section above: all equal.
- F1/F7 (archive): volumes φ², φ² + 2, φ³ + ½; face counts: equal. #41: Jewel volume 12 on cells of edge 2 (here 3 + 3√5/2 at
  cell edge φ): equal. #13: wedge φ³/20, needle (45 − 19√5)/600 at edge 1: equal.

**Disagreements with a published paper: none found** in these values. Observation only (not a paper): in DISCOVERIES.md on master the
table rows F30 and F38 have their Credit/Verified/Status/First-recorded cells empty.

## Not in Polyhedraverse (dataset solids)

DICTO GTI, DICTO FPD, DICTO Ogdoecontahedron, DICTO KRE, PHE, TPP, DPHP, TPH, TQH, TQP, TQHD, DICTO Metaxyhexecontahedron, DICTO
Palintriacontahedron, DICTO DBT, DICTO OTT, DICTO OCD Stella (16 of 23). Taken from Polyhedraverse and proved exact: Jewel (DRAGON_JEWEL), Dodeca-13
Wedge and Needle, skewed RD, ED F16, ED F18; the Hecatodihedron (TRANS_DHARMA_80, stored with 6 decimals) was built exactly from #28
and matched to it corner for corner (max deviation 1.7e-5).

## Named, published, but not yet in the dataset (what remains)

- Version 4 (2026-10-28): Icosaxes Bloom, Bud and Seed and Lotus Jewel Bloom, Bud and Seed (#59 v2; unions: open windows, a hollow, or
  overlapping pieces with no exact union in the study), Fallen Humpty / Slice-48 (#62/#63; numeric only, 120-digit roots, no exact closed
  form), the Icosaxes Kagome (#59; a network), the keyed #56 forms (Sonsam-K, Lahdeli-K, Ian Dury-K, Rhombo-K; floats only in #56).
- No exact geometry obtained in this pass: DICTO Hexa, Hexa-Key,
  Hexa Jewel (Polyhedraverse floats are approximate, e.g. −0.5000000091; need the study's exact data), Jewel and Sunstar clusters
  (#41, #42), Stretched dodecahedron (F11), Lotus Jewel (F21), FUJI and the 13s pieces (Polyhedraverse stores 7-digit floats), Kion,
  Atraktos, Aetos, Sphen, Sphenion (#29), GBPC and Bull-horns (#36), the #37 kit pieces, Fill set pieces and Mg (#37a), Five-sided
  Vajra, hexagonal Cleo, Monkey Staff B (#38), the #43 towers and the TQ series (TQP-252 … TQP-672; built only in a node pickle).
- #43 rays and Aktis (Triaktis, Tetraktis, Deltoid Aktis, Hex Aktis): tried; Polyhedraverse stores them turned, in coordinates outside
  ℚ(√5), so they need the study's exact frame.
- Packings still to add (published fills): Jewel + stella octangula (F10b/#41), Hexa + Hexa-Key 5 : 3 (F18), dodecahedra + Dogstars
  (#42), the #37/#37a kits, the #47 mixes, Spheroid-13 RD (F25). The checker handles convex pieces only; the non-convex fills need a
  convex split of each piece first.
- Non-filling packings not in the four DICTO named (not added): the OCD Stella crystals with icosahedra or octahedra (#31a), the OG on
  the octet (45.89%, #40), the densest lattice packings found by search (float values only).
- Out of format: the Reuleaux bodies (#45) are curved; the Hecatogdoecontahedron (#34a) is a compound (its two components are here).

## Unpublished names left out of the dataset and the inventory

DICTO Ball set 1 (B1, T1, T2), Tetoktjiru (Oktjiru, Tetjiru), the tetrapod clusters (TETRAPOD_FIVE_TO, TETRAPOD_FOUR_RD), DICTO Hexa
roof, DICTO square-faced block, DICTO leaning hexagonal prism, Pentagonal pocket (CLEO sphere), Kepler Star Diadem (app only), the #46
Mandala of Shells, the swept dodecahedra (#49 draft), the DICTO stretched solids (stretch-studies branch), DICTO Square and DICTO
Seal studies, Heikegani, scutoid pieces.

## Open questions for you

None left from the first build: the status labels are confirmed, the non-filling packings and the unit-volume size are in, and the
Jewel-Tetra/-Octa are the F15 clusters: merged into one row each, keeping the #41 names (DICTO 2026-10-23: "#41 more concise"),
with the F15 names noted. The same for the F16 Sunstar clusters = #42 Sunstar-Tetra/-Octa (corner match, scale φ/2; check script
scratchpad/ss/congruence_sunstar.py; DICTO 2026-10-23: keep the #42 names).
