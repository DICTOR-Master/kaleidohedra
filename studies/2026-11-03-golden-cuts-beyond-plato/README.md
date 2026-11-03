# Golden cuts beyond Plato (study, 2026-11-03)

DICTO chose this question from a list: after #88 ("Every Platonic Solid Has Exactly Two Golden Cuts"), which other
solids have golden cuts, and are they sections of the regular four-dimensional solids? Possible paper #89.
Results note (typeset): `~/Documents/papers-to-read/golden-cuts-beyond-plato.pdf` (source `note/paper.html`).

**Definitions (as #88).** A cut removes every corner by a plane perpendicular to the centre-corner line. On a solid
with unit edges, regular faces and all corners on one sphere, such a plane meets every edge at that corner at the same
distance x. An n-gon face becomes a 2n-gon with corner sides c_n x (c_n = 2cos(pi/n)) and original sides 1 - 2x; it is
*golden* when long/short = phi. Then x_G(n) = phi/(c_n + 2 phi) (corner sides long, "greater") or
x_L(n) = 1/(phi c_n + 2) (original sides long, "lesser"). For Catalan solids (corners of 2-3 orbits) the cut is per orbit
(y_o along the edges) and a face is golden when it becomes a 2n-gon whose corner sides all equal a and original sides all
equal b with a/b = phi or 1/phi.

## Results (all exact unless marked float)

**Platonic sanity (s1).** #88's ten cuts reproduced exactly (formula and golden-cuts-exact.md), and each rebuilt in
floating point with every face ratio phi.

**Theorem A (s1).** x_G(n), x_L(n) over n = 3, 4, 5, 6, 8, 10 are twelve different numbers (general proof: both decrease
strictly with c_n, and x_G(n) = x_L(m) would need c_n = phi^2 c_m > 2). So a solid of this kind has a cut making every
face golden only if all its faces have the same number of sides, and then exactly two. **All 13 Archimedean solids and
the elongated square gyrobicupola have none.** Each face kind alone has its two golden cuts (2 per face kind: 4 or 6 per
solid, all valid convex truncations); at x_G(n) an m-gon has ratio phi c_m / c_n, at x_L(n) ratio c_m / (phi c_n).

| n | x_G(n) (corner sides long) | x_L(n) (original sides long) |
|---|---|---|
| 3 | (3 - sqrt5)/2 = 1/phi^2 ~ 0.381966 | (5 - sqrt5)/10 = 1/(phi sqrt5) ~ 0.276393 |
| 4 | (sqrt10 + 2 sqrt5 - 3 sqrt2 - 2)/4 ~ 0.347943 | (sqrt10 + 3 sqrt2 - 2 sqrt5 - 2)/4 ~ 0.233196 |
| 5 | 1/3 | (7 - sqrt5)/22 ~ 0.216542 |
| 6 | (2 + sqrt15 + 6 sqrt5 - 7 sqrt3)/22 ~ 0.325683 | (2 + sqrt15 + 7 sqrt3 - 6 sqrt5)/22 ~ 0.208224 |
| 8 | phi/(sqrt(2+sqrt2) + 2 phi) ~ 0.318271 | 1/(phi sqrt(2+sqrt2) + 2) ~ 0.200411 |
| 10 | phi/(sqrt(phi sqrt5) + 2 phi) ~ 0.314904 | 1/(phi sqrt(phi sqrt5) + 2) ~ 0.196940 |

**Theorem B (s1).** Every face golden or regular (at least one golden) happens exactly when the face sizes are {3, 5},
because c_5 = phi c_3 is the only pair of regular polygons with c_m = phi c_n: the **icosidodecahedron** and the
**snub dodecahedron**, two cuts each:
- x = 1/(phi sqrt5): triangles golden (original sides long), pentagons regular decagons;
- x = 1/3: pentagons golden (corner sides long), triangles regular hexagons.
Icosidodecahedron, exact: x = 1/(phi sqrt5): 60 edges of length x, 120 of phi x; corners golden rectangles; volume
13/2 + 97 sqrt5/30. x = 1/3: 120 edges 1/3, 60 edges phi/3; volume 395/54 + 17 sqrt5/6. The first has White Knight's face
pattern (12 regular decagons, 20 truncated triangles of ratio phi, 30 golden rectangles) but is **not White Knight**: in
White Knight the long hexagon sides meet the rectangles (120 short + 60 long edges), here they meet the decagons (60 + 120).

**Theorem C (s2, s2b).** Per-orbit cuts of the Catalan solids: only the **rhombic dodecahedron** and the **rhombic
triacontahedron** admit cuts whose faces alternate a, b (a one-parameter family); each has **exactly two golden cuts**.
Rhombus of side 1, acute angle alpha: a = 2 y_sharp sin(alpha/2) = 2 y_blunt cos(alpha/2), b = 1 - aK,
K = (1/sin(alpha/2) + 1/cos(alpha/2))/2; greater b = 1/(1 + phi K), a = phi b; lesser b = 1/(1 + K/phi), a = b/phi.
- RD: K = (2 sqrt3 + sqrt6)/4. Greater a = 0.477001, b = 0.294803 (y_sharp = 0.413095, y_blunt = 0.292102), volume 2.94509.
  Lesser a = 0.322952, b = 0.522548 (y 0.279685, 0.197767), volume 3.03758. 12 octagons, 6 squares and 8 triangles of side a.
- RT: K = phi sqrt(2 + phi)/2. Greater a = 0.463634, b = 0.286541 (y 0.440942, 0.272517), volume 11.9873. Lesser
  b = 2/(2 + sqrt(2 + phi)) = 0.512543, a = 0.316769 (y 0.301265, 0.186192), volume 12.2076. 30 octagons, 12 pentagons, 20 triangles of side a.
- Other 11: the alternating equations have a unique solution with b < 0 (overlapping cuts: triakis tetrahedron,
  triakis octahedron, tetrakis hexahedron, deltoidal icositetrahedron, pentagonal icositetrahedron (float), triakis
  icosahedron, pentakis dodecahedron, deltoidal hexecontahedron, pentagonal hexecontahedron (float)) or none (disdyakis
  dodecahedron and triacontahedron: inconsistent). So no golden cut.
- Single-depth (equal cap height) and single-plane (equal distance from centre) cuts are special per-orbit cuts; neither
  golden cut of RD or RT is one of them, so these definitions give **no** golden Catalan cut. (The single-plane cut has
  one alternating member: ratio 2.3032 for RD, 1.5648 for RT.)

**Kepler-Poinsot (s3).** Same formula with k = 2cos(pi/p): exactly two golden cuts each, in the face-polygon sense.
Great dodecahedron 1/3, (7 - sqrt5)/22 (as the dodecahedron); great icosahedron 1/phi^2, 1/(phi sqrt5) (as the
icosahedron); small and great stellated dodecahedra (pentagram, k = 1/phi): greater (7 + sqrt5)/22, lesser 1/3, the
Galois conjugates of the pentagon's pair. The deeper pentagram cut passes the pentagram's crossing points (1/phi^2).
All eight are star polyhedra (self-intersecting faces), not solids bounding one region.

**4D sections (s4 float search, s5 exact).** Search: six regular polytopes x four main directions x 2400 heights,
77 targets. Sanity: #88's matches found again (Icosaxes / Unborn Axes in the 24-cell, the golden icosahedra and White
Knight in the 120-cell, Icosaxes in the 120-cell vertex-first). **New exact sections:**
- Greater / Lesser Golden Cut Tetrahedron = tesseract vertex-first sections x1+x2+x3+x4 = 2h at h = 1/phi^2 and
  h = 1/phi (corner layers at h = 0 and 1; x = (1-h)/(2-h); Archimedean truncated tetrahedron at h = 1/2). Also 120-cell
  vertex-first at atlas heights 25/16 + 11 sqrt5/16 (a corner layer) and 51/32 + 23 sqrt5/32 (middle of the next gap).
- Greater / Lesser Golden Cut Dodecahedron = 120-cell cell-first at atlas heights 37/32 + 17 sqrt5/32 and
  39/32 + 17 sqrt5/32: at 1/phi^2 and 1/phi of the gap from the icosidodecahedron layer (9/8 + sqrt5/2) to the
  dodecahedron layer (5/4 + 9 sqrt5/16); the Archimedean truncated dodecahedron is the middle (#65 atlas slice 120).
- Golden Cut Cubes: not found. None of the new solids (Archimedean one-kind cuts, ID and SD cuts, RD and RT cuts) was
  found in these directions. The snub cuts cannot be sections in any direction whose stabiliser contains their
  rotations (that stabiliser is generated by reflections, Steinberg), so such sections are mirror-symmetric.

**Space-filling (s6, light, positive only).** Cutting all cells of a tiling the same way leaves corner holes; checked by
volume: (1) Greater (Lesser) Golden Cut Tetrahedra + Icosaxes (Unborn Axes) + cuboctahedra of edge x; (2) Golden Cut
Cubes + octahedra; (3) golden cut rhombic dodecahedra + cubes + regular tetrahedra of edge a; (4) truncated octahedra
cut with one face kind golden + tetragonal disphenoids. These are the golden members of classical patterns (Andreini 1905).

**Exact recheck for #88 v2 (s7, 2026-11-03, after the study).** #88 compared Icosaxes with the 120-cell's vertex-first
section at phi/2 of the way to the tip (atlas height 11/8 + 5 sqrt5/8) in floating point. s7_icosaxes_exact.py redoes it
exactly in Q(sqrt5): the hyperplane meets no edge in its interior, the section is the layer of 24 corners at that height,
and a bijection to Icosaxes (DICTO Solids v7, exact) scales all 276 squared distances by 3 - sqrt5 exactly (also against
the octahedron cut at 1/phi^2). **HOLDS** (10/10 checks; data/s7-icosaxes-exact.json).

**Bijection proofs for the 120-cell sections (s8).** s5 compared sorted distance lists; s8_sections_bijection.py finds
for each of the four 120-cell sections (golden cut tetrahedra vertex-first, golden cut dodecahedra cell-first) a bijection
of corners scaling every squared distance by one factor, exact (4/4; data/s8-sections-bijection.json). Layers: cell-first
9/8 + sqrt5/2 has 30 corners (icosidodecahedron), 5/4 + 9 sqrt5/16 has 20 (dodecahedron); vertex-first 25/16 + 11 sqrt5/16
has 12, 13/8 + 3 sqrt5/4 has 4. Float-only extra: the search also matched the greater golden cut icosahedron at 120-cell
cell-first h/top 0.690983 (not checked exactly). fig5_tesseract.py: the tesseract strip for paper #89
(papers/golden-cuts-beyond-plato).

## Prior art (web + library, 2026-11-03)
- Zefiro 2011 (Visual Mathematics 13(2)): the icosidodecahedron truncated by a rhombic triacontahedron, stages with
  regular decagons at d = (4 tau + 3)/10 and regular hexagons at d = (tau + 4)/6. These are exactly the two cuts of
  Theorem B (d/R = 1 - x/(2 phi^2): 0.947214, 0.936339). The golden faces are not stated there. Credit Zefiro.
- Zefiro 2011 (cubic symmetry truncations): rhombic dodecahedron as truncating body, regular faces; no golden ratios.
- Koca et al. (2015, #88 ref 4): semi-uniform truncated octahedra; Koca group: quaternionic H3/H4 orbits.
- Boole Stott 1900: the section series. Andreini 1905: the honeycombs behind the fills.
- Not found: golden-ratio truncation of Archimedean, Catalan or Kepler-Poinsot solids as such.

## Uncertain
- The two pentagonal Catalan solids are done in floating point (b clearly negative).
- 4D: float search in four main directions only; "not found" is not a proof.
- KP: "sensible solid" is a matter of definition.
- Zefiro's figures were not all read; he may show the golden faces without naming them.

## Files
scripts/: gcb.py, gcb_exact.py (geometry), s1 ... s6, figs.py. data/: s1-archimedean.json, s2-catalan.json,
s2b-rhombic.json (incl. corner coordinates at unit edge), s3-kepler-poinsot.json, s4-sections4d.json (+ run log),
s5-exact4d.json, s6-spacefill.json, s7-icosaxes-exact.json, s8-sections-bijection.json; every file carries its checks (all pass: 235, 51, 12, 24, -, 7, 10, 10, 4).
Run on dicto-big-brother with ~/geom/bin/python from scripts/ (s4 and s5 need ~/kres-tmp/dataset-v7 and the #65 atlas code).
