# Ogdoecontahedron pyrochlore networks (DICTO, 2026-10-16)

DICTO's idea: the Ogdoecontahedron (OCD) might form pyrochlore attachment networks, growing or interacting around its faces with rhombic tilings.

## Step 1: the hexagon-joined network (exact in ℚ(√5), `scripts/network.py` → `data/network.txt`)

- **Joins.** Copies join face to face on hexagons. The OCD is centrally symmetric, so a copy shifted by t = 2dn/|n|² puts its opposite hexagon exactly on the shared one; this is checked exactly for all four bonds. No rotation is needed.
- **Network.** Joining through one tetrahedral set of four hexagons (pairwise cos −1/3) gives a **diamond network**. The bond vectors satisfy |t|² = 8/9 + 8√5/27.
- **No collisions.** The exact test: copies overlap iff half their offset lies inside the OCD, since K − K = 2K for a centrally symmetric K. Over 60 sites (1,770 pairs) no copies overlap. The only contacts are the 82 full-hexagon joints.
- **Pyrochlore joints.** The four joint hexagons around every site have centres at the corners of an exact regular tetrahedron (edge² 16/27 + 16√5/81). The joints sit at the diamond bond midpoints, which form the pyrochlore lattice of corner-sharing tetrahedra.
- **Packing.** One network fills (9225 − 3915√5)/1216 = 38.72% of space.

## Step 2a: the gaps hold a second network

A second copy of the network, shifted by 2t₀ (the diamond's empty sites), fits with no overlap. It touches the first network only on hexagons (69 more full-hexagon contacts in the test). Together the two networks fill **(9225 − 3915√5)/608 = 77.43%** of space, more than the densest packing of equal spheres (74.05%). The two networks are one **body-centred cubic lattice packing**: every copy is in the same orientation, and each touches 8 neighbours through 8 of its 20 hexagons, the four tetrahedral ones plus their opposites, which point to the corners of a cube. The other 12 hexagons and all 60 kites face the remaining **22.57%** of space.

Renders (`scripts/network_render.py`, `render_network.html`, `shoot_network.mjs`): `renders/ocdnet-*.png`, orthographic along a cube axis (a two-fold axis of the OCD). They show one network, the double network (first network warm, second cool), and sheet `ocdnet-sheet.png`. The "cut" views did not slice through; fix that when rendering the gaps.

## Step 3: the gaps filled (exact, `scripts/gaps.py` → `data/gaps.txt`)

In the bcc packing each copy has a Voronoi cell V: a truncated octahedron with 24 corners and volume 512/729 + 256√5/729. The OCD lies inside V and touches V's 8 hexagons, which are the joints. Each copy's share of the gap is therefore **V − OCD = 18728/13851 − 6296√5/13851 = 0.335695 (22.57% of space)**.

Cones from the centre over the OCD's 72 free faces (12 hexagons, 60 kites) fill it with **72 convex pieces of 3 kinds**, and the pieces sum to the gap exactly (remainder 0):

| Pieces | On | Shape | Volume |
|---|---|---|---|
| 48 | kites | wedge, 6 corners: 2 triangles, 3 quadrilaterals | 0.001891 |
| 12 | kites | 11 corners: 6 quadrilaterals, 2 pentagons | 0.004409 |
| 12 | free hexagons | 13 corners: 4 triangles, 1 quadrilateral, 4 pentagons, 1 hexagon | 0.016001 |

So the OCD plus these three gap pieces tile space: 1 + 48 + 12 + 12 per lattice point. **None of the piece faces is a rhombus.** The canonical cone fill works, but it is not the rhombic tiling DICTO pictured; rhombi would need a different division of the same gap (open).

Renders: `renders/ocdgap-{closed,cut,apart}.png` (`render_gaps.html`, `shoot_gaps.mjs`). The "cut" still does not slice (same issue as step 2).

## Open
- Fusions across the cell faces: gap pieces of neighbouring cells meet on V's square and hexagon faces and may fuse into fewer, nicer pieces.
- A rhombic division of the gap, for example around the free hexagons that face each other across V's square faces.

## Step 4: a partner shape for the 12 free hexagons? (DICTO, exploratory, float, `scripts/partner.py`)

There are 3 partner sites per OCD, at the square-face centres of its cell. Each meets 4 free hexagons (2 from each OCD on that cube axis), so 3 × 4 = all 12 free hexagons. Giving each gap piece to its nearest site, each site collects 24 pieces whose volume is **exactly one third of the gap per OCD**. But the union is **not convex**: its hull is twice its volume, so the partner is a dented solid cradled between OCDs. Partners meet each other on irregular triangles and other polygons, **no rhombi** (`data/partner.txt`); they touch the OCDs on 18 face planes (quadrilaterals, pentagons, 2 hexagons).

## Step 5: twinning, turning copies into the other golden frame (DICTO: "would rotating out of their connections change the shadow shapes?"; `scripts/twin.py` → `data/twin.txt`)

A twinned copy is the OCD turned 90° about a cube axis, which puts it in the other golden frame. That turn maps the 8 joint directions onto themselves. Positions stay the same (so still 77.43%), and no arrangement collides anywhere. At a joint between a plain copy and a twinned copy, the two hexagons share plane, centre and size but are **turned 15.52° against each other**. The contact becomes a 12-gon covering **94.4%** of the hexagon, and the six slivers join the gap, so the gap shapes change.

| Arrangement | Full joints | Twisted joints |
|---|---|---|
| (a) one network, B twinned | 0 | 40 |
| (b) double network, second network twinned | 64 (within each network) | 64 (between the networks) |
| (c) bcc alternating | 0 | 128 |

In (b) the two interpenetrating networks are the two golden frames, as in the toggle.

## Step 6: octahedral or tetrahedral bridges with hexagon faces? (DICTO; `scripts/bridge_shapes.py` → `data/bridge-shapes.txt`)

- **Octahedral sites (square-face centres): yes, a closed solid.** The planes of the 8 free hexagons facing the site enclose a solid with 8 corners and 8 faces (4 triangles, 4 quadrilaterals), volume 0.021229. It collides with no OCD. Each face lies in a hexagon's plane but only partly overlaps the hexagon: the face reaches past the hexagon edge, over the kites, which slope away. Three such bridges per OCD fill **19.0%** of the gap.
- **Tetrahedral sites (cell corners): no.** The planes of the facing hexagons do not close; the region runs off to infinity.

## Step 7: hexagonal prisms as limbs (DICTO: "hexagonal prisms of different angles as limbs"; `scripts/limbs.py` → `data/limbs.txt`)

Every copy has the same orientation and is centrally symmetric. So the copy at lattice point c has a hexagon exactly parallel, opposite and equally turned to our free hexagon H (centre p): it equals H + v with v = c − 2p. Sweeping H along v gives a **hexagonal prism**. It is right only for the existing joints (v = 0) and oblique otherwise. Its side faces are parallelograms with sides s and |v|, which are rhombi only if |v| = s.

- **One limb per free hexagon.** Each free hexagon has exactly one limb that hits no other OCD. It runs to the copy across the nearest square face: length 0.522476 = 2.196 s, **tilted 79.19°** from the hexagon normal, a steeply sheared prism. Its sides are parallelograms of 0.2379 × 0.5225, **not rhombi**.
- **Limb classes.** A limb's two ends are a hexagon and the opposite hexagon of the next copy, so the 12 free hexagons give **6 limbs per copy**. These come in 3 crossing pairs, one per cube axis, crossing at the square-face centres.
- **Collision-free choice.** Choosing one limb from each pair gives **3 limbs per copy** (8 ways), using 6 of the 12 free hexagons. They fill 12.9% of the gap.
- **Competition.** The limbs pass through the octahedral sites, so they compete with the octahedral bridges of step 6 for the same space.

## Step 8: pyrochlore sharing of the conflict zones (DICTO; `scripts/conflict.py` → `data/conflict.txt`)

Keep all 6 limbs per copy and let each crossing pair **share** its conflict zone, as pyrochlore tetrahedra share corners.

- **The zone.** It is the intersection of the two crossing limbs, one at each square-face centre (3 per copy): **12 corners, 10 faces, all quadrilaterals**, volume 0.002140 (14.9% of a limb). It lies inside the octahedral bridge of step 6 but is not the same solid.
- **Golden rhombi.** **2 of its faces are golden rhombi**: angles 63.4349° and 116.5651°, diagonals in the golden ratio 1.618034. These are the faces of the rhombic triacontahedron and of the golden rhombohedra. The other 8 faces are quadrilaterals with angles 80.12°–99.88°. (Float so far; exact check pending.)
- **Filling.** All 6 limbs with each zone counted once fill 23.8% of the gap per copy.

## Step 9: golden rhombohedra grown from the conflict-zone rhombi (DICTO; `scripts/grow.py` → `data/grow.txt`)

The zone's golden-rhombus edges run exactly along five-fold axes, so the growth stays in the icosahedral frame, quasicrystal-like. The bricks are golden rhombohedra, prolate and oblate, both faced only with golden rhombi. They grew greedily outward, accepted only without overlap; the limbs were left out, with the zone standing for their crossing. From one zone, **300 bricks (152 prolate, 148 oblate)** grew before the cap, volume 0.023006. The brick edge is 0.049892, 4.77 times smaller than the hexagon edge.

## Step 10: how golden rhombi meet the non-golden faces (DICTO: "how do they meet non-golden rhombi? at an angled combination junction?")

Golden rhombohedra can only make a flat surface on golden-rhombus planes, which are perpendicular to two-fold axes. The OCD's 20 hexagons are perpendicular to three-fold axes, and its 60 kites to no symmetry axis. So bare bricks meet them in a saw-tooth front, and the slivers are small because the bricks are small (DICTO: fill with resin). By symmetry there are only two junction situations, each with a fixed angle:

- **Hexagon junction: 20.9052°**, the same to three golden-rhombus planes spaced evenly around the hexagon. The adapter is a low three-sided cap whose upper faces are golden-rhombus planes meeting over the hexagon centre: the shape of a **rhombic triacontahedron's three-fold corner**.
- **Kite junction: 11.6407°**, with two mirror choices (the next is 31.2702°). The adapter is a shallow wedge.

With these two adapter kinds the OCD's faces become golden-rhombus surfaces the bricks can sit on, much like DICTO's RVCMG adapters between families. Not yet built or checked for fit.

## Step 11: our own pieces as adapters (DICTO: "where are the AXE and CLEOs when we need them?"; `scripts/cleo_adapter.py`)

Faces in the icosahedral frame: **AXE** has two three-fold and two five-fold faces; **CLEO** one three-fold and three five-fold; **FUJI** four three-fold and three five-fold. None has a golden-rhombus plane (perpendicular to a two-fold axis). The **Cleo-Ico** has a three-fold base and three two-fold sides at 69.09° to the base, a ready-made hexagon-to-golden-rhombi adapter. One stands on each free hexagon, base on alternate corners and tip outward: all 12 have golden sides, volume 0.007630 each, 27.3% of the gap. They hit no OCD, but 12 tips meet the tips of neighbouring copies' Cleo-Icos at the square-face centres; the fix is to use alternate ones or flatten the tips. Each hexagon keeps three small corner triangles.

## Step 12: the whole library (`scripts/library_scan.py`): see the end of this file.

## Step 13: the dual Hecatodihedron as partner (DICTO: "slice up the 102-faced partner"; `scripts/heca_partner.py`, `scripts/sectors.py`)

At exactly 4/9 of its unit-sphere polar size, the Hecatodihedron wraps the OCD with **all 102 faces through OCD corners**: the 90 tangent faces through the 90 sphere corners and the 12 pentagons through the 12 outer corners. This is the dual nesting, like an icosahedron inside a dodecahedron. In the packing, each Heca reaches 0.091 past its cell and overlaps the Hecas of its 8 joined neighbours (at the joints). The shell Heca − OCD = 0.112700. The first cube-octant slicing had a bug (its sum exceeded the shell). Sliced instead by DICTO's icosahedral and dodecahedral sectors (20 cones on the hexagons, 12 on the pentagons), the sums check. But the ratios are forced by symmetry alone (dodecahedral/icosahedral sector = 5/3; the same shell share of 8.91% in every sector), so this slicing shows no resonance beyond symmetry. Untested: the OCD–Heca compound at edge-crossing scale, the true analogue of the I–D compound (ID and RT).

X-ray sections through the centre, perpendicular to a five-, three- and two-fold axis (`scripts/xray_sections.py` → `renders/xray-sections.png`): OCD gold, Heca violet, the axes lying in each cut dashed.

## Step 14: the densest lattice packing (DICTO: "maybe a Dogstar analog"; `scripts/densest.py` → `data/densest.txt`)

A copy of the OCD on a lattice is a packing iff g(Bm) ≥ 1 for every nonzero integer m, where g is the gauge of 2·OCD (80 planes). Local search in the Betke–Henk style: fix the touching pairs' faces so the constraints are linear in the basis, minimise det B by SLSQP, update, and repeat. Over 200 starts the best density is **0.789260**, found again and again, against 0.774332 for our bcc packing. It is verified as a packing over coefficients up to 4. Each copy touches **12 neighbours: 10 on hexagons, 2 on kites**. Very likely the densest lattice packing, but not proven. Whether its holes are separate (a true Dogstar analog) or one labyrinth is being tested by voxel flood fill (`scripts/holes_flood.py`). The first wall-coverage test (`holes.py`) was invalid: here the contact faces do not lie in the Voronoi walls.

## Step 15: the X-shaped holes as meeting points (DICTO: "tips or tendrils meeting each other"; `scripts/tips_meet.py`)

The small X-shaped openings in the cube-axis renders are the square-face centres. There the limbs cross (with the golden-rhombus zone), the Cleo-Ico tips collide, and four free hexagons face inward. Cut each of the four Cleo-Ico tips by the symmetric planes between the four hexagon centres. Then the tips **meet face to face in a ring, each with its two neighbours (4 shared faces)**, each keeping 84.2% (a 6-corner solid: 2 triangles, 3 quadrilaterals). The meeting faces are not rhombi.

The flood fill of the densest packing's gap (`scripts/holes_flood.py` → `data/holes-flood.txt`) finds one gap component running through the whole 2×2×2 block at both resolutions (40³ and 64³ samples per cell; the gap fraction matches, 0.2107), plus tiny specks that are grid artefacts. So the densest packing's holes form **one connected labyrinth**: no Dogstar analog in the strict sense.

## Step 16: limb crossing + tip ring, and five-fold symmetry (DICTO; `scripts/combine.py` → `data/combine.txt`)

- **The combined junction** at a square-face centre has 2 crossing limbs (0.014410 each) and 4 trimmed tips (0.006423 each). Each tip lies 37.2% inside one limb. The union is 0.042810, of which the limbs alone are 0.026679, so the tips add 0.016131.
- **Five-fold, locally.** Of the hull edges (including face diagonals), 12 of 30 in the crossing zone run along five-fold axes, 6 of 30 in a limb, and 3 of 12 in a trimmed tip.
- **Five-fold, beyond one copy.** A lattice cannot carry five-fold symmetry. Copies on all 20 hexagons of one copy (the only icosahedral hexagon joins) collide in **30 of 190 pairs**: the neighbouring hexagons, the 30 edges of the dodecahedron of hexagon directions.

## Step 17: the frog chorus (DICTO; `scripts/chorus_space.py`, `chorus_anim_data.py`, `render_chorus.html`, `shoot_chorus.mjs`)

- **The voices.** No two neighbouring positions may be occupied at once. The largest such sets of hexagon directions include the dodecahedron's **5 inscribed cubes** (8 each; any two share 2), and each gives our clean cubic packing. These are the five voices; turning 72° about a five-fold axis takes each voice to the next.
- **In time.** An animation cycles the five voices around one copy, looking down the five-fold axis: `~/Videos/dicto/dicto-frog-chorus.mp4` (10 s, kept outside the repo). Stills: `renders/chorus-voice-*.png`, `chorus-voices-sheet.png`.
- **In space** (float). Five 72° wedges around a five-fold axis each carry one voice, with all copies in the same orientation, so the whole is exactly five-fold symmetric. Plain wedges clash once per boundary near the axis (best start angle 59°). With three five-fold sets of copies removed (15 of 56 within radius 2.8), nothing collides. The silent positions lie near the axis (0.47, 0.76 and 1.89 from it), which leaves an **open five-fold channel**, as five-fold twinned crystals concentrate strain there (Ino 1969, Marks 1984). Tested only to radius 2.8. Renders: `renders/chorus-space-*.png`.

## Step 18: the Bodhi pieces as fillers (DICTO; `scripts/bodhi_fill.py`, `split_sections.py`)

- **Faces.** Every face of all five Bodhi pieces (Vajra (fine), Chatra, Mudra, Crown Jewel, Diadem) is perpendicular to a two-fold axis: they are golden zonotopes, which fit flush with golden rhombohedra and each other. None can sit on an OCD hexagon (three-fold) or kite, so the chain is OCD → Cleo-Ico → Bodhi pieces and golden rhombohedra.
- **Envelope.** The golden envelope of the OCD (the 30 golden planes pushed in until they touch it) is a **rhombic triacontahedron**, volume 1.398921. Plain envelopes of neighbouring copies collide (4 pairs per copy in the bcc packing, 6 in the densest), poking through at the joints.
- **Cut envelopes.** Cut at the 8 joint planes, they no longer overlap. The two cut faces at a joint are triangles turned 180°, forming a **six-pointed star** around the joint hexagon; its six points face the gap and lie in a three-fold plane (Cleo-Ico territory).
- **The three-way split** of the bcc packing: OCD **77.4%**, non-golden shell inside the envelopes **11.8%** (adapters or resin), golden region between envelopes **10.7%** (Bodhi pieces). Exact sections: `renders/three-way-split.png`.

## Step 12 (library scan) is still running on dicto-node.

## Step 19: cutting the golden region into Bodhi pieces (DICTO; `scripts/golden_cut.py` → `data/golden-cut.txt`)

DICTO's working name for the whole structure (OCD pyrochlore network, adapters and golden fill): **Golden Bodhi Pyrochlore**.

The golden region of one bcc cell (V minus the cut envelopes of every nearby copy) was cut by every envelope face plane crossing it, the full arrangement of golden planes, so the cut is canonical. The volume checks: 0.159887, matching V minus the cut envelope. But the cut **shatters**: 1624 pieces of 751 kinds. Only 135 pieces have purely golden walls; 996 touch the artificial cell walls, and 1083 have faces in the joint planes (the star tips). Only 6 pieces match a Bodhi shape, all **Diadems**, tiny (volume 0.000009).

So the golden region does not divide naturally into Bodhi pieces. The likely reason: the envelopes sit on a cubic lattice, so their golden planes do not line up with the golden module that makes the Bodhi Seed's pieces so simple (there, the copies sit on five-fold axes at golden distances). The cubic/five-fold tension again, as in the frog chorus. A Bodhi-clean fill would need envelope positions in the icosahedral module, such as the five-fold chorus arrangement.

## Step 20: envelopes in the five-fold chorus (DICTO; `scripts/chorus_golden.py` → `data/chorus-golden.txt`)

Each copy of the spatial five-fold chorus gets a golden envelope cut at the joints it actually has. **No envelopes overlap** around the centre. The golden region in the central copy's cell (its Voronoi cell among the chorus sites) has volume 1.078188. It is large because it includes the open five-fold channel and the silent positions. The canonical golden cut gives **30 pieces of 22 kinds** (5 purely golden-walled), against 1624 pieces of 751 kinds in the cubic packing. Among them are **2 Mudras**, a Bodhi piece. Caveat: the two regions differ in size and shape (the central cell includes the channel), so the comparison is not like for like. The cell walls are still artificial cuts. Float.

**Correction (steps 19–20).** The golden cut is not canonical as stated. It stops splitting a piece once the piece is clear of every envelope, rather than cutting by every plane, so the pieces depend on the order the planes are tried. The five-fold fill (`renders/chorus-golden-*.png`) shows this: the region is five-fold symmetric but the pieces are not. Piece counts (30 here, 1624 in the cubic packing) and the Bodhi matches are therefore indicative only. The volumes, and the much smaller number of golden planes crossing the five-fold region, still hold. A canonical cut would split by every plane: more pieces, but symmetric and order-free.

## Step 21: the canonical cut, exact (`scripts/chorus_exact.py` → `data/chorus-exact.txt`; data `chorus-exact.json` on dicto-node, 2.4 MB, not committed)

- **Exact inputs.** All 41 chorus sites snap to exact lattice points in ℚ(√5). The envelope planes, joint cuts and cell walls are exact.
- **The canonical cut.** 100 distinct envelope planes cross the central copy's cell. Splitting by every one, order-free, gives **16,204 cells**, which sum **exactly** to the cell (2440/2187 + 1288√5/2187, remainder 0). **8,027** of them are golden, with exact volume (22420 − 8972√5)/2187 = 1.078188.
- **Five-fold symmetry of the canonical golden cut: confirmed.**
- **Kinds and Bodhi pieces.** There are 561 kinds (shape up to scale); 4,221 pieces have purely golden walls. Bodhi pieces: **5 Vajras (fine)**, one five-fold orbit. The earlier "2 Mudras" and "30 pieces" were artefacts of the early-stopping cut.

**Conclusion.** Even in the five-fold arrangement, the golden region does not divide naturally into Bodhi pieces; under the canonical cut it shatters. The Golden Bodhi Pyrochlore's golden fill needs either resin or a deliberate (non-canonical) choice of Bodhi pieces. Renders: `renders/chorus-golden-exact-*.png`.

## Step 22: the spatial five-fold chorus, exact, to radius 5 (`scripts/chorus_exact_big.py 5.0` → `data/chorus-exact-big.txt`)

- **Construction.** The five wedges were rebuilt to radius 5 from exact lattice points of the five voices: 336 sites. Clashing copies were silenced in whole five-fold orbits (chosen in float): **80 silenced, 256 kept**, exactly five-fold symmetric by construction.
- **Exact packing check** in ℚ(√5): any two copies further apart than twice the circumradius cannot overlap, so checking the 620 closer pairs is complete. Result: **0 overlaps**, and all 620 close pairs touch exactly face to face (the hexagon joints).
- **Where the silences fall.** Not only near the axis: silenced copies lie at distances from 0.29 to 4.65 from the axis. The kept fraction by distance from the axis is 0.05 within 1, 0.54 within 2, 0.67 within 3 and 0.73 within 4. So the structure has a **nearly empty core** (95% silent within distance 1 of the axis) **and silences along the wedge boundaries at every radius**, like grain boundaries that carry vacancies, thinning out as the wedges widen. The open-channel picture holds for the core, but the boundaries keep needing silences too.

This is the first exactly verified five-fold arrangement in the study.

## Fable review of the five-fold chorus (2026-10-16; `FABLE-REPORT.md`, `scripts/chorus_min_silence.py` → `data/chorus-min-silence.txt`)

A bounded Fable task, with DICTO's go; checked afterwards.

- **Known relative.** The *icosahedral irrational twin*: five cubic variants related by 72° about an irrational axis, or 44.48° about [111], with no common coincidence-site lattice (Ranganathan, Srivastava & Lord 2006, J. Mater. Sci. 41(23):7696–7703, doi:10.1007/s10853-006-0966-y; abstract verified via the IISc and CSIR eprint records). Our data matches this: neighbouring voices share one three-fold axis and differ by **44.4775°** about it (rerun checked; the same angle appeared in step 5's twin test). Historical precursor: Pauling's multiply twinned cubic crystals of icosahedral clusters (1985).
- **Contrast with fcc decahedra** (Ino 1969, Marks 1984). The chorus has no angle gap and no strain; the cost of five-fold symmetry is paid in vacancies.
- **Minimal silencing** (integer program, float clash test, radius 5, start angle 59°; rerun checked). The five-fold-symmetric minimum is **16 orbits, 80 copies**, the same as the greedy run, and the minimum is not unique. Without five-fold symmetry the minimum is 72. All silenced copies lie within 0.61 of a wedge boundary half-plane (the median for all sites is 0.77).
- **Fable's hypothesis** (not yet tested). The wedge boundaries are irrational interfaces, so the vacancies should follow a quasiperiodic, golden-type pattern whose density per boundary area settles to a constant.
- **Not found in the search** as a whole construction (exact hard-body irrational twin with vacancy accounting). Absence in one search is not proof; a specialist search is needed before any public claim.
- **Top recommended test.** Grow to radius 8–10 and measure the vacancies on one boundary half-plane: their density per area, and whether their spacings come in golden ratios.

Reference library: Ino 1969, Marks 1984 and 15 more added as link-only entries (refs repo).

## Step 23: boundary vacancies to radius 10 (`scripts/chorus_exact_big.py 8.0 / 10.0`, `scripts/chorus_boundary.py` → `data/chorus-boundary.txt`; render `renders/chorus-boundary.png`, movie `dicto-chorus-boundary.mp4` outside the repo)

- **Exact packing check:**
  - **radius 8:** 1471 sites, 240 silenced (float choice, five-fold orbits); 3630 close pairs, **0 overlaps**, 3605 touching.
  - **radius 10:** 2756 sites, 385 silenced; 7465 close pairs, **0 overlaps**, 7390 touching. The few close pairs that don't touch are separated by a gap.
- **Growth:** the boundary vacancies (outside the core) grow like boundary **area**, not like a line. Within radius r the counts are 5, 20, 60, 95, 145, 205 and 275 for r = 3 to 9, with the increments rising by about 10 per unit of r. The density per boundary area (5 half-discs) is still rising: 0.31 → 0.43 from r = 5 to 9. That is consistent with settling at a constant, but the density is **not yet shown to settle**.
- **Golden spacings on the boundary: inconclusive.** All spacings are combinations a + bφ of a base length, but that follows automatically from projecting a lattice in the golden frame. Matching gap ratios to single powers of φ found only a few. The 2D boundary pattern needs a proper quasiperiodicity test (e.g. its diffraction), not a 1D gap count.

## Step 24: the core (`scripts/chorus_core.py` on the radius-8 run → `data/chorus-core-r8.txt`; heights fitted on the radius-8 and radius-10 runs)

- **Core silences come in rings of 5** (one per wedge), all at the same angle in their wedge except one ring.
- **Ring heights along the axis:** every ring height is **(m + nφ)·u** with u = 0.98979, residual below 3·10⁻⁵ (float readout of exact sites).
  - At radius 8 there are 9 rings: (−4,−2), (−2,−2), (−4,0), (−3,0), (−2,0), (−2,2), (0,2), (−2,4), (0,4).
  - Radius 10 adds (2,4) and (0,6).
- **Ring distances from the axis:**
  - 0.1785, 0.2888, 0.4673, 0.7561 step by **φ**.
  - The radius-10 run adds a ring at 0.1103 = 0.1785/φ: a larger build finds rings closer to the axis by a factor φ.
- **The silences form a 1D chain.** They grow with the length of the axis: 2.81 per unit length at radius 8, 2.75 at radius 10.
- **Reading:** this is the standard cut-and-project mechanism. The five-fold axis is irrational in every voice's lattice, so the lattice points that come close to it are exactly a 1D model set (a Fibonacci-type quasiperiodic chain), which the hardness rule silences. The core is therefore a **quasiperiodic chain of silent pentagonal rings**, not a repeating stack. This is a reading of the measured data, with heights fitted to float precision; an exact proof is not done.
- **The empty channel:**
  - Its clear radius about the axis is 0.96 on average, 1.77 at most.
  - The central copy plugs it, so the channel is **not a continuous pipe**.
  - Its outline is weakly five-fold: the spread across the five copies of each direction is 0.028, against 0.075 overall.
  - Its cross-section never repeats along the axis (no autocorrelation peaks).

## Step 25: the golden ring heights, proved exactly (`scripts/chorus_heights_exact.py` → `data/chorus-heights-exact.txt`)

All in ℚ(√5). The five-fold axis runs through an exact OCD corner v, and every height is X·v/|v|.

- **Lemma (exact).**
  - **Bonds:** each of the 20 joint vectors has height (m + nφ)·u with u² = 8/81 − 8√5/405 (u = 0.233658). The pairs (m, n) are only (±1, 0) and ±(1, 2).
  - **All sites:** every site is a whole-number combination of joint vectors, so **every copy in the chorus, at any radius, sits at a golden height (m + nφ)·u**. The unit 0.98979 used in step 24 is φ³·u.
- **Silent copies (exact).**
  - All 385 silent copies of the radius-10 run have exact golden heights.
  - The core has **11 rings, every one of exactly 5 copies**, with heights from (−8 − 14φ)u to (12 + 18φ)u.
- **Ring distances (exact squared distances, in units of the innermost ring²).**
  - **φ powers:** φ², φ⁴, φ⁶ and φ⁸, so four rings step by exactly φ, φ², φ³ and φ⁴ in distance.
  - **Golden multiples:** five others are 4φ⁴, 5φ⁴, 9φ⁴, 4φ⁶ and 5φ⁶, i.e. distances 2φ², √5φ², 3φ², 2φ³ and √5φ³.
  - **No simple form:** one ring (distance 1.0042) is (13 + 5√5)/2·φ⁴, with no simple power form.
- **What is proved:**
  - Golden heights for every copy.
  - Exact five-copy rings.
  - Exact φ-steps among the inner rings.
- **What remains a reading, not proved here:** that the silenced ones form a Fibonacci-type model set (the cut-and-project window).

## Step 26: the core is a cut-and-project set (exact); the seams diffract (float) (`scripts/chorus_modelset.py` → `data/chorus-modelset.txt`, radius-10 run)

**(1) Core, exact in ℚ(√5).**
- **One plane:** in one wedge, 10 of the 11 core rings lie **exactly in one plane through the axis**.
- **A 2D lattice:** that plane's 73 sites in the build are all whole-number combinations of two basis vectors.
- **An irrational axis:** in that basis the axis has slope α/β = −1/2 − √5/2 = **−φ**, which is irrational (the Fibonacci slope). So the projection onto the axis is injective (all heights distinct, checked).
- **The window:** the silent sites in the plane are **exactly** those whose distance across from the axis is below a window edge W, where 1.11313 < W < 1.22345. Exact edges: transverse² = 544/81 − 992√5/405 for the outermost silent site, and 64/81 + 128√5/405 for the innermost kept one. **No kept site lies inside, and no silent site outside.**
- **What this proves:** the core chain is the lattice points of a 2D lattice inside a strip along an irrational line of slope φ, which is the definition of a **Fibonacci-type cut-and-project (model) set**. It is checked over every site of the radius-10 build; the infinite statement follows from the same construction, but only the build is checked.
- **Open:**
  - **The window:** whether it equals the canonical Fibonacci window, which would make the sequence exactly the Fibonacci word, is not checked.
  - **The off-plane ring:** the 11th ring (distance 1.0042) lies off the plane and belongs to a second, separate family.

**(2) Seams, float.**
- **Not a simple strip cut:** the offset from the seam plane alone does **not** decide silence. Kept and silent copies share offsets on both sides; silence is set by two lattices meeting.
- **Diffraction:** seam 0's 66 distinct vacancies, in its plane, give a strongest peak of I/N = 46.6, against a perfect Bragg peak of 66 and **11.8 ± 2.0 for random sets of the same size**. The pattern is strongly ordered.
- **Peak positions:** the 16 strongest peaks (some are side lobes of the same peak) all lie within 0.02–0.4 of projections of the two neighbouring voices' 3D reciprocal lattices. That is within the peak width set by the build size (about 0.3), which is the signature of a lattice cut by an irrational plane (incommensurate, quasiperiodic-type order).
- **Limit:** with 66 points this cannot tell a quasiperiodic seam from a large-period approximant. Consistent with quasiperiodic, not proven.
- **Method note:** the first diffraction pass folded all five seams together. That counts each vacancy 5 times and inflates the peaks fivefold, so it was discarded.

## Step 27: the canonical window, the core is the Fibonacci chain (`scripts/chorus_canonical.py` → `data/chorus-canonical.txt`)

Exact in ℚ(√5), core plane of step 26, radius-10 run.

- **(a) Gaps.** The 11 silent heights in the plane have three distinct gaps: S, L and T. **L/S = φ exactly**, and **T = L + S exactly**, so one point is missing.
- **(b) Canonical width.** The gap vectors for L and S are (1, −1) and (1, 0) in the plane basis (determinant 1), so they form a lattice basis. Their transverse parts have opposite signs. The canonical window length is L_can² = 64/81 + 128√5/405 (L_can = 1.223451). That is **exactly** the transverse distance of the innermost *kept* copy, the upper edge of the window bracket the build allows.
- **(c) The word.** The gaps read LLSLTLSLLS. The T straddles height 0, and the missing point is the **centre copy** itself, which sits on the axis (transverse 0). Splitting T back into LS or SL gives a factor of the Fibonacci word.
- **(d) The extended chain.** With window [0, L_can), the plane lattice extended exactly to heights ±45 gives **2 gaps, L and S, and a factor of the Fibonacci word** (L:S = 33:20 over this length).
- **Agreement with the build.** Within the build's height range the chain is exactly the **11 silent copies plus the centre**. The copy lying exactly on the far window edge (t = L_can) is kept.

**Result.** The chorus's core positions, the centre copy plus the silent rings in the core plane, are exactly the **canonical Fibonacci cut-and-project chain**. It is a *singular* member: both window edges are lattice points. The centre is on the closed edge and the innermost kept copy on the open one. In words: the silencing selects exactly the canonical Fibonacci window, with the centre as one of its points. Checked over the build (radius 10); extended exactly to ±45 by construction.

- **Not shown:** *why* hardness picks the canonical window. A reasonable guess is that the copy at t = L_can just touches; that is not checked.
- **Not covered:** the off-plane ring (distance 1.0042).

## Step 28: why the window, the five-fold ring clashes with itself (`scripts/chorus_window_why.py` → `data/chorus-window-why.txt`)

Exact in ℚ(√5).

- **The mechanism.** Every core-plane copy was tested against its own four ring-mates (itself turned by 72°k). **Overlap ⇔ t < L_can**, for all 11 silent and 4 kept plane copies. So the core silences are forced by the five-fold ring clashing with itself: a copy too close to the axis cannot coexist with its own rotations.
- **The edge copy.** The copy at t = L_can does **not** touch its ring-mates; it clears them by 28/81 − 4√5/27 ≈ 0.014. The step-27 guess was wrong.
- **Critical distance.** A ring-mate pair differs by a purely transverse vector proportional to t, so there is one exact critical distance: **t_c² = 8/9 + 8√5/45 (t_c = 1.134201)**, the same for every plane copy. It lies strictly between the largest silent t (1.113132) and L_can (1.223451). **t_c ≠ L_can.**
- **Consequence.**
  - The ring-clash rule alone gives the window [0, t_c), narrower than canonical. Within the build no plane lattice point has t in [t_c, L_can), so the two windows agree, and the core equals the canonical Fibonacci chain **for |height| < 12.812**. The build reaches |height| < 10.
  - Beyond that, the ring-clash chain keeps copies the canonical chain would include: the first is at height 12.812 (t = 1.1553), then −22.71 and 34.77. There it becomes the three-gap (L, S, L+S) cut-and-project chain, a Fibonacci chain with points thinned out: still an exact quasicrystal, but not the Fibonacci word.
- **Open:** whether some other clash (not a ring-mate) silences those copies, which would restore Fibonacci. That needs a build to about radius 14, or a targeted check of the copy at height 12.81.

## Step 29: the copy at height 12.8, a tie (`scripts/chorus_h128.py` → `data/chorus-h128.txt`)

Exact in ℚ(√5) for every overlap and touch; the greedy silencing is float, as in the chorus. All sites of all five voices in a cylinder around the axis (|height − 12.812| < 7, distance from the axis < 6.16): 1135 sites.

- **The target** is the core-plane copy at height 12.8121, t = 1.1553 (plane coordinates (8, −4)). It clears all four of its ring-mates, as step 28 predicted.
- **Its neighbours.** Of the 7 copies whose centres are close enough to matter, it **overlaps exactly one**: a copy at height 13.8019, distance 1.1690 from the axis, in wedge 1. That copy is *not* in the core plane, and its own ring does **not** clash with itself, so nothing else forces it silent. The target touches 4 other copies exactly.
- **So one of two rings must go:** the target's ring or the ring at height 13.80. Either single five-fold silencing resolves the clash.
  - Silencing the **target** keeps the spine on the canonical Fibonacci chain.
  - Silencing the **13.80 ring** keeps the target, and the spine becomes the thinned (L, S, L+S) chain.
- **What the chorus's own rule does.** The greedy rule (most clashes first, ties broken by distance from the centre) silences the 13.80 ring and keeps the target. Both rings have the same clash count, so this is decided by the **tie-break**, not by the geometry.
- On the patch, the other core-plane copies near the target agree with both windows.

**Result.** Hardness alone does not decide the spine beyond height 12.8. The canonical Fibonacci chain and the thinned chain are **equally minimal** there. They differ by which of two clashing rings is silenced. The chorus's tie-break chooses the thinned chain. Fibonacci holds exactly for |height| < 12.81 and continues only under a rule that prefers silencing core-plane rings.
