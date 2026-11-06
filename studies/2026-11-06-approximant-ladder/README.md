# The approximant ladder (DICTO 11-06: "how do we turn all of this into a universal lattice" -> "perfect lets climb the ladder")
From the periodic octet to the icosahedral (five-fold) order, rung by rung: periodic crystals of nested icosahedral clusters whose sizes
follow the Fibonacci ratios 1/1, 2/1, 3/2, ... (approximants), towards the icosahedral quasilattice; at the top E8 -> H4 -> 3D
(Elser and Sloane 1987). Connected: studies/2026-11-06-five-in-octet, 2026-11-06-nest-supercells.

## Rung 1: the 1/1 cubic approximant (scripts/rung1.py -> data-rung1.txt)
Regular icosahedra (edge 1, standard orientation: 2-fold axes on the cube axes) on a body-centred cubic lattice of side a = 2 phi^2 / 3
= 1.745356, each touching its 8 nearest neighbours across the face planes square-on to the cube diagonals. No overlaps (8 + 6 neighbours).
Icosahedra fill 0.820676 of space; gap 0.179324 = per cluster the truncated octahedron (bcc Voronoi cell, volume a^3/2) minus the
icosahedron, 0.476716. 8 of the icosahedron's 20 faces lie in the truncated octahedron's hexagons; across each square a gap of 0.063661.
- Contact: neighbours of the same orientation meet in a six-pointed star (their triangles turned 60 deg), not in whole faces. Whole-face
  contact would need each neighbour turned 180 deg about the shared diagonal; the four diagonals then demand turns that no two
  orientations can supply (two such turns compose to 141 deg). So rung 1 = touching clusters, star contacts, gap 17.9%.
- Every icosahedron carries the five-solid nest (as in nest-supercells/unity.py).
Next: fill the gap (truncated octahedron - icosahedron) with pieces or gravel; rung 2 (2/1): a larger cubic cell with clusters at the
Fibonacci-related positions.

## Seats for the nests, by harmonics (DICTO "then put nests in the clusters, harmonics?"; scripts/seats.py)
Bond-order harmonics of each point's neighbourhood (all points within 2.0): Q4 (cubic tone) and Q6 (icosahedral tone; perfect icosahedron
Q4 = 0, Q6 = 0.6633).
- 2/1: exactly ONE perfect icosahedral point per cell (Q4 0.0000, Q6 0.6633; its 12 neighbours form a regular icosahedron of edge 2);
  every other point scores far lower (best Q6 0.50). The seats form a simple cubic lattice of side 2 phi^3.
- 3/2 (577 points per cell, density converged): 6 seats per cell (Q4 < 0.05, Q6 > 0.55), nearest 4.5346 apart (= the 1/1 rung's
  nearest-neighbour distance).
- A nest at each seat: the icosahedron of the 12 neighbours (edge 2, radius 1.902) holding D > C > T and O; nests of neighbouring seats
  cannot meet (2 x 1.902 < 4.53). Golden rhombohedra (the golden skin) everywhere else.

## Rung 5/3 seats and nests (DICTO "keep climbing, put nests in the 5/3 seats"; memory-light generator, box R = 9 one slice at a time)
1220 points per (primitive) cell = the 754 + 466 rhombohedra (points and tiles are equal in number on every rung: 16, 136, ~576, 1220),
confirming the 5/3 count. 16 icosahedral seats per cell, nearest 4.5346 apart; all 16 carry a regular icosahedron of their 12
neighbours (radius 1.9021, edge 2), so every seat holds a nest (I > D > C > T, O).
Seats per cell: 1/1 1 (of 16 points), 2/1 1 (of 136), 3/2 6 (of 577), 5/3 16 (of 1220): share 0.0074 -> 0.0104 -> 0.0131, rising toward the
quasilattice's own share. Seat spacing 4.5346 on every rung from 3/2 on.

## The climb measured by harmonics: diffraction (DICTO "harmonics, other tools"; scripts/diffraction.py, same ball size on every rung)
Bond directions are exactly icosahedral on every rung; the rungs differ in the arrangement, which diffraction (3D waves) shows. Pattern
square-on to a five-fold axis; ten-fold score = correlation with itself turned 36 deg (1 = perfectly ten-fold); four-fold = turned 90 deg.
| rung | ten-fold | four-fold | top-50 spot share |
|---|---|---|---|
| 1/1 | 0.9158 | 0.9155 | 0.594 |
| 2/1 | 0.9736 | 0.8733 | 0.412 |
| 3/2 | 0.9937 | 0.8377 | 0.382 |
| 5/3 | 0.9969 | 0.8324 | 0.374 |
| 8/5 | 0.9974 | 0.8266 | 0.370 |
| 13/8 | 0.9976 | 0.8257 | 0.370 |
| quasilattice (golden, the top) | 0.9977 | 0.8254 | 0.369 |
Every rung moves toward the quasilattice in all three measures: the cubic tone fades, the ten-fold order grows. 8/5 reached by harmonics
without building its exact cell (side 2 phi^6 = 35.89). Figure diffraction-ladder.png (2/1, 3/2, 8/5, quasilattice).

## Corrections and proofs from the independent review (REPORT-fable.md, 6 Nov 2026; my own recheck where marked)
- BUG FIXED (rechecked): tiles.py built rhombohedron corners wrongly (Epar[ijk] @ b instead of b @ Epar[ijk]); with the fix the 2/1 seat
  IS a full rhombic triacontahedron (20 prolate round it; recheck: [12, 12, 14, 20] prolate round the four star points). The sentence
  "no full rhombic triacontahedra" above is WITHDRAWN. Seats = triacontahedron vertices (proved in the report).
- 1/1: 1 star point but 0 seats (the seat window has no interior there; recheck seats.py 1 1: see below). The "1/1: 1 seat" above is wrong.
- 3/2: 576 points per cell (577 was a boundary double count) = 356 + 220 tiles.
- PROVED (report): points per cell = tiles per cell on every rung (lattice parallelepiped + zonotope dissection); 8/5: 10336 = 6388 + 3948;
  13/8: 43784.
- PROVED (report): no two seats closer than sqrt3 phi^2 = 4.5346 (= the prolate rhombohedron's long body diagonal), attained from 3/2 on.
- Seat counts 1, 6, 16 are generic, not exact: expected N x (window share) = 1.38, 6.8, 15.8; they depend on the shift gamma. The seat share
  tends to tau^-9 = 0.01316, the KNOWN frequency of the triacontahedral vertex (Baake and Grimm 2012; Henley 1986); our 5/3 share 0.0131.
- KNOWN (report): the rational-perp cubic approximants (Elser and Henley 1985); cell sides 2 phi^n follow Ishimasa's rule (2019).
- PROVED (report, exact): the Dodeca-13 fits its own central dodecahedron at exactly 1/3.
- Kepler-nest: Pacioli's icosahedron known; "the nest's cube is the octahedron's dual cube" not found in the sources checked; it follows
  from eight icosahedron faces lying in the octahedron's face planes (shared insphere).
