# Exact renders of DICTO's four Vacuus builds (24 Nov 2026)

Purpose: DICTO asked for 3D renders of his physical Vacuus builds to use in paper #87 (DICTO Vacuus Solids) IN PLACE of his photos,
"similar but better". DICTO, 24 Nov: "the way I build all my PET bottle and B1NR sculptures is as Vacuus ... and hulls ... they are
skeletons and empty"; he confirmed SKELETAL renders. So builds 2-4 are open frameworks (struts and joints, or rings), with no
faces: the empty space shows. The cardboard octahedron (1) is the exception: DICTO 25 Nov, it is "three flat squares and can only
represent the octahedron", so it is drawn as three solid cards. The two ring-fin builds (3, 4) are drawn as he builds them: bottle rings inscribed in the Vacuus fins.
The photos were private reference only and are not in this folder. Nothing is fitted to a photo: every card corner is an exact corner and every
strut joins exact corners of the solid the build realises, and every ring is the exact incircle of its fin.

Result (renders/, frames on a dark ground; preview-sheet.jpg shows all nine). DICTO, 24 Nov: his Vacuus builds are exactly four.
1. Cardboard octahedron (octahedron-cardboard-cards*.jpg), corners at distance 1 on the axes: three solid flat square cards in the
   planes x = 0, y = 0, z = 0 (DICTO 25 Nov: "three flat squares and can only represent the octahedron"). Each card is the square with
   its corners on the two axes in its plane (for z = 0: (+-1, 0, 0) and (0, +-1, 0)), side sqrt 2, its 4 sides octahedron edges (builds.py
   asserts both); any two cards meet along a whole axis, drawn as a thin crease line. How the three cards are joined is not known (three
   whole cards at right angles cannot all be joined by simple half-slots), so no joint is drawn. Cardboard tan, solid faces, crisp dark
   outline. Pull-apart: each card moved 9/5 along its own normal (disjoint, as 9/5 > 1), the group recentred in the picture.
   Not the cube's Resonus cards: the cube [-1,1]^3 has its Resonus in the same three planes, but its cards are its middle squares, side 2,
   larger and turned 45 degrees.
2. B1NR cube (cube-b1nr-skeleton*.jpg), [-1,1]^3: the hull skeleton (12 edges) + the Vacuus skeleton (8 corner-to-centre struts): the
   empty cube that is six square pyramids meeting at the centre. Clear bottle-like tubes (see-through, bright core line, see-through
   joints). Pull-apart: the six pyramid frames (4 base edges + 4 struts each) moved 27/5 along the face normals (was 9/5, where two
   frames overlapped in the picture). Checked in the drawn view by projected bounding boxes (joint balls included): all six boxes
   pairwise disjoint, smallest gap 35 px of 1600, all inside the frame (data/builds.log).
3. B1NR cuboctahedron Vacuus, ring fins, no hull (cuboctahedron-ring-fins*.jpg; from DICTO's two photos of the build, 24 Nov):
   one white PET-bottle security ring in each of the 24 fins (fin = triangle O, a, b of an edge ab), inscribed in the fin and lying in
   its plane. The 24 edges lie in 4 regular hexagons through O, so the rings form 4 hexagonal plates of 6. Rings are flat bands (as the
   real rings), the outer face exactly the incircle; slightly see-through white. At each join a cut cable tie: a small flush clasp
   round the spoke, NO tails (DICTO 24 Nov: the build is unfinished, the tails are not part of the design, "cut them").
   Views: oblique; down a three-fold axis (1, 1, 1) (one plate face-on); the four plates pulled apart, each 2 along its own normal
   (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1), seen down (0, 0, 1), clasps removed; checked in the drawn view: the projected convex hulls
   of the four plates are pairwise disjoint, smallest gap 57 px of 1600, all in frame (data/builds.log).
4. B1NR dodecahedron Vacuus, ring fins, no hull (dodecahedron-ring-fins*.jpg): the same build on the dodecahedron (corners (+-1, +-1,
   +-1) and cyclic (0, +-1/phi, +-phi)): 30 rings in 30 fins, 15 plates of 2 (each plate holds two opposite edges). Views: oblique; down
   a five-fold axis (1, 0, phi). No pull-apart: a plate is only two rings on opposite sides of O, so 15 pulled plates show nothing new.
   The earlier rods-only renders of 3 and 4 (12 and 20 centre struts) are replaced and deleted (git history keeps them).

Reading of DICTO's photos (two private photos of the B1NR cuboctahedron, reference only, not in this folder; read 24 Nov):
- The pieces are white bottle-cap security rings (tamper bands, with their small inner tabs), flat bands about a fifth as wide as across,
  joined by clear cable ties whose uncut tails stick out (unfinished build). No hull, no rods: the rings alone carry the shape.
- The rings stand in many planes; groups of rings meet at a tie, the tie closing round where several rings touch side by side, which is
  what the incircle reading predicts (4 rings touching at each spoke midpoint). One view (IMG 9367) shows a triangle of rings in front
  with rings fanning out round it, as the render down a three-fold axis does.
- Counting: the rings overlap too much in two photos to count all 24 or to prove the four hexagonal planes; what is visible (ring size
  against the whole, joins of several rings at ties, no rings at the corners) fits the reading and nothing contradicts it.
  Verdict: CONSISTENT, not proved by the photos; the ring count 24 and the 4 x 6 plates come from the geometry.

Exact ring geometry (scripts/check.py, sympy, in Q(sqrt 3, sqrt 5); builds.py uses the same formulas in floats):
- Ring of the fin O, a, b: centre the incentre (|ab| O + |Ob| a + |Oa| b) / (|Oa| + |Ob| + |ab|), normal a x b, radius
  |a x b| / (|Oa| + |Ob| + |ab|) (twice the area over the perimeter).
- Cuboctahedron (corners the permutations of (+-1, +-1, 0); edge = spoke = sqrt 2): fins equilateral; centre (a + b)/3 at distance
  sqrt 6 / 3 from O; radius sqrt 6 / 6. Two rings in one plate that share a spoke touch at its midpoint (centres 2r apart); the 4 rings of
  the 4 fins on a spoke (2 plates x 2) all touch the spoke at its midpoint. So 12 tie points, 4 rings at each; 72 touching pairs
  (24 within plates + 48 across plates); no other pair meets.
- Dodecahedron (edge 2/phi, spoke sqrt 3): fin apex cos = sqrt 5 / 3, tan(apex/2) = 1/phi^2; each ring touches the two spokes at
  t = sqrt 3 - 1/phi from O and has radius r = t / phi^2 (= 0.4255); centre at sqrt 3 (a + b) / (2 sqrt 3 + 2/phi). The 3 fins at a
  corner v (in 3 different plates) touch the spoke O-v at the same point, so 20 tie points, 3 rings at each; 60 touching pairs, all
  across plates (the two rings of a plate are on opposite sides of O and do not meet); no other pair meets.

Withdrawn (DICTO 24 Nov): the white "Vacuus, as a solid cube" ring photo IS the B1NR cube ("just the same as fig 2": hull + centre
struts, six pyramid frames meeting at the centre). Our earlier reading of it as six diagonal rectangles was a misreading; that render
section, its frames and its code are deleted (they stay in git history).

Superseded (25 Nov): the skeletal octahedron (12 edges + 6 half-axes as three square frames, octahedron-cardboard-skeleton*.jpg) is
replaced by the three solid cards and deleted; it stays in git history.
Superseded: the filled-plane renders of this study (slotted cardboard boards, glass-faced pyramids, the twelve fins, whole white
rectangles; commits up to 6f890699) are replaced by the skeletal set and deleted, as nothing else referenced them; they stay in git history.

Checks (scripts/check.py, sympy, exact; all ok, data/check.log): octahedron 12 fins, right-angled, four in each coordinate plane; cube 12
fins with apex cos = 1/3, two in each of the six diagonal planes; six face pyramids fill the cube (6 x 4/3 = 8); skeleton strut sets:
each octahedron square frame 4 edges + 4 half-axes, each half-axis in 2 squares; B1NR 12 + 8 struts, each pyramid 4 + 4, each centre
strut in 3 pyramids; the pulled octahedron squares and B1NR pyramids disjoint; cuboctahedron 12 corners, 24 edges sqrt 2, centre struts
sqrt 2; dodecahedron (in Q(sqrt 5)) 20 corners, 30 edges 2/phi, degree 3, centre struts sqrt 3; (1, 0, phi) passes through a face centre.
Ring fins (Q(sqrt 3, sqrt 5)): 24 and 30 rings, one per fin; each in its fin's plane and tangent to the three sides at inner points; one
radius each (sqrt 6 / 6; (sqrt 3 - 1/phi)/phi^2); plates 4 x 6 and 15 x 2; touching pairs 72 (24 coplanar + 48 across) and 60 (0 + 60),
no pair crossing or overlapping; touching points 12 (4 rings each) and 20 (3 each), one on every spoke. Zero tests exact (simplify);
nonzero values certified by 30-digit error-controlled evaluation.
builds.py asserts that no scene of builds 2-4 contains a face (the octahedron: 3 cards, 6 triangles), the B1NR box separation, the cuboctahedron plate hull separation, and the ring
tangencies in floats (data/builds.log).

Method: scripts/builds.py writes the scenes for the house renderer (render3d.py of study 2026-11-21-scutoid-stand-in, three.js r128,
orthographic), with one small extension made in builds.py (the shared renderer file is unchanged): a tube may carry an opacity and an
inner core tube, and a ball an opacity, for the clear bottle tubes. Frames by its shots.mjs (Playwright); scripts/compose.py makes the sheet.
Sources checked: paper #87 text (Sections 1 and 6, Figures 1, 7, 8), its cut-sheet script, DICTO's photos (private, reference only),
including the two photos of the B1NR cuboctahedron ring build (24 Nov). Rings and clasps are a second small extension in builds.py
(flat bands from two open cylinders and two rims; clasps a small torus with a flush head).

## Pacioli's three golden rectangles (DICTO, 24 Nov: another connected origin for the Vacuus and the Resonus)

Geometry (scripts/pacioli.py, sympy in Q(sqrt 5), exact; all ok, data/pacioli.log). Icosahedron = cyclic permutations of
(0, +-1, +-phi), edge 2; the three rectangles are its corners in the planes x = 0, y = 0, z = 0.
(a) YES. Each golden rectangle (sides 2 and 2 phi) lies in a Vacuus plate plane of the icosahedron: its two short sides are icosahedron
    edges, and they are the only two edges in that plane. So each rectangle = two Vacuus fins (O with a short side) + two triangles O
    to a long side (2 phi, a vertex-to-vertex distance, not an edge). The icosahedron has 15 such planes (one per opposite edge pair, its 15
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

LEADS: DICTO to look at the preview sheet (nine views, four builds; 3 and 4 now ring fins, ties cut); then the renders replace Figure 1 of #87 at its next
version. Pacioli: a render of the icosahedron's golden rectangles (its 15, or Pacioli's three) is possible if wanted; where it goes (#87 or elsewhere) is DICTO's choice.
#87's "solidus/vacuus" vs the 1509 print's "Solidum/Vacuum" could be footnoted at the next version, with the manuscript "VACVVS".
