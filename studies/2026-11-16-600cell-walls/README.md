# Walls of Silence: are the new shapes hidden in the 600-cell's walls? (16 Nov 2026)

Naming (DICTO, 16 Nov 2026): this study is the start of the paper **Walls of Silence** (where the silent shapes live). With Silent Running: Twisted Silence (the mechanism; the law kind is twisted silence) it forms the Brief Geometry chapter **Twisted Walls of Silence**.

**Conclusion (with DICTO's ruling, 16 Nov: "cross walls also count"): every central plate of both new shapes is a 600-cell wall, confirmed exactly in Q(√5).** Solid A: all 30 plates are mirror walls. Solid B: 40 mirror walls + 40 cross walls (central sections parallel to the 600-cell's cells). Ordinary orbits without the twist have most of their plates in no 600-cell wall. DICTO's theory holds for both shapes: they were hidden in the 600-cell's walls.

**DICTO's theory (16 Nov 2026, his words):** "the reason that all the recent and otherwise undiscovered shapes are vacuus is that because of this they have previously been indistinguishable from 600 cell walls". Restated and confirmed by DICTO: each shape's walls (the central plates of its Vacuus) coincide with walls the 600-cell already has, so inside the 600-cell they look like part of its own structure.

## Test

P = the 600-cell, built as the closure of X under reflection in its own members (120 points; F lies in P at the same radius, 30 of 30).
The 600-cell has two kinds of wall: its 60 mirror hyperplanes (H4), and its own Vacuus plates, the central hyperplanes spanned by its 1200 triangles.
For each 2-face of a solid, we took the central hyperplane it spans and checked whether it is one of these walls.

| set | 2-faces | plates | 600-cell walls | not walls |
|---|---|---|---|---|
| 600-cell P (positive control) | 1200 triangles | 60 | 60 (its own Vacuus plates ARE its 60 mirrors: heart kind, 20 triangles per plate) | 0 |
| **solid A** (X, perms of (φ², φ², φ², φ, 0)) | 20 triangles + 10 hexagons | 30 | **30**: all 20 triangle plates and all 10 hexagon plates | 0 |
| **solid B** (F, perms of (φ², φ², 1, 1, 0)) | 50 triangles + 30 rectangles | 80 | **40**: 30 rectangle plates + 10 √2-triangle plates | 40 (the φ√2 triangles, both kinds B1, B2) |
| ordinary orbit (φ², φ², φ², 1.5, 0) (negative control) | 30 | 30 | 10 (hexagon plates only) | 20 |
| ordinary orbit (φ², φ², 1.2, 1.2, 0) (negative control) | 80 | 80 | 10 | 70 |

Reading: every orbit of the 5-cell's symmetry group has a few plates in the shared mirrors (the 10 S5 mirrors are H4 mirrors too).
The golden twist adds the rest. A gains all 20 triangle plates, so every wall of A is a 600-cell wall. B gains its 30 rectangle plates, but not its 40 φ√2 triangle plates.
In DICTO's picture, A is fully hidden in the 600-cell's walls; B is half hidden, and its φ√2 triangles are what a listener could see.

Files: scripts/walls.py, data/walls.log (FINAL ok). Ran on the compute machine, under 5 min.

## Lead 3 done: the 120-cell (16 Nov)

The 120-cell (dual, 600 corners, 120 cells, 720 pentagons) has its 720 pentagons on 60 central plates, and these are the SAME 60 H4 mirrors (12 pentagons per plate). So the 600-cell and 120-cell share one wall system: the 60 mirrors. B's 40 φ√2-triangle plates are in neither; B stays half hidden (40 of 80) even in the pair. Files: scripts/walls120.py, data/walls120.log (FINAL ok; checks 600 corners, 120 cells, 720 pentagons).

## Where B's 40 visible plates lie (16 Nov)

The Galois-twin 600-cell (closure of perms of (σ², σ², σ², σ, 0), σ = −1/φ) has the SAME 60 mirrors, so that is no new wall system (scripts/walls_twin.py, data/walls_twin.log).
Comparing the plate directions with the 600-cell's own directions (scripts/walls_where.py, data/walls_where.log; checks 720 edges, 1200 triangles, 600 cells):
- B's 30 rectangle plates and 10 √2-triangle plates: perpendicular to a corner of the 600-cell (its mirrors);
- **B's 40 φ√2-triangle plates: perpendicular to a corner of the 120-cell** (a cell centre of the 600-cell). Each is the central section of the 600-cell parallel to a pair of its opposite tetrahedral cells: the equator of a 120-cell corner axis.
So every plate of B is a central plane that the 600-cell–120-cell pair already has: 40 mirror walls and 40 equators of the 120-cell's corner axes (300 such planes). DICTO 16 Nov: "cross walls also count". So these cell-parallel central sections are 600-cell walls too.

Control for the equators (scripts/walls_where_ctl.py, data/walls_where_ctl.log): the ordinary orbits' non-mirror plates (40 + 30 and 20) point along NONE of the 600-cell's directions (corners, edge midpoints, triangle centres, cell centres). So the equators are special to the twist: with it, every one of B's 80 plates is a central plane of the 600-cell–120-cell pair; without it, most plates are in no such plane.

LEADS: (1) the same test on the other recent shapes (GET, the echo shapes, the 2I twisted classes of other degrees).

## The other recent shapes (16 Nov, later)

**Conclusion: the theory holds for the golden icosahedral shapes, and fails for the octahedral ones and the 120-cell silence sets.** It holds for R, the four 30-point silence sets, and the two icosahedral echo cuts; these are all-wall where random shapes of the same kind almost never are. It also holds for GET and the 60-point silence sets, but every ordinary shape of their kind passes too, so the test cannot single them out. It fails for the two octahedral echo cuts, the octahedral GP(2,0) solid and the two 240-point 120-cell silence sets. Exact in Q(√5) (Q(√2) for GP(2,0)).

**Walls used.** 4D shapes: plates = central hyperplanes of their 2-faces, tested against the 60 mirrors and 300 cell-parallel cross walls of the 600-cell (the census 120-cell has the same system; checked). 3D shapes: plates = the central plane through each edge (the fins of #87), tested against (i) the matching 3D figure and (ii) the 600-cell walls seen in the 3D central section that carries the shape's frame (a wall's trace on that section; the wall whose hyperplane is the section itself is left out).
- (i), icosahedral: 15 mirrors; cross walls parallel to opposite faces of the dodecahedron (6) and icosahedron (10). The triacontahedron's face-parallel sections are the mirrors themselves.
- (i), octahedral: 9 mirrors; cross walls parallel to opposite faces of the octahedron (4). The cube's and rhombic dodecahedron's are mirrors.
- (ii) is automatic for central sections of the 600-cell and 120-cell, because every 2-face of either spans a mirror. So for the echo cuts (i) is the real test; for GET, (ii) is a real test too.

| shape | plates | mirror walls | cross walls | no wall | theory |
|---|---|---|---|---|---|
| solid A, solid B (repeat; also −A, −B) | 30; 80 | 30; 40 | 0; 40 (600-cell cells) | 0; 0 | holds (positive control) |
| R, the third 20-point twisted class of 2I (C3) | 5 (its 70 2-faces lie on 5 plates) | 0 | 5 (600-cell cells) | 0 | holds |
| silence sets [C3 × C5] 30 points, (a), (b) | 45; 90 | 30; 60 | 15; 30 | 0; 0 | holds |
| silence sets [C5 × C5] 30 points, (a), (b) | 55; 55 | 55; 30 | 0; 25 | 0; 0 | holds |
| silence sets [C3 × C10] 60 points, (a), (b) | 30; 75 | 30; 60 | 0; 0 | 0; 15 | holds for (a), mostly for (b); not distinctive at 60 points |
| silence sets [C5 × C5].2 60 points, (a), (b) | 55; 30 | 55; 30 | 0; 0 | 0; 0 | holds; not distinctive at 60 points |
| silence sets [C5 × 2T] 240 points of the 120-cell, (a), (b) | 420; 600 | 60; 60 | 120; 120 | 240; 420 | **fails** |
| 600-cell central cut across a vertex axis (42/120/80) | 21 | 15 | 6 (dodecahedron faces) | 0 | holds |
| 120-cell central cut across a cell axis (GP(2,0) type, 80/120/42) | 25 | 15 | 10 (icosahedron faces) | 0 | holds |
| 600-cell central cut across a cell axis (84/240/158) | 45 | 9 | 0 (octahedron faces) | 36 | **fails** in cube/octahedron walls (45/45 in the 600-cell's own section walls, automatic) |
| 120-cell central cut across a vertex axis (78/120/44) | 31 | 3 | 4 (octahedron faces) | 24 | **fails** likewise (31/31 automatic) |
| octahedral GP(2,0) polar, cube cut at √2 (32/48/18) | 18 | 6 | 0 | 12 | **fails** (the ordinary cut at 3/2 gives the same 6 + 12) |
| GET A, GET B (60 edges each, centre of the parent triacontahedron) | 15 | 15 | 0 | 0 | holds, but not distinctive (below); same in (ii) |

**Controls.**
- **Must pass:** A, B (above); the triacontahedron (15 of 15 mirror, also in (ii)); the octahedron on the frame's 4-fold axes (3 of 3); the cube (6 of 6).
- **Must fail (mostly no wall), all did:**
  - ordinary S5 orbits: 20 of 30 and 70 of 80 in no wall;
  - the four echo cuts moved off centre to 3/10 of the height: 120/135, 90/90, 288/294, 132/138 in no wall (also mostly no wall in (ii));
  - GET A and GET B on a non-golden star (φ → 8/5): 30 of 33 each;
  - the cube cut at 3/2: 12 of 18.
- **Baselines for subsets of the 600-cell** (A, B, R and the 600-cell silence sets are all such subsets): random subsets already have most plates in walls.

  | random subsets | mean share in no wall | samples with every plate a wall |
  |---|---|---|
  | 20 of the 600-cell | 28% | 0 of 100 |
  | 30 of the 600-cell | 20% | 0 of 100 |
  | 60 of the 600-cell | 2% | 60 of 100 |
  | 240 of the 120-cell | 74% | 0 of 10 |

  So "all walls" sets A, B, R and the 30-point sets apart from chance, but the 60-point sets fail to stand out.
- **The GET family:** all 59 ordinary surfaces of the flip search (depth 1 to 5) and the six undecided candidates 2 to 7 also have their 60 edges on the 15 mirror planes. These surfaces are built from the triacontahedron's own rhombohedra, so their corners stay on the symmetry axes and every edge lies in a mirror. Measured from GET's own corner centroid instead, only 2 of 54 (A) and 3 of 51 (B) plates are walls.
- **Exactness:**
  - All zeros are decided exactly in Q(√5), with the a + bφ arithmetic of the echo-shapes study.
  - A nonzero value is certified when its float exceeds 1e-6, far above the rounding error, which is asserted below 1e-11.
  - An independent sympy pass re-decided every (plate, wall) pair for the 29 smaller shape comparisons, and all 29 agree.
  - Every plate was checked to be exactly one plane through the centre.
  - The f-vectors 42/120/80, 80/120/42, 84/240/158, 78/120/44 and 32/48/18 match the echo-shapes README.
  - 172 checks, 0 failed.
- **Coordinates came from the studies, not from memory:**
  - the S5 orbits, 600-cell and 120-cell from `2026-11-15-echo-shapes/scripts/shadow_echoes.py`;
  - the silence sets from `2026-11-16-remaining-silences/data/remaining-silences.json`, as indices into the census 600-cell of `2026-11-15-hidden-zeros-h4`;
  - GET and its family from `2026-11-15-grunbaum-k10/data/search6.json` (candidates 0, 1; tile12 confirms both tile);
  - GP(2,0) from the echo-shapes README definition.
  - The standard 120-cell of `shadow_echoes.py` is not dual-aligned with the standard 600-cell there, so its cuts use its own copy of the wall system (60 + 300).

Files: scripts/walls_others.py, data/walls_others.json, data/walls_others.log (FINAL ok, 28 s on the compute machine; a pilot ran first).

LEADS:
1. **Sharpen the baseline for 600-cell subsets.** Compare with random subsets of the same symmetry order or the same number of 2-faces, not only the same size. The 60-point sets cannot be judged until this is done.
2. **GET needs a test that does not depend on the centre.** Candidates: its tiling lattice's own walls, or the planes of its 16 cell rhombohedra.
3. **The octahedral shapes against the 24-cell's walls.** This covers the octahedral GP(2,0) solid and the two O_h echo cuts. Their natural host may be the 24-cell (F4) rather than the 600-cell. The same applies to the 6- and 8-point twisted classes of 2T and 2O, which were not run here.
4. **The 120-cell 240-point sets fail.** Test them against walls of the 120-cell–600-cell pair beyond the 360 used here, for example the hyperplanes parallel to its 2-faces.
5. **Not run:** the W(H4) twisted classes in S¹⁵ (no 600-cell wall system in 16 dimensions) and the dial's isolated 60-point orbits (not named as shapes).
