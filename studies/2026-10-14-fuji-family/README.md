# The FUJI family (study, DICTO, 2026-10-14)

Reading and checking, no app changes. DICTO's question (2026-10-14): FUJI keeps turning up when we are looking for something
else (his cuboctahedron spheres, the Lotus seed's surface, Bodhi kit B's FUJI-like B4). Could its shape found a new family?

## The family

Take a **flat-ended triangle** (DICTO's term: an equiangular hexagon, all angles 120°, sides 1 and r alternating, 0 ≤ r ≤ 1) and
put an apex over its centre with all six side edges of length 1. Call it **FUJI(r)**. Data: `family.json`, from
`scripts/family.py`; every check passes, and FUJI(1/φ) matches the Icosa-13 study's FUJI edge for edge.

- The base is cyclic: circumradius² = (1 + r + r²)/3, so **height² = (2 − r − r²)/3** and the volume is
  (√3/12)(1 + 4r + r²) · height.
- Its six side faces are **three equilateral triangles** (on the long sides) and **three isosceles triangles** (1, 1, r) with apex
  angle 2 arcsin(r/2).

| r | member | height | base angle, long side | base angle, short side | note |
|---|---|---|---|---|---|
| 0 | regular tetrahedron | √(2/3) | 70.53° | | the sharp triangle |
| 1/4 | | **3/4** | **60°** exactly | 49.11° | rational height |
| 1/2 | | 0.6455 | 48.19° = 90° − α | **α = 41.81°** exactly | the icosahedral angle again |
| 1/φ | **FUJI** | **1/√3** | **α = 41.81°** | δ = 37.38° | isosceles faces are **golden triangles** (36°) |
| 1 | flat | 0 | | | the regular hexagon: six equilateral triangles lie flat |

(α = arccos(√5/3), the gap two icosahedra leave either side of a shared edge. The r = 1/2 and r = 1/φ angles agree with α to 40
digits; a reason for the r = 1/2 coincidence has not been found.)

**What this explains.** DICTO hoped for sharp equilateral triangles in his cuboctahedron spheres and, when colouring the Lotus
seed, for regular hexagons. The family runs between exactly those two shapes: the sharp triangle gives the tetrahedron, and the
regular hexagon gives a pyramid of zero height. Every shape in between is a flat-ended triangle, and FUJI is the member whose side
faces are the golden triangles of icosahedral geometry.

## Where the shape turns up in DICTO's work

- His cuboctahedron spheres: sharp equilateral triangles wanted round the ports, blunt flat-ended ones made.
- The Lotus seed's surface: the 20 FUJI bases, where he hoped for regular hexagons.
- Bodhi kit B: the FUJI-like B4 in each outer three-fold corner.
- **All his DeltaZips and B1NR sculptures use rounded equilateral triangles** (DICTO, 2026-10-14): the curved form of the same
  idea, a triangle whose corners are taken off. The flat-ended triangle is its straight-edged version; how far the corners are
  cut (r) is what the family measures. First estimate from DICTO's figures (2026-10-14: about 2.5 cm of straight run
  between the ties on a side, about 3 cm corner to corner): each corner takes about 0.25 cm off each side, so r is about 0.1, near
  the sharp-triangle end. To be measured properly.
- **The recycling symbol** (DICTO, 2026-10-14): the three chasing arrows outline a triangle with blunted corners, in the same
  general range; it is the centre of DICTO's DeltaZips logo.

## Reading (2026-10-14)

- **DICTO's reference library:** nothing on equal-edged hexagonal pyramids or flat-ended triangle faces.
- **Not found** as a named solid in web searches; Hart's pyramid pages list only regular-faced pyramids (three).
- **The Mosseri–Sadoc composite tiles z, h, s, a are not FUJI:** their faces are golden triangles only (Papadopolos and
  Ogievetsky 1999, §4), while FUJI has three equilateral faces and a hexagon. Consistent with the Icosa-13 proof that FUJI is not a
  union of Mosseri–Sadoc tiles at its own scale or larger.
- **Flat-ended triangles that fill space (read 2026-10-14):** Damasceno, Engel and Glotzer (2012) study truncated tetrahedra from
  the tetrahedron (t = 0) to the octahedron (t = 1); the hexagons have sides σ(1 − t) and σt/2, so r = (t/2)/(1 − t) for
  t ≤ 2/3. At **t = 1/2** the solid fills space on its own (their "space-filling truncated tetrahedron", STT; centroids on β-tin,
  space group I4₁/amd), and they note the hexagons' 2:1 edge ratio. **So the STT's four hexagons are exactly FUJI(1/2)'s base**,
  the same member where the icosahedral angle α reappears. Checked from their Table S1 vertices: hexagons with sides 1 and 1/2 at
  distance 1/√6 from the centre (long side 1). FUJI(1/2) pyramids sit face to face on the STT's hexagons, but nothing is flush
  there (151.28° and 166.92° across the edges), so the augmented solid is not obviously special.
- **The same family runs through the whole tetrahedron-to-octahedron range:** t = 2/3 is the Archimedean truncated tetrahedron
  (r = 1, regular hexagons), and past it the hexagons become flat-ended triangles again on the octahedron side, which is the
  tetrahedral-octahedral (FCC, cuboctahedral) world of DICTO's spheres. FUJI's own ratio 1/φ occurs at t = 2/(φ + 2) = 0.5528
  (tetrahedron side) and at t = 2φ/(2φ + 1) = 0.7639 (octahedron side).
- **Odom's construction makes the whole family (read and checked 2026-10-14):** the Wolfram Demonstration "Hexagons and the
  Golden Ratio" (after George Odom's golden ratio in the equilateral triangle) extends each side of an equilateral triangle beyond
  both ends; with the extension in the golden ratio the six outer points make a hexagon with two edge lengths in the golden ratio,
  and two triangles among its corners belong to the compounds of two icosahedra and of five octahedra. Rebuilt here: extending
  side 1 by e at both ends always gives an **equiangular** hexagon (all 120°) with sides e and 1 + e, i.e. a flat-ended triangle
  with **r = e/(1 + e)**. So e = φ gives **FUJI's base exactly** (sides φ and φ²), e = 1 gives the space-filler's r = 1/2, and
  e = 1/φ gives r = 1/φ². Every member of the family is an Odom hexagon.

## Which FUJI(r) close gaps (checked 2026-10-14)

In the Lotus seed FUJI's base lies in one plane with the three icosahedron triangles on its long sides (41.81° + 138.19° = 180°).
The same test for other solids with unit triangles (`scripts/gaps.py`, `gaps.json`): FUJI(r) continues the plane of solid X's
triangles when its base angle on the long sides plus X's dihedral there is 180°.

| Solid (dihedral at the triangle's edge) | r | exact |
|---|---|---|
| icosahedron, pentagonal antiprism (138.19°) | 0.618034 | **1/φ: FUJI** |
| cuboctahedron, triangle-square (125.26°) | 0.366025 | **(√3 − 1)/2**; base angle the 'magic angle' arctan √2 = 54.74° |
| square antiprism, triangle-triangle (127.55°) | 0.414214 | **√2 − 1** (the silver ratio's inverse) |
| rhombicuboctahedron, triangle-square (144.74°) | 0.724745 | **(√6 − 1)/2**; base angle arctan(1/√2) = 35.26° |
| icosidodecahedron, triangle-pentagon (142.62°) | 0.691982 | base angle = δ, FUJI's own short-side angle |
| snub cube, snub dodecahedron, rhombicosidodecahedron | 0.70–0.94 | no closed form looked for |
| tetrahedron, octahedron, truncated tetrahedron, prisms | none | the octahedron gives r = 0, the tetrahedron itself |

**The antiprism pattern** (`scripts/antiprisms.py`): for the n-gonal antiprism with unit edges, **r = 2 cos(π/n) − 1**, checked to
10⁻¹² for n = 4 to 12, with n = 3 (the octahedron) giving r = 0. So the family is indexed by the antiprisms: the tetrahedron
(n = 3), √2 − 1 (n = 4), **FUJI (n = 5, golden)**, √3 − 1 (n = 6), and r → 1 as n grows (the flat regular hexagon). **Proved** in `PROOFS.md` (2026-10-14), with
the base-angle formulas cos L = (1 + 2r)/3 and cos² S = (2 + r)/(3(2 − r)), which also explain the r = 1/2 coincidence.

These are face-plane matches only: a full closure like the Lotus seed also needs the other gaps filled. The cuboctahedral member
(√3 − 1)/2 is the one to test first against DICTO's cuboctahedron spheres.

## Cuboctahedral closure, first test (2026-10-14)

The direct analogue of DICTO's 63-piece build, a unit cube with a unit cuboctahedron on each face (`scripts/cubo_closure.py`,
`cubo-closure.json`), does **not** close: no overlaps, but the hull (26 faces) is 40% gap, and the corner pocket (about 0.47) is not
FUJI((√3 − 1)/2) (0.265). The cuboctahedra are too large for the cube; the Lotus seed works because each J11 hides a cap inside the
dodecahedron. **DESHI-style test** (`scripts/cubo_deshi.py`, `cubo-deshi.json`): 12 unit cuboctahedra on the central one's 12 vertex axes,
parallel, slid in. Unlike icosahedra, they never come to share edges: first contact is at distance 2, **one shared corner** per
neighbouring pair and with the centre, and sliding further makes them overlap. The cluster is then the vertex-to-vertex cluster:
its hull is the cuboctahedron 3 times larger (14 faces, the three-fold face a triangle of side 3) and the **fill is exactly 13/27**,
the same as the icosahedral vertex-to-vertex cluster in the Icosa-13 study (there proved by hull = 3 × the solid). No FUJI-type
pocket appears. So the cuboctahedral member does not come from a parallel cage; where it does occur (DICTO's dictospheres, the
face-plane match with the cuboctahedron) is still to be explained, and turned or face-axis cages are the next candidates.

**How the dictosphere triangles came about (DICTO, 2026-10-14):** a cuboctahedral arrangement on a sphere with a PET-bottle
port in every square and every triangle. The squares should be much bigger than the triangles; with ports in both, the
triangles' corners came too close to the edges of the neighbouring holes, so the triangles were truncated to give even space round
the ports. So r was set by port clearance, not by angles.

**DICTO's dictospheres (2026-10-14, first figures):** flat-ended triangles with long sides about 4 cm and short sides about 1.5 cm,
r ≈ 0.375, within 3% of the cuboctahedral member (√3 − 1)/2 = 0.366. The 5 cm was measured across the inside of the face (DICTO), and it fits: across a flat-ended triangle with sides 4 and 1.5,
from a short side to the opposite long side, is (4 + 2 × 1.5) × √3/2 − 1.5 × √3/2 = 4.76 cm.

## The dictosphere explained (2026-10-14)

DICTO's description: 6 squares and 8 truncated triangles, the triangles meeting **short side to short side**, a 3 cm port in every
face, sphere about 7.5 cm across. That is the cube ∩ octahedron family between the truncated octahedron and the cuboctahedron:
|x|, |y|, |z| ≤ 1 and |x| + |y| + |z| ≤ s, with hexagon sides √2(s − 1) against the squares and √2(2 − s) against each other.
(`scripts/dictosphere.py`, `dictosphere.json`.)

- **Even space round the ports forces the sphere.** Across an edge shared by two faces, the clearances from the two face centres
  to the edge are equal exactly when the two face planes are the same distance from the centre (feet of the perpendiculars from
  the centre: t₁ = (d₂ − d₁ cos θ)/sin θ, t₂ = (d₁ − d₂ cos θ)/sin θ). So even space across every square–triangle edge means all
  14 faces touch one sphere: **s = √3**, and then **r = (√3 − 1)/2 = 0.366**, the cuboctahedral FUJI member.
- **Against DICTO's measurements:** with long sides of 4 cm, the model gives short sides of **1.46 cm** (measured 1.5), an inscribed
  sphere **7.73 cm** across (sphere about 7.5) and measured r = 0.375 against 0.366 (s = 1.727 against √3 = 1.732).
- **Ports of 3 cm diameter:** clearance **0.50 cm** from each square's port to its sides and **0.50 cm** from each triangle's port to
  its long sides (equal, as above), and 1.23 cm to the short sides, where the triangles meet each other.

**Port gaps (DICTO, rim to rim):** 3 cm triangle to triangle, 4 cm square to square. Straight across, the model's centre-to-centre
distances are 4.46 and 5.46 cm: they differ by exactly 1.00 cm, as DICTO's gaps do, which fixes the inscribed sphere at
ρ = 1/(1.4142 − 1.1547) = 3.86 cm, the same value the 4 cm long side gave. Subtracting, the holes would be about 1.46 cm across,
against the 3 cm port size given; to be checked (hole diameter vs bottle collar).

**Across the sphere (DICTO):** 8.4 cm between opposite flat port faces; and, along the surface with a steel tape, 8.4 cm
between the centres of two triangles on either side of a square (an arc of 109.47°), which gives a sphere of radius
4.40 cm, 8.8 cm across, in line with DICTO's 'a few mm wider' than 8.4. Equal depth holds by construction (DICTO): it is a sphere, and every port
has the same flat round it, so every flat sits at the same depth; and the true sphere a few mm wider. So the dictosphere is
a sphere with shallow flats, not the sharp solid (whose corners would stand 24% further out). On the sphere, even spacing means
each point of the surface belongs to its nearest port: the spherical Voronoi diagram of the 14 port centres, which is the
equal-depth solid projected onto the sphere. Its edges along the surface have ratio **0.356** (short/long), against 0.366 for the
flat faces and 0.375 measured: all within a few per cent, closer than hand measurement on a curved surface can separate.

So DICTO's working rule, even space round every port, fixes the shape exactly: the cube–octahedron solid with an inscribed sphere,
whose triangles are the flat-ended triangles of the cuboctahedral member. (It is also the Wulff shape of a cubic crystal whose
{100} and {111} surfaces have equal energy, since the Wulff construction puts the planes at distances proportional to the
energies.) Why the same r also makes FUJI(r)'s base continue the cuboctahedron's face planes is not yet explained.

## Does a blunted icosahedron fill space? (DICTO, 2026-10-14)

An icosahedron with its triangles blunted into flat-ended triangles is the icosahedron cut by the dodecahedron's planes: 20
flat-ended triangles and 12 pentagons (from the icosahedron to the icosidodecahedron). However deep the cut, it has only two
dihedral angles, because the face directions never change: 138.19° (triangle to triangle, the icosahedron's) and 142.62°
(triangle to pentagon, the icosidodecahedron's). **No member fills space on its own:** round any edge of a tiling the angles of
the tiles meeting there add to 360° (or to 180° where the edge lies on another tile's face), and with every angle between 138° and
143°, one is too few and two or three never make 180° or 360° (276°–285° and 414°–428°). The same argument rules out the plain
icosahedron. Filling space needs partner pieces, as in the Lotus seed, the Sunstar and the Spheres of Dharma.

By contrast the dictosphere's solid has angles 109.47° and 125.26°, and 109.47° + 2 × 125.26° = 360°: the angle condition for
filling space holds there (as for the truncated octahedron, which does fill space); whether its other proportions allow it is
not checked. **DICTO (2026-10-14): the dictospheres form rhombic dodecahedra, joined always triangle port to triangle port.** That is exactly
how the rhombic dodecahedron is built: all 24 of its edges run along the three-fold (body-diagonal) directions, which are the
triangle-port directions, e.g. from the corner (1, 1, 1) to the corner (2, 0, 0) along (1, −1, −1). So with a dictosphere at
each corner and a bottle along each edge, every bottle enters both spheres through triangle ports. In the space-filling packing of
rhombic dodecahedra each node is either a meeting of 4 edges (using 4 of the 8 triangle ports, a tetrahedral set) or of 8 edges
(using all 8). The square ports (on the cube axes) are not on any edge. (An earlier note here said square to triangle; corrected
by DICTO.)

## Does the dictosphere solid tile space? (2026-10-14)

The sphere itself leaves gaps (DICTO); the question is the flat-faced solid (cube ∩ octahedron with an inscribed sphere).

- **Not by translations.** A convex solid that fills space with translated copies must have centrally symmetric faces (Minkowski;
  Venkov; McMullen). The solid is centrally symmetric, but its flat-ended triangles are not (opposite sides 1.035 and 0.379). And
  because the solid has full cubic symmetry, every copy in the same orientation is a translate, so any tiling would need copies
  turned to other orientations.
- **The edge test passes only one way:** 109.47° + 125.26° + 125.26° = 360°, so along every edge of a tiling there would be one
  triangle–triangle edge and two triangle–square edges. Those edges have lengths 0.379 and 1.035, in the irrational ratio 1 + √3,
  so along any finite line of edges the two kinds cannot end together. This points strongly against a tiling, but a full proof
  for mixed orientations and endless edge lines has not been written.
- What does fill space is the **rhombic dodecahedron frame** the dictospheres build (above): the spheres are the nodes, the
  bottles the edges, and the cells are rhombic dodecahedra.

## Turned cuboctahedral cages (2026-10-14)

`scripts/cubo_cages.py` (run on dicto-node), `cubo-cages.json`: unit cuboctahedra on the 12 corner, 6 square or 8 triangle axes of
a central one, parallel or turned about their own axis (90°, 45°, 60°), slid in until they touch.

| Axes | Turned | Neighbours touch at | Centre that fits | Fill of hull | Flat-ended hull faces |
|---|---|---|---|---|---|
| 12 corner | no | one corner | 1 | 13/27 | none |
| 12 corner | 90° | one corner | 0.914 | 0.468 | none |
| 6 square | no | one corner | 1 | 0.574 | none |
| 6 square | 45° | a whole edge | 0.707 | 0.593 | none |
| 8 triangle | no | **a whole square** | 0.5 | **0.864** | none |
| 8 triangle | 60° | one corner | 1 | 0.480 | none |

None makes flat-ended triangles. (The parallel triangle-axis cage is a piece of the cuboctahedron–octahedron honeycomb, where
cuboctahedra share squares.) So the cuboctahedral member's homes are the dictosphere (even spacing) and the face-plane match, not a
cage of whole cuboctahedra.

## FUJI's flat-ended triangles in pyrochlore networks (2026-10-14)

The pyrochlore network is corner-sharing tetrahedra; its (111) layers are kagome nets of triangles and hexagons, and the space
between the tetrahedra is filled by truncated tetrahedra (tetrahedra + truncated tetrahedra fill space). When the two sets of
tetrahedra have different sizes, edge a and edge b (the **breathing pyrochlore** lattice, found in real spinel oxides: Okamoto,
Nilsen, Attfield and Hiroi 2013, doi:10.1103/PhysRevLett.110.097203), every kagome hexagon has sides a and b alternating with all
angles 120° (checked: the walk a, b, a, b, a, b turning 60° closes): **a flat-ended triangle with r = b/a.** So the breathing
ratio of a breathing pyrochlore is exactly the FUJI-family parameter: r = 1 is the ordinary pyrochlore (regular hexagons),
r = 1/2 the space-filling truncated tetrahedron's faces, r = 1/φ FUJI's base. DICTO's Rhombiverse and Kaleidohedra Pyrochlore and
3D Kagome worlds are the regular case.

## And the truncated octahedron (2026-10-14)

The truncated octahedron is the middle member of the dictosphere's family (cube ∩ octahedron, s = 1.5): regular hexagons, r = 1.
On one side (s < 1.5, towards the octahedron) its hexagons become flat-ended triangles with the short sides against the squares;
on the other (s > 1.5, towards the cuboctahedron) with the long sides against the squares: the dictosphere is s = √3 there. All
members have the same angles (109.47°, 125.26°), but by Minkowski's theorem only the truncated octahedron, whose hexagons are
centrally symmetric, fills space by translation (Kelvin's cell, the body-centred cubic packing's cell). So the truncated
octahedron is to the dictosphere what the regular hexagon is to FUJI: the symmetric r = 1 end that DICTO hoped for.

## Literature search on the family (2026-10-14)

- **The shape of the base** is the isogonal hexagon, also written t{3}, the truncated triangle (an equiangular hexagon with
  alternating long and short sides; Wikipedia, "Hexagon"). DICTO's word is the flat-ended triangle.
- **The pyramid FUJI(r)** (equal side edges on that hexagon): no source found that defines or studies it, as a family or as single
  members, in two extended searches and the reference library. Hart's pyramid pages list only the three regular-faced pyramids.
- **The antiprism angle** cos D = (1 − 4 cos(π/n))/3 is known: OEIS gives it for the heptagonal and nonagonal antiprisms (A394077 and
  neighbours). **The link r = 2 cos(π/n) − 1 to the pyramids was not found**: the part proved here (PROOFS.md) appears to be new.
- **Breathing pyrochlores** are known materials (Okamoto et al. 2013). Their breathing ratio is the family's r; one search summary
  quotes Yb–Yb spacings of 3.3 Å and 6.2 Å for Ba₃Yb₂Zn₅O₁₁ (r ≈ 0.53, near the space-filler's 1/2; to verify in the papers:
  Rau et al. 2018, doi:10.1088/1361-648X/aae45a; Dissanayake et al. 2022, doi:10.1038/s41535-022-00488-w). The Cr spinels
  LiGaCr₄O₈ and LiInCr₄O₈ are close to r = 1. No golden (r = 1/φ) breathing pyrochlore was found.
- **Truncated triangular nanoplates** of silver and gold (truncated nanoprisms) are flat-ended triangles studied for their optics;
  no link to the pyramids or to particular ratios was found.
- Not found: equiangular-hexagon pyramids among icosahedral quasicrystal tiles (Kramer, Danzer, Mosseri–Sadoc); FUJI remains outside
  those tile sets (Icosa-13 study proofs).

So, as far as these searches reach: the base shape, the antiprism angles, the breathing pyrochlore and the space-filler are known;
the FUJI family of pyramids, its base-angle formulas, the antiprism theorem linking them, and the identifications that tie the
family together (FUJI, Odom's hexagon, the golden breathing pyrochlore, the dictosphere) were not found.

## What defines a member? (legitimacy, started 2026-10-14)

DICTO: be careful; find the parameters that define the family before building more.

- **Why the side edges are 1.** A pyramid with equal side edges on an equiangular hexagon (sides a and b alternating) has two free
  ratios, b/a and (side edge)/a. Asking for equilateral faces on the long sides fixes the second: side edge = a. (Equilateral
  faces on the short sides are impossible, since the circumradius exceeds b.) So FUJI(r) is the one-parameter family of
  equal-edged pyramids on flat-ended triangles whose long faces are equilateral, which is what lets them meet the triangle faces
  of deltahedra and Archimedean solids.
- **Natural members** are then the r where something closes: the face-plane condition r = (−3 cos D − 1)/2 for a solid with unit
  triangles (the antiprisms r = 2 cos(π/n) − 1, the cuboctahedron, the rhombicuboctahedron, …); a whole cluster closing (so far only
  FUJI, in the Lotus seed); a space-filling or crystal structure (r = 1/2, breathing pyrochlores).
- **The same construction on other polygons** (equiangular 2k-gons with sides 1 and r alternating, equal side edges, equilateral
  long faces): it exists for k = 3, 4 and 5 only, each family starting at a regular-faced pyramid and ending flat:
  k = 3 from the tetrahedron to r = 1 (FUJI's family); **k = 4 from the square pyramid J1 (half the octahedron) to r = 2 sin 15° =
  0.5176**; **k = 5 from the pentagonal pyramid J2 to r = 2 sin 6° = 0.2091**; for k ≥ 6 the long sides alone already lie flat. So the
  FUJI family is one of exactly three "flat-ended pyramid" families, matching the three regular-faced pyramids. To study.

## Next

1. Done: the STT's faces are FUJI(1/2)'s base (above).
2. Done: FUJI's base is Odom's golden hexagon (above).
3. Done in part (face-plane matches above); next a full closure test for the cuboctahedral member. Where do flat-ended triangles appear in DICTO's
   cuboctahedral (FCC) work?

The family's name is DICTO's to choose ("FUJI family" is a working label).

DICTO · dictospheres.com
