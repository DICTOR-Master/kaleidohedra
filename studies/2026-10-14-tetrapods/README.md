# Tetrapods (DICTO, 2026-10-14): first pass

DICTO's group: shapes that close exactly **four meeting at a point**, or **four round one**; near misses noted. Every Polyhedraverse
shape (378). DICTO's two examples: rhombic dodecahedra (four at a point) and truncated octahedra (four round one).
`scripts/tetrapods.py` → `tetrapods.json` (run on dicto-node).

## Four meeting at a point: 38 exact

A corner of solid angle exactly π. For a three-faced corner this is enough (a spherical triangle with angle sum 2π tiles the sphere
four times by half-turns, the pattern of a disphenoid). Found with three-faced corners, among others: **rhombic dodecahedron** (its
three-fold corners), **truncated octahedron** (every corner), golden and other rhombohedra, the elongated dodecahedra (regular-hexagon,
Bain, DICTO skewed), the Bain RD, leaning square and hexagonal prisms, RD-Hemi, the RD and hexagonal-prism target cells, the Spheroid-13
RD pieces. With **five-faced** corners of solid angle exactly π, still to be checked as four-fold fits: the rhombic triacontahedron,
the rhombic icosahedron, the dodecahedron's flat stellation; four-faced: J65, two RD targets. Near misses within 3%: J87 (−2.83%),
pentagonal icositetrahedron (+2.91%), the golden-rhombus-to-U-hex adaptor (+1.52%), two hexagonal-prism targets (+1.61%).

## Four round one: what counts is still open

A centre with four congruent faces in tetrahedral positions (tetrahedron, octahedron, icosahedron, cuboctahedron, truncated tetrahedron,
truncated octahedron, ...) and another shape on all four. 2,378 combinations fit without overlap, too many to mean anything; 22 close
up (neighbouring outer pieces share a face), e.g. the tetrahedron with four rhombicuboctahedra or four square cupolas. DICTO's
truncated octahedra (a TO with TOs on its four tetrahedral hexagons) fit, but the four outer TOs do not touch: what makes them special
is that the cluster is part of a space filling (the bitruncated cubic honeycomb). So the rule for "four round one" needs DICTO's choice:
fit only, outer pieces touching, or part of a space filling.

## Four round one: DICTO's rule, part of a space filling (2026-10-14)

A centre with four pieces on four tetrahedrally placed faces counts when the five are part of a space filling. From the classical
honeycombs, all eight also found by the search as clean fits (`four-round-one-space-filling.json`):

| Honeycomb | Centre | Four pieces |
|---|---|---|
| alternated cubic (the octet) | tetrahedron | octahedra, on all four faces |
| alternated cubic (the octet) | octahedron | tetrahedra, on four alternate faces |
| quarter cubic | truncated tetrahedron | tetrahedra, on its four triangles |
| quarter cubic | truncated tetrahedron | truncated tetrahedra, on its four hexagons |
| quarter cubic | tetrahedron | truncated tetrahedra, on all four faces |
| bitruncated cubic | truncated octahedron | truncated octahedra, on four alternate hexagons (**DICTO's five TOs**) |
| rectified cubic | cuboctahedron | octahedra, on four alternate triangles |
| rectified cubic | octahedron | cuboctahedra, on four alternate faces |

And DICTO's own: the **Golden Breathing Pyrochlore** keeps the quarter-cubic pattern for every breathing ratio (a big tetrahedron
with four truncated tetrahedra round it, a truncated tetrahedron with four tetrahedra on its triangles), so it gives a whole
one-parameter family of four-round-one tetrapods. The four at a point list above (38) is already a space-filling property for the
lattice fillers among them (rhombic dodecahedron, truncated octahedron, rhombohedra, the elongated dodecahedra, the prisms).

## One polyhedron only (DICTO 2026-10-14: "same polyhedron, that's why I gave you two examples")

Both types use copies of a single shape, and the copies are part of its own space filling.

- **Four round one** (four copies on four tetrahedrally placed faces of a fifth): among the lattice space-fillers (parallelohedra), the
  copy across each face is a translate, so the five sit in the shape's own tiling (`scripts/same_shape.py`, checked: translates fit,
  no overlaps). In the group: the **truncated octahedron** (four alternate hexagons, DICTO's example). The Bain RD and the elongated
  dodecahedra (Bain, regular-hexagon) also qualify but are RD family and left out (DICTO: "don't fill it with RDs"). The rhombic
  dodecahedron, cube, hexagonal prism and the classic elongated dodecahedron have no four faces in tetrahedral positions. The truncated
  tetrahedron is ruled out under this rule (its tiling needs tetrahedra too).
- **Four meeting at a point** (corners of solid angle π), the group without filling it with rhombic dodecahedra (DICTO: "don't fill it
  with RDs"): one **rhombic dodecahedron** (DICTO's example), the **truncated octahedron** and the **leaning square and hexagonal
  prisms**. Left out as RD family: the elongated dodecahedra (elongated RDs: classic, regular-hexagon, Bain, DICTO skewed), the
  rhombohedron (the RD's quarter), the Bain RD, RD-Hemi, the RD target cells, the Spheroid-13 RD pieces and the octahedron's flat
  stellation (an RD). Next: test non-RD space-fillers outside the library (triakis truncated tetrahedron, gyrobifastigium, ...).
- The **truncated octahedron is in both types**: four meet at each of its corners, and four sit round it on alternate hexagons.

DICTO · dictospheres.com

## New shapes for the group (2026-10-14, `scripts/new_shapes.py` → `new/`)

DICTO asked for shapes made for the group rather than more rhombic dodecahedra. Two, both one polyhedron in its own space filling,
and both turn out to be **in both types**, as the truncated octahedron is:

**1. The diamond cell** (`new/diamond-cell.json`): the Voronoi cell of the diamond pattern, where every point has four nearest
neighbours in tetrahedral directions. 16 faces (4 hexagons, 12 triangles), 16 corners, volume 8 at diamond cube 4 (checked = 4³/8).
- *Four round one:* its four hexagons face the four bonds exactly; the cell across each is the same cell turned (the diamond's other
  half), so the five are part of the diamond tiling. Picture `renders/dia5.jpg`.
- *Four at a point:* at its four three-faced corners exactly four cells meet (at the other twelve corners, six meet). `renders/dia4.jpg`.
- Prior art: this cell is classical (the triakis truncated tetrahedron; its tiling is the diamond's Voronoi tiling, e.g. Conway,
  Burgiel and Goodman-Strauss, *The Symmetries of Things*, 2008). New here is only its place in DICTO's group.

**2. The keyed truncated octahedron** (`new/keyed-to.json`, shown with pyramid height h = 0.5): the truncated octahedron with a
hexagonal pyramid pushed **out** on four alternate hexagons and the same pyramid pressed **in** on the other four. 54 faces (6 squares,
48 triangles), 32 corners, volume unchanged.
- It still tiles by translation: across each bump hexagon the neighbour shows a dent, which takes the bump. Checked by sampling 3,000
  points per height: every point covered exactly once (no gaps, no overlaps) for h = 0.25, 0.4, 0.5 and 0.6.
- *Four round one:* the four neighbours across the bumps, each keyed in. `renders/key1.jpg` (alone), `renders/key5.jpg` (five).
- *Four at a point:* at each of its 24 truncated-octahedron corners exactly four cells meet (the 8 pyramid apexes are where two meet).
  `renders/key4.jpg`.
- Unlike the plain truncated octahedron, the keys fix which way each neighbour sits: the five cannot slide apart along a hexagon.
- A DICTO design study shape; we have not yet searched the literature for it, and DICTO chooses the name and the pyramid height.

## DICTO's choice: the five-TO piece (2026-10-14)

DICTO preferred neither new shape: "four TOs attached to a fifth would be much better". So the piece is **five truncated octahedra
fused**, four on four alternate hexagons of the fifth (`new/to.json` for the cell; `renders/five.jpg`).

- **It fills space by itself, every copy parallel** (plain translates, no turning or mirroring). Proof: the truncated octahedra of
  their space filling sit on the bcc lattice, generated by b1 = (1,1,1), b2 = (1,−1,−1), b3 = (−1,1,−1), with b4 = (−1,−1,1) =
  −(b1+b2+b3). Label each cell n1 b1 + n2 b2 + n3 b3 with n1 + 2 n2 + 3 n3 mod 5. The five cells of a piece (0, b1, b2, b3, b4) carry
  the labels 0, 1, 2, 3, 4, one of each, so the pieces placed on the cells labelled 0 cover every cell exactly once. Checked on 91
  cells: each covered once, none twice, none missing.
- The copies sit on a lattice of their own, of five times the volume; the nearest are 2 apart (along an axis) and √11 apart.
- Each piece touches 22 others (`renders/fivefill.jpg`: one piece gold, four neighbours pulled slightly apart).
- At a truncated-octahedron corner, four cells still meet, but from three pieces (two of the four belong to the same piece).
- Literature: not yet searched for this piece.

## DICTO's pair: and four standard RDs sharing a central corner (2026-10-14)

The four-at-a-point partner of the five-TO piece: **four rhombic dodecahedra** round one of their three-fold corners, fused into
one piece (`new/rd.json`; `renders/rd4.jpg`). Each pair of the four shares a face, and the four seams meet at the central corner
(all four centres √3/2 from it, at RD edge √3/2).

- **It fills space by itself, every copy parallel.** The RDs of their space filling sit on the fcc lattice, generated by a1 = (1,1,0),
  a2 = (1,0,1), a3 = (0,1,1). Label each cell n1 a1 + n2 a2 + n3 a3 with n1 + 2 n2 + 3 n3 mod 4: the four cells of a piece (0, a1,
  a2, a3) carry 0, 1, 2, 3, so pieces on the cells labelled 0 cover every cell once. Checked on 63 cells: each covered once.
- The copies sit on a lattice of four times the volume; the nearest are 2 apart, along the axes.

So DICTO's two examples are both single space-filling pieces: **five truncated octahedra** (four round one) and **four rhombic
dodecahedra** (four at a point).
