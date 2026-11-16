# The Queens' walls as the structure: the chambers they cut (16 Nov 2026)

**Conclusion (exact count, three independent methods): the Queens' 360 walls (60 mirrors + 300 cross walls) cut each Queen into 4,291,200 chambers = 14400 × 298. Inside one H4 Coxeter chamber there are 298 pieces, no two congruent, of 15 combinatorial types. Every chamber is a pyramid from the centre over one piece of a cell, with 5 to 11 corners. Mirrors alone give the control: 14400 congruent H4 Coxeter chambers (orthoschemes). The wall system cuts out none of the named shapes as chambers. For A, its own 30 walls cut it into 3360 chambers, and 120 of them are exactly the 600-cell's Coxeter chamber. For B, its own 80 walls cut it into 62,880 chambers, none of them a Queen chamber.** The Queens' structure is fine-grained. The large shapes of Study 1 are not its chambers; they are unions of chambers whose walls happen to be Queen walls.

DICTO's question (16 Nov 2026), in his words: "if these are the shapes where is the structure, and if these are the structure where are the shapes". Study 1 (`studies/2026-11-16-queens-vicinity-vacuus`) read the shapes as Vacuus. This study takes the walls as the structure and finds the shapes they cut out.

## The structure
- **Mirror walls:** 60 hyperplanes, the H4 mirrors, shared by the 600-cell and the 120-cell.
- **Cross walls:** 300 central sections, each parallel to a pair of opposite tetrahedral cells of the 600-cell. Their normals point to the 120-cell's corners.
- **The 120-cell adds no walls of its own.** Its cells are centred on the 600-cell's corner directions, so the sections parallel to its cells are the 60 mirrors (exact check). The full system is 360 walls.

## Method
Every chamber of the 360 walls lies inside one chamber C of W(H4), because the mirrors are among the walls, and W(H4) carries C onto its 14400 images. So #chambers = 14400 × #(regions of C cut by the cross walls through its interior). Inside C the 600-cell is the pyramid from the centre over 1/24 of one tetrahedral cell, and the 120-cell the pyramid over 1/120 of one dodecahedral cell. So every chamber is the pyramid from the centre over one piece of a cell, and the two Queens have the same chamber count and the same combinatorial types (the cones are the same; only the cutting cell differs).
1. **Exact (Q(√5))**: Zaslavsky's count in the open simplex section of C, summing |Möbius| over the flats that meet it. Lines and points are found by exact nullspaces, and "meets the interior" is decided by exact sign tests.
2. **Float splitting**: the cell piece is cut wall by wall, and the pieces are listed with their faces and volumes.
3. **Float whole lattice**: the full intersection lattice of the 360 hyperplanes in R⁴ (35,042 planes and 803,160 lines). Its sum of |Möbius| must equal 14400 × (1).

## Results (`data/chambers.log`, `data/chambers-control-cross-ab.json`)
**Control, mirrors only (exact).** The 60 mirrors have characteristic polynomial (t−1)(t−11)(t−19)(t−29), so they make 2·12·20·30 = **14400 chambers**, one class. Each is the H4 Coxeter chamber (orthoscheme): 5 corners, 10 edges, 10 triangles, 5 tetrahedral cells. For the 600-cell its corners are the centre, a cell centre, a triangle centre, an edge midpoint and a corner; for the 120-cell, the centre, a dodecahedron centre, a pentagon centre, an edge midpoint and a corner. In each Queen, 14400 × chamber volume = the Queen's volume (checked). No mirror meets the open chamber C.

**Mirrors + cross walls.** 25 of the 300 cross walls pass through the open chamber C, and 44 more touch its boundary only. In the simplex section they make 124 lines and 86 points inside the chamber; 8 of those lines and 21 of those points are where more walls than usual meet.
- **Regions of C: 298** by all three methods (exact Zaslavsky; float splitting; float lattice 4,291,200 = 14400 × 298).
- **Chambers: 4,291,200 in each Queen.** The characteristic polynomial of the 360 walls is (t − 1)(t³ − 359t² + 45959t − 2099281). The cubic factor is irreducible over Q, so unlike the mirrors alone the arrangement is not free with integer exponents.
- **Congruence classes:** 298 per Queen. The 298 pieces in C are pairwise non-congruent (distance-multiset test), and W(H4) moves each onto its 14400 copies. Volumes range over a factor of 249 (600-cell) and 274 (120-cell). Each tetrahedral cell of the 600-cell is cut into 24 × 298 = 7152 pieces; each dodecahedral cell of the 120-cell into 120 × 298 = 35,760.
- **The 15 combinatorial types** (the same in both Queens). Chamber f = (corners, edges, 2-faces, cells); base = the piece of the cell it stands on:

| chamber f | base faces | pieces in C |
|---|---|---|
| (5, 10, 10, 5) | 4 triangles (a 4-simplex: an orthoscheme-like simplex) | 155 |
| (6, 13, 13, 6) | 4 triangles + 1 quadrilateral | 59 |
| (7, 15, 14, 6) | 2 triangles + 3 quadrilaterals (prism-like base) | 34 |
| (7, 16, 16, 7) | 4 triangles + 2 quadrilaterals | 16 |
| (8, 18, 17, 7) | 2 triangles + 4 quadrilaterals | 10 |
| (8, 18, 17, 7) | 3 triangles + 2 quadrilaterals + 1 pentagon | 6 |
| (6, 14, 15, 7) | 6 triangles (triangular bipyramid base) | 3 |
| (9, 20, 18, 7) | 6 quadrilaterals (hexahedral base) | 3 |
| (9, 20, 18, 7) | 2 triangles + 2 quadrilaterals + 2 pentagons | 3 |
| (7, 16, 16, 7) | 5 triangles + 1 pentagon | 2 |
| (8, 19, 19, 8) | 4 triangles + 3 quadrilaterals | 2 |
| (11, 25, 22, 8) | 5 quadrilaterals + 2 pentagons (pentagonal-prism-like base) | 2 |
| (9, 21, 20, 8) | 2 triangles + 5 quadrilaterals | 1 |
| (9, 21, 20, 8) | 3 triangles + 3 quadrilaterals + 1 pentagon | 1 |
| (10, 23, 21, 8) | 1 triangle + 5 quadrilaterals + 1 pentagon | 1 |

- **Identification.** With mirrors only, the one class is the H4 Coxeter chamber (Coxeter's characteristic orthoscheme). The cross walls subdivide it into 298 pieces. None is a known named solid. All are pyramids from the centre, so none is congruent to a cell of either Queen or to any shape of Study 1.

## The converse for A and B
A and B are the W(A4) orbits of 20 and 30 corners of the 600-cell (Study 1 part ab). The question: which walls does each use, and do those walls alone cut out A, B or relatives of them?

Exact chamber counts are from the lattice of each solid's own plates. The pieces inside the solid come from float splitting of each cell, one pyramid from the centre per piece, and they match the exact counts.

| | walls used | the group those walls generate | chambers of its own walls | pieces inside the solid | classes (120 congruent copies each) | pieces = a Queen's Coxeter chamber |
|---|---|---|---|---|---|---|
| **A** | 30 of the 60 mirrors | all of W(H4): the 30 mirrors are not closed under their own reflections; their closure is all 60 mirrors | **3360** (χ = 1, −30, 355, −1650, 1324) | 3360 | 28 | **120**: the 5 tetrahedral cells (cells of the 600-cell) are cut by their own 6 symmetry planes into 24 orthoschemes each, and each pyramid over one is exactly the 600-cell's H4 Coxeter chamber |
| **B** | 40 mirrors + 40 cross walls | the 40 mirrors close up to all 60; the 40 cross walls, reflected in each other, leave the Queens' walls (more than 400 walls, so not a finite reflection system inside the 360) | **62,880** (χ = 1, −80, 2478, −31360, 28961); the mirror part alone 6240, the cross part alone 13,580 | 62,880 | 524 | none |

Walls through the interior of each cell: in A, 6 through each tetrahedron and 22 through each golden truncated tetrahedron. In B, 42, 46 and 62 through the three cell kinds. So:
- **A's walls cut out A exactly as a union of chambers, but not A itself or its cells.** The pieces are of 28 kinds. One kind is the Queens' own Coxeter chamber (in the 600-cell cells that A shares with the 600-cell). The other 27 kinds, from the golden truncated tetrahedra, are new pyramids with 5 to 9 corners: 14 simplex classes, 8 of type (6,13,13,6), 4 of (7,15,14,6), and one each of (8,18,17,7) and (9,20,18,7).
- **B's walls cut B much finer: 524 kinds of chamber, none a Queen chamber.** Their combinatorial types follow the Queens' list: 196 simplex classes, 146 of (7,15,14,6), 76 of (6,13,13,6), and so on.
- **No chamber of either system is congruent to A, B or one of their cells.** The relatives that appear are the H4 Coxeter chamber (in A) and pyramids of the same combinatorial types as the Queens' 298 pieces.

Converse in one line: A uses a half-system of the mirrors that still generates the whole Queen group, and so carries 120 true Queen chambers; B mixes mirrors with cross walls that do not form a reflection system, and so carries no Queen chamber.

## Files
- `scripts/chambers.py`: parts control, cross, ab (imports `qv_lib.py` and `study1.py` of the vicinity study). Job `qchambers` on the compute machine (24 checks, FINAL ok, about 4 min). `data/chambers.log` and `data/chambers-control-cross-ab.json` are its output. The JSON was first written into the vicinity study's data folder, because the imported `HERE` shadowed this script's own; it was moved here and the output path fixed after the run. A first run was stopped by hand at 26 min: a wall-closure loop iterated over a growing list. It was fixed (one snapshot per pass, cap checked inside) before the run reported here.

## LEADS
1. The 298 pieces have 15 combinatorial types; the simplex type (155 pieces) dominates. Which pieces carry a face of the golden-station truncated 600-cell (Study 1), whose Vacuus is the whole wall system?
2. The cubic factor t³ − 359t² + 45959t − 2099281: compute its roots, and find the subsystems of cross walls that are free (for example the 60 + 60 walls of one inscribed 600-cell in the 120-cell).
3. Coarser structures: mirrors + the 60 cross walls of one inscribed 600-cell, or + the 12 cross walls of one inscribed 24-cell. Do they cut out recognisable shapes (Study 1 found those shapes hidden in cross walls only)?

DICTO · dictospheres.com
