# The twin Vacuus of the OG — the Angeli family (11 Nov 2026)
DICTO: "it has perfect truncated triangles and penrose stars... what would a vacuus form of the og look like" → "do the twin vacuus".
DICTO named the twin Vacuus forms the **Angeli family** ("Angeli family, Angelus for one", 11 Nov 2026; twin forms only, not the #87 census Vacuus solids). The twin hull Vacuus below is the **twin OG Angelus**.
The OG's own Vacuus is in the #87 census (180 fins, 45 fin planes, 120 sheets, 2 strut lengths; reproduced here as control).
Twin = Galois swap √5 → −√5 on the exact OG coordinates (the "perpendicular" side of the 6D picture, og-margin §28).
scripts/twin_vacuus.py (exact OG coordinates from the five-fold-octet tools), data/twin-vacuus.json, figures/twin-vacuus.png. FINAL ok.

(i) TWIN HULL = convex hull of the 102 twin points: a NEW convex icosahedral solid, all 102 points corners, 200 TRIANGLES, 300 edges
(simplicial; the OG's 20 hexagons + 60 kites become 200 triangles). Struts (centre → corner) in 2 lengths, 1/φ = 0.618034 and 0.627748.
Its Vacuus: 300 fins, apex angles 10.0928° (60), 11.8246° (60), 24.2136° (120) and EXACTLY 36° (60); 81 fin planes through O;
186 flat sheets: 120 single fins, 60 pairs and SIX DISCS of ten fins each (10 × 36° = 360°): one full decagonal central disc across
each of the six five-fold axes. So the twin hull's Vacuus is a DISC VACUUS of the kind the census found in the Lion (6 decagon discs).
(ii) STAR TWIN = the OG's own 80 faces on the twin points: the swap keeps every face flat (off-plane ≤ 2e−16) and every face stays a
convex kite or hexagon, but the faces no longer bound a convex solid (they meet the twin hull's faces in only 20 % of the OG's edges,
§28). Its Vacuus has the OG's combinatorics: 180 fins, 45 fin planes, 120 sheets (60 single + 60 pairs), 2 strut lengths; apex angles
10.0928° (60) and 55.6906° (120).
EXACT COINCIDENCE: the star twin's large fin angle equals the OG kite's tip angle: cos² = 43/72 − (1/8)√5 for both (checked in ℚ(√5)):
the OG kite's tip angle reappears as the angle at the centre between the twin images of a kite–kite edge.
Figure: three panels (OG Vacuus, twin hull Vacuus, star twin Vacuus), fins coloured by apex angle; quick study figure, not a print
render (render standard not applied).

## Render and exact values (DICTO: "render the twin hull vacuus with the discs", "what are its laws")
figures/twin-hull-vacuus-discs.png (scripts/render_twin_discs.py, the #87 census renderer: own z-buffer, 3x supersampled, edges ≥ 2 px):
left, the 300 fins with the 60 disc fins in gold; right, the six decagonal discs alone in six colours inside a ghost of the hull.
EXACT (ℚ(√5), from the exact OG):
- Corners: 90 at radius² 3/2 − √5/2 = 1/φ² (radius 1/φ; the twins of the OG's 90 corners at radius² φ²), 12 at radius²
  (585 − 198√5)/361 (twins of the OG's 12 five-fold corners at (585 + 198√5)/361).
- Faces: 200 triangles; edges 300; corner degrees: 72 corners of degree 5, 30 of degree 8 (Euler 102 − 300 + 200 = 2).
- Fin apex angles: cos² = 17/18 + √5/90 (10.0928°, 60 fins), 547/648 + 11√5/216 (11.8246°, 60), 7/12 + √5/9 (24.2136°, 120),
  3/8 + √5/8 = cos² 36° (60 fins, exactly 36°).
- DISC LAW: the 60 fins of exactly 36° lie in six planes through O, ten per plane, and close into six complete decagonal discs, one
  perpendicular to each five-fold axis.
- Star twin: its large fin angle equals the OG kite's tip angle, cos² = 43/72 − √5/8 (exact).
Open: is the disc law a property of every twin level (the twins of D_1, D_2, …) or of the OG alone? Is the twin hull a known solid?

## Disc law on levels 0–10 (DICTO: "yes test the disc law on levels 1–10"; scripts/twin_disc_levels.py, data/twin-disc-levels.json, FINAL ok)
Twin hull of D_k (exact corners, twins without cancellation), its Vacuus, discs = coplanar fins through O adding to 360°.
k = 0: 102 hull corners, 200 triangles, 6 discs of ten 36° fins (control). k = 4: 90 corners, 140 triangles + 12 pentagons, again
6 discs of ten 36° fins. All other levels: no discs. The other twin hulls are, by face counts, the classical icosahedral solids:
k = 2 icosahedron (12 corners, 20 triangles); k = 3, 7 dodecahedron (20, 12 pentagons); k = 1, 5, 6 rhombicosidodecahedron type (60;
20 triangles, 30 squares, 12 pentagons); k = 8 truncated-icosahedron type (60; 12 pentagons, 20 hexagons); k = 10 truncated-
icosidodecahedron type (120; 30 squares, 20 hexagons, 12 decagons); k = 9: 180 corners, 20 triangles, 120 squares, 12 decagons.
Reading: the twins collapse inward (og-margin §28) and the outermost twin points form ONE symmetry orbit at most levels; the hull of one
icosahedral orbit is a Wythoff-type orbit polytope, hence the classical face counts. Discs need ten corners evenly round O in one
plane, which happens at k = 0 and 4, the two levels whose hull uses two orbits. Whether the faces are exactly regular: not yet checked.
CORRECTION: the script labels the discs "perp mirror/other" because it tests against the OG's own axes; the twin's symmetry is the
Galois-conjugate icosahedral group (its matrices conjugated), whose five-fold axes point elsewhere. The discs are perpendicular to the
twin's five-fold axes.
DICTO (11 Nov): "I feel like these vacuus shapes are like angels".

## Are the twin hulls exactly regular? (DICTO: "check if the twin hulls are exactly regular"; scripts/twin_regular.py, data/twin-regular.json, FINAL ok)
EXACTLY uniform (all faces regular, one edge length, corners on one sphere): k = 2 REGULAR ICOSAHEDRON; k = 3 and k = 7 REGULAR
DODECAHEDRON. The hidden (twin) side of the OG family passes through the true Platonic solids.
Archimedean PATTERNS with stretched faces (corners on one sphere, every face equiangular):
- k = 1, 5: rhombicosidodecahedron type; triangles and pentagons regular, the 30 squares are golden rectangles, sides φ² = 2.618034 : 1.
- k = 6: same type, rectangles 3.168859 : 1 (not yet identified exactly).
- k = 8: truncated-icosahedron type; pentagons regular, hexagons equiangular with alternating sides 1.054533 (truncated triangles).
- k = 10: truncated-icosidodecahedron type; rectangles (3.317083), truncated triangles and alternating-sided decagons, all equiangular.
Not equiangular: k = 0 (4 edge lengths, max/min 3.472136 = 2√5 − 1), k = 4 (3 edge lengths, max/min exactly 3; pentagons regular),
k = 9 (5 edge lengths, corners on two spheres).
DICTO (11 Nov): "the numbers run beautifully at least".

## The three ratios, exactly (DICTO: "identify the three ratios exactly"; scripts/twin_ratios_exact.py, data/twin-ratios-exact.json, exact ℚ(√5), FINAL ok)
Squared side lengths are exact in ℚ(√5); each ratio's square turned out to be a square in ℚ(√5), so the ratio itself is in ℚ(√5).
Controls reproduced: k = 0: 2√5 − 1; k = 1, 5: (3 + √5)/2 = φ²; k = 4: 3.
- k = 6 (rectangles of the rhombicosidodecahedron-type twin hull): **(17√5 − 19)/6 = 3.168859270…**
- k = 8 (the truncated-triangle hexagons): exact but not simple: p + q√5 with p = 3044292428786136875631557/3499264300708543451073182,
  q = 288809153275608825089507/3499264300708543451073182 (= 1.054532899…): numbers of 25 digits, as the coordinates of D_8 grow.
- k = 10 (rectangles of the truncated-icosidodecahedron-type twin hull): exact in ℚ(√5) with numerators and denominators of about
  500 digits (= 3.317083246…), stored in the json.
Script note: the first run printed the negative square root for k = 0 and 6 (1 − 2√5, (19 − 17√5)/6); fixed to take the positive root.

## Render: the Angeli at levels 2 and 3 (DICTO: "render the twin hull Angeli for levels 2 and 3"; scripts/render_angeli_levels.py, figures/angeli-levels-2-3.png)
Level 2 Angelus = Vacuus of the regular icosahedron (twin hull): 30 fins, all congruent, apex 63.4349° (cos = 1/√5), 15 fin planes
(opposite fins coplanar). Level 3 Angelus = Vacuus of the regular dodecahedron: 30 fins, apex 41.8103° (cos = √5/3), 15 fin planes.
These are the classical Vacuus of the two solids (also in the #87 census), here arising on the twin side of the OG family. Fins
coloured by their plane through the centre (12-colour palette, so 3 colours repeat among the 15 planes).
Levels 1 and 4 (figures/angeli-levels-1-4.png, one colour per fin plane): level 1 Angelus (golden-rectangle rhombicosidodecahedron
type): 120 fins, apex 12.8684° and 34.1211°, 60 fin planes. Level 4 Angelus (140 triangles + 12 pentagons): 240 fins, apex 11.8246°,
24.2136° and 36°, 66 fin planes (60 + the six disc planes). DICTO (11 Nov): "sometimes extra fins are hidden in 4D bodies".
DICTO (11 Nov): "never born and never dying suits angels". Precisely: each hidden fin is born at one exchange and ends at another, both inside the sweep, so neither its birth nor its end is ever seen from either 3D world; and in the twin sweeps no fin runs from top to bottom at all (top and bottom slices share 0 edges at every hop).
Render (DICTO: "render the hidden fins of the twin sweep"; scripts/render_hidden_fins.py, figures/hidden-fins-hops-0-1.png): the 3D slice
of the twin sweep at the slider height where most hidden walls are present; every edge of the slice is a wall, its fin = triangle
(centre, edge); hidden fins gold, the others grey, ghost of the slice. Hop 0 (height 0.4595 of 0.996 … 0): 150 fins, ALL 60 hidden
walls present at once. Hop 1 (height 0.3894 of 1.428 … 0): 330 fins, ALL 180 hidden walls present at once. So the hidden fins of a
hop live together in one middle band of the sweep: one hidden 3D world between the two visible ones.

## The middle world on hops 0–9 (DICTO: "yes test the middle world on hops 2–9"; scripts/middle_world.py, data/middle-world.json, FINAL ok)
All hidden walls of a twin hop present together in one slice? Hops 0, 1: YES (60/60, 180/180; a band of heights 0.41–0.46 and
0.29–0.39). Hops 2–9: NO. The most present at once: 180/240, 300/360, 120/270, 210/390, 600/1020, 660/1410, 450/960, 930/2250 (hops 2–9);
from hop 5 the fullest slice sits low, close to the bottom world (heights 0.047, 0.14, 0.001, 0.007, 0.005 against tops 0.5–2.3).
Verdict: one middle world only at the first two hops; later the hidden fins live in several overlapping bands (at least 2, up to
about 2.4 slices' worth), crowding toward the bottom. Law (9) holds for hops 0 and 1 only.
Render of hop 9's bands (DICTO: "render the hidden fin bands for hop 9"; scripts/render_bands.py, figures/hidden-bands-hop-9.png): profile
of hidden fins present against slider height (0 … 0.48) and the slices at the two strongest bands. The upper bands (heights about
0.13–0.20) hold 250–320 hidden fins; a dense stack sits just above the bottom world (0 … 0.02) with up to 930. At the two band slices
shown (0.0185 and 0.0046) EVERY fin of the slice is hidden (630 of 630, 930 of 930): whole hidden worlds, not mixtures. (Figure note:
the "bottom world" label overlaps the lowest bars.)
Hop 5's bands (DICTO: "render the hidden worlds for hop 5"; figures/hidden-bands-hop-5.png; label overlap fixed): bands at heights
about 0.2–1.0 (90–200 hidden fins) and one strong band just above the bottom (0.0466: 210 of 390). Unlike hop 9, these slices are
MIXED: 0.4367 holds 120 hidden fins among 300 (hidden fins scattered as single orbits through a visible-looking world); 0.0466 holds 210
hidden among 330, the hidden fins fanning round the five-fold directions in broad sheets. Hop 9 had wholly hidden worlds; hop 5 still
has its hidden fins woven into visible ones: the hidden share per slice grows with the hop.
Hop 7's bands (DICTO: "render the hidden worlds for hop 7"; figures/hidden-bands-hop-7.png): upper bands at heights about 0.10–0.20
(150–330 hidden fins) and a dense stack within 0.002 of the bottom world. The two strongest slices (0.0013 and 0.0012; the band
picker separates by index, so both fall in the bottom stack) are WHOLLY hidden: 420 of 420 and 660 of 660 fins, fanned round the
centre. So whole hidden worlds appear by hop 7 (hop 5: mixed; hops 7, 9: wholly hidden worlds just above the bottom world).
Hop 7's UPPER bands (DICTO: "render an upper band of hop 7"; render_bands.py with MINH = 0.05, bands now separated by height;
figures/hidden-bands-hop-7-upper.png): height 0.1724: 270 fins, 210 hidden — the slice has 152 corners, 120 faces (60 four-sided,
60 pentagons); height 0.0857: a WHOLLY hidden world of 90 fins — the slice has 32 corners, 60 triangles, 90 edges: the combinatorics of
the PENTAKIS DODECAHEDRON (a Catalan solid; whether its shape is exactly Catalan is not checked).
Is the hidden pentakis world exactly Catalan? (DICTO: "check if the hidden pentakis world is exactly Catalan"; scripts/pentakis_check.py,
FINAL ok) NO. (1) All 60 triangles ARE tangent to one sphere (face distances equal to machine precision: one symmetry orbit), and the
shape only scales within its band. (2) But its dual (hull of the 60 face directions) is a truncated-icosahedron PATTERN whose hexagons
have alternating sides 6.1468 : 1 (Catalan needs a regular truncated icosahedron, 1 : 1). The world has 3 edge lengths (the Catalan
pentakis has 2), long/short 1.1703 against the Catalan 1.1273, corner radii 0.8525 : 1 against 0.9742 : 1. It is a pentakis
dodecahedron with an insphere and congruent faces, but not the Catalan one.

## Other pentakis dodecahedra as starts (DICTO: "i wonder if other pentakis produce dodecahedrons, icosahedrons and rhombicosidodecahedrons"; scripts/pentakis_family.py, data/pentakis-family.json, exact ℚ(√5), FINAL ok)
Starts: the Catalan pentakis dodecahedron (polar dual of the regular truncated icosahedron) and regular dodecahedra with a pyramid on each
face, apex heights h = 1/20, 1/10, 1/5, 3/10 and 1/φ³ of the face distance. For EVERY start, levels 0–9:
- twin hulls cycle with period 4: REGULAR DODECAHEDRON (k ≡ 0) → rhombicosidodecahedron pattern (k ≡ 1) → REGULAR ICOSAHEDRON (k ≡ 2) →
  rhombicosidodecahedron pattern (k ≡ 3) → …; rectangle ratios repeat (Catalan: φ² = 2.618034 at k ≡ 1, 2φ² = 5.236068 at k ≡ 3;
  h = 1/φ³: 7.854102 and 1.723607; the others, all exact in ℚ(√5), in the json).
- the real family cycles too: pentakis (32 corners, 60 triangles, corners on 2 spheres) ↔ a 60-corner, 32-face solid with all corners
  on ONE sphere (truncated-icosahedron type), and D_{k+4} = D_k up to scale (same face count and corner-radius pattern) at every level.
So pentakis dodecahedra are CYCLING POINTS of the hop (period 4, like the Universal PiTet beats), and the twin cycle is the Galois image
of the real cycle. The OG family is the OUTSIDER: it does not cycle (faces grow without end) and touches the Platonic solids on its
hidden side only at k = 2, 3, 7. For the Platonic book Chapter 12 (with the Outsider opening). Next to check: the exact scale of the
4-cycle (D_{k+4} = c·D_k, c in ℚ(√5)) and whether "up to scale" is exact similarity (only face counts and radius pattern compared so far).

## The 4-cycle exactly, and the Angeli thread (DICTO: "check the exact scale of the 4-cycle and angel family thread"; scripts/pentakis_cycle.py, data/pentakis-cycle.json, exact ℚ(√5), FINAL ok)
EXACT SIMILARITY: D_{k+4} = c · D_k as exact point sets (same orientation) for k = 0 … 4, for each start; c in ℚ(√5), depending on the start:
Catalan pentakis c = 3549/9701 + (7712/48505)√5 = 0.721359782…; h = 1/5: c = 67300/187167 + (29680/187167)√5 = 0.714156329…;
h = 1/φ³: c = 158/435 + (14/87)√5 = 0.723045422…. So each pentakis start is a true cycle of the hop up to the scale c (no universal c).
ANGELI THREAD round the cycle (twin hull Vacuus at k = 0, 1, 2, 3; then it repeats):
- k ≡ 0: the DODECAHEDRON Angelus, 30 congruent fins, apex 41.8103°, cos² = 5/9 exactly, 15 fin planes — the same for every start;
- k ≡ 2: the ICOSAHEDRON Angelus, 30 congruent fins, apex 63.4349°, cos² = 1/5 exactly, 15 fin planes — the same for every start;
- k ≡ 1, 3: a rhombicosidodecahedron-pattern Angelus, 120 fins in 60 planes, two fin classes whose angles depend on the start
  (Catalan: 12.8684° and 34.1211° at k ≡ 1, 7.0663° and 37.6501° at k ≡ 3; all cos² exact in ℚ(√5), in the json). No discs anywhere.
The thread: dodecahedron Angelus → rhombicosidodecahedron Angelus → icosahedron Angelus → rhombicosidodecahedron Angelus → (scaled) back.
Render (DICTO: "render the Angeli thread for the Catalan pentakis"; scripts/render_thread.py, figures/angeli-thread-catalan.png): the four Angeli of one turn, 2 x 2, fins coloured by plane: k = 0 dodecahedron Angelus (30 fins, 41.81°), k = 1 rhombicosidodecahedron Angelus (120 fins, 12.87° and 34.12°), k = 2 icosahedron Angelus (30 fins, 63.43°), k = 3 rhombicosidodecahedron Angelus (120 fins, 7.07° and 37.65°); then the cycle returns scaled by c = 0.7214.
Render (DICTO: "render the Angeli thread for the OG levels 0 to 7"; scripts/render_thread_og.py, figures/angeli-thread-og-0-7.png): 2 x 4
panels, fins coloured by plane. k = 0 twin OG Angelus (300 fins, 81 planes, six discs); k = 1 rhombicosidodecahedron Angelus (120 fins,
12.87° and 34.12°); k = 2 icosahedron Angelus (30, 63.43°); k = 3 dodecahedron Angelus (30, 41.81°); k = 4 the 140 + 12 Angelus (240 fins,
66 planes, six discs); k = 5 = the k = 1 kind (12.87°, 34.12°); k = 6 rhombicosidodecahedron Angelus with new angles 10.98° and 35.28°;
k = 7 dodecahedron Angelus. No cycle: the OG's thread visits the Platonic Angeli irregularly (I at 2; D at 3, 7).
OBSERVED (4 decimals, not yet exact): the OG's k = 1 and k = 5 Angeli have the SAME fin angles (12.8684°, 34.1211°) as the Catalan
pentakis's k = 1 Angelus, and the same golden rectangles (φ²): the OG thread touches the pentakis cycle there. To check exactly
(cos² 6909/11881 + 1960√5/11881 and 7749/11881 + 176√5/11881 for the Catalan).
LEVEL-1 MATCH, EXACT (DICTO: "check the level 1 match exactly"; scripts/level1_match.py, FINAL ok): the OG's level-1 and level-5 Angeli
ARE the Catalan pentakis's level-1 Angelus: identical exact fin classes (cos² 6909/11881 + 1960√5/11881 and 7749/11881 + 176√5/11881, 60
fins each) and the twin hulls exactly similar (OG k = 1: c = (9 − 3√5)/2 = 3/φ²; OG k = 5: c = (567 − 243√5)/164; same orientation, exact
point sets). The outsider's thread passes exactly through the pentakis cycle at levels 1 and 5. CAUTION: c depends on the arbitrary size
of the Catalan start (built from the truncated icosahedron of edge 2), so c = 3/φ² is not yet meaningful; check with a natural common
normalisation (equal circumradius or insphere of the starts) before reading anything into it.
SCALE NORMALISED (DICTO: "check the 3/φ² scale with a common normalisation"; scripts/scale_norm.py, data/scale-norm.json, FINAL ok):
scaling a start by s scales its twin family by s' = conj(s), so only scales in ℚ(√5) keep the twin comparison. Equal circumradius
(s² = 21195/722 + 9423√5/722) and equal inradius (s² = 169/6 + 25√5/2) are NOT squares in ℚ(√5): those normalisations leave the golden
field. In-field normalisation: the 12 five-fold corners of the two starts made to coincide (s = (9 + 3√5)/2): then c = 1 EXACTLY. The
3/φ² was an artefact of the Catalan start's arbitrary size (its twin (9 − 3√5)/2). RESULT: an OG and a Catalan pentakis dodecahedron with
the same five-fold corners have IDENTICAL level-1 twin hulls, hence the identical level-1 Angelus (and the OG's level 5 gives it again,
scaled). The outsider and the clockwork meet in one identical hidden form.
Render (DICTO: "render the identical level 1 Angelus"; scripts/render_shared_angelus.py, figures/shared-level1-angelus.png, FINAL ok = the two level-1 twin hulls equal as exact point sets): left the OG (60 kites purple, 20 hexagons teal), middle the Catalan pentakis scaled to the same five-fold corners (60 triangles), right their common level-1 Angelus (120 fins, 60 planes, 12.87° and 34.12°). First render showed the fill triangles inside the OG faces; fixed (one outline per face).

## The gnomon polynomial (DICTO: "are we any closer to finding a polynomial" → "a gnomon", 11 Nov)
Each pentakis start is an exact GNOMON of the hop: D_{k+4} = c·D_k, c in ℚ(√5), so c is a root of a quadratic over ℤ, whose other root is
its twin c′ (the hidden side's scale per turn):
- Catalan pentakis: 48505 c² − 35490 c + 361 = 0 (c = 0.721359782, c′ = 0.010317364);
- pyramid height 1/φ³: 6525 c² − 4740 c + 16 = 0 (c = 0.723045422, c′ = 0.003391360);
- pyramid height 1/5: 561501 c² − 403800 c + 2000 = 0 (c = 0.714156329, c′ = 0.004987537).
One large root (the visible shrink per turn) and one tiny root (the twin collapse per turn), as φ and −1/φ. The OG has no gnomon polynomial:
no step or run of steps of its family is a classical gnomon (og-margin §3); it only approaches one (gnomon defect δ_k → 0). Open: a
polynomial for the OG family's LIMIT, and c as a function of the pyramid height h.

## Tracing the cross-occurrences: the OG is a truncated Catalan pentakis (DICTO: "fit c as a function of the pyramid height; could we tie any of these phenomena together by tracing back instances of cross occurrence at lower levels"; scripts/cross_trace.py, exact ℚ(√5), FINAL ok)
(1) SHARED PLANES: with the same five-fold corners (Catalan start scaled by s = (9 + 3√5)/2), ALL 60 kite planes of the OG are exactly the
60 face planes of the Catalan pentakis dodecahedron. The OG = the Catalan pentakis with its 20 six-fold corners cut off by the 20
hexagon planes (each kite = a pentakis triangle without its far tip).
(2) TRACE of exact twin-hull similarities (OG level k ↔ Catalan cycle step j): k = 1 ↔ j = 1 (c = 1, identical), k = 2 ↔ j = 2
(c = 1, identical), k = 3 ↔ j = 0 (c = (81 − 27√5)/164), k = 5 ↔ j = 1 (same c), k = 7 ↔ j = 0 (exact, long). Real side: the OG's level 1
CONTAINS ALL 60 corners of the Catalan's level 1 (shared kite/triangle planes give the same 60 foot points); levels 0 and 2 share the 12
five-fold corners. The 20 hexagon foot points are the outsider's extra; their twins lie inside the twin hull at levels 1 and 2 (identical
twin hulls), later they spread and the match returns only scaled (3, 5, 7). Ties: the shared Angelus, the Platonic Angeli of the OG at
2, 3, 7, and the kite echo all trace back to the OG = pentakis ∩ 20 hexagon planes.
(3) c(h), pentakis heights h = 1/20, 1/10, 3/20, 1/5, 1/4, 3/10: c = 0.680023, 0.696830, 0.688231, 0.714156, 0.724324, 0.719649 (exact in
ℚ(√5), in the log): NOT monotone; no smooth fit found (next: check whether the in-between solids change combinatorial type with h). The
pentakis shape at k = 2 equals that at k = 0 (radius ratio identical): the REAL cycle has period 2 up to a scale √c that lies OUTSIDE
ℚ(√5); the twin cannot follow a non-golden scale, so on the hidden side the cycle shows period 4 (dodecahedron and icosahedron alternate).

## The cut-depth family: the OG is the critical cut (DICTO: "set up the cut-depth family and it only has two edge lengths", "and a kite like the yantra", "regular hexagons"; scripts/cut_family.py, exact ℚ(√5), FINAL ok)
Catalan pentakis (same five-fold corners as the OG) with its 20 six-fold corners cut by planes ⊥ the three-fold axes at λ × the corner
radius. The OG's hexagon planes sit at λ* = 1/2 + √5/6 = φ²/3 exactly (the reciprocal of the margin constant 3/φ², here from the geometry).
λ = 0.95, 0.90: 132 corners, 60 pentagons + 20 hexagons, 3 edge lengths. λ = φ²/3: 102 corners, 60 KITES + 20 hexagons, 2 EDGE LENGTHS
(= the OG exactly, control). λ = 0.85, 0.80: 132 corners, 80 triangles + 60 pentagons, 4 edge lengths. λ = 0.75: the cuts overrun the
neighbours. Hexagons are regular at every depth in range (forced by the three-fold symmetry), so they do not single out the OG.
RESULT: the OG is the Catalan pentakis dodecahedron cut at its six-fold corners EXACTLY UNTIL THE CUTS TOUCH: there the dodecahedron edge
between two six-fold corners shrinks to zero, each pentagon becomes a kite and the edge lengths drop to the minimum, two (the rectification
move, as icosahedron → icosidodecahedron). No cut depth keeps the 4-cycle. The OG = the most economical break of the clockwork.
KITE vs YANTRA: in the Śrī Yantra the kite O-E-T-E appears where the legs of the great triangles meet; in the OG where the two corner
cuts meet. The shapes differ: OG kite 68.62°, 117.85°, 55.69°, 117.85° vs the classical yantra kites ≈ 78°, 106°, 70°, 106° (Huet, Kavi
Mahesh; sri-yantra study table).
Render (DICTO: "render the OG cut family with the kites"; scripts/render_cut_family.py, figures/og-cut-family.png, FINAL ok = the φ²/3 cut is the OG): uncut Catalan pentakis (60 triangles) → 0.95 (small hexagons, 60 pentagons) → 0.90 (larger hexagons) → φ²/3 the OG (pentagons become kites, purple) → 0.85 (the cuts overrun: 80 triangles + 60 pentagons). Faces coloured triangles gold, kites purple, pentagons orange, hexagons teal.

## Prior-art search: the OG as the cut Catalan pentakis (11 Nov night)

**Verdict: not found as such; partial (the same cut, at a shallower depth, is catalogued).** No source checked shows a convex icosahedral solid with 60 congruent kites + 20 regular hexagons (102 vertices, 180 edges, 80 faces, two edge lengths, kite ratio 1.20676). The closest relative is McCooey's **6-Truncated Pentakis Dodecahedron (canonical)**: the same operation (cut only the 20 six-fold vertices of the pentakis dodecahedron), but at the canonical depth. There the cuts do not touch, so each pentakis triangle becomes a **pentagon**: 132 vertices, 210 edges (150 short + 60 long), 80 faces = **60 pentagons + 20 hexagons** (counted from his data file), with coordinates in Q(√3, √5). The OG is the limit of that cut, where the 30 short edges left on the six-fold-to-six-fold pentakis edges shrink to zero (132 − 30 = 102 vertices, 210 − 30 = 180 edges) and the pentagons become kites. Its coordinates lie in Q(√5) alone. In Conway terms the canonical solid is t6kD. Hart's page says that tn fixes only the topology, so "t6kD" does not name the OG's combinatorics. Our own derivation from the operator matrices on the Wikipedia Conway-notation page gives the OG's combinatorial type as dL0D, the dual of the joined-lace dodecahedron (L0D: 12 pentagons + 30 quads + 60 triangles, 80 vertices). No source showed dL0D for the dodecahedron seed, and none showed it in this geometry.

**Other relatives checked (with face counts):**
- Pentakis dodecahedron kD: 60 triangles, 32 vertices (the parent).
- Truncated pentakis dodecahedron tkD (all 32 vertices cut) = Goldberg GP(3,0): 12 pentagons + 80 hexagons = 92 faces, 180 vertices.
- Chamfered dodecahedron cD: 12 pentagons + 30 hexagons, 80 vertices.
- Rectified truncated icosahedron: 60 triangles + 12 pentagons + 20 hexagons, 90 vertices.
- Deltoidal hexecontahedron oD: 60 kites, 62 vertices (kites, but no hexagons).
- Hexapentakis truncated icosahedron: dual of tkD, triangles and hexagons.
- McCooey's Joined Truncated Icosahedron (Archimedean–Catalan hull of tI + kD): the convex hull, not the OG (the OG lies inside; its hexagon planes are the tI hexagon planes of the canonical tI/kD compound, which pass through the midpoints of the kD six-to-six edges).
- Near-miss Johnson solids (icosahedral entries): chamfered dodecahedron, rectified truncated icosahedron, truncated truncated icosahedron, expanded truncated icosahedron, snub rectified truncated icosahedron. None has kites or 102 vertices.
- Tetrated dodecahedron, Goldberg polyhedra in general: no kites.

**Sources checked**
- Local library: ~/Documents/reference-library holds only README.md, WHERE-IS-THE-LIBRARY.txt, INDEX.pdf and one PDF. The full library is on the other machine and was not reachable from here (no ssh by instruction); ~/kaleidohedra-references does not exist locally. We grepped the README/txt files for pentakis, "truncated pentakis", "102 vertices", "60 kites", ogdoecontahedron, "rectified pentakis", "kites and hexagons", tkD: no hits. We grepped the INDEX.pdf text (12,132 lines) for pentakis, kite, "102 vert", ogdoe, rectif, Catalan, Conway, Hart, McCooey, near-miss, chamfer, Goldberg: no pentakis/kite/102 entries. It lists only Hart's Virtual Polyhedra, Conway–Burgiel–Goodman-Strauss, Antiprism `conway`, Goldberg 1937 and the Goldberg space-filler series, none about this solid. **The library MANIFEST.json files on the other machine still need a grep.**
- https://dmccooey.com/polyhedra/ (index), TruncatedCatalan.html, 6TruncatedPentakisDodecahedron2.html + .txt (vertex/face data counted), Hull.html, Derived.html (incl. Expanded Joined Truncated Pentakis Dodecahedron: not this solid)
- https://en.wikipedia.org/wiki/Truncated_pentakis_dodecahedron, https://mathworld.wolfram.com/TruncatedPentakisDodecahedron.html (via search results), https://en.wikipedia.org/wiki/Hexapentakis_truncated_icosahedron (via search results)
- https://en.wikipedia.org/wiki/Near-miss_Johnson_solid
- https://en.wikipedia.org/wiki/Solids_with_icosahedral_symmetry
- https://en.wikipedia.org/wiki/Conway_polyhedron_notation (operator matrices, both parts)
- https://georgehart.com/virtual-polyhedra/conway_notation.html (tn semantics)
- https://geogebra.org/m/uej4qnte (series of truncations of the biscribed pentakis dodecahedron: no face data given; not resolved)
- Search results seen but not opened: AMS Visual Insight "Rectified truncated icosahedron", Virtual Math Museum icosahedron page, Paul Bourke uniform polyhedra, robertlovespi.net ("180 kites" polyhedron page, a different solid), polytope wiki Pentakis dodecahedron.

**Web queries (standard mode):** "truncated pentakis dodecahedron kites hexagons"; polyhedron "60 kites" "20 hexagons" icosahedral; "dmccooey polyhedra pentakis dodecahedron truncated variants"; "t6kD" polyhedron conway notation; "polyhedron 102 vertices 180 edges 80 faces icosahedral kites hexagons"; "near-miss Johnson solid kites regular hexagons icosahedral Kaplan Hart" (returned only aviation results); "robertlovespi kites regular hexagons icosahedral polyhedron pentakis dodecahedron truncated"; "joined-lace" dodecahedron polyhedron conway L0 dual. We did not use extended mode.

**Still open:** grep the full library manifests on the other machine. Robert Austin's blog (robertlovespi.net) has thousands of polyhedra and was not searched page by page, so it is the likeliest place for an unnoticed match. Polyhedronisme and Antiprism `conway` were not run.
Judged (main session, 11 Nov night): accepted. Verdict PARTIAL: no published convex solid with 60 kites + 20 regular hexagons found; the
SHALLOWER cut is catalogued (McCooey, "6-Truncated Pentakis Dodecahedron (canonical)": same 20 six-fold vertices cut, cuts not touching,
60 pentagons + 20 hexagons, 132 vertices, coordinates in ℚ(√3, √5)); the OG is its touching limit (ℚ(√5) only). The Conway form "dL0D"
is the agent's own derivation, NOT in any source: check before quoting. Library gap closed here: the full library on the compute machine
has no cut-pentakis entry (its three pentakis entries are the Catalan solid, the TI–pentakis compound and the hexapentakis TI).
Open gaps: robertlovespi.net not searched page by page; Polyhedronisme/Antiprism not run; extended web search not used.
