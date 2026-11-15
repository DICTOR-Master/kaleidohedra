# Series front cover for The Platonic Solids, circle design (15 Nov 2026) - DICTO · dictospheres.com

Cover by DICTO: "just the five solids plain in a circle in DICTO order, Dodecahedron at the top". Not yet in the book: the current
white cover (book-platonic/front.html, cover/cover-skins.png) stays until DICTO chooses.

- Image: the five Platonic solids, plain and opaque, in the element colours of the DICTO square: Dodecahedron violet (138, 92, 196),
  Icosahedron blue (58, 112, 205), Cube green (72, 142, 72), Tetrahedron red (205, 62, 40), Octahedron yellow (232, 200, 82).
  Evenly on one circle, 72 degrees apart: Dodecahedron at the top, then clockwise Icosahedron, Cube, Tetrahedron, Octahedron.
  All five at the same circumradius (305 px on the 2400 px wide cover; circle radius 720 px), so the circle reads balanced.
- Views: Dodecahedron with a pentagon face toward the viewer, tipped to show the ring of faces around it; Icosahedron with a corner
  toward the viewer (the five-triangle cap), one point up; Cube in a three-quarter view (front, side and top, not square-on);
  Tetrahedron standing on a face, apex up, two side faces seen; Octahedron corner up (the double pyramid), four faces seen.
- Drawing: as the Golden Cycle cover's solids (studies/2026-10-29-golden-cover/scripts/golden_square.py): solid faces lit from the
  upper left, plus a gloss highlight per pixel from a point light, a soft sky term in the reflection and depth shading (nearer =
  brighter, no haze); edges in a dark shade of each solid's colour, supersampled 3x and reduced, so they are crisp and antialiased.
  Series ground (20, 15, 11).
- Lettering exactly as the previous design (studies/2026-11-15-platonic-cover): series line white, title in the series gold
  (217, 165, 33), subtitle in the icosahedron's blue (58, 112, 205), and the ◆ DICTO ◆ mark (front and back) in the dodecahedron's
  violet (138, 92, 196).
- Checks (X PASS lines): corner, face and edge counts of the five solids; every corner at circumradius 1 (1e-12); shortest corner
  distance attained by every edge (1e-12); Dodecahedron at the top and the clockwise order; even 72-degree spacing with the solids
  clear of each other; all inside the picture block; at least two faces seen on each solid.

Files: scripts/circle_scene.py (the picture), scripts/compose.py (cover ground + lettering + back mark), scripts/compare.py (the
five-cover comparison sheet: Space-Fillers, Golden Cycle, Star Cores, Permutohedron Paradigm, Platonic Solids), scripts/run.sh
(render + compose), scripts/ledtext.py (series LED lettering; DSEG14 by keshikan, SIL Open Font Licence, DSEG-LICENSE.txt; the kanji
of the series line from Noto Sans CJK, SIL Open Font Licence). Outputs: platonic-cover-front-series.png (2400 x 3394),
platonic-dicto-mark-back.png. Run through the job gate (pilot at SS=1, final at SS=3, FINAL ok).
