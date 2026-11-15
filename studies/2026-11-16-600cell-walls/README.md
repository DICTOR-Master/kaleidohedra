# Are the new shapes hidden in the 600-cell's walls? (16 Nov 2026)

**Conclusion: yes for solid A, half for solid B.** All 30 of A's central plates are walls of the 600-cell. For B, 40 of its 80 plates are walls. The other 40, through its φ√2 triangles, are the walls that give B away. Floating point (tolerance 1e-7); an exact recheck is to come.

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

LEADS: (1) exact recheck in Q(√5); (2) the same test on the other recent shapes (GET, the echo shapes, the 2I twisted classes of other degrees); (3) where B's 40 visible plates do lie: a second H4 wall system (e.g. the Galois-twisted mirrors, √5 ↦ −√5), which would make B hidden in the 600-cell and its Galois twin together.
