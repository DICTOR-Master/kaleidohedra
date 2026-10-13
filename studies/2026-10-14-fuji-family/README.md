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

## Next

1. Done: the STT's faces are FUJI(1/2)'s base (above).
2. Done: FUJI's base is Odom's golden hexagon (above).
3. Which FUJI(r) close gaps with which solids (r = 1/2 shares FUJI's α)? Where do flat-ended triangles appear in DICTO's
   cuboctahedral (FCC) work?

The family's name is DICTO's to choose ("FUJI family" is a working label).

DICTO · dictospheres.com
