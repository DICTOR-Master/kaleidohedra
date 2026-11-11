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
