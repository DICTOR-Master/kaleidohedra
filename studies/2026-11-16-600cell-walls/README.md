# Are the new shapes hidden in the 600-cell's walls? (16 Nov 2026)

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
