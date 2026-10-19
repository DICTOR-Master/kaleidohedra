# Universal PiTet: growing outward from the Cleo star (2026-10-19)

**Name (DICTO 2026-10-19): "Universal PiTet"**, after the triangles and pyramids that stay constant. DICTO: "even if pyramids don't hold, Pi does": the shells are a spherical progression (π) and the triangles stay throughout (Tet). The working name was "five-fold octet"; the folder keeps that name. Whether the name is already in use has not been checked yet.

DICTO's idea: build outward from the Cleo star in **spherical shells with the same pattern each time and different solids each time**. Multi-sided **Vajras** would take the place of the octet's octahedra, alongside different kinds of FUJI and CLEO, and some pieces may appear twice. This is a different construction from the Spheres of Dharma, even where it passes through the same solids. This came out of the play-first brainstorm (OG-13, spherical octet, ID channel).

**All numbers here are float checks** (`progression.py`, results in `data/progression.json`). No exact proof has been done yet.

Frame: an icosahedron of edge 1, with the five-fold axes through its corners. Every solid is built in this frame and checked against it.

**Known case:** D′ (radius φ²/√3) matches the app's Cleo star hull, `theaetetus-data.js`, view `cleostar`; the app data has 6 decimals.

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

## Triangles as the constant (DICTO 2026-10-19)

DICTO: "triangles are the only true constant in the universal octet". This holds for every stage built so far. Inside each shell, every face where two pieces meet is a triangle. Pentagons, hexagons and rhombi appear only on the shell surfaces (D′, ID, OG, RT). Read this way, the triangle is the invariant and the shell polygon is the variable, which fits both the flat octet and the 600-cell, where everything is triangles. This has been checked only on stages 1–3.

## Open

- **Rhythms (DICTO):** layers that overlap at different rhythms may cause local, shallower UO structures. The five-fold and three-fold columns already advance in different steps (for example, RT corners at 1.902 and √3), so where they interleave, look for thin local octet-like layers.
- **Pyramids as a constant:** triangles hold at every stage. Pyramids appear at stages 1 and 3 and in the hexagonal stage, but not as separate pieces in stage 2 (the twisted frusta, which join pyramids into Vajras) or stage 4 (the rhombus pieces). Check whether those pieces are best seen as pyramids joined together.

- An exact proof of each stage: every remainder exactly 0.
- The hexagonal Cleo pieces: from the OG hexagon inward, and outward to the RT's three-fold corner (√3).
- RT star faces, i.e. stellations (DICTO): the app's Stellations family has face-attach pieces for the RT, so play first.
- Which pieces appear twice: compare the stage pieces with the Cleo star's pieces and with AXE, CLEO and FUJI.
- Prior art: check the library before any claim, especially the RT stellations (Messer) and the frustum/antiprism pieces.

Related: `studies/2026-10-18-kit-projects/SCOPE.md` (bipyramid-only octet, not pursued), #34/#35 golden cycle, #37 octet truss.
