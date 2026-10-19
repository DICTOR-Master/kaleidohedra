# DICTO's five-fold octet: growing outward from the Cleo star (2026-10-19)

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

## Open

- An exact proof of each stage: every remainder exactly 0.
- The hexagonal Cleo pieces: from the OG hexagon inward, and outward to the RT's three-fold corner (√3).
- RT star faces, i.e. stellations (DICTO): the app's Stellations family has face-attach pieces for the RT, so play first.
- Which pieces appear twice: compare the stage pieces with the Cleo star's pieces and with AXE, CLEO and FUJI.
- Prior art: check the library before any claim, especially the RT stellations (Messer) and the frustum/antiprism pieces.

Related: `studies/2026-10-18-kit-projects/SCOPE.md` (bipyramid-only octet, not pursued), #34/#35 golden cycle, #37 octet truss.
