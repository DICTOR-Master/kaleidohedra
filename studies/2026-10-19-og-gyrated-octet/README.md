# The OG in the gyrated octet (DICTO 2026-10-19; first exact check, `check.py`, ℚ(√5))

DICTO's question: can the OG live in the gyrated octet (the tetrahedron–octahedron honeycomb stacked A B A B, the hcp twin of the octet) as well as in the octet (#37)?

- **Yes, every octahedron takes an OG**, exactly as in #37 (the 8 joint hexagons on the 8 faces of |x|+|y|+|z| = 2φ/3). OGs can't overlap, because the octahedra don't.
- **At a gyrated layer two octahedra share a face, and their OGs meet on exactly the same joint hexagon** (the same 6 corners, exactly).
- **The neighbour is a true mirror twin, not a translate.** In the bcc packing and in the octet every OG is a translate of the others; here the OG beyond the gyrated layer is the OG's mirror image in the shared face, and this mirror is *not* a symmetry of the OG (the OG has no mirror plane at right angles to a three-fold axis). **So the gyrated layers are twin boundaries of OGs**, the hcp stacking fault of the OG octet.
- **Round the hexagon:** each of its 6 edges opens into a wedge-shaped gap between the twins. The faces beside the hexagon tilt about 23.8° from the joint plane, so the gap's opening is 2 × 23.8 ≈ 47.6°; exactly, cos(the angle between a face and its mirror) = (7 − 36√5)/109.

**The twin, exactly (`twin.py`):** the mirror OG is **the OG turned 60° about the shared three-fold axis** (through the joint hexagon), checked exactly with the rational rotation about (1,1,1). It is not a 90° turn or the inverse. This is the classical twin of crystallography (the spinel law), the same 60° turn that changes fcc stacking into hcp. It differs from the chorus study's icosahedral twin, which turned 44.48° about a shared three-fold axis.

**One kit for both lattices (`kit.py`, exact):** cut each octahedron into the OG plus 8 caps (the octahedron minus the OG, one cap under each face, cut by the planes through the centre and the octahedron's edges), and keep each tetrahedron whole. No piece crosses a cell face, so **the same kit fills the octet and the gyrated octet, and any stacking in between**, with the same density (the OG fills 68.83% of its octahedron).
- Each cap: (octahedron − OG)/8 = **(277 − 79√5)/1539 ≈ 0.065205**.
- All 8 faces carry a joint hexagon, and the OG's symmetry inside the octahedron (pyritohedral: three-fold turns, half-turns, inversion) moves any face to any other.
- **The caps are chiral, exact (`hand.py`):** of the 18 OG corners in a face's cone, the three-fold turn maps them onto themselves, but none of the three mirrors through the face's axis does. So the caps come in **left and right hands, 4 + 4 per OG**: faces (1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1) one hand, the other four the other.
- At a twin boundary a cap meets its own mirror image across the hexagon, and the two could be fused into one symmetric "twin cap" piece. The paired tetrahedra form triangular bipyramids.

**Next (DICTO: tomorrow, jumping the queue):** pieces for these twin wedges and for the paired tetrahedra (triangular bipyramids); adapt #37's kits; check against the chorus study's icosahedral twin.

**DICTO 2026-10-19: "this is another paper!"** It would be the companion to #37 (the OG on the octet truss → the OG on the gyrated octet, twinned). Prior art to read first: crystal twinning (the spinel law), the gyrated tetrahedral-octahedral honeycomb, and the chorus study's icosahedral twin.

## A family trait? (DICTO 2026-10-19, float first look)
- **Golden envelope (RT):** does **not** fit as it is. Its three-fold corners poke 0.0909 beyond each octahedron face. Across a twin layer each key runs into the twin's envelope, overlapping it by ≈ 0.0175 per shared face. It would need trimming flat on twin faces, or interlocking keys.
- **OCD Stella (#31a):** **fits.** Its 8 joint faces lie exactly on the octahedron's 8 faces (the bcc hexagon walls, distance 0.622782; normals on the cube's diagonals), so it sits inside every octahedron. It fills 1.296011 / 1.673508 = **77.44%** of the octahedron (the OG 68.83%).
- The Stella's joint face is an equilateral **triangle** (circumradius 0.47576, 29.18% of the octahedron face). Twin Stellas meet on the whole joint triangle (a mirror in the joint plane leaves it in place), with the same 60° twin as the OGs.
- So: **the OG and its OCD Stella twin freely in the octet and the gyrated octet; the golden envelope only if trimmed.**

To make exact.

## The DICTO Jewel (DICTO 2026-10-19, float Monte Carlo, `jewel_twin.py`)
Stella–Jewel Lattice (Jewels on the even cells, an fcc of Jewels; stella octangulas on the odd cells), twinned in a (111) layer of Jewels (keep x+y+z ≥ 0, mirror the rest: …C B A B C…).
- Baseline (no twin): all 44 218 sample points within 2 of the plane covered exactly once, which validates the test (ray parity; the Jewel's volume comes out 12.03, exact 12).
- Twinned: **4.0% of the points are gaps and 4.2% overlaps**, all within about 1.6 of the plane. **The Jewel does not twin freely.**
- Why: the Jewel and the stella are framed by **cubes**, and a cube mirrored in a plane across its body diagonal is a different cube (that mirror is not a symmetry of the cube). An octahedron mirrored in its face is just the next octahedron of the gyrated octet, which is why the OG and the OCD Stella twin and the Jewel does not. The (111) layers alternate Jewels and stellas, so a twin through a stella layer meets the same obstacle.
- With the stellas paired in (they fill the odd cells throughout), other twin planes fail too (`jewel_twin_planes.py`): through a stella layer (x+y+z = 2) 5.1% gaps and 5.9% overlaps; between layers (x+y+z = 1 or 3) 18–19% gaps or overlaps.

## The belted envelope as a shape of its own (DICTO 2026-10-19, float, `belted.py`)
The golden envelope (rhombic triacontahedron round the OG, #37 frame) cut flat by the octahedron's two faces on one three-fold axis.
- **The cut runs exactly through the pole corner's three five-fold neighbours** (fraction 1.000000 of each edge): it takes off the corner pyramid on the three long diagonals. The 3 rhombi round each pole become half-rhombus triangles, and the pole is an equilateral triangle whose sides are the rhombi's long diagonals (0.824045; envelope edge 0.484362).
- **30 corners, 32 faces (24 golden rhombi + 6 half-rhombi + 2 equilateral pole triangles), 60 edges**; Euler 2. Symmetry D3d (the three-fold axis with the centre of symmetry).
- Volume **1.38111** = envelope 1.398921 − 2 keys (0.017811; the step-3 key (−44 + 20√5)/81 each). Sphericity 0.959; pole to pole 1.245563, width 1.539601.
- It holds the OG (the OG lies inside the octahedron) and sits in every octahedron of the gyrated octet: flat on the twin faces, keyed on the six side faces.
- To make exact; name to propose to DICTO.

## DBT exact (2026-10-20, `dbt_exact.py` on dicto-node → `dbt-exact.log`, `dbt-exact.json`; 18 PASS, 0 FAIL)
The DICTO Belted Triacontahedron is a rhombic triacontahedron (inradius 2/3, #37 frame) truncated at its two three-fold corners on (1,1,1). It began as the golden envelope round the OG; from here it is named as a solid of its own.
- No new corners: it keeps 30 of the RT's 32 corners and loses only the two pole corners. 60 edges, 32 faces: 24 rhombi, 6 half-rhombi, 2 equilateral pole triangles (side² = 8/3 − 8√5/9, side 0.824045).
- Each cut runs along a rhombus's LONG diagonal (diagonal ratio² = φ²).
- Volume (−872 + 440√5)/81 = 1.381110; RT (−320 + 160√5)/27 = 1.398921; each removed corner (−44 + 20√5)/81 = 0.008906 = exactly 1/6 of the oblate golden rhombohedron on the pole's three edges ((−88 + 40√5)/27).
- Symmetry D3d (order 12): three-fold turn, inversion, half-turns about the 3 golden two-fold axes perpendicular to (1,1,1).
- The OG lies inside; 36 of its corners touch the DBT's surface.
- Float only: surface 6.253707, sphericity 0.9590.
