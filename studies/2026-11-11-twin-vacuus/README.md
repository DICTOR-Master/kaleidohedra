# The twin Vacuus of the OG (11 Nov 2026)
DICTO: "it has perfect truncated triangles and penrose stars... what would a vacuus form of the og look like" → "do the twin vacuus".
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
