# Universal PiTet: growing outward from the Cleo star (2026-10-19)

**Name (DICTO 2026-10-19): "Universal PiTet"**, after the triangles and pyramids that stay constant. DICTO: "even if pyramids don't hold, Pi does": the shells are a spherical progression (π) and the triangles stay throughout (Tet). The working name was "five-fold octet"; the folder keeps that name. Whether the name is already in use has not been checked yet.

DICTO's idea: build outward from the Cleo star in **spherical shells with the same pattern each time and different solids each time**. Multi-sided **Vajras** would take the place of the octet's octahedra, alongside different kinds of FUJI and CLEO, and some pieces may appear twice. This is a different construction from the Spheres of Dharma, even where it passes through the same solids. This came out of the play-first brainstorm (OG-13, spherical octet, ID channel).

**All numbers here are float checks** (`progression.py`, results in `data/progression.json`). No exact proof has been done yet.

Frame: an icosahedron of edge 1, with the five-fold axes through its corners. Every solid is built in this frame and checked against it.

**Known case:** D′ (radius φ²/√3) matches the app's Cleo star hull, `theaetetus-data.js`, view `cleostar`; the app data has 6 decimals.

## Names (DICTO 2026-10-19)

- **DICTO GTI**, Golden Truncated Icosahedron: the icosahedron cut at 1/(2+φ) of each edge (rather than 1/3), giving 12 regular pentagons and 20 hexagons with sides alternating 1 : φ.
- **DICTO FPD**, Flat Pentakis Dodecahedron: the polar dual of the GTI, a dodecahedron with low five-sided pyramids, flatter than the Catalan one.
- **Monkey Staff B** (DICTO): the twisted frustum of stage 2 (D′ → ID), named after Dharma's Monkey Staff, a twisted pentagonal frustum of other proportions.
- The cycle: **ID → RT → DICTO GTI → DICTO FPD → ID × 10/φ⁴**. Below, "golden truncated icosahedron" = GTI and "Q" = FPD.

## Progression so far

| Stage | Next solid (tightest round the last) | Pieces filling the gap | Check |
|---|---|---|---|
| 0 | icosahedron = 20 Cleo-Icos | — | app |
| 1 | Cleo star → D′ | 20 Cleo spikes, 12 inward pyramids, 30 valley tetrahedra | app (Theaetetus, Cleo star view) |
| 2 | D′ → icosidodecahedron | **12 five-sided twisted pieces, one kind** (D′ pentagon below, the ID's pentagon above turned 36°, 10 triangles round the side) | sum = gap |
| 3 | ID → rhombic triacontahedron | 12 five-sided pyramids, 20 three-sided pyramids, **60 valley tetrahedra (one kind, one per ID edge)** | sum = gap |

- **Stage 2, the points meet at the dodecahedron's corners:** every D′ corner sits exactly at the centre of an ID triangle. Each ID triangle is made of three side triangles, one from each of three pieces, meeting at that corner.
- **Stage 3:** the ID's 30 corners sit on the RT's 30 face planes.
- **Corner radii (float):**

  | Solid | Radius |
  |---|---|
  | I | 0.95106 |
  | D′ | φ²/√3 |
  | ID | **φ** |
  | RT five-fold corners | **exactly twice the icosahedron's** |
  | RT three-fold corners | **√3** |

## The five-sided Vajra (DICTO: "multiple sided Vajras instead of octahedrons")

Three pieces line up along each five-fold axis:
- the Cleo star's inward pyramid, tip at an icosahedron corner;
- the stage 2 twisted piece;
- the stage 3 five-sided pyramid, tip at an RT corner.

Together they form **one convex piece**: the volume of their hull equals the sum of the three parts, 0.819824. That makes 12 double-pointed, five-sided Vajras with a 36° twist at the waist, reaching from radius 0.951 to 1.902. Along the three-fold axes the Cleo spike and the three-sided pyramid touch only at the D′ corner, a single point, so the three-fold column pinches there.

## Pure hexagonal Cleos (DICTO)

The **tightest OG round the ID** has its 20 regular hexagons **exactly in the ID's triangle planes**. That puts each D′ corner at the centre of an OG hexagon, and the OG fits inside the RT (scale 3φ/2 against `ocd-vertices.json`, the vertices from `studies/2026-10-16-ocd-pyrochlore/data/network.json`). So **ID ⊂ OG ⊂ RT**, and the pinch on the three-fold axis can become a regular-hexagon waist, the place for pure hexagonal Cleos. The pieces for this are not computed yet.

## Stage 3 through the OG: pure hexagonal Cleos (`hexstage.py`, `data/hexstage.json`, float)

At this size, 30 of the OG's corners **are** the ID's corners, its other 60 corners lie on the same sphere (radius φ), and the 12 apexes stand further out. Each regular hexagon (side 1/√3) is an ID triangle (edge 1) plus three small flat triangles.

| Shell | Pieces | Check |
|---|---|---|
| ID → OG | **12 of one kind**: the ID's pentagon below; on top, 5 kites and 5 small hexagon triangles of the OG; neighbours touch only along edges | sum = gap |
| OG → RT | **20 pure hexagonal Cleos** (regular hexagon base, apex at the RT's three-fold corner √3, height 0.2205), **12 five-fold caps** (dimpled: the OG apex pokes in), **120 tetrahedra, one volume** | sum = gap; 23,848 random points each in exactly one piece |

- **Five-fold column:** each ID → OG piece fills the dimple of its cap exactly, so together they make one convex piece (hull of the ID pentagon, 5 OG corners and the RT corner).
- **Three-fold column:** the D′ corner is exactly at the hexagon's centre, so the Cleo spike still meets the hexagonal Cleo at one point. **No six-waisted Vajra forms from these pieces**; the hexagon sits on top of the pinch.
- **Triangles:** every face between pieces here is still a triangle. The 120 tetrahedra may be mirror pairs (not yet checked).

## Stage 4: RT → a transitional golden truncated icosahedron (`stage4.py`, `data/stage4.json`, float)

DICTO: "keep going outwards, but there may be missing transitional solids." The next solid has its faces through the RT's 32 corners, at right angles to their axes, so the points meet again. It is a **truncated icosahedron that is not regular**: 12 regular pentagons and 20 hexagons whose sides alternate between 0.5279 and 0.8541, a ratio of **φ**, all 60 corners at radius 1.9544. It sits between the icosahedron and the regular truncated icosahedron, a transitional solid (prior art not checked).

- **Fill:** **30 identical convex pieces, one per RT rhombus**, each of volume **1/(2φ²)**. They add up to the gap.
- **Each piece:** the rhombus below; on top, 2 quadrilaterals (in the pentagon planes) and 2 pentagons (in the hexagon planes).
- **Walls:** every wall between neighbouring pieces is a **triangle** (120 of 120), so the triangle constant holds.
- **What comes next (not yet filled):** the same rule applied to its 60 corners gives a **pentakis-dodecahedron-type solid**: 60 triangles, the 12 five-fold corners at 2.0081, the 20 three-fold corners at 2.2053. That is the family the OG comes from (the OG is a pentakis dodecahedron with its 20 six-fold corners cut flat), so the OG family may come back here.

## Stage 5: golden truncated icosahedron → Q, a pentakis-dodecahedron type (`stage5.py`, `data/stage5.json`, float)

- **Q:** 60 triangles. Each Q face holds exactly one corner of the golden truncated icosahedron, so the points meet again. Five-fold corners at 2.0081, three-fold corners at 2.2053.
- **Fill:** 12 pieces on the pentagons (each 0.02290) and 20 on the hexagons (each 0.41122), one kind each; they add up to the gap. Every wall between pieces is a triangle (180 of 180).
- **Does the OG come back? Not exactly.** Q has the OG's parent shape type (a pentakis dodecahedron) but different proportions: three-fold to five-fold radius 1.0982 here, 1.0265 for the OG's parent. So cutting Q's six-fold corners flat gives an OG relative, not the OG.
- **Rhythm (DICTO's idea, first sign):** Q's three-fold / five-fold radius ratio **equals the RT's five-fold / three-fold ratio** (1.0982). On the RT the five-fold corners lead; on Q the three-fold corners lead by the same proportion. The two columns take turns, a rhythm of their own.

## Stage 6: Q → the ICOSIDODECAHEDRON again: a four-stage cycle (`stepper.py`, `cyclecheck.py`, `data/stage6on.*`, `data/cycle.json`, float)

- **Stage 6:** Q → a regular icosidodecahedron, filled by 60 identical pieces (one on each Q triangle). Walls all triangles (180 of 180).
- **The ID comes back, 10/φ⁴ = 1.45898 times larger** (float match to 10⁻¹⁴), and stage 7 gives the RT again at the same scale. So from the ID onward, **the UP repeats in a cycle of four: ID → RT → golden truncated icosahedron → Q → ID × 10/φ⁴**, outward without end (inward too, if the rule runs in reverse).
- **The step rule:** each next solid has its faces through the last one's corners at right angles to them; one piece per face of the last solid. Stages 1–2 were built by a different rule, "tightest round the last": that rule applied to D′ would give an icosahedron, not the ID.
- **Rhythm:** within each cycle the five-fold and three-fold columns take turns leading (RT and Q have mirrored ratios, 1.0982).
- **Re-checks:** stages 2 and 3 were also tested by random points: 37,268 and 54,650 points, each in exactly one piece.

## EXACT: the cycle is proved (`exact_cycle.py`, `data/exact_cycle.json`)

Exact arithmetic in ℚ(√5) (Fractions, exact signs). Start: the icosidodecahedron of radius φ in standard coordinates. The step rule needs no square roots: the face through corner v is v·x = v·v. Float is used only to guess which three faces meet at a corner; every guess is then proved exactly:

1. each corner solves its faces exactly and lies inside every face;
2. every listed face holds at least 3 corners, with all others inside it;
3. the faces close up (every edge in exactly two faces, Euler V − E + F = 2), so the corner list is complete.

| Step | Corners | Faces | Edges |
|---|---|---|---|
| ID → RT | 32 | 30 | 60 |
| → golden truncated icosahedron | 60 | 32 | 90 |
| → Q | 32 | 60 | 90 |
| → ID | 30 | 32 | 60 |

**The final ID equals the first exactly, scaled by 10/φ⁴ = 35 − 15√5.** Because the rule commutes with scaling, **the UP cycle repeats forever, outward**, with the same four shells of pieces each turn, 10/φ⁴ larger. Still float: the piece fills inside each shell (exact proofs of those are next), and stages 1–2 below the cycle.

## EXACT: the pieces of the four shells (`exact_shells.py`, `data/exact_shells.json`)

The exact solids of `exact_cycle.py` (ID radius φ, the same size as in this study). Pieces = one per face of the inner solid (the cone from the centre over that face, cut by the outer solid). These partition the gap by construction. Checked exactly: every corner of every piece, exact volumes, sum = gap, and **all faces of each kind form one symmetry orbit** under the 60 exact rotations, so every piece of a kind is congruent.

| Shell | Pieces (exact volume each) | Sum = gap |
|---|---|---|
| ID → RT | 12 on pentagons (5/12), 20 on triangles (3/8 − 17√5/120) | exact |
| RT → golden TI | 30 on rhombi ((3 − √5)/4 = 1/(2φ²)) | exact |
| golden TI → Q | 12 on pentagons, 20 on hexagons | exact |
| Q → ID × 10/φ⁴ | 60 on triangles | exact |

The stage-3 cut used for the Vajra (12 + 20 pyramids + 60 valley tetrahedra, 92 pieces) is also exact: the volumes sum to the gap and every piece lies inside the RT. Its no-overlap is shown only by the float random-point test.

**So from the ID outward the UP is exact all the way:** the solids, the cycle and the shell pieces. Still float: stages 1–2 (Cleo star → D′ → ID), the OG / hexagonal-Cleo split, and the Vajra's convexity.

## EXACT: all the way in (`exact_inner.py`, `data/exact_inner.json`)

ℚ(√5), with the icosahedron of edge 1 in the standard frame and the ID as twice its edge midpoints (radius φ). Each set of pieces is checked exactly for: exact volumes, sum = gap, every piece inside the outer solid and outside the inner one, and **no overlap** (for every close pair, a face plane of one has the other wholly on its far side). Volume sum plus no overlap means the pieces fill the gap with no hole.

| Shell | Pieces | Exact |
|---|---|---|
| Cleo star → D′ | 20 Cleo-Icos + 20 spikes + 12 inward pyramids + 30 valley tetrahedra (82) | fill, no overlap |
| D′ → ID | 12 twisted frusta, each 145/648 + 37√5/648; every D′ corner is an ID triangle centre | fill, no overlap |
| ID → RT (fine cut) | 12 + 20 pyramids + 60 valley tetrahedra (92) | fill, no overlap |
| ID → OG | 12 pieces | fill, no overlap |
| OG → RT | 20 hexagonal Cleos (1/4 − √5/12 each) + 12 dimpled caps (5/76 + 5√5/684) + 120 tetrahedra (1/24 − √5/72) | fill, no overlap |

- **The OG at this size, exactly:** its corners are the 30 ID corners, plus 2c − v for each corner v of each ID triangle (c the triangle's centre), plus 12 apexes on the kite planes. That gives 102 corners and 60 kites + 20 hexagons, matching the study's OG data to 4×10⁻¹⁶.
- **The five-sided Vajra is convex exactly:** inward pyramid + twisted frustum + outward pyramid = their hull, volume 55/108 + 5√5/36.
- **The dimpled cap + its ID → OG piece = their hull, exactly.**

**So the whole UP is now exact, from the 20 Cleo-Icos out through the endless cycle.** Note: `exact_cycle.py` starts from the mirror-image frame of the same ID; the cycle is the same in either.

## Triangles as the constant (DICTO 2026-10-19)

DICTO: "triangles are the only true constant in the universal octet". This holds for every stage built so far. Inside each shell, every face where two pieces meet is a triangle. Pentagons, hexagons and rhombi appear only on the shell surfaces (D′, ID, OG, RT). Read this way, the triangle is the invariant and the shell polygon is the variable, which fits both the flat octet and the 600-cell, where everything is triangles. This has been checked only on stages 1–3.

## Reverse cycle (DICTO 2026-10-19, float first look)

The reverse step takes as new corners the foot points of the last solid's faces (the point of each face plane nearest the centre). It undoes the forward step exactly, so **the UP cycle run in reverse just retraces itself**: RT → ID → Q/k → … inward without end, with no new solids. Starting from other seeds gives more:
- **D′:** forward and reverse alternate between the dodecahedron and the icosahedron (plain duality, nothing new).
- **The OG:** **no cycle within 5 steps.** Forward: 92 corners with 90 four-sided faces (a rhombic-enneacontahedron type, to check) → 180 → 212 → 270 → 452 corners. Reverse: 80 corners (120 triangles + 12 pentagons) → 132 → 140 → 162. The solids get more and more complex instead of closing. These are candidate "new duals" of the OG, to be studied.

## Polar reciprocation (DICTO 2026-10-19, float)

**The four UP stations are two true polar pairs: ID ↔ RT and golden truncated icosahedron ↔ Q** (each solid's polar reciprocal has the other's shape). The ID and the golden TI have all their corners on one sphere, so the UP step from them **is** polar reciprocation. The RT and Q have corners at two radii, so the UP step from them is **not** polar: it carries the RT on to the golden TI and Q on to the ID. **So the cycle alternates: polar, non-polar, polar, non-polar**, and the non-polar steps are what join the two classical dual pairs into one cycle and set the scale 10/φ⁴. The polar of the OG has 80 corners and 102 faces (60 triangles, 30 quadrilaterals, 12 pentagons), the Hecatodihedron type, as known.

## The polar cycle: UP is its own polar (DICTO 2026-10-19; EXACT, `exact_polar.py`, radius² 15 − 5√5)

Reciprocating the whole UP chain gives **the UP chain again**: no new solids, the same four in the same cyclic order, each step again following the UP rule with all corners on the next solid's faces. **The mirror is the DICTO GTI's circumsphere (radius √10/φ = 1.95440).** Reciprocation about it swaps **GTI ↔ FPD**, **RT ↔ ID×10/φ⁴** and **ID ↔ RT×10/φ⁴**, so it reflects the chain about the gap between the GTI and the FPD. The Spheres of Dharma's polar cycle gave new stations (the OG, the Hecatodihedron); UP's does not, because UP is self-polar. New shapes from reciprocation come only from other seeds, such as the OG's open family (above).

## The OG's outward family (DICTO: "the upward shapes", 2026-10-19, float)

The UP step applied outward from the OG (`stepper.nxt`):

| Step | Corners | Faces | Notes |
|---|---|---|---|
| 1 | 92 | **30 rhombi + 60 kites** (90 quadrilaterals, 2 shapes) | not the rhombic enneacontahedron, which has 90 rhombi |
| 2 | 180 | **12 regular pentagons + 20 regular hexagons + 60 hexagons** (92 faces) | the face counts of a Goldberg polyhedron GP(3,0) |
| 3 | 212 | 60 triangles + 120 pentagons | |
| 4 | 270 | 12 decagons + 20 hexagons + 120 pentagons | very round: corner radii within 0.56% |
| 5–14 | 452 → 12,009 | more and more face kinds | |

**Names (DICTO 2026-10-19):** step 1 **DICTO KRE** (Kite-Rhombic Enneacontahedron), step 2 **DICTO PHE** (Pentagon-Hexagon Enneacontadihedron), step 3 **DICTO TPP** (Triangle-Pentagon Polyhedron), step 4 **DICTO DPHP** (Decagon-Pentagon-Hexagon Polyhedron).

**Exact builds (`exact_upward.py`, `data/exact_upward.json`):** all four solids are proved exactly in ℚ(√5), with full icosahedral symmetry. OG → KRE (60 + 20 pieces), KRE → PHE (90) and PHE → TPP (92) fill exactly. **But DICTO DPHP does not contain DICTO TPP: 60 of TPP's 212 corners stand outside DPHP, by up to 0.0185** (the same happens again at step 5 → 6, with 132 corners). The UP rule makes each new face go through a corner at right angles to it, but when a solid's corners lie at several radii and close together in direction, a neighbouring corner can lie beyond that face. **So the OG family nests as shells only as far as TPP: OG ⊂ KRE ⊂ PHE ⊂ TPP.** DPHP is still a valid solid of the rule, but not a shell round TPP. The UP cycle is not affected (its exact checks prove each solid inside the next).

**Unlike UP, the family does not keep growing.** The volume levels off near 27.9 and the corner radii near 1.87–1.90, so it rounds towards a nearly spherical limit (still about 1.5% out of round at step 14) instead of cycling. From about step 7 on, near-duplicate corners make float unreliable, so only steps 1–4 are clean shapes to study. Prior art and names are still to do.

## Open

- **Rhythms (DICTO):** layers that overlap at different rhythms may cause local, shallower UO structures. The five-fold and three-fold columns already advance in different steps (for example, RT corners at 1.902 and √3), so where they interleave, look for thin local octet-like layers.
- **Pyramids as a constant:** triangles hold at every stage. Pyramids appear at stages 1 and 3 and in the hexagonal stage, but not as separate pieces in stage 2 (the twisted frusta, which join pyramids into Vajras) or stage 4 (the rhombus pieces). Check whether those pieces are best seen as pyramids joined together.

- An exact proof of each stage: every remainder exactly 0.
- The hexagonal Cleo pieces: from the OG hexagon inward, and outward to the RT's three-fold corner (√3).
- RT star faces, i.e. stellations (DICTO): the app's Stellations family has face-attach pieces for the RT, so play first.
- Which pieces appear twice: compare the stage pieces with the Cleo star's pieces and with AXE, CLEO and FUJI.
- Prior art: check the library before any claim, especially the RT stellations (Messer) and the frustum/antiprism pieces.

Related: `studies/2026-10-18-kit-projects/SCOPE.md` (bipyramid-only octet, not pursued), #34/#35 golden cycle, #37 octet truss.
