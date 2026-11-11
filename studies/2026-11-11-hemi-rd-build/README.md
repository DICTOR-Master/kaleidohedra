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
