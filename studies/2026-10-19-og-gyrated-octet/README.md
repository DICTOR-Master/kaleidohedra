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

## Penrose-core (P2) middle pieces in the gyrated octet (2026-10-20, `gyr_cores.py` on dicto-node → `gyr-cores.log`; float)
Only edges lying in the twin plane change: round them the cells run O T | T O, so the OG across the edge is the mirror twin, not the octet partner.
- Lower-layer P2 pieces never cross the twin plane (0 volume), so every piece off the plane is unchanged.
- **The old P2 piece fails at a plane edge:** half of it (0.0399) lies above the plane, 0.0198 of that inside the twin OG.
- **The facing stars are gone:** the twin's five-fold corner is 0.1407 from c1 (octet partner 0.3629), with axes 105.25° apart (octet: exactly opposite, 180°). The thick-Penrose-rhombus link c1→c2 that defines the Penrose core has no counterpart there.
- **A mirror middle piece works:** Mg = hull(star + its mirror image) − both OGs: one solid, volume 0.049215 (P2 piece 0.079735), sphericity 0.520, mirror-symmetric (so not left/right), split evenly by the plane. No overlap with any of 43 neighbouring pieces or with any OG.
- So a gyrated Penrose-core kit = the P2 set + Mg at twin-plane edges; octahedra and tetrahedra touching a twin plane get different notches on that face (new boundary shapes, not yet computed).

## Exact round-up for the companion paper (2026-10-20, dicto-node)
**OCD Stella (`stella_twin_exact.py` → `stella-twin.log`, 9 PASS).** Built exactly with the pyrochlore study's script, whose bcc lattice sits in a golden orientation; turned into the #37 frame by the lattice's own cube axes (the rotation carries that study's OCD exactly onto the #37 OG). Then: the Stella lies in the octahedron; each face holds its equilateral joint triangle (side² 8/3 − 8√5/9); share of the octahedron (604 − 267√5)/9 ≈ 77.44%; joint triangle = (7 − 3√5) ≈ 29.18% of a face; mirror twin = the Stella turned 60° (spinel law, as the OG); twins meet on the whole triangle. (A first exact run in the wrong frame failed; the 10-19 float numbers stand.)
**`gyr_exact.py` → `gyr-exact.log` (9 PASS):**
- Joint hexagon regular, side² 2/9 − 2√5/27; hexagon = (7 − 3√5)/2 ≈ 14.59% of a face, so a cap meets its twin across (3√5 − 5)/2 ≈ 85.41% of the face. (The Stella's joint triangle is exactly twice the OG's joint hexagon.)
- OG (−1000 + 1240√5)/1539 ≈ 1.151868 (68.83%); twin cap = a left cap + its mirror, a right cap = (554 − 158√5)/1539 ≈ 0.130410; tetrahedron (16 + 8√5)/81; bipyramid (32 + 16√5)/81 ≈ 0.836754.
- Mirror middle piece Mg exact: hull of a star and its mirror (2 + 2√5)/81, meets each OG in (−155 + 101√5)/4617; **Mg = (424 − 88√5)/4617 ≈ 0.049215** (matches the float run).
- **DBT in the gyrated octet:** its mirror in a pole face = the DBT turned 60° (true twin); it lies between its two twin planes; with a DBT in every octahedron (layer by translation, the layers above and below as mirror images), **no DBT overlaps the central one** (18 + 19 + 19 neighbours, exact separating planes).

## Penrose-core boundary pieces at twin planes (2026-10-20, `gyr_boundary.py` on dicto-node → `gyr-boundary.log`; float)
The #37 keyless Penrose-core kit (OG, 6 vertex caps per octahedron, a middle piece on every edge, tetrahedra; caps and tetrahedra notched by the middle pieces), with each edge's middle piece = hull of the two OGs' nearest five-fold stars minus both OGs. Run for the octet, a single twin plane and the gyrated octet.
- Octet (sanity): notched cap 0.058072, notched tetrahedron 0.265776, middle piece 0.079735, as #37.
- At a twin plane only three shapes change: **middle piece Mg 0.049215** (in place of 0.079735; no Penrose cores), **boundary cap 0.055477** (a cap whose vertex lies on a twin plane; sphericity 0.579 vs 0.587), **boundary tetrahedron 0.319340** (a tetrahedron with its face on a twin plane; sphericity 0.587 vs 0.517; left and right hands as before).
- A piece only feels the one layer plane it touches: with a single twin plane the 3 caps on that side are boundary caps and the other 3 octet caps; the 3 tetrahedra with a face there are boundary tetrahedra, the others octet. So **any stacking uses the octet kit plus these three shapes.**
- Gyrated octet: every cap and every tetrahedron is a boundary piece (6 caps congruent, 3 + 3 mirror images; tetrahedra 3 + 3 mirror images); per cell 3 middle pieces M0 (with their Penrose cores) and 3 Mg. Origin octahedron: OG + 6 caps + middle pieces inside = 1.673508 = octahedron. Per cell 1.151868 + 6(0.055477) + 3(0.079735) + 3(0.049215) + 2(0.319340) = 2.510263 = cell.
- Middle pieces reach at most 0.5542 from their edge midpoints. To make exact.
**Exact (`gyr_boundary_exact.py` on dicto-node → `gyr-boundary-exact.log`, `gyr-boundary-exact.json`; 17 PASS, 0 FAIL).** By convex pieces in ℚ(√5), for the octet, a single twin plane and the gyrated octet:
- Middle pieces: M0 = (310 + 26√5)/4617, Mg = (424 − 88√5)/4617; near the origin octahedron no two overlap and none enters a third OG (exact).
- **Boundary cap 23/162 − 47√5/1215 ≈ 0.055477** (octet cap (32 − 8√5)/243 minus (−25 + 14√5)/2430 ≈ 0.002595).
- **Boundary tetrahedron 41/162 + 4√5/135 ≈ 0.319340** (octet keyless tetrahedron (26 − 2√5)/81 plus (−55 + 44√5)/810 ≈ 0.053564).
- Octet run gives #37's cap and keyless tetrahedron; single twin plane: exactly the 3 caps and 3 tetrahedra on the plane are boundary pieces; gyrated: all 6 caps and all 6 tetrahedra are; origin octahedron and one gyrated cell sum exactly.
- (Congruence of equal-volume pieces and their hands: float overlap test, `gyr_boundary.py`.)

## The DBT's spaces, and growing it (DICTO 2026-10-20: "volume is very low", option 1; float, `dbt_spaces.py`, `dbt_grow.py` on dicto-node)
- In its octahedron the DBT touches each of the 12 edges at one golden point (1/φ² of the way along), leaving 6 separate corner spaces of (112 − 48√5)/81 ≈ 0.0576 each, sphericity 0.33.
- Option 1: the DBT's rhombic triacontahedron scaled by s about the OG centre, cut by the bisector planes to its neighbours (the twin planes stay the pole cuts). It meets 8 neighbours (2 across the twin planes, 6 in its layer). Share of space: s 1.00 55.0% · 1.04 61.1% · 1.08 67.1% · 1.12 72.9% · 1.16 78.4% · 1.20 83.4% · 1.25 88.9% · 1.30 93.0% · about 1.6 → 100% (the solid becomes the whole cell). All 30 rhombus planes survive up to s ≈ 1.16; 24 at 1.2.
- **But the leftover gets thinner, not chunkier:** it is one thin skin between the grown solids. Its sphericity per cell falls from 0.33 (s = 1) to 0.28 (1.08), 0.22 (1.16), 0.17 (1.25), 0.10 (1.30), and above 1.32 it breaks into slivers. So option 1 raises the share but gives no buildable leftover pieces.
- DICTO 2026-10-20: **keep the DBT as it is** (option 1 dropped). Also noted: the RT has 20 identical cut sites (its three-fold corners); 8 point through the octahedron faces (the keys), the DBT cuts 2; cutting all 8 gives (−608 + 320√5)/81 ≈ 1.3277 (52.9%) inside the octahedron, all 20 the icosahedron of the five-fold corners (reasoned, not yet checked).

## Filling the DBT's space (DICTO 2026-10-20 "keep filling the space"; `dbt_fill.py` on dicto-node, float)
As #37 step 27: every leftover point goes to its nearest site; piece = the site's Voronoi region minus the DBTs.
- **Tetrahedron centres (2 per cell):** each piece one solid, 0.564576 (= leftover / 2), sphericity 0.509, not mirror-symmetric.
- **Bipyramid centres (the twin-plane face centres, 1 per cell): each piece one solid, 1.129153 = the whole leftover of a cell ((976 − 432√5)/81), sphericity 0.586, mirror-symmetric in its twin plane.** So the gyrated DBT kit could be **DBT + one grown-bipyramid piece: 2 shapes.** 71 faces (flat Voronoi cuts plus the DBT's golden faces; some small, smallest ≈ 0.0023). Quick render `renders/dbt-fill-bip.png`.
- Open: congruence of the pieces at all sites (same volume and sphericity at 4 sites), thin edges, exact proof, a proper 3D view.

## The DICTO Octahedrally Truncated Triacontahedron (DICTO OTT; named by DICTO 2026-10-20): the triacontahedron cut at all 8 key sites (kept alongside the DBT)
**Exact (`cut8_exact.py` → `cut8-exact.log`, `cut8-exact.json`; 13 PASS):** RT ∩ octahedron. 24 corners, all corners of the RT (no new corners); 38 faces = 6 whole rhombi + 24 half-rhombi + 8 equilateral triangles on the octahedron faces (side² 8/3 − 8√5/9, the DBT's pole triangle); 60 edges. Volume (−608 + 320√5)/81 ≈ 1.327676 = RT − 8 keys = DBT − its 6 keys. Symmetry Th (the OG's), not Oh. The OG lies inside. Share 176/3 − 26√5 ≈ 52.89%. Leaves 6 corner spaces (112 − 48√5)/81 and whole tetrahedra: (704 − 272√5)/81 ≈ 1.182587 per cell. It lies inside its octahedron, so it works in every stacking.
**Fill (float, `dbt_fill.py cut8 …` → `fill-compare.log`):** gyrated, nearest bipyramid: one solid per cell, 1.182587, sphericity 0.612, mirror-symmetric (DBT: 0.586); gyrated, nearest tetrahedron 0.591293, 0.530 (DBT 0.509); octet, nearest tetrahedron (step-27 cubes) 0.591293, 0.638.
**Size (float, `cut8_size.py` → `cut8-size.log`; DICTO "size … ideal?"):** RT scaled by s, cut by the octahedron.
- s = φ²/3 ≈ 0.873: the 8 keys just touch the faces (no cut). s = 1: the 12 five-fold corners lie exactly on the 12 octahedron edges and the cuts run along long diagonals (no new corners).
- 1 < s < φ²/√5 ≈ 1.1708: deeper cuts make 60 corners, 48 of them new. At s = φ²/√5 the 12 other three-fold corners reach the octahedron faces (62.44%); above it the solid is the octahedron with its 6 corners cut by rhombus planes (corner spaces = 6 pyramids). s = φ: the whole octahedron (66.67%).
- Fill sphericity, gyrated / octet: s 1.00 0.612 / 0.638 · 1.10 0.602 / 0.619 · 1.17 0.522 / 0.622 · 1.25 0.537 / 0.631 · 1.40 0.501 / 0.652 · φ (plain octahedron) – / 0.671.
**3D page (2026-10-20):** `kits_page_data.py` (dicto-node) → `renders/kits-data.json`; `kits_page_template.html` → `renders/dbt-8cut-kits.html`, claude.ai/artifact/Eo6sAjAc3btvK1LvhAEaMy. DBT kit (gyrated), 8-cut kit (gyrated, octet): set and cluster (solid + the 6 / 6 / 8 fill pieces touching it), pull apart.
**Prior art check (2026-10-20):** library: Kabai's 54-faced space-filler (RT minus 8 half oblate rhombohedra, bcc), Kabai's RT clusters, a dimpled RT (rhombohedra removed at 4 corners) — all remove whole or half rhombohedra, none cuts flat at the key sites. Web: truncated RTs found cut the 12 five-fold corners (42 faces, Ih); a list of convex golden-rhombus polyhedra (orchidpalms) has only band-reduced and expanded RTs. No source found for the RT cut at 2 (D3d) or 8 (Th) three-fold corners, i.e. the RT cut by an octahedron.
