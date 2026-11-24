# Exact renders of three Vacuus builds (24 Nov 2026)

Purpose: DICTO asked for 3D renders of his physical Vacuus builds to use in paper #87 (DICTO Vacuus Solids) IN PLACE of his photos,
"similar but better". The photos were used as private reference only and are not in this folder. Nothing is fitted to a photo:
every piece is built from the exact coordinates of the solid the build realises.

Result (renders/, frames on a dark ground; preview-sheet.jpg shows all):
1. Cardboard octahedron Vacuus (octahedron-cardboard*.jpg): the three squares through one centre (corners at distance 1 on the
   axes), as DICTO's four pieces A (z = 0, one slot), B (x = 0, three slots), C (y = 0) cut in two along its x-diagonal, each half with
   one slot; board and slots to the scale of the cut sheet (edge 80 mm, board 3.5 mm, slot 3.8 mm; study 2026-11-02-vacuus-origami,
   cardboard_octahedron.py). Pull-apart: each piece moved back along the line it slides in on.
2. B1NR cube (cube-b1nr*.jpg, cube-vacuus-fins.jpg): the cube [-1,1]^3 as six square pyramids with apex at the centre, in clear see-through
   faces with crisp edges; pull-apart along the face normals; the twelve fins O-A-B alone (the cube's Vacuus).
3. White ring cube (cube-white-*.jpg), READING TO BE CONFIRMED BY DICTO: the cube's six diagonal planes (each through two opposite
   edges and the centre); in each, the two fins of the Vacuus solid white and the two triangles centre-to-face-diagonal that complete
   the rectangle see-through. No pull-apart (the six planes interpenetrate); one plane is shown alone instead.

Checks (scripts/check.py, sympy, exact; all ok): octahedron 12 fins, right-angled, four in each coordinate plane; cube 12 fins with apex
cos = 1/3, two in each of the six diagonal planes; six face pyramids fill the cube (6 x 4/3 = 8); every crossing of two cardboard
pieces is cleared by a slot on one of them (A x B along y, B x C along z), slot wider than board, C rests on A.

Method: scripts/builds.py writes the scenes for the house renderer (render3d.py of study 2026-11-21-scutoid-stand-in, three.js r128,
orthographic); frames by its shots.mjs (Playwright); scripts/compose.py makes the sheet. Polygons with slots triangulated by ear clipping.
Sources checked: paper #87 text (Sections 1 and 6, Figures 1, 7, 8), its cut-sheet script, DICTO's photos (private, reference only).

LEADS: DICTO to confirm the white cube reading (full diagonal planes vs the twelve fins only; are the outer faces ringed?; is it a B1NR
build?); DICTO to confirm the B1NR cube as six clear pyramids; then the renders replace Figure 1 of #87 at its next version.
