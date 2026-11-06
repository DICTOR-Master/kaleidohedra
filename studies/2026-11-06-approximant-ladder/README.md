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
