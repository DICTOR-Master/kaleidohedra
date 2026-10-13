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

## Reading (2026-10-14)

- **DICTO's reference library:** nothing on equal-edged hexagonal pyramids or flat-ended triangle faces.
- **Not found** as a named solid in web searches; Hart's pyramid pages list only regular-faced pyramids (three).
- **The Mosseri–Sadoc composite tiles z, h, s, a are not FUJI:** their faces are golden triangles only (Papadopolos and
  Ogievetsky 1999, §4), while FUJI has three equilateral faces and a hexagon. Consistent with the Icosa-13 proof that FUJI is not a
  union of Mosseri–Sadoc tiles at its own scale or larger.
- **Lead 1, flat-ended triangles that fill space:** the truncated tetrahedra between the tetrahedron and the octahedron have four
  flat-ended-triangle faces, and one of them fills space on its own, "a new space filling polyhedron, which has been overlooked in
  previous searches" (Damasceno, Engel and Glotzer 2012). Its r is to be read from the paper and checked.
- **Lead 2:** Wolfram Demonstration "Hexagons and the Golden Ratio": three equilateral triangles whose outer corners make a hexagon
  with two edge lengths in the golden ratio, linked to the compounds of two icosahedra and five octahedra. Close to FUJI's base and
  its three equilateral faces; page text not yet read.

## Next

1. Read Damasceno et al. for the space-filling member's r, and check whether FUJI(r) pyramids sit on its faces.
2. Read the Wolfram demonstration; compare its hexagon with FUJI's base.
3. Which FUJI(r) close gaps with which solids (r = 1/2 shares FUJI's α)? Where do flat-ended triangles appear in DICTO's
   cuboctahedral (FCC) work?

The family's name is DICTO's to choose ("FUJI family" is a working label).

DICTO · dictospheres.com
