# 2026-11-02 DICTO Vacuus Solids (DICTO named the family on 2026-11-02)

Conclusion: the DICTO Vacuus (one fin O–A–B per edge AB; one strut O→corner per corner) is well defined for 99 of 100 solids. Lotus
Hexa fails because O lies outside 24 of its face planes. The Vacuus is isofin (all fins congruent) only for the Platonic and Archimedean
solids, the rhombic dodecahedron, the rhombic triacontahedron and Delilah (= octahedron). Among DICTO's new solids, Kagemusha, Lion and
David have exact rational-π fin apex angles; Lahdeli has them in float64 only. Lion has six flat central decagons and Kagemusha one central
pentagon. 12 DICTO solids need only one centre-strut length. Status: study note (dicto-vacuus-solids.pdf in DICTO's reading folder),
not published. The object itself is classical (the face fan's 2-cones cut at the surface, i.e. the cone from O over the edge skeleton);
DICTO's family, its sheets and struts forms and this census are new within the sources checked.

**Definition (confirmed with DICTO).** O is the corner centroid, and the centre pyramids (one per face, apex O) fill the solid. The Vacuus
is the set of interfaces between neighbouring pyramids: for each edge AB, the flat triangle O–A–B (a fin). DICTO came to it by building
a cube from his PET-bottle system B1NR, which showed the cube as six pyramids. On 2026-11-02 he also asked for two views of every Vacuus:
**SHEETS** (the fins) and **STRUTS** (rods O→every corner, optionally with the solid's edges), because he builds with bottles and struts.

Run on compute-host (~/work/vacuus, python3). vacuus.py ran as background processes, 16 at a time via xargs, one per
solid; collect.py, render.py (9 at a time) and typeset.py ran after that. Everything finished, and nothing is left running.
- scripts/qf.py: exact arithmetic in Q(√d) (d = 2, 3, 5) with exact sign, and the exact rational-π test. If cos 2θ lies in a quadratic
  field, θ/π is rational only for cos 2θ ∈ {0, ±1/2, ±1, (±1±√5)/4, ±√2/2, ±√3/2}.
- scripts/classical.py: the 5 Platonic and 11 Archimedean solids from textbook coordinates, exact in Q/Q(√2)/Q(√5), and the 11 Catalan
  solids as exact polar reciprocals. Every hull is checked exactly, and every solid matches krp-core's registry (data/classical-krp.json)
  by its squared-distance key. The snub cube, snub dodecahedron and their duals are float64 from the registry. Output: data/classical/*.json.
- scripts/vacuus.py <solid json> <out>: computes, per solid:
  - well-definedness (Theorem 1);
  - fins: squared sides, apex angle, right angles, exact congruence classes, symmetry orbits;
  - wedges (dihedral angles between neighbouring fins along a strut, inside one pyramid), with sums checked: 2π round a strut,
    (n−2)π + solid angle round a pyramid, total 4π;
  - flat sheets and central discs;
  - struts: count, exact length classes, edge lengths, frame lengths.
  The per-solid JSON (data/shapes, 9 MB) stays on compute-host and is not in git.
- scripts/collect.py: writes data/vacuus-census.json (one row per solid with all classes, exact strings) and data/collect.log (the flag
  lists). It also runs the polar check over the 92 convex solids. With P* the polar about O:
  - apex(P*) = π − dihedral(P), largest error 4.4e-16;
  - wedges(P*) = π − face angles(P), largest error 3.5e-10;
  - fin(e) ⊥ fin(e*), largest |cos| 2e-10.
- scripts/render.py: plates renders/<slug>.png with SHEETS and STRUTS side by side. It is our own numpy z-buffer rasteriser, 3×
  supersampled, with edges ≥ 2 px at 300 dpi, a translucent ghost of the solid and the DICTO mark. renders/<slug>.colours.json holds the
  legend. There are plates for the 5 Platonic solids and 13 DICTO solids: OG, Kagemusha, TI Star core, Cube Pearl, Golden Clasp, Hamlet,
  DICTO Hecatodihedron, OCD Stella, DICTO GTI, Lion, DBT, DICTO OTT and Star Halo. Cleo is a piece, not a solid of DICTO Solids v7, so it
  has no plate.
- scripts/typeset.py: paper.html, printed with print.mjs (A4) to ~/Documents/papers-to-read/dicto-vacuus-solids.pdf (15 pages). Every
  page was looked at.

Findings (details in data/collect.log):
- Isofin: 5 Platonic, 13 Archimedean, rhombic dodecahedron, rhombic triacontahedron, Delilah. No new DICTO solid is isofin.
- Same fin multiset: Octahedron = Delilah, and FPD = Palintriacontahedron (one shape held as two v7 entries, as the halo census already
  flagged). DBT and DICTO OTT share both fin shapes in different counts (54+6 vs 36+24).
- Rational-π apex angles (exact):
  - classical: octahedron, cuboctahedron, icosidodecahedron, deltoidal icositetrahedron, disdyakis dodecahedron, triakis octahedron;
  - DICTO: Kagemusha (45°, 72°), Lion (36°), David (90°, 120°), Delilah (90°); Lahdeli (90°) in float64 only.
- Central discs: octahedron (3), cuboctahedron (4 hexagons), icosidodecahedron (6 decagons), deltoidal icositetrahedron (3 octagons),
  disdyakis dodecahedron (9 octagons), disdyakis triacontahedron (15 dodecagons), tetrakis hexahedron (6 hexagons), triakis octahedron
  (3 squares), Delilah. Among DICTO's new solids: Lion (6 decagons) and Kagemusha (1 regular pentagon of five 72° fins).
- Right-triangle fins: OG (60, right angle at a corner), DICTO Jewel (24), DICTO TQHD (60), ED F18 (2), David (2, at O), Lahdeli (12),
  Lotus Hexa (48); among the classical solids, the octahedron and triakis octahedron.
- Fins congruent across symmetry orbits: 18 DICTO solids, e.g. DBT (2 shapes in 6 orbits) and Keyaxes (5 in 13).
- Buildability: DICTO solids with one centre-strut length are Blockhead, Cube Pearl, DICTO GTI, David, Delilah, Dodecaxes, Golden
  Clasp, Goliath, Icosaxes, TI Star core, Unborn Axes and White Knight. A whole frame (struts + edges) in at most 3 lengths: Cube Pearl,
  DICTO GTI, David, Delilah, Goliath, Icosaxes, TI Star core, Unborn Axes, White Knight. The cuboctahedron is the only one-length frame.
- Placeholder names (rule: given at once): Isofin Vacuus, Disc Vacuus (Lion Disc Vacuus, Kagemusha Pentagon Disc), One-Strut Vacuus.

Prior art, sources checked 2026-11-02 (the full list is in the PDF):
- Library (ask-library, top 5 + page hits), six queries: Leonardo vacuus / Pacioli; central dissection into face pyramids; cone over
  the edge skeleton; face fan / normal fan; excavated polyhedra (Wenninger); planes through centre and edges / spherical tiling. Hits
  included Pacioli 1509 pp. 9, 40, 76; Kepler 1619; Wenninger, Polyhedron Models; Johnson 1966; Goldberg 1937; Grünbaum 2010;
  Betke–Henk 2000; Alexeev 2002; Cutler–Schulte 2011; Fedorov 1885 ch. 13 and others.
- Web, four searches: Leonardo's vacuus solids (Wikipedia Divina proportione, MPIWG Leonardo-online book 86, Matemáticas Visuales,
  CityU HK, NNJ Monza); centre-to-edge triangles (arXiv 1909.02874, 2303.09702, 2307.06017, 2209.08919; US 8,599,195, 11,697,058,
  4,608,653); face fan (arXiv 2511.04322, Macaulay2, OSCAR); excavated polyhedra (Wikipedia Excavated dodecahedron, Wenninger list).
- What is classical: Leonardo's vacuus is a hollowed edge frame with no centre. The face fan (= normal fan of the dual) and its cones
  over the edges, the dissection into face pyramids, and the polar identities are classical. The excavated polyhedra are closed solids.
- What is new within these checks: the centre-to-edge fins and centre struts proposed as a family of built solids (DICTO), and the
  census over DICTO Solids v7.

Limits:
- O is the corner centroid. For solids without a unique symmetry centre (C1, Cs, Cn types), another centre gives another Vacuus.
- Symmetry orbits and flat sheets in float64 use tolerances of 1e-7 and 1e-9; sheet coplanarity is exact where the data is exact.
- Delilah, Samson, Lahdeli, Sonsam and the snubs are float64 only.
