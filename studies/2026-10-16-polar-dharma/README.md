# Spheres of Dharma turned inside out: polar reciprocation (DICTO's 2026-10-13 idea; step 1, 2026-10-16)

After the flip test (studies/2026-10-16-flip-test: no skin turns over into a closed shell), the inside-out version by duality: each
station of the Ritsudō cycle replaced by its polar in the unit sphere; nesting reverses. `scripts/polar.py` (exact corners in Q(√5),
snapped from data/dharma_cycle.json; poles exact) -> `data/polar-step1.txt`, `data/reversed-chain.json`.

Reversed chain, inside to outside: dodecahedron ⊂ icosidodecahedron ⊂ dual of the Hecatodihedron (102 corners, 80 faces) ⊂ pentakis
dodecahedron ⊂ icosahedron ⊂ rhombic triacontahedron ⊂ dodecahedron φ³ larger. Closure exact: volume ratio 38 + 17√5 = φ⁹. Touching
carries over by duality (e.g. ID's 30 corners on the Hecatodihedron-dual's faces; the icosahedron's 12 corners are the triacontahedron's
5-fold corners). Layer volumes exact (see data). Sizes invert: Dharma's thick inner layer becomes the thick outer one.

Next (step 2): exact pieces for each layer; reciprocation does not carry Dharma's pieces over.

## Step 2 (2026-10-16): one kind of piece per layer

Each layer A ⊂ B cut into one piece per face F of A, cone(F) ∩ B ∩ {beyond F} (convex by construction; the Kion construction of #29);
faces of A lying on B's surface give nothing. `scripts/polar_pieces.py` -> `data/polar-step2.txt`, `data/polar-pieces.json`.

| Layer | Pieces | Each piece |
|---|---|---|
| D -> ID | 12 | 15 corners; 7 pentagons, 5 triangles |
| ID -> Hecatodihedron-dual | 12 (ID's 20 triangles lie on the outer surface) | 11 corners; 1 pentagon, 5 quadrilaterals, 5 triangles |
| Hecatodihedron-dual -> pentakis D | 20 (60 of 80 faces lie on the outer surface) | hexagonal pyramid |
| pentakis D -> I | 60 | 5 corners, 6 triangles (triangular bipyramid) |
| I -> RT | 20 | tetrahedron (Kepler's pyramids) |
| RT -> D(φ³) | 30 | 8 corners; 5 quadrilaterals, 2 triangles |

Every layer is ONE kind of piece (Dharma needs 2-3 in some); 154 pieces round the inner dodecahedron; sums match the layers (1e-9,
floats). No two neighbours fuse without a dent. Next: exact volumes, identify the shapes, renders, prior-art check.

## Step 3 (2026-10-16): exact, shapes, renders

`scripts/polar_exact.py` -> `data/polar-exact.txt`: every piece's corners exact (three exact planes each, Cramer in Q(√5)); each layer
one exact volume, sum − layer = 0 exactly in all six. Shapes: D→ID columns (7 pentagons incl. both stations' regular ones, 5 triangles
30-30-120°); ID→H* caps (regular pentagon, 5 quadrilaterals, 5 triangles 30-30-120°); H*→PD low pyramids on a regular hexagon (side edge
1.07 × base; not FUJI-family); PD→I irregular 5-corner wedges (incl. 30-60-90° triangles); I→RT Kepler's pyramids; RT→D roofs on the
rhombi, each ridge one dodecahedron edge, end triangles 54-72-54° (classical D/RT edge relation). Renders `renders/` (`scripts/render_polar.html`).

## Step 4: the tight nest (2026-10-16)

DICTO asked for a more even nest. The faithful polar version leaves two ends loose, because the original cycle's closure forces the outer dodecahedron to be the inner one × φ³. The triacontahedron could grow ×1.894 before touching the outer dodecahedron, and the inner dodecahedron ×1.232 before touching the icosidodecahedron. The four middle stations already touch, so they stay as they are. `polar_tight.py` tightens both ends (inner ×1.232241, outer ×0.527864):

- The outer layer drops from 25.23 to 1.915, and the closure goes from φ³ linear to 1.814635.
- The inradii are now 0.495, 0.567, 0.623, 0.653, 0.714, 0.764, 0.898.
- Each layer still has one kind of piece, and each layer sum equals the layer volume.
- The inner layer becomes 12 near-antiprism columns (10 corners, 2 pentagons, 10 triangles).
- The outer layer becomes 30 wedges (6 corners, a rhombus and 6 triangles) on the rhombi. Each wedge's ridge is a dodecahedron edge, and the 12 five-fold tips of the triacontahedron now touch the face centres of the outer dodecahedron.

The originals are unchanged: `reversed-chain.json`, `polar-pieces.json`, `polar-render.json` and `renders/polar-*.png`. The tight versions are named `*-tight*`: `data/polar-tight.txt`, `reversed-chain-tight.json`, `polar-tight-pieces.*`, `polar-tight-render.json` and `renders/polar-tight-*.png` (`node shoot_polar.mjs tight`). Exact check (`python3 scripts/polar_exact.py tight` → `data/polar-tight-exact.txt`): inner scale 11/18 + 5/18√5, outer scale 5 − 2√5, squared closure ratio 49815/2 − 22275/2·√5 (linear 1.814635, volume ×5.975, not a power of φ). Every layer has one exact piece volume, and in every layer the sum minus the layer volume is 0. The new end pieces are 12 × (−35/729 + 71/2187·√5) inside and 30 × (−7352/3 + 1096√5) outside.

## Step 5: Kepler–Poinsot solids in the big gap (2026-10-16, DICTO's question, faithful/original nest)

`polar_stars.py` treats each star as a filled body (nonzero winding number). The densities check out at the centre: 3, 3, 7, 7. For each star it finds the range of corner radius over which the triacontahedron (RT) sits inside the star and the star sits inside D(φ³) (`data/polar-stars.txt`):

- Great dodecahedron and small stellated dodecahedron: both fit for a corner radius from 1.453085 to 1.701302. At the low end, RT's 20 three-fold corners touch the dimple bottoms. At the high end, the star's 12 points touch the face centres of D(φ³).
- Great icosahedron: it does not fit. RT needs a corner radius of 1.984, and D(φ³) allows at most 1.701.
- Great stellated dodecahedron: it fits at exactly one size. Its 20 points are D(φ³)'s corners, and the RT touches it. `polar_gsd_exact.py` (`data/polar-gsd-exact.txt`) confirms this exactly in ℚ(√5): each of the chain's 12 icosahedron corners (which are also RT's five-fold tips) lies on 5 of the star's face planes. These 12 corners are the star's 12 valley points.

The GSD's two point sets (dodecahedron points and icosahedron valleys) are classical. What the check adds is that the polar Dharma chain already contains both, as its icosahedron station and its outer dodecahedron.

### Step 5b: the big gap cut around the great stellated dodecahedron (GSD)

The GSD body is the chain's icosahedron plus 20 spikes; its surface is 60 triangles, each seen once from the centre. `polar_gsd_pieces.py` cuts both sides of the star by the cones over those triangles. Results, exact in ℚ(√5), in `data/polar-gsd-pieces.txt`:

- RT → GSD: 60 tetrahedra T-K-a-b, all congruent. T is a star point, K a triacontahedron corner, and a, b are valley corners. Each has volume 188/3 − 28√5, and the sum minus the layer is 0.
- GSD → D(φ³): 60 irregular pentagonal pyramids, all congruent. Each has volume 112/3 − 248/15·√5, and the sum minus the layer is 0.
- The GSD's volume is −2320 + 1040√5, exactly 3 times the chain's icosahedron.
- The squared ratio of star points to valleys is 3φ³/√5. Apart from the fixed √3/√5 conversion between three-fold and five-fold corner radii, the step is φ³, the same φ³ by which the cycle closes.

Renders: `renders/polar-gsd-*.png` (`node shoot_polar.mjs gsd`). The `inner` view shows the star alone.

### Step 5c: the inner gap (inner dodecahedron → icosidodecahedron)

None of the four Kepler–Poinsot solids fit there (`data/polar-stars-inner.txt`). The Hecatodihedron (102 faces, 80 corners) does fit, but loosely: its scale can run from 0.314757 to 0.387857 of its original size, giving room ×1.2322, the same slack the dodecahedron has (`polar_heca_gap.py` → `data/polar-heca-gap.txt`). At the low end, the dodecahedron's 20 corners touch Hecatodihedron faces. At the high end, 20 Hecatodihedron corners touch the icosidodecahedron's triangles. Unlike the GSD in the big gap, no single size touches both. The same file lists the other original stations for comparison: the icosidodecahedron, dodecahedron, truncated icosahedron and RT fit, and the two icosahedra do not.

## Step 6: rounder solids? (2026-10-16, DICTO's question)

`polar_round.py` tests the icosahedral Archimedean solids and their Catalan duals (up to 120 faces) in both gaps; the results are in `data/polar-round.txt`. Each coordinate list is now checked against the chain's 5-fold axes. The first run had most of the solids in the mirror golden frame, which gave wrong numbers; it was corrected the same day.

- **Big gap, inside the great stellated dodecahedron, around RT:** only RT itself fits, and it locks (this also serves as a sanity check). RT's 12 tips sit in the star's 12 valleys, so anything rounder pushes out past them.
- **Inner gap, inside ID:** everything fits except the triakis icosahedron, but every fit floats. The room for each:
  - truncated icosidodecahedron: ×1.196
  - rhombicosidodecahedron: ×1.172
  - pentakis dodecahedron: ×1.152
  - truncated icosahedron: ×1.093
  - deltoidal hexecontahedron: ×1.074
  - disdyakis triacontahedron: ×1.053
  - (the rest are in the data file)

## Step 7: a dual pair instead of the Hecatodihedron? (2026-10-16, DICTO's question)

The test is the chain D ⊂ s1·X ⊂ s2·Y ⊂ ID; a pair locks when slack = 1. Results are in `polar_dual_pair.py` and `data/polar-dual-pair.txt`. No pair locks. These fit:

| Inner solid | Outer solid | Slack |
|---|---|---|
| rhombicosidodecahedron | deltoidal hexecontahedron | 1.0022 (nearest to locked, 0.2%) |
| RT | ID | 1.022 |
| disdyakis triacontahedron | truncated icosidodecahedron | 1.052 |
| deltoidal hexecontahedron | rhombicosidodecahedron | 1.074 |
| pentakis dodecahedron | truncated icosahedron | 1.093 |

The truncated icosidodecahedron does not fit inside its dual (slack 0.980). As DICTO noted, in the reversed chain the pair goes in reverse order.

## Step 8: the truncated icosidodecahedron pair in the inner gap (DICTO's choice)

`polar_pair.py` builds the chain D ⊂ DT ⊂ TID ⊂ ID ⊂ … The disdyakis triacontahedron (DT) touches the inner dodecahedron, and the truncated icosidodecahedron (TID) touches ID. In fact the TID's 12 decagons lie exactly in ID's pentagon planes. The play of ×1.052 sits between the pair. The cone cut (`data/polar-pair-pieces.txt`, float) gives:

- D → DT: 12 pieces of one kind (11 corners, 15 triangles and a pentagon).
- DT → TID: 120 pieces of one kind (one symmetry orbit; checked with `geomcheck.kinds`).
- TID → ID: 50 caps of two kinds, on the 30 squares and 20 hexagons.
- Each layer's sum equals the layer volume.

The outer layers are unchanged. Renders: `renders/polar-pair-*.png` (`node shoot_polar.mjs pair`).

**Exact check** (`polar_exact.py tid` → `data/polar-pair-exact.txt`): DT is scaled by 9 − 3√5 (= 6/φ²) and TID by 2/15, and the play is 5/9 + 2/9·√5 (= √5·φ³/9 ≈ 1.0525). Every layer's sum minus its layer volume is exactly 0. The DT → TID piece is −2300048/37125 + 3086012/111375·√5. The float hull's extra points that lie on edges (not true corners) are dropped, and the exact sums confirm that is safe.

## Step 9: the rhombicosidodecahedron pair (DICTO, 2026-10-16)

`polar_pair.py rid` builds the chain D ⊂ RID ⊂ DH ⊂ ID. The rhombicosidodecahedron (RID) touches the inner dodecahedron and the deltoidal hexecontahedron (DH) touches ID. The cut gives:

- D → RID: 12 pieces of one kind.
- RID → DH: 62 pieces in 3 kinds (12 + 30 + 20), on the pentagons, squares and triangles.
- DH → ID: 60 pieces of one kind.

**Exact check** (`polar_exact.py rid` → `data/polar-pair-rid-exact.txt`): RID is scaled by −153/11 + 69/11·√5 and DH by 1 + 3/5·√5. The play is exactly 62/123 + 137/615·√5 = 1.002181, so the pair is close to locked but not locked. All layer sums are exact. Renders: `renders/polar-pairrid-*.png`.

## Step 10: golden rectangles around the whole structure (DICTO's question)

`polar_golden_rect.py` (`data/polar-golden-rect.txt`) tests the 15 golden rectangles (5 perpendicular triples, 60 edges), with corners on the 12 five-fold axes, against the original nest.

- **Corners on the chain's icosahedron:** the corners are RT tips and GSD valleys. The rectangles cut through the inner shells.
- **Corners on D(φ³)'s face centres:** the rectangles lie inside D(φ³).
- **The smallest icosahedron around D(φ³):** not enough to enclose the nest.
- **The next turn of the cycle's icosahedron (the chain's icosahedron × φ³):** the rectangles clear the nest. **Each of D(φ³)'s 30 edges lies along one of the 30 long edges, centred on it**, and each long edge is exactly φ³ times as long (6.472 against 1.528). Exact check: corner radius² = 10 + 2√5, and long-edge midpoint radius² = 4 = D(φ³)'s midradius².

**Correction (2026-10-16):** I first reported only that the long edges "touch the edge midpoints". They contain the whole edges. This makes the result classical. The 30 long edges are the edges of D(φ³)'s **small stellated dodecahedron**, the first stellation, made by extending the dodecahedron's edges (Kepler 1619). Its 12 points are the next turn's icosahedron, and a pentagram chord is φ³ (= 1 + 2φ) times the pentagon's side. So the frame that encloses the nest is the outer dodecahedron's own small stellation.
Renders of the nest inside the 15 golden rectangles: `renders/polar-rect-*.png` (`node shoot_polar.mjs rect`; the render data is `data/polar-rect-render.json`, written by `polar_golden_rect.py`).

## Accuracy checks (from 2026-10-16)

The slips in steps 6–8 led to a shared module, `studies/_lib/geomcheck.py`, tested by `studies/_lib/test_geomcheck.py` (6 checks; each replays one of today's slips). Its rules are:

1. Frame: every solid is checked against the chain's own axes, using `frame` and `orient`.
2. Both nesting orders are always tested. Polar reversal swaps a dual pair's order.
3. Each formula is first checked on a case with a known answer.
4. Piece kinds are counted by symmetry orbit, using `corners` and `kinds`. Float face counts are not used.
5. An exact remainder of 0 is required before a claim.
6. Every number is labelled exact or float, and faithful or adjusted.

`polar_pieces.py` now uses rules 1 and 4.

## Prior art (checked 2026-10-16: reference library + web)

| Claim | Status | Source |
|---|---|---|
| Polar reciprocation reverses inclusion (P ⊂ Q gives Q* ⊂ P*), so the reversed chain nests, and a dual pair swaps order in it | **classical** (convex geometry). DICTO's order rule applies it. | stated in Firsching 2015 (library) |
| Fit and slack tests: the largest scaled copy of one polytope inside another | **known problem** (Croft; Firsching computes it exactly). Our tests are the concentric, same-orientation case. | Firsching 2015 |
| Nested icosahedral shells in general | **known context** (clusters, viruses, fullerenes) | Twarock–Valiunas–Zappa 2015; Dechant et al. 2014 (library); Spheres of Dharma shells = the Tsai-cluster family (#23) |
| GSD = icosahedron + 20 pyramids; GSD volume = 3 × that icosahedron | **classical**. The volume ratio follows from the standard formulas (5/4·(3+√5)a³ against 5/12·(3+√5)a³). | Kepler 1619; DISCOVERIES #27; Hafner 2007 |
| The GSD and the RT together | **related work**: Hafner dissects SSD + GSD into RT + hexecontahedron, with 60 tetrahedra each 1/6 of a prolate golden rhombohedron. Our 60 tetrahedra (GSD minus RT) are different pieces. In floating point, each has φ² times his volume on the RT edge (not yet checked exactly). | Hafner 2007 (link only) |
| The reversed Dharma cycle containing the GSD's points (its outer dodecahedron) and valleys (its icosahedron), locked with RT | **not found**. It follows directly from the classical facts above. Present it as an observation about DICTO's cycle, not as a new theorem. | library + web |
| Frame of 15 golden rectangles around the nest | **classical**: it is the outer dodecahedron's small stellated dodecahedron. | Kepler 1619 |
| Tight nest (5 − 2√5, 11/18 + 5/18·√5); dual pairs in the inner gap (TID pair: 6/φ², play √5·φ³/9; RID pair: play 1.00218); the exact cone-cut pieces and volumes | **not found** | library + web |
| The dual of the Hecatodihedron, and the Hecatodihedron itself | **not found** (#28) | — |
