# Exact skeletal renders of DICTO's four Vacuus builds (24 Nov 2026)

Purpose: DICTO asked for 3D renders of his physical Vacuus builds to use in paper #87 (DICTO Vacuus Solids) IN PLACE of his photos,
"similar but better". DICTO, 24 Nov: "the way I build all my PET bottle and B1NR sculptures is as Vacuus ... and hulls ... they are
skeletons and empty"; he confirmed SKELETAL renders. So every build is an open framework of struts (tubes) and joints (balls), with
no faces: the empty space shows. The photos were private reference only and are not in this folder. Nothing is fitted to a photo:
every strut joins exact corners of the solid the build realises.

Result (renders/, frames on a dark ground; preview-sheet.jpg shows all eight). DICTO, 24 Nov: his Vacuus builds are exactly four.
1. Cardboard octahedron (octahedron-cardboard-skeleton*.jpg), corners at distance 1 on the axes: the 12 edges + the 6 corner-to-centre
   struts, so the three squares x = 0, y = 0, z = 0 stand as frames (each: 4 edges + its two diagonals = 4 half-axes; each half-axis
   is shared by two squares). Cardboard-tan struts. Pull-apart: each square frame moved 9/5 along its own normal (disjoint, as 9/5 > 1).
2. B1NR cube (cube-b1nr-skeleton*.jpg), [-1,1]^3: the hull skeleton (12 edges) + the Vacuus skeleton (8 corner-to-centre struts): the
   empty cube that is six square pyramids meeting at the centre. Clear bottle-like tubes (see-through, bright core line, see-through
   joints). Pull-apart: the six pyramid frames (4 base edges + 4 struts each) moved 27/5 along the face normals (was 9/5, where two
   frames overlapped in the picture). Checked in the drawn view by projected bounding boxes (joint balls included): all six boxes
   pairwise disjoint, smallest gap 35 px of 1600, all inside the frame (data/builds.log).
3. B1NR cuboctahedron Vacuus, no hull (cuboctahedron-b1nr-struts*.jpg; DICTO 24 Nov, "both B1NR no hulls"): one clear rod from the
   centre to each of the 12 corners (permutations of (+-1, +-1, 0)), no edges. This is #87's STRUTS form ("one rod from O to every
   corner, with the solid's edges ... as an option") with the option not taken, so the reading is the definition itself. Views:
   oblique; down a three-fold axis (1, 1, 1).
4. B1NR dodecahedron Vacuus, no hull (dodecahedron-b1nr-struts*.jpg): one clear rod from the centre to each of the 20 corners
   ((+-1, +-1, +-1) and cyclic (0, +-1/phi, +-phi)), no edges. Views: oblique; down a five-fold axis (1, 0, phi).
   No pull-apart for 3 and 4: without edges a centre pyramid is a bare tuft of rods, so pulling them apart shows nothing new.

Withdrawn (DICTO 24 Nov): the white "Vacuus, as a solid cube" ring photo IS the B1NR cube ("just the same as fig 2": hull + centre
struts, six pyramid frames meeting at the centre). Our earlier reading of it as six diagonal rectangles was a misreading; that render
section, its frames and its code are deleted (they stay in git history).

Superseded: the filled-plane renders of this study (slotted cardboard boards, glass-faced pyramids, the twelve fins, whole white
rectangles; commits up to 6f890699) are replaced by the skeletal set and deleted, as nothing else referenced them; they stay in git history.

Checks (scripts/check.py, sympy, exact; all ok, data/check.log): octahedron 12 fins, right-angled, four in each coordinate plane; cube 12
fins with apex cos = 1/3, two in each of the six diagonal planes; six face pyramids fill the cube (6 x 4/3 = 8); skeleton strut sets:
each octahedron square frame 4 edges + 4 half-axes, each half-axis in 2 squares; B1NR 12 + 8 struts, each pyramid 4 + 4, each centre
strut in 3 pyramids; the pulled octahedron squares and B1NR pyramids disjoint; cuboctahedron 12 corners, 24 edges sqrt 2, centre struts
sqrt 2; dodecahedron (in Q(sqrt 5)) 20 corners, 30 edges 2/phi, degree 3, centre struts sqrt 3; (1, 0, phi) passes through a face centre.
builds.py asserts that no scene contains a face and the B1NR box separation (data/builds.log).

Method: scripts/builds.py writes the scenes for the house renderer (render3d.py of study 2026-11-21-scutoid-stand-in, three.js r128,
orthographic), with one small extension made in builds.py (the shared renderer file is unchanged): a tube may carry an opacity and an
inner core tube, and a ball an opacity, for the clear bottle tubes. Frames by its shots.mjs (Playwright); scripts/compose.py makes the sheet.
Sources checked: paper #87 text (Sections 1 and 6, Figures 1, 7, 8), its cut-sheet script, DICTO's photos (private, reference only).

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

LEADS: DICTO to look at the skeletal preview sheet (eight views, four builds); then the renders replace Figure 1 of #87 at its next
version. Pacioli: a render of the icosahedron's golden rectangles (its 15, or Pacioli's three) is possible if wanted; where it goes (#87 or elsewhere) is DICTO's choice.
#87's "solidus/vacuus" vs the 1509 print's "Solidum/Vacuum" could be footnoted at the next version, with the manuscript "VACVVS".
