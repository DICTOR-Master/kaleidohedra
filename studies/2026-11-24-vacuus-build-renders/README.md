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
3. White ring cube (cube-white-*.jpg), as DICTO stated on 24 Nov: the cube's SIX DIAGONAL PLANES, each a WHOLE white rectangle through
   two opposite edges and the centre (sides 2 and 2 sqrt 2, ratio sqrt 2). The provisional bow-tie / see-through reading is removed.
   The six cut through each other, so three views: cube-white-rectangles.jpg (assembled); cube-white-one-rectangle.jpg (the rectangle
   x = -z alone, nearly face-on, with the cube's twelve edges as thin lines to show where it sits); cube-white-three-pulled.jpg (the three
   rectangles through the body diagonal (-1,-1,-1)-(1,1,1), i.e. the planes x = y, x = z, y = z, each moved 2.4 along its own unit
   normal; the three normals sum to zero, so they spread at 120 degrees about the diagonal). Exact: the three still meet at a pull of
   sqrt(2)/2 and are pairwise disjoint beyond it, so at 2.4 they stand clear. The view of the pulled three was chosen by a search over
   directions for the largest smallest projected area with no projected overlap.

Checks (scripts/check.py, sympy, exact; all ok, data/check.log): octahedron 12 fins, right-angled, four in each coordinate plane; cube 12 fins with apex
cos = 1/3, two in each of the six diagonal planes; six face pyramids fill the cube (6 x 4/3 = 8); every crossing of two cardboard
pieces is cleared by a slot on one of them (A x B along y, B x C along z), slot wider than board, C rests on A; white cube: each diagonal
rectangle holds exactly two cube edges (opposite, parallel) and O, sides 2 and 2 sqrt 2; exactly three contain one body diagonal; the
pulled three are pairwise disjoint at pull 12/5 and still meet at sqrt(2)/2.

Method: scripts/builds.py writes the scenes for the house renderer (render3d.py of study 2026-11-21-scutoid-stand-in, three.js r128,
orthographic); frames by its shots.mjs (Playwright); scripts/compose.py makes the sheet. Polygons with slots triangulated by ear clipping.
Sources checked: paper #87 text (Sections 1 and 6, Figures 1, 7, 8), its cut-sheet script, DICTO's photos (private, reference only).

## Pacioli's three golden rectangles (DICTO, 24 Nov: another connected origin for the Vacuus and the Resonus)

Geometry (scripts/pacioli.py, sympy in Q(sqrt 5), exact; all ok, data/pacioli.log). Icosahedron = cyclic permutations of
(0, +-1, +-phi), edge 2; the three rectangles are its corners in the planes x = 0, y = 0, z = 0.
(a) YES. Each golden rectangle (sides 2 and 2 phi) lies in a Vacuus plate plane of the icosahedron: its two short sides are icosahedron
    edges, and they are the only two edges in that plane. So each rectangle = two Vacuus fins (O with a short side) + two triangles O
    to a long side (2 phi, a vertex-to-vertex distance, not an edge). It is the icosahedron's exact counterpart of DICTO's white ring cube
    rectangle (two cube fins + two triangles to face diagonals). The icosahedron has 15 such planes (one per opposite edge pair, its 15
    mirror planes), all golden, falling into 5 mutually perpendicular triples; Pacioli's three are one triple.
(b) NO. The three planes are not Resonus planes of the icosahedron (no face parallel) nor of the dodecahedron. Their normals are the
    two-fold axes (through edge midpoints); Resonus normals are three-fold (icosahedron) or five-fold (dodecahedron) axes.
(c) Dodecahedron (the dual: (+-1,+-1,+-1) and cyclic (0, +-1/phi, +-phi)): each Pacioli plane is also a dodecahedron Vacuus plate plane;
    it holds exactly two opposite dodecahedron edges, parallel to the golden rectangle's short sides, and the 4 dodecahedron corners in
    it make a rectangle of sides 2/phi and 2 phi, ratio phi^2 (not golden). Not Resonus.
    Icosidodecahedron (the 30 edge midpoints of the icosahedron, edge 1): each plane holds no icosidodecahedron edge (so not a Vacuus
    plate plane) and is parallel to none of its 20 + 12 faces (not Resonus); it holds 4 icosidodecahedron corners forming a square of
    side phi sqrt 2, two of which are the midpoints of the golden rectangle's short sides.
    Verdict: the rectangles connect to the Vacuus (of the icosahedron and dodecahedron), not to the Resonus.

History (d), from opened free sources.
- The 1509 Venice edition (Paganino Paganini) labels Leonardo's open-frame plates "Vacuum" (neuter), each with its number and a Greek
  transliteration in the margin. Read on the page images (Wikimedia Commons scans of a 1509 copy, files "De divina proportione -
  Illustration 13, 19, 25, 35, 41"): plate II "Tetraedron Planum Vacuum" (margin "Tetraedron Epipedon Cenon"); VIII
  "Hexaedron.Planum.uacuum."; XVI "Octaedron Planum Vacuum"; XXII "Icosaedron Planum Vacuum"; XXVIII "Dodecaedron Planum Vacuum".
  The book's own table "Nomina et numerus corporum" lists, per solid, "Planum vacuum", "Abscisum vacuum", "Eleuatum vacuum",
  "Abscisum eleuatum vacuum" (1509 scan, archive.org divinaproportion00paci; transcribed in Winterberg 1889, archive.org
  diviproporti00paci). The 1509 print uses "Exahedron siue Cubus" in the table and "Hexaedron" on the plate.
- The manuscript drawings use the masculine form: the plate reproduced on Commons as "Leonardo Ycocedron Abscisus.jpg" reads
  "YCOCEDRON · ABSCISVS VACVVS." (read on the image). Which manuscript (Geneva or Ambrosiana) it comes from is not stated reliably on
  that page (its description says 1509, which is wrong for a coloured hand drawing): UNCERTAIN; no Ambrosiana scan was opened.
- Paper #87 writes "solidus and vacuus": the manuscript form; the 1509 print has "Solidum"/"Vacuum". Noted only, not changed.
- The three golden rectangles: NOT FOUND in Pacioli's text. A search of the full Italian text (Winterberg's 1889 transcription, OCR) for
  rectangle/quadrilateral words, and a reading of the icosahedron construction (Compendium Cap. XXIX, Euclid XIII.16's method: pentagon,
  decagon, perpendiculars) found no description of three mutually perpendicular rectangles. The nearest passage is the 12th effect
  (Cap. XXI, "Del suo 12. quasi incomprehensibile effecto"): for a line a cut in mean and extreme ratio (major M, minor m),
  sqrt(a^2 + M^2) : sqrt(a^2 + m^2) = cube edge : icosahedron edge in one sphere (from Euclid XIV.9 via Campanus, as Pacioli says).
  Checked exact (pacioli.py). Our reading, not Pacioli's words: the two roots are the diagonals of a golden rectangle (M, a) and of a
  phi^2 rectangle (m, a), the very rectangles of (a) and (c). Pacioli does not draw or name them.
- Secondary attributions: Wikipedia "Divina proportione" says the book points out "golden rectangles can be inscribed by an icosahedron",
  citing Livio 2003, p. 132 (not opened; not free). Wikipedia "Golden rectangle" states the three-rectangle decomposition citing Burger and
  Starbird 2005, p. 382, with no mention of Pacioli. So "Pacioli's three rectangles" is, on these sources, a LATER ATTRIBUTION; the
  absence in the OCR text is strong but not proof (OCR errors, figures without text). Earliest true source of the three-rectangle
  figure: UNCERTAIN, not found.

Sources checked (24 Nov): archive.org divinaproportion00paci (1509, OCR text), diviproporti00paci and divinaproportio00pacigoog
(Winterberg 1889, Italian + German, OCR text), bub_gb_Z2JLAQAAIAAJ (1896 reissue, OCR text); Wikimedia Commons categories "De divina
proportione; polyhedra; skeletonic" and "...; Platonic solids" (plate images read: Illustrations 08, 13, 19, 22, 25, 35, 41; Leonardo
Ycocedron Abscisus); Wikipedia "Golden rectangle" and "Divina proportione" with their citations; Italian Wikisource (no transcription
found); web searches for the three-rectangle attribution (results: Wikipedia, Louvre Leonardo mini-site, Salamon KCL slides, Springer
AHES 2024 article s00407-024-00331-7; none opened gives a primary source). Not opened: Livio 2003, Burger-Starbird 2005, the Geneva and
Ambrosiana manuscripts.

LEADS: DICTO to look at the three white-cube views (row 3 of the preview sheet); DICTO to confirm the B1NR cube as six clear pyramids;
then the renders replace Figure 1 of #87 at its next version. Pacioli: the golden rectangle is the icosahedron's counterpart of the
white ring cube rectangle (both: two Vacuus fins + two centre triangles in a mirror plane through two opposite edges); a matching
render (icosahedron's 15 rectangles, or Pacioli's three) is possible if wanted; where it goes (#87 or elsewhere) is DICTO's choice.
#87's "solidus/vacuus" vs the 1509 print's "Solidum/Vacuum" could be footnoted at the next version, with the manuscript "VACVVS".
