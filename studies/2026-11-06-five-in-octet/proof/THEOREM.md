# Theorem (Five in the octet) - draft statement, exact check (DICTO 11-06 "start on theorem")

In the octet (tetrahedral-octahedral honeycomb) of edge 1:
1. Every octahedron O holds Kepler's nest O > I > D > C > T of regular solids: I in Pacioli's position (corners on O's edges in the golden
   ratio), edge sqrt2/phi^2; D on I's face centres (edge^2 = 1/3 - sqrt5/9); C on eight corners of D - and C is exactly O's dual cube
   (corners at O's face centres, (+-1,+-1,+-1)/(3 sqrt2)), edge sqrt2/3, so D touches O at those 8 points; T on four corners of C, edge 2/3.
2. Every tetrahedron of the octet holds the octahedron of its edge midpoints (edge 1/2) and so the same nest at half size; between them
   sits the Archimedean truncated tetrahedron (corners cut at 1/3, edge 1/3).
3. Hence the octet carries all five Platonic solids (and the truncated tetrahedron) in every cell, and the arrangement is periodic in three
   directions. The gap C - T is four copies of O's own centre pyramid scaled by 2/3.
Exact verification in Q(sqrt2, sqrt5): proof/exact_nest.py -> proof/exact_nest.out (all items True; sympy on compute-host).
Proof (outline): (1) Pacioli + duality; t = 1/(3 sqrt2) computed exactly equals O's face-centre coordinate; (2) midpoint octahedron and
truncation are classical; (3) the octet is periodic; scaling by 1/2 is the octet's self-similarity.
Prior art to check before claiming: each inscription is classical (Euclid XIII, Pacioli 1509, Kepler); the identity "the cube on the
dodecahedron dual to Pacioli's icosahedron is the octahedron's dual cube" and the octet lattice of nests - not yet found; library + web search to do.
