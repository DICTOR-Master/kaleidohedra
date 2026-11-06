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
