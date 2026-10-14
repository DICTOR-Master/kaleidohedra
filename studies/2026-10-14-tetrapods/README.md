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
