# DICTO's Hemi RD build (Polyhedraverse, 11 Nov 2026)
Source: DICTO's Rhombiverse world export (rhombiverse-world(5).json, store worldpoly): "RD-Hemi (bare) + 13x face-attached RD-Hemi (bare)",
14 nodes with exact transforms, 13 connections (data/dicto-build-worldpoly.json). DICTO's ideas: the hexagons are irregular with the long
sides opposite (11 Nov); "that can be filled with pyramids derived from a cube"; the open squares "echoed the all-cell permutohedron structure".
## Results (scripts/analyse_build.py; float geometry, volumes exact to 1e-6)
- 14 Hemi RDs (each half an RD, volume 1 with the RD of volume 2), no overlaps (sampled), 35 glued face pairs; outer surface 28 triangles,
  2 four-gons, 12 hexagons.
- Convex hull: 6 squares (side 1, normals along the cube axes) + 12 hexagons (normals along the RD's face directions, sides 1, sqrt3/2,
  sqrt3/2, 1, sqrt3/2, sqrt3/2: the long sides opposite, as DICTO saw) = the CHAMFERED CUBE (the RD with its six 4-valent corners cut off).
- Hull volume 15 = 14 pieces + 1. The missing volume is exactly six CUBE PYRAMIDS (base side 1, apex 1/2 inside, volume 1/6 each): under
  each of the six hull squares the whole pyramid is empty (sampled: 1.000 each, sum 6.000). DICTO's claim CONFIRMED: filling the six open
  squares with cube pyramids closes the build into the convex chamfered cube.
- The echo with the 4D permutohedron (DICTO): the six open squares sit on the cube axes exactly where the 3D permutohedron has its six
  squares, and in the 4D permutohedron those six squares are where a second kind of cell (hexagonal prisms) attaches, as here a second
  kind of piece (cube pyramids) does. The hexagons differ: 12 stretched ones on the RD directions here, 8 regular ones on the body
  diagonals in the permutohedron. So the echo is in the squares, not in the hexagons.
NEXT (open): exact version (rational coordinates); does the chamfered cube fill space with the cube pyramids or with RD halves (#58 says
an earlier Polyhedraverse build of RD halves, a slightly irregular truncated octahedron, did).
## It fills space with cube pyramids (DICTO 11 Nov: "does the chamfered cube fill space with the pyramids") - YES (scripts/fill_test.py, FINAL ok)
The closed build is the zonohedron with generators the three unit axis vectors and the four half body diagonals (volume 1 + 6 + 6 + 2 = 15).
Chamfered cubes at the lattice 2*FCC (contact on hexagons by (2,2,0); cell volume 16) plus a unit cube at each lattice point + (2,0,0)
(the cube of six cube pyramids lying between six squares, one from each of six chamfered cubes) fill space: 20,000 random points each
covered exactly once; volume 16 = 15 + 1 per lattice point. In DICTO's pieces: per lattice point, his 14 Hemi RDs + 12 cube pyramids
(6 in the dents under the squares, 6 forming the cube between squares). Numerical check with exact volumes; exact proof (rational
coordinates, face-to-face) is the next step. The chamfered cube alone does not tile by translations (its belt round an axis has 8 faces;
Venkov's belt condition needs 4 or 6).
## EXACT proof of the filling (scripts/exact_fill.py, rational arithmetic, FINAL ok)
Z = zonohedron with generators e1, e2, e3 and the four half body diagonals (32 vertices, volume exactly 15) = DICTO's closed build
(the hull of his 14 Hemi RDs, matched in analyse_build.py: 6 squares side 1, 12 hexagons sides 1 and sqrt3/2, volume 15).
Z + L and unit cubes Q + (2,0,0) + L (L = even points with a+b+c = 0 mod 4, det 16) tile space: 487 pairs of pieces within reach, each
separated by an exact separating axis (facet normals and edge cross products); densities 15 + 1 = 16 = det L; a packing of density 1 by
convex bodies is a tiling. So DICTO's 14 Hemi RDs + 12 cube pyramids per lattice point fill space. THEOREM (DICTO's construction and
idea; exact).
