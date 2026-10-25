# David and Goliath: the A15 stop at λ = 3/4 (2026-10-25)

Names by DICTO (2026-10-25). From the #53 relay census (A15 Cr₃Si, cubic cell edge 2, λ = w_Si − w_Cr): at λ = 3/4 the power cells are

- **Goliath** (the Si cell): a convex icosahedron, 20 triangles, 12 corners of degree 5, 30 edges with squared lengths 1 and 3/2, volume 7/2. Its corners are exactly the points (0, ±1/2, ±1) and their cyclic permutations: the vertex set of Jessen's orthogonal icosahedron, so Goliath is the convex hull of Jessen's icosahedron.
- **David** (the Cr cell): a tetrahedron (tetragonal disphenoid), squared edge lengths 1 and 3/2, volume 1/6, centred on its Cr site.
- Per cubic cell: 2 Goliaths + 6 Davids, 2·7/2 + 6·1/6 = 8 = the cell: they fill space face to face (power diagram).

Exact (Fraction arithmetic): `exact_a15.py` → `exact_a15.txt` (all checks True). `cells.py`: float cross-check, also the rock-salt stop at 4 − 2√3 (equilateral chamfered cubes + cubes of the same edge).
Prior art: one web search (2026-10-25) found no description of A15 tiled by these icosahedra and tetrahedra; Jessen's icosahedron and its convex hull are classical; a full search is still needed before any claim.
