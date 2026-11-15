# Series front cover for The Platonic Solids, circle design (15 Nov 2026) - DICTO · dictospheres.com

Cover by DICTO: "just the five solids plain in a circle in DICTO order, Dodecahedron at the top"; then the five at equal volume, as
translucent deep crystal. Not yet in the book: the current white cover (book-platonic/front.html, cover/cover-skins.png) stays until
DICTO chooses.

- Image: the five Platonic solids, plain (no settings), as deep crystal in the element colours of the DICTO square: Dodecahedron
  violet (138, 92, 196), Icosahedron blue (58, 112, 205), Cube green (72, 142, 72), Tetrahedron red (205, 62, 40), Octahedron yellow
  (232, 200, 82). Evenly on one circle (radius 720 px on the 2400 px wide cover), 72 degrees apart: Dodecahedron at the top, then
  clockwise Icosahedron, Cube, Tetrahedron, Octahedron.
- Equal volume: volume at edge 1 (exact) D (15 + 7√5)/4, I 5(3 + √5)/12, C 1, T 1/(6√2), O √2/3. Each edge = (V / volume at edge 1)^(1/3)
  for one common V, so the edges stand, with the cube's edge 1, at D 0.507222, I 0.771025, C 1, T 2.039649, O 1.284898
  (V = 36 cover units³, 1 unit = 100 px; circumradii 235, 242, 286, 412 and 300 px).
- Views: Dodecahedron with a pentagon face toward the viewer, tipped to show the ring of faces round it; Icosahedron with a corner
  toward the viewer (the five-triangle cap), one point up; Cube in a three-quarter view (front, side and top, not square-on);
  Tetrahedron standing on a face, apex up, two side faces seen; Octahedron corner up (the double pyramid).
- Rendering: path-traced in Blender Cycles (CPU, 1024 samples, denoised, 2400 x 2200 picture block, orthographic camera). Crystal
  and studio as the ring design (studies/2026-11-15-platonic-cover): refractive glass (IOR 1.45), tinted, with a volume absorption
  in the element colour at full strength (its own hue passes, the others are absorbed), so the colour deepens where the solid is
  thicker; small bevels give bright facet edges; light reaching a solid through its body comes from a banded light box, so the back
  facets and edges show inside it; soft boxes give the glints. The camera sees only the cover ground (20, 15, 11).
- Lettering exactly as the previous design: series line white, title in the series gold (217, 165, 33), subtitle in the
  icosahedron's blue (58, 112, 205), and the ◆ DICTO ◆ mark (front and back) in the dodecahedron's violet (138, 92, 196).
- Checks (X PASS lines): corner, face and edge counts; edge-1 coordinates exact (shortest corner distance 1 in doubles, attained by
  every edge); every mesh edge at its scaled length; every mesh volume = the common volume; Dodecahedron at the top, clockwise order,
  even 72-degree spacing; neighbours clear of each other; all inside the picture block.

Files: scripts/crystal_circle.py (Blender scene and render), scripts/compose.py (cover ground + lettering + back mark),
scripts/compare.py (the five-cover comparison sheet: Space-Fillers, Golden Cycle, Star Cores, Permutohedron Paradigm, Platonic
Solids), scripts/run.sh (render + compose), scripts/ledtext.py (series LED lettering; DSEG14 by keshikan, SIL Open Font Licence,
DSEG-LICENSE.txt; the kanji of the series line from Noto Sans CJK, SIL Open Font Licence). Outputs: platonic-cover-front-series.png
(2400 x 3394), platonic-dicto-mark-back.png. Run through the job gate (pilots at 800 x 733; final FINAL ok). The first, opaque
equal-circumradius drawing is in this folder's git history.
