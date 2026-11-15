# Series front cover for The Platonic Solids (15 Nov 2026) - DICTO · dictospheres.com

Cover by DICTO: "a ring with the Japanese character in the middle and crystal deep translucent colours". Not yet in the book: the
current white cover (book-platonic/front.html, cover/cover-skins.png) stays until DICTO chooses.

- Image: one gold finger ring, the series' ring (The Five Orders of Space follows Musashi's five rings; this book's ring is Wind),
  in a three-quarter view. The character 風 (Wind) stands in the middle of the hoop, in the ring's plane, in the same gold.
  The five Platonic solids sit on the band as crystal stones in D·I·C·T·O order, left to right, evenly 40 degrees apart over the
  upper arc, each face-down in a small gold collet with one prong per corner of its bottom face. All five at edge 1 (the same
  edge), in the element colours of the DICTO square: D violet (138, 92, 196), I blue (58, 112, 205), C green (72, 142, 72),
  T red (205, 62, 40), O yellow (232, 200, 82).
- Rendering: path-traced in Blender Cycles (CPU, 1024 samples, denoised, 2400 x 2200 picture block). Gold = metallic BSDF
  reflecting soft-box lights and a studio surround (highlights, reflection gradient, darker gold in shadow). Crystal = refractive
  glass (IOR 1.45), tinted, with a volume absorption in the element colour, so the colour deepens where the stone is thicker;
  light reaching a stone through its body comes from a banded light box, so the back facets and edges show inside it; small
  bevels give bright facet edges. The camera sees only the cover ground (20, 15, 11).
- Lettering as the series: series line white, title in the series gold (217, 165, 33), subtitle in the champagne of the ring's
  lit gold (236, 206, 140), and the ◆ DICTO ◆ mark (front and back) in the dodecahedron's violet (138, 92, 196), DICTO's choice.
- Checks before rendering (X PASS lines): corner, face and edge counts of the five solids; shortest corner distance = 1 exactly
  (doubles, to 1e-12) and attained by every edge; every mesh edge = 1 (single precision, 1e-6); neighbouring stones clear of each
  other; 風 inside the hoop.

Files: scripts/ring_scene.py (Blender scene and render), scripts/compose.py (cover ground + lettering + back mark),
scripts/compare.py (refreshes the fifth column of the five-cover comparison sheet), scripts/run.sh (render + compose),
scripts/ledtext.py (series LED lettering; DSEG14 by keshikan, SIL Open Font Licence, DSEG-LICENSE.txt; the kanji of the series line
from Noto Sans CJK). 風 in the ring from Noto Serif CJK Bold (SIL Open Font Licence). Outputs: platonic-cover-front-series.png
(2400 x 3394), platonic-dicto-mark-back.png. Run through the job gate (pilots at 800 x 733; final FINAL ok). The first design
(five stones in their gold settings of Chapter 10, Table 10.2) is in this folder's git history.
